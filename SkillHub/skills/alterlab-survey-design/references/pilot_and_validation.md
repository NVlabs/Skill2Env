# Pilot Testing and Instrument Validation

Three-phase pilot testing protocol plus reliability (Cronbach's alpha, item-total correlations), the validity-types table, and exploratory factor analysis code. Extracted from the Survey Design skill body.

## Pilot Testing

**Three-Phase Pilot Testing Protocol:**

```markdown
## Phase 1: Expert Review (n = 3-5 experts)

### Content Validity
- Do items adequately cover the construct?
- Are any important facets missing?
- Are items relevant to the target population?
- Content Validity Index (CVI): Rate each item as
  1 = Not relevant, 2 = Somewhat relevant, 3 = Quite relevant, 4 = Highly relevant
  Item-CVI = proportion of experts rating 3 or 4 (threshold: ≥ 0.78)
  Scale-CVI/Ave = mean of Item-CVIs (threshold: ≥ 0.90)

### Face Validity
- Do items appear to measure what they claim?
- Is the language clear and appropriate?
- Is the survey length reasonable?

---

## Phase 2: Cognitive Interviews (n = 5-10 from target population)

### Think-Aloud Protocol
"Please read each question out loud and tell me what you are thinking
as you decide on your answer."

### Probing Questions
- "What does [term] mean to you?"
- "How did you arrive at your answer?"
- "Was this question easy or difficult to answer? Why?"
- "Can you put this question in your own words?"
- "Is there anything confusing about this question?"
- "Would you change anything about this question?"

### Document
- Items that cause confusion or hesitation
- Items interpreted differently than intended
- Items where response options do not fit
- Suggested wording improvements
- Time to complete each section

---

## Phase 3: Quantitative Pilot (n = 30-50 from target population)

### Assess
- [ ] Completion rate and completion time
- [ ] Item-level missing data (flag items with >10% missing)
- [ ] Response distributions (flag items with >90% in one category)
- [ ] Internal consistency (Cronbach's alpha per subscale)
- [ ] Item-total correlations (flag items < 0.30)
- [ ] Inter-item correlations (flag pairs > 0.85 — redundancy)
- [ ] Open-ended feedback on survey experience
- [ ] Technical issues (display, skip logic, mobile compatibility)
```

## Instrument Validation

### Reliability

**Internal Consistency:**

```python
import pandas as pd
import numpy as np

def cronbachs_alpha(df):
    """
    Calculate Cronbach's alpha for a set of items.
    df: DataFrame where each column is an item and each row is a respondent.
    """
    n_items = df.shape[1]
    item_variances = df.var(axis=0, ddof=1)
    total_variance = df.sum(axis=1).var(ddof=1)

    alpha = (n_items / (n_items - 1)) * (1 - item_variances.sum() / total_variance)
    return alpha

# Example
data = pd.DataFrame({
    'item1': [4, 3, 5, 4, 3, 5, 4, 3, 2, 4],
    'item2': [3, 3, 4, 4, 2, 5, 4, 3, 3, 4],
    'item3': [4, 4, 5, 3, 3, 4, 5, 2, 3, 5],
    'item4': [3, 2, 4, 4, 3, 5, 4, 3, 2, 3],
})

alpha = cronbachs_alpha(data)
print(f"Cronbach's alpha: {alpha:.3f}")

# Interpretation:
# α ≥ 0.90  Excellent (but check for redundancy)
# 0.80 ≤ α < 0.90  Good
# 0.70 ≤ α < 0.80  Acceptable
# 0.60 ≤ α < 0.70  Questionable
# α < 0.60  Poor — revise items
```

**Item-Total Correlations:**

```python
def item_total_correlations(df):
    """Calculate corrected item-total correlations."""
    results = {}
    for col in df.columns:
        rest = df.drop(columns=col).sum(axis=1)
        corr = df[col].corr(rest)
        results[col] = round(corr, 3)
    return results

itc = item_total_correlations(data)
for item, corr in itc.items():
    flag = " ← REVIEW" if corr < 0.30 else ""
    print(f"  {item}: r = {corr}{flag}")
```

### Validity

| Type | Question | Method |
|------|----------|--------|
| **Content validity** | Do items cover the construct adequately? | Expert review, CVI calculation |
| **Face validity** | Do items appear to measure the construct? | Target population review |
| **Construct validity** | Does the instrument measure the theoretical construct? | Factor analysis (EFA/CFA) |
| **Convergent validity** | Does it correlate with similar measures? | Correlation with established instruments (r > 0.50) |
| **Discriminant validity** | Is it distinct from different constructs? | Low correlation with theoretically unrelated measures (r < 0.30) |
| **Criterion validity (concurrent)** | Does it correlate with a current criterion? | Correlation with gold standard measured simultaneously |
| **Criterion validity (predictive)** | Does it predict a future outcome? | Correlation with criterion measured later |
| **Known-groups validity** | Can it distinguish groups known to differ? | Compare scores between groups that should differ |

**Exploratory Factor Analysis (EFA):**

```python
from factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity, calculate_kmo

# Check suitability for factor analysis
chi_square, p_value = calculate_bartlett_sphericity(data)
print(f"Bartlett's test: χ² = {chi_square:.2f}, p = {p_value:.4f}")
# p < 0.05 → suitable for factor analysis

kmo_all, kmo_model = calculate_kmo(data)
print(f"KMO: {kmo_model:.3f}")
# KMO > 0.60 → suitable; > 0.80 → good; > 0.90 → excellent

# Determine number of factors (parallel analysis)
fa = FactorAnalyzer(rotation=None, n_factors=data.shape[1])
fa.fit(data)
eigenvalues, _ = fa.get_eigenvalues()
print("Eigenvalues:", [f"{ev:.3f}" for ev in eigenvalues])
# Retain factors with eigenvalue > 1 (Kaiser criterion)
# Also use scree plot and parallel analysis

# Run EFA with chosen number of factors
fa = FactorAnalyzer(n_factors=2, rotation='oblimin', method='ml')
fa.fit(data)

# Factor loadings
loadings = pd.DataFrame(
    fa.loadings_,
    index=data.columns,
    columns=[f'Factor {i+1}' for i in range(2)]
)
print("\nFactor Loadings:")
print(loadings.round(3))
# Items should load ≥ 0.40 on one factor and < 0.30 on others
```
