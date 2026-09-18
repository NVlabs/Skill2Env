# Technique 01: Information Gain Writing

## What It Is
Writing content that adds genuinely NEW information compared to what already ranks for a keyword. Based on Google's Information Gain patent (granted June 2024), which scores how much additional value a page provides beyond existing search results.

## Why It Works
Google's algorithm compares your content against other pages the user has already seen on the same topic. Pages that say the same thing as the top 10 get low Information Gain scores. Pages that add unique data, perspectives, or insights get high scores — and rank higher.

The API leak confirmed this via `OriginalContentScore` — a separate metric that evaluates content uniqueness across the index.

**Algorithm reasoning:** If 10 pages all explain "how to do X" the same way, Google gains nothing by showing an 11th identical page. But if page 11 adds a case study, original data, or a contrarian perspective? That's information gain — value the user can only get from YOUR page.

## Step-by-Step Process

### Step 1: SERP Gap Analysis
1. Search the target keyword and read the top 10 results fully
2. Create a spreadsheet: rows = topics covered, columns = each competitor
3. Mark what each competitor covers and — critically — what they DON'T cover
4. Identify patterns: where do all 10 say the same thing? Where do they disagree?
5. Note the "missing angles": perspectives, data types, or use cases nobody addresses

### Step 2: Unique Value Identification
6. Ask: "What do I know about this topic that these 10 pages don't include?"
7. Sources of unique value:
   - **First-party data**: "We analyzed 500 customer accounts..."
   - **Original case studies**: "Client X tried this and here's what happened..."
   - **Expert interviews**: "I spoke with [Name], who said..."
   - **Contrarian perspective**: "Most guides say X. In our experience, Y works better because..."
   - **Process documentation**: "Here's the exact 9-step process we use internally..."
   - **Failure stories**: "We tried the common approach and it failed because..."
   - **Tool comparison**: "We tested 4 tools and measured actual results..."
8. Select 3-5 information gain elements to include

### Step 3: Content Architecture
9. Structure the article to lead with unique insights, not rehashed basics
10. Place information gain elements in the first 30% of the content (Google evaluates engagement early)
11. Use unique headings that signal novel content (not generic "What is X?" and "Benefits of X")
12. Plan specific data points, quotes, and examples for each section

### Step 4: Writing with Information Gain
13. Every section must answer: "What can the reader ONLY learn here?"
14. Replace generic statements with specific ones:
    - Bad: "Many companies have seen success with this approach"
    - Good: "We implemented this for 12 e-commerce clients in 2025. Average conversion improvement was 23%, but 3 clients saw no change — all in the B2B space"
15. Add "not found elsewhere" sections: edge cases, failure modes, advanced tips

## Hidden Tips & Tricks

- **The "So What?" test**: After every paragraph, ask "So what? Where can I ONLY read this?" If the answer is "anywhere," the paragraph has zero information gain.
- **Use your analytics**: Your GSC data, your customer data, your A/B test results — these are information gain goldmines that competitors literally cannot replicate.
- **Cite non-obvious sources**: Everyone cites HubSpot and Ahrefs. Cite academic papers, industry reports from niche organizations, or government data nobody else uses.
- **The 10-10-80 rule**: 10% covering basics (for context), 10% discussing what the competition says, 80% unique content. Most AI content is 80-10-10 — the opposite.

## Common Mistakes

1. **Thinking "more words" = information gain** — A 5,000-word article repeating the same points as competitors has zero information gain. A 1,500-word article with original data has high gain.
2. **Adding information gain at the end** — Google evaluates engagement early. Put unique insights in the first 500 words, not the conclusion.
3. **Fabricating data** — Never make up statistics for information gain. One fabricated stat that gets fact-checked destroys all credibility.
4. **Confusing "different format" with "different information"** — Putting the same information in a table instead of paragraphs isn't information gain.

## When to Use This Technique

- **Always** for competitive keywords (keyword difficulty > 30)
- For any content where you have access to unique data or experiences
- When updating content that lost rankings (likely lost due to competitors with higher information gain)
- Critical for pillar/hub content that anchors a topic cluster

## Algorithm Confirmation (from Google Leak)

The Information Gain patent (granted June 2024) explicitly describes the scoring system:

> "Information gain scores indicate how much more information one source may bring to a person who has seen other sources on the same topic. Pages with higher information gain scores may be ranked higher."

This means Google is not just comparing your page to competitors -- it's comparing it to pages the *specific user* has already seen in their search session. Returning to search after reading 3 similar articles? The 4th needs to add something NEW.

**Tools Used:**
- keyword search — identify target keyword landscape
- competitor data — analyze who ranks for this topic
- opportunity detection — find keywords where we rank 4-20
- SERP feature detection — identify featured snippet / PAA opportunities
- page-level SEO data — analyze current page performance if updating
