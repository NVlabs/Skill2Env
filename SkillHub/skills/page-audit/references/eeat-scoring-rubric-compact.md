# E-E-A-T Scoring Rubric (Compact)

The page-audit skill loads this when scoring Dimension 3. For the full methodology, the `eeat-audit` skill has the long version. This rubric is the runtime-loadable checklist.

## The 30-second heuristic

Skim the page and count specific, datable, first-person observations: numbers with a year attached, a named client, a timestamped screenshot, an error message, a mistake the author made and fixed. Three or more = Experience is probably strong. Zero or one = Experience is absent, no matter how long the bio is.

This single heuristic predicts Dimension 3 more than the other three components combined. Experience is the most underrated E-E-A-T dimension because it's the hardest to fake and the easiest to skip.

## Experience (E1)

**Strong (8–10)**
- First-person usage accounts with dates ("we ran this Sept 2025 to March 2026")
- Original screenshots or photos, preferably timestamped
- Specific dollar amounts, version numbers, error messages
- What DIDN'T work before the current approach
- Unexpected or counterintuitive findings

**Weak (4–6)**
- Occasional "in my experience" framing with no specifics
- Generic examples that could apply anywhere
- A single anecdote with no numbers or dates attached

**Absent (1–3)**
- Pure desk-research synthesis with nothing grounded in doing the thing
- "Imagine you're doing X..." hypotheticals instead of "when I did X"
- Bio claims experience the content never demonstrates
- No images, or only stock photography

## Expertise (E2)

**Strong (8–10)**
- Discusses when the advice does NOT apply ("works for B2B SaaS above €5K ACV, not for consumer apps")
- Explains the *why* behind each recommendation
- Domain terminology used naturally (not stuffed, not oversimplified)
- Addresses 2+ edge cases or exceptions; tradeoffs acknowledged

**Weak (4–6)**
- Surface coverage with no nuance
- Correct facts but no "it depends" framing
- Terminology inconsistent or slightly wrong in spots

**Absent (1–3)**
- Generic content a smart writer could produce in 30 minutes of research
- Every claim presented as universal truth
- Terminology errors a practitioner would never make

## Authoritativeness (A)

**Strong (8–10)**
- Author has verifiable identity (LinkedIn, other published work, speaker pages)
- Content sits within a broader topical cluster on the same domain
- Cites recognized experts accurately and in context

**Weak (4–6)**
- Byline exists but bio is generic ("SEO expert with years of experience")
- Orphaned content, not connected to other pieces on the topic
- Vague citations ("studies show...") or missing

**Absent (1–3)**
- No author attribution, or attributed to "Editorial Team" / the brand
- Standalone page with no topical cluster around it
- No external citations, or citations to low-quality sources

## Trustworthiness (T)

**Strong (8–10)**
- Every statistic has a named source with date
- Affiliate relationships, sponsorships, biases disclosed clearly
- Claims hedged when appropriate ("in our testing" vs "always")
- Transparent methodology for any original data
- Last-updated date with a real changelog, not a fake date-bump

**Weak (4–6)**
- Inconsistent citations
- Affiliate links present but disclosure is buried
- Minor factual errors or outdated claims a practitioner would catch

**Absent (1–3)**
- Unverifiable claims, fabricated statistics, dead-URL citations
- Affiliate content disguised as editorial
- Known factual errors on YMYL topics
- No author, no date, no corrections

## Red flags: schema without substance

Gaming tells. Score any of these as immediate Trustworthiness problems.

- **Person schema + rich author bio + zero demonstrated experience in the content.** Markup claims "20 years experience"; content is a 400-word generic summary.
- **Review schema without reviews.** AggregateRating with no visible review text, or reviews written by the brand itself.
- **FAQ schema with questions no real user would ask.** Questions that use exact keyword verbiage rather than natural phrasing. FAQ was reverse-engineered from the schema, not from user data.
- **Credentials the content never needs.** "PhD in molecular biology" on a content marketing blog. There for E-E-A-T LARP, not because it informs the writing.
- **"Last updated" date that moves but the content doesn't.** Spot-check against the Wayback Machine if recency feels off.

## Cross-reference

For the full methodology (auditing author pages, Quality Rater Guidelines treatment of Experience, YMYL thresholds), invoke the `eeat-audit` skill. This file is the tight version for inline Dimension 3 scoring.
