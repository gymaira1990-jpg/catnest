# CatNest 仓库治理规范

## 本仓库是做什么的

CatNest（猫窝）是 G-CAT 数字文明研究的唯一容器：理论、项目、史记与工具。
涵盖诺亚世界协议、诺亚法典、巴别塔实验、小脑引擎 Cerebella、人造矿脉 AAD、
浑天核心计算 HCC、论文合集、经验分享等大类。

## 目录与命名规范

- 顶级大类用 `NN-名称/` 编号前缀（00-论文合集 / 01-诺亚 / ... / 08-金闪闪协议）
- 经验分享：`经验分享/NN-名称/README.md`（单 README 即文章全文）
- 新增大类/子项目必须同步更新 README 的四处：目录树 + 章节表格 + 统计数字 + 底部统计

## 发布流程（公开仓库红线）

1. **隐私审计**：push 前扫描本地用户名路径 / 真实 IP / API Key / token 模式，0 命中才可 push
2. **仓库治理门禁**：LICENSE / .github 五件套 / AGENTS.md / CHANGELOG.md 齐全
3. **版本一致**：README badge = VERSION = CHANGELOG 最新版本号一致
4. **双 remote 同步**：GitHub (origin) + ATomGIT (atomgit) 都要 push
5. 用经典 PAT（ghp_）push，细粒度 PAT 仅 API 读操作

## 提交规范

- 格式：`类型: 描述`（feat/fix/docs/refactor/chore）
- 禁止提交：.env / .pem / .key / .bak / 模型文件 / 保险柜内容
- 提交前 `git status` 确认无遗漏，重要节点打 tag

## 禁止事项

- ❌ 不提交真实服务器 IP、SSH 配置、API 密钥、Windows 路径
- ❌ 不用旧 workspace 覆盖线上（先拉取对比）
- ❌ 不在 README 里写死版本号（同步时易遗漏）
