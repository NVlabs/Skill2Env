# Publishing Sequence: When to Break the Spokes-First Rule

The SKILL.md default: publish 3-4 spokes first, then the hub, then the rest. This file covers the edge cases where that default is wrong.

## Why the default exists

If you publish an empty hub, it launches as a link-less orphan. It has nothing to link out to, and nothing linking back to it, so it accumulates no internal link equity. Publishing a handful of spokes first gives the hub something to reference on day one and gives you internal anchors pointing at it the moment it goes live.

That's the theory. In practice there are five situations where it doesn't hold.

## When to deviate

### 1. Brand-new domain with zero content

A site with no pages doesn't have the crawl budget to get 3-4 spokes indexed before the hub lands. You'll spend a month publishing spokes that aren't even in the index yet.

**Do this instead:** publish 1-2 spokes to establish the domain, then the hub, then scale. The point isn't to have mature spokes before the hub; it's to have *any* indexed content the hub can link to.

### 2. Site with existing content in the space

If the site already has 5-10 articles loosely in the topic area, don't treat this as a blank-slate cluster. Audit first. One of those articles may already function as a hub (broad intent, high traffic, ranks for the seed keyword), in which case you're *upgrading* the existing page and producing net-new spokes around it. Or an existing article may already function as a high-quality spoke, becoming row 1 of your spoke list so you skip writing that one.

**Do this instead:** audit existing URLs against the planned cluster before producing any new content. Publishing a fresh hub that competes with your own existing page is cannibalization.

### 3. Authoritative site with high crawl budget

On a site where Google crawls new URLs within hours (large publishers, established e-commerce, SaaS sites with strong domain signals), the multi-month drip doesn't serve a technical purpose. The whole point of sequencing is to give Google time to see the links form. If Googlebot is pulling new URLs within the same day, that's not a constraint.

**Do this instead:** publish the hub and the first batch of spokes in rapid succession, ideally within a single week, with the hub going live last or simultaneously. You still want the hub to launch with links pointing at it, but you don't need a month of delay to get there.

### 4. Time-sensitive topic

If the topic has a shelf life (a new product launch, a regulation change, a news cycle, a seasonal spike), publication speed beats architectural purity. A suboptimal cluster shipped in time to catch the search surge beats a perfect cluster shipped three weeks after the wave passed.

**Do this instead:** publish whatever you have ready first, hub or spoke, and fill in the rest as fast as you can. The cluster can be assembled retroactively. The search opportunity can't be.

### 5. Resource-constrained team

A solo operator or two-person team can't write 3-4 spokes in a month and still ship the hub in month 2. If you try to enforce the sequence on a team that doesn't have the throughput, you'll publish nothing for a quarter.

**Do this instead:** figure out which single piece has the biggest expected traffic (hub or spoke, doesn't matter) and ship that first. Ship the next one when it's ready. The cluster forms over time. Shipping nothing is worse than shipping out of order.

## Decision tree

Work through these in order. Stop at the first "yes."

1. **Does the topic have a hard deadline in the next 6 weeks?** → Ship fastest-ready piece first, ignore sequencing.
2. **Does the site already have a page ranking top-20 for the seed keyword?** → That's your hub. Don't publish a new one. Audit and upgrade, then publish net-new spokes around it.
3. **Can the team realistically ship 2+ pieces per month?** → No: ship highest-expected-traffic piece first, one per month. Yes: continue.
4. **Is the domain brand new (under ~50 indexed pages)?** → Ship 1-2 spokes, then the hub, then scale.
5. **Is the site well-indexed and crawled within hours of publication?** → Ship hub and first-batch spokes together in one week.
6. **None of the above?** → Default: 3-4 spokes in month 1, hub in month 2, remaining spokes months 3-4.

## Timeline expectations

For the default sequence on a mid-authority site:

- **Month 1-2:** First 3-4 spokes published. Indexation within days. Early rankings (positions 40-80) on long-tail queries.
- **Month 2-3:** Hub published, linked to the spokes. Hub shows up in the index within a week, ranks around 50-100 initially.
- **Month 3-6:** Remaining spokes published, each linking back to the hub. Hub climbs as it accumulates internal anchors. First spokes may reach top-20.
- **Month 6-12:** Cluster matures. Hub lands in top-20 on the seed keyword if competition allows. Topical authority shows up as the whole cluster lifting together, not just the hub.

These numbers assume a normal-authority domain. New domains are slower, established domains faster.

## Cross-reference

The general theory of hub-and-spoke clustering lives in [topic-cluster-strategy.md](./topic-cluster-strategy.md). That file explains *why* clusters work. This file is the operational decision layer: given that you've chosen to build a cluster, which order do you ship the pieces?
