# Triangulation

> Core value: Ensure data reliability

---

## Definition

Triangulation is a method that uses **multiple independent sources, multiple methods, and multiple perspectives** to verify the same conclusion.

Three dimensions:
1. **Source triangulation**: Different data sources (official data, third-party reports, expert interviews, user surveys)
2. **Method triangulation**: Different research methods (quantitative analysis, qualitative interviews, case studies)
3. **Perspective triangulation**: Different viewpoints (enterprise perspective, user perspective, competitor perspective)

---

## When to Use

**Typical application scenarios**:
- Key data verification
- Multi-source information comparison
- Reducing bias risk
- Improving conclusion credibility

**Usage principles**:
- Multi-source data cross-validation
- Multiple methods complement each other
- Multiple independent analyses

**Verification dimensions**:
- Data source triangulation (different sources)
- Method triangulation (different methods)
- Researcher triangulation (different analysts)
- Theory triangulation (different theoretical perspectives)

---

## Why It Matters

Problems with a single source:
- May be incorrect
- May be outdated
- May be biased
- May be incomplete

Triangulation improves the reliability of conclusions through cross-validation.

---

## Core Principles

**Triangulation is a mandatory step, not optional.**

Every report must:
1. Perform triangulation on core data/conclusions
2. Output a "Data Validation Checklist"

---

## Verification Level Classification

| Level | Verification Degree | Criteria | Notation |
|-------|-------------------|----------|----------|
| **Level A** | Full triangulation | 3 independent sources cross-validated | ✅ High Confidence Level |
| **Level B** | Dual-source verification | 2 independent sources corroborate each other | ⚠️ Medium Confidence Level |
| **Level C** | Single source (credible) | Only 1 source, but source is credible | ⚠️ Low Confidence Level |
| **Level D** | Single source (questionable) | Only 1 source, source credibility questionable | ❌ Reference only |

---

## Operating Steps

### Step 1: Identify Data Requiring Verification

**Must verify**:
- Market size, growth rates
- Competitor data (users, revenue, market share)
- User data (scale, profile, behavior)
- Key industry metrics

**May skip verification**:
- Background information, common knowledge descriptions
- Non-core supplementary data

### Step 2: Find Multiple Sources

**Source priority**:

| Source Type | Credibility | Examples |
|------------|-------------|---------|
| Official data | High | Corporate filings, government statistics, public company announcements |
| Authoritative third-party | Medium-high | iResearch, Analysys, McKinsey reports |
| Media reports | Medium | Major financial media, industry media |
| Corporate self-reported | Medium-low | Official website, PR releases, founder interviews |
| Anonymous/vague sources | Low | "According to industry insiders," "per public data" |

### Step 3: Cross-validate

Compare data from different sources:
- Are they consistent?
- If not, how large is the discrepancy?
- What's the reason for the discrepancy?

### Step 4: Handle Inconsistencies

When sources are inconsistent:

1. **Assess source credibility**
   - Official data > Third-party > Media > Corporate self-reported

2. **Check for scope differences**
   - Are definitions the same? (e.g., "market size" definition)
   - Are time periods the same?
   - Are geographic scopes the same? (e.g., "domestic" vs "global")

3. **Select or estimate**
   - If credibility differs significantly, choose the more credible source
   - If credibility is similar, take a range or median
   - Must explain the selection rationale

### Step 5: Attempt Indirect Verification

When a direct second source cannot be found, attempt indirect verification:

**Logic checks**:
- Is the data internally consistent?
- If market size is 10 billion, is the top company having 8 billion in revenue reasonable?

**Extrapolation from related data**:
- Calculate the target data from related data
- E.g., estimate revenue from user count x ARPU

**Benchmark comparison**:
- Compare with similar industries/companies for reasonableness

### Step 6: Label Verification Level

Label each core data point with its verification level:

```
Market size: 10 billion [Source: iResearch Report | Verification: Level B]
Competitor user count: 5 million [Source: Company website | Verification: Level C]
```

---

## Handling Single Sources

When **all verification methods are exhausted and only a single source remains**:

1. **Assess source credibility**
2. **Attempt indirect verification**
3. **Clearly label**

Example:
```
Data: Industry XX market size approximately 5 billion
Source: iResearch "2024 XX Industry Report" (single source)
Verification level: Level C (single authoritative source, no cross-validation found)
Indirect check: Top company A has revenue of 2 billion, accounting for ~40% market share — logically consistent
Risk note: Recommend supplementing with other sources in future research
```

---

## Output Format

### Data Labeling Format

In the report, after each core data point, label:

```
[Data] [Source: XX | Verification: Level A/B/C/D]
```

### Data Validation Checklist (Mandatory for Reports)

Every report must include at the end:

```markdown
## Data Validation Checklist

### Level A Data (High Confidence)
| Data | Source 1 | Source 2 | Source 3 |
|------|----------|----------|----------|
| Market size 10 billion | iResearch Report | Analysys Data | Top company filing extrapolation |

### Level B Data (Medium Confidence)
| Data | Source 1 | Source 2 | Notes |
|------|----------|----------|-------|
| User base 5 million | Company website | Media report | Two sources corroborate |

### Level C Data (Low Confidence)
| Data | Source | Indirect Check | Risk Note |
|------|--------|---------------|-----------|
| Sub-market size 1 billion | Single report | Logically consistent | Recommend supplementing verification |

### Level D Data (Reference Only)
| Data | Source | Issue | Recommendation |
|------|--------|-------|----------------|
| XX data | Anonymous source | Cannot verify | Not used as key conclusion support |

### Verification Coverage
- Total core data points: X
- Level A: X (X%)
- Level B: X (X%)
- Level C: X (X%)
- Level D: X (X%)
```

---

## Common Mistakes

### Mistake 1: Using Only a Single Source

❌ "Market size is 10 billion" (only one source)
✅ Label the source and verification level, try to find other sources

### Mistake 2: Ignoring Source Credibility

❌ Treating corporate self-reported data as fact
✅ Assess source credibility, cross-validate

### Mistake 3: Not Handling Contradictions

❌ Pretending not to see when sources contradict
✅ Explain the discrepancy, justify the selection

### Mistake 4: Not Creating a Validation Checklist

❌ Report without a Data Validation Checklist
✅ Every report must have a validation checklist

---

## Application in This Skill

### Stage 4 Research Execution

1. When collecting data, actively seek multiple sources
2. Perform triangulation on core data
3. Record in `evidence_base.md`

### Stage 6 Report Generation

1. Label each core data point with verification level
2. Append Data Validation Checklist at the end of the report
3. Level D data must not support key conclusions

---

## Relationship with Other Methodologies

- **Hypothesis-driven method**: Triangulation ensures the reliability of hypothesis validation
- **ACH (Analysis of Competing Hypotheses)**: Triangulation provides reliable evidence
- **Anti-patterns**: Triangulation avoids the "single-source dependency" anti-pattern
