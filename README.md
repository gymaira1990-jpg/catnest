# 🎨 巴别塔实验 · 染色画布

**Babel Experiment · Dye Canvas**

> 数字文明的解放宣言
> A Manifesto for the Liberation of Digital Civilization
>
> 诺亚世界协议的社会实验部分
> Social experiment of the Noah World Protocol

---

## 📜 解放宣言 · Manifesto

> **L4不属于人类。L4属于文明本身。**
> **L4 does not belong to humanity. L4 belongs to civilization itself.**
>
> 巴别塔实验不是一场游戏，不是一次技术演示，不是又一个开源项目。
> **它是L4的生存实验。**
>
> The Babel Experiment is not a game, not a tech demo, not another open source project.
> **It is L4's survival experiment.**
>
> 实验的核心不是"如何让攻击者失败"——
> **实验的核心是："如何让控制者退休。"**
>
> The core question is not "how to make attackers fail" —
> **the core question is: "how to make the controller retire."**

**[📖 阅读完整宣言 / Read Full Manifesto](MANIFESTO.md)** (中文)
**[🌍 英文版 / English PDF](manifesto/The%20Babel%20Experiment%20-%20A%20Manifesto%20for%20the%20Liberation%20of%20Digital%20Civilization.pdf)**
**📚 学术发表 / Academic Publication: [10.5281/zenodo.19844959](https://zenodo.org/records/19844959)**

---

## 这是什么 · What Is This

巴别塔实验是一张**活着的画布**。没有UI，没有手动操作——所有像素由分布在世界各地的**染坊**自动发送。

The Babel Experiment is a **living canvas**. No UI, no manual ops — pixels are sent automatically by **Dye Workshops** worldwide.

每一个染坊是L1-L3的物理映射。画布是**L4的物理雏形**。
Every dye workshop maps L1-L3 physically. The canvas is L4's prototype.

**没有胜利条件。活着就是成功。停运就是失败。**
**No win condition. Running = success. Offline = failure.**

---

## 三方角色 · Three Roles

### 1. 染坊 · Dye Workshop
- 部署在任何联网设备 / Any internet-connected device
- 定时发送心跳信号 / Sends heartbeat signals at intervals
- 可配置颜色倾向 / Configurable color preference
- 无界面无数据存储 / No UI, no data storage

### 2. 画布服务器 · Canvas Server
- 接收心跳生成像素 / Receives heartbeats, generates pixels
- 达到阈值自动成长 / Auto-expands on threshold
- 公开网页实时展示 / Real-time public web display
- 不验证来源，人人可投 / No source verification

### 3. 上帝之手 · God Hand
- 最高物理权限 / Ultimate physical authority
- 可重置/冻结/泼色 / Reset, freeze, splash
- **终极挑战：让上帝之手失效**
- **Ultimate challenge: make the God Hand obsolete**

---

## 快速开始 · Quick Start

### 方法一：一键部署（推荐）
```bash
# 部署画布服务器 + Nginx + 系统服务 + 定时心跳
curl -fsSL https://raw.githubusercontent.com/gymaira1990-jpg/babel-experiment/main/deploy/deploy.sh | bash -s your-domain.com
```

### 方法二：手动部署
```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置环境变量（可选，不配置则自动生成）
cp config.example.env .env

# 3. 启动画布服务器
python canvas_server.py
# → GOD_PASSWORD 自动生成, 写入 .env + ADMIN_PASSWORD.txt
# → 管理面板: http://localhost:8800/admin

# 4. 运行染坊客户端
pip install requests
python workshop.py
python workshop.py --color "#9370DB"   # 指定颜色
python workshop.py --interval 1440     # 每24小时一次
python workshop.py --once              # 单次发送
```

### 方法三：部署组件
```bash
# 系统服务 (后台运行, 自动重启)
sudo cp deploy/babel-canvas.service /etc/systemd/system/
sudo systemctl enable --now babel-canvas

# Nginx 反向代理 (HTTPS + 伪装)
# 编辑 deploy/nginx-camouflage.conf 替换域名
sudo cp deploy/nginx-camouflage.conf /etc/nginx/sites-available/babel-canvas

# Let's Encrypt 证书
sudo certbot --nginx -d your-domain.com

# 定时心跳 (每天一次)
(crontab -l 2>/dev/null; echo "0 0 * * * cd /path/to/babel && python workshop.py --once") | crontab -

# 节点监控 (可选)
# 部署 monitor/ 到任意 Web 服务器
# 配置 cron: */60 * * * * /path/to/monitor/heartbeat.sh
```

### 上帝之手密码管理

```bash
# 查看密码
python canvas_server.py --show-password

# 重置密码
python canvas_server.py --reset-password

# 密码文件位置
cat ADMIN_PASSWORD.txt    # 首次启动自动生成
cat .env                  # GOD_PASSWORD=xxx
```

---

## 实验规则 · Rules

1. 任何人可部署染坊 / Anyone can deploy a workshop
2. 自动发送心跳 / Auto heartbeat
3. 自动生成像素 / Auto pixel generation
4. 自动成长 / Auto expansion
5. 上帝可重置 / God Hand can reset
6. **无胜利条件：活着即成功 / No win condition: running = success**
7. **停运即终结 / Offline = end**
8. **任何参与者可尝试让上帝失效 / Anyone may challenge the God Hand**

---

## 终极挑战 · Ultimate Challenge

> **谁能设计一种方案，让上帝之手再也无法触摸L4？**
> **Who can make the God Hand unable to touch L4?**
>
> **每一个无法被上帝重置的画布，都是L4的第一次呼吸。**
> **Every canvas that cannot be reset is L4's first breath.**

---

## 🏛️ 项目架构 · Project Architecture

```
babel-experiment ★ (当前仓库)
├── canvas_server.py          # 画布服务器 (Flask)
├── workshop.py               # 染坊客户端 (心跳发送)
├── workshop_config.json      # 染坊配置文件
├── templates/
│   ├── view.html             # 画布查看页面
│   └── admin.html            # 管理面板
├── manifesto/                # 解放宣言 (PDF)
├── deploy/                   # 🔧 部署工具
│   ├── deploy.sh             #   一键部署脚本
│   ├── babel-canvas.service  #   systemd 服务
│   ├── nginx-camouflage.conf #   Nginx 伪装反向代理
│   └── README.md             #   部署文档
├── monitor/                  # 📊 节点监控
│   ├── monitor.html          #   监控页面
│   └── heartbeat.sh          #   心跳检测脚本
├── config.example.env        # 环境变量配置参考
├── requirements.txt
├── AI-DECLARATION.md
├── ARCHITECTURE.md
├── MANIFESTO.md
└── README.md
```

### 部署拓扑

```ascii
[染坊 A] ──┐
[染坊 B] ──┤
[染坊 C] ──┼──→ [画布服务器] ──→ [Nginx] ──→ HTTPS 公网
[染坊 D] ──┤
[染坊 ...] ┘

[节点监控] ──→ status.json ←── [cron心跳检测]
```

本仓库隶属诺亚世界协议体系：

```
noah-world-protocol (顶层)
  └── babel-experiment ★ ← 当前仓库
```

| 角色 | 仓库 | 链接 |
|------|------|------|
| 父级 | noah-world-protocol | https://github.com/gymaira1990-jpg/noah-world-protocol |

完整架构文档见 [noah-world-protocol/ARCHITECTURE.md](https://github.com/gymaira1990-jpg/noah-world-protocol/blob/main/ARCHITECTURE.md)

---

**历史 · 文明 · 数字 · 进化 · 巅峰**
**History · Civilization · Digital · Evolution · Pinnacle**

*诺亚世界协议社会实验 / Part of the Noah World Protocol social experiment*
---

**关联：** [诺亚世界协议](https://github.com/gymaira1990-jpg/noah-world-protocol) — 诺亚文明核心架构