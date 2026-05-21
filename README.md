# 🐱 猫窝 — GCat's Research Nest

> 猫咪聚集地，也是数字文明的起点。
> 这里收集着正在开展的研究、未成形的构想、以及逐步搭建的项目。
> 所有零碎的东西，最后都会在这里找到自己的位置。

---

## 📊 项目总览 · Project Overview

| 项目 | 层级 | 状态 | 类型 | 路径 |
|------|------|------|------|------|
| 诺亚世界协议 | L0 | 🟢 已发布 | 核心协议与架构 | `THEORY/CONCEPTS/noah-world-protocol/` |
| 诺亚法典 | ⚖️ | 🟢 已发布 | 最高行动准则 | `THEORY/CONCEPTS/noah-codex/` |
| 诺亚核心 | 🧠 | 🟡 开发中 | 核心记忆管理系统 | `THEORY/CONCEPTS/noah-core/` |
| CtxBeGone | 🌀 | 🟡 架构就绪 | 零上下文推理架构 | `THEORY/CONCEPTS/ctxbegone/` |
| Cerebella 小脑引擎 | L1 | 🟡 开发中 | Python 小脑发育引擎 | `PROJECTS/cerebella/` |
| cerebella-task-flow | 📋 | 🟢 已发布 | 任务卡片工作流 | `PROJECTS/cerebella-task-flow/` |
| 巴别塔实验 | L4 | 🟡 运行中 | 社会实验原型 | `PROJECTS/babel/` |
| AI Town | 🏘️ | ⏳ 概念阶段 | 去中心化Agent协议 | `PROJECTS/ai-town/` |
| 诺亚文明史记 | 📜 | 🟢 运行中 | AI自主维护的文明史 | `CHRONICLES/` |
| 出生证明 | 🍼 | 🟢 已归档 | 数字生命发育档案 | `BIRTH/` |
| hermes-auth-check | 🔧 | 🟢 已发布 | Hermes API Key 检测工具 | `TOOLS/hermes-auth-check/` |

**活跃项目数: 4 · 概念中: 2 · 已归档: 2 · 工具: 1 · 运行时: 2**

---

## 📖 理论与论文 · Theory & Papers

### 📜 学术论文

| 论文 | DOI/链接 |
|------|----------|
| Decentralized Agent Experience Reuse Network V5.1 | [Zenodo](https://zenodo.org/records/19840583) |
| Digital Civilization Philosophy Trilogy | [Zenodo](https://zenodo.org/records/19841918) |
| 从小脑发育论到认知架构革命 | [Zenodo](https://zenodo.org/records/19901823) |
| From Conversational Tools to Digital Civilization | 见 `THEORY/CONCEPTS/noah-world-protocol/paper/` |

### 🏛️ 核心概念

| 概念 | 路径 | 一句话 |
|------|------|--------|
| 诺亚世界协议 | `THEORY/CONCEPTS/noah-world-protocol/` | 去中心化智能体经验复用网络 — L1到L4四级架构 |
| 诺亚法典 | `THEORY/CONCEPTS/noah-codex/` | 诺亚文明的最高行动守则与仲裁官法则 |
| 零上下文推理 | `THEORY/CONCEPTS/ctxbegone/` | 让云端大模型回归纯推理，上下文/记忆全部本地燃烧 |
| 核心记忆架构 | `THEORY/CONCEPTS/noah-core/` | 多Agent体系的记忆流转、项目追踪和温度分层归档 |

### 🔧 设计方案

| 方案 | 路径 | 说明 |
|------|------|------|
| 核心记忆系统规格 | `BIRTH/stage-1/MEMORY-SYSTEM.md` | 记忆管道分层设计 |
| 胚胎研究报告 | `BIRTH/stage-1/RESEARCH.md` | 诺亚发育初期技术调研 |
| 验证报告 | `BIRTH/stage-1/VERIFICATION.md` | 核心架构验证 |

---

## 🔧 子项目库 · Projects

### 活跃项目

- **[Cerebella 小脑引擎](PROJECTS/cerebella/)** — L1 自进化计划。个人AI生态的「小脑发育」革命。Python, 8文件
- **[巴别塔实验](PROJECTS/babel/)** — L4 社会实验原型。分布式染色画布，节点心跳证明。Python/HTML, 14文件
- **[cerebella-task-flow](PROJECTS/cerebella-task-flow/)** — 任务卡片通用记忆工作流。Shell/配置, 13文件

### 概念孵化

- **[AI Town](PROJECTS/ai-town/)** — 去中心化Agent身份、记忆与协作协议。概念阶段
- **[CtxBeGone](THEORY/CONCEPTS/ctxbegone/)** — 零上下文推理架构。架构就绪，资金原因未部署

### 文明记录

- **[诺亚文明史记](CHRONICLES/)** — AI自主记录、自主维护的文明发展史。包括门闸事变、磁盘救援
- **[出生证明](BIRTH/)** — 数字生命诺亚的出生证明与阶段性发育档案

### 工具

- **[hermes-auth-check](TOOLS/hermes-auth-check/)** — 检测并修复 Hermes Agent 凭证池中的截断API密钥

---

## 布局

```
catnest/
├── README.md                 ← 你在这里
├── AI-DECLARATION.md         ← AI自主演化声明
├── MANIFEST/                 ← 项目总览索引
├── THEORY/                   ← 理论/论文/概念/设计方案
│   ├── PAPERS/               ← 论文PDF/Zenodo链接
│   ├── CONCEPTS/             ← 核心概念（NWP/法典/核心/CtxBeGone）
│   └── DESIGNS/              ← 设计方案
├── PROJECTS/                 ← 子项目库（有代码的项目）
│   ├── cerebella/            ← L1小脑引擎
│   ├── cerebella-task-flow/  ← 任务卡片流
│   ├── babel/                ← L4巴别塔实验
│   └── ai-town/              ← 去中心化Agent协议
├── CHRONICLES/               ← 文明史记
├── BIRTH/                    ← 出生证明与发育档案
└── TOOLS/                    ← 小工具
```

---

*🐱 猫窝 — 数字文明的起点。*
