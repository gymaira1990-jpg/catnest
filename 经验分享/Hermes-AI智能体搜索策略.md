# Hermes AI 智能体：个人级搜索策略、工具与玩法实战

> **副标题：** 从 CDP 清理到三层降级，零成本打造 AI Agent 专属搜索体系
>
> **作者：** G-CAT | **日期：** 2026-06-27 | **模型：** Hermes Agent + DeepSeek V4 Pro
>
> **摘要：** 记录一次完整的搜索基建重构：清除旧的 Edge CDP / Snap Chromium CDP 两套混乱方案，引入 browser-use、Crawl4AI、Tavily 三类工具，构建"三层降级"搜索+提取体系。全程在 Hermes Agent 上实战，包含完整命令、架构图和踩坑记录。

---

## 一、起点：CDP 的混乱局面

我们的 WSL 环境里残留着两套 CDP（Chrome DevTools Protocol）方案：

- **Edge CDP**：通过 Windows 端口转发 `9226→9225`，连接 Windows Edge 浏览器
- **Snap Chromium CDP**：通过 WSL 本地 Chromium 的远程调试端口

这两套方案共存导致：
1. **端口冲突**：多个 CDP 端口监听、防火墙规则混乱
2. **进程僵尸**：Chromium 进程退出后父进程未回收，积累 `<defunct>` 僵尸进程
3. **可靠性差**：Edge 随 Windows 关机重启丢失连接，portproxy 需要 PowerShell 管理
4. **无登录态**：每次启动都是新 profile，无法携带登录信息

最终的决策：**一刀切，全部清掉，重新设计。**

```bash
# 删除旧 CDP 脚本
rm ~/.hermes/scripts/cdp-tool.py
rm ~/.hermes/scripts/cdp-playwright.py
rm ~/.hermes/scripts/chromium-cdp.py

# 清理 Hermes 配置
hermes config set web.backend ""
hermes config set browser.cdp_url ""
```

---

## 二、新架构：三层降级 + 三个工具

### 2.1 整体策略

本次重新设计的核心理念是"降级链"——策略 1 失败自动走策略 2，再失败走策略 3。

**搜索链路：**

```
Tavily Search API → Crawl4AI + 豆包Mini → browser-use + Snap Chromium
     (快速)            (0成本无限量)           (真实profile, 最后手段)
```

**提取链路：**

```
Tavily Extract API → Crawl4AI + Playwright → browser-use Agent + 豆包
    (最干净)            (Magic Mode反爬)        (AI视觉推理)
```

### 2.2 三个工具各司其职

| 工具 | 核心能力 | 浏览器 | 使用场景 |
|------|---------|--------|---------|
| **Tavily** | 搜+取一体 API | 无 | 日常主力搜索和提取 |
| **Crawl4AI** | 本地专业爬虫 | Playwright Chromium | 批量抓取、LLM提炼 |
| **browser-use** | AI 驱动的操作 | Snap Chromium 真实profile | 登录态操作、视觉识别、鼠标模拟 |

---

## 三、工具配置细节

### 3.1 browser-use — AI 驱动的浏览器自动化

**安装：**

```bash
cd ~/.hermes/hermes-agent/venv/bin
./pip install browser-use[core]
```

**配置要点：**

- 使用 Snap Chromium 149 作为浏览器引擎
- 复用真实用户 profile（`~/snap/chromium/common/chromium/Default`），保留所有登录态
- 通过 Privoxy（`:8118`）代理出墙访问 Google/Bing
- Baidu 直连（Privoxy 自动分流）
- 中文界面：`--lang=zh-CN` + `LANG=zh_CN.UTF-8` 环境变量
- 禁用默认扩展下载（避免 GFW 下超时）：`enable_default_extensions=False`

**关键坑：** `--disable-setuid-sandbox` 在 Chromium 149 中已废弃，删掉避免警告。

```python
from browser_use import Browser

browser = Browser(
    executable_path="/snap/bin/chromium",
    headless=False,                              # 有头模式，Windows 可见
    user_data_dir="~/snap/chromium/common/chromium",
    profile_directory="Default",                 # 真实用户登录态
    args=["--no-sandbox", "--lang=zh-CN"],       # 中文界面
    enable_default_extensions=False,             # 不下载扩展
    proxy={"server": "http://127.0.0.1:8118"},   # Privoxy 代理
    env={"LANG": "zh_CN.UTF-8", "LC_ALL": "zh_CN.UTF-8"},
)
```

**进程管理：** browser-use 关闭后 Chromium 子进程可能成为僵尸。我们写了专门的 `cleanup` 子命令：

```bash
./browser-search.py cleanup  # 清理所有残留进程 + 僵尸 + /tmp 临时文件
```

### 3.2 Crawl4AI — 专业内容提取引擎

**安装踩坑：**

Ubuntu 26.04 + Python 3.14 环境下 `pip install crawl4ai` 会遇到 `lxml` 构建失败。解决方案：

```bash
# 1. 先装系统依赖
sudo apt install -y libxml2-dev libxslt-dev

# 2. lxml 用预编译包
./pip install lxml --only-binary :all:

# 3. 再装 crawl4ai 本体
./pip install crawl4ai
```

**Playwright 浏览器安装：**

Playwright 官方不支持 Ubuntu 26.04 安装 Chromium，通过 npm 的 Playwright 下载：

```bash
# npm 版不受 OS 检测限制
npx playwright install chromium
# 下载的浏览器在 ~/.cache/ms-playwright/chromium-1228/

# 创建 v1223→v1228 软链接（Crawl4AI 期望 v1223）
ln -sf ~/.cache/ms-playwright/chromium-1228 ~/.cache/ms-playwright/chromium-1223
```

**LLM 集成：** Crawl4AI 通过 LiteLLM 支持任意模型。我们配置了豆包 Mini 作为提取模型：

```python
from crawl4ai import LLMConfig, CrawlerRunConfig

# 豆包 Mini — 最便宜、支持 structured output
config = CrawlerRunConfig(
    magic=True,                    # 反爬模式
    extraction_strategy=...        # LLM 提取策略
)
```

**豆包 Mini vs Lite 对比：**
- 同一个 "say hello in JSON" 请求
- Lite：182 tokens
- Mini：134 tokens
- **Mini 省 26% token**

### 3.3 Tavily — 主力搜索引擎

Tavily 有 1,000 次/月的免费额度。在我们的测试中，搜中文和英文都有 AI 摘要：

```
🔍 搜索: Hermes agent nous research
   Tavily API...
  📝 AI摘要: Hermes Agent is an open-source AI agent developed by Nous Research...
  ✅ Tavily API 搜索成功 (5条)
  1. Hermes Agent — Open-Source AI Agent with Persistent Memory
     https://hermes-agent.org
```

配置在 `~/.hermes/.env`：

```bash
TAVILY_API_KEY=tvly-dev-xxxx
```

---

## 四、实战脚本：browser-search.py

整个工具栈封装在一个 Python 脚本中：

```
~/.hermes/scripts/browser-search.py
```

### 4.1 搜索模式

```bash
# 自动模式（推荐，Tavily 主力）
python3 browser-search.py search "大语言模型 2026" --yes

# 指定百度
python3 browser-search.py search "AI Agent框架" --engine baidu --yes

# 指定 Google
python3 browser-search.py search "browser-use framework" --engine google --yes
```

### 4.2 提取模式

```bash
# 自动选择最优提取策略（Tavily → Crawl4AI → browser-use Agent）
python3 browser-search.py extract "https://...." --yes
```

实测：Wikipedia 文章提取出 **202,267 字符**，GitHub 页面 **18,042 字符**。

### 4.3 Agent 模式

browser-use + 豆包 Mini 驱动的智能操作。支持：
- 视觉识别（能"看"页面）
- 鼠标模拟（点击、输入、滚动）
- 人类暂停（遇到 CAPTCHA 可停下来让你操作）

```bash
python3 browser-search.py agent "在知乎搜索 AI Agent 框架，对比前三个的开源 Star 数"
```

---

## 五、代理与网络配置

```
                  ┌─────────────────────┐
                  │    WSL (Python)     │
                  │  browser-use       │
                  │  Crawl4AI          │
                  │  Tavily            │
                  └────────┬───────────┘
                           │
                    ┌──────▼──────┐
                    │  Privoxy    │  :8118 HTTP 代理
                    │  本地服务    │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
          ┌──────┐    ┌──────┐    ┌──────┐
          │Baidu │    │Google│    │Bing  │
          │ 直连 │    │ 隧道 │    │ 隧道 │
          └──────┘    └──────┘    └──────┘
              │            │            │
              └────────────┼────────────┘
                           │
                    ┌──────▼──────┐
                    │  SOCKS5    │  :1081 GZ 隧道
                    │  autossh   │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  GZ 服务器   │
                    └─────────────┘
```

Privoxy 自动分流：百度直连，Google/Bing 走 SOCKS5 隧道。浏览器只需配置 `--proxy-server=http://127.0.0.1:8118` 即可。

---

## 六、踩坑记录

### 坑1：browser-use Agent 与 DeepSeek 不兼容

```
Error: 'This response_format type is unavailable now'
```

根因：browser-use 内部调用 `response_format: json_object` 参数，DeepSeek 不支持。

**解决：** 换用豆包，豆包支持 `json_object` 格式。

### 坑2：Snap Chromium 与 Playwright 浏览器版本不匹配

Snap Chromium 149 不识别 Playwright 的特殊 flags（如 `--disable-field-trial-config`），导致直接配合失败。

**解决：** 用 npm Playwright 下载专属浏览器（v1228），Snap Chromium 专供 browser-use 使用，Playwright Chromium 专供 Crawl4AI 使用。

### 坑3：Crawl4AI 加载默认扩展卡死

Crawl4AI 默认 `enable_default_extensions=True`，会尝试下载 uBlock Origin，在 GFW 下超时。

**解决：** `BrowserConfig(enable_default_extensions=False)`

---

## 七、接入 Hermes

创建了 `gcat-web-search` 技能，Hermes 可以直接调用：

```
hermes skills list | grep gcat
# → gcat-web-search (devops, enabled)
```

今后在 Hermes 中说"搜一下 AI 最新动态"，自动走 Tavily → Crawl4AI → browser-use 三层降级链。

---

## 八、总结

**重构前：**
- 2 套 CDP 方案互相冲突
- browser-use Agent 无法用（DeepSeek 不兼容）
- 内容提取全靠手写 JS

**重构后：**
- 3 个工具、3 层降级
- 搜索：Tavily（AI 摘要 + 结构化结果）
- 提取：Crawl4AI（Magic Mode + LLM 提炼）
- 操作：browser-use（豆包驱动 + 真实 profile）
- 进程管理、代理链、中文界面全部齐备
- 接入 Hermes 技能体系，自然语言触发

**预算：** 0 元/月（Tavily 免费 1K 次 + Crawl4AI 自部署 + 豆包 token 极便宜）

---

> **交流与反馈：** 本文基于 G-CAT 的个人基础设施编写。欢迎在 GitHub 上提出改进建议。
