# Cerebella 开发路线图

> 三阶段实施路线 · 从点亮单一技能到自动化成长闭环

---

## Phase 1：点亮单一技能（Day 1）

**目标**：让用户和代码脑完整协作一次。

### 任务
- [ ] 编写 `src/brain_coding/coder_agent.py`，直接调用 Ollama API
- [ ] 系统提示词强制注入全局规则（如声明身份）
- [ ] 交付物：能正确生成 Python 代码的本地命令行脚本

### 检验标准
- 命令行输入代码需求 → 获得可运行的 Python 代码
- 提示词规则正确生效
- CPU 占用 ≤ 2 线程

---

## Phase 2：双脑协作与记忆（Day 2-3）

**目标**：跑通「交互 → 路由 → 工作 → 记忆」的最简闭环。

### 任务
- [ ] 部署 SuperMemory（Docker），验证 API 读写
- [ ] 编写 `bridge_supermemory.py`（封装记忆存取）
- [ ] 编写 `bridge_clawrouter.py`（实现意图路由）
- [ ] 改造 `coder_agent.py`：任务完成后自动存入 SuperMemory

### 检验标准
- 管家模型正确区分「写代码」vs「闲聊」
- 专家模型完成任务后自动记忆
- 记忆存取延迟：热记忆 < 500ms

---

## Phase 3：自动化与成长闭环（Day 4-5）

**目标**：文件交互、项目管理、前端展示全部就绪。

### 任务
- [ ] 编写 `daemon_filesystem.py`（watchdog 文件监控）
- [ ] 编写 `index.html`（极简聊天界面，≤80 行）
- [ ] 实现任务书优先级：文件区 > 聊天窗口
- [ ] 实现「巡逻 AI」自动更新 `.task` 文件状态
- [ ] 实现技能收割器（`scripts/harvest_skill.py`）
- [ ] 搭建 Token 成本分析器（`scripts/cost_tracker.py`）

### 检验标准
- 任务书 `pending → in_progress → done` 全自动流转
- 双击 `start_all.bat` 后 30 秒内所有服务就绪
- 意图路由准确率 ≥ 85%
- `/cost` 命令可用，数据准确

---

## V2 目标（Phase 1 之后）

- [ ] **NPU 模式验证**：在 Intel Core Ultra / AMD Ryzen AI 上测试零 CPU/GPU 占用推理
- [ ] **LoRA 微调管道**：解决 GPU 与游戏冲突方案后，开启自动微调
- [ ] **多专业脑扩展**：代码脑 → 写作脑 → 绘画脑 → 数据分析脑
- [ ] **技能卡标准**：标准化模型打包、分发、加载
- [ ] **GitHub 发布**：完整的开源文档 + 快速上手指南

---

> 详见 [架构文档](ARCHITECTURE.md)
