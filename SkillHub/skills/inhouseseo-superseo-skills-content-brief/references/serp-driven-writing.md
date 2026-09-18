# Technique 05: SERP-Driven Writing

## What It Is

Writing content based on what ACTUALLY ranks in Google, not what theoretically should work. Every structural decision -- headings, length, format, keyword placement -- is derived from analysis of the current top 10 results for the target keyword.

## Why It Works

Google's ranking system is empirical. What ranks IS what Google rewards. SERP analysis reverse-engineers the patterns that currently win for a specific query. This approach beats theoretical best practices because it accounts for query-specific factors: intent, competition level, SERP features, and user expectations.

Kyle Roof's 400+ controlled experiments at PageOptimizer Pro proved that on-page signals alone can achieve rankings -- but only when those signals match what Google expects for that specific query.

## E-E-A-T: What Actually Matters

### The Reality (vs. What Google Says)

**Kyle Roof's tested position:** E-E-A-T elements will NOT help you rank, but they help you KEEP your rank once evaluated. He ranked a Lorem Ipsum page for "Rhinoplasty Plano" using on-page signals alone. E-E-A-T is defensive, not offensive.

**The priority:** Trust > Expertise > Experience > Authoritativeness

**Cyrus Shepard's 50-site case study (4,000+ websites across 2023 updates):**
- Winners: used first-person pronouns, demonstrated first-hand experience
- Losers: excessive ads (14.01 per page vs. 6.32 on winners), over-optimized anchor text
- 17 on-page features showed statistically significant correlations

### E-E-A-T Signals the Writing Skill Should Produce

**Experience signals (the new "E"):**
- First-person language: "in my testing," "when I tried," "our data shows"
- Specific case studies with real numbers and dates
- References to original photos, screenshots, or videos
- Practical tips that only come from doing the thing

**Expertise signals:**
- Depth of coverage (not just mentioning a topic, but explaining the WHY)
- Correct use of industry terminology
- Nuanced positions (not just repeating the obvious)
- Citing specific sources (not "experts say")

**Trust signals:**
- Author attribution with verifiable credentials
- Transparent methodology ("here's how we tested this")
- Honest limitations ("this approach doesn't work for X")
- Clear source attribution for claims

## Keyword Placement (Kyle Roof's Tested Hierarchy)

Based on 400+ controlled experiments:

**Group A (Highest weight):**
- Meta title -- the undisputed #1 on-page signal

**Group B:**
- URL path
- H1 heading
- Body content (~2% density, naturally distributed)
- H2 headings (primary keyword or close variation in 2-3 H2s)
- H3/H4 headings
- Anchor text of internal links TO this page

**Group C:**
- Bold text
- Italic text
- Image alt text

**Group D (Lowest):**
- Schema markup text
- HTML tags
- Open graph text

**Not indexed at all:**
- Meta description (doesn't affect rankings, but affects CTR)
- Meta keyword tag

**Kyle Roof's evolved position:** Stop counting exact-match keywords. Instead, ensure the page includes the FULL VOCABULARY of the topic. Topical completeness matters more than keyword density.

## Content Length by Intent

Ahrefs found near-zero correlation (0.04) between word count and ranking. The data by intent:

| Intent | Optimal Length | Rationale |
|--------|---------------|-----------|
| Informational (comprehensive guide) | 1,500-3,000+ | Needs to cover the full topic |
| Informational (specific question) | 800-1,500 | Answer directly, don't pad |
| Commercial investigation (comparison) | 1,200-2,500 | Depth in evaluation criteria |
| Commercial investigation (roundup) | 2,000-4,000 | Multiple items need coverage |
| Transactional | Minimal needed | No fluff; specs, pricing, CTA |
| Local service | 300-500 unique words | Must be genuinely unique per location |

**Key rule:** Match the SERP. If top 5 results average 2,000 words, write 2,000-2,500. If they average 800, writing 3,000 wastes effort and may signal wrong intent.

## Featured Snippet Optimization

**Format distribution:** Paragraph (70%), List, Table, Video

**Optimal answer length:** 40-50 words (293 characters average)

**Query-format mapping:**
- "How" queries -> ordered list snippets (46.91%)
- "Does/Are/Is/Can/Should/Will" queries -> paragraph snippets
- Comparison queries -> table snippets
- "What is" queries -> paragraph snippets (definition format)

**Implementation:** Place a 40-60 word direct answer immediately after the relevant H2. Format it as the snippet type Google expects for that query. Then expand below.

## People Also Ask Coverage

PAA prevalence spiked 34.7% on mobile and 37.5% on desktop (2024-2025). Your site does NOT need to rank #1 to appear in PAA.

**Strategy:**
- Include 3-5 PAA questions as H2 or H3 headings
- Answer each in 40-60 words immediately after the heading
- Then expand with detail below the direct answer
- Use the exact question phrasing when natural

## Algorithm Signals That Matter (From the Leak)

### NavBoost (Confirmed)
Uses rolling 13-month window of click data. Tracks:
- **goodClicks** -- positive engagement
- **badClicks** -- negative engagement
- **lastLongestClicks** -- where the user's search ENDED (strongest signal)

**Writing implication:** Content must immediately engage. The first screen of content determines whether users stay or pogo-stick back. Front-load value.

### Information Gain (Patent Granted June 2024)
Measures how much UNIQUE information a document provides beyond what already exists. NOT about length -- about saying something competitors don't.

**Writing implication:** Every article must contain at least one section that adds genuinely new information: original data, unique analysis, contrarian perspective, or specific case study.

### Site Authority (Confirmed in Leak)
Despite public denials, Google has a site-level authority metric. Homepage authority influences the entire domain.

**Writing implication:** Each piece of content contributes to site-level authority. Thin, low-quality content hurts the whole domain (HCU classifier operates site-wide).

## Content Scoring Tools: Reality Check

Surfer SEO, Clearscope, Frase analyze top-ranking pages and identify patterns. Ahrefs tested correlation with actual rankings:
- NeuronWriter + Ahrefs: Strongest (but modest) correlation
- Clearscope: ~0.30
- Surfer SEO: ~0.27

**The fundamental limitation:** These tools measure FIRST-STAGE retrieval signals only (lexical matching, BM25-style). After that:
1. RankEmbed adds candidates keyword matching missed
2. Mustang applies ~100+ signals including NavBoost, quality scores
3. DeepRank applies BERT-based understanding to final 20-30 results

**Bottom line:** Use SERP-derived topical completeness as a baseline check, not a ranking guarantee. The writing skill should ensure all SERP-common topics are covered, but the real ranking signals come from engagement, uniqueness, and authority.

## Content Freshness

### QDF (Query Deserves Freshness)
Activates for: breaking news, recurring events, topics with frequent updates. When active, newer content temporarily outranks stronger traditional signals.

### AI Citation Freshness
ChatGPT shows strongest recency preference: 76.4% of most-cited pages were updated within 30 days.

### Practical Rules
- Date-stamp all content with publication and last-updated dates
- Update high-traffic content every 3-6 months
- Don't just change the date -- Google detects fake freshness
- 51% of companies report updating content is more effective than creating new

## Tips

- Match SERP format exactly: if the top 5 all use comparison tables, include a comparison table
- Check SERP features before writing: featured snippets, PAA, video carousels each require different content structures
- Use SERP feature detection to identify which SERP features are available for target keywords
- Monitor ranking changes after publishing to validate SERP-driven decisions

## Common Mistakes

1. **Ignoring the SERP entirely** -- writing based on assumptions instead of what currently ranks
2. **Over-optimizing for content scoring tools** -- these only measure first-stage retrieval signals
3. **Writing longer than needed** -- if the SERP rewards 800-word answers, a 3,000-word article signals wrong intent
4. **Copying competitor structure without adding value** -- matching format is necessary but insufficient; you still need information gain

## Key Sources

- Kyle Roof -- PageOptimizer Pro: [nichepursuits.com](https://www.nichepursuits.com/kyle-roof-hcu/), [pageoptimizer.pro](https://www.pageoptimizer.pro/bestplacestoputakeyword)
- Cyrus Shepard -- [zyppy.com](https://zyppy.com/seo/google-update-case-study/)
- [Content Scoring: First Gate in Google's Pipeline (Search Engine Land)](https://searchengineland.com/content-scoring-tools-work-but-only-for-the-first-gate-in-googles-pipeline-469871)
- [Ahrefs Content Score Study](https://ahrefs.com/blog/seo-content-score-study/)
- [NavBoost Analysis (Hobo)](https://www.hobo-web.co.uk/navboost-how-google-uses-large-scale-user-interaction-data-to-rank-websites/)
- [Google Leak Analysis (Hobo)](https://www.hobo-web.co.uk/the-google-content-warehouse-leak-2024/)
- [Information Gain Patent (SEJ)](https://www.searchenginejournal.com/googles-information-gain-patent-for-ranking-web-pages/524464/)
- [Featured Snippet Statistics 2025](https://mycodelesswebsite.com/featured-snippet-statistics/)
