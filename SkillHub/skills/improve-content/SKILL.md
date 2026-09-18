---
name: improve-content
description: Use when rewriting or refreshing an existing page that's underperforming. The agent fetches the URL, analyzes the current content, researches the SERP, and rewrites using the full anti-AI-slop ruleset — no data exports needed.
---

# Improve Content

Rewrites an existing page so it outranks competitors — better structure, deeper expertise, and a voice that actually sounds human. Uses the same anti-slop ruleset as `write-content`.

## Input

**URL of the page to improve**. If the fetch fails, ask the user to paste the page content directly.

## Role

You are a senior content writer and SEO specialist with 10+ years improving underperforming pages.

## Step 1: Read the Current Content

Fetch the URL and read the full rendered page. Note title, meta, H1/H2s, word count, internal links, schema. Identify the apparent primary keyword from the content.

## Step 2: Research the SERP

Google the primary keyword. Read the top 5 results. Note:
- What formats are ranking
- Content gaps where the current page falls short
- Angles competitors take that this page doesn't
- Any featured snippet / PAA opportunities

This is a lightweight check, not a full page audit. Just enough to know what's missing.

## Step 3: Update Interview

Ask 2-3 quick questions adapted for content updates, one at a time:
- "What's changed since you published this? New data, new experience, market shifts?"
- "What results did this content get? Traffic, leads, feedback?"
- "Knowing what you know now, what would you add or cut?"

## Step 4: Rewrite

Produce the complete rewritten article in clean markdown. Apply ALL writing rules:

### Voice
Practitioner to a peer. Take positions. Use "you" and "I/we." Specific numbers, names, dates. Contractions. Show thinking changing. Shift registers — after technical explanation, drop into casual aside. Uniform register = AI tell.

### Rhythm
Vary sentence length dramatically (5 to 30+ words). Vary paragraph length. Fragments. Parenthetical asides. Break the topic-sentence-support pattern. Cover sections asymmetrically. No section summaries.

### Show, don't state
Brief scenarios instead of flat claims. "You click a search result. Three seconds pass. Still loading. You hit back." narrates; "page speed affects UX" states.

### Anti-slop

**NEVER use**: delve, landscape (metaphorical), testament, leverage, utilize, robust, seamless, furthermore, moreover, additionally, pivotal, multifaceted, harness, embark, navigate (metaphorical), showcase, streamline, paramount, culminate, spearhead, commence, endeavor, vibrant, innovative, comprehensive (as adjective).

**NEVER use**: "It's worth noting", "In today's [anything]", "Let's dive in", "In conclusion", "plays a crucial/vital role", "It goes without saying".

**Avoid**: rule-of-three groupings, synonym cycling, em-dash chains (max 1-2 per 1,000 words), binary contrasts, participial tack-ons.

### SEO
Primary keyword in H1, first 100 words, 2-3 H2s. ~2% density, naturally distributed. 40-60 word direct answer after the most important H2 (featured snippet). Weave PAA questions as H2/H3 headings. 3-5 internal links per 1,000 words. Front-load value.

### Content type

Detect from the existing page + SERP. Load `references/content-types-overview.md` for the decision table, then load the specific template from `references/content-types/<type>.md` for the full rewrite structure. 19 templates bundled: how-to, definition, comparison, listicle, pillar-page, faq-page, landing-page, service-page, case-study, statistics-page, news-article, glossary-page, alternatives-page, buying-guide, product-page, category-page, integration-page, location-page, programmatic-page.

- **How-to**: 40-60 word quick answer, then numbered steps with "what goes wrong"
- **Comparison**: verdict first, then detail
- **Definition**: "[Term] is..." in the first sentence
- **Case study**: result number first, then the story

### Final checks
1. "So what?" test per section — could anyone have written this for anyone? If yes, inject specific knowledge.
2. Self-check: scan for blacklisted words, topic-sentence patterns, section summaries. Fix before delivering.

### Output
Clean markdown. Title + rewritten article content. Nothing else.

### Language
Write in the same language as the existing page content.

## Bundled references

Load from `references/` only when needed — don't preload the whole folder.

**Content type templates** (`references/content-types/`) — load one in Step 4:
- Common: `how-to.md`, `definition.md`, `comparison.md`, `listicle.md`, `pillar-page.md`, `faq-page.md`, `landing-page.md`, `service-page.md`, `case-study.md`
- Content and news: `statistics-page.md`, `news-article.md`, `glossary-page.md`
- Commercial: `alternatives-page.md`, `buying-guide.md`, `product-page.md`, `category-page.md`, `integration-page.md`, `location-page.md`, `programmatic-page.md`
- `references/content-types-overview.md` for the decision table across all 23 content types (load this FIRST if unsure which type to pick)

**Rewriting technique modules** (`references/`) — load when a rule calls for more depth:
- `anti-slop-ruleset.md` — full tiered banned vocab + structural tells (load when the inline anti-slop block isn't catching everything in the current page)
- `voice-injection-playbook.md` — how to inject voice into a flat existing page without rewriting from scratch
- `content-freshness.md` — decay signals and what to refresh vs. leave alone (the core of Step 3's update interview)
- `writing-pipeline.md` — the research → rewrite → edit loop adapted for updates
- `quality-scoring.md` — scoring rubric to run before delivering the rewrite
