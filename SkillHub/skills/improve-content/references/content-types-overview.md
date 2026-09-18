# Content Types Overview

Quick-reference index covering all 23 content-type templates. Use this file to pick the right content type for a SERP, check its target word count, dominant schema, snippet format, and H1/H2 skeleton without loading the full per-type file. Load the individual `content-types/<type>.md` only when you need the depth (process detail, anti-AI focus, common mistakes, example topics).

## Decision table

| Content type | Dominant intent | Word count | Primary schema | Snippet format | H1 pattern | Key H2s (first 3-4) |
|---|---|---|---|---|---|---|
| how-to | Informational | 1,500-3,000 | HowTo + FAQ | Ordered list | "How to [Action] [Qualifier]" | Quick answer / Prerequisites / Step-by-step / Common mistakes |
| definition | Informational | 1,000-2,000 | DefinedTerm + FAQ | Paragraph | "What Is [Term]? [Subtitle]" | Quick definition / How it works / Types / Benefits |
| pillar-page | Informational + navigational | 3,000-5,000+ | Article + FAQ | Paragraph (list per section) | "The Complete Guide to [Topic] [Year]" | Table of contents / Overview / Core subtopics / Practical steps |
| faq-page | Informational | 1,500-2,500 | FAQPage + BreadcrumbList | Paragraph (per Q) | "[Topic] FAQ: Veelgestelde vragen over [topic]" | Intro / Category 1 / Category 2 / Costs |
| statistics | Informational | 2,000-3,500 | Article + Dataset | List | "[Topic] Statistics [Year]: [X] Key Facts and Trends" | Key highlights / Category stats / Regional data / Trends |
| news | Informational + navigational | 800-1,500 | NewsArticle + FAQ | Paragraph | "[News event]: [Impact or what it means]" | Key takeaways / What happened / Why it matters / What to expect |
| thought-leadership | Informational | 1,200-2,500 | Article + Person | Paragraph (low priority) | "[Strong opinion or provocative question]" | Conventional wisdom / Why it's wrong / Supporting arguments / Counterarguments |
| glossary | Informational | 5,000-15,000 (200-400/term) | DefinedTermSet + BreadcrumbList | Paragraph (per term) | "[Industry] Woordenlijst: [X] Begrippen Uitgelegd" | Intro / A / B / C ... |
| comparison | Commercial investigation | 1,200-2,500 | FAQ + Product | Table | "[Product A] vs [Product B]: [Outcome promise]" | Quick verdict / At-a-glance table / How we compared / Head-to-head |
| listicle | Commercial investigation | 2,000-4,000 | ItemList + FAQ | List | "Best [Category] for [Audience/Use Case] in [Year]" | Top picks at a glance / How we evaluated / 1. Top pick / 2. Second pick |
| alternatives | Commercial investigation | 1,500-3,000 | ItemList + FAQ | List | "[X] Alternatieven: [N] Beste Opties in [Year]" | Why look for alternatives / Comparison table / Alternative 1 / Alternative 2 |
| product-review | Commercial investigation | 1,500-2,500 | Review + Product | Paragraph | "[Product] Review [Year]: [Honest verdict]" | Quick verdict / What is [Product] / Our experience / Pros |
| buying-guide | Commercial investigation | 2,000-3,500 | Article + FAQ | List | "[Category] Kopen: Waar Moet Je Op Letten?" | Quick checklist / Criterion 1 / Criterion 2 / Budget guide |
| product-page | Transactional | 1,000-1,500 | Product + Offer + AggregateRating | Product rich result | "[Product Name] — [Key Differentiator]" | Description / Features and specs / What's included / Who is this for |
| category-page | Commercial + navigational | 300-1,000 (editorial) | CollectionPage + ItemList | List | "[Category Name]" | Intro / Product grid / Koopgids / Subcategories |
| landing-page | Transactional | 800-1,200 | WebPage or Service + FAQ | Not primary | "[Clear value proposition in one line]" | Problem statement / Solution / How it works / Social proof |
| pricing-page | Transactional | 500-1,500 | Product + Offer | Table | "Prijzen" or "[Product] Pricing" | Pricing tiers / Feature comparison table / Which plan / What's included |
| integration-page | Commercial + navigational | 800-1,500 | SoftwareApplication + HowTo | List | "[Your Product] + [Partner Tool] Integratie" | What it does / Key features / How to set it up / Use cases |
| service-page | Commercial + transactional | 1,200-2,000 | Service + LocalBusiness + FAQ | List | "[Service Name] — [Key Benefit or Location]" | What we do / Who this is for / How it works / Deliverables |
| location-page | Local + transactional | 1,200-1,500 | LocalBusiness + Service + FAQ | Paragraph | "[Service] in [Location]" | Local context / Services in [Location] / Why choose us / Recent projects |
| case-study | Commercial investigation | 1,500-2,500 | Article + Organization | Paragraph | "[Client/Industry]: [Key Result in Numbers]" | Overview / The challenge / Our approach / The results |
| about-page | Navigational + trust | 500-1,500 | Organization + Person | Knowledge Panel (not snippet) | "Over [Brand]" or "About [Brand]" | Mission / Our story / Our team / Expertise |
| programmatic-page | Informational + commercial | 500-1,200 | Depends on type + BreadcrumbList | Table | "[Variable A] [Connector] [Variable B]" | Data summary / Key data / How [B] compares / Trends over time |

## Intent → content type mapping

Search intent is the primary filter. Pick based on what the top 5 SERP results are actually doing, not what you think they should be doing.

**Informational.** User wants to understand something. Not buying yet.
- "how to [x]" / "[x] tutorial" → how-to
- "what is [x]" / "[x] meaning" → definition
- "[topic] explained" / "guide to [topic]" → pillar-page
- "[topic] questions" / PAA cluster → faq-page
- "[topic] statistics" / "[topic] data [year]" → statistics
- "[term] vocabulary" / 30+ terms in niche → glossary
- "[event] [year]" / breaking topic → news
- "why [industry belief]" / contrarian query → thought-leadership

**Commercial investigation.** User is shopping but hasn't picked a product.
- "best [category] for [audience]" → listicle
- "[A] vs [B]" → comparison
- "[product] alternatives" → alternatives
- "[product] review" → product-review
- "[category] buying guide" / "what to look for in [x]" → buying-guide
- "[service] results" / "[industry] case study" → case-study

**Transactional.** User is ready to convert.
- "[product name]" / "[product] kopen" → product-page
- "[product] pricing" / "[product] kosten" → pricing-page
- "[service] aanvragen" / "[tool] free trial" → landing-page
- "[service] inhuren" / "[service] kosten" → service-page
- "[tool A] + [tool B] integration" → integration-page
- "[service] in [city]" / "[service] near me" → location-page

**Navigational + trust.** User is verifying who you are.
- "[brand] about" / "who is behind [brand]" → about-page
- "[category]" root browse → category-page
- Long-tail pattern at scale with structured data → programmatic-page

Note: several content types span two intent classes. Pillar pages are informational but also navigational (hub for the cluster). Category pages are commercial but also navigational (people type the category name to browse). Pick the dominant intent, but don't be surprised when a page has to satisfy both.

A few more overlaps worth flagging. Integration pages and category pages both straddle commercial and navigational. Programmatic pages can skew either informational or commercial depending on the variable. Service pages are commercial in SERP but behave like transactional once the visitor lands.

## When to load the full per-type file

The decision table gives you enough to pick the type and draft the skeleton. Load the full `content-types/<type>.md` when:

- **pillar-page**: you need the hub-and-spoke linking architecture, the visual-break rhythm (image/table every 300-500 words), and the regular-update cadence rules. The overview doesn't capture the "every cluster article links back" rule, which is the whole point of the pattern.
- **comparison**: you need the full 10-section framework, especially the "verdict first per criterion" rule at the H3 level. Comparison articles fail hard if you just know the H2 skeleton.
- **how-to**: you need the quick-answer targeting (40-60 words, ordered list after the most relevant H2) and the step-by-step "one action per step" constraint. The anti-AI section on error messages and version numbers is the highest-signal part.
- **case-study**: you need the PAS-adjacent structure (challenge → approach → results → takeaways) and the "lead with the number in H1 and first 50 words" rule. The overview skips the client-permission and visual-proof requirements.
- **product-review**: you need the "who should skip" framing and the Google review-update requirements around hands-on evidence.
- **programmatic-page**: you need the quality-gate logic (noindex thin pages, conditional template copy, sibling linking). Shipping programmatic without reading the full file gets you penalized.
- **listicle**: you need the "methodology section + updated quarterly" rule and the 7-10 item sweet spot.
- **glossary**: you need the A-Z navigation pattern, anchor-link scheme, and the cross-reference style between terms.
- **location-page**: you need the doorway-page warning. Location pages without genuinely unique per-city content get penalized. The overview doesn't make this loud enough.

For everything else the overview table is usually enough to draft the first pass. Go deeper if the draft feels generic or if you're unsure about a specific structural element.

## Cross-reference: YMYL-sensitive types

YMYL ("your money or your life") topics trigger elevated E-E-A-T and Trust scrutiny from Google's quality raters. The content types that live closest to YMYL need named authors, visible credentials, transparent methodology, and verifiable evidence. That list: **pricing-page**, **service-page**, **product-review** (Google's review update explicitly targets this type), **case-study**, **about-page** (the page raters read to assess the whole site's trust), **thought-leadership**, and any **news** article about health, finance, legal, or safety topics. For these, skip stock photos, add real author bylines with linked credentials, include dated evidence (screenshots, numbers, timelines), and publish visible update logs. If you're writing in a regulated niche (medical, financial advice, legal), the Trust bar is higher than any of the per-type files capture. Add a subject-matter expert reviewer byline and cite primary sources (regulators, peer-reviewed studies) rather than secondary blogs.

## Word count targets by intent

The overriding rule: match the average word count of the top 5 ranking results, then add roughly 10%. Don't pad to hit a number. Don't under-write to stay "concise" when the SERP is hungry for depth.

| Intent class | Typical range | Rule of thumb |
|---|---|---|
| Informational (simple) | 800-1,500 | Match SERP average; news and short definitions fall here |
| Informational (deep) | 1,500-3,500 | How-to, statistics, FAQ, buying guide: depth signals expertise |
| Informational (hub) | 3,000-5,000+ | Pillar pages only; every section earns its place |
| Commercial investigation | 1,200-3,000 | Comparison, listicle, alternatives, review: enough to build confidence before conversion |
| Transactional | 500-1,500 | Pricing, product, landing, integration: short and scannable, conversion over coverage |
| Trust / navigational | 500-1,500 | About, category: authentic over long, unique content over padding |
| Programmatic at scale | 500-1,200 per page | Quality gates first; noindex anything thin |

When the SERP has mixed formats (one pillar, three listicles, one FAQ), write for the dominant format but cover the angles the minority formats introduce. If the top 5 are all 3,500 words and yours is 1,200, you're not competing. You're just hoping.

## Related reference files

If you need the underlying methodologies rather than the content-type skeletons, load these from the same `references/` directory:

- `intent-matching.md`: the full intent-classification logic and SERP-reading playbook
- `serp-driven-writing.md`: how to read the top 5 and extract the winning format
- `structured-data-snippets.md`: the full schema-markup catalog with examples
- `anti-slop-ruleset.md`: the banned-vocabulary list and structural tells
- `voice-injection-playbook.md`: how to inject first-person experience into any type
- `eeat-signal-embedding.md`: where and how to place author, credentials, and evidence
