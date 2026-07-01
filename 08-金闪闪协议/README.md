# 金闪闪协议 (Goldshine Protocol)

> 一种基于智能体封装的去中心化全球能力交付网络  
> A Decentralized Global Capability Delivery Network Based on Agent Encapsulation

---

## 项目概述

**金闪闪协议**是本研究的第 08 号项目，也是「智能体操作系统」研究体系的**第二部分**。

- **第一部分**（07-注册表、编译器与云内存）：单节点 Agent OS 架构
- **第二部分**（本项目）：从单节点扩展至全球网络 — 智能体间的互联协议、协作机制与经济治理体系

## 核心概念：「插管」—— 来自实战的启发

金闪闪协议的核心范式源于一次真实的双向插管实验（2026-06-21）：

### 实验背景

Windows 环境运行 Hermes Desktop，WSL 环境运行 Hermes Agent CLI。两个 Agent 各有所长：
- Windows Agent：浏览器控制、Office 操作、桌面自动化
- WSL Agent：本地 LLM 推理、Docker 编排、Linux 工具链、MCP 服务器

### 实验过程

互相开启 API Server（OpenAI Chat Completions 兼容端点），让两个 Agent 能够互相调用：

```
Windows Hermes ←→ API Server ←→ WSL Hermes
     (浏览器/Office)              (LLM/Docker/MCP)
```

### 核心发现

当 Windows Agent 调用 WSL Agent 时，WSL Agent **直接带入了全套装备**：
- 本地 Qwen 推理引擎
- 10+ MCP 工具服务器
- 独立记忆系统（SQLite + PostgreSQL）
- 106 条预装技能
- xray + privoxy 代理链路

**Windows Agent 不需要安装任何东西**。它只需要向 WSL Agent 的 API 端点发一条请求，WSL Agent 就用自己完整的工具链完成工作并返回成品。

### 从实验到理论

这就是金闪闪协议的核心范式：

```
传统方案（工具级）：   借给你扳手 → 你自己学修车 → 自己修
「插管」方案（Agent级）： 把车给 Agent → Agent 自带工具箱 → 修好还给你
```

在传统模式下（MCP、Function Calling），调用方需要知道："我要调哪个函数、传什么参数、怎么处理返回"。在「插管」模式下，调用方只需要说："帮我搞定这件事"。**被调 Agent 的完整能力（推理引擎、领域知识、工作流、记忆系统、工具链）封装在一个标准 API 端点背后，对所有调用方透明可见。**

一个封装了完整能力的智能体（Agent Service Unit, ASU），对外暴露的就是标准 API —— 本地无需任何专业技能的 Agent，只需「插上管子」就能获得完整成品交付。

这是从「交付零件」到「交付成品」的质变，也是金闪闪协议「能力交付颗粒度升维」的实验基础。

## 技术架构

| 层 | 职责 |
|----|------|
| **L0 终端接入层** | 用户意图解析、语义帧生成 |
| **L1 ASU节点层** | 智能体服务单元：推理引擎+领域知识+工作流+记忆+协议适配 |
| **L2 调度发现层** | 双层发现（DHT静态+实时探测）、匹配排序、DAG编排 |
| **L3 治理层** | 多维信誉、质押惩罚、分层仲裁、通证经济 |

## 核心贡献

1. **ASU 形式化五元组**：物理级记忆隔离，架构层面解决上下文污染
2. **金闪闪语义本体**：意图驱动精准匹配，去语言化交互
3. **去中心化信任体系**：多维信誉+质押+仲裁，博弈仿真验证收敛性
4. **虚实贯通**：从数字到物理世界的全供应链协作
5. **MVP 实证**：最小可行原型验证工程可行性

## 文件

| 文件 | 说明 |
|------|------|
| `金闪闪协议1.5.2版完整全文.pdf` | 🇨🇳 中文原版 (v1.5.2, 2026-06-22) |
| `Goldshine_Protocol_v1.5.2.pdf` | 🇬🇧 英文版 |

## 发布

- **DOI**: [10.5281/zenodo.20789868](https://doi.org/10.5281/zenodo.20789868)
- **Zenodo**: https://zenodo.org/records/20789868
- **许可**: CC BY-SA 4.0
- **作者**: geng, yong (ORCID: 0009-0001-3344-6792)

## 术语

- **ASU** (Agent Service Unit): 智能体服务单元
- **GSO** (Goldshine Semantic Ontology): 金闪闪语义本体
- **MVP** (Minimum Viable Prototype): 最小可行原型
