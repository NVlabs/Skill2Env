---
name: ai-bot-log-audit
description: Use when analyzing server logs to understand how AI crawlers (GPTBot, ClaudeBot, PerplexityBot) interact with your site. Use when optimizing content placement for LLM retrieval, diagnosing why AI search isn't citing your content, or auditing crawl patterns to find optimization gaps.
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# AI Bot Log Audit

> Analyze server logs to understand how AI crawlers retrieve your content, then optimize placement and structure for maximum citation probability. Based on Metehan Yeşilyurt's log file analysis framework.

## When to Use This Skill

Use this skill when you need to:

- **Audit AI bot crawl patterns** on your site (what they fetch, how often, what they skip)
- **Diagnose citation gaps** — your content exists but AI search doesn't cite it
- **Optimize content placement** for LLM retrieval mechanics (lost-in-the-middle, embedding similarity)
- **Compare AI bot behavior** across different products (Google, OpenAI, Anthropic, Perplexity)
- **Build a GEO strategy** grounded in actual crawl data, not assumptions
- **Identify which pages AI bots prioritize** and which they ignore

This skill is particularly valuable for:
- SEO professionals adding AI search to their optimization scope
- Publishers monitoring AI traffic and content extraction
- Technical SEOs conducting log file analysis
- Content strategists deciding what to optimize for AI visibility

---

## Methodology Foundation

**Source Expert:** Metehan Yeşilyurt (SEO Consultant, speaker at BrightonSEO, The Search Session)

**Core Thesis:** Log file analysis reveals the real mechanics of AI search retrieval. Different AI products (AI Overviews, AI Mode, Perplexity) use fundamentally different retrieval pipelines, so optimizing for "AI search" requires understanding each product's specific crawl and retrieval behavior.

> "AI Overviews, AI Mode, and Web Guide are three completely different products with different retrieval behaviors. You can't optimize for 'AI search' as if it's one thing." — Metehan Yeşilyurt, The Search Session

**Key Insight:** The shift from traditional SEO to AI search optimization is from chasing clicks in deterministic SERPs to chasing citations in machine-generated text. Log files reveal the mechanics behind citation selection.

---

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Guides log analysis methodology | Which log data to provide |
| Identifies patterns in crawl behavior | Strategic priority of AI products |
| Recommends content placement optimizations | Content creation/modification scope |
| Maps retrieval behavior to optimization actions | Resource allocation for changes |
| Creates audit templates and checklists | Which recommendations to implement |

---

## What This Skill Does

When invoked, I will guide you through:

1. **Log Collection** — Identify and extract AI bot activity from server logs
2. **Bot Identification** — Map user agents to AI products
3. **Crawl Pattern Analysis** — Understand what AI bots fetch and ignore
4. **Retrieval Mechanics** — Learn how each AI product processes your content
5. **Optimization Actions** — Specific changes to improve AI citation probability

---

## Instructions

### Phase 1: AI Bot Identification

#### Known AI Crawlers (2026)

| Bot User Agent | Operator | Purpose | Respects robots.txt? |
|---------------|----------|---------|---------------------|
| **GPTBot** | OpenAI | Training data + ChatGPT Browse | Yes |
| **ChatGPT-User** | OpenAI | Real-time browsing in ChatGPT | Yes |
| **OAI-SearchBot** | OpenAI | SearchGPT / ChatGPT Search | Yes |
| **ClaudeBot** | Anthropic | Training data collection | Yes |
| **PerplexityBot** | Perplexity | Real-time search + answer generation | Yes (mostly) |
| **Google-Extended** | Google | Gemini/AI training (deprecated — now part of Googlebot) | N/A |
| **Googlebot** | Google | Traditional crawl + AI Overviews + AI Mode | Yes |
| **Bytespider** | ByteDance | Training for TikTok AI features | Yes |
| **CCBot** | Common Crawl | Open dataset used by many AI models | Yes |
| **Applebot-Extended** | Apple | Apple Intelligence features | Yes |

#### Log Extraction Commands

```bash
# Extract all AI bot hits from Apache/Nginx access logs
grep -iE "(GPTBot|ChatGPT-User|OAI-SearchBot|ClaudeBot|PerplexityBot|Bytespider|CCBot|Applebot-Extended)" access.log > ai_bots.log

# Count hits by bot
awk -F'"' '{print $6}' ai_bots.log | grep -oE "(GPTBot|ChatGPT-User|OAI-SearchBot|ClaudeBot|PerplexityBot|Bytespider|CCBot)" | sort | uniq -c | sort -rn

# Top pages crawled by AI bots
awk '{print $7}' ai_bots.log | sort | uniq -c | sort -rn | head -50

# Crawl frequency by day
awk '{print $4}' ai_bots.log | cut -d: -f1 | tr -d '[' | sort | uniq -c

# Response codes for AI bots (are they getting 200s or errors?)
awk '{print $9}' ai_bots.log | sort | uniq -c | sort -rn
```

---

### Phase 2: Crawl Pattern Analysis

#### What to Look For

| Pattern | What It Means | Action |
|---------|--------------|--------|
| **Bot fetches page frequently** | Page is in retrieval index, content matters | Optimize this page first |
| **Bot fetches page once then stops** | Page was evaluated and deprioritized | Improve content quality/freshness |
| **Bot never fetches a page** | Page not discovered or blocked | Check internal linking, sitemap, robots.txt |
| **Bot gets 404/500** | Technical issue blocking retrieval | Fix immediately |
| **Bot fetches but doesn't cite** | Content retrieved but not selected for answers | Improve structure, uniqueness, authority |

#### Crawl Budget Analysis

AI bots have crawl budgets like traditional bots. If your site is large:

```
QUESTIONS TO ANSWER:
1. What % of pages are being crawled by AI bots?
2. Are high-value pages being fetched?
3. Are AI bots wasting time on low-value pages (tag pages, pagination)?
4. What's the crawl frequency — daily? weekly? sporadic?
5. Do different AI bots prioritize different pages?
```

#### Comparative Bot Behavior

Map how each bot interacts with your site differently:

```
ANALYSIS TEMPLATE:

GPTBot:
  Pages fetched: ___
  Top pages: ___
  Crawl frequency: ___
  Response codes: ___

PerplexityBot:
  Pages fetched: ___
  Top pages: ___
  Crawl frequency: ___
  Response codes: ___

ClaudeBot:
  Pages fetched: ___
  Top pages: ___
  Crawl frequency: ___
  Response codes: ___
```

---

### Phase 3: Understanding Retrieval Mechanics

Each AI product uses a different retrieval pipeline. Optimizing requires understanding the mechanics.

#### Perplexity: Embedding Similarity + Source Diversification

Perplexity uses high embedding similarity to match content to queries, then actively diversifies sources.

**What this means for you:**
- Semantic match matters more than keyword match
- Being the single best source isn't enough — Perplexity diversifies
- Your content needs to be retrievable AND complementary to other sources
- Structured, extractable content wins (tables, definitions, clear claims)

#### Google AI Overviews: Search Index + LLM Layer

AI Overviews sit on top of existing Google Search rankings. Your traditional SEO signals matter.

**What this means for you:**
- If you don't rank on page 1 for traditional search, you're unlikely to appear in AI Overviews
- The AI layer selects from already-ranked pages and synthesizes
- E-E-A-T signals are inherited from search ranking

#### Google AI Mode: Multi-Step Query Fan-Out

AI Mode decomposes complex questions into sub-queries, retrieves for each, then synthesizes.

**What this means for you:**
- Content that answers sub-questions gets included
- Comprehensive topical coverage across your site matters
- Internal linking between related topics helps AI Mode stitch answers together

---

### Phase 4: LLM Vulnerability Awareness

Understanding known LLM processing weaknesses helps you position content for maximum retrieval.

#### 4 Key LLM Vulnerabilities

| Vulnerability | Description | Optimization |
|--------------|-------------|-------------|
| **Recency bias** | LLMs weight recent information higher, even when older info is more accurate | Date your content clearly. Update regularly. Recent timestamps = retrieval advantage |
| **Lost-in-the-middle** | LLMs process beginnings and endings of context better than middles | Place key claims, definitions, and statistics at the START and END of pages/sections |
| **Data poisoning susceptibility** | LLMs can be influenced by coordinated content patterns | Not actionable for you, but be aware: competitors can game AI answers |
| **Prompt injection** | LLMs can be manipulated via hidden instructions | Not actionable for SEO, but relevant for security audits |

#### Lost-in-the-Middle: Practical Content Placement

This is the most actionable vulnerability for SEO:

```
PAGE STRUCTURE FOR LLM RETRIEVAL:

TOP (HIGH ATTENTION):
├── Key definition / direct answer
├── Critical statistics with context
└── Main claim / thesis

MIDDLE (LOW ATTENTION):
├── Supporting details
├── Tables and structured data (LLMs handle these well regardless of position)
├── Examples and elaboration
└── Supporting evidence

BOTTOM (HIGH ATTENTION):
├── Summary of key points
├── FAQ with direct answers
├── Conclusion with standalone claims
└── Updated date
```

> "FAQs at the end of the page, tables in the middle — that's the lost-in-the-middle fix. LLMs handle structured data well regardless of position, but flowing text in the middle gets deprioritized." — Metehan Yeşilyurt

---

### Phase 5: Audit Report Template

#### AI Bot Log Audit Report

```markdown
# AI Bot Log Audit: [Site Name]
**Date:** [Date]
**Period analyzed:** [Date range]
**Log source:** [Apache/Nginx/CDN]

## Executive Summary
[2-3 sentence overview of findings]

## Bot Activity Overview

| Bot | Total Hits | Unique Pages | Avg Daily Hits | Status |
|-----|-----------|-------------|----------------|--------|
| GPTBot | ___ | ___ | ___ | Active/Inactive |
| PerplexityBot | ___ | ___ | ___ | Active/Inactive |
| ClaudeBot | ___ | ___ | ___ | Active/Inactive |
| ChatGPT-User | ___ | ___ | ___ | Active/Inactive |

## Top Pages by AI Bot Activity
1. [URL] — [hits] hits — [which bots]
2. [URL] — [hits] hits — [which bots]
3. [URL] — [hits] hits — [which bots]

## Pages Not Crawled (Expected High-Value)
- [URL] — Likely cause: [blocked/not linked/low authority]
- [URL] — Likely cause: [___]

## Technical Issues
- [N] pages returning 404 to AI bots
- [N] pages returning 500 to AI bots
- robots.txt blocking: [yes/no — which bots?]

## Content Optimization Recommendations

### Priority 1: Fix Technical Issues
- [ ] [Specific fix]

### Priority 2: Optimize High-Traffic AI Pages
- [ ] Apply lost-in-the-middle structure to [page]
- [ ] Add entity schema to [page]
- [ ] Update freshness signals on [page]

### Priority 3: Improve Discoverability
- [ ] Internal link to [uncrawled page] from [crawled hub]
- [ ] Add to sitemap: [page]
- [ ] Create content for [gap topic]

## robots.txt Recommendations
[Current AI bot directives and recommended changes]
```

---

## Examples

### Example 1: Publisher Losing AI Traffic

**Context:** News publisher noticed declining traffic from AI referrals. Log audit reveals:

**Findings:**
- GPTBot hits dropped 60% after robots.txt change (accidentally blocked)
- PerplexityBot only crawling homepage and top 5 articles
- Most content pages have zero AI bot visits
- AI bots hitting 404s on URL structure that changed 3 months ago

**Actions:**
1. Fix robots.txt — allow GPTBot and PerplexityBot
2. Add 301 redirects for old URL structure
3. Improve internal linking from high-crawl pages to deep content
4. Add article schema with datePublished and dateModified
5. Restructure top articles with lost-in-the-middle optimization

### Example 2: SaaS Blog Not Getting AI Citations

**Context:** SaaS company publishes weekly blog but never appears in ChatGPT or Perplexity answers.

**Findings:**
- ClaudeBot and GPTBot crawl regularly (technical access is fine)
- Content is generic ("10 Tips for..." format) — interchangeable with competitors
- No original data, case studies, or unique insights
- Author pages have no Person schema
- Brand search volume: 100/month (competitors: 3,000+)

**Actions:**
1. Content strategy shift: original research > generic guides
2. Add Person schema for all authors with credentials
3. Place unique data/claims at start and end of articles (lost-in-the-middle)
4. Build entity authority for 2 key authors (podcast appearances, guest posts)
5. Create comparison content where their product is one of the compared options

---

## Checklists & Templates

### Quick Audit Checklist

```
ACCESS CHECK
[ ] AI bots not blocked in robots.txt (check each bot separately)
[ ] AI bots getting 200 responses (not 403/404/500)
[ ] Sitemap accessible and up to date
[ ] Key pages present in sitemap

CRAWL PATTERNS
[ ] High-value pages are being crawled by AI bots
[ ] Crawl frequency is consistent (not declining)
[ ] AI bots not wasting budget on low-value pages
[ ] Multiple AI bots active (not just one)

CONTENT OPTIMIZATION
[ ] Key claims at beginning and end of pages (not buried in middle)
[ ] Tables and structured data for comparisons
[ ] FAQ sections at bottom of major pages
[ ] Content is updated with recent dates
[ ] Unique data or original insights present

ENTITY SIGNALS
[ ] Author/organization schema on relevant pages
[ ] Entity mentioned consistently across the site
[ ] Cross-platform entity presence established
```

---

## Skill Boundaries

### What This Skill Does Well
- Guiding server log analysis for AI bot patterns
- Explaining retrieval mechanics for different AI products
- Recommending content placement optimizations
- Creating structured audit reports

### What This Skill Cannot Do
- Access or parse your actual server logs
- Query live AI search results
- Guarantee citation in AI responses
- Replace technical SEO expertise for complex log analysis

---

## References

**Primary Sources:**
- Metehan Yeşilyurt — "Log Files, AI Bots, and the Real Mechanics of AI Search" (The Search Session, Advanced Web Ranking)
- Mark Williams-Cook — Signal decay thesis and query fan-out analysis
- Lily Ray — Entity-first framework and cross-platform authority

**Tools Referenced:**
- Screaming Frog Log File Analyzer
- GoAccess (open-source log analyzer)
- queryfan.com (query fan-out analysis)

**Technical References:**
- OpenAI GPTBot documentation
- Anthropic ClaudeBot documentation
- Google Search Central — Googlebot and AI features

---

## Related Skills

- **llm-optimized-content** — Content optimization for AI search (GEO)
- **entity-seo-playbook** — Building entity authority for AI visibility
- **lighthouse-audit** — Technical SEO and performance audit
- **seo-content-writer** — SEO content creation with E-E-A-T
- **schema-markup** — Structured data implementation

---

## Skill Metadata

```yaml
name: ai-bot-log-audit
category: seo-tools
subcategory: geo
version: 1.0.0
author: GUIA
source_expert: Metehan Yeşilyurt (SEO Consultant, BrightonSEO speaker) — The Search Session podcast
difficulty: intermediate
mode: centaur
tags: [ai-bots, log-analysis, geo, ai-search, crawl-audit, perplexity, gptbot, claudebot, retrieval, lost-in-the-middle]
created: 2026-02-10
updated: 2026-02-10
```
