# Hermes AI 智能体：个人级搜索策略、工具与玩法实战

> **副标题：** Tavily 主搜 + Crawl4AI 后援 + browser-use 操控浏览器 — 零成本 AI Agent 搜索工具链
>
> **作者：** G-CAT | **日期：** 2026-06-27
>
> **适用环境：** Hermes Agent + WSL/Linux | **依赖：** Python ≥3.11

---

## 一、为什么折腾这套工具链？

用 Hermes Agent 一段时间后，搜索是个绕不开的痛点：

- `web_search` 返回的结果质量参差不齐，中文内容尤其灾难
- 需要抓取网页内容时，工具返回的是截断的、带广告和导航的 HTML 垃圾
- 被反爬虫机制拦截，拿不到真正的正文
- 每天要手动做大量重复的浏览器操作（查资料、填表、翻页、提取），浪费时间

这套方案的思路：**Tavily 主搜，Crawl4AI 后援，browser-use 负责浏览器自动化操作。**

**「为什么不用 Google Custom Search API？」** — 100 次/天免费额度，用完就收费，且结果不带 AI 摘要。Agent 一天搜几十次，一周就超了。

**「为什么不用 DuckDuckGo？」** — 中文搜索质量惨不忍睹。英文尚可但远不如 Tavily 的结构化输出。

**「为什么不只用 Playwright？」** — Playwright 是浏览器自动化框架，不是搜索工具。它能控制浏览器但不知道"该搜什么"。需要一个 **AI 大脑**来做决策。

成本核算：**一台能跑 Python 的机器 + 免费的 Tavily API（1,000次/月）+ 豆包 token（极便宜）**。

---

## 二、架构总览

```
搜索链路:
  Tavily API → Crawl4AI + 豆包
  (主力搜索)    (后援抓取, 0成本无限量)

浏览器自动化:
  browser-use Agent
  (AI驱动浏览器, 解放手动操作)
```

搜索和抓取各有一个主力+一个后援。Tavily 挂了自动走 Crawl4AI，反过来不降级（Tavily 更快更便宜所以是首选）。browser-use 是独立功能线——当你需要登录、填表、批量操作时才用。

### 三个工具定位

| 工具 | 角色 | 核心能力 | 适合场景 | 免费额度 |
|------|------|----------|----------|----------|
| **Tavily** | 主力搜索 | AI 摘要 + 结构化结果 | 日常搜索、快速提取 | 1,000次/月 |
| **Crawl4AI** | 后援抓取 | Playwright 内置 + LLM 提炼 + 批量 | 复杂页面、大量抓取 | 无限（自部署） |
| **browser-use** | 浏览器自动化 | AI 视觉识别 + 鼠标模拟 + 登录态 | 登录操作、多步骤填表、复杂交互 | 无限（自部署） |

### 决策树：什么时候用哪个？

```
用户问"搜索/查一下/找一下 X" 
  → Tavily 直接搜 → 返回结构化结果 ✅

用户给了一个 URL 要"提取/阅读/分析内容"
  → Tavily Extract → 成功 → 返回 Markdown ✅
  → 失败（反爬/需要JS渲染）→ Crawl4AI Magic Mode ✅

用户说"帮我登录 XX 网站填表/批量操作"
  → browser-use Agent（AI 驱动浏览器自动化）✅
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
# 1. 打开 https://tavily.com 注册账号（用 GitHub/Google 直接登）
#    登录后到 Dashboard → API Keys → 复制密钥（tvly- 开头）
#    免费额度 1,000 次/月，个人 Agent 完全够用

# 2. 把密钥写到 Hermes 环境变量
echo "TAVILY_API_KEY=tvly-你的密钥" >> ~/.hermes/.env

# 3. 切 Hermes 的搜索后端
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

关键差异：`content` 字段是**AI 提炼的摘要**，不是网页前 200 个字符。Agent 不用打开网页就能判断相关性。

### 提取模式

Tavily Extract 把网页下载下来，AI 提取正文（去广告、去导航、去评论区），输出 Markdown。

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

## 五、工具三：browser-use — AI 驱动的浏览器自动化

### 定位：解放你的双手

前面两个工具（Tavily + Crawl4AI）覆盖了**搜索和抓取**的全部场景。browser-use 的定位不同——它是一个**浏览器操控 Agent**，而不是搜索引擎。它用 AI 帮你做那些烦人的手动操作：

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

**怎么拿豆包 API Key：**
1. 打开 [火山引擎 ARK](https://console.volcengine.com/ark) 注册/登录
2. 左侧菜单 → API Key 管理 → 创建 API Key
3. 复制 key 写到 Hermes 环境变量：`echo "ARK_API_KEY=你的key" >> ~/.hermes/.env`

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

## 七、集成脚本：browser-search.py 完整代码

把三个工具封到一个脚本，放在 `~/.hermes/scripts/browser-search.py`。

### 脚本核心结构

```python
#!/usr/bin/env python3
"""G-CAT AI搜索工具 — 三层工具链统一入口"""
import os, sys, json, asyncio, argparse
import requests

# ── 配置 ──
TAVILY_KEY = os.environ.get("TAVILY_API_KEY", "")
DOUBAO_KEY = os.environ.get("ARK_API_KEY", "")
DOUBAO_BASE = "https://ark.cn-beijing.volces.com/api/v3"

# ── 策略1：Tavily 搜索 ──
def tavily_search(query: str, max_results: int = 5) -> dict:
    """主力搜索，速度快、带AI摘要"""
    resp = requests.post(
        "https://api.tavily.com/search",
        json={"api_key": TAVILY_KEY, "query": query, "max_results": max_results}
    )
    return resp.json()

# ── 策略1b：Tavily 提取 ──
def tavily_extract(url: str) -> dict:
    """快速提取网页正文"""
    resp = requests.post(
        "https://api.tavily.com/extract",
        json={"api_key": TAVILY_KEY, "urls": [url]}
    )
    return resp.json()

# ── 策略2：Crawl4AI 抓取 ──
async def crawl4ai_extract(url: str) -> str:
    """后援抓取引擎 — JS渲染 + 反爬"""
    from crawl4ai import AsyncWebCrawler, CrawlerRunConfig

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url,
            config=CrawlerRunConfig(
                magic=True,
                remove_overlay_elements=True,
                word_count_threshold=15,
            )
        )
        return result.markdown

# ── 策略3：browser-use 浏览器操控 ──
async def browser_agent(task: str):
    """浏览器自动化 — 登录、填表、多步骤操作"""
    from browser_use import Agent, Browser
    from browser_use.llm.openai.chat import ChatOpenAI

    browser = Browser(
        headless=False,
        args=["--no-sandbox"],
        proxy={"server": "http://127.0.0.1:8118"},
    )
    llm = ChatOpenAI(
        model="doubao-seed-2-0-mini-260215",
        api_key=DOUBAO_KEY,
        base_url=DOUBAO_BASE,
    )
    agent = Agent(task=task, llm=llm, browser=browser, use_vision=True)
    result = await agent.run()
    await browser.close()
    return result

# ── 主入口 ──
def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="mode")

    p = sub.add_parser("search")
    p.add_argument("query")
    p.add_argument("--engine", default="auto")
    p.add_argument("--yes", action="store_true")

    p = sub.add_parser("extract")
    p.add_argument("url")
    p.add_argument("--yes", action="store_true")

    p = sub.add_parser("agent")
    p.add_argument("task")

    p = sub.add_parser("cleanup")

    args = parser.parse_args()

    if args.mode == "search":
        # 主力 Tavily，失败不降级（搜索链路Tavily为主）
        result = tavily_search(args.query)
        for r in result.get("results", []):
            print(f"📌 {r['title']}")
            print(f"   {r['url']}")
            print(f"   {r.get('content', '')[:120]}")
            print()
    elif args.mode == "extract":
        # Tavily Extract → 失败走 Crawl4AI
        try:
            r = tavily_extract(args.url)
            print(r["results"][0].get("raw_content", r["results"][0].get("content")))
        except:
            content = asyncio.run(crawl4ai_extract(args.url))
            print(content)
    elif args.mode == "agent":
        result = asyncio.run(browser_agent(args.task))
        print(result)
    elif args.mode == "cleanup":
        os.system("pkill -f chromium-browser 2>/dev/null; pkill -f ms-playwright 2>/dev/null")
        print("已清理 Chromium 进程")

if __name__ == "__main__":
    main()
```

### 使用方式

```bash
# 搜索（Tavily 主力）
python3 ~/.hermes/scripts/browser-search.py search "大语言模型 2026 最新进展" --yes

# 提取（Tavily → 失败走 Crawl4AI）
python3 ~/.hermes/scripts/browser-search.py extract "https://example.com/article" --yes

# 浏览器操控（手动触发，不参与降级）
python3 ~/.hermes/scripts/browser-search.py agent "登录 GitHub 找到她的简历并截图"

# 清理残留
python3 ~/.hermes/scripts/browser-search.py cleanup
```

`--yes` 跳过交互确认，适合 Agent 自动化调用。提取模式内部只做搜索链路的降级（Tavily Extract → Crawl4AI），browser-use 是独立触发的手动武器。

---

## 八、接入 Hermes Agent

创建技能文件 `~/.hermes/skills/devops/gcat-web-search/SKILL.md`：

```yaml
---
name: gcat-web-search
description: G-CAT 定制搜索+提取工具。Tavily/Crawl4AI/browser-use三层搜索+三层提取。
version: 1.0
triggers:
  - 搜索
  - 查一下
  - 搜一下
  - 提取
  - 抓取
  - 帮我搜
---

# G-CAT Web Search

搜索链路: Tavily API（主力）→ Crawl4AI（后援抓取）
浏览器操控: browser-use Agent（独立触发）

## 搜索
`web_search` 走 Tavily，自动返回结构化结果+AI摘要。

## 提取
`web_extract` 先走 Tavily Extract → 失败走 Crawl4AI Magic Mode。

## 复杂浏览器操作
业务说 "登录XX网站/填表/批量操作" → 调 `browser-search.py agent <task>`

## 清理
`browser-search.py cleanup` 清理残留 Chromium 进程（建议加 cron 每4h跑一次）。
```

配置完成后，当你说"帮我搜最新的 LLM 论文"，Hermes 自动走 Tavily；说"提取这篇文章的内容"，自动走提取链路；说"登录 GitHub 帮她找简历并截图"，走 browser-use。

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

三个工具覆盖了 AI Agent 需要的所有场景，总成本几乎为零：

| 哪用 | 工具 | 具体场景 | 成本 | 要代理？ |
|------|------|----------|------|---------|
| 搜 | Tavily | 日常搜索 + 快速提取 | 免费 1K次/月 | 不用（直连） |
| 抓 | Crawl4AI | 后援抓取 + JS渲染 + 反爬 | 0 元（自部署） | 看目标站 |
| 控 | browser-use | 浏览器自动化 + 登录 + 填表 | 豆包 ¥0.01/任务 | 看目标站 |

几点经验：
- 搜索链路里 Tavily 是绝对主力，大部分场景根本用不到后援
- browser-use 是独立武器，不要把它塞进搜索降级链里
- 外部操作前先跑 `curl -x http://127.0.0.1:8118` 确认代理活着——比事后排查省一百倍时间
- browser-use 别用 DeepSeek 当大脑——会报 400
- 任务结束记得 `browser.close()`，不然 Chromium 僵尸进程吃内存

全文代码可以直接复制跑。有什么问题或者改进建议，去 [GitHub](https://github.com/gymaira1990-jpg/catnest) 提。

---

> **作者：** G-CAT · **GitHub:** [gymaira1990-jpg/catnest](https://github.com/gymaira1990-jpg/catnest)
