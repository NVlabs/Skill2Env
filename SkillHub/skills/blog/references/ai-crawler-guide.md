# Technical AI Visibility: Crawler Access & Rendering

## Contents

- [robots.txt Template for AI Crawlers](#robotstxt-template-for-ai-crawlers)
- [Cloudflare AI Crawl Control: CRITICAL](#cloudflare-ai-crawl-control----critical)
- [llms.txt Implementation](#llmstxt-implementation)
- [Server-Side Rendering Requirements](#server-side-rendering-requirements)
- [Performance Requirements](#performance-requirements)
- [Testing AI Crawler Visibility](#testing-ai-crawler-visibility)
- [AI Crawler Traffic Growth](#ai-crawler-traffic-growth)
- [AI Crawler Checklist](#ai-crawler-checklist)

## robots.txt Template for AI Crawlers

Allow all known AI crawlers explicitly. Most AI crawlers default to respecting
robots.txt, so an absent rule may mean blocked depending on the platform's
default behavior.

```
# ===========================================
# AI Search & LLM Crawlers: Explicitly Allow
# ===========================================

# OpenAI
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

# Anthropic (three-bot framework)
User-agent: ClaudeBot
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: Claude-User
Allow: /

# Deprecated Anthropic strings (kept for legacy compatibility):
# User-agent: Claude-Web
# User-agent: anthropic-ai

# Google AI (training & AI Overviews)
User-agent: Google-Extended
Allow: /

# Perplexity
User-agent: PerplexityBot
Allow: /

User-agent: Perplexity-User
Allow: /

# Meta
User-agent: Meta-ExternalAgent
Allow: /

# ByteDance
User-agent: Bytespider
Allow: /

# Google AI agents (Project Mariner)
User-agent: Google-Agent
Allow: /

# DuckDuckGo AI
User-agent: DuckAssistBot
Allow: /

# Apple (Siri, Apple Intelligence)
User-agent: Applebot-Extended
Allow: /

# Amazon (Alexa, product search)
User-agent: Amazonbot
Allow: /

# You.com
User-agent: YouBot
Allow: /

# Phind (developer search)
User-agent: PhindBot
Allow: /

# Exa (AI-native search engine)
User-agent: ExaBot
Allow: /

# Common Crawl (used by many AI models)
User-agent: CCBot
Allow: /

# ===========================================
# Traditional Search Engines
# ===========================================

User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: *
Allow: /

# ===========================================
# Sitemap
# ===========================================
Sitemap: https://example.com/sitemap.xml
```

### Crawler Identification Reference

Each provider now operates a **three-bot framework**: training bot, search/indexing bot, and
retrieval bot. Blocking the search/indexing bot means your content won't appear in that AI
platform's answers. Retrieval bots (user-triggered) may not fully respect robots.txt.

| Crawler | Operator | Type | Respects robots.txt |
|---------|----------|------|---------------------|
| GPTBot | OpenAI | Training | Yes |
| OAI-SearchBot | OpenAI | Search indexing | Yes |
| ChatGPT-User | OpenAI | User retrieval | Yes |
| ClaudeBot | Anthropic | Training | Yes |
| Claude-SearchBot | Anthropic | Search indexing | Yes |
| Claude-User | Anthropic | User retrieval | Yes |
| ~~Claude-Web~~ | Anthropic | Deprecated | - |
| ~~anthropic-ai~~ | Anthropic | Deprecated | - |
| Google-Extended | Google | AI/Gemini training | Yes |
| Google-Agent | Google | Project Mariner agentic (2026) | Yes |
| PerplexityBot | Perplexity | Search indexing | Yes |
| Perplexity-User | Perplexity | User retrieval | Partial |
| Applebot-Extended | Apple | Apple Intelligence training | Yes |
| Meta-ExternalAgent | Meta | High-volume data collection | Yes |
| Bytespider | ByteDance | Training/indexing | Partial (documented issues) |
| Amazonbot | Amazon | Alexa / product search | Yes |
| DuckAssistBot | DuckDuckGo | DuckAssist AI answers | Yes |
| YouBot | You.com | AI search engine | Yes |
| PhindBot | Phind | Developer-focused AI search | Yes |
| ExaBot | Exa | Neural search engine | Yes |
| CCBot | Common Crawl | Open dataset (used by many LLMs) | Yes |

### robots.txt Strategy by Bot Type

Treat each bot category differently based on your goals:
- **Training bots** (GPTBot, ClaudeBot, CCBot): Your choice. Blocking has no direct search
  visibility impact, but affects whether your content influences future model training.
- **Search/indexing bots** (OAI-SearchBot, Claude-SearchBot, PerplexityBot): **Allow these.**
  Blocking means your content won't appear in ChatGPT, Claude, or Perplexity answers.
- **Retrieval bots** (ChatGPT-User, Perplexity-User): May not fully respect robots.txt. These
  are triggered by live user queries and may fetch content regardless of directives.

---

## Cloudflare AI Crawl Control: CRITICAL

**Since July 2025, Cloudflare blocks AI crawlers by default on new domains.**
This is the single most common reason blogs are invisible to AI systems despite
having correct robots.txt configuration.

### How to Fix

1. Log in to Cloudflare dashboard
2. Navigate to **Security > Bots > AI Crawlers**
3. Review the list of AI crawlers
4. **Toggle "Allow" for each AI crawler you want to permit**
5. Save changes

### What Cloudflare Blocks by Default

| Crawler | Default Status (New Domains) |
|---------|------------------------------|
| GPTBot | Blocked |
| ClaudeBot | Blocked |
| PerplexityBot | Blocked |
| CCBot | Blocked |
| Google-Extended | Blocked |
| Applebot-Extended | Allowed |
| Googlebot | Allowed (not an AI crawler) |

### Verification

After updating Cloudflare settings, verify access:

```bash
# Simulate GPTBot user-agent
curl -s -A "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; GPTBot/1.0; +https://openai.com/gptbot)" https://yourdomain.com/blog/test-post | head -50

# Check for Cloudflare block page (403 or challenge page)
curl -s -o /dev/null -w "%{http_code}" -A "Mozilla/5.0 (compatible; ClaudeBot/1.0)" https://yourdomain.com/
```

If you get a 403 or an HTML page with "Cloudflare" in it, the crawler is blocked.

---

## llms.txt Implementation

The `llms.txt` standard (proposed by llmstxt.org, Sep 2024) provides a machine-readable
summary of your site for LLMs. Place at site root: `https://example.com/llms.txt`.

**Important caveat:** No major AI platform has confirmed reading llms.txt. Google's Gary Illyes
stated Google doesn't support it (Jul 2025). Semrush testing showed zero AI crawler visits to
llms.txt files across 9 test sites. It is low-cost to implement but benefits are currently
unproven. Implement it - but don't rely on it as a visibility strategy.

### Specification

- Plain text file, UTF-8
- Under 10KB total
- Structured list of important URLs with brief descriptions
- Helps LLMs understand site structure and find authoritative content

### Template

```
# Example Blog

> A blog about modern web development, SEO, and content strategy.

## Main Pages

- [Home](https://example.com/): Main landing page with latest articles
- [About](https://example.com/about): Company information and mission
- [Blog](https://example.com/blog): All published articles

## Popular Articles

- [Complete Guide to Technical SEO in 2026](https://example.com/blog/technical-seo-guide): Comprehensive technical SEO guide covering Core Web Vitals, crawlability, and schema markup.
- [How AI Overviews Changed Search](https://example.com/blog/ai-overviews-impact): Data-driven analysis of AI Overview impact on organic traffic with case studies.
- [Content Strategy for B2B SaaS](https://example.com/blog/b2b-saas-content-strategy): Framework for building a content program that drives pipeline.

## Topic Clusters

- [SEO](https://example.com/topics/seo): All articles about search engine optimization
- [Content Strategy](https://example.com/topics/content-strategy): Content planning and execution
- [Web Development](https://example.com/topics/web-development): Frontend and backend development guides

## Authors

- [Sarah Chen](https://example.com/author/sarah-chen): Content strategist, B2B SaaS specialist
- [Marcus Rivera](https://example.com/author/marcus-rivera): Senior frontend engineer, React expert
```

### Key Rules

- Do not exceed 10KB (LLMs may truncate or ignore larger files)
- Use markdown-style links: `[Title](URL): Description`
- Include only your most important and highest-quality pages
- Update when you publish significant new content
- This is NOT a sitemap replacement: it supplements sitemap.xml

---

## Server-Side Rendering Requirements

AI crawlers do NOT execute JavaScript. Content rendered only via client-side
JavaScript is invisible to all AI systems except Googlebot and AppleBot.

### Rendering Strategy Ranking

| Strategy | AI Visibility | Performance | Recommendation |
|----------|--------------|-------------|----------------|
| **SSG** (Static Site Generation) | Best | Best | Preferred for blogs |
| **SSR** (Server-Side Rendering) | Excellent | Good | Good for dynamic content |
| **ISR** (Incremental Static Regeneration) | Excellent | Good | Good for large sites |
| **CSR** (Client-Side Rendering) | None | Poor for crawlers | Never use for content |

### JavaScript Execution by Crawler

| Crawler | Executes JavaScript | Renders Pages |
|---------|-------------------|---------------|
| GPTBot | No | No |
| OAI-SearchBot | No | No |
| ChatGPT-User | No | No |
| ClaudeBot | No | No |
| Claude-SearchBot | No | No |
| Claude-User | No | No |
| PerplexityBot | No | No |
| Perplexity-User | No | No |
| Meta-ExternalAgent | No | No |
| Bytespider | No | No |
| Amazonbot | No | No |
| CCBot | No | No |
| **Googlebot** | **Yes** | **Yes** |
| **AppleBot** | **Yes** | **Yes** |
| **ChatGPT Operator** (agentic) | **Yes** | **Yes** |
| **Google-Agent** (agentic) | **Yes** | **Yes** |

### Vercel Findings

Vercel analyzed 500M+ GPTBot fetches and found **zero evidence of JavaScript
execution**. GPTBot reads raw HTML only. Content loaded via React hydration,
Vue mounting, or any client-side framework is completely invisible.

### Exception: Agentic Tools

Standard AI crawlers do not execute JavaScript. However, **agentic tools** are different:
- **ChatGPT Operator** (OpenAI): Full JS rendering with computer vision capabilities.
- **Google-Agent / Project Mariner** (Google, 2026): Operates through Chrome with full rendering.

These are user-directed agents, not automated crawlers. They can see JS-rendered content,
but they do not replace the need for SSR - standard crawlers still dominate citation indexing.

---

## Performance Requirements

AI retrieval systems have strict latency budgets. Slow sites are excluded from
candidate answer pools before content quality is even evaluated.

**Note:** The thresholds below are industry best practices and observations from SEO tooling
(Discovered Labs, Prerender.io, Kevin Indig). They are NOT officially published specifications
from OpenAI, Anthropic, or Perplexity. Treat as directional targets, not guaranteed cutoffs.

### Thresholds

| Metric | Target | Hard Limit | Consequence |
|--------|--------|------------|-------------|
| TTFB (Time to First Byte) | < 200ms | < 600ms | Excluded from candidate pools |
| Full page load (HTML) | < 500ms | < 1,000ms | Reduced crawl frequency |
| Response size (HTML) | < 200KB | < 500KB | Partial content extraction |

### Optimization Priorities

1. **Use a CDN**: Content must be served from edge locations
2. **Enable compression**: gzip or Brotli for all text responses
3. **Minimize HTML bloat**: Remove unused CSS/JS from HTML response
4. **Cache aggressively**: Static pages should have long cache headers
5. **Pre-render**: Use SSG or SSR, never CSR for content pages

---

## Testing AI Crawler Visibility

### Quick Test: See What AI Crawlers See

```bash
# Basic: view raw HTML (what all AI crawlers receive)
curl -s https://yourdomain.com/blog/your-post | head -200

# Check if main content is in HTML source
curl -s https://yourdomain.com/blog/your-post | grep -c "<article"

# Check for JS-only rendering indicators
curl -s https://yourdomain.com/blog/your-post | grep -c "id=\"__next\""
curl -s https://yourdomain.com/blog/your-post | grep -c "id=\"root\""
curl -s https://yourdomain.com/blog/your-post | grep -c "id=\"app\""

# If the above returns content in a <noscript> tag or empty divs,
# your content is behind JS and invisible to AI crawlers.
```

### Full Crawler Simulation

```bash
# Simulate GPTBot
curl -s -H "User-Agent: Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; GPTBot/1.0; +https://openai.com/gptbot)" \
  https://yourdomain.com/blog/your-post > /tmp/gptbot-view.html

# Simulate ClaudeBot
curl -s -H "User-Agent: Mozilla/5.0 (compatible; ClaudeBot/1.0; +https://claudebot.ai)" \
  https://yourdomain.com/blog/your-post > /tmp/claudebot-view.html

# Check if content exists
wc -l /tmp/gptbot-view.html
grep -c "your-expected-heading-text" /tmp/gptbot-view.html
```

### Red Flags (Content Invisible to AI)

| Indicator | What It Means |
|-----------|---------------|
| Empty `<div id="root"></div>` | React CSR: content loads via JS only |
| Empty `<div id="__next"></div>` without SSR | Next.js without getServerSideProps/getStaticProps |
| `<noscript>` contains the content | Content explicitly hidden from non-JS clients |
| `<script>` tags contain all content as JSON | Data fetched client-side, not in HTML |
| HTML under 5KB for a full blog post | Content not rendered server-side |

---

## AI Crawler Traffic Growth

Traffic from AI crawlers is growing exponentially. Sites that block or fail
to serve these crawlers are losing compounding visibility.

| Metric | Value | Source |
|--------|-------|--------|
| GPTBot traffic growth | +305% YoY | Cloudflare Radar, 2025 |
| PerplexityBot traffic growth | +157,490% YoY | Cloudflare Radar, 2025 |
| AI crawling volume overall | +32% YoY | Cloudflare, 2025 |
| Top 10 domains' citation share | 46% of all ChatGPT citations per topic | Growth Memo, Mar 2026 |
| AI referral traffic share | 1.08% of all web traffic | Similarweb, May 2025 |
| AI referral traffic growth | +527% Jan-May 2025 | Similarweb, 2025 |

---

## AI Crawler Checklist

| Check | Pass | Fail |
|-------|------|------|
| robots.txt allows AI crawlers | All major bots listed with `Allow: /` | Missing entries or `Disallow: /` |
| Cloudflare AI settings reviewed | AI crawlers explicitly allowed in dashboard | Default block left in place |
| llms.txt present at site root | Under 10KB, lists key URLs | Missing or over 10KB |
| Content in HTML source | `curl` returns full content | Empty divs, JS-only rendering |
| TTFB under 200ms | Measured from CDN edge | Over 600ms = excluded |
| Schema in HTML source | JSON-LD in `<head>` or `<body>` | Schema injected via JS |
| Sitemap.xml accessible | Valid XML, all blog URLs included | Missing or returns 404 |
| No Cloudflare challenge on bot UA | 200 status code | 403 or challenge page |
