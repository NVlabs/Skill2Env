# Zero-Click and AI Overview Impact

When a keyword ranks but the clicks don't come, it's usually because the SERP is answering the question before the user ever leaves the page. This file tells you how to spot that pattern and decide whether to keep pursuing the keyword anyway.

## The Headline Numbers

Two independent studies put the organic CTR drop from AI Overviews in roughly the same range, and both used production data from real sites.

**[Ahrefs, December 2025](https://ahrefs.com/blog/ai-overviews-reduce-clicks-update/):** 58% lower average CTR on the top-ranking page when an AI Overview is present. Methodology: 300,000 keywords from their Keywords Explorer database (150k with an AIO, 150k informational without), using aggregated GSC data from December 2023 (pre-AIO) versus December 2025. On AIO keywords, position 1 CTR fell from 0.073% to 0.016%. On informational keywords without an AIO, position 1 fell from 0.076% to 0.039%, so some of the decline is a broader behavioral shift. The 58% figure isolates the AIO-specific delta.

**[Seer Interactive, September 2025](https://www.seerinteractive.com/insights/aio-impact-on-google-ctr-september-2025-update):** 61% drop in organic CTR for AIO-present informational queries, from 1.76% to 0.61%. Paid CTR dropped 68%. Sample: 3,119 informational queries, 42 client organizations, 25.1 million organic impressions, June 2024 through September 2025. Seer also reports CTR fell 41% on queries *without* AI Overviews over the same window, which matches the broader decoupling story.

The two studies used different methodologies and different keyword samples and landed within 3 percentage points of each other. That's unusual alignment for SEO research, and it's the reason we treat "roughly 60% organic CTR loss under an AIO" as the planning assumption for informational intent.

## The Citation Bonus

Seer's same study found pages cited *inside* the AI Overview earn 35% more organic clicks than non-cited peers in the same SERP (0.70% vs 0.52% organic CTR in Q3 2025). Paid lift for cited brands was 91%. Seer can't prove causation (authority signals may drive both citation likelihood and baseline clickability), but the pattern is strong enough to plan around.

Separately, [Ahrefs' February 2026 update](https://ahrefs.com/blog/ai-overview-citations-top-10/) found that only 38% of AIO citations come from pages ranking in the top 10 for the original query, down from 76% seven months earlier. They analyzed 863,000 keywords and 4 million AI Overview URLs. The remaining citations split between pages ranking 11-100 (31.2%) and pages outside the top 100 entirely (31%). This matters because it breaks the old assumption that "rank top 10 and you'll get cited." Google's January 27, 2026 Gemini 3 upgrade is the most likely explanation: query fan-out pulls citations from sub-queries that may not match the main query's top 10 at all.

## What This Means Practically

Getting cited in an AIO is now less about ranking the main query and more about matching a fan-out sub-query Google generates to build the summary. That changes the optimization target: instead of only ranking for "best CRM for startups," you're also trying to match sub-queries like "CRM pricing for 5-person teams" or "Pipedrive vs HubSpot for SaaS," because those are what Google decomposes the main prompt into.

## Which Queries Trigger AI Overviews

AIOs appear most often on:

- **Informational, question-format queries** ("how to...", "what is...", "why does..."). The Seer study explicitly scoped to this category because it's most vulnerable.
- **Comparison and multi-criteria queries**. [Conductor's query fan-out analysis](https://www.conductor.com/academy/query-fan-out/) notes that complex queries trigger extensive fan-out, which feeds the AIO generation pipeline.
- **Early-funnel research queries** where there's no single authoritative source and users benefit from a synthesized answer.
- **Health and finance categories** saw outsized AIO growth (206-273%) between January and March 2025 per [Digital Bloom 2026](https://thedigitalbloom.com/learn/organic-traffic-crisis-report-2026-update/).

AIOs appear *less* often on:

- Pure navigational queries (brand searches)
- Local-intent queries where a map pack dominates
- Very high-commercial-intent queries ("buy X now") where Google prioritizes shopping ads
- Fresh news queries where there's no stable answer to synthesize
- Ambiguous single-word queries where intent is unclear

## When to Still Target a Keyword With AIO Displacement

The decision is rarely "abandon the keyword." It's "reframe what winning looks like." Run through these questions:

1. **Can you plausibly get cited inside the AIO?** If yes, you still get 35% *more* clicks than peers, not fewer. Citation eligibility depends on matching fan-out sub-queries, not just ranking the main query.
2. **Is this keyword part of a cluster where multiple pages can earn citations across the fan-out?** If yes, one page losing direct clicks may be offset by three others earning citation visibility.
3. **Does brand exposure in the AIO itself have value independent of clicks?** For commerce brands, being named in an AIO is effectively free advertising even without the click.
4. **Is there a transactional tail you're really targeting?** The AIO may suppress the informational head query's CTR, but the transactional tail ("buy X," "sign up for X") is usually AIO-free and carries the conversion weight anyway.
5. **If none of the above: accept the structurally low click potential.** Don't burn effort on a keyword whose whole value has been absorbed upstream. Move it to the "impression-only brand exposure" bucket or cut it entirely.

## The Zero-Click Baseline

Even before AIOs enter the picture, [Digital Bloom's 2026 report](https://thedigitalbloom.com/learn/organic-traffic-crisis-report-2026-update/) puts overall Google zero-click rates at 60%, with mobile zero-click at 77%. That's the floor. AIOs sit on top of it. So when you apply the 58-61% AIO-specific CTR drop to a SERP that's already operating under a 60% zero-click ceiling, the click potential for informational keywords with AIOs is genuinely thin. This isn't doom framing, it's planning input: stop treating impressions as a proxy for traffic for these query types.

## Cross-References

- `ctr-benchmarks-by-position.md` has the exact CTR numbers by position with and without SERP features.
- `serp-features-recognition.md` covers how to tell which SERP features are present without a paid tool.
- The `featured-snippet-optimizer` skill holds the decision on when to target a featured snippet versus accept AIO displacement. If both a snippet and an AIO are present on the same SERP, defer to that skill for the target tradeoff.
