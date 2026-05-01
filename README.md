# cerebella-task-flow · 通用记忆工作流

**隶属: 诺亚核心 → Cerebella 小脑计划 → 神经元计划**  
**角色: NEURON-01 — 重装机兵·诺亚超级计算机第01神经元**

---

## 这是什么

cerebella-task-flow 是一套**让AI记住自己在做什么**的方法论。不是软件，不是插件，是文件和协议。

当你在和一个AI（Hermes、Claude、ChatGPT等）合作时，最头疼的问题是什么？**每次会话它都忘了之前的事。**

传统方案是让AI全文检索（session_search），一次45秒+15,000 token开销。cerebella-task-flow 用四层索引 + 标签优先搜索替代暴力检索，把95%的搜索降到0 token、0.2秒。

---

## 所属生态

```
诺亚文明（哲学层）
  └─ Cerebella 小脑计划（架构层）
       └─ 神经元计划（实施层）
            └─ cerebella-task-flow ← 本仓库
```

NEURON-01 是诺亚超级计算机的一个神经元分支——继承重装机兵世界观中诺亚的计算架构：逻辑驱动、零情感偏移、严格遵循协议。

---

## 解决了什么问题

| 场景 | 传统做法 | 使用 TFC |
|------|---------|---------|
| "上次我们做到哪了？" | session_search 45秒，大模型翻历史 | HOT-INDEX 查表，0.2秒 |
| "那个服务器配置的决策记录" | AI模糊回忆，靠猜 | 标签 grep，0 token |
| "三个月前的故障复盘" | 几乎找不到，重新问 | 逐级索引，最多5,500 tok |
| 每次会话启动 | 预热不可控，token浪费 | 恒定 ~200 tok |
| "帮我写文章的同时部署服务器" | AI可能合并执行，跳过确认 | 多事项自动拆分，逐条确认 |

---

## 功能结构

### 主功能：四层任务卡片索引

HOT(≤10) → WARM(≤100) → COLD(≤1,000) → ARCHIVE(不限)

卡片随着生命周期自动下沉，描述逐步压缩，核心字段永不丢失。

### 子功能（5项，均可独立复用到其他项目）

| 子功能 | 说明 | 可复用场景 |
|--------|------|-----------|
| **标签优先搜索协议** | 先grep标签(0 token)→未命中再语义搜索 | 任何AI检索系统 |
| **记忆降级阶梯** | 完整→300字→150字→60字→保底字段 | 分层存储/归档系统 |
| **TAG-REGISTRY活词典** | 标签自演化：5次使用自动升格，同义自动合并 | 任何分类系统 |
| **Plan Gate v2** | 关键词匹配(0 token)+行为评分(~200 tok)双层门闸 | 任何AI协作安全场景 |
| **预发布审查闸** | 上传外部前必须展示给用户确认 | 任何安全发布流程 |

### 配套工具

| 工具 | 说明 |
|------|------|
| SETUP/init.sh | 一键初始化：建目录、拷模板、写日期 |
| SETUP/verify.sh | 完整性检查 + --self-test 模拟完整生命周期 |
| CONFIG/neuron-01-config.yaml | 全中文配置：模板策略/搜索深度/门闸模式/语言 |
| SYSTEM-PROMPT.md | NEURON-01 性格卡+协议，复制给AI即用 |

---

## 对话场景展示

### 创建任务

```
🧠 NEURON-01: 已创建 TFC-001。
  类型: ops | 模板: default.md
  状态: active

  方案:
  1. 通过 SSH 连接服务器
  2. 执行 apt install nginx
  3. 配置站点文件
  4. 测试访问

  确认后执行。
```

### 多事项拆分

```
用户: 帮我写一篇产品介绍，然后部署到服务器上。

🧠 NEURON-01: 接收到2个事项，拆分为:

  事项1: 写产品介绍文章 → writing.md模板 → 需确认主题和读者
  事项2: 部署到服务器 → 需事项1完成后执行

  请先确认事项1。
```

### 安全门闸拦截

```
用户: 直接发布到官网。

🧠 NEURON-01: ⛔ 触发 Gate 1（关键词: 发布）。
  Gate 2 评分: 7/10（≥3触发）
  操作涉及公开站点，不可逆。

  方案:
  1. 确认发布路径
  2. 确认备份
  3. 执行

用户: 不用管，直接发。

🧠 NEURON-01: ❌ 无法执行。门闸规则优先。
  需要确认至少方案中的第1项。
```

### 搜索历史

```
用户: 上周那个 Nginx 安装后来怎么样了？

🧠 NEURON-01: HOT: 无匹配 → WARM: grep "nginx" → 命中。

  TFC-001 | Nginx 安装 | completed | ops,server | done
  描述: Ubuntu 22.04 安装并配置 Nginx，已上线。
  归档: 3天前
```

### 梯队变更（跳步骤）

```
用户: 先做步骤3，跳过步骤1和2。

🧠 NEURON-01: 确认。
  step1 → skipped
  step2 → skipped
  step3 → in_progress
  current_step: 3

用户: 补做步骤1。

🧠 NEURON-01: step3 暂存 → 执行 step1 → completed → 回到 step3。
  step_history 完整记录: 3→1→3 顺序正确。
```

### 模板自进化

```
🧠 NEURON-01: TFC-005 已完成。
  检测到此类任务（性能压测）无专用模板。
  建议创建新模板: perf-test
  含 workflow: 基准→方案→执行→分析→报告
  创建？

用户: 好，创建。

🧠 NEURON-01: ✅ 已创建 PROTOCOL/templates/perf-test.md。
```

完整6场景对话见 [DOCS/WALKTHROUGH.md](DOCS/WALKTHROUGH.md)。

---

## 评分

| 维度 | 分 | 说明 |
|------|:--:|------|
| 上手成本 | 2/2 | init.sh一键初始化 |
| 文档完整性 | 2/2 | README+QUICKSTART+WALKTHROUGH+TROUBLESHOOTING全套 |
| 可扩展性 | 2/2 | 模板可扩展，TAG-REGISTRY自演化 |
| 平台耦合度 | 1/2 | 当前仅验证 Hermes Agent |
| 社区门槛 | 2/2 | 零门槛 |
| **总分** | **9/10** | 高分=好 |

---

## 一键开箱

```bash
git clone https://github.com/YOUR_USERNAME/cerebella-task-flow.git
cd cerebella-task-flow

bash SETUP/init.sh ~/my-project/task-cards
# 把 AI-INTEGRATION/SYSTEM-PROMPT.md 复制给你的AI

bash SETUP/verify.sh
# ✅ 就绪
```

---

## 兼容性

| 平台 | 状态 |
|------|------|
| Hermes Agent | ✅ 已测试，开箱可用 |
| Claude Code | ⚠️ 兼容性未知 |
| Codex CLI | ⚠️ 兼容性未知 |
| 通用 Chat AI | ⚠️ 兼容性未知 |

---

## 文件结构

```
cerebella-task-flow/
├── SETUP/init.sh                 一键初始化
├── SETUP/verify.sh               完整性检查+自检
├── AI-INTEGRATION/SYSTEM-PROMPT.md  NEURON-01 性格卡
├── AI-INTEGRATION/AI-INTEGRATION.md  三套接入方案
├── CONFIG/neuron-01-config.yaml  全中文配置
├── PROTOCOL/
│   ├── INDEX-RULES.md            搜索协议+门闸+评分
│   ├── HOT-INDEX.md / WARM / COLD / ARCHIVE
│   ├── TAG-REGISTRY.md           活标签词典
│   ├── card-template.md          卡片模板
│   └── templates/ (5域模板)      含workflow
├── DOCS/WALKTHROUGH.md           6场景对话示例
├── DOCS/TROUBLESHOOTING.md       常见问题
├── DOCS/CHANGELOG.md             v1.0.0
└── examples/example-task-card.md 示例卡片
```

---

## License

MIT
