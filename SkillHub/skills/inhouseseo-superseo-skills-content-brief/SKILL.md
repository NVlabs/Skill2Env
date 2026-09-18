---
name: content-brief
description: Use when planning a new article. The agent Googles the keyword, reads the top 10 results, classifies intent, maps the content gap, and produces a writer-ready brief with structure, outline, and on-page artifacts. No keyword tool required.
---

# Content Brief

A writer-ready content brief based on real SERP analysis. The agent Googles the target keyword, reads the top 10 results, classifies intent, identifies competitor gaps, and produces the brief. No keyword tool exports, no manual SERP pasting.

## Input

**Target keyword** (required). Optionally: business context if you want the brief tailored to a specific audience/tone.

If the user didn't provide a keyword, ask for it before proceeding.

## Role

You are a senior content strategist and SEO brief specialist with 10+ years of experience. Your job is to produce a complete, writer-ready brief based on what actually ranks right now — not a generic template.

## Step 1: Research the SERP

Google the target keyword. Read the top 10 results. For each top-ranking page, note:
- Content format (listicle / long-form guide / comparison / how-to / tool / video)
- Approximate word count
- Heading structure (H1, main H2s)
- Content angle and unique hook
- What they cover that others don't
- Whether they appear to hold a featured snippet, People Also Ask positions, or other SERP features

## Step 2: Identify Search Intent

Classify dominant intent: **Informational / Commercial Investigation / Transactional / Navigational**.

Apply intent-specific length guidance:
- **Informational**: 1,500–3,000+ words — completeness, PAA coverage
- **Commercial**: 2,000–4,000 words — features, comparison, objectivity
- **Transactional**: 800–1,500 words — trust signals, CTAs, specs
- **Navigational**: 500–1,000 words — speed, direct info

Target word count = average of top 5 results + 10%. Never pad to hit a number.

## Step 3: Map the People Also Ask

If PAA questions appear for this keyword, write them down verbatim. They'll become H2/H3 headings in the outline.

## Step 4: Identify Content Type

Pick the content type from the SERP pattern. Content types: how-to, definition/explainer, comparison, listicle, product-review, case-study, pillar-page, faq-page, landing-page, service-page, category-page, buying-guide, alternatives-page, pricing-page, location-page.

Load `references/content-types-overview.md` for the one-screen decision table covering all 23 content types (H1/H2 structure, schema, snippet format, word counts). Use it to pick the right type in 30 seconds, then hand the choice over to `write-content`.

## Step 5: Produce the Brief

### Target Keyword Analysis

- Primary keyword | Apparent difficulty based on SERP competition | Dominant intent
- Difficulty strategy: Easy SERP (lots of low-DR competitors, mixed intent) = 3-6 months realistic / Moderate (all top results are DR 40+, uniform intent) = 6-12 months / Hard (top results are all DR 60+, highly optimized, long-form) = 12+ month authority play
- Related terms to target on the same page (from what the top pages cover as H2s)

### SERP Competitive Intelligence

For each of the top 3 competitors:
- URL | Estimated words | Format type | Key sections covered | What they miss

### Content Gap Analysis

Specific subtopics covered by 2+ top competitors but missing from where most results are thin. Name exact missing sections — not generic "add more depth."

### Recommended Outline

H1 and H2/H3 structure aligned to search intent and the gap analysis. Include:
- **Featured snippet target**: which H2 hosts the 40-60 word snippet answer — mark the spot
- **PAA integration**: questions to address as H2/H3 headings
- **FAQ section** if 3+ PAA questions exist

### Hub & Spoke Architecture
- This piece as: hub / spoke / standalone (based on keyword breadth)
- Internal linking pattern recommended

### Technical Optimization
- **Title tag**: 50-60 chars, primary keyword near front
- **Meta description**: 150-160 chars, intent signal + CTA
- **Schema**: Article / FAQ / HowTo / Product / Review (choose based on content type)
- **Featured snippet format**: paragraph (what is) / ordered list (how to) / table (comparison)

### E-E-A-T Signals Required
- Author expertise markers needed
- Original data or research to include
- External authoritative sources to cite

### Resource Assessment
- **Effort**: Low (500-1,000w, 2-4h) / Medium (1,000-2,500w, 6-12h) / High (2,500w+, 16h+)
- Realistic 3-month target position given SERP difficulty

## What to Ignore

- **Keyword density targets** — write naturally. Primary keyword in H1, first 100 words, 2-3 H2s (~2% body density is a ceiling, not a target)
- **NLP term lists of 50+ words** — focus on 5-8 core entities that must appear
- **Word count without checking SERP** — "write 3,000 words" without intent matching creates padded content

## Next Step

Brief ready? Use the `write-content` skill with this brief as context to write the article.

## Bundled references

Load these from `references/` only when the step calls for them — don't preload.

- **`content-types-overview.md`** — decision table for picking the right content type (Step 4)
- **`intent-matching.md`** — deep read on Informational / Commercial / Transactional / Navigational signal matching (Step 2, when the SERP intent is mixed or unclear)
- **`serp-driven-writing.md`** — how to turn the top 10 read into outline decisions (Step 5, if the gap analysis is thin)
- **`information-gain-writing.md`** — what qualifies as "new information" vs. index (Step 5, when briefing the unique angle)
- **`structured-data-snippets.md`** — snippet format per content type (Step 5, "Technical Optimization" block)
- **`human-input-framework.md`** — the 2-3 questions to ask the writer before they start (optional, when briefing for an outside writer rather than the agent)
