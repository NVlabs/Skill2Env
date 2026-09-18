# Spoke Selection: A Worked Example

Going from a raw SERP scrape to a finished spoke list. SKILL.md tells you *what* to do. This shows *how* it looks when you do it.

## Seed topic

**Email marketing for SaaS.** Moderate difficulty, rich PAA, strong commercial intent. The seed SERP is dominated by long-form guides from Customer.io, Encharge, HubSpot, and a couple of marketing blogs.

## Step 1: Raw SERP scrape

Pull everything Google offers: PAA, Related Searches, "People also search for," and the H2s of the top 5 ranking guides. Don't filter yet, just capture.

Raw question list:

1. What is email marketing for SaaS?
2. How is SaaS email marketing different from e-commerce email?
3. Best email marketing tools for SaaS companies?
4. What email sequences should a SaaS company send?
5. What is a SaaS onboarding email sequence?
6. How do you write a welcome email for SaaS?
7. What is a trial conversion email?
8. How do you reduce churn with email?
9. What is a win-back email campaign?
10. What KPIs should SaaS email marketers track?
11. How often should a SaaS company email its users?
12. What is product-led email marketing?
13. Should SaaS companies use newsletters?
14. What is a lifecycle email campaign?
15. How do you segment a SaaS email list?
16. What are transactional emails in SaaS?
17. How do you avoid the spam folder for SaaS emails?
18. What is the average open rate for SaaS emails?

That's 18 raw queries. The goal is 8-10 non-overlapping spokes. Overlap is the enemy: two spokes that both answer "how do I write good onboarding emails" will cannibalize each other.

## Step 2: Cluster by semantic overlap

Group questions that belong to the same answer. If two questions share the same underlying intent and would be answered by the same article, fold them.

**Cluster A: Foundational / definition**
- 1 (What is email marketing for SaaS?)
- 2 (SaaS vs e-commerce email)
- 12 (Product-led email marketing)

These answer "what is this and how is it different?" They belong in the hub's intro, not in a spoke.

**Cluster B: Lifecycle and sequences**
- 4 (What sequences should SaaS send?)
- 5 (Onboarding sequence)
- 6 (Welcome email)
- 14 (Lifecycle email campaign)

4 and 14 both map the lifecycle. 5 and 6 are the first touches. Fold into two spokes: the full lifecycle map, and onboarding specifically.

**Cluster C: Conversion / revenue**
- 7 (Trial conversion email)
- 8 (Reduce churn with email)
- 9 (Win-back campaign)

Three distinct lifecycle moments, each large enough for its own spoke. If resource-constrained, 8 and 9 could fold into one "retention and win-back" piece.

**Cluster D: Operations and deliverability**
- 10 (KPIs to track)
- 11 (Send frequency)
- 17 (Avoiding spam folder)
- 18 (Average open rate)

10 and 18 overlap (both metrics). 17 is deliverability. 11 is cadence. Three spokes at most.

**Cluster E: Tools and stack**
- 3 (Best tools)
- 16 (Transactional email in SaaS)

3 is a commercial-intent comparison and becomes a spoke. 16 is technical and mostly answered on product docs, so it becomes an FAQ on the deliverability spoke.

**Cluster F: Segmentation and list management**
- 13 (Newsletters for SaaS?)
- 15 (How to segment a SaaS list)

15 is a standalone spoke. 13 is an opinion piece; fold it into the lifecycle spoke as a section.

## Step 3: Prioritize by difficulty and traffic potential

For each candidate spoke:

- **Difficulty:** who ranks top 10? All DR 80+ domains means 6-12 months to crack the top 20. A DR 40-60 spread is more achievable.
- **Traffic potential:** primary keyword volume plus the related long-tail terms riding along.

Rank highest-value first:

1. SaaS onboarding email sequence (high intent, mid difficulty)
2. SaaS email marketing tools comparison (high intent, high difficulty)
3. Trial-to-paid conversion email sequence (high intent, mid difficulty)
4. Reducing SaaS churn with email (high intent, mid difficulty)
5. SaaS email KPIs and benchmarks (moderate intent, low difficulty, evergreen)
6. SaaS customer lifecycle email map (moderate intent, high topical value)
7. Email list segmentation for SaaS (moderate intent, low-mid difficulty)
8. SaaS email deliverability guide (technical, mid difficulty, long shelf life)
9. Win-back email campaigns for SaaS (lower volume, low difficulty)
10. SaaS email send frequency and cadence (low volume, easy ranks)

That's 10 spokes. Good number.

## Step 4: Hub vs spoke classification

Not all of the 18 raw questions become articles. Some are too broad (those belong in the hub). Some are too narrow (those become FAQs inside an existing spoke).

**Hub-level** (broad, foundational, lives inside the hub):
- 1, 2, 12: the "what is SaaS email marketing and how is it different" questions

**Spoke-level** (specific, standalone article):
- The 10 listed above

**FAQ-level** (too narrow for its own article, folds into a parent):
- 13 (newsletters) → into the lifecycle spoke
- 16 (transactional email) → FAQ inside deliverability spoke
- 18 (average open rates) → subsection of the KPIs spoke

## Step 5: Final spoke map

| # | Spoke Topic | Target Keyword | Content Type | Words | Answers Question |
|---|---|---|---|---|---|
| 1 | SaaS Onboarding Email Sequence | saas onboarding email sequence | How-to + template | 2,500 | #5, #6 |
| 2 | Best Email Marketing Tools for SaaS | email marketing tools for saas | Comparison | 3,500 | #3 |
| 3 | Trial-to-Paid Conversion Emails | trial conversion email | How-to + examples | 2,000 | #7 |
| 4 | Reducing SaaS Churn With Email | reduce saas churn with email | Strategy guide | 2,500 | #8 |
| 5 | SaaS Email KPIs and Benchmarks | saas email marketing kpis | Listicle + data | 2,000 | #10, #18 |
| 6 | SaaS Customer Lifecycle Email Map | saas lifecycle emails | Framework article | 3,000 | #4, #14, #13 |
| 7 | Segmenting a SaaS Email List | saas email segmentation | How-to | 1,800 | #15 |
| 8 | SaaS Email Deliverability Guide | saas email deliverability | Technical guide | 2,800 | #17, #16 |
| 9 | Win-Back Email Campaigns for SaaS | saas win-back email | How-to + examples | 1,800 | #9 |
| 10 | How Often Should SaaS Companies Email Users | saas email frequency | Short opinion + data | 1,200 | #11 |

Total cluster: 1 hub + 10 spokes, roughly 23,000 words of new content.

## Step 6: Internal link graph

Every spoke links back to the hub. Beyond that, only link between spokes when the connection is *natural*. Don't force cross-links.

```
HUB: Complete Guide to SaaS Email Marketing
  |
  +-- 1. Onboarding Sequence --> 2, 6
  +-- 2. Tools Comparison --> 1, 8
  +-- 3. Trial Conversion --> 1, 6
  +-- 4. Reducing Churn --> 6, 9
  +-- 5. KPIs and Benchmarks --> 8
  +-- 6. Lifecycle Map --> 1, 3, 4, 9
  +-- 7. List Segmentation --> 6
  +-- 8. Deliverability --> 5, 2
  +-- 9. Win-Back --> 4, 6
  +-- 10. Email Frequency --> 5
```

Spoke 6 (the lifecycle map) is the center of the graph: most spokes link to it naturally. That's a sign 6 is doing real work as a connective piece. If no spoke naturally links to another, the cluster is probably too fragmented: you're building ten unrelated articles, not a cluster.

## Rejected questions: what to do with them

Some of the 18 didn't make the spoke list. They still have value:

- **Fold as FAQ sections:** "Do I need a newsletter?" works well as an H2 Q-and-A inside spoke 6. Captures long-tail impressions without diluting the main content.
- **Hold for future expansion:** some questions are worth a spoke later, once the cluster has proven it can rank. "Email marketing for PLG vs sales-led SaaS" is a legitimate spoke 11 once the core 10 are live.
- **Drop entirely:** questions too narrow to sustain an article, or already well-covered by an obvious primary source. Don't force a spoke for the sake of the number.

## Cross-reference

Once you've got a spoke list like this, feed any single row into the `content-brief` skill with the target keyword. That produces a writer-ready brief for that specific spoke. Spoke selection happens once per cluster; content-brief happens once per article.
