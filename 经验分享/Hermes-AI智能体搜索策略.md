# Hermes AI 智能体：个人级搜索策略、工具与玩法实战

> **副标题：** Tavily + Crawl4AI + browser-use — 三层降级，零成本打造 AI Agent 专属搜索体系
>
> **作者：** G-CAT | **日期：** 2026-06-27
>
> **适用环境：** Hermes Agent + WSL/Linux | **依赖：** Python ≥3.11

---

## 一、架构总览：三层降级

核心理念：策略 1 失败自动走策略 2，再失败走策略 3。没有单点依赖。

```
搜索链路:
  Tavily API → Crawl4AI + 豆包 → browser-use
  (最快)       (0成本无限量)       (真实浏览器, 最后手段)

提取链路:
  Tavily Extract → Crawl4AI Playwright → browser-use Agent
  (最干净)         (Magic Mode反爬)      (AI视觉驱动)
```

### 三个工具定位

| 工具 | 角色 | 核心能力 | 适合场景 |
|------|------|---------|---------|
| **Tavily** | 主力搜索 | AI 摘要 + 结构化结果 | 日常搜索、快速提取 |
| **Crawl4AI** | 专业抓取 | 本地爬取、LLM 提炼、批量 | 复杂页面、大量抓取 |
| **browser-use** | AI 操作 | 视觉识别、鼠标模拟、登录态 | 登录操作、多步骤任务 |

---

## 二、工具安装与配置

### 2.1 Tavily API

Tavily 提供 1,000 次/月的免费额度，搜索质量高、AI 摘要自动生成。

```bash
# 注册获取 API Key: https://tavily.com
# 配置到 Hermes
echo "TAVILY_API_KEY=tvly-..." >> ~/.hermes/.env

# 配置 Hermes 使用 Tavily
hermes config set web.search_backend tavily
hermes config set web.extract_backend tavily
```

搜索效果：中英文均支持，自动生成 AI 摘要和结构化结果（标题、URL、摘要、评分）。

### 2.2 browser-use — AI 驱动浏览器操作

browser-use 是一个开源的浏览器 Agent 框架（85K+ Stars），支持视觉识别、鼠标模拟、人类暂停。

```bash
# 安装
pip install browser-use[core]

# 确保系统已安装 Chromium
# Linux: sudo apt install chromium-browser
# 或 snap: snap install chromium
```

**基础配置：**

```python
from browser_use import Browser

browser = Browser(
    executable_path="/usr/bin/chromium-browser",  # Chromium 路径
    headless=False,                                # 有头模式，方便观察
    args=["--no-sandbox"],
    proxy={"server": "http://127.0.0.1:8118"},    # 如需代理
)
```

**使用真实浏览器 profile（保留登录态）：**

```python
browser = Browser(
    user_data_dir="~/.config/chromium",           # 你的 Chromium profile 路径
    profile_directory="Default",
    headless=False,
)

# 启动后即可使用已登录的 Google/GitHub 等
await browser.start()
await browser.navigate_to("https://github.com")
```

**Agent 模式（AI 驱动操作）：**

```python
from browser_use import Agent, Browser
from browser_use.llm.openai.chat import ChatOpenAI

llm = ChatOpenAI(
    model="your-model",
    api_key="your-api-key",
    base_url="https://api.openai.com/v1",
)

agent = Agent(
    task="打开 GitHub 搜索 browser-use 项目，查看 Star 数",
    llm=llm,
    browser=browser,
    use_vision=True,  # 启用视觉识别
)
await agent.run()
```

### 2.3 Crawl4AI — 专业内容抓取

Crawl4AI 是一个开源的 LLM 友好型爬虫，输出干净 Markdown，支持 Magic Mode 反爬。

```bash
# 安装
pip install crawl4ai

# 安装系统依赖
sudo apt install -y libxml2-dev libxslt-dev

# 安装 Playwright 浏览器
playwright install chromium
```

**基础使用：**

```python
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig

async with AsyncWebCrawler() as crawler:
    result = await crawler.arun(
        url="https://example.com/article",
        config=CrawlerRunConfig(
            magic=True,           # 反爬模式
            word_count_threshold=15,
            remove_overlay_elements=True,
        )
    )
    print(result.markdown)  # 干净的 Markdown 格式
```

**配合 LLM 智能提取：**

```python
from crawl4ai import LLMConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy

llm_strategy = LLMExtractionStrategy(
    llm_config=LLMConfig(
        provider="openai/your-model",
        api_token="your-api-key",
    ),
    instruction="提取正文内容，去掉导航、广告、评论",
    chunk_token_threshold=2000,
)

config = CrawlerRunConfig(
    extraction_strategy=llm_strategy,
    magic=True,
)
```

**批量并行抓取：**

```python
urls = ["https://site1.com", "https://site2.com", "https://site3.com"]
async with AsyncWebCrawler(max_pages=3) as crawler:
    results = await crawler.arun_many(urls, config=config)
    for r in results:
        print(len(r.markdown))
```

### 2.4 豆包模型配置（可选，降低费用）

豆包（火山引擎）支持 OpenAI 兼容 API，且 `doubao-seed-2-0-mini` 极其便宜：

```python
from browser_use.llm.openai.chat import ChatOpenAI

llm = ChatOpenAI(
    model="doubao-seed-2-0-mini-260215",
    api_key="your-ark-api-key",
    base_url="https://ark.cn-beijing.volces.com/api/v3",
)
```

豆包 Mini 比 Lite 省约 26% token，支持 structured output（browser-use Agent 运行正常）。

---

## 三、代理配置（可选）

如果你的环境需要代理访问 Google 等网站，推荐使用 Privoxy 作为 HTTP 代理层：

```
浏览器 → Privoxy (:8118) → SOCKS5 隧道 → 境外服务器
                           ↓
                  国内网站直连 (自动分流)
```

Privoxy 配置示例（`/etc/privoxy/config`）：

```
forward-socks5 / 127.0.0.1:1080 .   # SOCKS5 隧道
# Privoxy 默认监听 127.0.0.1:8118
```

浏览器配置代理：

```python
proxy={"server": "http://127.0.0.1:8118"}
```

---

## 四、集成脚本

将以上三个工具整合为一个脚本，实现自动降级调用。

```bash
~/.hermes/scripts/browser-search.py
```

**搜索模式：**

```bash
# 自动模式（推荐，Tavily 主力）
python3 browser-search.py search "大语言模型 2026" --yes

# 指定搜索引擎
python3 browser-search.py search "AI Agent" --engine google --yes
python3 browser-search.py search "深度学习" --engine baidu --yes
```

**提取模式：**

```bash
# 自动选择最优策略（Tavily → Crawl4AI → browser-use Agent）
python3 browser-search.py extract "https://example.com/article" --yes
```

**Agent 模式：**

```bash
# AI 驱动的复杂浏览器操作
python3 browser-search.py agent "在知乎搜索 AI Agent 框架并对比"
```

**进程清理：**

```bash
python3 browser-search.py cleanup
```

关键技术点：
- 三层降级由策略 1→2→3 顺序尝试，首个成功即返回
- `--yes` 参数跳过交互确认，适合自动化场景
- 搜索模式输出结构化结果（标题 + URL + 摘要）
- 提取模式优先用 Tavily API（最快最干净），失败才走浏览器

---

## 五、接入 Hermes

创建技能文件 `~/.hermes/skills/devops/gcat-web-search/SKILL.md`，Hermes 即可根据关键词自动调用。

技能触发条件：当用户说"搜索""提取""查一下"时，Hermes 会自动选择对应模式。

搜索：Hermes 直接调用 `web_search` 工具（Tavily 后端），快速返回。
提取：调用 `browser-search.py extract`。
复杂操作：调用 `browser-search.py agent`。

---

## 六、踩坑与建议

**1. 浏览器版本匹配**

确保 Playwright 下载的 Chromium 版本与 Crawl4AI 期望的版本一致。如不一致，创建软链接：

```bash
ln -sf ~/.cache/ms-playwright/chromium-1228 ~/.cache/ms-playwright/chromium-1223
```

**2. 代理超时**

Crawl4AI 默认会下载浏览器扩展（如 uBlock Origin），GFW 环境下可能超时。关闭它：

```python
BrowserConfig(enable_default_extensions=False)
```

**3. Agent 与 LLM 兼容性**

browser-use Agent 内部使用 `response_format: json_object`，确保所选 LLM 支持该参数。如 DeepSeek 不支持，可用 OpenAI/豆包/Anthropic 替代。

**4. 进程残留**

浏览器操作后检查残留进程。browser-use Agent 退出时应确保 `browser.close()` 被调用。

---

## 七、总结

用三个开源工具覆盖所有搜索需求：

| 层级 | 工具 | 成本 |
|------|------|------|
| 搜 | Tavily | 免费 1K 次/月 |
| 抓 | Crawl4AI | 0 元（自部署） |
| 控 | browser-use | 豆包 token（极便宜） |

全文代码可直接复制运行。欢迎在 GitHub 上交流改进。

---

> **作者：** G-CAT · **GitHub:** [gymaira1990-jpg/catnest](https://github.com/gymaira1990-jpg/catnest)
