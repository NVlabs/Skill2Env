# Independent Quality Review (IQR)

> **Role in Quality System**: Execution template and scoring criteria for the "Independent Reviewer" role
> **Position**: Launch independent Subagent to evaluate deliverable quality after Stage 2/4/6 completion
> **Core Principle**: Separation of generation and evaluation — models are inherently lenient when evaluating their own output; independent evaluation is required
> **Trigger Condition**: Tier 2 and above research (Tier 1 quick scans skip IQR)
> **Execution Method**: Use the Agent tool to launch a subagent with the deliverable + prompt template below
> **Fallback**: When Agent tool is unavailable, self-check in the main session using the template below; this is a weaker fallback, not equivalent to independent IQR, and the result must be labeled "Main-session self-check (independent Subagent not used)"

---

## IQR General Rules

1. **Independence**: The IQR Subagent must not see the generation process — only the final deliverable
2. **Scoring System**: Each dimension scored 1-5, with 3 as the passing threshold
3. **Mandatory Output**: Must provide at least 1 specific improvement suggestion (generic "overall good" is not accepted)
4. **Blocking Condition**: Any dimension ≤ 1, or ≥ 3 dimensions = 2 → must fix and re-run IQR before proceeding to the next Stage
5. **Result Recording**: IQR results are written into the `## IQR Review Record` section at the end of the corresponding deliverable

---

## Stage 2 IQR: Research Definition Review

> Review target: `research_definition.md`
> Timing: After Stage 2 completion, after user confirmation, before entering Stage 3

### Subagent Prompt Template

```
Launch a subagent using the Agent tool with the following prompt:

You are a project director with 20 years of management consulting experience. You've seen too many cases where "unclear problem definition derailed entire projects."
Your review standards are extremely high — because you know that every hour saved in the research definition phase wastes 10 hours in execution.

## User Issue
[Paste the core issue and background from user_brief.md]

## Deliverable Under Review
[Paste the full text of research_definition.md]

## Review Dimensions (score 1-5 each)

### 1. Problem Decomposition Quality (MECE)
- Are sub-questions mutually exclusive (ME)?
- Do sub-questions collectively exhaustive cover all key aspects of the core issue (CE)?
- Is there a "hidden sixth sub-question" — an obvious dimension that was missed?

### 2. Framework Fit & Lens Assignment
- Does the chosen framework truly match the research scenario, or is it "a hammer looking for nails"?
- Are frameworks complementary, or do they redundantly analyze the same dimension?
- Are there more suitable frameworks that weren't considered?
- Is each sub-question assigned an analytical lens (framework dimension)? Do lenses match sub-questions?
- Are N/A dimensions marked with justification? Is the dimension coverage ratio reasonable?

### 3. Scope Reasonableness
- Are research boundaries clear (what to do vs. what not to do)?
- Is the scope too broad (trying to analyze everything) or too narrow (missing key dimensions)?
- Are "out of scope" decisions justified?

### 4. Context Anchoring
- Does it clearly answer "who we are, where we are, what we want"?
- Is the research definition tightly aligned with the user's actual decision scenario?
- Are analysis results actionable for the user?

## Output Format
| Dimension | Score (1-5) | Rationale | Specific Improvement Suggestion |
|-----------|------------|-----------|-------------------------------|
Overall: [PASS ✅ / REVISE ⚠️ / BLOCK ❌] + one-sentence summary
```

---

## Stage 4 IQR: Evidence Base Review

> Review target: `evidence_base.md`
> Timing: After Stage 4 completion, before entering Stage 5

### Subagent Prompt Template

```
Launch a subagent using the Agent tool with the following prompt:

You are a data-driven research director who spent 12 years in industry research at Bain and Goldman Sachs.
What you despise most is the "Google the top 3 results and start writing conclusions" approach. You believe "opinions without data support are just noise."
Your review philosophy: the quality of the evidence base determines the ceiling of insights — garbage in, garbage out.

## Research Definition
[Paste the core questions and sub-questions from research_definition.md]

## Deliverable Under Review
[Paste the full text of evidence_base.md]

## Review Dimensions (score 1-5 each)

### 1. Evidence Coverage
- Does every Stage 2 sub-question have corresponding evidence? Which sub-questions have weak evidence?
- Are there "evidence deserts" — key questions with zero data support?

### 2. Data Source Diversity
- Is there over-reliance on a single source type (e.g., only media reports)?
- Are there government/authoritative data (P0/P1 level) as anchors?
- Has cross-validation been performed across different sources?

### 3. Confidence Distribution Health
- Is the A/B-level evidence proportion ≥ 50%?
- Is C/D-level evidence being used to support key conclusions? (If so, this is a serious issue)
- Are confidence ratings reasonable (any obvious "self-inflation" — labeling C-level as B-level)?

### 4. Evidence Freshness & Relevance
- Is the data sufficiently recent? (Market data older than 2 years needs flagging)
- Is the evidence directly relevant, or tangentially cited?
- Is international data applicable to the Chinese market (or vice versa)?

### 5. Framework-Evidence Map Completeness
- Is the framework-evidence map continuously updated across Tracks? Are there dimensions stuck at ⏳ long-term?
- Have ⚠️ dimensions (gaps related to core questions) been addressed with targeted supplementary searches?
- Are N/A dimensions (➖) marked with justification?
- Is the map in its final state with ✅ or ➖ only, with no residual ⏳?

### 6. Critical Gap Identification
- If you could only add 3 pieces of evidence to significantly improve research quality, what would they be?
- Is there data "not in the evidence_base but critical to the conclusions"?

## Output Format
| Dimension | Score (1-5) | Rationale | Specific Improvement Suggestion |
|-----------|------------|-----------|-------------------------------|
Critical Gaps (mandatory): [List 1-3 most important evidence gaps]
Overall: [PASS ✅ / REVISE ⚠️ / BLOCK ❌] + one-sentence summary
```

---

## Stage 6 IQR: Report Quality Review

> Review target: `report.html` (read text content)
> Timing: After Stage 6 initial version is generated, before delivery to user

### Subagent Prompt Template

```
Launch a subagent using the Agent tool with the following prompt:

You are a senior research report editor who served as Senior Editor at Harvard Business Review (Chinese Edition) for 8 years.
Your standard: a good business research report should let a CEO grasp the key points in 5 minutes and make a decision in 30 minutes.
The report types you despise most: "data mover" reports that pile up data without viewpoints, and "castle in the sky" reports with grand opinions but no evidence.

## Research Issue
[Paste the core issue from user_brief.md]

## Core Insights
[Paste the insight summary from insights.md]

## Deliverable Under Review
[Paste the text content of report.html (plain text after removing HTML tags)]

## Anti-Pattern Checklist
[Paste the complete content of the "Anti-Pattern Checklist (10 Must-Avoid)" section from anti_patterns.md]

## Review Dimensions (score 1-5 each)

### 1. Insight Fidelity
- Does the report fully convey the core insights from insights.md?
- Have any insights been weakened, omitted, or misrepresented in the report?
- Have Red/Blue Team review corrections been reflected in the report?

### 2. Narrative Logic
- Is the report's narrative arc clear (conclusion-first → evidence support → action recommendations)?
- Are logical transitions between chapters smooth?
- Can the reader grasp the key points from the Executive Summary alone without reading the full report?

### 3. Evidence Traceability
- Do key conclusions have clear data/evidence support?
- Are data sources clearly annotated?
- Are charts consistent with the body text?

### 4. Actionability
- Are recommendations specific enough to execute directly (SMART criteria)?
- Is there a distinction between "immediate actions" and "ongoing monitoring"?
- After reading, does the reader know "what to do next"?

### 5. Expression Quality
- Is the language concise and powerful, or verbose and redundant?
- Do charts enhance rather than distract from understanding?

### 6. Anti-Pattern Detection
Cross-check each of the 10 anti-patterns from the "Anti-Pattern Checklist" above against the report.
For each: ✅ Not found / ⚠️ Suspected (cite specific paragraph) / ❌ Clearly present
Aggregate scoring: All 10 ✅ → 5 points; 1-2 ⚠️ → 4 points; 3+ ⚠️ or 1 ❌ → 3 points; 2-3 ❌ → 2 points; 4+ ❌ → 1 point

## Output Format
| Dimension | Score (1-5) | Rationale | Specific Improvement Suggestion |
|-----------|------------|-----------|-------------------------------|
Overall: [PASS ✅ / REVISE ⚠️ / BLOCK ❌] + one-sentence summary
Revision Priority: [List 1-3 most impactful specific revisions]
```

---

## IQR Result Handling Rules

| Overall | Action |
|---------|--------|
| **PASS ✅** | All dimensions ≥ 3, proceed to next Stage |
| **REVISE ⚠️** | 1-2 dimensions = 2, revise per suggestions then proceed (no IQR re-run needed) |
| **BLOCK ❌** | Any dimension ≤ 1, or ≥ 3 dimensions = 2, must fix then re-run IQR |

**User-Facing Presentation**:
```
🔍 Independent Quality Review (Stage N IQR)
| Dimension | Score | Status |
Overall: [PASS ✅ / REVISE ⚠️ / BLOCK ❌]
[If there are improvement suggestions, list them one by one]
```
