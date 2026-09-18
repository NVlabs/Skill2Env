# Technique 10: Search Intent Matching

## What It Is
Writing content that matches the exact type of information a user expects when they search a keyword -- not just covering the topic, but delivering it in the FORMAT and DEPTH the user needs at that moment in their journey.

## Why It Works
Google's NavBoost system (confirmed by the 2024 API leak) tracks what happens after a user clicks a search result: do they stay, engage, and convert -- or do they bounce back to try another result? Content that mismatches intent causes pogo-sticking, which directly harms rankings.

The December 2025 Core Update doubled down on intent matching: pages optimized for the wrong intent dropped 30-90% regardless of content quality or domain authority.

## The Four Intent Types

### 1. Informational ("I want to learn")
- **Keywords**: "how to...", "what is...", "why does...", "guide to..."
- **User expectation**: Comprehensive answer, step-by-step instructions, explanations
- **Format**: Long-form articles, how-to guides, explainers, tutorials
- **Critical first 100 words**: Must signal "this page teaches you [exact topic]"
- **SEO signals**: HowTo schema, FAQ schema, table of contents

### 2. Commercial Investigation ("I want to compare")
- **Keywords**: "best...", "vs...", "review...", "top 10...", "comparison..."
- **User expectation**: Hands-on comparison, recommendations, honest assessment
- **Format**: Comparison tables, review articles, listicles with scoring
- **Critical first 100 words**: Must mention the things being compared and signal real testing
- **SEO signals**: Product schema, Review schema, comparison tables

### 3. Transactional ("I want to buy/do")
- **Keywords**: "buy...", "price...", "sign up...", "download...", "[product name]"
- **User expectation**: Clear pricing, easy purchase path, conversion-focused
- **Format**: Product pages, landing pages, pricing pages
- **Critical first 100 words**: Value proposition + CTA visibility
- **SEO signals**: Product schema, Offer schema, clear CTAs

### 4. Navigational ("I want to find a specific page")
- **Keywords**: "[brand name]", "[brand] login", "[product] pricing"
- **User expectation**: The exact page they're looking for
- **Format**: The actual page (homepage, login, pricing)
- **SEO signals**: Brand entity signals, sitelinks

## Step-by-Step Process

### Step 1: Intent Classification
1. Search the target keyword in Google
2. Look at the TOP 3 results -- Google has already classified intent
3. Note the content TYPE ranking: are they blog posts? Product pages? Comparison articles? YouTube videos?
4. If top 3 are all comparison articles and you write a how-to guide, you WILL NOT rank

### Step 2: Format Matching
5. Match the dominant format in the SERP:
   - All listicles -> write a listicle
   - All how-to guides -> write a how-to guide
   - Mix of formats -> the intent is fragmented; pick the one that aligns with your content type
6. Exception: if ALL top 10 use the same format, there's an opportunity to differentiate IF you still match intent (e.g., a video among all text results)

### Step 3: Depth Calibration
7. Measure competitor word counts for the top 5 results
8. Your content should match or slightly exceed the depth level
9. **But**: more words does not equal better depth. A 5,000-word article for "what time is it in Tokyo" is absurd. Match the COMPLEXITY of the intent.

### Step 4: First-100-Words Optimization
10. The first 100 words must immediately signal intent match
11. **Informational**: Answer the core question within the first paragraph, then expand
12. **Commercial**: Name the products/options being compared and establish credibility
13. **Transactional**: State the value proposition and make the CTA visible
14. Users who don't see intent match in 5 seconds bounce -- NavBoost penalizes this

### Step 5: Content Structure for Intent
15. Structure the article to match how users consume content for each intent:
    - **Informational**: TL;DR -> detailed sections -> summary/checklist
    - **Commercial**: Quick comparison table -> detailed reviews -> recommendation
    - **Transactional**: Benefit headline -> features -> social proof -> CTA
    - **Mixed**: Address primary intent first, secondary intents in supporting sections

## Content Length by Intent

Ahrefs found near-zero correlation (0.04) between word count and ranking. Match the SERP, not a word count target.

| Intent | Optimal Length | Rationale |
|--------|---------------|-----------|
| Informational (comprehensive guide) | 1,500-3,000+ | Needs to cover the full topic |
| Informational (specific question) | 800-1,500 | Answer directly, don't pad |
| Commercial investigation (comparison) | 1,200-2,500 | Depth in evaluation criteria |
| Commercial investigation (roundup) | 2,000-4,000 | Multiple items need coverage |
| Transactional | Minimal needed | No fluff; specs, pricing, CTA |
| Local service | 300-500 unique words | Must be genuinely unique per location |

**Key rule:** Match the SERP. If top 5 results average 2,000 words, write 2,000-2,500. If they average 800, writing 3,000 wastes effort and may signal wrong intent.

## Tips

- **Check "People Also Ask"**: These reveal the JOURNEY. If PAA for "best CRM" includes "is Salesforce worth it?" and "CRM pricing comparison," users are in commercial investigation -- not informational.
- **Search intent can shift**: "AI writing tools" in 2023 = informational ("what are they?"). In 2026 = commercial investigation ("which one should I use?"). Always verify current SERP, don't assume.
- **Mobile vs desktop intent**: The same keyword can have different intent on mobile (quick answer) vs desktop (deep research). Optimize for both, but prioritize based on traffic split.
- **Featured snippet = informational confirmation**: If Google shows a featured snippet, the intent is informational. Structure your content to capture it (direct answer in 40-60 words).

## Common Mistakes

1. **Writing a blog post for a transactional keyword**: "Buy running shoes" -> users want a product page, not a 2,000-word guide
2. **Writing a product page for an informational keyword**: "How to choose running shoes" -> users want guidance, not a buy button
3. **Ignoring mixed intent**: Some keywords have genuinely mixed intent. Your page must address the primary intent fully and nod to secondary intents
4. **Over-optimizing for one intent type**: Don't force transactional CTAs into informational content. It feels manipulative and users bounce.
