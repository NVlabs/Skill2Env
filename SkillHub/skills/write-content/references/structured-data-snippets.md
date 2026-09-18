# Technique 13: Structured Data & SERP Feature Capture

## What It Is
Using structured data (JSON-LD schema markup) and content formatting to capture SERP features -- featured snippets, FAQ dropdowns, How-To cards, and rich results that increase visibility, CTR, and NavBoost signals.

## Why It Works
SERP features occupy prime real estate above or within organic results. Pages with rich results get 20-40% higher CTR than plain blue links. Higher CTR feeds NavBoost (Google's click-based ranking signal), creating a compound ranking advantage.

Additionally, structured data is how content gets cited by AI Overviews and AI search engines. Without it, your content is less likely to be selected as a source for AI-generated answers.

## SERP Features by Content Type

| Content Type | Target SERP Features | Schema Types |
|-------------|---------------------|-------------|
| Blog post | Featured snippet, PAA | Article, FAQPage |
| How-to guide | HowTo card, Featured snippet | HowTo, FAQPage |
| Product page | Product rich result, Review stars | Product, Review, Offer |
| FAQ page | AI Overview citation, PAA | FAQPage |
| Comparison | Comparison table, Review stars | Article, Product, Review |
| Recipe | Recipe card | Recipe |
| Event | Event listing | Event |
| Local business | Local pack, Knowledge panel | LocalBusiness |

## Step-by-Step Process

### Step 1: Identify Feature Opportunities
1. Use SERP feature detection from to see which features appear for target keywords
2. Search the keyword manually -- what features are currently showing?
3. Note: featured snippets, PAA boxes, HowTo cards, video carousels
4. Check if any competitor has a SERP feature you could capture

### Step 2: Content Formatting for Featured Snippets
5. **Paragraph snippets** (most common):
   - Place a direct answer in 40-60 words immediately after an H2 matching the query
   - Start with the definition/answer, then expand
   - Example: "What is information gain?" -> H2 -> 45-word direct answer -> detailed explanation
6. **List snippets**:
   - Use numbered or bulleted lists with clear H2 header
   - 5-8 items is optimal
   - Each item should be a clear, scannable point
7. **Table snippets**:
   - Use HTML tables with clear column headers
   - 3-5 columns, 4-10 rows
   - Comparison data is ideal for table snippets

### Step 3: FAQ Schema Implementation
8. Identify 3-5 questions users ask about the topic (use PAA boxes as source)
9. Include each question as an H2 or H3
10. Answer directly in 40-100 words
11. Implement FAQPage schema with each Q&A pair:
   ```json
   {
     "@context": "https://schema.org",
     "@type": "FAQPage",
     "mainEntity": [{
       "@type": "Question",
       "name": "What is information gain in SEO?",
       "acceptedAnswer": {
         "@type": "Answer",
         "text": "Information gain in SEO measures how much new, unique information your content provides compared to other pages on the same topic. Google's patented Information Gain Score rewards pages that add original data, perspectives, or insights not found in competing results."
       }
     }]
   }
   ```

### Step 4: HowTo Schema
12. For tutorial/guide content, implement HowTo schema:
    - Each step as a separate `HowToStep`
    - Include `estimatedCost` and `totalTime` when applicable
    - Add `tool` and `supply` arrays
    - Include images per step when possible

### Step 5: Article/Product Schema
13. **Article schema** (for blog posts, guides):
    - `author` with name and URL
    - `datePublished` and `dateModified`
    - `image` (required for rich results)
    - `headline` matching H1
14. **Product schema** (for product/review pages):
    - `offers` with price, availability, currency
    - `review` with `ratingValue` and `bestRating`
    - `brand` entity

### Step 6: Validation
15. Test all structured data with Google's Rich Results Test
16. Monitor Search Console for structured data errors
17. Verify rich results appear in SERPs after indexing

## Tips

- **PAA as keyword research**: "People Also Ask" questions are literally Google telling you what related queries users search. Answer them in your content -> PAA placement and AI Overview citations.
- **Featured snippet "sniping"**: Find a keyword where the current featured snippet is mediocre. Write a better, more direct answer in the same format. Google swaps snippets regularly.
- **Don't over-schema**: Adding 50 FAQ items or marking up content that doesn't qualify for a schema type can trigger manual actions. Only mark up content that genuinely matches the schema type.
- **AI Overview sourcing**: Structured data helps your content get selected as a source for AI Overviews. Content with clear schema markup is easier for AI systems to parse and cite.

## Common Mistakes

1. **FAQ schema for non-questions**: Only use FAQPage schema for actual Q&A content. Using it for bullet points or regular content is a misuse.
2. **Missing required fields**: Schema without required fields (like `image` for Article) won't generate rich results
3. **Duplicate schema**: Having both FAQPage and HowTo on the same page can conflict. Choose the primary schema type.
4. **Not monitoring**: Structured data can break (especially after CMS updates). Monitor Search Console regularly.

## GEO (AI Citation) Impact

Structured data directly impacts AI citation rates:
- **FAQ schema has 3.2x higher citation rate** in AI Overviews
- **92% of AI Overview citations** come from top-10 ranking pages -- SERP features help you get there
- **Answer-first formatting** (40-60 word direct answers under H2s) produces +340% AI citations
- Content with clear schema markup is easier for AI systems to parse and cite

Write comprehensive content (for Google) with clear, extractable summary answers at the start of each section (for AI). The overlap between SERP feature optimization and AI citation optimization is ~80%.

## Tools Used
- SERP feature detection -- identify which features appear for target keywords
- keyword search -- find keywords with featured snippet opportunities
- page-level SEO data -- check current SERP feature status for existing pages
