# Technique 16: Quality Scoring System

## What It Is
A 100-point composite scoring system that evaluates AI-generated content across five dimensions before output. Content scoring below threshold is automatically revised. This is the final quality gate preventing bad content from being published.

## Why It Works
Organizations using structured quality gates report 45% fewer post-publication content issues. The scoring system provides objective, repeatable assessment and identifies WHICH areas need improvement rather than a binary pass/fail.

## Scoring Breakdown (100 Points Total)

### Content Quality (30 points)

**Topical Completeness (0-10):**
- Are all SERP-common topics covered? (from brief's competitor analysis)
- Are PAA questions from the brief addressed?
- Scoring: 10 = all topics covered, 7 = 80%+, 5 = 60%+, 3 = 40%+, 0 = below 40%

**Depth of Coverage (0-10):**
- Does each major section contain specific examples, data points, or analysis?
- Are claims supported with evidence rather than stated as fact?
- Scoring: count sections with at least one specific example/data point. 10 = all sections, proportional down

**Originality (0-10):**
- Does the content contain at least one section adding information not found in the top 10 SERP results?
- Are there unique insights, original analysis, contrarian perspectives, or proprietary data?
- Scoring: 10 = multiple unique sections, 7 = one strong unique section, 4 = unique framing of known info, 0 = pure rehash

### SEO Optimization (25 points)

**Keyword Placement (0-8):**
- Primary keyword in meta title: +2
- Primary keyword in H1: +2
- Primary keyword in first 100 words: +2
- Primary keyword or variation in 2+ H2s: +2

**Internal Links (0-5):**
- 3-5 verified internal links per 1,000 words: +3
- All links validated against real sitemap: +2
- Deduct 2 points per hallucinated link

**Meta Quality (0-4):**
- Meta title under 60 chars with keyword + hook: +2
- Meta description under 155 chars with CTA: +2

**Schema Markup (0-4):**
- Correct primary schema for content type: +2
- FAQ schema present (if FAQ section exists): +2

**Featured Snippet Targeting (0-4):**
- Target snippet format identified and implemented: +2
- 40-60 word direct answer at correct position: +2

### E-E-A-T Signals (15 points)

**First-Person Experience (0-5):**
- Uses "I/we tested," "in my experience," "our data shows": +2
- Contains specific case study or personal testing data: +3
- Scoring: presence of genuine experience signals, not just the words

**Specific Data & Examples (0-5):**
- Named companies, specific numbers, dated events: +2
- At least one example that is not a common/obvious example: +3
- Deduct points for "many companies" or "experts agree" without names

**Source Attribution (0-5):**
- Claims backed by named sources with dates: +3
- External links to authoritative references: +2

### Anti-Slop Score (15 points)

**Zero Tier 1 Phrases (0-5):**
- 5 = zero Tier 1 words/phrases detected
- Deduct 1 point per Tier 1 detection (minimum 0)

**Burstiness (0-3):**
- Measure sentence length standard deviation
- 3 = high variation (SD > 8 words), 2 = moderate (SD 5-8), 1 = low (SD 3-5), 0 = uniform

**Voice Consistency (0-3):**
- Content matches the loaded voice document characteristics
- 3 = strong match, 2 = moderate, 1 = weak, 0 = no voice detected

**Horoscope Test (0-4):**
- Count paragraphs that pass the specificity check (topic-specific, audience-specific)
- 4 = all pass, 3 = 80%+, 2 = 60%+, 1 = 40%+, 0 = below 40%

### AI Citation Readiness (15 points)

**Answer-First Formatting (0-5):**
- Key sections lead with extractable 40-60 word answers: +3
- Direct answer appears within first 100 words of the article: +2

**FAQ Schema (0-3):**
- FAQPage schema present with 3+ properly formatted Q&As: +3

**Claim-Evidence Pairs (0-4):**
- Data claims include named source + date: +2
- Statistics include specific numbers (not "many" or "most"): +2

**Entity Richness (0-3):**
- Named entities (companies, people, tools) used instead of generic references: +2
- Entity relationships explicitly stated: +1

## Readability Targets

| Audience | Flesch Reading Ease | Grade Level | When to Use |
|----------|-------------------|-------------|-------------|
| General consumer (NL) | 60-70 | Grade 7-9 | Comparison sites, how-tos, consumer guides |
| Professional / B2B | 50-60 | Grade 9-12 | SaaS content, industry analysis |
| Technical | 40-50 | Grade 12+ | Developer docs, technical guides |

Readability is assessed but NOT part of the 100-point score (since optimal readability varies by audience and content type).

## Quality Gate Actions

| Score Range | Risk Level | Action |
|-------------|-----------|--------|
| 85-100 | Ready | Output for publication |
| 70-84 | Minor issues | Output with annotations on weak areas for human review |
| 60-69 | Needs revision | Auto-revise weak sections (re-enter Phase 4), maximum 2 cycles |
| 0-59 | Major issues | Full rewrite (re-enter Phase 3), alert human reviewer |

## Auto-Revision Strategy

When score is 60-69, target the weakest category first:

1. **Low Content Quality:** Add missing topics from brief, inject specific examples into thin sections
2. **Low SEO:** Fix keyword placement, add missing internal links, generate meta tags
3. **Low E-E-A-T:** Add first-person experience language, inject specific data points, add source citations
4. **Low Anti-Slop:** Run additional editing passes against banned phrase list, increase sentence length variation
5. **Low GEO:** Restructure key sections with answer-first formatting, add FAQ schema, add source attributions

**Maximum 2 revision cycles.** Research (Self-Refine) shows diminishing returns after 2 cycles, and quality can actually degrade with over-revision.

## Reporting Format

```markdown
## Quality Report

**Overall Score: XX/100** [Ready | Minor Issues | Needs Revision | Major Issues]

| Category | Score | Status |
|----------|-------|--------|
| Content Quality | XX/30 | [pass/flag] |
| SEO Optimization | XX/25 | [pass/flag] |
| E-E-A-T Signals | XX/15 | [pass/flag] |
| Anti-Slop | XX/15 | [pass/flag] |
| AI Citation Ready | XX/15 | [pass/flag] |

**Readability:** Flesch XX (Grade Level X) -- [appropriate/too complex/too simple for target audience]

**Issues Found:**
1. [Specific issue + location in content + suggested fix]
2. [...]

**Strengths:**
1. [What scored well]
2. [...]
```

## Key Sources

- [AgriciDaniel/claude-blog](https://github.com/AgriciDaniel/claude-blog) -- 100-point system across 5 dimensions
- [aaron-he-zhu/seo-geo-claude-skills](https://github.com/aaron-he-zhu/seo-geo-claude-skills) -- 80-item CORE-EEAT framework
- [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) -- 50-point scoring across 5 dimensions
- [AI Content Quality Control Guide 2026 (Koanthic)](https://koanthic.com/en/ai-content-quality-control-complete-guide-for-2026-2/)
- [Self-Refine: Iterative Refinement (Learn Prompting)](https://learnprompting.org/docs/advanced/self_criticism/self_refine)
