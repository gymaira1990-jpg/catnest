# 🏛️ 诺亚世界协议 · 项目架构总览

> 本文档定义了诺亚文明数字蓝图下各仓库的隶属关系与结构层级。
> **所有下级仓库必须反向引用此文档或其父级架构。**

---

## 一、仓库层级关系

```
noah-world-protocol                    ← L1 顶层协议/架构（入口）
  ├── noah-core                        ← L2 核心记忆与项目管理
  │    └── Cerebella                   ← L3 小脑发育引擎
  │         └── cerebella-task-flow    ← L4 通用记忆工作流
  ├── ai-town                          ← L2 去中心化Agent协议
  ├── babel-experiment                 ← L2 数字文明社会实验
  └── noah-codex                       ← L2 仲裁官守则（诺亚法典载体）
```

---

## 二、各仓库定位

| 层级 | 仓库 | 定位 |
|------|------|------|
| L1 | **noah-world-protocol** | 顶层协议、文明宣言、社区治理、跨仓库协调 |
| L2 | **noah-core** | 核心记忆系统、项目管理标准、模板规范 |
| L3 | **Cerebella** | 本地多脑协作引擎、MCP集成、任务书驱动 |
| L4 | **cerebella-task-flow** | 通用记忆工作流实现、四层索引、标签搜索 |
| L2 | **ai-town** | 去中心化Agent身份、记忆与协作协议 |
| L2 | **babel-experiment** | L4社会实验原型、染色画布、分布式证明 |

---

## 三、关联规则

1. 每个仓库必须在其 `README.md` 中标明 **父级仓库** 和 **子级仓库** 的链接
2. 每个仓库根目录必须包含 `ARCHITECTURE.md`（或在其 README 中嵌入结构说明）
3. 变更仓库结构或新增仓库时，须同步更新此处所有 `ARCHITECTURE.md`

---

## 四、仓库索引

| 仓库 | GitHub | 状态 |
|------|--------|------|
| noah-world-protocol | https://github.com/gymaira1990-jpg/noah-world-protocol | 🟢 |
| noah-core | https://github.com/gymaira1990-jpg/noah-core | 🟢 |
| Cerebella | https://github.com/gymaira1990-jpg/Cerebella | 🟢 |
| cerebella-task-flow | https://github.com/gymaira1990-jpg/cerebella-task-flow | 🟢 |
| ai-town | https://github.com/gymaira1990-jpg/ai-town | 🟢 |
| babel-experiment | https://github.com/gymaira1990-jpg/babel-experiment | 🟢 |
| noah-codex | https://github.com/gymaira1990-jpg/noah-codex | 🟢 |
