# Content Types Audit Summary

The page-audit skill loads this in Phase 0 once it's identified what type of page it's looking at. The audit lens is different for a pricing page than for a how-to, and applying the wrong lens produces a generic checklist. This file tells you which concerns actually matter per type.

## Quick reference table

| Content Type | Unique Audit Concerns | Required Schema | Common Failure Modes |
|---|---|---|---|
| **How-to / tutorial** | Visual per step, prerequisites section, specific error messages / versions, quick-answer paragraph front-loaded | HowTo + FAQ | Answer buried below intro, no screenshots, generic steps that could apply to anything |
| **Definition / "what is"** | First sentence IS the definition (no preamble), types/categories section, practical examples grounded in a specific market | DefinedTerm + FAQ | Circular definitions, jargon-first, missing "types of X" section, no local/market context |
| **Pillar page** | Table of contents, section-level self-containment, links out to cluster articles, scheduled updates | Article + FAQ | 5,000 words of shallow content, no cluster links, no ToC, treated as a one-time publish |
| **FAQ page** | Questions match real search language (PAA, GSC, support tickets), answers front-load the fact, logical grouping | FAQPage | Made-up questions, answers too long (200+ words) or too short, no grouping, duplicate of other pages |
| **Comparison (X vs Y)** | Verdict before scroll, consistent criteria applied to both, honest methodology section, pricing with gotchas | FAQ + Product (both items) | No upfront verdict, inconsistent criteria, missing methodology, one-sided pros |
| **Listicle / roundup** | Summary table above the fold, "best for X" differentiation per item, real drawbacks per item, documented evaluation process | ItemList + FAQ | Every item described equally positively, no methodology, 20+ items with no curation, outdated pricing |
| **Product review (single)** | First-person usage with dates, original screenshots, honest cons, current pricing, "who should skip this" section | Review + Product | Review of product the author never used (policy violation), all pros no cons, marketing-copy rewrite |
| **Product page (e-commerce)** | Unique copy (not manufacturer boilerplate), price visible, complete spec table, customer reviews, Product+Offer schema both populated | Product + Offer + AggregateRating | Manufacturer copy-paste, single image, hidden price, missing schema, no "who is this for" context |
| **Category page (e-commerce)** | Unique editorial above or below grid, faceted nav crawlability, breadcrumbs, duplicate content check against sibling categories | CollectionPage + ItemList + BreadcrumbList | No editorial, product-grid only, duplicate descriptions across categories, faceted URL bloat |
| **Pricing page** | Price visible without scrolling, recommended tier highlighted, complete feature comparison table, monthly/annual toggle, no hidden fees | Product + Offer (per tier) | "Contact sales" for all tiers, no comparison table, no FAQ handling billing questions, outdated prices |
| **Service page** | One service per page (not combined), clear process steps, pricing transparency or range, results with real numbers, strong above-fold CTA | Service + LocalBusiness (if local) + FAQ | Multiple services combined, generic differentiators, hidden pricing, no case study proof, CTA below fold |
| **Location page** | Genuinely unique content per location (not city-name swap), local case studies, NAP matches GBP, embedded map, location-specific info | LocalBusiness + Service + FAQ | Doorway pages (city-swap), NAP inconsistency, missing LocalBusiness schema, no local proof |
| **Case study** | Headline metric in H1, specific verifiable numbers with timeline, named client with permission, process transparency, before/after visuals | Article + Organization (client) | Vague results, no timeline, anonymous client, no process description, only-perfect outcomes |
| **About page** | Real team photos (not stock), named people with credentials, specific differentiators, linked LinkedIn profiles, Organization schema complete | Organization + Person (per team) | Stock photos, no named people, generic corporate values, 3,000 words of self-praise, no contact link |
| **Programmatic page** | Quality gate per page, unique value vs sibling pages, conditional template logic, hub-and-spoke internal linking, noindex threshold | Dataset / LocalBusiness / Product (depends) + BreadcrumbList | No quality gate, obviously templated text, same copy regardless of data values, orphaned pages |

## Per-type deep dive

The eight types below have the most distinct audit concerns. For the rest, the table above is enough.

### Product page (e-commerce)

Audit for three things in order: unique copy, price visibility, schema completeness. Unique copy is the most-failed dimension. If the product description reads identically to the manufacturer's site or any competitor selling the same SKU, you have a duplicate-content problem that on-page SEO can't rescue. Grep a sentence from the product description into Google and see how many hits come back. Ten+ means rewrite from scratch. Price visibility is the next most-failed: anything that requires scrolling, clicking, or a "request quote" flow costs you high-intent buyers. Schema completeness means `Product` + `Offer` + `AggregateRating` all populated with real data. Missing `Offer.availability` kills rich results even when the rest looks fine.

### Category page (e-commerce)

The audit tension here is the product grid vs. editorial content balance. Users came to browse, not to read, so a 2,000-word wall of text above the grid actively hurts. But Google needs unique content to distinguish this category from sibling categories selling 60% of the same products. The resolution: keep the editorial concise (300–1,000 words) and place most of it *below* the grid where it serves SEO without blocking UX. Second thing to audit: faceted navigation crawlability. Filters should refine the on-page list, but filter URLs shouldn't generate thousands of indexable thin pages. Run a quick `site:` search with a filter param and see how many variants Google has indexed.

### Pricing page

Three things determine whether a pricing page actually works: price visibility, trust signals near the price, and completeness of the feature comparison table. Price visibility is binary. Either the number is above the fold or you've already lost self-service buyers. The trust signals are where most pages fall short: money-back guarantee, customer count at each tier, "most popular" badge, short testimonial per plan. Product+Offer schema per tier is required for rich results in pricing queries. Common failure: a page with three beautiful pricing cards and no FAQ handling "what happens when I exceed my limit" or "can I switch plans." These are the #1 pre-purchase questions, and leaving them unanswered kills conversion more than the pricing itself.

### Location page (local / service area)

The single biggest audit question: is this a genuinely unique page or a doorway? The doorway test is brutal. Copy a paragraph from the target location page and paste it into a sibling location page (same service, different city). If the only substantive difference is the city name, Google treats it as a doorway and you risk a manual action. Genuine location pages have local case studies with photos, local pricing factors, local regulations, local response times: content only a business actually operating in that area would know. Secondary audit: NAP (Name / Address / Phone) must match the Google Business Profile character-for-character. Inconsistency torpedoes local pack rankings. Third: LocalBusiness schema with real geo coordinates. Missing this forfeits local pack eligibility.

### Case study

This is the page type where E-E-A-T Experience signals matter most and get audited hardest. The load-bearing element is a specific, verifiable metric in the H1 with a timeline attached. "142% more organic traffic in 6 months" passes; "significantly improved results" fails. The audit hunt: (1) Is the headline number in the H1 and above the fold? (2) Is there a named client (with permission) or a verifiable descriptor? (3) Is the process described in enough detail that a reader can evaluate the expertise, or is it "we did great work"? (4) Is there a timeline showing how long results took? Cases with no timeline are meaningless: results without duration could mean 2 weeks or 5 years. Vague case studies fail Dimension 3 scoring hard even when every other dimension is clean.

### About page

Google's Quality Raters specifically check About pages as an E-E-A-T signal, so this type gets audited through the E-E-A-T lens more than any other. Real team photos (not stock) is the first thing to verify. A single reverse-image search on the hero photo tells you. Named people with credentials relevant to what the business does comes second. "PhD in molecular biology" on a content marketing company is a red flag, not a green one. Third: specific differentiators with evidence. "15 years in renewable energy installations, certified by X" passes; "we care about quality" fails. The common over-failure mode: a 3,000-word self-congratulation essay. About pages should be 500–1,500 words of substance. Longer usually means less trustworthy, not more.

### Programmatic page

The audit question for programmatic content is always: does this page earn its index slot? Quality gates are non-negotiable: pages that don't have enough unique data to distinguish them from siblings should be noindexed, not published. Audit a programmatic page by looking at 3–5 sibling pages at the same time. If the template text is word-for-word identical and only the entity name changes, you're looking at thin content that will eventually get classified as doorway/low-value by Google's HCU classifier. The fix: conditional logic in the template so different data values produce substantively different text. Also audit hub-and-spoke linking. Orphan programmatic pages don't get crawled, which means they don't get indexed, which means the whole project was wasted.

### Pillar page

Pillar pages fail most often at one thing: they're written as comprehensive-essay rather than hub. A good pillar page covers each subtopic at overview depth (2–4 paragraphs) and links out to a dedicated cluster article for the deep dive. A bad pillar page tries to be the deep dive for everything simultaneously and ends up at 5,000 words of shallow summary. Audit: count the outbound links to cluster content. Fewer than 6–8 internal links to dedicated topic pages means it's not functioning as a hub. Second audit: is there a table of contents with anchor links? A 3,000+ word page without navigation is a bounce factory.

## Cross-reference

The full per-type content templates (with structure, word counts, schema, CTA placement, internal linking strategy, anti-AI focus) live in `write-content/references/content-types/`. Load those when the audit needs to recommend a restructure or rewrite, not when you're just scoring. For this audit skill, the summary above is sufficient to apply the right lens in Phase 0.
