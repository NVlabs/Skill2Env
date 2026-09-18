# CTR Benchmarks by Position

What a ranking position is actually worth in clicks, once you factor in the SERP features sitting on top of it.

## Why This File Exists

Position alone doesn't tell you anything useful anymore. A position 1 on a clean SERP isn't the same as a position 1 under an AI Overview, and neither looks like a position 1 on a local-intent query with a map pack. Before you judge whether a keyword is worth chasing, you need to know what the actual click share looks like at the positions you can realistically win.

All numbers below come from [First Page Sage's 2026 CTR report](https://firstpagesage.com/reports/google-click-through-rates-ctrs-by-ranking-position/) unless otherwise noted. First Page Sage defines a "clean" SERP as one with no maps, images, videos, or shopping results, just standard organic and paid listings. Treat the baseline column as an upper bound, not an average.

## The Main Table

| Position | Baseline CTR (clean SERP) | CTR when you hold the featured snippet | CTR with AI Overview (not cited) | CTR with AI Overview (cited) | CTR when local pack is present |
|---|---|---|---|---|---|
| 1 | 39.8% | 42.9% | ~16.7% (see note) | ~22.6% (see note) | 23.7% |
| 2 | 18.7% | 27.4% | ~7.9% | ~10.6% | 15.1% |
| 3 | 10.2% | n/a | ~4.3% | n/a | n/a |
| 4 | 7.2% | n/a | ~3.0% | n/a | n/a |
| 5 | 5.1% | n/a | ~2.1% | n/a | n/a |
| 6 | 4.4% | n/a | ~1.8% | n/a | n/a |
| 7 | 3.0% | n/a | ~1.3% | n/a | n/a |
| 8 | 2.1% | n/a | ~0.9% | n/a | n/a |
| 9 | 1.9% | n/a | ~0.8% | n/a | n/a |
| 10 | 1.6% | n/a | ~0.7% | n/a | n/a |

**Featured snippet rows:** First Page Sage reports 42.9% when the position 1 page also holds the snippet, and 27.4% when the position 2 page holds it (a common configuration). Losing a snippet you previously held costs 20-40% of organic clicks ([First Page Sage 2026](https://firstpagesage.com/reports/google-click-through-rates-ctrs-by-ranking-position/)).

**AI Overview rows:** First Page Sage lists a direct "AIO present, Position 1" number of 38.9%, but that figure bakes in both cited and uncited pages. The harder, more honest number comes from [Ahrefs' December 2025 analysis of 300,000 keywords](https://ahrefs.com/blog/ai-overviews-reduce-clicks-update/): an AI Overview on the query correlates with a 58% drop in clicks to the top-ranking page versus the pre-AIO baseline. Applied to 39.8%, that lands position 1 near 16.7% when you're the top result sitting under an uncited AIO. [Seer Interactive's September 2025 study](https://www.seerinteractive.com/insights/aio-impact-on-google-ctr-september-2025-update) puts the drop at 61% and reports that pages cited *inside* the AI Overview earn 35% more clicks than non-cited peers, which is how the "cited" column gets you back to ~22.6%. Both studies are from informational query samples, so the 58-61% drop isn't a universal constant; it's the most-studied intent class.

**Local pack rows:** First Page Sage reports 23.7% for position 1 and 15.1% for position 2 when a local pack sits on top. Worth noting: [Backlinko's local click study](https://backlinko.com/google-user-behavior), updated in BrightLocal's 2026 data, finds that 42-47% of clicks on local-intent queries go *into* the pack itself. If you're not in the 3-pack and the query has local intent, the organic blue links below are competing for roughly half the remaining clicks.

## Mobile vs Desktop Differential

[Advanced Web Ranking's Q3 2025 CTR report](https://www.advancedwebranking.com/blog/ctr-google-2025-q3) found position 1 desktop CTR fell by 0.99 percentage points versus Q2 2025, while mobile stayed roughly flat. More importantly, the gap between position 1 and position 2 is much wider on desktop (53.45%) than mobile (39.03%). Mobile users scroll further because the top of the SERP is taller, so the compression between positions is gentler.

Informational queries specifically: position 1 dropped 1.25 pp on mobile and position 2 gained 1.18 pp on desktop in the same report. Don't over-interpret a quarter of movement, but the trend is consistent with AI Overviews eating into the very top of the SERP on informational intent.

## Zero-Click Context

Before anyone gets excited about 39.8% at position 1, remember that roughly 60% of Google searches end without any click at all ([Digital Bloom 2026 Organic Traffic Crisis Report](https://thedigitalbloom.com/learn/organic-traffic-crisis-report-2026-update/)), and mobile zero-click behavior hits 77%. The CTR percentages above are shares of the *clicks* that happen, not shares of the *searches*. On a 1,000-impression keyword with a 60% zero-click rate, position 1 gives you 39.8% of 400 clicks: 159, not 398.

## When CTR Data Doesn't Apply

**Brand and navigational queries.** Someone searching "hubspot login" or "mailchimp pricing" is looking for a specific page they already know exists. Position 1 CTR on pure navigational queries typically sits between 50% and 80% depending on sitelinks and SERP layout ([aggregated across industry studies](https://backlinko.com/google-ctr-stats)). Don't apply the 39.8% baseline to keywords where your own brand is in the search string. You'll underestimate your click share and misread the opportunity.

**Extremely high-intent transactional queries.** "Buy X" type queries compress the CTR curve because users are hunting for a very specific page type. Position 1 often outperforms the baseline, and positions 4-10 often underperform because users bounce back to try a better match.

**Very low-volume long-tail.** Sub-10 monthly impression keywords don't behave like the averages. One user can be 100% CTR or 0% CTR on any given day. Don't forecast these with the table.

## How to Use This File in a Keyword Deep Dive

1. Identify which SERP features are present on the keyword's SERP (see `serp-features-recognition.md`).
2. Pick the column that matches the SERP reality, not the baseline.
3. Apply the zero-click discount for informational intent before you estimate traffic.
4. Cross-reference with `zero-click-and-aio-impact.md` if the SERP has an AI Overview. The answer for whether the keyword is still worth targeting depends on whether you can get cited inside it.
