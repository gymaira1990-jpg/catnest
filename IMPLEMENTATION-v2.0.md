# Cerebella 项目工程实现方案 v2.0 （完全复用版）

> **组装航母，而非铸造零件。**
>
> 本方案严格遵循"拿来主义"——每一行代码，只要能找到现成的、好用的，就绝不自己写。

---

## 1. 核心策略

我们的核心工作只有三项：

1. **搬运与部署**：把选中的开源项目拉下来，配置好，跑起来。
2. **适配与桥接**：写最薄的胶水代码，让这些独立的项目能互相"说话"。
3. **业务逻辑注入**：把 Cerebella 独有的"任务书"、"多脑调度"、"三阶段成长"等逻辑，作为插件或配置文件，注入到现成的框架中。

---

## 2. 基础组件选型清单

| 组件 | 来源仓库 | 用途 |
|------|---------|------|
| **Ollama** | `ollama/ollama` | 本地模型推理的总后端，管理所有小脑模型 |
| **Open WebUI** | `open-webui/open-webui` | 直接用作聊天交互界面，支持多模型切换、RAG |
| **SuperMemory** | `supermemoryai/supermemory` | 永久记忆仓库，管理热/温/冷记忆，自带 API |
| **Dify** | `langgenius/dify` | 可视化工作流编排器，支持 AI 工作流、知识库 |
| **ClawRouter** | `blockrun/clawrouter` | 意图路由逻辑，作为路由脑的 AI 部分 |

---

## 3. Cerebella 胶水层

在部署上述组件后，开发一个轻量级的 Python 胶水项目 **Cerebella Core**。它不负责任何 AI 推理或记忆存储，**只负责调度与连接**。

**主要功能：**

- **与 Open WebUI 集成**：利用其 API 监听用户新对话，调用 ClawRouter 判断意图
- **与 SuperMemory 集成**：任务完成后将对话摘要、成果存入对应记忆层级
- **与 Dify 集成**：创建新技能时调用 Dify API 创建工作流应用并注册到小脑列表
- **管理任务书 (`*.task` 文件)**：核心模块，负责：
  - **解析**：读取 `.task` 文件，获取任务需求、状态、指派的脑
  - **状态机驱动**：跟踪文件状态（待办 → 进行中 → 已完成/已验收）
  - **触发动作**：状态变更时调用对应专业脑或归档

---

## 4. MVP 组装指南

### 第一步：底座部署（30分钟）

1. **安装 Ollama**（已装可跳过）
2. **一键安装 Open WebUI**：
   ```bash
   docker run -d -p 3000:8080 --name open-webui --restart always ghcr.io/open-webui/open-webui:main
   ```
3. **一键安装 SuperMemory**：
   ```bash
   git clone https://github.com/supe-memory/supermemory.git && cd supermemory
   docker compose up -d
   ```
4. **一键安装 Dify**：
   ```bash
   git clone https://github.com/langgenius/dify.git && cd dify/docker
   docker compose up -d
   ```

### 第二步：胶水代码开发

1. **改造 ClawRouter，注入路由脑**
   - 克隆 `blockrun/clawrouter` 到 `brains/` 目录
   - 修改 prompt 和模型调用，输出标准 Cerebella 意图格式
   - 在 `core/router.py` 写 `route_intent(user_input)` 函数

2. **开发任务书文件监控器 (`core/task_watcher.py`)**
   - 用 Python `watchdog` 库监控"任务发布区"文件夹
   - 检测新的 `.task` 文件，解析内容提取任务指令
   - 驱动状态机，调用 Open WebUI 或 Dify 工作流执行

3. **集成 SuperMemory 记忆**
   - 任务状态变为 `[已完成/已验收]` 时调用 API 存入
   - 通过生存周期或标签实现四层记忆管理

### 第三步：打通全链路

运行 Cerebella Core，系统自动监听任务文件夹，通过 Open WebUI 互动，知识沉淀到 SuperMemory。

---

## 5. 后续迭代方向

- **专业脑训练**：利用 Unsloth 微调专属 LoRA 模型，注册到 Ollama
- **技能卡片化**：LoRA 模型 + Dify 工作流 + SuperMemory 记忆库打包为"技能卡"
- **项目脑增强**：自动组建临时"项目组"协同工作

---

*本方案来自 Cerebella 项目 · 由 GCAT 整理*
*提供一种实现思路给想自己动手的开发者参考*
