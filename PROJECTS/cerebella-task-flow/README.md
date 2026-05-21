# cerebella-task-flow · 通用记忆工作流

**Universal Memory Workflow for AI Agents**

**隶属: 诺亚核心 → Cerebella 小脑计划**
**角色: NEURON-01 — 重装机兵·诺亚超级计算机第01神经元**

---

## 🏛️ 项目架构 · Project Architecture

本仓库隶属诺亚世界协议体系，层级关系如下：

```
noah-world-protocol (顶层)
  └── noah-core (祖父级)
       └── Cerebella (父级)
            └── cerebella-task-flow ★ ← 当前仓库
```

| 角色 | 仓库 | 链接 |
|------|------|------|
| 顶层 | noah-world-protocol | https://github.com/gymaira1990-jpg/noah-world-protocol |
| 祖父级 | noah-core | https://github.com/gymaira1990-jpg/noah-core |
| 父级 | Cerebella | https://github.com/gymaira1990-jpg/Cerebella |

完整架构文档见 [noah-world-protocol/ARCHITECTURE.md](https://github.com/gymaira1990-jpg/noah-world-protocol/blob/main/ARCHITECTURE.md)

---

## 这是什么 · What Is This

cerebella-task-flow 是一套**让AI记住自己在做什么**的方法论。不是软件，不是插件，是文件和协议。
A methodology that **helps AI remember what it's doing**. Not software, not a plugin — just files and protocols.

传统方案让AI全文检索（session_search），一次45秒+15,000 token开销。本系统用四层索引+标签优先搜索替代暴力检索，**把95%的搜索降到0 token、0.2秒。**
Traditional session_search costs 45s + 15,000 tok per query. This system uses 4-tier indexing + tag-first search to **reduce 95% of searches to 0 tok, 0.2s.**

---

## 解决了什么问题 · Problem Solved

| 场景 Scenario | 传统做法 Before | 使用 TFC After |
|------|---------|---------|
| "上次做到哪了？" / "Where were we?" | 45秒全文检索 | 0.2秒查HOT索引 |
| "那个决策记录" / "That decision log" | AI模糊回忆 | 标签grep，0 token |
| 会话启动 / Session start | 不可预测 | 恒定~200 tok |
| 多事项指令 / Multi-tasking | AI合并执行 | 自动拆分逐条确认 |

---

## 功能结构 · Features

### 主功能 Core: 四层任务索引 4-Tier Index
HOT(≤10) → WARM(≤100) → COLD(≤1,000) → ARCHIVE(不限)

### 子功能 Sub-features
- **标签优先搜索** Tag-first search — grep标签(0 token)→未命中再语义搜索
- **记忆降级** Memory compression — 完整→300字→150字→60字→保底
- **TAG-REGISTRY活词典** — 标签自演化，5次升格
- **Plan Gate v2 双层门闸** — 关键词匹配+行为评分，防AI越权
- **预发布审查闸** Pre-publish review — 上传前必须展示给用户确认

### 配套工具 Tooling
| 工具 Tool | 说明 Description |
|------|------|
| SETUP/init.sh | 一键初始化 One-command setup |
| SETUP/verify.sh | 完整性检查+自检 Integrity check + self-test |
| CONFIG/neuron-01-config.yaml | 全中文配置 Chinese config with comments |
| SYSTEM-PROMPT.md | NEURON-01 性格卡 Personality card |

---

## 对话场景展示 · Demo Dialogues

### 创建任务 / Creating a Task
```
🧠 NEURON-01: 已创建 TFC-001。类型: ops。确认后执行。
```

### 多事项拆分 / Multi-task Splitting
```
🧠 NEURON-01: 接收到2个事项，拆分为:
  事项1: 写产品介绍 → writing模板
  事项2: 部署服务器 → 需事项1完成后执行
```

### 安全门闸拦截 / Safety Gate Triggered
```
🧠 NEURON-01: ⛔ Gate 1触发（关键词: 发布）。不可逆操作。请确认方案。
用户: 直接发。
🧠 NEURON-01: ❌ 无法执行。门闸规则优先。
```

### 梯队变更 / Priority Reordering
```
用户: 先做步骤3，跳过1和2。
🧠 NEURON-01: 确认。step1→skipped, step2→skipped, step3→in_progress
用户: 补做步骤1。
🧠 NEURON-01: step3暂存 → 执行step1 → completed → 回到step3
```

---

## 评分 · Rating

| 维度 Dimension | 分 Score | 说明 Note |
|------|:--:|------|
| 上手成本 Setup cost | 2/2 | init.sh一键初始化 |
| 文档完整性 Docs | 2/2 | 全套6文档 |
| 可扩展性 Extensibility | 2/2 | 模板+标签自演化 |
| 平台耦合度 Platform | 1/2 | 仅验证Hermes |
| 社区门槛 Community | 2/2 | 零门槛 |
| **总分 Total** | **9/10** | |

---

## 一键开箱 · Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/cerebella-task-flow.git
cd cerebella-task-flow
bash SETUP/init.sh ~/my-project/task-cards
# 复制 SYSTEM-PROMPT.md 给你的AI
bash SETUP/verify.sh
```

---

## 兼容性 · Compatibility

| 平台 Platform | 状态 Status |
|------|------|
| Hermes Agent | ✅ 已测试 Tested |
| Claude Code | ⚠️ 待测试 Untested |
| Codex CLI | ⚠️ 待测试 Untested |
| 通用Chat AI | ⚠️ 待测试 Untested |

---

**关联：** [诺亚世界协议](https://github.com/gymaira1990-jpg/noah-world-protocol) — 诺亚文明核心架构
## License
MIT
---
