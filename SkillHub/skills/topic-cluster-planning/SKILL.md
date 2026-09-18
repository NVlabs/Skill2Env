---
name: topic-cluster-planning
description: Use when planning a topic cluster (hub + spokes) for a new content area. The agent researches the space, identifies the hub topic, maps the spokes, and produces a specific content plan with internal linking strategy.
---

# Topic Cluster Planning

Builds a hub-and-spoke architecture for a new content area. Hub = a broad pillar page that owns the topic. Spokes = specific articles that target long-tail keywords and link up to the hub. Done right, this signals topical authority to Google and concentrates link equity on the pages that matter.

## Input

**Seed topic or broad keyword** (required). Example: "email marketing", "keto diet", "small business accounting".

Optionally: your domain, so the agent can check what you've already published in this space.

## Role

You are a senior SEO content strategist specializing in topical authority architecture. You think in clusters, not individual articles.

## Step 1: Research the Topic Space

Google the seed topic. Read:
- The top 10 results for the broad keyword
- The People Also Ask questions
- The "Searches related to" at the bottom of the SERP
- 2-3 major publications in the space to see how they structure their content

Note:
- Who dominates the broad keyword? (This tells you the difficulty level.)
- What sub-topics emerge from PAA and related searches?
- What specific questions do people ask?

## Step 2: Identify the Hub

The hub is the one page that deserves to own the broad topic. It should:
- Target the broad/seed keyword directly
- Cover the topic comprehensively at a high level (don't go deep on every sub-topic)
- Link out to all the spoke articles

**Hub content type options:**
- **Ultimate guide** ("The Complete Guide to X") — best for broad informational topics
- **Pillar + chapters** (pillar page with a TOC linking to deep-dive chapters) — best for very broad topics with clear sub-chapters
- **Category page with curated featured content** — best for product/service topics

State your recommended hub format with reasoning.

## Step 3: Map the Spokes

From the PAA questions, related searches, and competitor coverage, identify 8-15 specific spoke topics. Each spoke should:
- Target a long-tail keyword or specific question
- Go deeper on one narrow sub-topic than the hub can
- Link back to the hub (primary)
- Link to 2-3 related spokes

For each spoke, specify:
- Target keyword / question it answers
- Content type (how-to / definition / comparison / case study / listicle)
- Approximate word count
- Why it matters for the cluster (what sub-topic does it own?)

**Rule of thumb:** a spoke should answer a question the hub can only summarize.

## Step 4: Map the Internal Linking

Draw the link graph:
- Every spoke links to the hub with a keyword-rich anchor
- Hub links to every spoke (usually in a "In this guide" TOC or a "Related deep dives" section)
- Related spokes link to each other (but sparingly — don't over-link)
- External links from the hub to 3-5 authoritative sources in the space

**Critical:** the first link from any spoke TO the hub is what Google's algorithm weights most heavily. Make sure it's contextual (within the article body), with a descriptive anchor text.

## Step 5: Publishing Order

Don't publish the hub first. Publish 3-4 high-quality spokes first, then the hub with links to them. Then publish the remaining spokes, each linking back to the now-established hub.

This prevents the hub from launching as a link-less orphan that has nothing to point to.

## Step 6: Output

### Cluster Overview
- Seed topic | Estimated difficulty (Easy / Moderate / Hard) based on SERP competition
- Realistic timeline to build out (how many articles, how many months)

### Hub
- Recommended format (Ultimate guide / Pillar + chapters / Category)
- Target keyword (the broad seed)
- Main H2 sections (roughly 5-10)
- Approximate word count
- What the hub should NOT cover in depth (save that for spokes)

### Spoke List

| # | Spoke Topic | Target Keyword | Content Type | Words | Hub Anchor Text |
|---|---|---|---|---|---|

8-15 rows. Sorted by priority: highest-impact/easiest-to-rank first.

### Publishing Sequence

1. **Month 1**: 3-4 spokes (pick from rows 1-4)
2. **Month 2**: Publish the hub, link it to the published spokes
3. **Month 3-4**: Remaining spokes, each linking back to the hub

### Internal Link Map
A simple list showing which spokes link to which other spokes. Not every spoke needs to link to every other — just the naturally related ones.

### External Linking Strategy
3-5 authoritative external sources the hub should cite. (Not competitors — actual authoritative sources: research papers, industry standards, government/university resources, or the primary creators of the concepts you're discussing.)

### Success Metrics
- **Month 3**: Hub should rank somewhere in top 50 for the seed keyword
- **Month 6**: At least 2-3 spokes ranking in top 20 for their long-tail keywords
- **Month 9**: Hub ranking top 20, cluster driving consistent organic traffic
- **Month 12**: Cluster becomes a topical authority signal for the whole domain

## What to Ignore

- **Publishing everything at once** — Google needs time to see the cluster form. Spread it over 3-4 months.
- **Over-linking between spokes** — if it doesn't feel natural in the article, skip it
- **Keyword density in the hub** — the hub is about breadth, not keyword stuffing

## Next Step

For each spoke, use `content-brief` with the spoke's target keyword to produce a writer-ready brief. Then `write-content` to write the article.

## Bundled references

Load from `references/` only when the step calls for them.

- **`first-link-weight-evidence.md`** — the evidence behind "the first link in the body is weighted most heavily" and why it matters for spoke → hub linking (Step 4, when briefing the writer on anchor placement)
- **`publishing-sequence-decisions.md`** — the full decision framework for "don't publish the hub first" and the exceptions (Step 5, when the user pushes back on the staggered launch)
- **`spoke-selection-worked-example.md`** — a full cluster worked end-to-end (seed → hub → 12 spokes → link map) for a sample niche, to anchor Step 3 when spoke selection feels arbitrary
- **`topic-cluster-strategy.md`** — the theory behind hub-and-spoke architecture and topical authority signals (background, optional)
- **`pillar-page-template.md`** — exact H1/H2 structure for the hub page (Step 2, after the hub format is chosen)
