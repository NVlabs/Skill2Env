# Technique 40: Programmatic SEO Pages

## What It Is
Template-driven pages generated at scale from structured data, targeting long-tail keyword patterns. Each page targets a specific variation of a repeating search pattern (e.g., "[service] in [city]", "[tool] for [industry]", "[metric] by [country]"). Quality gates are essential to avoid thin content penalties.

## When to Use
Informational/commercial intent -- user searches for a specific variation of a common pattern. Use when you have structured data that can populate hundreds or thousands of unique, genuinely useful pages. Only viable when each page provides real value beyond what a single page with filters could offer.

## Structure Template

```
H1: "[Dynamic Variable A] [Static Connector] [Dynamic Variable B]"
    (e.g., "Gemiddelde energieprijs in [Stad] -- [Jaar]")

Data summary section:
    Key metric or answer prominently displayed
    Comparison to national average or benchmark
    Last updated date

H2: [Variable A] in [Variable B]: overzicht
    3-5 sentences of template text with dynamic data points
    Must read naturally -- not obviously template-generated

H2: Key data / Statistics
    Table or data visualization with location/variable-specific data
    Sourced from your structured dataset

H2: How [Variable B] compares
    Comparison to similar entities (nearby cities, similar industries)
    Data table or chart

H2: Trends over time
    Historical data if available
    Chart showing change over time for this specific variable

H2: What this means for you
    Actionable interpretation of the data
    Template text with conditional logic based on data values

H2: Related pages
    Links to similar programmatic pages (nearby cities, related topics)
    Links to parent hub page

H2: Methodology
    Brief explanation of data source and update frequency
    Link to detailed methodology page
```

## Word Count
500-1,200 words per page (quality over quantity -- thin pages at scale create more problems than they solve)

## Schema Markup
- **Primary:** Depends on content type (Dataset, LocalBusiness, Product, Event)
- **Secondary:** BreadcrumbList (essential for large-scale site architecture)

## Featured Snippet Strategy
- **Format:** Table snippet for data-driven queries
- **Target:** The key data table or comparison table
- **Tip:** Structured data makes programmatic pages highly eligible for rich results

## CTA Placement
- After data summary: relevant tool, calculator, or comparison
- After "what this means": service page or conversion CTA
- End of page: parent category or related pages for continued browsing

## Internal Linking Strategy
- **Hub-and-spoke:** All programmatic pages link to a parent hub page
- **Sibling links:** Related pages link to each other (nearby cities, related categories)
- **Upward:** Link to pillar content for the broader topic
- **Receive links:** Hub page and blog content link to programmatic pages
- **Breadcrumbs:** Essential for helping search engines understand the hierarchy

## Key Success Factors
1. **Quality gates are essential:** Every page must pass a minimum quality threshold before indexing
2. **Unique value per page:** Each page must contain data or insight not available on other pages
3. **Natural language:** Template text must read naturally -- not like a mad-libs fill-in
4. **Conditional logic:** Different data values should trigger different text (not the same copy for all)
5. **Noindex thin pages:** Pages with insufficient data should be noindexed rather than published
6. **Internal linking structure:** Without proper hub-and-spoke linking, Google will not crawl thousands of pages
7. **Monitor for quality:** Regularly audit a sample of programmatic pages for quality degradation

## Common Mistakes
- **No quality gates:** Publishing thousands of thin, nearly-identical pages (Google penalty risk)
- Template text that reads obviously generated ("Welcome to our page about [city]")
- No conditional logic (same text regardless of whether data is high, low, or missing)
- Publishing pages with missing or insufficient data
- No internal linking strategy (orphaned programmatic pages will not get indexed)
- Not monitoring page quality over time (data changes can create broken or misleading pages)
- Scaling before validating (always test with 50-100 pages before generating thousands)

## Example Topics by Niche
- Energy: "Energieprijzen per gemeente -- [Stad]: gemiddeld tarief en vergelijking"
- Telecom: "Glasvezel beschikbaarheid [Postcode] -- providers en snelheden"
- SaaS: "[Tool] for [Industry]: features, pricing, and alternatives"
- E-commerce: "[Product categorie] prijzen in [Land] -- actueel overzicht"
- Local services: "[Vakman] in [Stad]: gemiddelde tarieven en beschikbare vakmensen"
