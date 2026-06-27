# Hermes AI 智能体：个人级搜索策略、工具与玩法实战

> **副标题：** Tavily + Crawl4AI + browser-use — 三层降级，零成本打造 AI Agent 专属搜索体系
>
> **作者：** G-CAT | **日期：** 2026-06-27
>
> **适用环境：** Hermes Agent + WSL/Linux | **依赖：** Python ≥3.11

---

## 一、为什么需要自己的搜索体系？

如果你在用 Hermes Agent 或类似的 AI 智能体，你可能遇到过这些问题：

- `web_search` 返回的结果质量参差不齐，中文内容尤其灾难
- 需要抓取网页内容时，工具返回的是截断的、带广告和导航的 HTML 垃圾
- 有些网站需要登录才能看（GitHub、知乎），普通抓取直接 403
- 被反爬虫机制拦截，拿不到真正的正文
- 想让 Agent 像人一样操作浏览器（点击、滚动、填表），但现有工具做不到

**「为什么不用 Google Custom Search API？」** — 100 次/天免费额度，用完就收费，且结果不带 AI 摘要。对于每天几十次的 Agent 搜索需求，一周就超了。

**「为什么不用 DuckDuckGo？」** — 中文搜索结果质量极差，几乎不可用。英文尚可但远不如 Tavily 的结构化输出。

**「为什么不只用 Playwright？」** — Playwright 是浏览器自动化框架，不是 AI 搜索工具。它提供的是 API 级控制（点击元素、等待加载），但不知道"该搜什么""该点哪里"。你需要一个 **AI 大脑**来决策。

这套方案用三个工具覆盖全场景，总成本：**一台能跑 Python 的机器 + 免费的 Tavily API（1,000次/月）+ 豆包 token（极便宜）**。

---

## 二、架构设计：三层降级策略

### 核心设计理念

```
搜索链路:
  Tavily API → Crawl4AI + 智谱/豆包 → browser-use Agent
  (最快/最便宜)    (0 成本无限量)         (真实浏览器, 最后手段)

提取链路:
  Tavily Extract → Crawl4AI Playwright → browser-use Agent
  (最干净/结构化)   (Magic Mode 反爬)      (AI 视觉驱动)
```

**关键原则：不依赖任何单一工具。** 每一层失败自动降级到下一层。首个成功的结果即刻返回，不会因为某个 API 挂了就整体失败。

### 三个工具定位

| 工具 | 角色 | 核心能力 | 适合场景 | 免费额度 |
|------|------|----------|----------|----------|
| **Tavily** | 主力搜索+提取 | AI 摘要 + 结构化结果 | 日常搜索、快速提取 | 1,000次/月 |
| **Crawl4AI** | 专业抓取 | 本地爬取、LLM 提炼、批量 | 复杂页面、大量抓取 | 无限（自部署） |
| **browser-use** | AI 操作 | 视觉识别、鼠标模拟、登录态 | 登录操作、多步骤任务 | 无限（自部署） |

### 决策树：什么时候用哪个？

```
用户问"搜索/查一下/找一下 X" 
  → Tavily 直接搜 → 返回结构化结果 ✅

用户给了一个 URL 要"提取/阅读/分析内容"
  → Tavily Extract → 成功 → 返回 Markdown ✅
  → 失败（反爬/需要JS渲染）→ Crawl4AI Magic Mode ✅
  → 失败（需要登录/复杂交互）→ browser-use Agent ✅

用户说"打开 GitHub 帮我..." 或 "登录 XX 网站..."
  → browser-use Agent（真实浏览器 + 登录态）✅
```

---

## 三、工具一：Tavily — 主力搜索引擎

### 为什么是 Tavily？

在选型时我对比了多个方案：

| 方案 | 优点 | 缺点 | 结论 |
|------|------|------|------|
| Google Custom Search | 搜索结果质量高 | 100次/天免费，超量收费；无 AI 摘要 | ❌ |
| DuckDuckGo API | 免费 | 中文结果极差 | ❌ |
| Bing Search API | 结构化好 | 需要 Azure 订阅，流程繁琐 | ❌ |
| Serper.dev | 速度快 | 收费（$50/月起） | ❌ |
| **Tavily** | AI 摘要+结构化+1K次/月免费 | 偶尔延迟（3-5秒） | ✅ |

Tavily 是 **专为 AI Agent 设计的搜索引擎**。它不只是返回链接和标题——每条结果都带着 AI 生成的摘要和相关性评分。对中文搜索的支持也相当不错。

### 安装配置

```bash
# 1. 注册获取 API Key：https://tavily.com
#    免费额度 1,000 次/月，足够个人 Agent 使用

# 2. 配置到 Hermes
echo "TAVILY_API_KEY=tvly-你的密钥" >> ~/.hermes/.env

# 3. 告诉 Hermes 使用 Tavily
hermes config set web.search_backend tavily
hermes config set web.extract_backend tavily
```

配置完成后，Hermes 的 `web_search` 和 `web_extract` 工具会自动走 Tavily。

### 效果对比

**普通搜索返回：**
```
标题 + URL + 一段截断的描述
```

**Tavily 搜索返回：**
```json
{
  "title": "文章标题",
  "url": "https://...",
  "content": "AI 生成的约 200 字内容摘要",
  "score": 0.92,
  "raw_content": null
}
```

关键差异：`content` 字段是**经过 AI 提炼的摘要**，不是网页的前 200 个字符。这意味着 Agent 不需要打开网页就能判断这篇文章是否相关。

### 提取模式

Tavily Extract 是把整个网页下载下来，再用 AI 提取纯净正文（去广告、去导航、去评论区）。返回的是干净 Markdown。

```bash
# Hermes 里直接调用
web_extract("https://example.com/article")
# 返回：标题 + 正文 Markdown
```

**注意：** 提取模式消耗 1 次 API 额度（和搜索一样）。1,000 次/月对个人 Agent 通常够用，但如果每天大量提取，建议用 Crawl4AI 分担。

---

## 四、工具二：Crawl4AI — 专业内容抓取引擎

### 为什么需要它？

Tavily Extract 有两个局限：
1. **消耗 API 额度**（每次 1 次调用）
2. **对需要 JS 渲染的页面可能拿不到内容**（SPA 应用、动态加载）

Crawl4AI 解决了这两个问题：
- **零成本无限量** — 完全在本地运行
- **真实浏览器渲染** — 内置 Playwright，能执行 JavaScript
- **Magic Mode** — 自动绕过 Cloudflare、反爬虫机制
- **LLM 智能提取** — 用 AI 从 HTML 中提取结构化数据

### 安装

```bash
# 安装 crawl4ai
pip install crawl4ai

# 安装系统依赖（Ubuntu/Debian）
sudo apt install -y libxml2-dev libxslt-dev

# 安装 Playwright 浏览器
playwright install chromium
```

### 基础用法

```python
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig

async with AsyncWebCrawler() as crawler:
    result = await crawler.arun(
        url="https://example.com/article",
        config=CrawlerRunConfig(
            magic=True,                     # 反爬模式
            word_count_threshold=15,        # 过滤太短的片段
            remove_overlay_elements=True,   # 去掉弹窗/广告
        )
    )
    print(result.markdown)  # 干净的 Markdown
```

### LLM 智能提取

当页面结构复杂（论坛、文档站、多栏目页面），直接用 Markdown 可能包含大量噪音。让 LLM 帮你筛：

```python
from crawl4ai import LLMConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy

llm_strategy = LLMExtractionStrategy(
    llm_config=LLMConfig(
        provider="openai/gpt-4o-mini",      # 或 doubao-seed-2-0-mini
        api_token="你的API密钥",
    ),
    instruction="提取正文内容，去掉导航、广告、评论、侧边栏",
    chunk_token_threshold=2000,             # 超过此 token 数自动分段
)

config = CrawlerRunConfig(
    extraction_strategy=llm_strategy,
    magic=True,
)
```

**省钱提示：** 提取任务不需要强模型。GPT-4o-mini 或豆包 Mini 足够，一个页面约消耗 1,000-3,000 token（豆包 Mini 约 ¥0.0005-0.0015）。

### 批量并行抓取

```python
urls = [
    "https://site1.com/page1",
    "https://site2.com/article",
    "https://site3.com/docs",
]

async with AsyncWebCrawler(max_pages=3) as crawler:
    results = await crawler.arun_many(urls, config=config)
    for r in results:
        print(f"标题: {r.metadata.get('title', 'N/A')}")
        print(f"内容长度: {len(r.markdown)} 字符")
```

`max_pages=3` 表示同时打开 3 个浏览器页面并行抓取。注意别设太高——每个页面约消耗 200-400MB 内存。

---

## 五、工具三：browser-use — AI 驱动的浏览器 Agent

### 什么时候需要它？

前面两个工具覆盖了 90% 的场景。剩下的 10% 才是 browser-use 的用武之地：

- **需要登录的网站**（GitHub private repo、知乎、付费内容）
- **多步骤操作**（搜索 → 点结果 → 翻页 → 提取）
- **需要视觉理解的页面**（验证码、图表、截图）
- **复杂交互**（填表、下拉选择、文件上传）

browser-use 本质上是一个**用 AI 大脑驱动的浏览器**。你给它一个自然语言任务，它自己决定点击哪里、输入什么、等待多久。

### 安装

```bash
pip install browser-use[core]

# 确保系统有 Chromium
# Ubuntu/Debian:
sudo apt install chromium-browser
# 或 Snap:
snap install chromium
```

### 基础配置

```python
from browser_use import Browser

browser = Browser(
    executable_path="/usr/bin/chromium-browser",
    headless=False,                           # 有头模式，方便观察
    args=["--no-sandbox"],
    proxy={"server": "http://127.0.0.1:8118"}, # 需要代理时添加
)
```

### 使用真实浏览器 Profile（保留登录态）

这是 browser-use 最强大的玩法：**直接复用你日常浏览器的登录态**，无需每次在代码里处理验证码和登录流程。

```python
browser = Browser(
    user_data_dir="~/.config/chromium",       # Chromium 默认配置目录
    profile_directory="Default",              # 使用默认 Profile
    headless=False,
)
await browser.start()
# 浏览器打开后你已经登录了 GitHub、Google 等
await browser.navigate_to("https://github.com/你的私有仓库")
```

**注意：** 有头模式下浏览器窗口会弹出来。如果是在服务器上跑，用 `headless=True`，但需要单独准备一个登录过的 headless profile。

### Agent 模式（AI 驱动操作）

```python
from browser_use import Agent, Browser
from browser_use.llm.openai.chat import ChatOpenAI

# LLM 配置（推荐豆包 Mini，便宜且支持 structured output）
llm = ChatOpenAI(
    model="doubao-seed-2-0-mini-260215",
    api_key="你的豆包API密钥",
    base_url="https://ark.cn-beijing.volces.com/api/v3",
)

agent = Agent(
    task="打开 GitHub，搜索 browser-use 项目，告诉我 Star 数和最近更新日期",
    llm=llm,
    browser=browser,
    use_vision=True,          # 启用视觉识别
)

result = await agent.run()
print(result)
```

**`use_vision=True` 的作用：** Agent 不只是看 DOM 树，还会「截图」并用视觉 AI 分析页面。这对理解图表、识别布局、处理非标准 HTML 至关重要。

### 关键 LLM 选型注意事项

browser-use Agent 内部使用 `response_format: json_object` 模式（要求 LLM 输出结构化 JSON）。**DeepSeek 不支持这个参数** —— 如果用了 DeepSeek，Agent 会报 400 错误。

| LLM | 支持 `response_format`? | 推荐？ |
|-----|------------------------|--------|
| GPT-4o / GPT-4o-mini | ✅ | ✅ 效果好但贵 |
| Claude 3.5 Sonnet | ✅ | ✅ 效果好但贵 |
| 豆包 Mini/Lite | ✅ | ✅ **推荐**（便宜+支持） |
| DeepSeek V3/V4 | ❌ | ❌ 不支持 |

**推荐方案：** 豆包 `doubao-seed-2-0-mini`。单个简单任务约消耗 5,000-15,000 token（¥0.002-0.007），复杂任务 20,000-50,000 token（¥0.01-0.025）。

---

## 六、代理配置：让工具在墙内正常工作

如果你的环境在中国大陆，Tavily API 可以直接访问（它托管在境外但没被墙），但 Google、GitHub、Twitter 等网站需要代理。

### 推荐方案：Privoxy 自动分流

```
浏览器 → Privoxy (:8118) → SOCKS5 隧道 → 境外服务器 → 目标网站
                ↓
        国内网站直连 (自动分流，不走隧道)
```

**Privoxy 配置（`/etc/privoxy/config`）：**

```config
# 所有流量默认走 SOCKS5 隧道
forward-socks5 / 127.0.0.1:1080 .

# Privoxy 默认监听 127.0.0.1:8118
listen-address 127.0.0.1:8118
```

所有工具的 proxy 参数统一填 `http://127.0.0.1:8118`：

```python
# Crawl4AI
BrowserConfig(proxy="http://127.0.0.1:8118")

# browser-use
Browser(proxy={"server": "http://127.0.0.1:8118"})

# Playwright
browser = await playwright.chromium.launch(
    proxy={"server": "http://127.0.0.1:8118"}
)
```

### 检查代理是否工作

在开始任何依赖外网的操作前，养成先验证的习惯：

```bash
# 测试代理连通性
curl -s --max-time 5 -x http://127.0.0.1:8118 https://www.google.com -o /dev/null -w "%{http_code}"
# 返回 200 = 代理正常

# 对比直连（应该超时或 000）
curl -s --max-time 5 https://www.google.com -o /dev/null -w "%{http_code}"
# 返回 000 或超时 = 直连被墙，确认需要代理
```

---

## 七、集成脚本：一条命令搞定搜索

把三个工具封装到 `~/.hermes/scripts/browser-search.py`，Hermes 通过 skill 自动调用。

### 搜索模式（自动降级）

```bash
# 日常使用（Tavily 主力，最快最便宜）
python3 browser-search.py search "大语言模型 2026 最新进展" --yes

# 指定引擎
python3 browser-search.py search "AI Agent 框架" --engine google --yes
python3 browser-search.py search "深度学习" --engine baidu --yes

# --yes：跳过交互确认，适合自动化/Agent 调用
```

内部逻辑：Tavily API 搜索 → 成功则返回 → 失败则走 Crawl4AI → 失败则走 browser-use。

### 提取模式（自动降级）

```bash
# 自动选择最优策略
python3 browser-search.py extract "https://example.com/deep-article" --yes

# 策略：Tavily Extract → Crawl4AI Magic → browser-use Agent
```

### Agent 模式（手动触发，不走降级）

```bash
# AI 驱动的复杂浏览器操作
python3 browser-search.py agent "在知乎搜索 '大模型推理优化'，打开前 3 篇文章，提取每篇的核心观点"
```

### 进程清理

```bash
# 杀掉残留的 Chromium 进程
python3 browser-search.py cleanup
```

**为什么需要这个？** 浏览器操作异常退出时可能留下僵尸 Chromium 进程，占用内存和端口。建议定时清理或设为 cron。

---

## 八、接入 Hermes Agent

创建技能文件让 Hermes 自动识别搜索意图：

```bash
# 文件路径：~/.hermes/skills/devops/gcat-web-search/SKILL.md
```

技能内容（简化版）：

```markdown
# Trigger keywords
搜索 | 查一下 | 搜一下 | 提取 | 抓取 | 帮我搜

# Action
web_search → Tavily (默认)
web_extract → Tavily Extract → Crawl4AI → browser-use (自动降级)
复杂操作 → browser-search.py agent
```

配置完成后，当你说"帮我搜一下最新的 LLM 架构论文"，Hermes 自动调用 `web_search`（走 Tavily）；当你说"提取这篇文章的内容"，自动走提取链路。

---

## 九、踩坑记录（真实经历）

### 1. 浏览器版本不匹配 — Playwright Chromium vs 系统 Chromium

**现象：** `playwright install chromium` 下载的版本是 Chromium 1228，但 Crawl4AI 0.9.0 期望的是 1223。启动时报 `BrowserType.launch: Executable doesn't exist`。

**解决：** 创建软链接：

```bash
ln -sf ~/.cache/ms-playwright/chromium-1228 ~/.cache/ms-playwright/chromium-1223
```

**教训：** Crawl4AI 和 Playwright 的版本耦合很紧。升级 Crawl4AI 后务必检查 Playwright 浏览器版本匹配。

### 2. 代理下载超时 — Crawl4AI 默认下载浏览器扩展

**现象：** 首次运行 Crawl4AI 时卡在"Downloading extensions..."，几分钟后超时。在 GFW 环境下，从 Chrome Web Store 下载扩展（如 uBlock Origin）必然超时。

**解决：** 关闭默认扩展下载：

```python
from crawl4ai import BrowserConfig

config = BrowserConfig(
    enable_default_extensions=False,  # 关键！
)
```

**教训：** 所有会触发外部下载的功能在 GFW 环境下都可能超时。安装工具后第一次运行要在配置中明确关闭这类选项。

### 3. DeepSeek 不能用于 browser-use Agent

**现象：** 用 DeepSeek 作为 browser-use Agent 的 LLM，报错 `400 Bad Request: response_format not supported`。

**根因：** browser-use Agent 内部使用 OpenAI 的 `response_format: {"type": "json_object"}` 参数要求 LLM 输出结构化 JSON。DeepSeek API 不支持此参数。

**解决：** 换用豆包 Mini/Lite 或任何支持 `response_format` 的 OpenAI 兼容 API。

```python
# ✅ 豆包 Mini（推荐：便宜+支持）
llm = ChatOpenAI(
    model="doubao-seed-2-0-mini-260215",
    api_key="...",
    base_url="https://ark.cn-beijing.volces.com/api/v3",
)

# ❌ DeepSeek
llm = ChatOpenAI(
    model="deepseek-chat",  # 不支持 response_format
    ...
)
```

**教训：** 在选 Agent 驱动模型前，先确认它是否支持 `response_format: json_object`。不是所有 OpenAI 兼容 API 都完整实现了这个特性。

### 4. 进程残留 — 浏览器异常退出后 Chromium 还在跑

**现象：** Agent 任务完成后，`ps aux | grep chromium` 发现多个残留进程，累计占用 2-3GB 内存。反复调用后系统内存耗尽。

**解决：**

```python
# 在 Agent 任务结束后确保清理
try:
    result = await agent.run()
finally:
    await browser.close()  # 必须 close
```

同时设置 `browser-search.py cleanup` 作为定时 cron：

```bash
# 每 4 小时清理一次残留
echo "0 */4 * * * python3 ~/.hermes/scripts/browser-search.py cleanup" | crontab
```

### 5. Snap Chromium 沙箱问题

**现象：** 用 Snap 安装的 Chromium 在无头模式下报 `Failed to move to new namespace: PID namespaces supported`。

**解决：** 启动时加上 `--no-sandbox`（仅在本地开发/受控环境使用）：

```python
browser = Browser(
    args=["--no-sandbox"],
)
```

**安全警告：** `--no-sandbox` 降低了浏览器安全性。仅在你信任的本地环境使用。不要在生产/公开服务中使用。

### 6. 中文页面编码问题

**现象：** Crawl4AI 提取某些中文页面时，Markdown 输出乱码。

**解决：** Crawl4AI 内部会自动处理编码，乱码通常是因为网站的 `<meta charset>` 声明错误。在配置中显式设置：

```python
config = CrawlerRunConfig(
    magic=True,
    page_timeout=30000,              # 30秒超时（中文站有时慢）
    wait_for="body",                 # 等页面加载完
)
```

---

## 十、总结

三个工具覆盖了 AI Agent 需要的所有搜索场景，总成本几乎为零：

| 层级 | 工具 | 场景 | 成本 | 需要代理？ |
|------|------|------|------|-----------|
| 搜 | Tavily | 日常搜索 + 快速提取 | 免费 1K次/月 | 否（直连可用） |
| 抓 | Crawl4AI | 大量抓取 + JS渲染 + 反爬 | 0 元（自部署） | 看目标网站 |
| 控 | browser-use | 登录操作 + 多步骤 + 视觉 | 豆包 token（约 ¥0.01/任务） | 看目标网站 |

**核心原则：**
1. 三层降级，无单点依赖
2. Tavily 是主力，大部分任务不需要后两层
3. 代理要提前验证，不要假设网络通
4. browser-use 的 LLM 不要选 DeepSeek（不支持 response_format）
5. 任务结束后记得 `browser.close()`

全文代码可直接复制运行。欢迎在 [GitHub](https://github.com/gymaira1990-jpg/catnest) 上交流改进。

---

> **作者：** G-CAT · **GitHub:** [gymaira1990-jpg/catnest](https://github.com/gymaira1990-jpg/catnest)
