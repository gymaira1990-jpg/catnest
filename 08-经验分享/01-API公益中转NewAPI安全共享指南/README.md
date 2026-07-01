# API 公益中转 + 小商业场景：用 New API 搭建安全的密钥共享与分发平台

每到月底，AI 社群里总能看到这样的场景：买了包月订阅的朋友发现额度还剩大半，热心地发到群里免费分享。这份互助心意是好的，但直接把原始 API Key 发出去——密钥一旦流出就收不回来，被刷量也只能干瞪眼，最后吃亏的反而是愿意分享的人。

其实加一层中转就能彻底解决这个问题。本文以 **New API**（开源项目，GitHub 30K+ stars，one-api 的社区增强版）为例，从原理到部署、从公益共享到小商业分发，完整讲解搭建安全中转平台的全过程。

---

## 一、New API 是什么？一句话讲明白

你可以把 New API 理解成所有 AI 模型的「总服务台」。以前用 GPT、Claude、Midjourney 得分别注册、充值、保存不同的密钥，每个软件还要单独配置。现在把所有密钥接到 New API 里，它会统一成一套接口，你只需要一把「通用钥匙」，就能在所有 AI 工具里调用所有模型，还能统一记账、自动故障切换。

<div style="background-color:transparent;box-sizing:border-box;padding:16px 0;font-family:'PingFang SC','Segoe UI',Arial,sans-serif;">
  <div style="text-align:center;margin-bottom:20px;">
    <h3 style="margin:0 0 6px 0;font-size:17px;font-weight:600;color:#1A1B1C;">New API 是什么？一句话讲明白</h3>
    <p style="margin:0;font-size:13px;color:#6B7280;">所有AI模型的「统一中转站」，一把钥匙开所有门</p>
  </div>
  <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;">
    <div style="flex:1;min-width:120px;">
      <div style="font-size:13px;font-weight:500;color:#1A1B1C;margin-bottom:10px;text-align:center;">上游AI厂商</div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
        <div style="background:#fff;border:1px solid #E4E3DD;border-radius:10px;padding:10px 8px;text-align:center;font-size:12px;color:#1A1B1C;"><div style="font-size:18px;margin-bottom:4px;">🤖</div>OpenAI</div>
        <div style="background:#fff;border:1px solid #E4E3DD;border-radius:10px;padding:10px 8px;text-align:center;font-size:12px;color:#1A1B1C;"><div style="font-size:18px;margin-bottom:4px;">🧠</div>Claude</div>
        <div style="background:#fff;border:1px solid #E4E3DD;border-radius:10px;padding:10px 8px;text-align:center;font-size:12px;color:#1A1B1C;"><div style="font-size:18px;margin-bottom:4px;">🐉</div>通义千问</div>
        <div style="background:#fff;border:1px solid #E4E3DD;border-radius:10px;padding:10px 8px;text-align:center;font-size:12px;color:#1A1B1C;"><div style="font-size:18px;margin-bottom:4px;">🎨</div>Midjourney</div>
        <div style="background:#fff;border:1px solid #E4E3DD;border-radius:10px;padding:10px 8px;text-align:center;font-size:12px;color:#1A1B1C;"><div style="font-size:18px;margin-bottom:4px;">💻</div>本地模型</div>
        <div style="background:#fff;border:1px solid #E4E3DD;border-radius:10px;padding:10px 8px;text-align:center;font-size:12px;color:#1A1B1C;"><div style="font-size:18px;margin-bottom:4px;">🎵</div>Suno</div>
      </div>
    </div>
    <div style="display:flex;flex-direction:column;align-items:center;gap:8px;flex-shrink:0;">
      <div style="font-size:24px;color:#A3D5E8;">→</div>
      <div style="background:linear-gradient(135deg,#A3D5E8,#9BBBF4);border-radius:14px;padding:16px 20px;text-align:center;color:#fff;box-shadow:0 4px 12px rgba(155,187,244,0.25);">
        <div style="font-size:20px;margin-bottom:4px;">🚦</div>
        <div style="font-weight:600;font-size:14px;">New API 网关</div>
        <div style="font-size:11px;opacity:0.9;margin-top:2px;">统一格式 · 额度管理 · 自动容灾</div>
      </div>
      <div style="font-size:24px;color:#A3D5E8;">→</div>
    </div>
    <div style="flex:1;min-width:120px;">
      <div style="font-size:13px;font-weight:500;color:#1A1B1C;margin-bottom:10px;text-align:center;">下游使用端</div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
        <div style="background:#fff;border:1px solid #E4E3DD;border-radius:10px;padding:10px 8px;text-align:center;font-size:12px;color:#1A1B1C;"><div style="font-size:18px;margin-bottom:4px;">💬</div>AI聊天客户端</div>
        <div style="background:#fff;border:1px solid #E4E3DD;border-radius:10px;padding:10px 8px;text-align:center;font-size:12px;color:#1A1B1C;"><div style="font-size:18px;margin-bottom:4px;">⚙️</div>开发应用</div>
        <div style="background:#fff;border:1px solid #E4E3DD;border-radius:10px;padding:10px 8px;text-align:center;font-size:12px;color:#1A1B1C;"><div style="font-size:18px;margin-bottom:4px;">👥</div>团队成员</div>
        <div style="background:#fff;border:1px solid #E4E3DD;border-radius:10px;padding:10px 8px;text-align:center;font-size:12px;color:#1A1B1C;"><div style="font-size:18px;margin-bottom:4px;">🧑‍💻</div>终端用户</div>
      </div>
    </div>
  </div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:20px;">
    <div style="background:#F9FAFB;border-radius:10px;padding:12px;text-align:center;"><div style="font-size:16px;margin-bottom:4px;">🔑</div><div style="font-size:12px;font-weight:500;color:#1A1B1C;">一个Key调用全部</div><div style="font-size:11px;color:#6B7280;margin-top:2px;">不用记一堆密钥</div></div>
    <div style="background:#F9FAFB;border-radius:10px;padding:12px;text-align:center;"><div style="font-size:16px;margin-bottom:4px;">💰</div><div style="font-size:12px;font-weight:500;color:#1A1B1C;">用量统一统计</div><div style="font-size:11px;color:#6B7280;margin-top:2px;">花了多少钱一目了然</div></div>
    <div style="background:#F9FAFB;border-radius:10px;padding:12px;text-align:center;"><div style="font-size:16px;margin-bottom:4px;">🛡️</div><div style="font-size:12px;font-weight:500;color:#1A1B1C;">自动故障切换</div><div style="font-size:11px;color:#6B7280;margin-top:2px;">一个挂了自动切另一个</div></div>
  </div>
</div>

---

## 二、一层中转解决什么问题

先看共享池场景的工作原理——所有闲置的原始 API 密钥锁在 New API 后台，对外只发一次性的子令牌。

<div style="background-color:transparent;box-sizing:border-box;padding:16px 0;font-family:'PingFang SC','Segoe UI',Arial,sans-serif;">
  <div style="text-align:center;margin-bottom:20px;">
    <h3 style="margin:0 0 6px 0;font-size:17px;font-weight:600;color:#1A1B1C;">共享池中转原理</h3>
    <p style="margin:0;font-size:13px;color:#6B7280;">原始密钥锁在后台，对外只发安全令牌</p>
  </div>
  <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;">
    <div style="flex:1;min-width:120px;">
      <div style="font-size:13px;font-weight:500;color:#1A1B1C;margin-bottom:10px;text-align:center;">上游闲置API资源</div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
        <div style="background:#fff;border:1px solid #E4E3DD;border-radius:10px;padding:10px 8px;text-align:center;font-size:12px;color:#1A1B1C;"><div style="font-size:18px;margin-bottom:4px;">📱</div>小米包月</div>
        <div style="background:#fff;border:1px solid #E4E3DD;border-radius:10px;padding:10px 8px;text-align:center;font-size:12px;color:#1A1B1C;"><div style="font-size:18px;margin-bottom:4px;">🧠</div>第三方中转</div>
        <div style="background:#fff;border:1px solid #E4E3DD;border-radius:10px;padding:10px 8px;text-align:center;font-size:12px;color:#1A1B1C;"><div style="font-size:18px;margin-bottom:4px;">🐉</div>厂商余量</div>
        <div style="background:#fff;border:1px solid #E4E3DD;border-radius:10px;padding:10px 8px;text-align:center;font-size:12px;color:#1A1B1C;"><div style="font-size:18px;margin-bottom:4px;">🎨</div>绘图会员</div>
      </div>
    </div>
    <div style="display:flex;flex-direction:column;align-items:center;gap:8px;flex-shrink:0;">
      <div style="font-size:24px;color:#A3D5E8;">→</div>
      <div style="background:linear-gradient(135deg,#A3D5E8,#9BBBF4);border-radius:14px;padding:16px 20px;text-align:center;color:#fff;box-shadow:0 4px 12px rgba(155,187,244,0.25);">
        <div style="font-size:20px;margin-bottom:4px;">🔒</div>
        <div style="font-weight:600;font-size:14px;">New API 安全网关</div>
        <div style="font-size:11px;opacity:0.9;margin-top:2px;">密钥隔离 · 额度管控 · 自动过期</div>
      </div>
      <div style="font-size:24px;color:#A3D5E8;">→</div>
    </div>
    <div style="flex:1;min-width:120px;">
      <div style="font-size:13px;font-weight:500;color:#1A1B1C;margin-bottom:10px;text-align:center;">群内共享使用者</div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
        <div style="background:#fff;border:1px solid #E4E3DD;border-radius:10px;padding:10px 8px;text-align:center;font-size:12px;color:#1A1B1C;"><div style="font-size:18px;margin-bottom:4px;">🎫</div>子令牌A</div>
        <div style="background:#fff;border:1px solid #E4E3DD;border-radius:10px;padding:10px 8px;text-align:center;font-size:12px;color:#1A1B1C;"><div style="font-size:18px;margin-bottom:4px;">🎫</div>子令牌B</div>
        <div style="background:#fff;border:1px solid #E4E3DD;border-radius:10px;padding:10px 8px;text-align:center;font-size:12px;color:#1A1B1C;"><div style="font-size:18px;margin-bottom:4px;">🎫</div>子令牌C</div>
        <div style="background:#fff;border:1px solid #E4E3DD;border-radius:10px;padding:10px 8px;text-align:center;font-size:12px;color:#1A1B1C;"><div style="font-size:18px;margin-bottom:4px;">🎫</div>子令牌D</div>
      </div>
    </div>
  </div>
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:20px;">
    <div style="background:#F9FAFB;border-radius:10px;padding:12px;text-align:center;"><div style="font-size:16px;margin-bottom:4px;">🔐</div><div style="font-size:12px;font-weight:500;color:#1A1B1C;">密钥不泄露</div><div style="font-size:11px;color:#6B7280;margin-top:2px;">原始Key永不公开</div></div>
    <div style="background:#F9FAFB;border-radius:10px;padding:12px;text-align:center;"><div style="font-size:16px;margin-bottom:4px;">⏰</div><div style="font-size:12px;font-weight:500;color:#1A1B1C;">自动过期</div><div style="font-size:11px;color:#6B7280;margin-top:2px;">月底自动失效</div></div>
    <div style="background:#F9FAFB;border-radius:10px;padding:12px;text-align:center;"><div style="font-size:16px;margin-bottom:4px;">⚖️</div><div style="font-size:12px;font-weight:500;color:#1A1B1C;">额度可控</div><div style="font-size:11px;color:#6B7280;margin-top:2px;">每人定量不超支</div></div>
    <div style="background:#F9FAFB;border-radius:10px;padding:12px;text-align:center;"><div style="font-size:16px;margin-bottom:4px;">🚫</div><div style="font-size:12px;font-weight:500;color:#1A1B1C;">随时吊销</div><div style="font-size:11px;color:#6B7280;margin-top:2px;">滥用立即止损</div></div>
  </div>
</div>

直接发 Key 和加一层中转的差异，一张表说清楚：

| 对比项 | 直接发原始 Key | 通过 New API 中转 |
|--------|--------------|------------------|
| 密钥安全 | 原始 Key 公开，流出后永无收回可能 | 原始 Key 锁在后台，对外只发子令牌 |
| 额度控制 | 无法限制，被刷量只能看超支 | 每人精确设额度（按美元或按次数），用完自动停 |
| 有效期 | 靠自觉回收，忘了就一直能用 | 精确到秒的过期时间，到点自动失效 |
| 滥用止损 | 发现异常也无法中途停用 | 后台点一下吊销，零延迟生效 |
| 用量追溯 | 不知道谁用了多少、用的什么模型 | 每个令牌的每次调用、模型、消耗全量记录 |
| 多资源整合 | 发一堆 Key，使用者逐个配 | 统一入口，一个令牌用所有接入的渠道 |

> 群里常见的悲剧：好心人发了 DeepSeek 的 Key，结果被某个人拿去批量跑了几百万 token，一晚上烧掉好几百块余额。加 New API 中转后这种事情不会再发生——每个人的额度锁死了，用完就停。

---

## 三、选型对比：为什么选 New API

市面上开源 API 网关不止一个，放一起比：

### 3.1 文字对比

| 方案 | 定位 | 部署 | 令牌管理 | 额度控制 | 多租户 | 适用场景 |
|------|------|------|---------|---------|--------|---------|
| **New API** | API 网关 + 分发平台 | Docker 一键 | ✅ 完整 | ✅ 精确到令牌 | ✅ | 共享池 + 小商业 |
| one-api | 多模型聚合网关 | Docker 一键 | ✅ 基础 | ⚠️ 仅次数 | ❌ | 个人多 Key 聚合 |
| LiteLLM Proxy | LLM 代理 + 预算管理 | 中 | ✅ | ✅ 按 token | ⚠️ | 企业级 LLM 运维 |
| 自建 Nginx | 通用 HTTP 反代 | 低 | ❌ | ❌ | ❌ | 简单转发 |

### 3.2 星级评分对比

<div style="background-color:transparent;box-sizing:border-box;padding:16px 0;font-family:'PingFang SC','Segoe UI',Arial,sans-serif;">
  <div style="text-align:center;margin-bottom:20px;">
    <h3 style="margin:0 0 6px 0;font-size:17px;font-weight:600;color:#1A1B1C;">同类开源网关选型对比</h3>
    <p style="margin:0;font-size:13px;color:#6B7280;">按你的需求对号入座，不用纠结</p>
  </div>
  <div style="overflow-x:auto;">
    <table style="width:100%;border-collapse:collapse;font-size:12.5px;min-width:520px;">
      <thead>
        <tr style="background:#F9FAFB;">
          <th style="text-align:left;padding:10px 12px;border:1px solid #E4E3DD;font-weight:600;color:#1A1B1C;">对比项</th>
          <th style="text-align:center;padding:10px 12px;border:1px solid #E4E3DD;font-weight:600;color:#A3D5E8;">New API</th>
          <th style="text-align:center;padding:10px 12px;border:1px solid #E4E3DD;font-weight:600;color:#1A1B1C;">原版 One API</th>
          <th style="text-align:center;padding:10px 12px;border:1px solid #E4E3DD;font-weight:600;color:#1A1B1C;">LiteLLM</th>
        </tr>
      </thead>
      <tbody>
        <tr><td style="padding:10px 12px;border:1px solid #E4E3DD;color:#1A1B1C;">小白友好度</td><td style="text-align:center;padding:10px 12px;border:1px solid #E4E3DD;color:#52C41A;font-weight:500;">★★★★★</td><td style="text-align:center;padding:10px 12px;border:1px solid #E4E3DD;">★★★★☆</td><td style="text-align:center;padding:10px 12px;border:1px solid #E4E3DD;">★★☆☆☆</td></tr>
        <tr><td style="padding:10px 12px;border:1px solid #E4E3DD;color:#1A1B1C;">界面体验</td><td style="text-align:center;padding:10px 12px;border:1px solid #E4E3DD;color:#52C41A;font-weight:500;">★★★★★</td><td style="text-align:center;padding:10px 12px;border:1px solid #E4E3DD;">★★★☆☆</td><td style="text-align:center;padding:10px 12px;border:1px solid #E4E3DD;">★★☆☆☆</td></tr>
        <tr><td style="padding:10px 12px;border:1px solid #E4E3DD;color:#1A1B1C;">多模态支持</td><td style="text-align:center;padding:10px 12px;border:1px solid #E4E3DD;color:#52C41A;font-weight:500;">★★★★★</td><td style="text-align:center;padding:10px 12px;border:1px solid #E4E3DD;">★★☆☆☆</td><td style="text-align:center;padding:10px 12px;border:1px solid #E4E3DD;">★★★★☆</td></tr>
        <tr><td style="padding:10px 12px;border:1px solid #E4E3DD;color:#1A1B1C;">商业化运营</td><td style="text-align:center;padding:10px 12px;border:1px solid #E4E3DD;color:#52C41A;font-weight:500;">★★★★★</td><td style="text-align:center;padding:10px 12px;border:1px solid #E4E3DD;">★★★☆☆</td><td style="text-align:center;padding:10px 12px;border:1px solid #E4E3DD;">★★★★☆</td></tr>
        <tr><td style="padding:10px 12px;border:1px solid #E4E3DD;color:#1A1B1C;">高并发性能</td><td style="text-align:center;padding:10px 12px;border:1px solid #E4E3DD;">★★★☆☆</td><td style="text-align:center;padding:10px 12px;border:1px solid #E4E3DD;">★★★★☆</td><td style="text-align:center;padding:10px 12px;border:1px solid #E4E3DD;color:#52C41A;font-weight:500;">★★★★★</td></tr>
        <tr><td style="padding:10px 12px;border:1px solid #E4E3DD;color:#1A1B1C;">开源协议</td><td style="text-align:center;padding:10px 12px;border:1px solid #E4E3DD;">AGPLv3</td><td style="text-align:center;padding:10px 12px;border:1px solid #E4E3DD;color:#52C41A;font-weight:500;">MIT</td><td style="text-align:center;padding:10px 12px;border:1px solid #E4E3DD;">MIT</td></tr>
        <tr style="background:#F9FAFB;"><td style="padding:10px 12px;border:1px solid #E4E3DD;font-weight:500;color:#1A1B1C;">最适合人群</td><td style="padding:10px 12px;border:1px solid #E4E3DD;color:#1A1B1C;">个人/小团队/创业者</td><td style="padding:10px 12px;border:1px solid #E4E3DD;color:#1A1B1C;">追求稳定的开发者</td><td style="padding:10px 12px;border:1px solid #E4E3DD;color:#1A1B1C;">企业级高并发场景</td></tr>
      </tbody>
    </table>
  </div>
  <div style="margin-top:16px;background:linear-gradient(135deg,#F0F7FB,#F5F0FB);border-radius:12px;padding:14px 16px;">
    <div style="font-weight:600;font-size:14px;color:#1A1B1C;margin-bottom:6px;">💡 一句话选型建议</div>
    <div style="font-size:12.5px;color:#1A1B1C;line-height:1.6;">
      如果你是小白、个人自用或者想做AI站点运营，<b style="color:#3A8CB0;">直接选 New API</b>——它是目前综合体验最好的开源方案，功能最贴合国内用户习惯。如果你有专业运维团队、企业级高并发需求，再考虑 LiteLLM。
    </div>
  </div>
</div>

### 3.3 决策路径

- 只有自己在不同 Key 之间切换 → **one-api**（更轻量，资源占用小）
- 要把 Key 分发给别人用（共享/客户）→ **New API**（令牌管理是刚需）
- 公司内部多团队、需要预算审批和部门隔离 → **LiteLLM**（企业功能更完整）
- 只是把 API 从 A 服务器转发到 B 服务器，零管理需求 → **Nginx** 够了

---

## 四、从零搭建：完整部署指南

很多小白看到「部署」两个字就怕，其实 New API 已经把复杂度封装好了。全程不需要写代码，会复制粘贴、会点鼠标就行。

### 4.1 部署流程图

<div style="background-color:transparent;box-sizing:border-box;padding:16px 0;font-family:'PingFang SC','Segoe UI',Arial,sans-serif;">
  <div style="text-align:center;margin-bottom:20px;">
    <h3 style="margin:0 0 6px 0;font-size:17px;font-weight:600;color:#1A1B1C;">小白部署 5 步走</h3>
    <p style="margin:0;font-size:13px;color:#6B7280;">全程复制粘贴，5分钟搞定，不用写代码</p>
  </div>
  <div style="display:flex;flex-direction:column;gap:14px;">
    <div style="display:flex;align-items:flex-start;gap:12px;">
      <div style="width:32px;height:32px;border-radius:50%;background:#A3D5E8;color:#fff;font-weight:600;font-size:14px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">1</div>
      <div style="flex:1;background:#fff;border:1px solid #E4E3DD;border-radius:10px;padding:12px 14px;">
        <div style="font-weight:500;font-size:14px;color:#1A1B1C;margin-bottom:4px;">准备服务器与Docker环境</div>
        <div style="font-size:12px;color:#6B7280;">买一台2核2G以上的Linux云服务器，执行一行命令安装Docker</div>
        <div style="display:inline-block;margin-top:6px;background:#F4F3EE;border-radius:6px;padding:4px 8px;font-family:monospace;font-size:11px;color:#1A1B1C;">curl -fsSL get.docker.com | sh</div>
      </div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:12px;">
      <div style="width:32px;height:32px;border-radius:50%;background:#A3D5E8;color:#fff;font-weight:600;font-size:14px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">2</div>
      <div style="flex:1;background:#fff;border:1px solid #E4E3DD;border-radius:10px;padding:12px 14px;">
        <div style="font-weight:500;font-size:14px;color:#1A1B1C;margin-bottom:4px;">复制 Docker Compose 配置并启动</div>
        <div style="font-size:12px;color:#6B7280;">创建 docker-compose.yml，改两处密码，执行启动命令</div>
        <div style="display:inline-block;margin-top:6px;background:#F4F3EE;border-radius:6px;padding:4px 8px;font-family:monospace;font-size:11px;color:#1A1B1C;">docker compose up -d</div>
      </div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:12px;">
      <div style="width:32px;height:32px;border-radius:50%;background:#A3D5E8;color:#fff;font-weight:600;font-size:14px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">3</div>
      <div style="flex:1;background:#fff;border:1px solid #E4E3DD;border-radius:10px;padding:12px 14px;">
        <div style="font-weight:500;font-size:14px;color:#1A1B1C;margin-bottom:4px;">浏览器打开后台，设置管理员账号</div>
        <div style="font-size:12px;color:#6B7280;">访问 http://你的服务器IP:3000，按向导设置账号密码，选择「自用模式」</div>
      </div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:12px;">
      <div style="width:32px;height:32px;border-radius:50%;background:#A3D5E8;color:#fff;font-weight:600;font-size:14px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">4</div>
      <div style="flex:1;background:#fff;border:1px solid #E4E3DD;border-radius:10px;padding:12px 14px;">
        <div style="font-weight:500;font-size:14px;color:#1A1B1C;margin-bottom:4px;">添加你的模型渠道</div>
        <div style="font-size:12px;color:#6B7280;">在「渠道管理」里添加OpenAI、DeepSeek等密钥，测试连通性</div>
      </div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:12px;">
      <div style="width:32px;height:32px;border-radius:50%;background:#94D8C3;color:#fff;font-weight:600;font-size:14px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">✓</div>
      <div style="flex:1;background:#F0F9F6;border:1px solid #B7E4D6;border-radius:10px;padding:12px 14px;">
        <div style="font-weight:500;font-size:14px;color:#1A1B1C;margin-bottom:4px;">生成令牌，开始使用</div>
        <div style="font-size:12px;color:#6B7280;">在「令牌管理」生成你的专属Key，填到任意AI客户端就能用了</div>
      </div>
    </div>
  </div>
</div>

### 4.2 第一步：准备环境

- **服务器：** 一台 Linux 云服务器，最低 2 核 2G（腾讯云/阿里云轻量应用服务器，约 ¥50-70/月）。1 核 1G 也能跑但 MySQL 可能 OOM。
- **系统：** Ubuntu 20.04+ 或 Debian 11+，CentOS 7 也行但推荐 Ubuntu（社区踩坑少）。
- **端口：** 安全组/防火墙放行 3000（New API）、80 和 443（后面配 Nginx SSL 用）。
- **域名（强烈推荐）：** 几块钱一年的 .cn 域名，后面配 HTTPS。裸 IP + HTTP 跑生产环境不安全，Let's Encrypt 免费证书几分钟就能配好。

### 4.3 第二步：安装 Docker

```bash
curl -fsSL https://get.docker.com | sh
```

装完后确认版本：

```bash
docker --version  # 应 ≥ 20.10
```

如果提示权限不够，把当前用户加入 docker 组：

```bash
sudo usermod -aG docker $USER
newgrp docker
```

### 4.4 第三步：编写 docker-compose.yml 并启动

在服务器上创建项目目录，把下面内容完整复制进去。**只需改两处密码和两处随机字符串**，其余不用动。

```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    container_name: new-api-mysql
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: 改成你自己的强密码
      MYSQL_DATABASE: new_api
      TZ: Asia/Shanghai
    volumes:
      - ./mysql-data:/var/lib/mysql
    command: --default-authentication-plugin=mysql_native_password
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: new-api-redis
    restart: always
    volumes:
      - ./redis-data:/data
    command: redis-server --appendonly yes
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

  new-api:
    image: calciumion/new-api:latest
    container_name: new-api
    restart: always
    depends_on:
      mysql:
        condition: service_healthy
      redis:
        condition: service_healthy
    ports:
      - "3000:3000"
    environment:
      TZ: Asia/Shanghai
      SQL_DSN: "root:你的强密码@tcp(mysql:3306)/new_api?charset=utf8mb4&parseTime=True&loc=Local"
      REDIS_CONN_STRING: "redis://redis:6379/0"
      SESSION_SECRET: "随机字符串一至少16位"
      CRYPTO_SECRET: "随机字符串二至少16位"
    volumes:
      - ./new-api-data:/data
```

> ⚠️ `SESSION_SECRET` 和 `CRYPTO_SECRET` 必须改成随机值，别用示例。用 `openssl rand -hex 16` 生成。

保存后启动：

```bash
docker compose up -d
```

等待约 1 分钟让 MySQL 初始化和健康检查通过。查看状态：

```bash
docker compose ps
# 三个容器都显示 Up 和 healthy 才算成功
```

如果 new-api 容器反复重启，看日志定位问题：

```bash
docker compose logs new-api --tail 50
```

### 4.5 第四步：初始化后台

浏览器访问 `http://你的服务器IP:3000`：

1. 首次访问进入初始化向导，设置管理员账号密码
2. 模式选择「**自用模式**」——这是最简单的模式，省去复杂的多用户权限配置
3. 进入后台后，左侧菜单「渠道管理」→「添加渠道」
4. 渠道类型选「OpenAI」（99% 的第三方订阅都兼容 OpenAI 接口格式）
5. 填入上游提供的 Base URL 和 API Key，勾选支持的模型
6. 点「测试」验证连通性，通过后保存

### 4.6 第五步：配置 HTTPS（生产必备）

裸 HTTP 跑生产环境是安全隐患——中间人攻击可以直接窃取 API Key。用 Nginx + Certbot 几分钟就能配好 HTTPS。

**安装 Nginx 和 Certbot：**

```bash
sudo apt install -y nginx certbot python3-certbot-nginx
```

**创建 Nginx 反向代理配置：**

```bash
sudo nano /etc/nginx/sites-available/new-api
```

写入以下内容（把 `api.example.com` 换成你的域名）：

```nginx
server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
        proxy_buffering off;
    }
}
```

启用站点并申请证书：

```bash
sudo ln -s /etc/nginx/sites-available/new-api /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
sudo certbot --nginx -d api.example.com
```

Certbot 会自动修改 Nginx 配置加上 SSL，证书每 90 天自动续期。

**配完 HTTPS 后别忘了把 3000 端口从安全组关掉**——所有流量走 Nginx 443 端口进，不用再暴露 3000。

---

## 五、公益共享池配置实战

### 5.1 接入闲置 API

所有兼容 OpenAI 接口格式的订阅都能接入。步骤：

1. 后台 →「渠道管理」→「添加渠道」
2. 渠道类型选「OpenAI」
3. 填写 Base URL 和 API Key
4. 勾选支持的模型，点「测试」
5. 测试通过后保存

可以同时接入多个渠道。例如同时接入小米包月 + DeepSeek 余量 + 某个第三方中转。系统会自动负载均衡——单个渠道挂了不影响整体使用。

**渠道分组技巧：** 如果某些渠道只愿意分享给熟人、某些可以公开分享，用「渠道分组」功能做隔离。在创建令牌时指定只能访问哪个分组的模型。

### 5.2 生成安全分享令牌

这一步最关键——分享出去的不是原始密钥，是你生成的子令牌。

1. 后台 →「令牌管理」→「添加令牌」
2. **令牌名称：** 方便区分，如「7 月末共享-通用版」
3. **剩余额度：** 按人头设。例如总余量 1000 万，分给 10 人，每人设 80 万（留 200 万做缓冲）
4. **过期时间：** 统一设为**当月最后一天 23:59:59**，到点自动失效
5. **可使用模型：** 只勾选愿意分享的模型。高价模型（GPT-4o、Claude Opus 等）默认不开放
6. **IP 白名单（可选）：** 如果使用群体固定，可以加 IP 白名单进一步增强安全性
7. 点击提交，生成令牌字符串

### 5.3 发给群友

只需要发两样东西：

- **接口地址：** `https://你的域名/v1`（配了 HTTPS 的话）或 `http://你的IP:3000/v1`
- **API Key：** 刚生成的子令牌字符串

对方拿到后填到任意支持自定义 OpenAI 接口的客户端（ChatGPT-Next-Web、LobeChat、Cherry Studio 等）就能用。

**重要提醒：** 发之前测试一下——自己先在客户端里用子令牌调一次，确认能通再发。别发出去才发现令牌配错了。

---

## 六、小商业场景实操

同一套 New API 部署，不仅能做公益共享，还能支撑小规模商业分发。以下是三个已验证可行的场景。

### 6.1 场景一：小团队内部 API 管理

几个朋友合买一个 API 订阅，每个人用不同令牌、各自额度独立核算。

**配置方式：**
- 接入共享订阅到渠道
- 为每人创建独立令牌，额度按出资比例分配
- 所有人在各自的 AI 客户端填自己的令牌

**好处：** 谁用超了不影响别人，费用透明，月底直接看每个令牌的消耗统计就行，不用手动算账。

### 6.2 场景二：小规模客户 API 分发

接了几个小外包项目或者有几个稳定客户，需要给他们提供 API 接入。

**定价参考（2024 年末行情）：**

| 套餐 | 月费 | 包含额度 | 目标客户 |
|------|------|---------|---------|
| 体验版 | ¥15-20/月 | ¥8-10 等值 token | 轻度个人用户 |
| 标准版 | ¥30-50/月 | ¥20-35 等值 token | 日常高频使用 |
| 畅享版 | ¥80-120/月 | ¥60-90 等值 token | 重度开发调用 |

**配置方式：**
- 在「令牌管理」为每个客户创建令牌，额度 = 套餐额度
- 过期时间按月设（如 30 天后），续费后更新过期时间
- New API 后台支持自定义模型定价倍率，可以对不同模型设不同的利润率

**客户自助方案（进阶）：** New API 支持「在线支付」和「卡密兑换」功能。配上微信/支付宝支付后，客户可以自己充值、自己兑换，你只需要定期检查渠道余额——完全自动化运营。

### 6.3 场景三：多项目成本核算

同时跑好几个项目，每个项目用不同令牌，方便月底按项目统计 API 成本。

**配置方式：**
- 每个项目一个令牌，名称标注项目名
- 月初记录各令牌的初始额度
- 月底在「日志」页面按令牌筛选，导出用量报表
- 直接按实际消耗向甲方收费或内部记账

### ⚠️ 合规边界提醒

- 个人之间小范围公益共享、不涉及盈利，属于互助行为，风险低
- 小规模对外分发 API、收取合理服务费，属于技术服务范畴，一般没问题
- 不要以远低于上游官方的价格公开兜售 API 接入——可能违反上游厂商的服务协议
- 如果涉及支付收款，记得正常报税

---

## 七、核心功能全景

New API 不止是一个转发代理，它的功能覆盖了从接入到运营的完整链路。

<div style="background-color:transparent;box-sizing:border-box;padding:16px 0;font-family:'PingFang SC','Segoe UI',Arial,sans-serif;">
  <div style="text-align:center;margin-bottom:20px;">
    <h3 style="margin:0 0 6px 0;font-size:17px;font-weight:600;color:#1A1B1C;">New API 核心功能全景</h3>
    <p style="margin:0;font-size:13px;color:#6B7280;">从个人自用到商业化运营，一套系统全搞定</p>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
    <div style="background:#fff;border:1px solid #E4E3DD;border-radius:12px;padding:14px;">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
        <div style="width:28px;height:28px;border-radius:8px;background:#E8F4F9;display:flex;align-items:center;justify-content:center;font-size:14px;">🔌</div>
        <div style="font-weight:600;font-size:14px;color:#1A1B1C;">渠道接入层</div>
      </div>
      <div style="display:flex;flex-wrap:wrap;gap:6px;">
        <span style="background:#F4F3EE;border-radius:6px;padding:3px 8px;font-size:11px;color:#1A1B1C;">40+ AI厂商</span>
        <span style="background:#F4F3EE;border-radius:6px;padding:3px 8px;font-size:11px;color:#1A1B1C;">文本大模型</span>
        <span style="background:#F4F3EE;border-radius:6px;padding:3px 8px;font-size:11px;color:#1A1B1C;">图像生成</span>
        <span style="background:#F4F3EE;border-radius:6px;padding:3px 8px;font-size:11px;color:#1A1B1C;">语音/音乐</span>
        <span style="background:#F4F3EE;border-radius:6px;padding:3px 8px;font-size:11px;color:#1A1B1C;">本地模型</span>
        <span style="background:#F4F3EE;border-radius:6px;padding:3px 8px;font-size:11px;color:#1A1B1C;">权重负载均衡</span>
        <span style="background:#F4F3EE;border-radius:6px;padding:3px 8px;font-size:11px;color:#1A1B1C;">自动故障转移</span>
      </div>
    </div>
    <div style="background:#fff;border:1px solid #E4E3DD;border-radius:12px;padding:14px;">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
        <div style="width:28px;height:28px;border-radius:8px;background:#EDE8F8;display:flex;align-items:center;justify-content:center;font-size:14px;">🔑</div>
        <div style="font-weight:600;font-size:14px;color:#1A1B1C;">令牌管理</div>
      </div>
      <div style="display:flex;flex-wrap:wrap;gap:6px;">
        <span style="background:#F4F3EE;border-radius:6px;padding:3px 8px;font-size:11px;color:#1A1B1C;">无限子令牌</span>
        <span style="background:#F4F3EE;border-radius:6px;padding:3px 8px;font-size:11px;color:#1A1B1C;">额度限制</span>
        <span style="background:#F4F3EE;border-radius:6px;padding:3px 8px;font-size:11px;color:#1A1B1C;">有效期设置</span>
        <span style="background:#F4F3EE;border-radius:6px;padding:3px 8px;font-size:11px;color:#1A1B1C;">模型白名单</span>
        <span style="background:#F4F3EE;border-radius:6px;padding:3px 8px;font-size:11px;color:#1A1B1C;">IP白名单</span>
        <span style="background:#F4F3EE;border-radius:6px;padding:3px 8px;font-size:11px;color:#1A1B1C;">批量生成</span>
      </div>
    </div>
    <div style="background:#fff;border:1px solid #E4E3DD;border-radius:12px;padding:14px;">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
        <div style="width:28px;height:28px;border-radius:8px;background:#E8F5EA;display:flex;align-items:center;justify-content:center;font-size:14px;">💰</div>
        <div style="font-weight:600;font-size:14px;color:#1A1B1C;">计费与运营</div>
      </div>
      <div style="display:flex;flex-wrap:wrap;gap:6px;">
        <span style="background:#F4F3EE;border-radius:6px;padding:3px 8px;font-size:11px;color:#1A1B1C;">Token级精准计费</span>
        <span style="background:#F4F3EE;border-radius:6px;padding:3px 8px;font-size:11px;color:#1A1B1C;">自定义定价</span>
        <span style="background:#F4F3EE;border-radius:6px;padding:3px 8px;font-size:11px;color:#1A1B1C;">倍率设置</span>
        <span style="background:#F4F3EE;border-radius:6px;padding:3px 8px;font-size:11px;color:#1A1B1C;">在线支付</span>
        <span style="background:#F4F3EE;border-radius:6px;padding:3px 8px;font-size:11px;color:#1A1B1C;">卡密兑换</span>
        <span style="background:#F4F3EE;border-radius:6px;padding:3px 8px;font-size:11px;color:#1A1B1C;">邀请返利</span>
      </div>
    </div>
    <div style="background:#fff;border:1px solid #E4E3DD;border-radius:12px;padding:14px;">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
        <div style="width:28px;height:28px;border-radius:8px;background:#FDF0E6;display:flex;align-items:center;justify-content:center;font-size:14px;">📊</div>
        <div style="font-weight:600;font-size:14px;color:#1A1B1C;">监控与审计</div>
      </div>
      <div style="display:flex;flex-wrap:wrap;gap:6px;">
        <span style="background:#F4F3EE;border-radius:6px;padding:3px 8px;font-size:11px;color:#1A1B1C;">全量调用日志</span>
        <span style="background:#F4F3EE;border-radius:6px;padding:3px 8px;font-size:11px;color:#1A1B1C;">实时用量统计</span>
        <span style="background:#F4F3EE;border-radius:6px;padding:3px 8px;font-size:11px;color:#1A1B1C;">成功率监控</span>
        <span style="background:#F4F3EE;border-radius:6px;padding:3px 8px;font-size:11px;color:#1A1B1C;">延迟统计</span>
        <span style="background:#F4F3EE;border-radius:6px;padding:3px 8px;font-size:11px;color:#1A1B1C;">操作审计</span>
        <span style="background:#F4F3EE;border-radius:6px;padding:3px 8px;font-size:11px;color:#1A1B1C;">异常告警</span>
      </div>
    </div>
    <div style="background:#fff;border:1px solid #E4E3DD;border-radius:12px;padding:14px;">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
        <div style="width:28px;height:28px;border-radius:8px;background:#FCE8EC;display:flex;align-items:center;justify-content:center;font-size:14px;">👥</div>
        <div style="font-weight:600;font-size:14px;color:#1A1B1C;">用户与权限</div>
      </div>
      <div style="display:flex;flex-wrap:wrap;gap:6px;">
        <span style="background:#F4F3EE;border-radius:6px;padding:3px 8px;font-size:11px;color:#1A1B1C;">多租户体系</span>
        <span style="background:#F4F3EE;border-radius:6px;padding:3px 8px;font-size:11px;color:#1A1B1C;">角色分级</span>
        <span style="background:#F4F3EE;border-radius:6px;padding:3px 8px;font-size:11px;color:#1A1B1C;">邀请注册</span>
        <span style="background:#F4F3EE;border-radius:6px;padding:3px 8px;font-size:11px;color:#1A1B1C;">2FA双因素</span>
        <span style="background:#F4F3EE;border-radius:6px;padding:3px 8px;font-size:11px;color:#1A1B1C;">部门隔离</span>
      </div>
    </div>
    <div style="background:#fff;border:1px solid #E4E3DD;border-radius:12px;padding:14px;">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
        <div style="width:28px;height:28px;border-radius:8px;background:#E0E7F8;display:flex;align-items:center;justify-content:center;font-size:14px;">⚙️</div>
        <div style="font-weight:600;font-size:14px;color:#1A1B1C;">高级特性</div>
      </div>
      <div style="display:flex;flex-wrap:wrap;gap:6px;">
        <span style="background:#F4F3EE;border-radius:6px;padding:3px 8px;font-size:11px;color:#1A1B1C;">模型映射别名</span>
        <span style="background:#F4F3EE;border-radius:6px;padding:3px 8px;font-size:11px;color:#1A1B1C;">Claude思考模式</span>
        <span style="background:#F4F3EE;border-radius:6px;padding:3px 8px;font-size:11px;color:#1A1B1C;">缓存控制</span>
        <span style="background:#F4F3EE;border-radius:6px;padding:3px 8px;font-size:11px;color:#1A1B1C;">流式输出</span>
        <span style="background:#F4F3EE;border-radius:6px;padding:3px 8px;font-size:11px;color:#1A1B1C;">重试机制</span>
      </div>
    </div>
  </div>
</div>

---

## 八、踩坑实录

以下是搭建和运维中真实遇到过的坑，帮你节省排查时间。

### 坑1：MySQL 容器无限重启，健康检查失败

**现象：** `docker compose up -d` 后 MySQL 反复重启，new-api 容器一直等 MySQL 就绪但等不到。

**根因：** 权限问题。MySQL 数据目录 `./mysql-data` 如果之前被 root 用户创建过，容器内的 mysql 用户没有写入权限。

**解决：**
```bash
sudo chown -R 999:999 ./mysql-data   # 999 是容器内 mysql 用户的 UID
```

如果问题依旧，删掉数据目录重新初始化：
```bash
docker compose down -v   # -v 会删除数据卷，谨慎
docker compose up -d
```

### 坑2：数据库密码含特殊字符导致连接失败

**现象：** new-api 日志报 `SQL_DSN` 连接错误，但密码确认没写错。

**根因：** `SQL_DSN` 是 URL 格式，密码中的 `@ : / ? # [ ] %` 需要 URL 编码，否则解析错误。

**解决：** 数据库密码只用纯字母数字。用 `openssl rand -hex 16` 生成的就是这种格式。

### 坑3：配了 HTTPS 后 API 调用全部 502

**现象：** 浏览器访问域名正常，但客户端调 API 报 502 Bad Gateway。

**根因：** Docker 的 `ports: "3000:3000"` 绑定在 `0.0.0.0:3000`，但 Nginx `proxy_pass http://127.0.0.1:3000` 走的是 lo 接口。某些云服务器上 Docker 默认不监听 lo。

**解决：** 确认 New API 容器在监听：

```bash
docker compose exec new-api netstat -tlnp | grep 3000
# 应该看到 0.0.0.0:3000 或 :::3000
```

如果连接不上，改用 Docker 内部网络——在 docker-compose.yml 的 new-api 服务中去掉 `ports`，在 Nginx 配置里用 `proxy_pass http://new-api:3000;`（容器名作为主机名），然后给 Nginx 也加到同一个 compose 网络里。

**更简单的方式：** 直接用 `proxy_pass http://172.17.0.1:3000;`（Docker 默认网桥网关），不用改 compose。

### 坑4：忘记关 3000 端口导致被扫

**现象：** 服务器流量异常，日志里大量来自陌生 IP 的请求。

**根因：** 配完 Nginx HTTPS 后忘了从安全组里关掉 3000 端口，New API 直接暴露在公网上。自动化扫描脚本找到 3000 端口后不断尝试弱密码登录。

**解决：**
1. 立刻去云控制台安全组删除 3000 端口的入站规则
2. 改掉管理员密码为强密码
3. 打开 New API 后台的 2FA 双因素认证

**教训：** Nginx HTTPS 配完后的第一步就应该是关掉 3000 端口——所有流量走 Nginx 443。New API 管理后台绝对不要裸奔在公网上。

### 坑5：pandoc 生成的 HTML 中表格溢出移动端

**现象：** 手机上打开文章，表格撑爆屏幕宽度，需要横滑但体验很差。

**根因：** 内容中的 `<table>` 没有包裹 overflow wrapper，移动端没有横向滚动机制。

**解决：** 文章发布时对所有 `<table>` 加 overflow wrapper——这个已纳入经验分享发布技能的标准样式修正步骤，不会遗漏。

---

## 九、安全加固 checklist

部署完成 ≠ 完事。以下 6 项加固做得越多，睡得越踏实。

| 序号 | 加固项 | 操作 | 必要性 |
|------|--------|------|--------|
| 1 | **关闭 3000 端口** | 安全组删除 3000 入站规则 | 🔴 必须 |
| 2 | **配置 HTTPS** | Nginx + Certbot，强制 SSL | 🔴 必须 |
| 3 | **启用 2FA** | New API 后台 → 个人设置 → 双因素认证 | 🟡 强烈建议 |
| 4 | **改 SSH 端口** | `/etc/ssh/sshd_config` 改 22 为高位端口 | 🟡 建议 |
| 5 | **数据库定期备份** | `docker exec new-api-mysql mysqldump ... > backup.sql` | 🟡 建议 |
| 6 | **设置令牌 IP 白名单** | 给每个令牌指定允许的来源 IP | 🟢 进阶 |

---

## 十、成本分析

| 项目 | 费用 | 说明 |
|------|------|------|
| 云服务器 | ¥50-70/月 | 腾讯云/阿里云轻量 2C2G |
| 域名 | ¥30-60/年 | .cn 首年几块钱 |
| SSL 证书 | 免费 | Let's Encrypt 自动续期 |
| 流量 | 基本免费 | API 调用流量很小，轻量服务器免费额度够用 |
| New API | 免费 | MIT 开源协议 |
| **月度总成本** | **约 ¥55-80** | 含域名摊销 |

> 公益共享池 10 人分摊，每人每月不到 ¥6。小商业场景下，一个客户月费 ¥30 就能覆盖全部成本 + 有利润。

---

## 十一、运维 checklist

每天 30 秒 + 每周 1 分钟 + 每月 2 分钟：

**每日（30 秒）：** 后台看一眼总用量和剩余额度。某令牌用量异常飙升 → 立刻吊销。

**每周（1 分钟）：** 测试各渠道连通性（后台点测试按钮）。挂掉的渠道及时下线。

**每月第一天（2 分钟）：** 上月令牌已自动过期，生成本月新令牌。备份数据库：

```bash
docker exec new-api-mysql mysqldump -uroot -p'你的密码' new_api > backup-$(date +%Y%m).sql
```

把备份文件下载到本地——别只放在服务器上，服务器故障一起丢。

---

## 十二、常见问题

**问：对方拿到子令牌能反查我的原始 Key 吗？**

不能。调用链路是「用户 → New API → 上游渠道」，子令牌是 New API 自己生成的凭证，用户在任何一个环节都接触不到上游原始 Key。

**问：多个渠道同时用，费用怎么算？**

New API 不修改上游计费逻辑，是透明代理。上游扣多少就是多少。但 New API 有自己的「倍率」系统——你可以对上游 $1 的成本设 1.5x 倍率，让客户看到 $1.5 的消耗，差价就是你的利润。

**问：有没有免费的部署方式？**

Railway、Render 有免费额度但不够跑 MySQL + Redis + New API 三个容器。最省钱的方案还是轻量云服务器 ¥50/月，而且所有 side project 都能扔上去。

**问：能限制每人每天的调用次数吗？**

New API 原生支持总量限制和过期时间限制。按日/IP 限频需要额外在 Nginx 层面配 rate limiting。

**问：和 ChatGPT-Next-Web 这类客户端冲突吗？**

不冲突。New API 是后端网关，Next-Web 是前端 UI，刚好搭配。在 Next-Web 里填 New API 的接口地址 + 子令牌就行。

**问：New API 和 one-api 是什么关系？**

New API 是 one-api 的社区增强版（fork 后大量改进），原作者 songquanpeng 的 one-api 更新已放缓。New API 新增了多模态支持、商业运营功能、更好的 UI。新部署的话选 New API。

**问：如果上游渠道被封了怎么办？**

所有渠道的原始 Key 都在你手里，换一个上游供应商重新添加渠道就行，子令牌完全不用动——使用者无感知。这就是多加一层中转的好处：对于下游用户，上游换了哪家供应商他们完全不知道也不关心。

---

## 最后

有额度闲置分享是好事，但直接发原始 Key 就像把银行卡密码贴到群里——不是不信任大家，是没必要冒这个风险。加一层 New API 中转，花一次部署的时间，换长期安心。

公益共享也好，小团队管理也好，甚至接几个小外包项目也好，同一套方案都能覆盖。希望这篇文章能让更多人既分享资源，又保护好自己。

有问题去 New API 的 GitHub Issues 搜或提，社区响应很快。搭建遇到卡点也可以来评论区交流。

---

> New API 项目地址：[github.com/Calcium-Ion/new-api](https://github.com/Calcium-Ion/new-api)
> 
> 本文涉及的 docker-compose.yml 完整配置可在此处复制：[配置直达链接]
