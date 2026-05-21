# 诺亚大脑架构 · 六维验证报告

> 验证时间: 2026-05-04
> 验证范围: 全部6个需求维度
> 数据来源: 文件系统检查 + SSH远程检查 + SQLite查询

---

## 维度1: 大模型带小脑 + 触发式学习

**状态**: ⚠️ 部分实现

### 已实现
- ✅ **双轮飞进 (EVO-004)**: `router-brain.py v4` (line 592-616) 有 `route_dual()` 函数 — 0.5B先跑，置信度≥80直接用，<80则DeepSeek兜底。大小模型差异记录到轻量DB
- ✅ **触发规则**: 5条硬编码触发规则 (backup/cleanup/health/sync/deploy)，命中即执行脚本
- ✅ **行政标准典编码**: 15条L1-L5 codex规则嵌入LanceDB (`codex_rules`表)，替代大模型推理
- ✅ **触发脚本**: 4个脚本存在 (`~/.router-brain/scripts/`): backup.sh, cleanup.sh, health_check.sh, sync_knowledge.sh

### 未实现/差距
- ❌ **触发式学习机制不存在**: `log_comparison()` 只做对比日志，没有"学习"逻辑。没有任何自动更新规则/记忆/知识的闭环。只有"路由+记录"，没有"学习"
- ⚠️ **dual-router.py 半废弃**: `soft-context/dual-router.py` 有废弃注释(L262引用了不存在的emotional-brain.py)，但内容仍完整。废弃模块也有副本。状态混乱
- ⚠️ **0.5B调用链路**: 0.5B在 `classify_intent()` 中作为兜底(低置信度)调用，但Ollama可能不在WSL中运行

### 任务卡
```
TASK-001: 实现触发式学习闭环 — route_dual() 的日志对比结果应驱动规则表更新
TASK-002: 清理 dual-router.py — 确定是保留route_dual()进router-brain还是删除
```

---

## 维度2: 情感脑路由 + 0.5B安全阀

**状态**: ⚠️ 部分实现

### 已实现
- ✅ **3B情感脑**: `scheduler.py` 有 `call_emotional_brain()` (line 60-79) — 调用本地 qwen2.5:3b 处理chat意图
- ✅ **情绪检测**: `router-brain.py` 有 `detect_mood()` (line 279-335) — 基于关键词的情绪分类(angry/frustrated/happy/neutral/confused)
- ✅ **SOUL.md 强制路由**: `~/.hermes/SOUL.md` (line 43-51) 明确定义路由路径: 本地0.5B → 高置信度直连 → 低置信度 first_neuron_bridge → 写工具走审计
- ✅ **三级路由**: `first_neuron_bridge.py` 实现本地0.5B → 远程第一神经元 → 专业脑的三级降级
- ✅ **审计日志**: `tool_guardrails.py` `_log_audit()` 记录所有写/改/删操作到轻量DB
- ✅ **noah_core.emotional_wrap()**: 零token机械语言包装替代emotional-brain.py

### 未实现/差距
- ❌ **emotional-brain.py 不存在**: `dual-router.py` line 263 引用 `emotional-brain.py`，但该文件不存在。这是一个断引用
- ⚠️ **安全阀覆盖面有限**: `tool_guardrails.py` 的 `_noah_preflight()` 只拦截5个关键文件(SOUL.md/身份宪法/tool_guardrails.py/prompt_builder.py/run_agent.py)。没有对"所有写/改/删操作"的全面拦截——写普通文件仍可通过
- ⚠️ **0.5B安全阀不完整**: router-brain 的 classify_intent 依赖关键词评分+0.5B兜底，但0.5B不可用时直接降级为chat(置信度40)。没有发出警报
- ⚠️ **情绪缓冲**: scheduler.py 中的情绪处理只有3B情感脑一条路径，没有在0.5B层面做情绪缓冲

### 任务卡
```
TASK-003: 清理 emotional-brain.py 断引用 — 更新 dual-router.py line 263 指向 noah_core.emotional_wrap
TASK-004: 扩展 tool_guardrails 安全阀 — 增加 risk-level 概念: low(写日志)/medium(写代码)/high(写系统文件)
```

---

## 维度3: 卢修斯数据神殿嵌入式API + 专业脑解锁

**状态**: ✅ 已实现 (基本就绪)

### 已实现
- ✅ **卢修斯数据神殿 8000 (第一神经元 v3.0)**: ✅ HEALTHY — 返回 `{"status":"ok","model":"qwen2.5:1.5b-instruct-q4_K_M","embedding":"doubao-embedding-vision-251215","version":"3.0"}`
- ✅ **卢修斯数据神殿 8001 (专业脑 v1.0)**: ✅ HEALTHY — 返回 `{"status":"ok","model":"qwen2.5:1.5b-instruct-q4_K_M","version":"1.0"}`
- ✅ **语义搜索可用**: pgvector搜索 "诺亚法典" 返回5条结果(含诺亚法典体系、档案馆结构等)
- ✅ **专业脑深度分析**: `/analyze` 端点可调用，返回 task_type/confidence/needs_tools/needs_skills 等结构化结果
- ✅ **first_neuron_bridge 连线**: 实现本地0.5B → 远程第一神经元(8000) → 专业脑(8001)的完整降级链路

### 未实现/差距
- ⚠️ **SSH隧道延迟**: 本地→卢修斯通过SSH tunnel调用(非直接HTTP)，每次调用增加~500ms-2s延迟
- ⚠️ **专业脑逻辑未在agent主循环中**: `professional_analyze()` 只在 first_neuron_bridge 中调用，不在 Hermes agent 主循环中
- ⚠️ **pgvector表结构未知**: 无法直接查询pgvector表（SSH psql被拒绝），仅通过search接口验证数据存在
- ⚠️ **专业脑无本地缓存**: 每次分析都远程调用，无缓存机制

### 任务卡
```
TASK-005: 将 first_neuron_bridge 路由逻辑集成到 Hermes agent 的 pre-processing 钩子中
TASK-006: 评估是否需要为卢修斯API添加本地缓存层
```

---

## 维度4: 数据库全量录入矢量库

**状态**: ⚠️ 部分实现

### 已实现
- ✅ **pgvector 中三大典均存在**: 搜索"诺亚法典"→命中(相似度0.50), "行政标准典"→命中(0.44), "钢铁守护圣典"→命中(0.45)
- ✅ **知识图库10条记录**: `~/.hermes/knowledge/知识图库/entries/` 涵盖 hermes-agent/qq-bot/desktop/open-webui/hermes-web-ui/第一神经元/腾讯云/软件源/豆包/DeepSeek
- ✅ **LanceDB 10个表**: vector_memory(日常联想), relation_memory(关键词标签), trigger_rules(触发规则), codex_rules(行政标准典), knowledge_index, project_index, skills_index, tfc_index, session_memory, log_index
- ✅ **档案馆存在**: 行政标准典目录(/noah-档案馆/行政标准典/) + 钢铁守护圣典.md + 知识档案馆/ 都在

### 未实现/差距
- ❌ **非"全量"**: 知识图库只收录了10个条目。档案馆中有大量项目档案、对话存档、行为法典冲突检测报告等未进入矢量库
- ❌ **LanceDB仅做关键词匹配**: `vector_memory` 和 `relation_memory` 是静态关键词表，不是真正的矢量嵌入库。`knowledge_index` 存在但数据量未知
- ⚠️ **pgvector数据局限**: 通过search接口只能返回5条/次，无法统计总量。从返回内容看主要是架构/治理类文档
- ⚠️ **本地vs远程数据不统一**: pgvector有17+条记录，本地LanceDB只有规则数据，没有做矢量同步

### 任务卡
```
TASK-007: 审计知识图库entries/ — 识别哪些档案馆内容应该录入但尚未录入
TASK-008: 建立 LanceDB ↔ pgvector 的双向同步机制
```

---

## 维度5: 本地小数据库（情感存储+0.5B规则）

**状态**: ✅ 已实现 (基本满足需求)

### 已实现
- ✅ **lightweight.db 119条记录**: 分布在25个分类(codex:21, knowledge:16, selflog:14, dual:13, rule:13, brain:11, scene:6, 等)
- ✅ **recent-memory.json**: 43轮对话记录，含频率+时间戳
- ✅ **情感存储分离**: brain/identity/mood 类存储在 lightweight.db 中，与 codex/rule 规则存储分离
- ✅ **0.5B规则存储分离**: `~/.router-brain/memory/` 下10个LanceDB表，与 `~/.hermes/knowledge/soft-context/` 下的情感/记忆数据物理分离
- ✅ **动态规则加载 (L3-L5)**: `noah_core.py` 实现按task_type加载对应规则文件(code/novel/chat/knowledge/general)
- ✅ **LanceDB表规则已编码**: codex_rules 表有15条行政标准典规则，trigger_rules有5条触发规则
- ✅ **规则文件系统**: 5个规则文件(`rules/`: chat_policy.txt, code_policy.txt, general_policy.txt, knowledge_policy.txt, novel_policy.txt)

### 未实现/差距
- ⚠️ **无情感-规则关联**: 情感检测结果和规则加载之间没有联动。用户情绪不好也应该加载更保守的规则
- ⚠️ **recent-memory.json 无压缩**: 43轮后未触发压缩(last_compress_round=0)，文件大小11280字节

### 任务卡
```
TASK-009: 增加情绪-规则联动 — 负面情绪时自动加载更保守的安全规则
```

---

## 维度6: 全链路数据流验证

**状态**: ⚠️ 部分实现

### 已实现
- ✅ **memory_tool.py 导入链路**: Hermes agent 的 memory_tool.py 直接 import noah_core + lightweight-db + recent-memory (line 45-47)
- ✅ **noah_core 完整管道**: clean_input → call_router → build_work_order → emotional_wrap → quick_route
- ✅ **scheduler.py 完整管道**: call_router → intent分类 → 分流(trigger/chat/work/knowledge) → _append_context → _check_compress
- ✅ **noah-pipeline.py 结构化工单**: denoise → route → work_order → route_decision → archive(含hooks) → output
- ✅ **事件驱动触发器**: event-trigger.sh 覆盖 session-end/milestone/tfc-done/post-op 四种触发类型
- ✅ **三级钩子系统**: hooks.py 提供自检(self_check_hook) + 状态同步(status_sync_hook) + 省Token(token_save_hook)

### 未实现/差距
- ❌ **路由脑未接入agent主循环**: Hermes agent 的核心循环(`AIAgent.run_conversation()`) 不调用 `router-brain.py` 或 `scheduler.py`。memory_tool.py 虽然 import noah_core 但只在 memory 操作时调用，不是每次用户输入都走路由
- ❌ **缺失全链路强制路由**: 设计需求是"用户输入→0.5B路由→(置信度判断)→分流"，但实际 Hermes agent 收到输入后直接走LLM，不走本地0.5B路由
- ⚠️ **scheduler.py 与 agent 独立运行**: scheduler.py 是独立CLI工具，Hermes agent 不自动调用它
- ⚠️ **first_neuron_bridge 不是强制的**: SOUL.md要求走路由路径，但agent运行时无法自动触发 first_neuron_bridge.py
- ⚠️ **无端到端测试**: 无法验证完整链路(用户输入→0.5B路由→情感/专业/逻辑/知识库→输出)是否工作

### 关键数据流追查

```
设计需求:
  用户输入 → 0.5B路由 → 置信度≥80 → 直接处理
                      ↓ 置信度<80
          → 情感脑/第一神经元/专业脑/知识库

实际数据流(memory_tool.py集成):
  用户输入 → Hermes agent LLM → (如触memory卡) → memory_tool.py
       → lightweight-db / recent-memory / noah_core(emotional_wrap)
       不经过路由脑!

实际数据流(scheduler.py独立):
  用户输入 → scheduler.py → call_router(router-brain.py)
       → trigger/chat(qwen2.5:3b)/work(DeepSeek)/knowledge(四级检索)
       独立运行，Hermes agent不调用!
```

### 任务卡
```
TASK-010: (关键) 将 router-brain.py 的路由逻辑注入 Hermes agent pre-processing
          — 在 agent 处理用户输入前，先调0.5B路由确定intent+置信度
TASK-011: (关键) 建立强制路由链 — agent启动时自动加载 SOUL.md + session-loader，
          每次用户输入前做路由分类，低置信度走 first_neuron_bridge
TASK-012: 创建端到端数据流测试 — 模拟完整链路验证每一步输出被下一步正确消费
```

---

## 综合评分

| 维度 | 状态 | 评分 | 核心差距 |
|------|------|------|----------|
| 1.大模型带小脑+触发式学习 | ⚠️ 部分实现 | 6/10 | 无学习闭环，只有路由 |
| 2.情感脑路由+0.5B安全阀 | ⚠️ 部分实现 | 6/10 | emotional-brain.py断引用,安全阀覆盖面有限 |
| 3.卢修斯数据神殿API+专业脑 | ✅ 已实现 | 8/10 | SSH延迟，agent主循环未集成 |
| 4.数据库全量录入 | ⚠️ 部分实现 | 5/10 | 非全量，知识图库仅10条 |
| 5.本地小数据库 | ✅ 已实现 | 8/10 | 无情绪-规则联动 |
| 6.全链路数据流 | ⚠️ 部分实现 | 4/10 | 路由脑未接入agent主循环 |

**总体评分: 6.2/10**

### 优先级建议
1. **P0 (必须修)**: TASK-010 + TASK-011 — 路由脑接入agent主循环
2. **P0 (必须修)**: TASK-003 — 清理 emotional-brain.py 断引用
3. **P1 (重要)**: TASK-001 — 建立触发式学习机制
4. **P1 (重要)**: TASK-007 — 审计并补充知识图库
5. **P1 (重要)**: TASK-004 — 扩展安全阀覆盖面
6. **P2 (优化)**: TASK-008 + TASK-012 — 同步+测试
