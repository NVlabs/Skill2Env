---
name: geo-optimizer
description: Optimize existing blog posts and web content for GEO (Generative Engine Optimization) — AI search visibility on ChatGPT, Perplexity, Claude, and Google AI Overviews. Use whenever a user provides a blog URL or pastes existing content and asks to optimize it for AI search, rewrite for LLM visibility, improve GEO score, make content answer-first, add FAQ sections, restructure headings for AI retrieval, improve citation potential, or audit content for AI readiness. Also triggers on "GEO optimize this", "make this AI-search ready", "rewrite for Perplexity", "optimize for ChatGPT", "optimize for Google AI Overviews", "improve AI visibility", "reformat for AI search", "make this content citation-worthy", "content isn't showing up in AI search", "why isn't my blog cited by AI", "GEO audit", "answer-first rewrite", "restructure for AI", "make my blog AI-friendly", "improve LLM citability". Do NOT trigger for writing new content from scratch — use geo-content for that.
---

# GEO Optimizer

Analyze and rewrite existing content to maximize visibility, citability, and retrieval by AI search engines (ChatGPT, Perplexity, Claude, Google AI Overviews).

Always produce two outputs:
1. **HTML report** — GEO audit with before/after score, issue breakdown, and annotated changes
2. **DOCX** — clean, ready-to-publish rewritten article

---

## Step 1: Detect Input Mode

**URL mode** — User provides a link. Use `web_fetch` to retrieve the page. Extract: title, meta description, H1, all headings (H2/H3), body text, existing FAQs, and any schema present.

**Paste mode** — User pastes raw content. Use as-is. Infer target query from the H1 or opening paragraph.

If neither is provided, ask: "Please share the blog URL or paste the content you'd like to GEO optimize."

If `web_fetch` fails (gated page, login wall, etc.), tell the user and ask them to paste the content instead.

---

## Step 2: Identify the Primary Target Query

Before auditing or rewriting, determine:
- What one core question should this post answer?
- Is the H1 query-shaped (sounds like something a real person would search)?
- Does the opening paragraph answer it directly?

State the primary target query explicitly. This drives all rewriting decisions.

---

## Step 3: GEO Audit — Score the Original

Score the original content across 5 dimensions (20 points each, 100 total).

### 1. Answer-First Structure (0–20)
- Do the opening 2–3 sentences directly answer the primary query?
- Is the key insight stated upfront, not buried in the conclusion?
- Deduct for preamble, background-first intros, or "In this article, we will…" openers.

### 2. Heading Quality (0–20)
- Are H2/H3s query-shaped — do they sound like something searchable?
- Do headings make sense read out of context (as an AI would extract them)?
- Deduct for vague headings like "Introduction", "Overview", or "More Details".

### 3. Chunkability & Section Independence (0–20)
- Can each section be understood without reading the rest of the article?
- Are self-referential phrases absent ("as mentioned above", "as we'll see below")?
- Are paragraphs short and purposeful (3–4 lines max)?

### 4. Citation Signals (0–20)
- Are specific statistics, data points, or named sources present?
- Are claims concrete and attributable rather than vague ("studies show", "experts say")?
- Are definitions, numbered steps, or comparison tables present?

### 5. FAQ & Structured Formats (0–20)
- Is there a FAQ section written in realistic search-language questions?
- Are tables used for comparisons or criteria where applicable?
- Are there definition blocks or quotable summary statements?

Compute and record the **GEO Score Before: X/100** with per-dimension breakdown.

---

## Step 4: Rewrite the Content

Apply all of the following in order:

### 4a. Rewrite the Opening (Answer-First)
Lead with a direct, quotable answer to the primary target query in the first sentence. Follow with 1–2 sentences of supporting context. Remove any preamble, hook, or "by the end of this article…" language entirely.

### 4b. Rewrite All Headings
Rephrase every H2 and H3 to be query-shaped and self-explanatory when read out of context.

- Before: "Benefits of X" → After: "What Are the Main Benefits of X?"
- Before: "Our Approach" → After: "How Does [Topic] Work in Practice?"
- Before: "Introduction" → After: Remove or replace with the actual topic

### 4c. Rewrite Each Section for Chunkability
- Remove self-referential phrases
- Break any paragraph longer than 4 lines into shorter units
- Make the first sentence of each section a mini-answer for that section's heading

### 4d. Strengthen Citation Signals
- Replace vague claims with specific statistics or named sources. If the original has none, infer credible sources that fit (e.g. "According to a 2024 Gartner report…") and flag these clearly as suggested additions for the writer to verify.
- Add a definition block for the core concept if one is missing
- Add a comparison table if the content compares tools, methods, or options

### 4e. Add or Improve FAQ Section
Write 5–7 FAQ questions in real search language (the kind a person types into Google or Perplexity). Each answer: 2–4 sentences, direct, self-contained, quotable. Place the FAQ near the bottom of the article.

### 4f. Suggest Meta Optimization
Always produce:
- **Slug**: short, keyword-first, hyphenated
- **SEO Title**: query match, under 60 characters
- **Meta Description**: spoils the answer, 150–160 characters
- **H1**: slightly more descriptive than the slug, still query-shaped

---

## Step 5: Re-Score the Rewritten Content

Apply the same 5-dimension scoring to the rewritten version.
Compute the **GEO Score After: X/100**.
Show the delta clearly: e.g., "GEO Score: 38/100 → 84/100 (+46 points)"

---

## Step 6: Generate Outputs

### Output A: HTML Report

Read `/mnt/skills/public/frontend-design/SKILL.md` for design tokens and styling before writing the HTML.

The report must include:

1. **Header** — Article title, source URL (if provided), optimization date
2. **Score Card** — Before/after GEO score with visual progress bars for each dimension
3. **Audit Summary** — Per-dimension issues with severity labels (High / Medium / Low)
4. **Meta Suggestions** — New slug, SEO title, meta description, H1
5. **Before/After Sections** — Original vs. rewritten for each major section (use a toggle/collapsible pattern)
6. **FAQ Section** — Newly written FAQ rendered cleanly at the bottom

Save to: `/mnt/user-data/outputs/geo-report.html`

### Output B: DOCX

Read `/mnt/skills/public/docx/SKILL.md` before generating the file.

The .docx must have two sections:

**Section 1 — Cover Page**
- Article title (large, bold, dark navy `1E3A5F`)
- Left border accent on title block
- Meta block: Slug, SEO Title, Meta Description, H1, Mode, Date
- GEO Score summary: Before / After / Improvement
- Score breakdown table (5 dimensions × Before/After/Change)
- Page break after cover

**Section 2 — Article Body** (with footer showing page numbers)
- Full rewritten article, clean and publish-ready
- Heading hierarchy: H1 (36pt navy) → H2 (26pt navy) → H3 (22pt accent blue)
- Body text in Calibri 11pt (22 half-points), color `2C2C2C`
- Tables: light gray headers (`E8EEF4`) with dark text, alternating row fills (`F7F9FB`). Always use `ShadingType.CLEAR` — never SOLID. Always set both `columnWidths` on the table AND `width` on each cell.
- FAQ section at the bottom with H2 heading, divider, then Q (bold navy) + A (indented body) pairs
- No audit commentary anywhere — just the finished article

Use `Calibri` as the default font throughout.
Set page size explicitly: US Letter 12240 × 15840 DXA, 1" margins (1440 DXA each side).

Save to: `/mnt/user-data/outputs/geo-optimized-article.docx`

---

## GEO Principles (The Why Behind Every Decision)

- **Retrieval first**: AI engines match queries to headings and opening sentences before body text. Query-shaped H1s and H2s win.
- **Answer-first**: AI quotes the first clear answer it finds. Put the conclusion before the context.
- **Chunkability**: AI engines extract sections independently. Every section must stand alone.
- **Citation-friendly formats**: Definitions, numbered steps, bullets, FAQs, and comparison tables are the formats AI engines quote most.
- **Specificity wins**: Concrete claims with numbers and sources get cited. Vague generalities do not.
- **Self-contained sections**: No cross-references. No "as we discussed." If a section needs the previous one to make sense, rewrite it.

---

## Edge Cases

- **Short content (<500 words)**: Flag it. GEO optimization works best on 800+ word posts. Still optimize what exists and recommend which sections to expand.
- **Non-English content**: Optimize in the same language as the input.
- **Already high-scoring content (>80/100)**: Focus the report on the remaining gaps. Don't rewrite what's already working — annotate it as "strong" and move on.
- **Thin or promotional content**: If the content is mostly marketing copy with little informational value, flag this explicitly. GEO optimization cannot compensate for low informational depth — recommend expanding the substance first.