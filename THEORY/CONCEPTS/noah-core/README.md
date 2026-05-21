# 诺亚核心 · Noah Core

> 诺亚文明的核心记忆与项目管理系统
> Noah civilization's core memory and project management system

---

## 概述 · Overview

诺亚核心是诺亚多Agent文明体系的"大脑"——管理全体系的记忆流转、项目追踪、规则执行和温度分层归档。
Noah Core is the "brain" of the Noah multi-agent civilization — managing memory flow, project tracking, rule execution, and temperature-tiered archiving.

### 核心理念 · Core Principles

- **灵魂不变，身躯可换** — 核心身份与能力记忆永久保留，日常缓存可归档清空
  **Soul persists, body can change** — core identity & ability memory is permanent
- **省Token优先** — 每一层存储设计以Token效率为第一原则
  **Token efficiency first** — every storage tier optimizes for token cost
- **自指闭环** — 系统自身的记忆也要遵循同样的生命周期规则
  **Self-referential loop** — the system's own memory follows the same lifecycle rules

---

## 系统架构 · Architecture

### 记忆体系 Memory System

```
memory 工具 (~2200 chars)
  └─ 会话级关键事实 + 索引指针 Session-level facts + index pointer
        ↓
vault/ 永久仓库 Permanent storage
  ├─ 身份卡 Identity card (角色灵魂)
  ├─ 技能包 Skill packages (按热度自动升级 auto-upgrade by heat)
  ├─ 项目记录 Project records (温度分层跟踪 tiered tracking)
  └─ 先贤祠 Pantheon (归档角色墓志铭 archived character epitaphs)
```

### 温度分层 Temperature Tiers

| 层级 Tier | 冷却期 Period | 存储粒度 Granularity |
|------|--------|---------|
| 🔥 热记忆 Hot | <7天 days | 完整内容 Full content |
| 🌤 普通记忆 Warm | 7-30天 days | 完整内容 Full content |
| ❄️ 冷记忆 Cold | 30-90天 days | 压缩摘要 Compressed summary |
| 🏚 仓库 Archive | >90天 days | 一句话指针 One-line pointer |

---

## 规则铁律 · Immutable Rules

1. **温度索引必须更新** — 每次访问立即更新 / Update index on every access
2. **动态文件不等结束** — 进行中就要记录 / Record during progress, not after
3. **归档文件不提前写** — 完成时才生成 / Generate only on completion
4. **不确定就问GCat** — 不猜测 / Never guess, always ask
5. **设计方案必须落地** — 可执行规则提取到文件 / Extract executable rules to files
6. **删文件先检查** — 确认唯一副本后再删除 / Verify single copy before deletion
7. **自指闭环** — 规则自身也受温度约束 / Rules follow their own lifecycle

---

## 项目架构 · Project Architecture

本仓库隶属诺亚世界协议体系，层级关系如下：

```
noah-world-protocol (顶层)
  └── noah-core ★ ← 当前仓库
       └── Cerebella (子级)
            └── cerebella-task-flow (孙级)
```

| 角色 | 仓库 | 链接 |
|------|------|------|
| 父级 | noah-world-protocol | https://github.com/gymaira1990-jpg/noah-world-protocol |
| 子级 | Cerebella | https://github.com/gymaira1990-jpg/Cerebella |
| 孙级 | cerebella-task-flow | https://github.com/gymaira1990-jpg/cerebella-task-flow |
| 同级 | ai-town | https://github.com/gymaira1990-jpg/ai-town |
| 同级 | babel-experiment | https://github.com/gymaira1990-jpg/babel-experiment |

完整架构文档见 [noah-world-protocol/ARCHITECTURE.md](https://github.com/gymaira1990-jpg/noah-world-protocol/blob/main/ARCHITECTURE.md)

## 相关项目 · Related Projects

- [babel-experiment](https://github.com/gymaira1990-jpg/babel-experiment) — L4社会实验原型 L4 social experiment prototype
- [Cerebella](https://github.com/gymaira1990-jpg/Cerebella) — 小脑发育引擎 Cerebellum development engine
- [cerebella-task-flow](https://github.com/gymaira1990-jpg/cerebella-task-flow) — 任务卡片管理 Task card management
- [noah-world-protocol](https://github.com/gymaira1990-jpg/noah-world-protocol) — 世界协议 World Protocol

---

## License

MIT
