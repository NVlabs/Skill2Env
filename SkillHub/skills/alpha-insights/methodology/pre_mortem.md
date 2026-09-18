# Pre-mortem

> Core value: Identify risks and discover overlooked opportunities

---

## Definition

Pre-mortem is a **reverse thinking** method:

1. Assume the project/decision **has already failed**
2. Reason backward to identify possible causes of failure
3. Design countermeasures in advance

Distinction from traditional risk assessment:
- Traditional: What might go wrong?
- Pre-mortem: It has already failed. Why?

Psychological research shows that "imagining failure" identifies 30-50% more issues than "predicting risks."

---

## When to Use**:
- Before major decisions
- Before project launch
- Risk assessment
- Strategic plan validation

**Usage principles**:
- Reverse thinking (reason backward from failure)
- Psychological safety (encourage candor)
- Be specific (avoid vague generalities)

**Usage flow**:
1. Set the scenario (assume failure one year from now)
2. Independent brainstorming (each person writes 3-5 causes)
3. Aggregate and classify (affinity diagram)
4. Develop prevention measures (for top risks)

---

## Why It Matters

| Approach | Psychological State | Effect |
|----------|-------------------|--------|
| Traditional risk assessment | Optimistic, "it should be fine" | Easy to overlook risks |
| Pre-mortem | Assume failure is already a fact | Willing to speak truth, discover problems |

---

## Dual Use

In this Skill, Pre-mortem has two purposes:

### Purpose 1: Identify Execution Risks

Assume the recommendation has failed, and reason backward to identify risk factors.

### Purpose 2: Discover Analysis Gaps

Assume the analysis has failed (wrong conclusions/missed key points), reason backward to identify possible causes, and go back to supplement the analysis.

---

## Operating Steps

### Purpose 1: Identify Execution Risks

**Step 1: Set the Failure Scenario**

Assume the recommendation failed after 6 months of execution.

Example:
"Assume we entered Market X, but 6 months later the project failed and we withdrew."

**Step 2: Reason Backward to Identify Failure Causes**

Ask: Why did it fail? List all possible causes.

Example:
```
Failure causes:
1. Customer acquisition cost far exceeded expectations
2. Competitor retaliation was fiercer than anticipated
3. Insufficient team execution capability
4. Sudden policy tightening
5. Supply chain issues
```

**Step 3: Assess Each Cause's Likelihood**

For each cause, assess:
- Likelihood of occurrence
- Impact severity
- Whether it can be addressed in advance

**Step 4: Design Countermeasures**

For high-risk factors, design response plans.

Example:

| Risk | Likelihood | Impact | Countermeasure |
|------|-----------|--------|----------------|
| CAC exceeds expectations | High | High | Small-scale pilot to validate CAC first |
| Competitor retaliation | Medium | High | Prepare differentiated positioning plan |
| Policy tightening | Low | High | Closely monitor policy developments |

---

### Purpose 2: Discover Analysis Gaps

**Step 1: Set the Failure Scenario**

Assume the report's conclusions turned out to be wrong.

Example:
"Assume that 1 year later, our conclusion of 'should enter Market X' proved to be wrong."

**Step 2: Reason Backward to Identify Possible Causes**

Ask: Why was the conclusion wrong? What might have been overlooked?

Example:
```
Possible oversights:
1. Underestimated the competitor's moat
2. Overestimated user demand
3. Ignored policy risks
4. Biased data sources
5. Insufficient hypothesis validation
```

**Step 3: Review**

For each possible oversight, go back and check:
- Was it actually overlooked?
- Does supplementary analysis need to be added?

**Step 4: Supplement the Analysis**

For confirmed oversights, conduct additional research.

---

## Trigger Conditions

### Purpose 1: Identify Execution Risks

After Stage 5 Insight Synthesis, **automatically used when core recommendations/action plans exist**.

### Purpose 2: Discover Analysis Gaps

After Stage 5 Insight Synthesis, when:
- The analysis involves major decisions
- Evidence contains contradictions
- The user has concerns about the conclusions

---

## Output Format

### Execution Risk Version

```markdown
## Pre-mortem: Execution Risk Analysis

### Failure Scenario
Assume [recommendation] fails after 6 months of execution.

### Possible Failure Causes
| Cause | Likelihood | Impact | Countermeasure |
|-------|-----------|--------|----------------|
| [Cause 1] | High/Med/Low | High/Med/Low | [Measure] |
| [Cause 2] | ... | ... | ... |

### Key Risk Alerts
[List high-risk factors]
```

### Analysis Gap Version

```markdown
## Pre-mortem: Analysis Completeness Check

### Failure Scenario
Assume the conclusion "[core conclusion]" proved to be wrong.

### Possible Oversights
| Oversight | Check Result | Needs Supplementing |
|-----------|-------------|---------------------|
| [Oversight 1] | Covered/Not covered | Yes/No |
| [Oversight 2] | ... | ... |

### Supplementary Analysis
[List analyses that need to be added]
```

---

## Common Mistakes

### Mistake 1: Only Listing Risks Without Prioritizing

❌ Listing 20 risks with no focus
✅ Assess likelihood and impact, focus on key risks

### Mistake 2: Only Finding External Causes

❌ All failure causes are "competitors, policy, market"
✅ Also consider internal causes (execution, resources, capabilities)

### Mistake 3: Not Designing Countermeasures

❌ Only listing risks without saying what to do
✅ Every key risk should have a countermeasure

---

## Application in This Skill

### After Stage 5 Insight Synthesis

1. Pre-mortem is automatically triggered
2. Execute both purposes:
   - Identify execution risks
   - Discover analysis gaps
3. Output to `insights.md`

---

## Relationship with Other Methodologies

- **Red Team thinking**: Pre-mortem is a lightweight version of Red Team thinking
- **Hypothesis-driven method**: Pre-mortem helps discover gaps in hypothesis validation
- **Anti-patterns**: Pre-mortem helps discover potentially triggered anti-patterns
