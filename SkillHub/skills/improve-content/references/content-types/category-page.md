# Technique 32: E-Commerce Category Pages

## What It Is
Navigational/commercial content that organizes products within a category, combining product listings with SEO-optimized category descriptions. The primary landing page for category-level searches. Captures "[category]", "[category] kopen", and "[category] vergelijken" searches.

## When to Use
Commercial/navigational intent -- user wants to browse options within a product category. Every product category and meaningful subcategory needs its own page. These pages often rank for high-volume head terms.

## Structure Template

```
H1: "[Category Name]"
    (e.g., "Zonnepanelen" or "Draadloze Koptelefoons")

Category intro (above product grid):
    2-3 sentences: what the category includes, key buying criteria
    Filter/sort options prominent

Product grid / listing:
    Product cards: image, name, price, rating, key spec
    Filterable by: price, brand, rating, key attributes
    Sortable by: price, popularity, rating, newest

H2: [Category] koopgids (below product grid)
    3-5 paragraphs of unique, helpful category content
    Key criteria for choosing within this category
    Links to buying guide, comparisons, reviews

H2: Popular subcategories
    Links to subcategory pages with brief descriptions

H2: Veelgestelde vragen over [category]
    3-5 FAQ items specific to the category

H2: Related categories
    Cross-links to adjacent categories
```

## Word Count
300-1,000 words of unique content (excluding product listings -- the content supplements, not replaces, the product grid)

## Schema Markup
- **Primary:** CollectionPage (with name, description)
- **Secondary:** ItemList (for the product listing with ListItem entries)
- **Tertiary:** BreadcrumbList (for navigation hierarchy)

## Featured Snippet Strategy
- **Format:** List snippet for "types of [category]" queries
- **Target:** The subcategories section or a bulleted list of product types
- **Alternative:** Paragraph snippet for "what are [category]" queries via the intro text

## CTA Placement
- **Primary:** Product cards with "bekijk" or "add to cart" per product
- Filters and sorting: prominent, easy to use (improves engagement signals)
- After category description: link to buying guide or comparison tool
- Above fold: featured/promoted products or current deals

## Internal Linking Strategy
- **Upward:** Link to parent category via breadcrumbs
- **Downward:** Link to subcategory pages and individual product pages
- **Sideways:** Link to related categories
- **Supporting:** Link to buying guide, comparison articles, and how-to content
- Receive links from pillar pages, navigation, and blog content

## Key Success Factors
1. **Unique category content:** Do not rely solely on product listings -- add editorial content
2. **Faceted navigation done right:** Filters must be crawlable but not create duplicate URL bloat
3. **Above-the-fold products:** Product listings must be visible without scrolling past a wall of text
4. **Breadcrumb navigation:** Clear hierarchy for both users and search engines
5. **Pagination or load-more:** Handle large catalogs without harming crawlability
6. **Category-specific filters:** A koptelefoon page filters on noise cancelling; a zonnepaneel page filters on wattage

## Common Mistakes
- No unique content (just a product grid with no editorial value)
- Too much content above the product grid (users came to browse products)
- Duplicate content across similar category pages
- Faceted navigation creating thousands of indexable thin pages
- Missing breadcrumbs (confuses both users and crawlers)
- No internal links to supporting content (buying guides, how-tos)
- Broken pagination or infinite scroll that search engines cannot crawl

## Example Topics by Niche
- Energy: "Zonnepanelen -- vergelijk en koop bij de beste aanbieders"
- Telecom: "Sim only abonnementen -- vergelijk alle providers"
- SaaS: "SEO Tools -- vergelijk de beste SEO software"
- E-commerce: "Draadloze koptelefoons -- bekijk ons assortiment"
- Local services: "Schilders in Amsterdam -- bekijk en vergelijk vakmensen"
