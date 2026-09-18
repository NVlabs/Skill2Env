# Technique 15: Writing Pipeline Architecture

## What It Is

A multi-phase, multi-agent pipeline for producing high-quality SEO content. Based on analysis of 15+ agentic writing systems, this architecture represents the consensus best approach: specialized phases with quality gates, not a single monolithic generation.

## Why It Works

Research consistently shows that multi-agent pipelines outperform single-prompt generation:
- Section-by-section generation maintains quality over long articles
- Specialized agents (writer vs. critic) produce better results than a generalist
- One to two revision cycles capture 95% of improvement (Self-Refine research)
- Quality gates prevent bad content from being output

Human-written articles still generate 5.44x more traffic and hold attention 41% longer than pure AI. The pipeline must close this gap through specialization.

Single-prompt content generation fails because one prompt can't simultaneously optimize for research depth, writing quality, SEO mechanics, anti-detection, and fact accuracy. Each agent focuses on ONE thing well, and each stage builds on verified output from the previous stage.

## The 7-Agent Model

The pipeline uses seven specialized agents, each with a distinct role and optimal configuration:

| Agent | Role | Temperature | Tools |
|-------|------|-------------|---------------|
| Researcher | Analyze topic landscape, SERP competition, information gaps | Low (0.2-0.3) | keyword search, competitor data, SERP feature detection |
| Outliner | Create SERP-optimized content structure | Low-Medium (0.3-0.4) | opportunity detection, keyword cluster data |
| Writer | Generate first draft with anti-detection built in | Medium (0.5-0.7) | page content rendering (competitor analysis) |
| Humanizer | Audit and fix surviving AI patterns | Low (0.2-0.3) | None |
| Fact-Checker | Verify all claims, statistics, attributions | Low (0.1-0.2) | None |
| SEO Optimizer | Keyword placement, meta elements, schema, linking | Low (0.2-0.3) | internal link data, SERP feature detection |
| Quality Reviewer | Final holistic review and scoring | Low (0.2-0.3) | None |

## Implementation Architecture

```
+--------------+     +----------+     +--------+     +-----------+
| RESEARCHER   | --> | OUTLINER | --> | WRITER | --> | HUMANIZER |
+--------------+     +----------+     +--------+     +-----------+
                                                          |
+--------------+     +----------+     +----------------+  |
| QUALITY      | <-- | SEO      | <-- | FACT-CHECKER   | <+
| REVIEWER     |     | OPTIMIZER|     |                |
+--------------+     +----------+     +----------------+
      |
      v
  [FINAL OUTPUT]
  - Article (markdown)
  - Meta elements
  - Quality scorecard
  - SEO checklist
  - Schema JSON-LD
  - AI-detection risk score
```

## User Approval Workflow

The pipeline is NOT fully autonomous. Human checkpoints are mandatory:

1. User invokes "write content" -> triggers RESEARCHER
2. RESEARCHER output presented to user for review/approval
3. OUTLINER generates structure -> user approves or modifies
4. Pipeline PAUSES to collect human input (experiences, data, opinions)
5. WRITER generates with all context -> HUMANIZER audits
6. FACT-CHECKER flags issues -> user verifies first-party claims
7. SEO OPTIMIZER + QUALITY REVIEWER finalize
8. Final output with scorecard presented to user

At every human checkpoint, the user can modify, reject, or redirect. This is not optional overhead -- it is the mechanism that prevents high-quality slop.

## Pipeline Architecture (Detailed Phases)

### Phase 1: Preparation (Context Loading)

**Inputs loaded:**
1. Content Brief (from Content Brief Generator)
2. Voice Document (from your saved business context or user-provided)
3. Content Type Template (selected based on intent/type from brief)
4. Anti-Slop Rules (banned phrases, structural patterns)
5. Internal Link Map (from internal link data)
6. Competitor Content Analysis (from page content rendering on top competitor URLs)

**Critical:** All context must be loaded BEFORE writing begins. Loading mid-article breaks voice consistency.

**The RESEARCHER agent performs:**
1. Queries tools: keyword search, competitor data, SERP feature detection
2. Analyzes top 10 SERP results for the target keyword
3. Maps competitor content coverage (topics covered, depth, unique angles)
4. Identifies information gaps (topics nobody covers)
5. Notes SERP features present (PAA, featured snippets, video carousels)
6. Recommends target word count based on competitor analysis

**Output:** Research brief with SERP gap analysis, competitor coverage map, information gain opportunities.

### Phase 2: Outline Generation

**The OUTLINER agent generates a detailed outline from the content brief:**
1. SERP-derived H2/H3 structure (matching what ranks)
2. Keywords mapped to specific sections
3. Internal links planned for specific paragraphs
4. Data points / examples planned per section
5. Featured snippet target identified (format + section)
6. PAA questions assigned to sections
7. Word count allocation per section
8. "Human input required" points marked (case studies, data, opinions)

**Human approval gate:** Present outline for approval before proceeding. In automated mode, validate against brief structure. The user can add, remove, or reorder sections.

### Phase 3: Section-by-Section Writing

**Why section-by-section:** For articles over 1,500 words, full-article generation leads to quality drift, repetition, and context distraction. Section-by-section maintains focused context.

**The WRITER agent processes each section:**
1. Load section brief (H2/H3 structure, assigned keywords, planned links, planned examples)
2. Load voice document (reload for each section to maintain consistency)
3. Apply content type template rules
4. Inject human-provided content at designated points
5. Write the section with anti-detection built in (varied sentence length 3-40 words, Tier 1 word avoidance)
6. Place internal links at natural anchor points
7. Update scratchpad with key points covered (prevents repetition)
8. Compress section summary for context management

**Context management:** After each section, create a summary of what has been covered. Use the summary (not full text) as context for subsequent sections. This prevents the model from losing focus as context grows.

**Key finding from Anthropic:** Model performance drops around 32,000 tokens even with million-token windows due to context distraction. Use "just-in-time context" -- lightweight identifiers that dynamically load data at runtime, not monolithic context blocks.

**Section compression strategy:** Each completed section is reduced to a 2-3 sentence summary containing: key points made, data cited, keywords used, links placed. The full text is stored separately. The writer for the next section sees only these summaries plus the current section's brief.

### Phase 4: Anti-Slop Editing

**Separate from writing.** The writer agent should be "naive" about quality rules (DonAldente pattern) -- its job is to write naturally. The editor/critic is separate and ruthless.

**The HUMANIZER agent runs two passes:**

**Pass 1: Detection**
- Scan for Tier 1 banned phrases (always remove)
- Scan for Tier 2 clustering (flag if 3+)
- Scan for Tier 3 density (flag clusters)
- Check structural patterns (uniform sentence length, rule-of-three, etc.)
- Check burstiness (sentence length standard deviation must be > 5 words per paragraph)
- Check rhythm uniformity (flags sections where all sentences are 15-25 words)
- Score total points

**Rewrite:** For each flagged section, rewrite preserving meaning while eliminating the pattern. Do not just delete -- replace with human-sounding alternatives.

**Pass 2: Surviving Pattern Check**
- Re-scan the full text after Pass 1 rewrites
- First-pass rewrites retain 15-20% of AI patterns
- Specifically check for recycled transitions, lingering inflation, new uniformity

**Horoscope Test:** For each paragraph, ask: "Could anyone have written this, for anyone?" If yes, flag for specificity injection.

**Critical threshold:** If the Humanizer has to rewrite more than 20% of the content, the Writer prompt needs improvement. The Writer should produce mostly clean output; the Humanizer is a quality gate, not the primary fix.

### Phase 5: Fact-Checking

**The FACT-CHECKER agent verifies:**
1. All factual claims in the content
2. Statistics against named sources
3. Fabricated or unverifiable claims (flag for removal)
4. All "experts say" have named experts
5. URLs and references are real and current
6. Claims that need human verification (first-party data)

**Output:** Fact-checked draft + verification report with confidence levels per claim.

### Phase 6: SEO Optimization

**The SEO OPTIMIZER agent handles:**

**Keyword checks:**
- Primary keyword in meta title, H1, first paragraph, 2-3 H2s
- ~2% body density (naturally distributed, not forced)
- Keyword variations in H3s and image alt text

**Internal link validation:**
- Every internal link must point to a real, existing page
- Validate against internal link data
- Use descriptive anchor text (not "click here")
- 3-5 contextual links per 1,000 words

**Meta generation:**
- Meta title: primary keyword + benefit/hook, under 60 characters
- Meta description: value proposition + CTA, under 155 characters
- 5 title variations, 3 description variations

**Schema markup:**
- Generate JSON-LD based on content type (HowTo, FAQ, Product, etc.)
- Include FAQPage schema for all content with FAQ sections
- Validate schema structure

**Featured snippet targeting:**
- Verify the target snippet section has a 40-60 word direct answer
- Format matches expected snippet type (paragraph/list/table)

### Phase 7: Quality Scoring

**The QUALITY REVIEWER agent performs a holistic review and scores on a 100-point composite:**

| Category | Points | Components |
|----------|--------|------------|
| Content Quality | 30 | Topical completeness (10), Depth/examples per section (10), Originality (10) |
| SEO Optimization | 25 | Keyword placement (8), Internal links verified (5), Meta quality (4), Schema (4), Snippet targeting (4) |
| E-E-A-T Signals | 15 | First-person experience (5), Specific data/examples (5), Source attribution (5) |
| Anti-Slop Score | 15 | Zero Tier 1 phrases (5), Burstiness (3), Voice consistency (3), Horoscope Test (4) |
| AI Citation Ready | 15 | Answer-first formatting (5), FAQ schema (3), Claim-evidence pairs (4), Entity richness (3) |

**The reviewer also checks:**
- Flow and logical progression across the full article
- Voice consistency throughout (not just per-section)
- Information gain elements are present and effective
- EEAT signals are woven in (not bolted on)

**Quality gates:**
- Score < 60: Full rewrite (re-enter Phase 3)
- Score 60-69: Auto-revise weak sections (re-enter Phase 4 for flagged sections)
- Score 70-84: Flag issues for human review, output with annotations
- Score 85+: Ready for publication

**Auto-revision:** Target the weakest scoring category first. If Anti-Slop scored low, run additional editing passes. If E-E-A-T scored low, inject experience signals. Maximum 2 revision cycles (research shows quality degrades beyond this).

## Key Design Decisions

### Sequential, Not Parallel
Each agent needs the previous agent's output. The Writer can't write without the Outline. The Humanizer can't audit without the draft. Parallel execution produces worse results because agents lack context. CrewAI and LangGraph implementations have confirmed that sequential pipelines produce higher quality.

### Context Passing Is Full, Not Summarized
Each agent receives the FULL output of the previous agent, not a summary. Summaries lose critical nuances (specific data points, exact quotes, structural decisions). The exception is section-to-section context within the Writer phase, where compression prevents context distraction.

### Anti-Detection Is Built In, Not Bolted On
The Writer already follows anti-detection guidelines. The Humanizer is a QUALITY GATE, not the primary fix. If the Humanizer has to rewrite more than 20% of the content, the Writer prompt needs improvement.

### Human Input Is Required, Not Optional
The pipeline HALTS at the Writer stage to request human input (case studies, data, opinions). Without this input, the pipeline produces content with zero information gain -- which defeats the entire purpose.

## Output Format

```markdown
---
title: [Generated meta title]
description: [Generated meta description]
keywords: [Primary keyword, secondary keywords]
schema_type: [HowTo | FAQ | Article | Product | etc.]
word_count: [Actual word count]
quality_score: [0-100]
tarsnippet data: [paragraph | list | table | none]
---

# [H1 with primary keyword]

[Article content in Markdown]

---
<!-- Internal links used: [list of URLs] -->
<!-- Schema JSON-LD: [embedded or separate file] -->
<!-- Quality breakdown: Content X/30, SEO X/25, E-E-A-T X/15, Anti-Slop X/15, GEO X/15 -->
```

## Systems Studied

| System | Key Innovation | Adopted |
|--------|---------------|---------|
| SEO Machine | Editor agent targeting AI patterns | Yes -- Phase 4 |
| DonAldente anti-slop | Naive drafter + ruthless critic | Yes -- Phase 3 vs 4 separation |
| claude-blog | Dual Google + AI citation scoring | Yes -- Phase 7 scoring |
| Agentic-SEO-Skill | Confidence labeling on claims | Adapted -- source attribution |
| AutoGen Reflection | JSON-summarized multi-reviewer | Adapted -- structured quality scoring |
| Self-Refine research | 1-2 revision cycles optimal | Yes -- max 2 revision cycles |
| Anthropic context engineering | Just-in-time context loading | Yes -- section compression |

## Common Mistakes

1. **Running all agents with the same LLM temperature**: Researcher needs low temperature (factual), Writer needs medium (creative), Humanizer needs low (precise editing). See the agent table above for recommended values.
2. **Skipping the Fact-Checker**: AI confidently fabricates statistics. One fake stat destroys the entire article's credibility.
3. **Making the pipeline fully autonomous**: Without human input, the pipeline produces high-quality AI slop. Human input at the Writer stage is the critical differentiator.
4. **Post-processing instead of pre-processing**: Anti-detection works 5x better when built into the writing prompt vs applied after.
5. **Monolithic context loading**: Loading all context at once causes performance degradation past 32K tokens. Use section compression and just-in-time context instead.
6. **Over-revising**: More than 2 revision cycles produces diminishing returns and can actually degrade quality. Fix the upstream prompt instead.

## Key Sources

- [TheCraigHewitt/seomachine](https://github.com/TheCraigHewitt/seomachine)
- [DonAldente-AI/anti-slop-system](https://github.com/DonAldente-AI/anti-slop-system)
- [AgriciDaniel/claude-blog](https://github.com/AgriciDaniel/claude-blog)
- [Self-Refine: Iterative Refinement (Learn Prompting)](https://learnprompting.org/docs/advanced/self_criticism/self_refine)
- [Effective Context Engineering (Anthropic)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Building Effective Agents (Anthropic)](https://www.anthropic.com/research/building-effective-agents)
