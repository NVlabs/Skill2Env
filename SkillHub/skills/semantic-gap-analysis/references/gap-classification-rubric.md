# Gap Classification Rubric

The four-bucket taxonomy in Step 4 (Core / Differentiator / Commodity / Opportunity) is useful only if the decision criteria are concrete. Otherwise it becomes gut-feel, and two people running the skill on the same page get different briefs. This rubric makes the call mechanical.

Every gap you find in Step 3 runs through the same three questions:

1. **How many of the top 3 competitors cover it?**
2. **How deep is the coverage where it appears?**
3. **Does the gap correlate with ranking position?**

Those three answers map to one of four buckets.

## Core gap

**Criteria (all three must be true):**
- Present in all 3/3 top-ranking competitors.
- Treated as a material section in at least 2 of them (full H2 section, multi-paragraph treatment, or dedicated table/list — not a sentence in passing).
- Directly related to the primary target keyword's core intent, not a tangent.

**Action:** Must add. Highest priority. A core gap means Google has decided this topic is part of the answer to the query, and you're missing it. No amount of depth elsewhere compensates.

**Example:** Target keyword is "how to proof bread dough." All three top results have a section on "signs your dough is fully proofed" (poke test, volume change, spring-back). Your page explains how to proof but skips the how-to-recognize-it step. That's a core gap — without it, your page isn't actually answering the question.

## Differentiator gap

**Criteria:**
- Present in 1 or 2 of the 3 top competitors (not all three).
- The competitor(s) that cover it are ranking above the one that doesn't — i.e. the gap correlates with position.
- Treated at paragraph depth or better, not a one-liner.

**Action:** Add if scope allows. Medium priority. The signal here is that the gap is working for the competitors who include it. It's not mandatory for relevance, but it's pulling weight on ranking.

**Example:** Target keyword is "best TypeScript ORMs." Position 1 and position 2 both have a "runtime schema validation" section (Zod integration, TypeBox, Valibot). Position 3 skips it. You're pitching to TypeScript developers — this is exactly the audience that cares about runtime validation, and the ranking order suggests Google is rewarding the coverage. Add it.

## Commodity gap

**Criteria:**
- Present in all 3 competitors but shallow in all 3 (a sentence, a bullet, a single mention).
- Doesn't appear to correlate with ranking position — everyone covers it the same minimal way.
- Feels like a checkbox topic rather than a reason-to-read topic.

**Action:** Add briefly or skip. Low priority. The only reason to add a commodity gap is to avoid the "obvious omission" signal — if everyone mentions something once, a page that doesn't mention it at all looks incomplete. A single sentence is enough.

**Example:** Target keyword is "Stripe Connect vs Adyen." All three competitors have a single line noting "both support 3D Secure." No one expands on it. That's a commodity gap — add a sentence, don't build a section.

## Opportunity gap

**Criteria:**
- Present in 0 of the top 3 competitors.
- Relevant to the topic's entity space (passes the "would a domain expert expect this to be covered?" test).
- Has external signal that it matters: People Also Ask boxes, related searches, forum threads, or an obvious hole in the comparison axes.
- Contributes to Information Gain — the Google patent (US11769017B1) for ranking documents by the novel information they contribute to a query.

**Action:** Own this angle. This is your differentiation. Opportunity gaps are where you stop competing on coverage and start competing on insight. Treat them as the lead section if the gap is genuinely compelling.

**Example:** Target keyword is "best TypeScript ORMs." None of the top 3 cover "how each ORM handles schema drift in production migrations." PAA has "what happens when Prisma migrations fail in production." It's clearly relevant, clearly absent, and clearly what practitioners care about. That's your opportunity gap and probably your headline angle.

## Worked example: "best TypeScript ORMs" SERP

Hypothetical gap inventory from a real audit:

| # | Gap | 3/3? | Depth | Rank correlation? | Bucket |
|---|---|---|---|---|---|
| 1 | Prisma section | 3/3 | Full section all 3 | n/a | Core |
| 2 | Drizzle section | 3/3 | Full section all 3 | n/a | Core |
| 3 | TypeORM section | 3/3 | Full section all 3 | n/a | Core |
| 4 | Runtime schema validation (Zod, etc) | 2/3 | Subsection | Yes, top 2 have it | Differentiator |
| 5 | Edge runtime compatibility (Cloudflare Workers, Vercel Edge) | 1/3 | Subsection | Yes, the one has it is #1 | Differentiator |
| 6 | "ORM" vs "query builder" distinction | 3/3 | One sentence each | No | Commodity |
| 7 | License comparison (MIT vs Apache vs Elastic) | 0/3 | — | — | Opportunity |
| 8 | Schema drift handling in production migrations | 0/3 | — | PAA signal present | Opportunity |

Priority order for the rewrite:
1. Gaps 1–3 (core) — confirm we have full sections on Prisma, Drizzle, TypeORM. These are table stakes.
2. Gap 4 (differentiator) — add a subsection on runtime validation integration per ORM.
3. Gap 8 (opportunity) — lead with this if the PAA signal is strong. It's the headline angle.
4. Gap 5 (differentiator) — add a row to the comparison table on edge runtime support.
5. Gap 7 (opportunity) — include as a sidebar or footnote, lower value than gap 8.
6. Gap 6 (commodity) — one sentence in the intro acknowledging the ORM/query-builder line.

That's a brief. It tells the writer exactly what to add, in what priority, and at what depth.

## Edge case: commodity gaps that are actually opportunities in disguise

Sometimes you'll find a topic where all 3 competitors cover it shallowly, none go deep, and the shallowness itself is the opportunity. The criterion is: would deeper treatment serve the reader meaningfully better? If yes, promote it from commodity to opportunity.

**Example:** Target keyword is "how to choose a running shoe." All three top results say "consider your pronation" in a single sentence, none explain what pronation actually means or how to self-assess it. That's nominally a commodity gap — universal shallow coverage — but the shallowness is a failure of the SERP, not a signal that the topic doesn't matter. A page that adds a real pronation assessment guide turns a commodity gap into an opportunity gap and probably overtakes the SERP.

The test: if you can imagine a reader finishing the top 3 and still not knowing the answer to the subtopic, the subtopic is an opportunity, regardless of how many times it's mentioned. The count-based rules get you 90% of the way; this edge case covers the rest.

## When the rubric points both ways

Occasionally a gap looks like a core gap (present in 3/3) but all three treatments are shallow, so it also looks like a commodity gap. Call this a core-commodity gap: add it, but don't overbuild. A paragraph is enough. The rubric's goal isn't taxonomic purity — it's helping you decide how much effort to spend on each addition. Match the depth to the importance signal, and move on.
