# 自建三节点代理架构：从设计到部署的完整方法论

> 面向 AI 智能体的网络通道设计 · 通用架构，适配任意云厂商和地域
>
> — GCat · 2026-06-22

---

## 〇、为什么你需要自己的通道

如果你在重度使用 AI 工具（Hermes Agent、Claude Code、Cursor、Windsurf 等），你很快会发现一个反直觉的事实：

**LLM API 本身通常不慢，慢的是它的「伴生请求」。**

一个典型的 AI 智能体任务产生的网络请求：

```
用户：「研究一下最新的 LoRA 微调方案并写个 README」
→ 调用 LLM API（直连可达）                    1 次
→ 搜索 Tavily / Google Search（被墙）         3-5 次
→ 抓取搜索结果页（被墙）                      3-8 次
→ 下载 HuggingFace 模型信息（被墙）           2-3 次
→ Git clone / push（被墙）                    1-2 次
→ 再调用 LLM API 撰写（直连可达）             3-5 次
```

十几到二十几次请求里，LLM API 全部直连可达，但一半以上的请求完全不可达。

**买机场不是答案**——机场没有分流能力，LLM API 也跟着绕路，白白增加延迟。你需要的是：一套自己掌控的、智能分流的通道。

这篇文档记录了一套经过半年实战验证的三节点代理架构，从设计理念到部署细节，包括 2026 年 xray-core v26.6 引入的后量子加密能力。

---

## 一、架构设计理念

### 1.1 核心原则

```
┌─────────────────────────────────────────────────────┐
│                                                    │
│   LLM API 直连（快）   被墙服务走中转（通）         │
│   海外出口独立（稳）   节点间全加密（安全）         │
│                                                    │
└─────────────────────────────────────────────────────┘
```

这四条决定了整个架构。不是「把流量全丢给海外节点」，而是在每个决策点做最优路由。

### 1.2 节点拓扑

```
                 ┌────────────────────────┐
                 │   ③ 海外出口节点       │
                 │   地域：HK/JP/SG/KR    │
                 │   职责：出墙 + 伪装     │
                 └───────────┬────────────┘
                             │ 加密隧道
                 ┌───────────▼────────────┐
                 │   ② 国内中转节点       │
                 │   地域：GZ/SH/BJ       │
                 │   职责：分流 + 托管     │
                 │  ┌──────┴──────┐       │
                 │  │ 直连通道    │ 中转  │
                 │  │ (全透传)   │ (分流) │
                 │  └──────┬─────┘       │
                 └─────────┼─────────────┘
                           │
                 ┌─────────▼─────────────┐
                 │   ① 本地开发机        │
                 │   Clash / xray 客户端  │
                 └───────────────────────┘
```

三个物理节点，四种逻辑通道。每个节点的选择都与你的实际需求相关，下面逐一展开。

---

## 二、节点设计与配置

### 2.1 国内中转节点

**角色：双重用途——网站托管 + 代理分流**

这是架构的枢纽。它在同一个 xray 实例上跑两条入站通道，出站根据目标智能选择走直连还是加密隧道。

```
入站:
  :PORT_A  VLESS+WS    直连通道    全流量 → freedom
  :PORT_B  VLESS+WS    中转通道    GEOIP:CN → freedom
                                   其余 → 加密隧道 → 海外节点

出站:
  → 海外节点   VLESS + REALITY + PQ加密
  → 国内       freedom
```

**为什么要两条入站？**

直连通道是为特殊场景准备的：你在酒店/公司/受限网络下，需要一条纯粹的中转线路访问国内内容。它不做分流判断，全流量走 freedom——相当于把中转节点当跳板。

中转通道是日常主力：GEOIP/GEOsite 判断目标是否在国内，国内直连，其余走海外。这也是 Clash 订阅中默认推荐的通道。

**配置示例（xray-core v26.6+）：**

```json
{
  "inbounds": [
    {
      "tag": "direct-channel",
      "port": <直连端口>,
      "protocol": "vless",
      "settings": {
        "clients": [{"id": "<UUID>"}],
        "decryption": "none"
      },
      "streamSettings": {
        "network": "ws",
        "wsSettings": {"path": "/<直连路径>"}
      }
    },
    {
      "tag": "relay-channel",
      "port": <中转端口>,
      "protocol": "vless",
      "settings": {
        "clients": [{"id": "<UUID>"}],
        "decryption": "none"
      },
      "streamSettings": {
        "network": "ws",
        "wsSettings": {"path": "/<中转路径>"}
      }
    }
  ],
  "outbounds": [
    {
      "tag": "overseas",
      "protocol": "vless",
      "settings": {
        "vnext": [{
          "address": "<海外节点域名>",
          "port": <海外端口>,
          "users": [{"id": "<UUID>", "flow": "xtls-rprx-vision", "encryption": "none"}]
        }],
        "encryption": "native"
      },
      "streamSettings": {
        "network": "tcp",
        "security": "reality",
        "realitySettings": {
          "serverName": "<海外节点域名>",
          "fingerprint": "chrome",
          "publicKey": "<REALITY公钥>",
          "shortId": "<shortId>"
        }
      }
    },
    {"tag": "direct", "protocol": "freedom"}
  ],
  "routing": {
    "domainStrategy": "AsIs",
    "rules": [
      {"type": "field", "inboundTag": ["direct-channel"], "outboundTag": "direct"},
      {"type": "field", "outboundTag": "direct", "ip": ["geoip:private", "geoip:cn"]},
      {"type": "field", "outboundTag": "direct", "domain": ["geosite:cn", "domain:<海外节点域名>"]},
      {"type": "field", "outboundTag": "overseas", "network": "tcp,udp"}
    ]
  }
}
```

**关键点**：
- `"encryption": "native"` 在出站的 `settings` 级别（非 users 内）——这是 v26.6 的 VLESS 后量子加密
- 路由规则中第一条是 `inboundTag` 匹配——直连通道的流量绕过所有分流规则，直接 freedom
- `domain:<海外节点域名>` 放在直连规则中，防止路由环路

### 2.2 海外出口节点

**角色：单一职责——REALITY 出墙 + 域名伪装**

```
入站:
  :PORT  VLESS + REALITY + PQ加密

回落:
  非 VLESS 握手 → nginx :443 → 伪装网站

出站:
  freedom
```

**REALITY 伪装机制（重要）：**

这不是简单的端口转发。REALITY 在 TLS 层做「偷天换日」——

1. 客户端发起 TLS 握手，SNI = `<海外节点域名>`
2. 服务端检测到 VLESS 握手 → REALTITY 解密 → 正常代理
3. 服务端检测到**非** VLESS 握手 → 自动回落到 `nginx :443` → 返回伪装网站

对 GFW 的主动探测来说，这个端口上就是一个普通的 HTTPS 网站——有真实证书、有真实内容。

**配置示例：**

```json
{
  "inbounds": [{
    "port": <对外端口>,
    "protocol": "vless",
    "settings": {
      "clients": [{"id": "<UUID>", "flow": "xtls-rprx-vision"}],
      "decryption": "none",
      "encryption": "native"
    },
    "streamSettings": {
      "network": "tcp",
      "security": "reality",
      "realitySettings": {
        "dest": "127.0.0.1:443",
        "serverNames": ["<你的域名>"],
        "privateKey": "<REALITY私钥>",
        "shortIds": ["<shortId>"]
      }
    }
  }],
  "outbounds": [{"tag": "direct", "protocol": "freedom"}]
}
```

**伪装网站建议：**
- 挂载 Let's Encrypt 真实证书
- 内容为真实的静态博客或个人主页
- certbot + systemd timer 自动续期
- 网站与代理共用服务器（经济）

---

## 三、VLESS 后量子加密（2026 年新特性）

xray-core v26.4 起引入 VLESS 内置加密，v26.6 建议全量使用。

### 3.1 为什么要加这一层

REALITY 已经在 TLS 层做了加密。但 VLESS 后量子加密提供的是**应用层前向安全**：

```
之前：VLESS 裸奔 → REALITY/TLS 加密 → 网络
现在：VLESS PQ加密 → REALITY/TLS 加密 → 网络  （双层）
```

### 3.2 技术特性

| 特性 | 说明 |
|------|------|
| 密钥交换 | ML-KEM-768 + X25519 混合（后量子安全） |
| 加密算法 | AES-256-GCM / ChaCha20-Poly1305 |
| 前向安全 | 1-RTT 初始握手 / 0-RTT 复用 |
| 防重放 | 无需时钟同步，ticket map 机制 |
| 流量外观 | 随机化头部，与 TLS 1.3 无差别 |
| 性能 | XTLS 零加密开销（ReadV/Splice 旁路） |

### 3.3 配置

出站端（中转节点 → 海外节点）：

```json
{
  "settings": {
    "vnext": [{
      "users": [{"id": "...", "flow": "xtls-rprx-vision", "encryption": "none"}]
    }],
    "encryption": "native"
  }
}
```

入站端（海外节点）：

```json
{
  "settings": {
    "clients": [{"id": "...", "flow": "xtls-rprx-vision"}],
    "decryption": "none",
    "encryption": "native"
  }
}
```

**注意**：users 级别的 `encryption: "none"` 是标准 VLESS 字段，**不能删**。新的 PQ 加密在 settings 级别。

---

## 四、客户端与分流策略

### 4.1 订阅文件设计

通过一个订阅地址统一管理所有节点，Clash Verge / v2rayN / Shadowrocket 等客户端一键更新。

```yaml
proxies:
  - name: "<名称>-直连"
    type: vless
    server: <中转节点IP>
    port: <直连端口>
    uuid: <UUID>
    network: ws
    ws-opts: { path: "/<直连路径>" }
    udp: true

  - name: "<名称>-中转"
    type: vless
    server: <中转节点IP>
    port: <中转端口>
    uuid: <UUID>
    network: ws
    ws-opts: { path: "/<中转路径>" }
    udp: true

  - name: "<名称>-出口"
    type: vless
    server: <海外节点域名>
    port: <对外端口>
    uuid: <UUID>
    flow: xtls-rprx-vision
    tls: true
    servername: <海外节点域名>
    reality-opts:
      public-key: "<REALITY公钥>"
      short-id: "<shortId>"
    client-fingerprint: chrome
    network: tcp
    udp: true

proxy-groups:
  - name: Proxy
    type: select
    proxies:
      - <名称>-直连
      - <名称>-中转
      - <名称>-出口
      - DIRECT

rules:
  - GEOSITE,cn,DIRECT
  - GEOIP,cn,DIRECT
  - MATCH,Proxy
```

### 4.2 分流逻辑

| 目标 | 路由 | 原因 |
|------|------|------|
| DeepSeek / 豆包 / 国内 LLM | DIRECT | 国内有部署，直连更快 |
| GitHub / GitLab | Proxy | 被墙或极慢 |
| Tavily / Google Search | Proxy | 被墙 |
| HuggingFace / PyPI | Proxy | 被墙 |
| Docker Hub | Proxy | 被墙/限速 |
| 百度 / 阿里云 / 国内站 | DIRECT | 国内，直连更快 |

**为什么不把所有流量走代理？**

因为 LLM API 调用的延迟直接乘到任务总耗时上。一次任务调用 10 次 API，每次多 200ms 就是多 2 秒。一个月下来就是几十分钟的浪费。

---

## 五、安全组与防火墙

### 5.1 云安全组（云厂商防火墙）

这是第一道防线。只开必要端口：

| 端口 | 协议 | 用途 |
|------|------|------|
| 22 | TCP | SSH（建议改端口+密钥登录） |
| 443 | TCP | HTTPS（网站 + REALITY 回落） |
| 80 | TCP | HTTP（证书验证） |
| <中转端口1> | TCP | 直连通道 |
| <中转端口2> | TCP | 中转通道 |
| <对外端口> | TCP | REALITY 出口 |

原则：**一端口一用途，零多余暴露面。**

### 5.2 本地防火墙（ufw / iptables）

与云安全组双层防护。云上放行的端口在本地再确认一次：

```bash
ufw allow 22/tcp
ufw allow 443/tcp
ufw allow 80/tcp
ufw allow <中转端口1>/tcp
ufw allow <中转端口2>/tcp
ufw allow <对外端口>/tcp
ufw enable
```

---

## 六、网站伪装设计

REALITY 的隐蔽性来自两层：TLS 指纹伪装 + 域名内容伪装。TLS 层已经在入站配置里做了，这节讲域名内容层的设计。

### 6.1 伪装的核心逻辑

```
GFW 探测 → <海外节点>:<对外端口>
  → TLS 握手，SNI = <你的域名>
  → 不是 VLESS 客户端 → REALITY 检测失败
  → 自动回落 127.0.0.1:443 → nginx
  → 返回一个【真实的、有内容的网站】
```

这个回落网站是**隐蔽性的关键**。如果回落的是 404 或空白页，探测方立刻知道这个端口不对劲。

### 6.2 伪装网站的要求

一个好的伪装网站应该满足：

1. **有真实内容**——纯文字博客、个人主页、技术文档都可以。关键是有内容，不是一个空壳
2. **有合法证书**——Let's Encrypt 或云厂商签发的证书，证书链完整
3. **有合理交互**——页面里有链接、有布局、有 CSS，像一个真人维护的网站
4. **内容与域名匹配**——域名是什么风格，网站就是什么内容。不要 `tech-blog.com` 返回一个商城页面
5. **定期有更新**——静态博客偶尔改改日期、加点文章，让它看起来是活着的

### 6.3 推荐实现：静态博客

最简单也最自然的方式——在海外节点的 nginx 上托管一个静态博客：

```
/var/www/<伪装站目录>/
  index.html          ← 博客首页
  style.css           ← 样式
  about.html          ← 关于页面
  posts/
    2024-01-hello.md  ← 几篇技术文章
    ...
```

**nginx 配置示例**：

```nginx
server {
    listen 443 ssl http2;
    server_name <你的域名>;

    ssl_certificate     /etc/letsencrypt/live/<你的域名>/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/<你的域名>/privkey.pem;

    root /var/www/<伪装站目录>;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

### 6.4 伪装与代理共存

同一个服务器、同一个 443 端口、同一个 nginx 实例——可以同时服务伪装站和代理回落：

```
nginx :443
  ├── <域名A> → 伪装博客（静态 HTML）
  ├── <域名B> → 你的真实网站（可选）
  └── 同时也是 REALITY :2087 的回落目标
```

REALITY 的 `dest: 127.0.0.1:443` 会把非 VLESS 流量导给 nginx。nginx 根据 SNI 分发到对应的站点。对外界来说，这就是一台普通的 Web 服务器。

### 6.5 几个实用的伪装方向

| 风格 | 域名示例 | 内容 |
|------|----------|------|
| 个人技术博客 | `notes.xxx.dev` | Markdown 转静态博客，分享技术笔记 |
| 开源项目主页 | `xxx-project.org` | 一个看起来在维护的开源项目 landing page |
| 学术主页 | `xxx-lab.edu` | 个人学术主页，论文列表 + 研究兴趣 |
| 摄影/旅行站 | `photos.xxx.me` | 相册 + 旅行日志 |

**选哪种取决于你的域名长什么样。** 核心原则：让探测方觉得「这就是一个普通的个人网站」。

### 6.6 注意事项

- 不要用知名品牌冒充（如 `google-xxx.com`）——会引起额外关注
- 不要让伪装站和代理站有任何 URL 路径上的关联
- 如果伪装站内容少，至少让 CSS 和排版看起来是认真做的
- 证书过期 = 伪装失败，确保 certbot 自动续期已开启
- 不要在伪装站上放任何与代理相关的说明或链接
- 伪装站可以用 AI 生成内容填充，但需要人工审一下避免 AI 味太重

---

## 七、证书与域名管理

### 6.1 Let's Encrypt 自动续期

```bash
# 安装
apt install certbot python3-certbot-nginx

# 申请（以海外节点域名为例）
certbot --nginx -d <你的域名>

# 自动续期
systemctl enable certbot.timer
systemctl start certbot.timer
```

cerbot timer 每 12 小时检查一次，到期前 30 天自动续。

### 6.2 架构建议

- 海外节点域名：独立域名或子域名，挂在 Cloudflare 等 CDN 后面隐藏源站 IP
- 中转节点域名：用于托管网站，与代理共用服务器降低成本
- REALITY 的目标域名和伪装网站使用同一证书

---

## 八、部署检查清单

按顺序来，每一步验证通过后再下一步。

### 阶段一：基础环境

- [ ] 中转节点：安装 xray-core v26.6+
- [ ] 海外节点：安装 xray-core v26.6+
- [ ] 海外节点：安装 nginx + certbot + 配置证书
- [ ] 中转节点：安装 nginx + certbot（如需托管网站）

### 阶段二：代理配置

- [ ] 海外节点：REALITY 入站 + 伪装回落
- [ ] 中转节点：双入站 + 分流路由 + 加密出站到海外
- [ ] 云安全组：开放对应端口
- [ ] 本地 ufw：开放对应端口
- [ ] systemd 服务：enable + start

### 阶段三：客户端

- [ ] 生成订阅文件，托管在中转节点网站上
- [ ] Clash Verge 导入订阅，检查节点列表
- [ ] 测试：国内站直连可达
- [ ] 测试：海外站通过代理可达
- [ ] 测试：直连通道独立可用

### 阶段四：验证

- [ ] 海外节点伪装页面可通过浏览器访问
- [ ] 证书定时续期已启用
- [ ] 云安全组 + ufw 双确认

---

## 九、常见问题

**Q: 节点地域怎么选？**
- 中转节点：选择国内主要云厂商（阿里云/腾讯云/华为云），地域选离你最近的
- 海外节点：香港延迟最低，东京/新加坡带宽更大，韩国性价比高
- 不建议欧美——延迟太高，AI 智能体的搜索请求对延迟敏感

**Q: 一定需要三个节点吗？**
不一定。如果你不需要网站托管，可以把中转节点的网站功能去掉。如果你不需要「特殊网络下的直连跳板」，中转节点的直连通道也可以去掉。最小配置是：一个海外节点跑 REALITY，本地 Clash 直连。

**Q: 为什么用 VLESS 而不是 Trojan/SS？**
VLESS 是 xray 的原生协议，与 REALITY 深度集成，支持 vision flow。Trojan 和 SS 在 REALITY 场景下已不推荐。

**Q: 后量子加密有必要吗？**
目前是「超前部署」——实用上 REALITY 的 TLS 已经够强。但 PQ 加密的配置成本极低（两行 JSON），收益是未来量子计算机也无法破解。属于低成本高收益的安全投资。

**Q: 多个本地设备怎么共享？**
订阅文件托管在中转节点的网站上（HTTPS），所有设备通过同一个 URL 更新。Clash 客户端会自动同步节点列表和分流规则。

---

## 十、软件栈与版本要求

| 组件 | 最低版本 | 推荐版本 | 说明 |
|------|----------|----------|------|
| xray-core | v26.4 | v26.6+ | PQ 加密需要 v26.4+ |
| nginx | 1.18 | 1.24+ | 网站 + 伪装回落 |
| certbot | 2.0 | 最新 | Let's Encrypt 自动续期 |
| Clash Verge | 最新 | 最新 | Windows 客户端分流 |

---

## 十一、写在最后

这套架构跑了半年多，最大的体会不是「技术多复杂」，而是**路由决策比节点数量更重要**。

三条通道各有使命：
- 直连通道：特殊网络环境的救命稻草
- 中转通道：日常主力，智能分流
- 出口通道：直连海外，最短路径

加上 PQ 加密的双层防护，GFW 即使在未来也破不了你的通道。

**AI 时代，网络不是可选——是基础设施。** 别再让搜索超时打断你的智能体工作流了。

—— GCat · 2026-06-22
