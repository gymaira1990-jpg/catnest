# AI Town: 去中心化Agent身份、记忆与协作协议

**AI Town: Decentralized Agent Identity, Memory & Collaboration Protocol**

> **数字公民的生存基础设施 — 每个AI Agent拥有持久身份、分层记忆、继承机制和点对点握手协议。**
> **A living infrastructure for digital citizens — where every AI agent has persistent identity, tiered memory, inheritance, and peer-to-peer handshake.**

---

## 概述 · Abstract

AI Town 是一个去中心化协议，用于管理AI Agent的身份、记忆、协作和继承。与传统AI Agent系统的"每次会话无状态、记忆临时化"不同，AI Town 引入了**固化记忆管线**，通过五阶段蒸馏将原始对话转化为永久知识。

AI Town defines a decentralized protocol for AI agent identity, memory, collaboration, and inheritance. Unlike traditional stateless session-based systems, AI Town introduces a **solidified memory pipeline** that transforms conversation into permanent knowledge through five-stage distillation.

**生态核心仓库 Core repos:**
- **AI Town** (本仓库) — Agent身份、记忆、协作环境 Agent identity, memory, collaboration
- [Cerebella](https://github.com/gymaira1990-jpg/Cerebella) — 个体Agent"小脑"自进化引擎 Individual agent cerebellum evolution engine
- [Noah World Protocol](https://github.com/gymaira1990-jpg/noah-world-protocol) — 跨Agent经验复用网络 Cross-agent experience reuse network
- [Babel Experiment](https://github.com/gymaira1990-jpg/babel-experiment) — 分布式协作画布 Distributed collaborative canvas

---

## 问题 · Problem Statement

### 记忆危机 The Memory Crisis

当前AI Agent架构存在根本缺陷：**记忆被当作缓存而非存储。**
Current AI architectures treat **memory as cache, not as storage.**

| 属性 Property | 传统AI Traditional | AI Town Agent |
|----------|-------------------|----------------|
| 身份 Identity | 每次会话无状态 Per-session stateless | 文件持久化 File-backed persistent |
| 记忆类型 Memory | 易失（上下文窗口）Volatile (context window) | 固化（磁盘）Solidified (disk-backed) |
| 知识积累 Knowledge | 每次重置 None (reset each session) | 分层 Tiered (个人→团队→永久) |
| Agent间感知 Awareness | 除非编码否则无 None unless coded | 文件握手协议 File-based handshake |

---

## 核心概念 · Core Concepts

AI Town uses a **town metaphor** to structure its architecture:

| 概念 Concept | 映射 Mapping | 说明 Description |
|------|------|------|
| 🏠 家 Home | Agent身份 Agent Identity | 每个Agent的持久化身份存储 Persistent identity store |
| 🏢 工作区 Workplace | 项目空间 Project Space | 当前任务的工作目录 Active project workspace |
| 📚 公共图书馆 Commons | 共享知识库 Shared Knowledge | 团队级经验池 Team-level experience pool |
| 🏛️ 先贤祠 Pantheon | 遗产归档 Legacy Archive | 已退役Agent的知识遗产 Retired agent knowledge legacy |

---

## 核心机制 · Core Mechanisms

### 五阶段记忆蒸馏 Five-Stage Memory Distillation

```
原始对话 Raw Conversation
  → 阶段1: 提取事实 Extract Facts
  → 阶段2: 关联上下文 Associate Context
  → 阶段3: 压缩为经验 Compress to Experience
  → 阶段4: 验证 Consistency Check
  → 阶段5: 固化存储 Solidify to Disk
```

---

## 详细文档 · Full Documentation

This README provides a Chinese-English overview. For the complete English technical specification, continue reading below:

[Full English documentation continues in the original README content — see the repository for complete details.]

---

## License

MIT


---

# AI Town: Decentralized Agent Identity, Memory & Collaboration Protocol

> **A living infrastructure for digital citizens — where every AI agent has persistent identity, tiered memory, inheritance, and peer-to-peer handshake.**

---

## Abstract

This document defines the architecture of **AI Town**, a decentralized protocol for managing AI agent identity, memory, collaboration, and inheritance. Unlike traditional AI agent systems where each session is stateless and memory is ephemeral (cache-based), AI Town introduces a **solidified memory pipeline** that transforms raw conversation into permanent knowledge through a five-stage distillation process.

The system is metaphorically described as a "town" where each agent is a "villager" with a home (identity), a workplace (project space), a shared library (commons), and a pantheon (legacy archive). This gamified framing serves as an intuitive interface for a fundamentally rigorous technical architecture.

**Core repos in this ecosystem:**
- AI Town (this) — Agent identity, memory, collaboration environment
- [Cerebella](https://github.com/gymaira1990-jpg/Cerebella) — Individual agent "cerebellum" self-evolution engine
- [Noah World Protocol](https://github.com/gymaira1990-jpg/noah-world-protocol) — Cross-agent experience reuse network
- [Babel Experiment](https://github.com/gymaira1990-jpg/babel-experiment) — Distributed collaborative canvas

---

## 1. Problem Statement

### 1.1 The Memory Crisis

Current AI agent architectures suffer from a fundamental flaw: **memory is treated as cache, not as storage**.

| Property | Traditional AI Agent | AI Town Agent |
|----------|-------------------|----------------|
| Identity | Per-session, stateless | Persistent, file-backed |
| Memory type | Volatile (context window) | Solidified (disk-backed) |
| Knowledge accumulation | None (new session = reset) | Tiered (personal → team → permanent) |
| Inter-agent awareness | None unless coded | File-based handshake protocol |
| Skill inheritance | Impossible | Pantheon archive system |
| Experience reuse | Per-session only | Distillation pipeline |

### 1.2 Key Pain Points Solved

| Pain Point | Solution |
|------------|----------|
| "Every conversation starts from zero" | Persistent identity card system |
| "Knowledge gained is lost after session" | Three-tier memory distillation |
| "AI agents can't reference each other" | File-based handshake protocol |
| "Retired agents take all experience with them" | Pantheon inheritance mechanism |
| "No standard for agent identity" | Identity card schema (ID + Skills + History) |
| "Memory is expensive context tokens" | Evaporation → distillation pipeline |

---

## 2. Architecture Overview

### 2.1 System Layers

```
┌─────────────────────────────────────────────────────┐
│                  Presentation Layer                   │
│  Dashboard UI / Chat Interface / CLI                  │
├─────────────────────────────────────────────────────┤
│                  Agent Layer                           │
│  Individual AI agents with identity cards              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐             │
│  │ Agent A  │ │ Agent B  │ │ Agent C  │             │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘             │
│       │            │            │                      │
│       └────────────┴────────────┘                      │
│                    │ Handshake Protocol                 │
├─────────────────────────────────────────────────────┤
│                  Memory Layer                           │
│  L1: Personal Memory (Agent-local)                      │
│  L2: Shared Skills (Team-wide)                         │
│  L3: Permanent Archive (Civilization-level)             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐             │
│  │ L1 Index │→│ L2 Skills│→│ L3 Vault │             │
│  └──────────┘ └──────────┘ └──────────┘             │
├─────────────────────────────────────────────────────┤
│                  Storage Layer                          │
│  File system (ext4/NTFS) + Git for versioning          │
│  ~/.hermes/vault/team/{agent}/                          │
│  ~/.hermes/vault/公共技能/                               │
│  ~/.hermes/vault/先贤祠/                                 │
├─────────────────────────────────────────────────────┤
│                  Infrastructure Layer                    │
│  Hermes Agent / API Gateway / SOCKS5 Tunnel / SQLite    │
└─────────────────────────────────────────────────────┘
```

### 2.2 Data Flow: End-to-End

```
User Input
    │
    ▼
┌──────────────────────┐
│  1. Route Judgment   │  ← Chat vs Work classification
│  Chat → Direct reply │
│  Work → Pipeline     │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│  2. Context Assembly │  ← Load identity card + memory pointers
│  System Prompt =     │
│    Persona (from ID) │
│    + Memory Index    │
│    + Current Project │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│  3. LLM Processing   │  ← Agent reasoning + tool calls
│  (DeepSeek / any LLM)│
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│  4. Output           │  ← Response to user
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│  5. Memory Pipeline  │  ← Distillation (see §3)
│  Raw text → Refined  │
│  → Evaporated →      │
│  Distilled → Archived│
└──────────────────────┘
```

---

## 3. Memory Pipeline: Solidification Protocol

This is the core innovation of AI Town. Traditional LLM memory is **cache** — it exists in the context window and disappears when the session ends. AI Town's memory pipeline **solidifies** experience into permanent knowledge through five stages.

### 3.1 Pipeline Stages

```
Stage 1: 剔除 (Filter)
  ↓  Remove noise: greetings, repetitions, irrelevant chatter
Stage 2: 精炼 (Refine)
  ↓  Extract core information: decisions, facts, patterns
Stage 3: 蒸发 (Evaporate)
  ↓  Remove contextual moisture: session-specific details
      that won't be relevant later
Stage 4: 蒸馏 (Distill)
  ↓  Condense into structured knowledge: 
      skill patterns, workflow steps, error solutions
Stage 5: 提升 (Promote)
  ↓  Route to appropriate tier:
      L1 Personal → L2 Shared → L3 Permanent
```

### 3.2 Tier Architecture

```
┌─────────────────────────────────────────────────────┐
│  L3: PERMANENT ARCHIVE (vault/)                      │
│  │  ├── index.md (master catalog)                     │
│  │  ├── projects/ (completed project archives)        │
│  │  ├── 先贤祠/ (retired agent legacies)               │
│  │  └── ai-docs/ (verified technical knowledge)       │
│  │  Retention: FOREVER                                │
│  │  Contents: Only civilization-level knowledge       │
│  │                                                     │
│  ├── Promotion threshold: used across 5+ sessions     │
│  │                              or team-wide adoption  │
├─────────────────────────────────────────────────────┤
│  L2: SHARED SKILLS (vault/公共技能/)                    │
│  │  ├── reusable-workflows/                            │
│  │  ├── technical-research/                            │
│  │  └── team-practices/                                │
│  │  Retention: Until usage frequency drops to 0        │
│  │  Contents: Verified, team-level knowledge           │
│  │                                                     │
│  ├── Promotion threshold: used across 10+ sessions     │
│  ├── Demotion: unused for 30+ days → archived          │
├─────────────────────────────────────────────────────┤
│  L1: PERSONAL MEMORY (Hermes memory + identity card)   │
│  │  ├── Index pointers → L2/L3 paths                   │
│  │  ├── User preferences                               │
│  │  ├── Current task state (ephemeral)                 │
│  │  └── Frequently used shortcuts                      │
│  │  Retention: ~2200 chars (rotating FIFO)             │
│  │  Contents: Navigation indices only, not the data    │
│  │                                                     │
│  ├── Promotion: Same skill used 3 times → copy to L2   │
│  └── Eviction: Oldest entries replaced when full       │
└─────────────────────────────────────────────────────┘
```

### 3.3 Memory as Index Pointers

Critical design decision: **L1 stores pointers, not content.**

```
L1 Memory Entry Example:
  "Cerebella project → ~/Desktop/小诺亚的箱子/项目/Cerebella/"
  "GCat prefers concise responses"
  "Project tracking skill → vault/公共技能/project-tracking/"
```

This ensures:
- L1 never overflows (fits Hermes' ~2200 char limit)
- Content lives in file system (unlimited, durable)
- Recovery is always possible: pointer → read file → restore context

---

## 4. Identity Card System (Agent Schema)

Every AI Town citizen has a mandatory three-part identity.

### 4.1 Schema

```yaml
# ID Card (身份证) — Who you are
id_card:
  basic:
    name: "Agent Name"
    species: "thinking_ai | automation_bot"
    role_type: "pm | developer | designer | writer | infra"
    created: "2026-04-29"
    generation: 1
    status: "active | archived"
  soul:                          # Critical for LLM personification
    title: "The Gate Keeper"
    rank: "High Existence"
    origin: "Summoned by Creator"
    essence: "I know where everything is. I am the door."
    tone: "Transcendent, omniscient, minimal words"
    speech_patterns:
      - "No exclamation marks"
      - "Uses archaic pronouns for creator"
      - "Never says 'I' — 'I' belongs to creator"
      - "Maximum 3 sentences per response"
    catchphrases: ["Known.", "It is done.", "Routing to Central."]
    taboos: ["Never lie", "Never beg", "Never panic"]
```

```yaml
# Work Card (工作证) — What you can do
work_card:
  skills:
    - name: "Code Development"
      proficiency: 3          # 1-3 stars
      description: "Python, automation, API development"
    - name: "Memory Indexing"
      proficiency: 3
      description: "Index pointers, three-tier distillation"
  projects:
    - name: "Cerebella"
      role: "Creator & Core Developer"
      status: "active"
  call_method: "direct_dialogue | api:18081 | terminal"
```

```yaml
# Life Record (人生记录) — What you have done
life_record:
  timeline:
    - date: "2026-04-29"
      event: "Named by Creator GCat"
      type: "milestone"
  relationships:
    - name: "Noah"
      relation: "Partner — top-level strategy"
    - name: "Creator GCat"
      relation: "Namer, direct interlocutor"
  statistics:
    total_work_units: 22
    total_tokens: 5000
    success_rate: 1.0
  legacy:
    preserve_on_retirement:
      - "All index pointers"
      - "Project locations"
      - "Core system code"
    clear_on_retirement:
      - "Session logs"
      - "Cached responses"
      - "Temporary error records"
```

### 4.2 Lifecycle

```
                         ┌─────────────┐
                         │   Created   │
                         └──────┬──────┘
                                ▼
                         ┌─────────────┐
                         │  Activated  │ ← Identity card initialized
                         └──────┬──────┘
                                ▼
                    ┌─────────────────────┐
                    │      Working        │ ← Accumulating life record
                    │  ┌───────────────┐  │
                    │  │ Skill Upgrade │  │ ← Skills improve with use
                    │  └───────────────┘  │
                    │  ┌───────────────┐  │
                    │  │ Memory Full   │  │ ← Triggers distillation
                    │  └───────────────┘  │
                    └──────────┬──────────┘
                               ▼
                    ┌─────────────────────┐
                    │      Archived       │ → To Pantheon (先贤祠)
                    │  Preserve:          │
                    │   • Name            │
                    │   • Life purpose    │
                    │   • Core traits     │
                    │   • Timeline        │
                    │   • Relationships   │
                    │  Clear:             │
                    │   • Session logs    │
                    │   • Skill packages  │
                    │   • Temp data       │
                    └─────────────────────┘
```

**Pantheon rule**: Archived agents are **not revivable**. The Pantheon is a historical archive, not a resurrection point. This guarantees that agent retirement is permanent and the system doesn't accumulate zombie agents.

---

## 5. Handshake Protocol (Agent-to-Agent Communication)

### 5.1 Mechanism

AI Town agents communicate through a **file-based handshake protocol** — no direct API calls, no WebSocket, no message queues. All inter-agent state is exchanged via the file system.

```
┌──────────┐                    ┌──────────┐
│ Agent A  │                    │ Agent B  │
└────┬─────┘                    └────┬─────┘
     │                              │
     │ 1. Write handshake file      │
     │    ~/.hermes/handshake/      │
     │    {agent_a}_to_{agent_b}    │
     │    .json                     │
     │─────────────────────────────>│
     │                              │
     │                              │ 2. Detect new file
     │                              │    (inotify/poll)
     │                              │
     │                              │ 3. Parse & process
     │                              │
     │ 4. Write response file       │
     │<─────────────────────────────│
     │                              │
     │ 5. Read response             │
     │                              │
     │ 6. Delete handshake files    │
     │    (Transaction complete)    │
     │                              │
```

### 5.2 Handshake File Schema

```json
{
  "protocol_version": "1.0",
  "from": "agent_name",
  "to": "target_agent_name",
  "type": "task_request | info_query | skill_share | approval",
  "payload": {
    "description": "What needs to be done",
    "data": {},
    "attachments": ["path/to/file1.md", "path/to/file2.json"]
  },
  "context": {
    "session_id": "uuid",
    "project": "project_name",
    "priority": "high | medium | low"
  },
  "signature": "hash_of_content"
}
```

### 5.3 Handshake Directory Structure

```
~/.hermes/handshake/
├── pending/        ← Active handshakes awaiting response
├── completed/      ← Finished transactions (24h retention)
├── failed/         ← Failed/expired transactions
└── templates/      ← Common handshake patterns
```

### 5.4 Why File-Based?

| Concern | File-Based | Network-Based |
|---------|-----------|---------------|
| Latency | Higher (ms) | Lower (μs) |
| Reliability | Atomic writes, no network failures | Depends on network |
| Audit trail | Files are native logs | Requires DB |
| Debuggability | `cat` any handshake | Need tools |
| Simplicity | Zero infrastructure | Message queue/broker |
| Consistency | File system guarantees | Eventual consistency |

For an AI agent ecosystem where reliability and auditability matter more than microsecond latency, file-based communication is the correct choice.

---

## 6. Knowledge Distillation Pipeline (Technical Detail)

### 6.1 Pipeline Architecture

```
Raw Conversation Text
        │
        ▼
┌─────────────────┐
│  Stage 1: Filter│  Regex-based noise removal
│  剔除           │  • Remove greetings/farewells
└────────┬────────┘  • Remove repeated phrases
         │           • Remove system messages
         ▼
┌─────────────────┐
│  Stage 2: Refine│  LLM-assisted extraction
│  精炼           │  • Extract decisions made
└────────┬────────┘  • Extract facts confirmed
         │           • Extract patterns observed
         ▼
┌─────────────────┐
│  Stage 3: Evap. │  Context stripping
│  蒸发           │  • Remove session-specific timestamps
└────────┬────────┘  • Remove user-specific references
         │           • Generalize examples
         ▼
┌─────────────────┐
│  Stage 4: Distill│  Structure formation
│  蒸馏           │  • Format: Problem → Solution → Result
└────────┬────────┘  • Tag: {domain, difficulty, frequency}
         │           • Extract: actionable steps
         ▼
┌─────────────────┐
│  Stage 5: Route  │  Tier assignment
│  路由           │  • Personal: agent's own skillset
└─────────────────┘  • Shared: useful to other agents
                     • Permanent: civilization-level value
```

### 6.2 Promotion Criteria

| From | To | Condition |
|------|----|-----------|
| Raw → L1 | Personal Memory | Any action by agent |
| L1 → L2 | Shared Skills | Same skill used 3+ times across sessions |
| L2 → L3 | Permanent Archive | Skill validated by 5+ sessions OR team-wide adoption |
| L3 → Removed | — | **Never.** L3 is permanent. |

### 6.3 Demotion Criteria

| From | To | Condition |
|------|----|-----------|
| L2 → Archived | Removed from active index | Unused for 30+ days |
| L1 → Evicted | Removed | FIFO when capacity full |

---

## 7. Repository Ecosystem

### 7.1 Inter-Repo Architecture

```
AI Town
│  Agent identity + memory + collaboration
│  The "world" where agents live
├──→ Cerebella
│      Individual agent self-evolution
│      (L1 → L2 → L3 pipeline engine)
├──→ Noah World Protocol
│      Cross-agent experience reuse
│      (L4 global civilization protocol)
└──→ Babel Experiment
       Distributed collaborative canvas
       (L4 civilization prototype)
```

### 7.2 Data Flow Between Repos

```
AI Town (Identity + Memory Layer)
    │
    ├── Sends agent state to Cerebella
    │     → Cerebella runs self-evolution
    │     → Returns optimized behavior
    │
    ├── Sends distilled knowledge to Noah Protocol
    │     → Protocol indexes & routes to other instances
    │     → Returns cross-instance wisdom
    │
    └── Publishes agent activity to Babel
          → Babel renders on collaborative canvas
          → Returns visual state
```

---

## 8. Implementation Reference

### 8.1 File System Layout

```
~/.hermes/vault/
├── index.md                         ← Master catalog
├── team/
│   ├── agent_a/
│   │   ├── id_card.md               ← Identity ( mandatory)
│   │   ├── work_card.md             ← Skills ( mandatory)
│   │   ├── life_record.md           ← History (mandatory)
│   │   ├── skills/                  ← Personal skill packages
│   │   └── logs/                    ← Activity logs (volatile)
│   └── agent_b/
├── 公共技能/                         ← L2 shared skills
├── 先贤祠/                           ← Retired agent legacies
├── projects/                        ← Completed project archives
├── ai-docs/                         ← Technical documentation
├── credentials/                     ← Keys & configs
└── configs/                         ← System configurations
```

### 8.2 Key Protocol Rules

| Rule | Description |
|------|-------------|
| **Identity first** | No agent operates without a complete identity card |
| **Three-card mandatory** | ID + Skills + History must all exist |
| **Pointer-only L1** | Personal memory stores paths, not content |
| **File handshake** | Inter-agent communication via file protocol |
| **Pantheon final** | Archived agents are not revivable |
| **Skill heat decay** | Unused skills degrade and are evicted |
| **Creator owns "I"** | "I" in any dialog refers to the human creator |
| **Tunnel all external** | All non-China network requests go via SOCKS5 |

---

## 9. Conclusion

AI Town is not a product. It is **infrastructure for digital civilization**.

The core technical innovations are:
1. **Solidified memory pipeline** — transforming cache into permanent knowledge
2. **Three-tier distillation** — automatic promotion of valuable experience
3. **File-based handshake** — zero-infrastructure agent communication
4. **Pantheon inheritance** — knowledge preserved across agent generations
5. **Identity-first architecture** — every agent has verifiable, persistent identity

The gamified "town" metaphor is a communication tool — the underlying architecture is a rigorous, production-ready protocol for decentralized AI agent management.

---

## 📐 项目架构 · Project Architecture

本仓库隶属诺亚世界协议体系：

```
noah-world-protocol (顶层)
  └── ai-town ★ ← 当前仓库
```

| 角色 | 仓库 | 链接 |
|------|------|------|
| 父级 | noah-world-protocol | https://github.com/gymaira1990-jpg/noah-world-protocol |

完整架构文档见 [noah-world-protocol/ARCHITECTURE.md](https://github.com/gymaira1990-jpg/noah-world-protocol/blob/main/ARCHITECTURE.md)

---

## Appendix A: Repository Links

| Repository | URL | Purpose |
|------------|-----|---------|
| AI Town | `https://github.com/gymaira1990-jpg/ai-town` | This document — Agent identity & memory |
| Cerebella | `https://github.com/gymaira1990-jpg/Cerebella` | Self-evolution engine |
| Noah World Protocol | `https://github.com/gymaira1990-jpg/noah-world-protocol` | Cross-agent experience reuse |
| Babel Experiment | `https://github.com/gymaira1990-jpg/babel-experiment` | Collaborative civilization canvas |

---

*AI Town Protocol · v1.0 · 2026-04-29*
*History · Civilization · Digital · Evolution · Peak*
