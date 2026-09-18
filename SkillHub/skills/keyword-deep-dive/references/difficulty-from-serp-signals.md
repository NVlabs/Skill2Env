# Difficulty From SERP Signals

How to classify a keyword as Easy, Moderate, or Hard by reading the actual SERP instead of trusting a KD score from a paid tool.

## Why We Reject KD Scores

KD scores from Ahrefs, Moz, and Semrush are modeled estimates built from different formulas. Ahrefs leans primarily on referring domains; Semrush blends backlink strength with keyword characteristics. There's no industry-standard formula, and [Keywords Everywhere's comparison](https://keywordseverywhere.com/blog/how-the-top-tools-calculate-kd/) notes the tools can differ by 30+ points on the same keyword. A KD of 15 in one tool can be a KD of 55 in another. That's not a minor disagreement; it's a signal that the metric isn't measuring what you care about.

What you actually care about: *can a site like mine realistically earn a page-1 position in the next 6-12 months?* That's a question about the specific SERP and your specific position on it, not a single number. The rubric below replaces the KD score with a signal count you can read from the live SERP in 10 minutes.

## Easy Signals

- Top 10 dominated by small sites (no recognizable publisher logos)
- Thin content in the top 5 (pages under 1,000 words with minimal structure)
- Only 3-4 pages actually answer the query; positions 5-10 are loose matches
- Clean blue-link SERP with no featured snippet or AI Overview
- No Wikipedia or government domain in top 10
- Top 3 have no visible E-E-A-T signals

Most of these present? A modest-authority site can plausibly reach top 5 in 3-6 months with a single well-executed page.

## Moderate Signals

- Mix of authority and small sites in top 10 (HubSpot alongside a small blog or a forum thread)
- 1-2 SERP features present but not dominating
- Content depth varies (800-word pages alongside 3,000-word pages), meaning Google hasn't locked in a depth preference
- Top 10 Domain Rating roughly mixed in the 30-60 range

This is where the game is won with a better page than the mid-pack incumbents. Expect 6-12 months to top 5 with sustained execution and internal linking from your existing cluster.

## Hard Signals

- Every top 10 is a high-authority site (major publishers or well-known category leaders)
- Top 10 content consistently 2,500+ words with strong structure
- Multiple SERP features stealing clicks (featured snippet, AI Overview, image pack stacked on one SERP)
- Original data or proprietary frameworks in top 3 that you'd have to build from scratch
- Every top 5 has named authors with credentials plus first-party research artifacts
- A dedicated niche-authority site holds a top 3 position

Expect 12-24 months before top 5 is realistic. A one-page play won't work; you'll need a cluster plus authority growth, usually backed by original research.

## The 10-Point Rubric

Count each signal that applies. Sum the points and map to a bucket.

1. **Top 10 includes Wikipedia or a government/institutional domain.** (+1)
2. **Top 10 has more than 5 high-authority publishers** (HubSpot, Forbes, NYT, major SaaS brands). (+1)
3. **Every top 5 result is over 2,500 words.** (+1)
4. **Featured snippet is held by a top-3 authority brand.** (+1)
5. **AI Overview is present on the SERP.** (+1)
6. **Every top 5 has named authors with visible credentials.** (+1)
7. **Top 3 include original data or proprietary frameworks.** (+1)
8. **Top 10 has consistent freshness signals indicating active maintenance.** (+1)
9. **A dedicated niche-authority site holds a top 3 position.** (+1)
10. **Meta descriptions in top 5 are clearly CTR-optimized.** (+1)

**Mapping:**

- **0-3 = Easy.** A focused new page can plausibly reach top 5 in 3-6 months. Single-page play is viable.
- **4-6 = Moderate.** Cluster approach recommended. 6-12 months to top 5. Requires better content than mid-pack incumbents.
- **7-10 = Hard.** 12-24 months. Requires original research plus sustained authority building.

The rubric is directional, not mathematical. If you're between two buckets, pick the harder one and let reality correct you.

## "Shouldn't Attempt" Signals

Some SERPs are unwinnable regardless of rubric score. If any of these apply, the honest answer is "skip this keyword."

- **Wikipedia holds top 3.** You're not outranking Wikipedia on general-knowledge queries. Target a long-tail variation.
- **Reddit dominates top 10.** Reddit threads rank because users explicitly want discussion format. Google's "hidden gems" update cemented Reddit's position on many queries. You can't replicate a forum discussion with an article.
- **Government or official organization dominates.** On regulations or health guidelines, Google trusts the source of authority rather than content quality. Outranking is not realistic.
- **Pure news cycle SERP.** See `serp-volatility-heuristics.md` Level 4. These belong to Google News publishers.
- **AI Overview displaces most clicks AND the query is informational AND you can't get cited inside the AIO.** Click potential is too thin. See `zero-click-and-aio-impact.md`.
- **Top 3 is all branded product pages on a non-brand query.** Google has decided the keyword is transactional and your editorial content won't rank. Either build a product or skip.

## How to Apply This

After reading the top 10, walk through the 10-point rubric and score. Check the "shouldn't attempt" signals; if any apply, flag and recommend pivoting. Map the score to Easy / Moderate / Hard and use it for the timeline estimate in Step 6 of the main skill. If the SERP signals something the rubric misses, override it and explain why. The rubric is a shortcut, not a rule.
