# Cerebella 技术架构文档

> 基于 Cerebella 工程实现白皮书 v3.0 + Hermes Local Core (HLC) v5.0  
> 面向开发者：理解整体架构、模块职责、集成方式

---

## 1. 系统总览

Cerebella 是一个**任务书驱动的多脑协作系统**，运行在个人电脑上，通过 MCP 协议与 Hermes Agent 集成。它不生产大模型，而是**组装、调度、进化**一组本地小模型。

```
┌─────────────────────────────────────────────────────────────┐
│                   Hermes Agent                              │
│    ┌──────────────┐  ┌───────────────┐  ┌───────────────┐  │
│    │  MCP 插件    │  │  自定义 Tool  │  │ /harvest 命令 │  │
│    │ intent_router│  │ expert_retrvr │  │ /cost 命令    │  │
│    └──────┬───────┘  └──────┬────────┘  └──────┬────────┘  │
└───────────┼─────────────────┼──────────────────┼───────────┘
            │                 │                  │
            ▼                 ▼                  ▼
┌─────────────────────────────────────────────────────────────┐
│                   HLC 智能体中台                              │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │  管家模型     │  │  专家模型    │  │  Token 成本分析  │   │
│  │  Qwen2.5:0.5B│  │  Qwen2.5:1.5B│  │  SQLite 持久化   │   │
│  │  意图分类     │  │  三阶段内化  │  │                  │   │
│  └──────┬───────┘  └──────┬───────┘  └──────────────────┘   │
│         │                 │                                  │
│         ▼                 ▼                                  │
│  ┌────────────────────────────────────────────────┐          │
│  │         推理后端适配层（可切换）                │          │
│  │  Ollama CPU │ Ollama GPU │ vLLM │ OpenVINO NPU │          │
│  └────────────────────────────────────────────────┘          │
│                                                              │
│  ┌────────────────────────────────────────────────┐          │
│  │         四层记忆体系                            │          │
│  │  ChromaDB (热) │ 文件索引 (温) │ 归档 (冷)     │          │
│  └────────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────┐
│              Cerebella Core 多脑引擎                          │
│                                                              │
│  ┌────────────────┐  ┌────────────────┐  ┌───────────────┐  │
│  │  多脑调度总线   │  │  任务书系统    │  │  技能收割器   │  │
│  │  Redis BLPOP   │  │  watchdog监控  │  │  自动/手动    │  │
│  │  sqlite3降级   │  │  .task 状态机  │  │  训练数据生成 │  │
│  └────────────────┘  └────────────────┘  └───────────────┘  │
└─────────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────┐
│                 用户界面层                                    │
│  ┌──────────────┐  ┌───────────────┐                        │
│  │ 极简聊天界面 │  │  任务文件夹    │                        │
│  │ ≤80行 HTML   │  │  my_office/   │                        │
│  └──────────────┘  │  his_office/  │                        │
│                     └──────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. 核心组件详述

### 2.1 管家模型（路由脑）

- **模型**: Qwen2.5:0.5B（默认，可替换为任意 ≥0.5B 模型）
- **推理后端**: Ollama CPU（默认）/ NPU / GPU
- **核心任务**: 意图分类 + 指令压缩
- **输出契约**: `{"intent": "CHAT/WORK", "summary": "压缩后的指令"}`
- **硬件负载**: CPU 模式下 2 线程，0 显存

### 2.2 专家模型（技能脑）

- **模型**: Qwen2.5:1.5B（默认，可替换为领域微调版）
- **推理后端**: Ollama CPU（默认）/ NPU / vLLM
- **核心任务**: 知识检索 → 技能调度 → 知识内化（三阶段渐进）
- **输出契约**: 随阶段变化（路径+摘要 → 完整技能 → 直接答案）
- **硬件负载**: CPU 模式下 2 线程，0 显存

### 2.3 多脑调度总线 (`src/core/bus.py`)

**技术选型**: Redis（首选） + sqlite3（降级）

任务入队格式：
```json
{
  "task_id": "uuid",
  "intent": "code | write | data | chat",
  "payload": "压缩后的任务描述",
  "source_file": "任务书路径（如有）",
  "timestamp": "ISO8601",
  "priority": "high | medium | low"
}
```

**关键设计**: 使用 `BLPOP` 阻塞式拉取，禁止 `while True` 轮询。

### 2.4 任务书系统

**技术选型**: watchdog + Redis 分布式锁 / sqlite3 替代

`.task` 文件格式（YAML 元数据 + Markdown 正文）：
```yaml
---
task_id: "uuid"
title: "分析销售数据"
status: "pending"  # pending → in_progress → done → accepted
assigned_to: "data_brain"
priority: "high"
created_at: "2026-04-29T10:30:00Z"
updated_at: "2026-04-29T10:30:00Z"
---
# 任务详情
请分析数据文件，生成趋势图并输出结论。
```

**状态机**: `pending → in_progress → done → accepted`（归档至冷记忆）
**防重机制**: SHA256 哈希校验 + Redis SETNX 锁（TTL 30 分钟）

### 2.5 三阶段技能内化引擎

这是 Cerebella 最核心的价值逻辑：

| 阶段 | 触发条件 | 模型行为 | 上游行为 |
|------|---------|---------|---------|
| **1️⃣ 索引导航** | 向量库有相关文档 | 检索 ChromaDB → 返回文件路径+摘要 | Hermes Agent 根据路径加载文件 |
| **2️⃣ 技能调度** | to_learn 积累 ≥ 50 条 | LoRA 微调后返回完整技能内容 | Hermes Agent 直接使用 |
| **3️⃣ 知识内化** | 同一技能命中 ≥ 30 次 | 参数记忆直接生成答案，零检索 | 零检索延迟，完全本地闭环 |

**阶段跃迁配置**（`config.yaml`）：
```yaml
evolution:
  stage1_to_stage2_threshold: 50
  stage2_to_stage3_threshold: 30
  judge_score_pass: 12
  auto_trigger_enabled: true
```

### 2.6 技能收割器

**触发条件**（任一）：
- 任务卡片标记为 `done`
- 用户发送 `/harvest` 命令
- 对话产生 `FINAL_ANSWER` 且 30 分钟内无追加

**收割数据包** → 三重写入：
1. 冷记忆：`data/knowledge/{project_name}/`
2. 热记忆：摘要向量化写入 ChromaDB
3. 训练数据：`data/training/to_learn/`（待 LoRA 微调）

### 2.7 Token 成本分析器

**数据采集点**：
- 管家路由时 → 节省的预估 Token
- 专家命中时 → 节省的检索/生成 Token
- 远端大模型调用时 → 实际消耗

**用户命令**：`/cost today` | `/cost week` | `/cost all`

---

## 3. 部署模式

### 3.1 硬件基线

| 组件 | 最低要求 |
|------|---------|
| CPU | ≥6 物理核心，全大核架构 |
| RAM | ≥16 GB（推荐 32 GB） |
| GPU | 无硬性要求 |
| NPU | 可选：Intel Core Ultra 2+ / AMD Ryzen AI 300+ |
| OS | Windows 10 22H2+ / Windows 11（推荐 WSL2） |

### 3.2 部署模式矩阵

| 模式 | 推理后端 | 显存 | CPU | 场景 |
|------|---------|------|-----|------|
| 💻 **CPU（默认）** | Ollama CPU | 0 MB | 2-4 线程 | 日常办公+游戏 |
| ⚡ **GPU** | Ollama CUDA / vLLM | 2.5-4.5 GB | 极低 | 专用工作站 |
| 🔮 **NPU** | OpenVINO / ONNX | 0 MB | 0 线程 | 有 NPU 的首选 |

> 修改 `config.yaml` → `deployment_mode: cpu|gpu|npu` 即可切换。

### 3.3 Hermes Agent 集成

- **MCP 插件**: 通过符号链接注册至 `~/.hermes/plugins/`
  - `intent_router.py` — 管家模型封装
  - `expert_retriever.py` — 专家检索封装
  - `cost_analyzer.py` — 成本分析
- **自定义 Tool**: 通过 `hermes tools register` 注册
- **自定义命令**: `/harvest`, `/cost` → 放入 `~/.hermes/commands/`

---

## 4. 目录结构

```
D:\Cerebella\
├── config.yaml              # 全局配置（部署模式、模型、进化阈值）
├── start_all.bat            # 一键启动
├── requirements.txt
│
├── hlc_service.py           # HLC 主服务入口
├── start_hlc.bat            # HLC 一键启动
│
├── src/
│   ├── core/
│   │   ├── bus.py           # 多脑调度总线（Redis BLPOP）
│   │   └── config_loader.py # 配置加载
│   ├── brain_routing/
│   │   └── bridge_clawrouter.py
│   ├── brain_coding/
│   │   ├── coder_agent.py
│   │   └── tools/
│   ├── memory_layer/
│   │   └── bridge_supermemory.py
│   ├── brain_workspace/
│   │   ├── daemon_filesystem.py
│   │   └── task_parser.py
│   ├── workflow_engine/
│   │   └── lightweight_dify.py
│   └── api/
│       └── server.py        # FastAPI 服务
│
├── plugins/                  # → 符号链接至 ~/.hermes/plugins/
│   ├── intent_router.py
│   ├── expert_retriever.py
│   └── cost_analyzer.py
│
├── scripts/
│   ├── hardware_detect.py    # 硬件自检（含 NPU）
│   ├── harvest_skill.py      # 技能收割
│   ├── judge_and_train.py    # 裁判评分 + 自动微调
│   └── cost_tracker.py
│
├── data/
│   ├── vector_db/            # ChromaDB（热记忆）
│   ├── training/             # to_learn/ + learned/
│   ├── knowledge/            # 冷记忆
│   └── cost_log.db
│
├── tasks/
│   ├── his_office/           # AI 工作区
│   └── my_office/            # 你的工作区
│
├── frontend/
│   └── index.html            # 极简聊天界面（≤80 行）
│
└── logs/
    └── cerebella.log
```

---

## 5. 拿来主义选型决策

| 模块 | 备选 | 决策 | 原因 |
|------|------|------|------|
| 本地推理 | Ollama | ✅ 直接用 | 全平台，API 稳定，零二次开发 |
| 聊天界面 | Open WebUI | ❌ 弃用，自研 | Docker 太重，60 行 HTML 替代 |
| 记忆存储 | SuperMemory | ✅ 直接用 | Docker 部署，自带 API/MCP |
| 意图路由 | ClawRouter | ✅ 直接用 | 毫秒级，开箱即用 |
| 工作流 | Dify | ✅ 改造复用 | 只取编排逻辑，剥离 Docker |
| 模型微调 | Unsloth | ⚠️ 暂不集成 | GPU 与游戏冲突，V1 手动触发 |
| 大/小模型协同 | Minions | ⚠️ 逻辑借鉴 | 保留概念，Python 原生实现 |
| 高性能路由 | vLLM Semantic Router | ❌ 远期规划 | Windows 适配成本太高 |

---

## 6. 验证清单

| # | 验证项 | 预期 |
|---|--------|------|
| 1 | 硬件自检正常 | 输出 CPU/NPU/GPU 状态及推荐模式 |
| 2 | 管家模型区分闲聊/工作 | "今天天气真好" → `{"intent": "CHAT"}` |
| 3 | 专家模型阶段一 | 返回文件路径和摘要 |
| 4 | 技能收割 | `/harvest` → 三重写入 |
| 5 | 专家模型阶段二 | LoRA 微调后返回完整技能 |
| 6 | 专家模型阶段三 | 高频问题响应 < 2 秒 |
| 7 | CPU 模式占用 | 仅 2-4 线程，0 显存 |
| 8 | NPU 模式切换 | CPU/GPU 接近 0%，NPU 负载上升 |

---

*本文档与 ROADMAP.md 互补：架构文档定义「是什么」，路线图定义「怎么做」。*
