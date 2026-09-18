# Survey Methodology Reference

## 1. Scale Development Process (DeVellis & Thorpe, 2022)

### Eight Steps of Scale Development

| Step | Description | Key Activities |
|------|-------------|---------------|
| 1. Determine clearly what you want to measure | Conceptual definition | Literature review; theoretical framework; distinguish from related constructs |
| 2. Generate an item pool | Write candidate items | Over-generate (3-4x final items); review existing instruments; expert input |
| 3. Determine the format for measurement | Choose response format | Likert, semantic differential, VAS; number of response options; labels |
| 4. Have initial item pool reviewed by experts | Content validity assessment | Subject matter experts rate relevance, clarity, representativeness; compute CVI |
| 5. Consider inclusion of validation items | Plan for bias detection | Social desirability scale; attention checks; lie scales |
| 6. Administer items to a development sample | Data collection | n ≥ 300 for factor analysis; representative of target population |
| 7. Evaluate the items | Psychometric analysis | Item analysis, factor analysis, reliability; refine item set |
| 8. Optimize scale length | Final item selection | Balance reliability with parsimony; short form development if needed |

### Item Analysis Decision Table

| Statistic | Threshold | Action |
|-----------|-----------|--------|
| Item mean | Extreme (near floor or ceiling) | Consider removing — low discriminating power |
| Item variance | Very low | Consider removing — insufficient variability |
| Corrected item-total correlation | < 0.30 | Remove or revise — poor relation to construct |
| Corrected item-total correlation | > 0.80 | Check for redundancy with other items |
| Cronbach's alpha if item deleted | Higher than overall alpha | Consider removing — item hurts reliability |
| Inter-item correlation | < 0.15 | Item may not belong to the scale |
| Inter-item correlation | > 0.85 | Redundant pair — remove one |
| Factor loading (EFA) | < 0.40 | Remove or reassign to different factor |
| Cross-loading | > 0.30 on secondary factor | Remove or revise — ambiguous factor membership |
| Communality | < 0.20 | Remove — item shares little variance with others |

---

## 2. Sampling Theory

### Probability Sampling Designs — Detailed

**Simple Random Sampling (SRS)**
- Every member of the population has an equal probability of selection: P = n/N
- Requires a complete list (sampling frame) of the population
- Standard error of the mean: SE = s / sqrt(n)
- Most statistically efficient for homogeneous populations

**Stratified Random Sampling**
- Population divided into mutually exclusive strata based on a variable correlated with the outcome
- Sample independently within each stratum
- Two allocation approaches:
  - Proportionate: n_stratum = (N_stratum / N_total) x n_total
  - Disproportionate: Oversample small strata for adequate subgroup analysis

**Cluster Sampling**
- Randomly select clusters (natural groupings: schools, hospitals, cities)
- Then sample within selected clusters (or census entire cluster)
- Design effect (DEFF): Ratio of variance under cluster sampling to SRS
  - DEFF = 1 + (m - 1) x ICC
  - m = average cluster size, ICC = intraclass correlation
  - Effective sample size: n_eff = n / DEFF
  - Must inflate sample size by DEFF when planning

**Multi-Stage Sampling**
- Example: Randomly select districts → randomly select schools within districts → randomly select classrooms → survey all students in selected classrooms
- At each stage, selection probabilities must be calculated for proper weighting

### Response Rate Calculation (AAPOR Standards)

```
Response Rate 1 (RR1) = Complete interviews / (Complete + Partial + Refusals +
                         Non-contact + Other + Unknown eligibility)

Response Rate 3 (RR3) = Complete interviews / (Complete + Partial + Refusals +
                         Non-contact + Other + e(Unknown eligibility))
Where e = estimated proportion of unknowns that are eligible

Cooperation Rate = Complete / (Complete + Partial + Refusals)

Contact Rate = (Complete + Partial + Refusals) /
               (Complete + Partial + Refusals + Non-contact)
```

### Strategies to Improve Response Rates

| Strategy | Expected Effect | Evidence Base |
|----------|----------------|---------------|
| Pre-notification (letter/email) | +3-6% | Dillman et al. (2014) |
| Personalized invitations | +4-8% | Edwards et al. (2009) |
| Monetary incentive (unconditional) | +10-15% | Singer & Ye (2013) |
| Lottery/prize draw incentive | +2-5% | Moderate effect |
| Follow-up reminders (3-4 contacts) | +15-25% | Dillman et al. (2014) |
| Shorter survey | +5-10% per 5 min reduction | Galesic & Bosnjak (2009) |
| University sponsorship (vs. commercial) | +5-10% | Edwards et al. (2009) |
| Deadline | Mixed evidence | May help or hurt depending on population |
| Mixed-mode (mail + online) | +5-10% | Dillman et al. (2014) |

---

## 3. Psychometric Validation Framework

### Validity Evidence (Standards for Educational and Psychological Testing, AERA/APA/NCME, 2014)

The Standards framework organizes validity evidence into five sources:

| Source of Evidence | Description | Methods |
|-------------------|-------------|---------|
| **Test content** | Evidence that items adequately represent the content domain | Expert review, CVI, alignment tables, item specifications |
| **Response processes** | Evidence that respondents engage with items as intended | Cognitive interviews, think-aloud protocols, eye-tracking, response time analysis |
| **Internal structure** | Evidence that item relationships match the theoretical structure | Factor analysis (EFA/CFA), internal consistency, item response theory |
| **Relations to other variables** | Evidence of expected relationships with external variables | Convergent validity, discriminant validity, criterion validity, known-groups validity |
| **Consequences of testing** | Evidence that test use produces intended outcomes without unintended harm | Impact studies, differential item functioning (DIF), fairness reviews |

### Confirmatory Factor Analysis (CFA) — Fit Indices

| Index | Acceptable | Good | Interpretation |
|-------|-----------|------|----------------|
| Chi-square (χ²) | p > 0.05 | — | Sensitive to sample size; rarely non-significant with n > 200 |
| χ²/df | < 5.0 | < 3.0 | Relative chi-square; less sensitive to sample size |
| CFI | > 0.90 | > 0.95 | Comparative Fit Index; 0-1 scale |
| TLI | > 0.90 | > 0.95 | Tucker-Lewis Index; can exceed 1.0 |
| RMSEA | < 0.08 | < 0.06 | Root Mean Square Error of Approximation; includes 90% CI |
| SRMR | < 0.08 | < 0.05 | Standardized Root Mean Square Residual |

**CFA Example in Python (using semopy):**

```python
import semopy
import pandas as pd

# Define CFA model
model_desc = """
# Factor 1: Teaching Self-Efficacy
TSE =~ item1 + item2 + item3 + item4

# Factor 2: Research Self-Efficacy
RSE =~ item5 + item6 + item7 + item8

# Factor 3: Service Self-Efficacy
SSE =~ item9 + item10 + item11 + item12
"""

model = semopy.Model(model_desc)
result = model.fit(data)

# Inspect fit indices
stats = semopy.calc_stats(model)
print(stats.T)

# Inspect factor loadings
print(model.inspect())
```

### Measurement Invariance Testing

When comparing groups (gender, culture, time), measurement invariance must be established:

| Level | What is Constrained | Tests Whether |
|-------|-------------------|---------------|
| Configural | Factor structure same across groups | Same constructs measured in each group |
| Metric (weak) | Factor loadings equal across groups | Items have same meaning across groups |
| Scalar (strong) | Factor loadings AND intercepts equal | Groups can be compared on latent means |
| Strict | Factor loadings, intercepts, AND residual variances equal | Observed scores are comparable across groups |

Criterion: Change in CFI ≤ 0.01 between levels indicates invariance holds.

---

## 4. Dillman's Tailored Design Method

### Core Principles

1. **Social exchange theory**: Respondents are more likely to complete surveys when they perceive the benefits of responding outweigh the costs
2. **Reduce costs**: Minimize time, effort, cognitive burden, and privacy concerns
3. **Increase rewards**: Provide information about why the survey matters; show respect; offer tangible rewards
4. **Establish trust**: Sponsorship by legitimate organization; professional design; confidentiality assurances

### Contact Sequence for Web Surveys

| Contact | Timing | Content |
|---------|--------|---------|
| 1. Pre-notification | Day 0 | Brief letter/email announcing the survey; why selected; importance |
| 2. Survey invitation | Day 3-5 | Link to survey; full explanation; deadline |
| 3. First reminder | Day 7-10 | Thank those who completed; reminder to others |
| 4. Second reminder | Day 14-21 | Different appeal; emphasize uniqueness of their contribution |
| 5. Final reminder | Day 28-35 | Last chance; deadline emphasis |

### Questionnaire Design Principles (Dillman)

1. Use a conventional question format that respondents are accustomed to
2. Ask the most important questions first
3. Group related questions together
4. Place sensitive questions after less sensitive ones
5. Use transition statements between sections
6. Avoid vague quantifiers ("usually," "sometimes") — use specific frequencies
7. Make response categories mutually exclusive and exhaustive
8. Provide a "Does not apply" or "Not applicable" option when appropriate
9. Minimize the use of open-ended questions in self-administered surveys
10. Pre-test every survey with cognitive interviews

---

## 5. Common Survey Biases — Detection and Correction

### Detecting Careless Responding

```python
import pandas as pd
import numpy as np

def detect_careless_responding(df, likert_cols):
    """
    Detect potentially careless respondents using multiple indicators.
    """
    flags = pd.DataFrame(index=df.index)

    # 1. Straightlining: same response to all items
    flags['straightline'] = df[likert_cols].apply(
        lambda row: row.nunique() == 1, axis=1
    )

    # 2. Low variance in responses
    flags['low_variance'] = df[likert_cols].var(axis=1) < 0.5

    # 3. Failed attention check(s)
    if 'attention_check' in df.columns:
        flags['failed_attention'] = df['attention_check'] != expected_value

    # 4. Completion time too fast (< 1/3 of median)
    if 'duration_seconds' in df.columns:
        median_time = df['duration_seconds'].median()
        flags['too_fast'] = df['duration_seconds'] < (median_time / 3)

    # 5. Inconsistency between reverse-coded item pairs
    # (requires specifying pairs)

    # Summary: flag respondents with 2+ indicators
    flags['total_flags'] = flags.sum(axis=1)
    flags['exclude'] = flags['total_flags'] >= 2

    print(f"Flagged for exclusion: {flags['exclude'].sum()} of {len(flags)} respondents")
    return flags
```

### Handling Missing Data in Surveys

| Pattern | Likely Cause | Approach |
|---------|-------------|----------|
| Missing Completely at Random (MCAR) | Technical glitch, random skip | Listwise deletion acceptable if < 5% |
| Missing at Random (MAR) | Missingness related to observed variables | Multiple imputation; full information maximum likelihood |
| Missing Not at Random (MNAR) | Missingness related to the missing value itself | Pattern mixture models; sensitivity analysis; selection models |

**Rule of thumb**: If > 5% of data are missing, use multiple imputation rather than listwise deletion.

---

## 6. Mixed-Mode Survey Design

### Mode Effects and Equivalence

| Feature | Online | Paper | Phone | In-Person |
|---------|--------|-------|-------|-----------|
| Social desirability | Low | Low | High | Highest |
| Coverage | Varies (internet access) | Excellent (with mailing list) | Declining (cell-only households) | Excellent |
| Cost per response | Low | Medium | High | Highest |
| Response rate | Low-Medium (10-30%) | Medium (30-50%) | Medium (20-40%) | High (50-70%) |
| Data quality | Good (skip logic, validation) | Medium (can skip items) | Good (interviewer probes) | Good (visual aids) |
| Best for | Large samples, tech-savvy populations | Elderly, low-internet populations | Brief surveys, follow-ups | Complex instruments, vulnerable populations |

### Ensuring Mode Equivalence

1. Keep question wording identical across modes
2. Match visual presentation as closely as possible
3. Test for measurement invariance across modes
4. Include mode as a covariate in analyses
5. Document mode-specific response rates separately

---

## Key References

- AERA, APA, & NCME. (2014). *Standards for educational and psychological testing*. AERA.
- Brislin, R. W. (1970). Back-translation for cross-cultural research. *Journal of Cross-Cultural Psychology*, 1(3), 185-216.
- DeVellis, R. F., & Thorpe, C. T. (2022). *Scale development: Theory and applications* (5th ed.). Sage.
- Dillman, D. A., Smyth, J. D., & Christian, L. M. (2014). *Internet, phone, mail, and mixed-mode surveys* (4th ed.). Wiley.
- Fowler, F. J. (2014). *Survey research methods* (5th ed.). Sage.
- Groves, R. M., et al. (2009). *Survey methodology* (2nd ed.). Wiley.
- Krosnick, J. A., & Presser, S. (2010). Question and questionnaire design. In *Handbook of survey research* (2nd ed.). Emerald.
- Podsakoff, P. M., et al. (2003). Common method biases. *Journal of Applied Psychology*, 88(5), 879-903.
- Willis, G. B. (2005). *Cognitive interviewing*. Sage.
- Wild, D., et al. (2005). Principles of good practice for the translation and cultural adaptation process for Patient-Reported Outcomes (PRO) measures. *Value in Health*, 8(2), 94-104.
