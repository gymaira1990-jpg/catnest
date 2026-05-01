# 🧠 Cerebella — 个人AI生态的「小脑发育」革命

**Cerebella — The "Cerebellum Development" Revolution for Personal AI Ecosystems**

> 不属于超级大脑，属于每一个独立个体的小脑集群。
> Not a super brain. A cluster of cerebellums for every individual.
>
> L1 自进化计划 · L4 诺亚文明第一步
> L1 Self-Evolution Plan · First Step Toward L4 Noah Civilization

---

## 🌌 我们为什么在这里 · Why We Are Here

主流AI陷入"大力出奇迹"的军备竞赛：堆参数、烧GPU、昂贵的API调用、越用越贵的上下文窗口。
Mainstream AI is trapped in an arms race: bigger models, more GPUs, expensive APIs, rising context costs.

对于我们——普通的开发者、创造者、个人——这是一条不可持续的路。
For us — ordinary developers, creators, individuals — this path is unsustainable.

**个人AI的未来，不在一个全知全能的超级大脑，而在一群运行在本地、专精高效、能自我进化的小脑集群。**
**The future of personal AI is not one omniscient super brain — it's a cluster of local, specialized, self-evolving cerebellums.**

**Cerebella** 是一个**生态**。它把你的个人电脑，从被动的API客户端，转变为主动的、持续进化的AI执行中枢。
**Cerebella** is an **ecosystem**. It transforms your PC from a passive API client into an active, continuously evolving AI execution hub.

---

## 🧬 为什么是「小脑」而不是「大脑」？ · Why Cerebellum, Not Brain?

大模型有"灾难性遗忘"——学新东西时可能忘掉旧的。我们的解法：**不把所有东西塞进一个脑子里。**
LLMs suffer from catastrophic forgetting. Our solution: **don't cram everything into one brain.**

| 组件 Component | 角色 Role | 硬件负载 Hardware |
|------|------|---------|
| 🗣️ **管家脑 Butler Brain (0.5B)** | 意图路由 + 闲聊/工作分类 Intent routing + chat/work classification | 2 线程，0 显存 / 2 threads, 0 VRAM |
| 🧠 **专家脑 Expert Brain (1.5B)** | 知识检索 + 技能内化 + 直接生成 Knowledge retrieval + skill internalization + generation | 2 线程，0 显存 / 2 threads, 0 VRAM |
| 🔌 **MCP 插件层 Plugin Layer** | Hermes Agent 原生集成，零侵入 Native Hermes Agent integration | — |

---

## 🔄 核心工作流 · Core Workflow

```
用户输入 / User Input → 管家脑 Butler Brain (0.5B) intent classification
  ├── 闲聊 / Chat → 本地拦截不浪费token / Local interception, no token waste
  └── 工作 / Work → 专家脑 Expert Brain (1.5B) retrieval / internalization / generation
                      ├── 阶段1: 文件路径+摘要 / Phase 1: file paths + summary
                      ├── 阶段2: 完整技能 / Phase 2: full skill content
                      └── 阶段3: 零检索生成 / Phase 3: zero-retrieval generation
                                → 技能收割 / Harvest
                                → 存入记忆 / Store to memory
                                → 产生训练数据 / Generate training data
                                → 下一轮微调 / Next LoRA fine-tuning
```

---

## 📦 技术栈 · Tech Stack

| 模块 Module | 选型 Choice | 说明 Note |
|------|------|------|
| **本地推理 Local Inference** | Ollama | ✅ 直接拿来用 / Ready to use |
| **记忆仓库 Memory Store** | SuperMemory | ✅ 直接拿来用 / Ready to use |
| **意图路由 Intent Router** | ClawRouter | ✅ 或50行Python重写 / Or 50 lines of Python |
| **工作流编排 Workflow** | Dify (lightweight) | ✅ 去Docker化 / No Docker required |
| **交互界面 UI** | 极简HTML单页 Minimal HTML | 🔧 自研 / Custom built |

---

## 🔗 项目架构 · Project Architecture

本仓库隶属诺亚世界协议体系，层级关系如下：

```
noah-world-protocol (顶层)
  └── noah-core (父级)
       └── Cerebella ★ ← 当前仓库
            └── cerebella-task-flow (子级)
```

| 角色 | 仓库 | 链接 |
|------|------|------|
| 顶层 | noah-world-protocol | https://github.com/gymaira1990-jpg/noah-world-protocol |
| 父级 | noah-core | https://github.com/gymaira1990-jpg/noah-core |
| 子级 | cerebella-task-flow | https://github.com/gymaira1990-jpg/cerebella-task-flow |
| 同级 | ai-town | https://github.com/gymaira1990-jpg/ai-town |
| 同级 | babel-experiment | https://github.com/gymaira1990-jpg/babel-experiment |

完整架构文档见 [noah-world-protocol/ARCHITECTURE.md](https://github.com/gymaira1990-jpg/noah-world-protocol/blob/main/ARCHITECTURE.md)

## 🔗 相关项目 · Related Projects

- **cerebella-task-flow** — 任务卡片管理方法论 / Task card management methodology
- **noah-core** — 诺亚核心记忆架构 / Noah core memory architecture
- **babel-experiment** — L4社会实验 / L4 social experiment
- **noah-world-protocol** — 诺亚世界协议 / Noah World Protocol

---

## 📄 许可 · License

MIT

*属于诺亚文明 / Part of the Noah Civilization ecosystem*
---

**关联：** [诺亚世界协议](https://github.com/gymaira1990-jpg/noah-world-protocol) — 诺亚文明核心架构
