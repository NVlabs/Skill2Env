# Hypothesis-driven Method

> Source: McKinsey & Company
> Core value: Improve analysis efficiency, avoid aimless exploration

---

## Definition

Hypothesis-driven is a working method:

1. First propose **testable hypotheses**
2. Then design **a research plan to validate hypotheses**
3. Use data to **prove or disprove hypotheses**
4. Based on results, **iterate or draw conclusions**

Opposite of "collect information first, then find conclusions," hypothesis-driven means "hypothesis first, then validate."

---

## When to Use

**Typical application scenarios**:
- Time-constrained rapid analysis
- Data-rich environments requiring focus
- Validation-oriented research
- Strategic decision support

**Usage principles**:
- Form hypotheses based on experience and initial insights
- Validate or falsify hypotheses with data
- Avoid confirmation bias, actively seek opposing evidence

**Usage flow**:
1. Initial hypothesis (based on experience/intuition)
2. Design validation (what data is needed)
3. Collect data (targeted search)
4. Validate/revise (update hypotheses)

---

## Why It Matters

| Approach | Process | Efficiency | Risk |
|----------|---------|------------|------|
| Information-driven | Broadly collect information first → Then distill conclusions | Low, prone to "analysis paralysis" | Information overload, can't find the key point |
| Hypothesis-driven | Propose hypothesis first → Targeted validation | High, focused on key questions | May miss things, supplement with MECE |

---

## Operating Steps

### Step 1: Propose Initial Hypotheses

Based on available information and intuition, propose **testable hypotheses**.

Good hypothesis criteria:
- **Specific**: Not "the competitor is strong," but "Competitor A's user growth rate is 2x ours"
- **Testable**: Data can be found to prove or disprove it
- **Debatable**: Uncertainty exists, worth validating

❌ "The competitor is doing well" — Not testable
✅ "Competitor A's growth is primarily driven by subsidy strategy" — Testable

### Step 2: Decompose Hypotheses

Break down hypotheses into **validation conditions**: If the hypothesis is true, what should we observe?

```
Hypothesis: Competitor A's growth is primarily driven by subsidy strategy

Validation conditions:
1. Competitor A's subsidy intensity > industry average
2. Competitor A's subsidized user growth > non-subsidized users
3. Competitor A's user growth drops after subsidies stop
```

### Step 3: Design the Validation Plan

For each validation condition, design:
- What data is needed?
- Where to obtain it?
- How to analyze it?

### Step 4: Execute Validation

Collect data, validate or disprove hypotheses.

**Key: Actively seek counterexamples (falsification thinking)**

Don't only look for evidence supporting the hypothesis. Actively ask:
- Under what circumstances would the hypothesis not hold?
- Are there counterexamples?

### Step 5: Iterate or Conclude

- **Hypothesis validated**: A conclusion can be drawn
- **Hypothesis disproved**: Propose a new hypothesis, re-validate
- **Partially validated**: Revise the hypothesis, continue validation

---

## Embedded Elements

### Falsification Thinking

**Core principle**: Actively seek evidence that could prove the hypothesis wrong.

Operating method:
- For each hypothesis, after listing "what we should observe if true," add "what we should observe if false"
- When searching keywords, search both positive and negative keywords
- When encountering opposing evidence, take it seriously rather than ignoring it

Example:
```
Hypothesis: Competitor's growth comes from subsidies

Supporting evidence:
- Competitor's subsidy intensity is high
- Subsidized user growth is fast

Opposing evidence (must actively seek):
- Competitor's non-subsidized user growth is also fast → Suggests subsidies aren't the only reason
- Competitor's growth didn't drop after subsidies stopped → Suggests subsidies aren't the main driver
```

### Bayesian Thinking

**Core principle**: Judgments are probabilistic, continuously updated with new evidence.

Operating method:
- Don't say "the competitor will definitely enter," say "probability of competitor entry is approximately 60%"
- Update probability judgment with each new piece of evidence
- Mark confidence level in the final report

Example:
```
Initial judgment: Probability of competitor entering new market 30%
New evidence 1: Competitor hired a team in this field → Updated to 50%
New evidence 2: Competitor CEO publicly denied it → Updated to 30%
New evidence 3: Competitor registered related trademarks → Updated to 60%

Final conclusion: Competitor entry probability approximately 60%, recommend close monitoring
```

---

## How to Express Hypotheses

### Good Hypotheses

| Criteria | ❌ Poor Hypothesis | ✅ Good Hypothesis |
|----------|---------------------|----------------------|
| Specific | "Market has opportunities" | "Segment X market size will double within 2 years" |
| Testable | "Users like this feature" | "Feature A usage rate > 50%" |
| Debatable | "Competitor is strong" | "Competitor A's user retention is 20% higher than ours" |

### Sources of Hypotheses

1. **User input**: The user's existing judgments or questions
2. **Preliminary research**: Intuition after a quick scan
3. **Framework derivation**: Possible situations derived from analytical frameworks
4. **Counter-intuitive**: Hypotheses contrary to common belief (often the most valuable)

---

## Application in This Skill

### Stage 3 Hypothesis Generation

1. Based on the Research Definition, generate 3-7 core hypotheses
2. **Each hypothesis must be tagged with the corresponding Stage 2 sub-question number and analysis Lens** (Q→H→Lens mapping)
3. Sub-questions without hypotheses must note the reason (e.g., "factual compilation type, no hypothesis set")
4. Decompose each hypothesis into validation conditions
5. Design the validation plan
6. Output to `research_plan.md`

### Stage 4 Research Execution

1. Collect data per the validation plan
2. Actively seek opposing evidence
3. Update hypothesis probability
4. Record in `evidence_base.md`

### Output Format

```markdown
## Hypothesis List

### Q→H→Lens Mapping Overview

| # | Hypothesis | Corresponding Sub-question | Analysis Lens |
|---|-----------|---------------------------|---------------|
| H1 | [Hypothesis statement] | Q2 [Sub-question name] | [Framework dimension, e.g., PESTEL-E] |
| H2 | [Hypothesis statement] | Q3 [Sub-question name] | [Framework dimension, e.g., Five Forces-Competition] |
| H3 | [Hypothesis statement] | Q4 [Sub-question name] | [Framework dimension, e.g., BMC] |

> Sub-questions without hypotheses: Q1 (factual compilation), Q5 (integrated analysis)
> Analysis Lens inherited from `research_definition.md` sub-question lens assignment

### H1: [Hypothesis statement] (← Q2 [Sub-question name] | Lens: [Framework dimension])
- Confidence Level: [Initial probability]
- Validation conditions:
  1. [Condition 1]
  2. [Condition 2]
- Validation plan:
  - Data sources: [List]
  - Analysis methods: [List]
- Current status: [Pending/Validated/Disproved]

### H2: ...
```

---

## Common Mistakes

### Mistake 1: Hypothesis Too Vague

❌ "Competitor has advantages"
✅ "Competitor A's customer acquisition cost is 30% lower than ours"

### Mistake 2: Hypothesis Not Testable

❌ "Users' latent demand is high"
✅ "60% of users in the survey expressed demand for X"

### Mistake 3: Only Finding Supporting Evidence

❌ Only searching "competitor subsidy success"
✅ Simultaneously searching "competitor subsidy success" and "competitor subsidy failure"

### Mistake 4: Reluctance to Disprove Hypotheses

❌ Forcing explanations when counterexamples are found
✅ Acknowledge the hypothesis doesn't hold, propose a new one

---

## Relationship with Other Methodologies

- **MECE Principle**: Hypothesis List should be MECE, covering all possibilities
- **Issue Tree**: Issue Tree can be transformed into a Hypothesis List
- **ACH**: Use ACH for systematic hypothesis validation at critical junctures
- **Triangulation**: Use multi-source data to validate hypotheses
