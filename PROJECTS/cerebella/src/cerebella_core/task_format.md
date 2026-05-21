# Cerebella 任务书 (.task) 标准

## 文件格式

YAML 头部元数据 + Markdown 正文。

```yaml
---
task_id: "唯一ID（自动生成或手动指定）"
title: "任务标题"
capability: "所需能力标签（如 coding/chat/reasoning/vision）"
status: "pending"        # pending → in_progress → completed → verified
assigned_to: ""          # 路由中心分配后填写
assigned_model: ""       # 实际执行模型
created_at: "2026-04-29T06:00:00"
updated_at: "2026-04-29T06:00:00"
completed_at: ""
tags: []                 # 可选标签
---

## 任务描述

详细的需求描述。

## 产出物

预期交付的内容。

## 验收标准

怎样算完成。
```

## 状态机

```
pending ──→ in_progress ──→ completed ──→ verified
              ↑                  │              │
              └── 失败可退回 ────┘              │
                   pending                      │
                                                │
           archived（完成后自动归档到看过的/）
```

## 文件位置

- 任务发布区：`~/Cerebella/tasks/`（放入即触发）
- 进行中：原地更新 status 字段
- 已完成：原地标记 completed
- 已验收：移到 `~/Cerebella/tasks/看过的/`
