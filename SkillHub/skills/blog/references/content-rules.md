# Content Structure Rules: Dual Optimization

## Contents

- [Answer-First Formatting (Strong AI Citation Improvement)](#answer-first-formatting-strong-ai-citation-improvement)
- [Title Optimization](#title-optimization)
- [Summary Box Requirement](#summary-box-requirement)
- [Heading Hierarchy](#heading-hierarchy)
- [Sentence Rules](#sentence-rules)
- [Paragraph Rules](#paragraph-rules)
- [Readability Targets](#readability-targets)
- [Visual Content Rules](#visual-content-rules)
- [Anti-Pattern Detection](#anti-pattern-detection)
- [Content Length Guidelines](#content-length-guidelines)
- [Citation & Statistics Rules (GEO)](#citation--statistics-rules-geo)
- [Information Gain: The Key Differentiator](#information-gain----the-key-differentiator)
- [Meta Description Formula](#meta-description-formula)
- [Citation Format](#citation-format)
- [Citation Tiers](#citation-tiers)
- [Self-Promotion Rules](#self-promotion-rules)
- [Internal Linking](#internal-linking)

## Answer-First Formatting (Strong AI Citation Improvement)

The most impactful single optimization. Every H2 section must open with a
40-60 word paragraph that:

1. Contains at least one specific statistic with source attribution
2. Directly answers the heading's implicit question
3. Uses natural, conversational language

### Pattern
```markdown
## How Does X Impact Y in 2026?

[Stat] ([Source](url), year). [Direct answer in 1-2 more sentences, explaining
the implication for the reader. Keep this opening paragraph to 40-60 words total.]
```

### Why It Works
AI systems extract answers from section openers. If your answer is buried in
paragraph 3 of a section, it will not be cited. Lead with the answer, then
explain.

44.2% of all LLM citations come from the first 30% of text (Growth Memo,
Feb 2026). Use declarative "X is Y because Z" sentence structures for maximum
AI extractability. Target 40-60 words per answer paragraph - this is the optimal
length for paragraph featured snippet capture.

## Title Optimization

| Parameter | Target | Impact |
|-----------|--------|--------|
| Character length | 40-60 characters | 8.9% higher CTR (Backlinko) |
| Sentiment | Positive framing | +4.1% CTR vs neutral titles |
| Brackets/parentheses | Include when relevant | ~40% more clicks (HubSpot) |
| Power words | 1-2 per title | "Definitive," "Essential," "Data-Backed" |
| Keyword placement | Front-loaded | Primary keyword in first 3 words when possible |

### Title Formula
Pattern: `[Power Word] [Topic]: [Specific Outcome/Number] [Year]`
Example: "Definitive Guide to GEO: 7 Strategies That Drive AI Citations in 2026"

Avoid: clickbait, ALL CAPS words, excessive punctuation, vague promises.

## Summary Box Requirement

Every post must open with a summary box immediately after the title/intro:

- **Length**: 40-60 words total across all bullet points (standalone summary)
- **Purpose**: AI extraction target - LLMs frequently cite these verbatim
- **Content**: 3-5 bullet points covering core findings with one key statistic
- **Format**: Visually distinct block (callout, bordered box, or blockquote)
- **Rule**: Must be comprehensible without reading the rest of the article

### Pattern
The default label is **Key Takeaways** (professional, universally understood).
Alternative labels configurable per persona: "The Bottom Line" (business/finance),
"What You'll Learn" (educational/tutorial), "At a Glance" (scan-optimized),
"In Brief" (journalistic).

Format: 3-5 bullet points (not a prose paragraph):
```markdown
> **Key Takeaways**
> - [Core finding with statistic] ([Source], year)
> - [Second key insight or recommendation]
> - [Third actionable takeaway]
```

For backward compatibility, blog-analyze accepts both "TL;DR" and "Key Takeaways".

## Heading Hierarchy

### Rules
- ONE H1 per page (the title only)
- H2s for main sections (target 6-8 per post)
- H2 every 200-300 words (Yoast flags sections >300 words without a subheading)
- H3 every 100-200 words under each H2 for deeper structure
- H3s for subsections - never skip levels (no H2 → H4)
- Include primary keyword naturally in 2-3 headings

### Question-Format Headings
Convert 60-70% of H2s to questions:
- "The Future of X" → "What Does X Look Like in 2026?"
- "Strategies for Y" → "How Do You Achieve Y in 2026?"
- Keep 2-3 statement headings for variety

### Why Questions Work
AI systems directly extract answers following question formats. Search engines
show these in People Also Ask. Users scan headings as questions they want answered.

## Sentence Rules

| Parameter | Target | Flag At | Source |
|-----------|--------|---------|--------|
| Average sentence length | 15-20 words | >22 words | Yoast, Siteimprove |
| Max sentence length | 25 words | >20 words | Yoast flags >20 |
| Sentences over 20 words | ≤25% | >25% | Yoast threshold |
| Sentence length variance | StdDev ≥5 words | <5 StdDev | Wikipedia AI guidelines |
| AEO-optimal average | 15-18 words | - | GEO research synthesis |

### Sentence Rhythm
Mix short (5-10 words), medium (15-20 words), and occasional long (20-25 words)
sentences. Uniform sentence length signals AI authorship. Human writing has
natural burstiness - a short punchy sentence after a longer explanatory one.

No more than 3 consecutive sentences within 5 words of each other's length.

## Paragraph Rules

| Parameter | Target | Flag At | Hard Limit | Source |
|-----------|--------|---------|------------|--------|
| Paragraph length | 40-80 words | >100 words | 150 words (200 = Yoast red) | Yoast, NNGroup |
| Sentences per paragraph | 2-3 | >3 | 4 max | NNGroup scanning research |
| Mobile paragraph max | 60 words / 2-3 visual lines | - | - | WCAG, Baymard |
| Extractable chunks | 50-150 words | - | - | GEO citation research |

### Key Principle
Start each paragraph with the most important sentence. This enables both
readers and AI to grasp concepts by scanning. 79% of users scan rather than
read (NNGroup). Concise, scannable formatting improves usability 124-159%
(NNGroup).

### Paragraph Sentence Limit
Maximum 2-3 sentences per paragraph. This is a hard rule. Single-sentence
paragraphs are acceptable and often preferred for emphasis. Paragraphs
exceeding 3 sentences should be split.

One topic per paragraph - no topic drift within a paragraph.

## Readability Targets

| Metric | Target | Acceptable | Source |
|--------|--------|-----------|--------|
| Flesch Reading Ease | 60-70 | 55-75 | Yoast ≥60; Spotlight 18K prompts: 60-75 = 31% more AI citations |
| Flesch-Kincaid Grade | 7-8 | 6-9 (B2B/technical: 8-10) | Siteimprove, First Page Sage |
| Gunning Fog | 7-8 | Max 12 | Springer 2023: highest correlation with engagement |
| SMOG | ≤8 | - | Healthcare gold standard |

Flesch 60-70 is the optimal band for both engagement and AI citation.
Content in this range demonstrates expertise through clear expression of
complex ideas - not oversimplification. The key is conversational authority:
natural language that mirrors how experts actually explain things.

AI systems prefer content that is fluent, specific, and well-structured.
Readability alone doesn't determine AI citation - content must also demonstrate
expertise and provide unique value.

### Readability Bands by Audience
| Audience | Flesch Grade | Flesch Ease | Max Sentence | Use When |
|----------|-------------|-------------|--------------|----------|
| Consumer | 6-8 | 60-80 | 20 words | General audience, lifestyle, health |
| Professional (B2B) | 8-10 | 50-60 | 25 words | Business, marketing, finance |
| Technical/Developer | 10-12 | 30-50 | 30 words | Engineering, API docs, data science |

Default target (no persona active): Grade 7-8, Flesch Ease 60-70.
When a persona is active, use the persona's readability band instead.
Content clarity is the #2 factor for AI citation probability (+32.83%
score differential, ZipTie.dev). Average US adult reads at 7th-8th grade level.

## Visual Content Rules

| Parameter | Target | Minimum | Source |
|-----------|--------|---------|--------|
| Image/visual frequency | Every 200-350 words | 1 per 500 words | BuzzSumo, NNGroup |
| Bold/emphasis | 3-5 per 300 words | - | Competitive analysis |
| Bold % of total text | <10% | - | Diminishing impact above 10% |

### Lists
Use bulleted or numbered lists when 3+ parallel items exist. Don't force lists
where prose works better - lists are for scannable parallel items, not for
every piece of information.

### Visual Impact
Content with visuals gets 94% more views (MDG Advertising, c. 2014 via Jeff Bullas; stat is
10+ years old) and 150% more social engagement. More recent: Semrush 2026 found blogs with
7+ images per post receive 116% more organic traffic.
NNGroup: visitors read only ~20% of words on a page - visuals anchor scanning
patterns and guide the eye to key information.

### Visual Rhythm (Mandatory Pacing)
Insert a visual element (image, chart, or callout) every 300-500 words.
- Minimum: 1 visual per 500 words; optimal: 1 per 300-350 words
- Alternate visual types: image -> chart -> callout -> image (no consecutive same-type)
- Hero image: above the fold, 1920x1080 (16:9) or 1200x630 (OG-compatible)
- All images: explicit width/height attributes for CLS prevention (score <= 0.1)
- Below-fold images: loading="lazy"; hero image: fetchpriority="high"
- Posts with 10+ visuals are 2x more likely to report strong results (Orbit Media)
- 79% of people scan content rather than reading it (NNGroup)

## Anti-Pattern Detection

### AI Trigger Words (≤5 per 1,000 words)
Red-flag words that spiked >50% post-ChatGPT. Flag if total exceeds 5 per
1,000 words:

delve, tapestry, multifaceted, testament, pivotal, robust, cutting-edge,
furthermore, indeed, moreover, utilize, leverage, comprehensive, landscape,
crucial, foster, illuminate, underscore, embark, endeavor, facilitate,
paramount, nuanced, intricate, meticulous, realm

### Em Dashes (Zero Tolerance)
NEVER use em dashes (-) in blog content. Em dashes are a strong AI writing
signal. Replace with commas, hyphens (-), colons, or periods. Split sentences
if an em dash was used to join two independent clauses.

### Passive Voice (≤10% of sentences)
Yoast threshold. Clusters of passive voice signal automated content.

### Transition Words (20-30% of sentences)
Yoast optimal: ~25%. Below 20% feels choppy; above 35% reads AI-generated.

### Keyword Density (0.5-2%)
Flag at >2.5%, penalize at >3%. Primary keyword: 3-5 times naturally.

### Filler Content Detection
QRG 2025 targets "artificially inflated content." Flag: entity drift,
topical dilution, needless repetition, intent mismatch.

## Content Length Guidelines

| Content Type | Target Length | Minimum |
|-------------|-------------|---------|
| Pillar guide | 3,000-4,000 words | 2,500 |
| Standard blog post | 2,000-2,500 words | 1,500 |
| Comparison post | 1,500-2,000 words | 1,200 |
| FAQ/listicle | 1,500-2,000 words | 1,000 |
| News/update | 800-1,200 words | 600 |

Sweet spot: 1,500-2,500 words for most content. Minimum 700 words
(absolute floor: 300 words for news updates). Long-form (2,000+ words)
gets 3x more AI citations than short posts.

Reading time: word count ÷ 225, rounded up. Optimal reading time is
5-7 minutes (~1,100-1,575 words). Engagement falls off sharply after
7 minutes; approaches zero at 14+ minutes (Medium, Smartocto 2025).

## Citation & Statistics Rules (GEO)

| Parameter | Target | GEO-Optimized | Source |
|-----------|--------|--------------|--------|
| Statistic density | 1 per 200 words | 1 per 150 words | Princeton GEO paper |
| External citations | 1-3 per 1,000 words | - | GEO best practices |
| Internal links | 2-5 per 1,000 words | - | SEO + engagement |

Statistics addition boosts AI visibility up to 41% (Princeton GEO paper,
KDD 2024). For lower-ranked sites, citing authoritative sources boosts
visibility up to 115%. The combination of fluency + statistics outperforms
any single optimization tactic by 5.5%.

### Attribution Format
Always attribute statistics: `[Number]% [claim] ([Source](url), [Year])`.
Unattributed statistics damage E-E-A-T trust signals and are flagged as
fabrication risks in quality scoring.

**FLOW evidence triple format (drafting requirement):**

- Year anchor in prose: "In 2026, [Source] found..." (NOT: "...found ... (Source, 2026).")
- Inline citation: publisher AND title, e.g. "Ahrefs, AI Overviews CTR update".
- Source block: full URL plus `retrieved YYYY-MM-DD` for every cited source.

Drop unverifiable stats. Replace contradicted stats with verified alternatives. See `flow-alignment.md`.

## Information Gain: The Key Differentiator

Google's Information Gain patent (US11354342B2, 2022) rewards content with
novel data points beyond what top-ranking results cover. AI synthesizes
consensus but cannot create new data. Optimize by:

1. **Original research**: Surveys, proprietary data, experiments (+25.1% top-10, Stratabeat)
2. **Personal perspective**: Opinions AI cannot replicate
3. **Expert interviews**: Practitioners with first-hand knowledge
4. **Case studies**: Real metrics and results
5. **Industry-segmented analysis**: Break down by vertical (+43.4% top-10, Animalz)

## Meta Description Formula

Pattern: "[Key statistic]. Here's how [strategy] delivers [outcome] in 2026."

Rules:
- 150-160 characters (desktop ~920px); mobile shows only ~120 characters (~680px)
- Front-load key information in the first 120 characters for full mobile visibility
- Include one specific statistic
- No keyword stuffing
- End with value proposition or call to action
- Fact-dense, not vague

## Citation Format

Inline: `[Number]% [claim] ([Source](url), [Year])`. Always name the source.
Study: Name the paper, institution, and year. Quote: Use quotation marks with speaker name and date.

## Citation Tiers

| Tier | Examples | Trust |
|------|----------|-------|
| 1 - Primary Authority | Google Search Central, .gov, .edu, W3C | Highest |
| 2 - Primary Data | Ahrefs, SparkToro, Seer, BrightEdge, Princeton GEO Paper | High |
| 3 - Trusted Journalism | Search Engine Land, SEJ, The Verge, Wired, TechCrunch | Good |
| 4-5 - AVOID | SEO tool blogs (non-research), affiliate sites, content mills | Hurts E-E-A-T |

## Self-Promotion Rules

- Maximum 1 brand mention per post (author bio context only)
- Remove "At [Company], we..." patterns and promotional links
- Author section should demonstrate E-E-A-T credentials, not sell

## Internal Linking

- 5-10 internal links per 2,000-word post, descriptive anchor text
- Ensure bidirectional linking (pillar ↔ supporting pages)
