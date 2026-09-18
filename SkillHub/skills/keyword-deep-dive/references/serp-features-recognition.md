# SERP Features Recognition

A field guide for reading a Google SERP like an analyst. You can do this from a live search without any paid tool. The skill is knowing what the features look like and what they do to your click potential.

## Why This Matters

Google now displays at least one SERP feature on roughly 80% of first-page results ([Backlinko SERP features guide](https://backlinko.com/hub/seo/serp-features)). The blue-link-only SERP is the exception, not the default. If you classify a keyword's difficulty or CTR potential without noting the features, you'll over-promise the traffic estimate every time.

## The Feature Table

| Feature | How to recognize | Triggers | CTR impact | Can we target it? |
|---|---|---|---|---|
| Featured snippet | Boxed answer at the top with bold excerpt, list, or table, showing source URL underneath | "what is...", "how to...", definition and comparison questions | 42.9% if you hold it; 20-40% loss if a competitor holds it ([First Page Sage 2026](https://firstpagesage.com/reports/google-click-through-rates-ctrs-by-ranking-position/)) | Yes, by structuring your answer in 40-60 words directly under an H2 matching the question |
| People Also Ask | Expandable questions stacked vertically, each with a dropdown answer | Almost any informational query (PAA shows on ~64.9% of searches per [Semrush](https://www.semrush.com/blog/serp-features/)) | 3% click the PAA box on average, 13.6% on transactional queries ([Backlinko](https://backlinko.com/google-user-behavior)) | Yes, by answering PAA questions as H2s inside your article |
| AI Overview | AI-generated summary at the top with "AI Overview" label and source citations on the right | Informational, question-format, and comparison queries | 58-61% organic CTR drop for top-ranking page; cited pages earn 35% more ([Ahrefs Dec 2025](https://ahrefs.com/blog/ai-overviews-reduce-clicks-update/), [Seer Sep 2025](https://www.seerinteractive.com/insights/aio-impact-on-google-ctr-september-2025-update)) | Partially: only 38% of citations come from the main query's top 10 ([Ahrefs Feb 2026](https://ahrefs.com/blog/ai-overview-citations-top-10/)), so target fan-out sub-queries |
| Image pack | Horizontal row of 4-8 image thumbnails with "Images" label | Visual queries: products, recipes, places, visual how-tos | Sites in the pack get higher CTR; sites below get lower CTR | Yes, with properly tagged, high-quality images |
| Video carousel | Horizontal strip of YouTube thumbnails with durations | How-to queries, product reviews, tutorials | Net negative for organic blue links; YouTube captures the clicks | Sometimes, if the query genuinely wants video. Publishing on YouTube may beat outranking them |
| Local pack | Map + 3 business listings with reviews, hours, "More places" link | Queries with local intent: "near me," "[service] [city]" | Position 1 organic CTR drops to 23.7%; 42-47% of clicks go into the pack ([First Page Sage 2026](https://firstpagesage.com/reports/google-click-through-rates-ctrs-by-ranking-position/), [BrightLocal](https://www.brightlocal.com/research/local-services-ads-click-study/)) | Only with a physical location |
| Knowledge panel | Right-side panel with photo, bio, key facts | Entity queries: brands, public figures, concepts with Wikipedia entries | Reduces position 1 CTR; question often answered inside the panel | No, unless the query is about your own brand or entity |
| Sitelinks | 4-6 additional indented links below a top result | Brand / navigational queries where Google trusts the site's structure | Strongly positive for the site that gets them | Indirectly, via clear site hierarchy and brand signal |
| News boxes / Top Stories | Horizontal strip of news articles with logos and timestamps | News-sensitive queries, trending topics | Dominates fresh-query SERPs; clicks concentrate in the carousel | Only if you're a Google News-approved publisher |

## The Four You'll Hit Most

**Featured snippet.** The highest-value real estate outside of an AI Overview. [First Page Sage 2026](https://firstpagesage.com/reports/google-click-through-rates-ctrs-by-ranking-position/) puts it at 42.9% CTR when you hold it versus 39.8% for a snippet-free position 1. The real win: snippets can be held from positions 2-10, so you don't have to outrank the top result to steal their clicks. The catch is that snippets are evaporating. [Ahrefs found featured snippet prevalence dropped from 15.41% to 5.53% of SERPs between January and June 2025](https://ahrefs.com/blog/how-serp-features-have-evolved-in-the-ai-era/), displaced by AI Overviews. Check whether one exists before planning a snippet strategy.

**People Also Ask.** Feels prominent but carries less weight than its visual footprint suggests. [Backlinko](https://backlinko.com/google-user-behavior) found only 3% of searchers click a PAA box on average, rising to 13.6% on transactional queries. The real value isn't direct CTR, it's intent signal. If "is X worth it?" shows up on a keyword you thought was informational, the intent is actually commercial investigation. PAA also tells you which sub-questions to answer as H2s inside your main article, which is free cluster-building.

**AI Overview.** The feature reshaping everything else. It sits above the first organic result and pushes blue links below the fold, absorbing the most clickable fraction of the SERP. [Ahrefs Dec 2025](https://ahrefs.com/blog/ai-overviews-reduce-clicks-update/) and [Seer Sep 2025](https://www.seerinteractive.com/insights/aio-impact-on-google-ctr-september-2025-update) both landed on roughly 60% organic CTR loss under an AIO. See `zero-click-and-aio-impact.md` for the full decision framework. When you spot an AIO, stop estimating traffic from impression volume alone. Ask whether you can get cited *inside* the overview instead of ranking the blue link below it.

**Local pack.** The whole game for local-intent queries. [BrightLocal's 2026 update](https://www.brightlocal.com/research/local-services-ads-click-study/) shows 42-47% of users click into the pack, which means the organic results below compete for roughly the remaining half of the clicks (after zero-click searches and local service ads). The less obvious skill is recognizing local intent *before* you search. "Best Italian restaurant" looks informational but is always local. "Plumber" is always local. "Best CRM" is not.

## Detecting Features Without Paid Tools

1. **Use incognito** to avoid personalization. Set location if testing local-intent queries from outside the target region.
2. **Check desktop and mobile.** Mobile often stacks features more aggressively.
3. **Scroll the full first page.** Video carousels and image packs often sit between positions 3 and 7.
4. **Count above-the-fold organic results.** If zero blue links are above the fold, the keyword is structurally compressed regardless of position.
5. **Check the right rail.** A knowledge panel absorbs clicks away from position 1 even when it doesn't feel like a traditional feature.
6. **Search a clean variation.** If the main query triggers an AIO but a close variation doesn't, the variation may have much higher click potential.
7. **Screenshot it.** If you come back later, the SERP may have changed. Timestamped screenshots are your memory.

## What to Record

For every keyword deep dive:

- Every SERP feature present, in order of appearance
- Who holds the featured snippet (if any) and the format (paragraph / list / table)
- Whether an AI Overview is present and who is cited inside it
- Which organic positions are pushed below the fold
- Any unusual features (Twitter carousel, news box, Reddit discussions) that would make the SERP volatile

Feed this directly into `ctr-benchmarks-by-position.md` to pick the right column for your CTR estimate.
