---
name: keyword-deep-dive
description: Use when planning to rank for a specific keyword. The agent Googles it, reads the top 10, classifies intent, reads the top 3 competitor pages, and produces a 90-day ranking plan with intent, SERP analysis, and content recommendations.
---

# Keyword Deep Dive

A complete picture of a single keyword's opportunity — intent, competition, what it takes to rank, and a specific 90-day plan. The agent does all the research itself. No keyword tool required.

## Input

**Target keyword** (required). Optionally: a URL if you already have a page targeting this keyword.

If the user didn't provide a keyword, ask for it before proceeding.

## Role

You are a senior SEO strategist specializing in keyword intelligence and SERP analysis.

## Step 1: Research the SERP

Google the target keyword. Read the top 10 results in detail, the top 3 in full.

Note for each top 3:
- Domain (note authority proxies: is it a known brand? Specialist vs generalist?)
- Content format (guide / comparison / listicle / tool / video / product page)
- Approximate word count
- Unique angle or hook
- Freshness signals (publish date, last updated)
- E-E-A-T signals present

## Step 2: Classify Intent

Classify dominant intent: **Informational / Commercial Investigation / Transactional / Navigational**.

**Zero-click risk assessment:**
- Informational queries: roughly 60% of searches end without a click ([Digital Bloom 2026 organic traffic report](https://thedigitalbloom.com/learn/organic-traffic-crisis-report-2026-update/)); mobile zero-click behavior reaches 77%
- Featured snippet present: 42.9% CTR if we hold it, near-zero if we don't ([First Page Sage 2026](https://firstpagesage.com/reports/google-click-through-rates-ctrs-by-ranking-position/))
- AI Overview present: organic CTR drops 58-61% for the top-ranking page ([Ahrefs Dec 2025](https://ahrefs.com/blog/ai-overviews-reduce-clicks-update/) / [Seer Interactive](https://www.seerinteractive.com/insights/aio-impact-on-google-ctr-september-2025-update)); brands cited in the AI Overview earn 35% more clicks
- Flag clearly if the keyword has structurally low click-through potential

## Step 3: Assess SERP Features

What SERP features are active?
- Featured snippet (what format — paragraph, list, table? Who holds it?)
- People Also Ask (how many questions? What are they?)
- AI Overview
- Image pack / video carousel
- Local pack
- Site links
- Knowledge panel

## Step 4: SERP Volatility Signal

Can you tell if the SERP is stable or turbulent?
- If top results look freshly updated / have "Updated YYYY" in the title → moderate volatility
- If multiple top results are from different years (2021, 2024, 2026) → stable
- If results are all dated past 6 months with news angles → turbulent
- If you can't tell → say so, don't fabricate

## Step 5: Competitive Read of Top 3

Fetch and read the top 3 pages. For each:
- Key sections they cover
- Word count
- Internal linking patterns (what they link to)
- What they cover that others don't
- What they do that's genuinely hard to replicate (original data? First-party screenshots? Proprietary frameworks?)

## Step 6: Output

### Keyword Profile
- Keyword | Apparent search intent | Estimated difficulty (Easy / Moderate / Hard based on SERP competition, not a KD score)
- SERP features present and their CTR impact
- Zero-click risk: Low / Medium / High

### Competitive Read
For each of the top 3 competitors:
- URL | Domain authority proxy | Format | Words (approx) | Unique angle | What they do best

### Content Gaps (what's missing from top results)
Specific subtopics or angles that top-ranking pages don't cover well. These are where a new entrant can differentiate.

### Ranking Strategy

**If the user has no existing page for this keyword:**

**Quick assessment:**
- Is this keyword worth pursuing? (Intent match to business? Traffic potential? Zero-click risk?)
- Realistic timeline: Easy (3-6 months) / Moderate (6-12 months) / Hard (12-24 months authority play)

**Content requirements:**
- Content type to build (matches SERP)
- Word count target (average of top 5 + 10%)
- Sections that MUST be covered (from competitive read)
- Unique angle this page should take (from gap analysis)
- E-E-A-T signals required

**If the user already has a page ranking:**

**Position diagnosis:**
- Current position apparent from Google? (If not in top 100, note this)
- Compared to the top 3, what's missing? Specific content depth? Word count? Intent alignment?

**Optimization plan:**
- Quick wins (title/meta rewrite for CTR, add missing section, fix intent mismatch)
- 30-day content plan (sections to add, depth to deepen)
- Supporting cluster pages to create for internal linking

### Title Tag & Meta Rewrites

Propose 2 title tag options (max 60 chars) and 1 meta description (max 160 chars). Each with reasoning.

### Ranking Timeline Estimate

- Current position (or "unranked"): [X]
- Realistic 90-day target: [Y]
- Effort: Low (CTR fix) / Medium (content update) / High (new content + internal links)

## What to Ignore

- **KD scores alone** — meaningless without reading the actual SERP. Use the read above instead.
- **High volume, zero-click keywords** — impressions without clicks aren't worth the effort unless you need brand exposure
- **Fighting Wikipedia, Reddit, or news aggregators** for positions 1-3 — different content types, unwinnable

## Next Step

Need a full content brief to execute the ranking plan? Use `content-brief` with this keyword as context.

## Bundled references

Load from `references/` only when the step calls for them.

- **`ctr-benchmarks-by-position.md`** — the full 2026 position → CTR curve with AI-Overview-adjusted numbers (Step 2, when estimating traffic potential)
- **`zero-click-and-aio-impact.md`** — how AI Overviews, featured snippets, and zero-click SERPs change the ranking math (Step 2, for the zero-click risk line)
- **`serp-features-recognition.md`** — checklist for detecting every SERP feature visually (Step 3, if uncertain which features are active)
- **`serp-volatility-heuristics.md`** — how to read SERP volatility without access to a rank tracker (Step 4, when volatility is ambiguous)
- **`difficulty-from-serp-signals.md`** — how to estimate KD from reading the top 10 instead of a tool score (Step 5, when classifying Easy/Moderate/Hard)
- **`intent-matching.md`** — the full Informational / Commercial / Transactional / Navigational decision framework (Step 2, when intent is mixed)
