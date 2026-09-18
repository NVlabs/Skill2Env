# Analysis of Competing Hypotheses (ACH)

> Core value: Systematically overcome confirmation bias, improve judgment accuracy

---

## Definition

ACH (Analysis of Competing Hypotheses) is a method for **systematically validating multiple competing hypotheses**:

1. List **all possible hypotheses** (including those you disagree with)
2. List **all evidence**
3. Build a "hypothesis x evidence" matrix
4. Assess how each piece of evidence supports/refutes each hypothesis
5. **The hypothesis least supported by evidence may actually be the correct one**

---

## When to Use

**Typical application scenarios**:
- Intelligence analysis and competitive intelligence
- Multi-hypothesis evaluation
- High-uncertainty decisions
- Strategic forecasting

**Usage principles**:
- List all reasonable hypotheses
- Use an evidence matrix for systematic evaluation
- Falsification over confirmation

**Usage flow**:
1. List hypotheses (all possibilities)
2. Collect evidence (supporting and opposing)
3. Build matrix (evidence vs. hypotheses)
4. Assess consistency (strong falsifying evidence)
5. Form judgment (most likely hypothesis)

---

## Why It Matters

The pitfall of traditional thinking:
- Start with a preferred hypothesis
- Only look for evidence supporting that hypothesis
- Ignore or downplay opposing evidence
- Arrive at a biased conclusion

ACH overcomes confirmation bias systematically by **forcing consideration of all possibilities**.

---

## Trigger Conditions

Activate when **2 or more** of the following are met:

| Condition | Judgment Criteria |
|-----------|-------------------|
| Conclusion criticality | The judgment directly impacts a major decision (enter/don't enter, invest/don't invest) |
| Hypothesis diversity | 3 or more reasonable, mutually competing hypotheses exist |
| High bias risk | The analyst or user has an obvious inclination |
| Evidence complexity | Evidence is contradictory or comes from diverse sources |

---

## Operating Steps

### Step 1: List All Possible Hypotheses

Based on available information, list **all reasonable hypotheses**, including those you disagree with.

Criteria:
- Each hypothesis should be possible (not obviously wrong)
- Hypotheses are mutually competing (only one can be correct)
- Typically 3-6 hypotheses

Example:
```
Question: Why is Competitor A growing fast?

Hypotheses:
H1: Aggressive subsidy strategy
H2: Better product experience
H3: Successful channel expansion
H4: Accumulated brand effect
```

### Step 2: List All Evidence

Collect **all evidence** related to the question, including:
- Evidence supporting a hypothesis
- Evidence opposing a hypothesis
- Neutral evidence related to multiple hypotheses

Example:
```
E1: Competitor A's marketing spend grew 200% YoY
E2: Competitor A's user satisfaction at 85%, above industry average
E3: Competitor A ranks #1 in Douyin and Xiaohongshu ad spend
E4: After Competitor A stopped subsidies, user growth dropped 30%
E5: Competitor A's product iteration speed is 2x the industry average
E6: Competitor A's NPS score is continuously rising
```

### Step 3: Build the Evidence Matrix

Build a "hypothesis x evidence" matrix, assessing each piece of evidence's impact on each hypothesis.

Symbols:
- `+` Supports
- `++` Strongly supports
- `-` Opposes
- `--` Strongly opposes
- `N` Neutral/irrelevant
- `?` Uncertain

Example:

| Evidence | H1:Subsidy | H2:Product | H3:Channel | H4:Brand |
|----------|------------|------------|------------|----------|
| E1: Marketing +200% | + | N | + | + |
| E2: Satisfaction 85% | N | ++ | N | + |
| E3: #1 Douyin spend | + | N | ++ | + |
| E4: Growth -30% after subsidy stop | ++ | - | - | - |
| E5: Fast iteration | N | ++ | N | + |
| E6: NPS rising | N | + | N | ++ |

### Step 4: Analyze the Matrix

**Key principle: Focus on evidence "discriminating power," not quantity**

- Some evidence supports all hypotheses → Low discriminating power, low value
- Some evidence only supports/opposes specific hypotheses → High discriminating power, high value

Analysis of the example above:
- E2, E5 strongly support H2 (good product)
- E4 strongly supports H1 (subsidy is the main driver), while opposing H2, H3, H4
- E3 supports H3 (channel), but also supports H1, H4

### Step 5: Draw Conclusions

**Don't look at which hypothesis has "the most support" — look at which hypothesis has "the least refutation"**

Calculation method:
1. Count the `+`, `++`, `-`, `--` for each hypothesis
2. Focus on `--` (strong opposition) evidence
3. Hypotheses opposed by `--` evidence have significantly reduced likelihood

Example conclusion:
- H1 (Subsidy): Supported by E1, E3, E4, no strong opposition → High likelihood
- H2 (Product): Supported by E2, E5, E6, but opposed by E4 → Medium likelihood
- H3 (Channel): Supported by E3, but opposed by E4 → Low likelihood
- H4 (Brand): Supported by E1, E6, but opposed by E4 → Low likelihood

**Overall judgment**: The competitor's growth is primarily driven by subsidy strategy, with product experience as a secondary factor.

### Step 6: Sensitivity Analysis

Question: If a piece of evidence were wrong, would the conclusion change?

- Key evidence: E4 (growth drop after subsidy stop) — If this evidence is incorrect, the conclusion could reverse
- Recommendation: Further verify the reliability of E4

---

## Output Format

```markdown
## ACH Analysis Results

### Question
[The question being analyzed]

### Hypothesis List
| # | Hypothesis |
|---|-----------|
| H1 | [Hypothesis 1] |
| H2 | [Hypothesis 2] |
| H3 | [Hypothesis 3] |

### Evidence Matrix
| Evidence | H1 | H2 | H3 |
|----------|----|----|----|
| E1 | + | N | - |
| E2 | ++ | - | N |
| E3 | - | ++ | + |

### Analysis Conclusion
- Most likely correct hypothesis: H1
- Reasoning: [Explanation]
- Key evidence: [List high-discriminating evidence]
- Sensitivity: [Which evidence, if wrong, would affect the conclusion]

### Confidence Level
[High/Medium/Low]
```

---

## Common Mistakes

### Mistake 1: Incomplete Hypotheses

❌ Only listing hypotheses you agree with
✅ Listing all reasonable hypotheses, including ones you disagree with

### Mistake 2: Biased Evidence

❌ Only collecting evidence supporting a specific hypothesis
✅ Collecting all relevant evidence, including neutral and opposing

### Mistake 3: Only Counting Support

❌ Choosing whichever hypothesis has the most `+`
✅ Focus on `--` (strong opposition), eliminate refuted hypotheses

### Mistake 4: Ignoring Sensitivity

❌ Not verifying the reliability of key evidence
✅ Identify key evidence and further verify

---

## Application in This Skill

### Stage 3 Hypothesis Validation

1. When trigger conditions are met, auto-load and notify the user (per `_index.md` Tier 2 notification template)
2. Execute step by step
3. Output to the ACH analysis section of `research_plan.md`

### Relationship with Hypothesis-driven Method

- **Hypothesis-driven method**: The overall working approach
- **ACH**: An enhanced validation tool for critical judgments

ACH is the "upgrade" of hypothesis-driven method, used for more critical and complex judgments.
