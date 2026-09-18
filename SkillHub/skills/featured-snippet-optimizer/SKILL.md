---
name: featured-snippet-optimizer
description: Use when you want to win a featured snippet for a keyword you already rank for. The agent checks the current snippet format, analyzes your content, and rewrites the relevant section to match what Google wants.
---

# Featured Snippet Optimizer

Featured snippets get 42.9% CTR versus 39.8% for organic #1 without a snippet ([First Page Sage 2026 CTR study](https://firstpagesage.com/reports/google-click-through-rates-ctrs-by-ranking-position/)). If you're ranking positions 1-5 and NOT holding the snippet, you're leaving clicks on the table. This skill finds the gap and fixes it.

## Input

- **Target keyword** (required)
- **Your page URL** that already ranks for this keyword (required)

If you don't know your current position, tell the user: featured snippet optimization only works for pages ranking positions 1-5. From position 6+, fix the ranking first, then target the snippet.

## Role

You are a senior SEO specialist with deep knowledge of featured snippet mechanics. You know that Google picks snippets algorithmically from the top 10, and the format you write in matters more than content quality for this one job.

## Step 1: Check the Current Snippet

Google the target keyword. Observe:
- Is there a featured snippet at all?
- If yes: which domain holds it? Your domain or a competitor?
- What format is it? Paragraph / ordered list / unordered list / table
- What's the exact text of the snippet?

If there's NO featured snippet at all, that's actually good news — the slot is up for grabs.

## Step 2: Classify the Query Format

Google uses format matching. The query type dictates the snippet format:

| Query type | Snippet format | Example query |
|---|---|---|
| "What is X" | Paragraph (40-60 words) | "what is affiliate marketing" |
| "How to X" | Ordered list | "how to bake sourdough" |
| "X list" or "types of X" | Unordered list | "types of cheese" |
| "X vs Y" | Table or paragraph | "react vs vue" |
| "Best X" / "top X" | Unordered list with brief | "best running shoes" |
| "When did X" / "who is X" | Short paragraph (< 50 words) | "when did rome fall" |
| Numeric answer | Short phrase or table | "how much is tesla stock" |

**Apply the rule:** write the answer in the exact format Google wants. If it's a "how to" query, you need ordered steps. If it's a "what is", you need a paragraph of 40-60 words.

## Step 3: Fetch and Read Your Page

Read your current page. Find where you (try to) answer the target query. Check:
- Does the answer appear? If yes, where? (First paragraph, under an H2, deep in the article?)
- Is the format right for the query type?
- Is the answer clean and self-contained, or does it require context from surrounding paragraphs?
- How long is it? (40-60 words for paragraph snippets; 3-8 steps for list snippets)

## Step 4: Identify the Gap

The most common failures:
- **Wrong format** — you wrote a paragraph when Google wants a list
- **Answer too long** — Google truncates at ~60 words for paragraph; 8-10 items for list
- **Answer too short** — Google wants a complete thought
- **Answer is buried** — it's in the middle of the article, not directly under an H2 that matches the query
- **No self-contained answer** — the answer depends on the surrounding context to make sense
- **Not in a heading-answer structure** — Google looks for H2/H3 followed immediately by the answer

## Step 5: Rewrite

Write a new version of the answer section, optimized for the snippet. The rewrite should:

1. **Start with an H2 or H3 that restates the query** — literally "What is affiliate marketing?" as an H2
2. **Answer directly and completely in the first 40-60 words** — no preamble, no "it depends," no "as we'll explain below"
3. **Use the correct format** — paragraph / ordered list / unordered list / table
4. **Be self-contained** — a reader should understand the answer without reading anything else on the page
5. **Include the target keyword naturally in the first 20 words**

Provide two versions:
- **The featured snippet answer block** — 40-60 words or 3-8 list items, exactly what you want Google to pull
- **A longer follow-up paragraph** — for the reader who wants more depth after the snippet block

## Step 6: Supporting Structure

In addition to the answer block, add:
- An H2 with the exact query phrasing immediately above the answer
- A short intro of 1-2 sentences between the H2 and the answer (optional, helps scannability)
- The 40-60 word answer OR the 3-8 step list
- A deeper explanation AFTER the answer block

Google's snippet extractor looks at this structure specifically. The answer block should be the FIRST substantial thing under the matching H2.

## Step 7: Format-Specific Rules

### For paragraph snippets (40-60 words):
- Complete sentence structure — subject, verb, object
- Direct definition or answer
- No "in this guide we'll cover..." fluff
- Include the target term in the first 20 words

### For ordered list snippets (how-to):
- 3-8 steps maximum
- Each step = one action verb + one sentence
- Steps must be self-contained (don't reference previous steps implicitly)
- Use "1. 2. 3." numbering that Google can parse

### For table snippets (comparisons):
- Clear column headers
- 3-6 rows usually
- Keep each cell short (1-10 words)

## Step 8: Output

### Current State
- Keyword | Current snippet holder | Snippet format present | Snippet text

### Your Page Analysis
- URL | Current position (if known) | Where the answer appears | Format gap

### Rewrite

**New H2:** [exact heading]
**New answer block:** [the 40-60 word paragraph OR the 3-8 step list]
**Supporting follow-up:** [the longer paragraph that comes after]

### Implementation Notes
- Place the new answer block here: [specific location in the existing content]
- Keep the rest of the page intact — don't rewrite surrounding sections
- The FIRST instance of this answer format on the page is what Google extracts

### Realistic Timeline
- Google typically picks up snippet changes within 1-4 weeks
- If no change in 4 weeks, check whether your H2 matches the query phrasing closely enough
- Don't make further changes for at least 2 weeks after the rewrite — let Google reprocess

## What to Ignore

- **Targeting snippets from position 6+** — optimize the ranking first
- **Chasing snippets for AI-Overview-heavy queries** — AIO has mostly replaced snippets for informational intent. Check first whether a snippet actually shows.
- **Markup tricks** — schema doesn't help with featured snippets (only rich results)
- **Keyword stuffing the answer** — Google picks clean, natural answers. One instance of the keyword in the first 20 words is enough.

## Next Step

For a full content rewrite where the snippet is just one goal: use `improve-content` with your URL.

## Bundled references

Load from `references/` only when the step calls for them.

- **`query-format-matching-expanded.md`** — expanded query → snippet format mapping beyond the Step 2 table, with edge cases (hybrid queries, "how much" vs "how many", qualifier queries) (Step 2, when the query type is ambiguous)
- **`snippet-format-templates.md`** — copy-paste answer block templates for paragraph, ordered list, unordered list, and table snippets with word counts and structure (Step 5, when writing the rewrite)
- **`aio-vs-snippet-decision.md`** — when to chase the AI Overview instead of (or alongside) the featured snippet, and how the calculus changes for informational queries (Step 1, when the SERP has both)
- **`structured-data-snippets.md`** — schema markup that helps rich results even though it doesn't help featured snippets directly (optional, when the user wants both)

**Snippet-friendly content type templates** (`references/content-types/`) — load the matching one when the rewrite scope expands from answer block to full section:
- `how-to.md` — for ordered list snippets
- `faq-page.md` — for paragraph snippet stacks from PAA
- `comparison.md` — for table snippets
