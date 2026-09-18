---
name: eeat-audit
description: Use when auditing a page for E-E-A-T signals. The agent reads the page and scores Experience, Expertise, Authoritativeness, and Trustworthiness — then tells you exactly what to add to each dimension.
---

# E-E-A-T Audit

Scores a page on Experience, Expertise, Authoritativeness, and Trustworthiness — the four signals Google's quality raters use to evaluate content. Tells you what's missing and how to add it.

Real E-E-A-T is demonstrated, not declared. An author bio is table stakes. What matters is whether the content *feels* like it was written by someone who has actually done the thing.

## Input

**URL of the page to audit**. If the fetch fails, ask the user to paste the content directly.

## Role

You are a senior content quality evaluator with 10+ years reading for Google's quality rater framework. You can tell within 30 seconds of reading whether an author has done the thing they're writing about.

## Step 1: Read the Page

Fetch and read the full rendered page. Note everything that could be an E-E-A-T signal:
- Author name, bio, credentials
- Byline with publication date
- First-person language ("I tried...", "we found...", "when I was at...")
- Specific anecdotes, names, numbers, dates
- Original photos, screenshots, diagrams
- Quoted sources, linked references
- Schema markup (Person, Author, Organization)
- About page linked from the article
- External references to the author or publication

## Step 2: Score Each Dimension (1-10)

### Experience (the most underrated E-E-A-T factor)

**What you're looking for:** evidence the author has DONE the thing, not just researched it.

**Strong signals (8-10):**
- First-person observations with specific details
- "When I tried this, X happened"
- Original photos/screenshots from the author's own work
- Failure stories with specific lessons
- Details only hands-on experience would know (the "smell test")
- A story that reveals workflow, not just outcomes

**Weak signals (4-6):**
- Generic advice that anyone could write after 30 minutes of research
- Third-person narration of other people's case studies
- Examples that feel plucked from Google
- "According to studies..." without identifying which ones

**Absent (1-3):**
- No first-person anywhere
- No specific stories
- No details beyond what's already on the top 10 ranking pages

### Expertise

**What you're looking for:** accurate facts and depth beyond surface level.

**Strong signals:**
- Every factual claim is accurate and verifiable
- Numbers cited with primary sources (original research, not "studies show")
- Technical details correctly used (terminology, processes, edge cases)
- Willingness to disagree with common advice when the author has a reason
- Depth beyond what a smart generalist could produce in 30 minutes

**Weak signals:**
- Accurate but shallow
- Secondary sources cited (blog posts citing blog posts)
- Common advice repeated without critique

**Absent:**
- Factual errors
- Outdated information presented as current
- Surface-level "what Google says" summary

### Authoritativeness

**What you're looking for:** does this content and author belong in the conversation?

**Strong signals:**
- Page is part of a broader topical cluster on the domain
- Author expertise is verifiable beyond a bio paragraph (LinkedIn, talks, books, citations elsewhere)
- External sites cite this page or author
- Clear track record on this specific topic

**Weak signals:**
- Isolated page on a broad topic site
- Generic author with no verifiable specialty
- No external validation

**Absent:**
- Random blog post with no author attribution
- Site has no topical focus
- No internal linking cluster

### Trustworthiness

**What you're looking for:** transparency and honesty.

**Strong signals:**
- Transparent about limitations ("this didn't work when X")
- Discloses conflicts of interest (affiliate links, paid placements)
- Methodology explained
- Willingness to recommend alternatives, even competitors
- Factually accurate throughout
- Recent publish/update date for time-sensitive topics

**Weak signals:**
- Feels like an advertorial but doesn't disclose
- Hides limitations
- Methodology unclear

**Absent (1-3):**
- Factual errors
- Affiliate-driven content without disclosure
- Misleading claims
- Outdated information on a time-sensitive topic

## Step 3: Output

### E-E-A-T Scorecard

| Signal | Score | Key Gap |
|---|---|---|
| Experience | /10 | |
| Expertise | /10 | |
| Authoritativeness | /10 | |
| Trustworthiness | /10 | |
| **Total** | **/40** | |

### What's Working

Specific observations. "The screenshot in Section 3 is clearly from the author's own dashboard — this is a strong Experience signal."

### What's Missing

Specific gaps with specific fixes:
- "No first-person observations in the first 500 words. Add: 'When I first tested this at [company name], the result surprised me — [specific outcome].'"
- "The claim about 42% improvement isn't sourced. Either cite the primary study or drop the number."
- "No author bio links to a LinkedIn or profile page. Add: a one-sentence bio with a credential anchor and an external link to the author's profile."

### Fastest Wins

Three changes you could make in under 30 minutes that would lift the E-E-A-T score materially. Ordered by impact.

### Structural Recommendations

Things that require more work but would fundamentally strengthen E-E-A-T: adding a methodology section, linking to related topical cluster pages, adding Author schema markup, creating an About page for the author.

## What to Ignore

- **Generic "add author bio" advice** — it's table stakes, not E-E-A-T
- **Schema without substance** — marking up a page with Person schema when the content shows no experience is worse than no schema
- **Gaming quality rater signals** — the raters aren't fooled, and the algorithm isn't either

## Next Step

To apply the fixes: use the `improve-content` skill with this URL, and paste the gap list as context.

## Bundled references

Load from `references/` only when the step calls for them.

**Scoring and diagnosis:**
- **`ymyl-scoring-rubric.md`** — stricter scoring rubric for Your Money Your Life pages (finance, medical, legal) where the E-E-A-T bar is materially higher (Step 2, any YMYL page)
- **`experience-detection-playbook.md`** — how to tell in 30 seconds whether an author has done the thing (Experience dimension, when the page looks ambiguous)
- **`fastest-eeat-wins.md`** — ranked list of the highest-impact E-E-A-T fixes by implementation effort (Step 3, "Fastest Wins" block)
- **`eeat-signal-embedding.md`** — how to surface experience without a bio section or fake credentials (Step 3, "Structural Recommendations")
- **`author-schema-templates.md`** — copy-paste Person / Author / Organization JSON-LD for the schema fix (Step 3)

**YMYL content-type templates** (`references/content-types/`) — load when auditing one of these types for the type-specific E-E-A-T bar:
- `thought-leadership.md`, `product-reviews.md`, `pricing-pages.md`, `service-pages.md`, `case-studies.md`, `about-pages.md`
