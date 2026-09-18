# AI Search & GEO Statistics — May 2026 Review

*Last reviewed: 2026-05-23, post-Google-May-2026-core-update,
post-Gemini-3-rollout, post-Google-FAQ-rich-result-deprecation.*

Numbers below are from named, dated sources. Where a claim comes from
a single study, that's flagged. Treat any percentage as directional
unless replicated. If a stat is not here, it's because the underlying
source was too thin to repeat.

---

## What actually shifted Nov 2025 → May 2026

| Shift | Source |
|-------|--------|
| Gemini 3 became the default model for Google AI Overviews on 27 Jan 2026 | 9to5Google, SE Ranking |
| Google retired FAQ rich results in Search on 7 May 2026 (console reporting drops Jun 2026, API support drops Aug 2026) | Google Search Central, Search Engine Land |
| Google March 2026 Core Update re-weighted "Information Gain" (novel knowledge added vs. recycled). May 2026 Core Update applied spam policies to AI-generated responses in Search | developers.google.com, Search Engine Land |
| ChatGPT 7 May 2026 update gave referral links more prominence; Similarweb measured a step-change in referral traffic and ~60% of it now lands on brand homepages rather than deep pages | Aleyda Solis citing Similarweb |
| schema.org released v30.0 on 19 Mar 2026 (added `Credential`, `Error`; deprecated `Attorney` in favour of `LegalService`) | schema.org releases page |
| IndexNow added Internet Archive and Amazon to its participant list in early 2026 | indexnow.org `searchengines.json` |

## Citation behaviour by AI platform (directional)

These numbers come from third-party studies in the first half of
2026. They are useful for shaping recommendations, not for promising
results.

| Platform | Behaviour | Source |
|---|---|---|
| Google AI Overviews | After the Gemini 3 swap, ~42% of previously cited domains were replaced; ~88% of answers now cite 3+ sources; ~1% cite a single source | SE Ranking 100k-keyword study, Feb 2026 |
| Google AI Mode | Separate citation surface from AI Overviews — URL overlap ~14%. Uses query fan-out (multiple sub-queries per user prompt) | The Slide Factory analysis, blog.google I/O 2026 |
| ChatGPT (Search + Atlas) | Cites fewer sources but with deeper absorption per source; position bias is strong — material in the first ~30% of a page captures a disproportionate share of citations | iPullRank, AIBoost analysis |
| Perplexity | Sub-document / passage-level retrieval with a cross-encoder rerank — sections that are self-contained and independently citable get pulled even when the page as a whole isn't | Authority Tech, July 2025 arXiv study (366k+ citations) |
| Claude | Notably conservative citer; in one cross-platform study, ~39% of queries got citations vs. ~56% ChatGPT and >95% Perplexity / Google AI Mode. Brave Search visibility correlated highly with Claude citation in the same study | Prime AI Center, Oltre |
| Grokipedia | Lost most search visibility by mid-Feb 2026; Wikipedia outranks Grokipedia for "Grokipedia" itself. Treat as optional, not primary | Techdemis |

## Tactics worth keeping (re-validated in 2026)

The Princeton GEO tactics from 2024 have held up in the AgenticGEO
and "Citation Selection vs. Absorption" studies in 2026, with one
important amendment from the Ahrefs schema test below.

- Add statistics with named denominators and units.
- Quote named authorities (with credentials visible).
- Increase fluency — shorter sentences, more concrete nouns.
- Cite primary sources inline with links.
- Write authoritatively (declarative, not hedged).

## Tactics worth demoting

- **Schema markup as a GEO lever.** Ahrefs tested 1,885 pages that
  added JSON-LD schema and measured ~+2.4% lift on Google AI Mode —
  noise-level. Schema still earns its place for entity clarity, rich
  results, and Google Shopping, but stop pitching it as a citation
  trick. Pair it with original data publication.
- **llms.txt for citation boost.** GPTBot, ClaudeBot, PerplexityBot
  and OAI-SearchBot do not consume `llms.txt` in production as of
  May 2026 (presenc.ai survey). It IS now a Lighthouse 13.3 audit
  item under "Agentic Browsing" — useful for AI agents that drive
  the page directly, but it does not move SERP or AI-citation
  ranking. Generate it, but don't oversell it.
- **Keyword stuffing, content padding, simplification, pure
  persuasion** — all measured as negative or null in the 2026 GEO
  studies. The skill's content optimizer treats these as anti-patterns.

## Numbers we used to cite that are gone

The following appeared in `statistics-2025.md` and have been removed
because they were unsourced or no longer applicable:

- "527% AI-referred traffic growth" — single-vendor blog post,
  never replicated.
- "+35% TL;DR / +40% credentials / +40% heading hierarchy /
  3.2× freshness" — these specific percentages traced back to a
  single white paper; the underlying tactics remain valid, the
  numerical lift does not.
- "33-40% higher visibility" — unattributed marketing line.

## Open questions worth watching

- **Apple "World Knowledge Answers"** — slated for iOS 26.4. Gemini
  backed per public reporting; ranking signal mix unknown until
  ship.
- **WebMCP** in Chrome 149 origin trial — lets a site declare tools
  / actions for AI agents. Long-horizon; nothing actionable yet.
- **`/.well-known/agent.json` and `agents.md`** — emerging
  conventions for agent-facing site metadata. Shopify shipped both
  to all stores in May 2026. Worth tracking, not yet worth a
  generator script.
- **"Preferred Sources"** in Google AI Mode citations — personalised
  citation surface; rank-tracking becomes multi-persona. Not yet a
  generic tactic.
