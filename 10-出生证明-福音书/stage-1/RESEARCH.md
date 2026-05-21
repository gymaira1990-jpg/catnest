# PROJ-008 · 胚胎阶段研究报告

> **研究院产出 · 深度研究**
> 日期: 2026-05-04 | 版本: v1.0
> 项目: PROJ-008 诺亚文明·数字方舟计划
> 阶段: 胚胎阶段（Phase Embryo）
> 目标: 本地独立环境 + 初始核心 + 观察对话窗口 + 记忆系统 + 自洽

---

## 一、问题定义

### 1.1 为什么需要胚胎阶段？

现有 `noah-factory/` 经过多轮迭代（EVO-002/003/004/005, TFC-016/017/018）已积累55+组件、6726行代码、31个Python文件、7个Shell脚本（不含外部依赖）。其中：

- 部分组件已废弃（`dual-router.py` 有断引用）
- 部分组件功能重叠（多个路由实现共存）
- Hermes 依赖仍然存在（`run_hermes()`）
- 没有一个「干净的起点」

胚胎阶段的目标是：**从零建一个最小自治核心，只取经过验证的最优组件，不做任何历史遗留妥协。**

### 1.2 核心需求

```
① 独立环境          ← 全新目录，不依赖 Hermes，零历史债务
② 初始核心          ← 最小可用 AI Agent 本体
③ 观察+对话窗口     ← 既能看状态，也能对话
④ 接最新记忆系统    ← storage.py 四层存储 + 记忆检索
⑤ 逻辑自洽          ← 规则 → 行为 → 校验 闭环
⑥ 为发育铺垫        ← 架构可扩展，不给未来设限
```

---

## 二、现有资产审计（可复用部分）

### 2.1 可直接复用的核心模块

深入研究 `soft-context/` 代码后发现的结论：

**现有代码已在事实上接近独立。** 与 Hermes 的唯一绑定只有：

| 绑定点 | 位置 | 影响 | 修复方案 |
|:-------|:-----|:----|:---------|
| `run_hermes()` | noah.py:156-182 | 工具执行依赖 Hermes CLI | 胚胎阶段暂不需要工具执行（纯对话+观察），可移除 |
| `router-brain.py` 动态导入 | noah_core.py:203-241 | 0.5B路由分类 | 有兜底逻辑（降级到 quick_route），可移除 |
| LanceDB | storage.py | 矢量存储 | 可降级为纯SQLite模式 |
| 卢修斯同步 | storage.py | 远程推送 | 初期不需要，可移除 |

### 2.2 可复用组件清单

| 组件 | 行数 | 依赖 | 复用方式 |
|:----|:---:|:-----|:---------|
| `noah_core.py` | 912 | 无外部（只调 subprocess + re） | 直接复制+精简router-brain引用 |
| `storage.py` | 409 | LanceDB(可选) + httpx(LLM嵌入) | 复制+使LanceDB可选+移除卢修斯同步 |
| `scheduler.py` | 422 | Ollama(可选) + DeepSeek API | 复制+使Ollama可选 |
| `lightweight-db.py` | 186 | 纯stdlib (sqlite3) | **直接复制，零改动** |
| `recent-memory.py` | 331 | 纯stdlib (json) | 直接复制 |
| `compressor.py` | 217 | 纯stdlib | 直接复制 |
| `noah.py` REPL | 300 | scheduler + storage + noah_core | 重写入口逻辑+移除Hermes绑定 |
| session-loader 逻辑 | - | 文件读取 | 简化后嵌入 |

### 2.3 不可复用的（不带的）

| 组件 | 原因 |
|:-----|:-----|
| `run_hermes()` 工具执行 | 胚胎阶段不需工具执行 |
| `router-brain.py` | 模块化到 noah_core.quick_route() 中 |
| `dual-router.py` | 已废弃 |
| `hooks.py` | 工厂级超重，胚胎阶段用简化版 |
| `auto-skill.py` | 发育阶段功能 |
| `sync-to-lucius.py` | 远程同步 |

---

## 三、胚胎架构设计

### 3.1 目录结构

```
~/noah-embryo/                          ← 独立环境，干净起点
│
├── noah.py              (入口)          ← REPL + 单次对话模式
├── core/
│   ├── __init__.py
│   ├── engine.py                       ← 对话引擎（路由+执行）
│   ├── router.py                       ← 意图分类（0.5B 关键词+兜底）
│   ├── rules.py                        ← 规则加载+自洽校验
│   └── memory.py                       ← 记忆系统封装
│
├── storage/
│   ├── __init__.py
│   ├── lightweight-db.py               ← SQLite 键值存储 (186行，零改动)
│   ├── recent-memory.py                ← 三级压缩近期记忆 (331行，零改动)
│   └── archiver.py                     ← 四层存储引擎 (精简版 storage.py)
│
├── web/
│   ├── index.html                      ← 观察+对话窗口 (单页HTML)
│   ├── style.css
│   └── app.js
│
├── data/                               ← 运行时数据目录
│   ├── lightweight.db                  ← SQLite 数据库
│   ├── recent-memory.json              ← 近期对话存档
│   └── archives/                       ← L4 MD 归档
│
├── rules/                              ← 规则文件
│   ├── codex_rules.json                ← 世界观规则(含战锤)
│   └── policies/                       ← 行为策略
│
├── tests/                              ← 自洽性测试
│   └── test_self_consistency.py
│
└── start.sh                            ← 一键启动脚本
```

### 3.2 架构图

```
┌─────────────────────────────────────────────────────┐
│                 诺亚胚胎 · Noah Embryo                │
│                                                     │
│  用户输入                                              │
│    │                                                  │
│    ▼                                                  │
│  ┌──────────┐                                         │
│  │ 观察窗口  │  ← web/index.html (状态面板+对话)       │
│  │ 对话窗口  │                                         │
│  └────┬─────┘                                         │
│       │ HTTP SSE                                       │
│       ▼                                               │
│  ┌──────────────┐                                     │
│  │  noah.py      │  ← 入口：REPL / Web 双模式          │
│  │  (入口)       │                                     │
│  └──────┬───────┘                                     │
│         │                                              │
│         ▼                                              │
│  ┌──────────────────┐   ┌─────────────┐               │
│  │  engine.py       │──▶│  router.py  │ 意图分类       │
│  │  对话引擎        │   └──────┬──────┘               │
│  │  路由+执行+记忆  │          │ chat/work/knowledge   │
│  └──────┬───────────┘          ▼                      │
│         │              ┌──────────────┐               │
│         │              │  rules.py    │ 规则校验       │
│         │              │  自洽检查     │               │
│         │              └──────┬───────┘               │
│         ▼                     ▼                       │
│  ┌──────────────────────────────────────┐             │
│  │           记忆系统                     │             │
│  │  ┌──────────┐ ┌──────────┐ ┌───────┐ │             │
│  │  │L1 内存   │ │L2 SQLite │ │L3 MD  │ │             │
│  │  │recent-   │ │light-    │ │archi- │ │             │
│  │  │memory    │ │weight    │ │ves/   │ │             │
│  │  └──────────┘ └──────────┘ └───────┘ │             │
│  └──────────────────────────────────────┘             │
│         │                                              │
│         ▼                                              │
│  ┌──────────────────┐                                 │
│  │  LLM API 层      │  ← DeepSeek / 豆包 / Ollama     │
│  │  (可切换)        │                                  │
│  └──────────────────┘                                 │
└─────────────────────────────────────────────────────┘
```

### 3.3 三要素：观察 · 对话 · 记忆

**观察窗口** (`web/index.html`):
- 状态面板: 心率(心跳间隔)、记忆状态(HOT/WARM/COLD)、规则状态
- 对话面板: SSE 流式对话
- 日志面板: 最近操作记录
- 战锤主题(深红+金色)

**对话引擎** (`engine.py`):
- 输入降噪 → 意图分类(router.py) → 规则校验(rules.py) → LLM调用 → 记忆存储
- 纯 API 驱动（无本地模型依赖），Ollama 可选

**记忆系统** (3层，非4层):
- L1 近期记忆: `recent-memory.py`（对话压缩）
- L2 持久化: `lightweight-db.py`（SQLite关键词检索）
- L3 归档: `archiver.py`（MD文件时间线）

对比「开发展」的4层(LanceDB):
- 胚胎阶段不需要矢量检索（可验证的假设，发育阶段再加）
- LanceDB 作为可选升级路径设计好接口

---

## 四、逻辑自洽方案

### 4.1 自洽三角

```
 规则 (rules.py) ←→ 行为 (engine.py)
      ↕                  ↕
   校验 (test_self_consistency.py)
```

| 维度 | 机制 | 实现 |
|:----|:-----|:-----|
| **规则→行为** | `engine.py` 每轮对话前调用 `rules.py` 做规则匹配 | 规则命中→行为受约束 |
| **行为→规则** | `rules.py` 从行为日志中提取新规则 | 自动发现模式 |
| **校验→规则** | `test_self_consistency.py` 验证规则无冲突 | 启动时自动运行 |
| **校验→行为** | 输出前校验是否符合已激活规则 | 实时干预 |

### 4.2 规则层级（精简版）

| 层 | 名称 | 文件 | 示例 |
|:-:|:-----|:-----|:-----|
| L1 | 代码硬约束 | `engine.py` 嵌入式 | 不输出密钥、不执行rm -rf |
| L2 | 反射规则 | `rules.py` 自动加载 | 亚空间防护(置信度<60%→标记) |
| L3 | 动态规则 | `rules/codex_rules.json` | 战锤世界观规则 |
| L4 | 自洽校验 | `tests/` | 启动时验证 |

### 4.3 启动自检流程

```
start.sh
  │
  ├─ ① 检查依赖 (Python版本 / 必要模块)
  ├─ ② 初始化 data/ 目录 (如果不存在)
  ├─ ③ 运行 test_self_consistency.py
  │     ├─ 规则无冲突 → ✅
  │     └─ 有冲突 → ⛔ 输出冲突报告，退出
  ├─ ④ 启动 web 服务 (端口 7860)
  └─ ⑤ 打印状态 + 打开浏览器
```

---

## 五、发育铺垫设计

### 5.1 预留的进化路径

| 当前 | 未来 | 接入方式 |
|:-----|:-----|:---------|
| 纯 API 驱动的 LLM 调用 | Ollama 本地模型（0.5B/3B） | `engine.py` 中 `_call_llm()` 工厂模式 |
| 3层记忆(内存+SQLite+MD) | 4层(+LanceDB矢量) | `archiver.py` 中 `search()` 接口注入矢量层 |
| 单用户 REPL/Web | 多角色户籍 | `router.py` 中 `identity` 参数预留 |
| 无工具执行 | Hermes 工具引擎/子进程 | `engine.py` 中 `execute_tool()` 插槽预留 |
| 单实例 | 多实例协作 | 对话ID + session 隔离已设计 |
| 本地 only | 远程卢修斯同步 | `storage/sync.py` 接口预留(无实现) |

### 5.2 代码级接口设计原则

所有未来扩展点用**接口 + 默认实现**模式：

```python
# 示例：LLM 调用工厂
class LLMBackend:
    """LLM 后端抽象 — 发育阶段可插拔"""
    def chat(self, messages, **kwargs) -> str:
        raise NotImplementedError

class APIBackend(LLMBackend):
    """默认：API 驱动"""
    def chat(self, messages, **kwargs):
        return call_deepseek_api(messages, **kwargs)

class OllamaBackend(LLMBackend):
    """可选：本地模型"""
    def chat(self, messages, **kwargs):
        return call_ollama(messages, **kwargs)
```

---

## 六、实施计划

### 6.1 文件创建清单

| 优先级 | 文件 | 类型 | 说明 |
|:------:|:----|:----|:-----|
| P0 | `start.sh` | Shell | 一键启动+自检 |
| P0 | `noah.py` | Python | 入口，重写自现有noah.py但移除Hermes绑定 |
| P0 | `core/engine.py` | Python | 对话引擎 |
| P0 | `core/router.py` | Python | 意图分类(keyword + API兜底) |
| P0 | `core/rules.py` | Python | 规则加载+自洽校验 |
| P0 | `core/memory.py` | Python | 记忆系统封装 |
| P0 | `web/index.html` | HTML | 观察+对话窗口 |
| P0 | `web/style.css` | CSS | 战锤主题 |
| P0 | `web/app.js` | JS | SSE流式+状态面板 |
| P1 | `storage/lightweight-db.py` | Python | 直接复制现有，零改动 |
| P1 | `storage/recent-memory.py` | Python | 直接复制现有，零改动 |
| P1 | `storage/archiver.py` | Python | 精简版storage.py |
| P1 | `rules/codex_rules.json` | JSON | 世界观规则(含战锤) |
| P1 | `tests/test_self_consistency.py` | Python | 自洽性自动测试 |
| P2 | 各项详细单元测试 | Python | 发育阶段补充 |

### 6.2 文件依赖顺序

```
阶段A 基础设施 (P0):
  start.sh → 目录初始化 → lightweight-db.py → recent-memory.py
  rules/codex_rules.json → core/rules.py

阶段B 核心逻辑 (P0):
  core/router.py → core/engine.py → core/memory.py → noah.py

阶段C 界面 (P0):
  web/index.html + style.css + app.js → start.sh 自动启动

阶段D 自洽 (P1):
  tests/test_self_consistency.py → 启动时自动运行
```

### 6.3 估计工作量

| 阶段 | 文件 | 预估行数 | 工时 |
|:----|:-----|:--------:|:---:|
| A | 基础设施(复制+精简) | ~600 | 0.5天 |
| B | 核心逻辑(重写) | ~500 | 1天 |
| C | Web界面(新建) | ~400 | 1天 |
| D | 自洽测试(新建) | ~150 | 0.5天 |
| E | 集成+调试 | - | 0.5天 |
| | **合计** | **~1650** | **3.5天** |

---

## 七、与现有系统对比

| 维度 | 现有 noah-factory | 胚胎 noah-embryo |
|:-----|:-----------------|:-----------------|
| 代码量 | ~6700 行(.py) + Shell | ~1650 行 |
| 依赖 | Hermes CLI + LanceDB + Ollama + 卢修斯数据神殿 | Python stdlib + httpx + LLM API |
| 历史债务 | dual-router废弃、emotional-brain幽灵引用 | 零 |
| 工具执行 | Hermes 代理 | 预留接口，暂无实现 |
| 矢量检索 | LanceDB 10表 | 预留接口，发育阶段加 |
| 启动时间 | 依赖 session-loader.sh | 自检 → 启动，<1秒 |
| 世界观 | 写在多个典中 | rules/codex_rules.json 单文件 |
| 可测试性 | 无独立测试 | test_self_consistency.py 启动自跑 |

---

## 八、结论与建议

### 8.1 建议

1. **胚胎阶段不是「重写一切」** — 现有 `lightweight-db.py`(186行) 和 `recent-memory.py`(331行) 是纯stdlib写的高质量代码，**零改动直接复用**

2. **胚胎阶段也不是「最小哈囉世界」** — 它必须有可工作的记忆系统、自洽校验、可发育的架构接口

3. **最佳方案**: 上述 `noah-embryo/` 架构，约1650行代码，3.5天工作量

### 8.2 为什么这个方案最优

| 方案 | 工作量 | 独立程度 | 可发育性 | 记忆系统集成 |
|:----|:-----:|:--------:|:--------:|:----------:|
| A: 在noah-factory上修补 | 2天 | ❌ 仍有遗留 | ❌ 架构受限 | ✅ 已有 |
| B: 从零全写 | 7天+ | ✅ 最干净 | ✅ 最好 | ❌ 从头写 |
| **C: 胚胎独立(本方案)** | **3.5天** | **✅ 干净** | **✅ 预留** | **✅ 复用最佳** |
| D: 只做WebUI | 2天 | ❌ 仍然依赖 | ❌ 单点 | ❌ 无 |

---

## 九、产出物

| 产出 | 路径 |
|:----|:-----|
| **本报告** | `方案设计/胚胎阶段-研究报告-v1.md` |
| **架构图** | 见全局架构图 (`proj-008-architecture.html` 层0-4) |
| **实施计划** | 待GCat确认后由工程院拆TFC |

---

**等待GCat确认方向 → 进入工程院实施。**
