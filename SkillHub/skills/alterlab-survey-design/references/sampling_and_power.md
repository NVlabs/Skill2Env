# Sampling Strategies and Sample Size / Power

Probability and non-probability sampling methods, sample size formulas for descriptive surveys, and Python power analysis for comparative surveys. Extracted from the Survey Design skill body.

## Sampling Strategies

**Probability Sampling (every member of population has a known, non-zero chance of selection):**

| Method | How It Works | Pros | Cons |
|--------|-------------|------|------|
| Simple random | Select randomly from complete list | Unbiased, generalizable | Requires complete sampling frame |
| Systematic | Select every kth element from list | Easy to implement | Periodicity risk if list has pattern |
| Stratified | Divide population into strata, then random sample within each | Ensures representation of subgroups | Requires knowledge of population characteristics |
| Cluster | Randomly select clusters (schools, hospitals), then sample within | Practical when no individual-level list exists | Higher sampling error than SRS |
| Multi-stage | Combine methods (e.g., cluster then stratified) | Flexible, practical for large populations | Complex to implement and analyze |

**Non-Probability Sampling (no guarantee of representativeness):**

| Method | How It Works | Pros | Cons |
|--------|-------------|------|------|
| Convenience | Recruit whoever is available | Fast, cheap | Not generalizable; strong bias |
| Purposive | Select participants based on specific criteria | Targets relevant subgroups | Researcher bias in selection |
| Snowball | Existing participants recruit others | Access to hard-to-reach populations | Biased toward connected individuals |
| Quota | Set quotas for subgroups, then convenience sample within | Ensures diversity on key dimensions | Not truly random within quotas |

## Sample Size Determination

```
For descriptive surveys (estimating proportions):
n = (Z² × p × (1-p)) / E²

Where:
  Z = Z-score for confidence level (1.96 for 95%)
  p = Expected proportion (use 0.5 if unknown — most conservative)
  E = Margin of error (e.g., 0.05 for ±5%)

Example: 95% confidence, 5% margin of error, unknown proportion
n = (1.96² × 0.5 × 0.5) / 0.05² = 384.16 → 385 respondents

Adjust for finite population:
n_adj = n / (1 + (n-1)/N)
Where N = population size

Adjust for expected response rate:
n_needed = n_adj / expected_response_rate
Example: 385 / 0.30 = 1,284 invitations needed for 30% response rate
```

**For comparative surveys (detecting differences between groups):**

```python
# Power analysis for two-group comparison
from scipy import stats
import numpy as np

def sample_size_two_groups(effect_size, alpha=0.05, power=0.80):
    """
    Calculate sample size per group for independent samples t-test.

    effect_size: Cohen's d (0.2=small, 0.5=medium, 0.8=large)
    alpha: significance level
    power: desired statistical power
    """
    z_alpha = stats.norm.ppf(1 - alpha/2)
    z_beta = stats.norm.ppf(power)
    n = 2 * ((z_alpha + z_beta) / effect_size) ** 2
    return int(np.ceil(n))

# Examples (normal approximation; exact noncentral-t values are ~1 larger:
# 394 / 64 / 26 — use statsmodels TTestIndPower for the exact figures)
print(f"Small effect (d=0.2):  {sample_size_two_groups(0.2)} per group")   # 393
print(f"Medium effect (d=0.5): {sample_size_two_groups(0.5)} per group")   # 63
print(f"Large effect (d=0.8):  {sample_size_two_groups(0.8)} per group")   # 25
```
