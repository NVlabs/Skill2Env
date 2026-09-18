# Worked Code Examples

Copy-paste Python for the common analyses, extracted from the skill body. Primary
libraries: `scipy.stats`, `statsmodels`, `pingouin>=0.6`, `pymc`, `arviz`.

> **pingouin 0.6 column names**: output columns were renamed from hyphenated to clean
> snake_case — `p-val`→`p_val`, `p-unc`→`p_unc`, `cohen-d`→`cohen_d`, `CI95%`→`CI95`,
> `p-tukey`→`p_tukey`. The examples below use the 0.6 names. Also note `pg.ttest`'s
> `CI95` is the CI on the **mean difference**, not on Cohen's d — get the effect-size CI
> from `pg.compute_esci`.

## T-Test with Complete Reporting

```python
import pingouin as pg

# Run independent t-test (correction='auto' applies Welch's if variances differ)
result = pg.ttest(group_a, group_b, correction='auto')

# Extract results (pingouin >= 0.6 column names)
t_stat = result['T'].values[0]
df = result['dof'].values[0]
p_value = result['p_val'].values[0]
cohens_d = result['cohen_d'].values[0]
md_lo, md_hi = result['CI95'].values[0]  # CI on the MEAN DIFFERENCE

# CI on Cohen's d (separate call)
d_lo, d_hi = pg.compute_esci(stat=cohens_d, nx=len(group_a), ny=len(group_b),
                             eftype='cohen')

# Report
print(f"t({df:.0f}) = {t_stat:.2f}, p = {p_value:.3f}")
print(f"Cohen's d = {cohens_d:.2f}, 95% CI [{d_lo:.2f}, {d_hi:.2f}]")
```

## ANOVA with Post-Hoc Tests

```python
import pingouin as pg

# One-way ANOVA
aov = pg.anova(dv='score', between='group', data=df, detailed=True)
print(aov)

# If significant, conduct post-hoc tests
if aov['p_unc'].values[0] < 0.05:
    posthoc = pg.pairwise_tukey(dv='score', between='group', data=df)
    print(posthoc)  # adjusted p-values are in the 'p_tukey' column

# Effect size
eta_squared = aov['np2'].values[0]  # Partial eta-squared
print(f"Partial η² = {eta_squared:.3f}")
```

## Linear Regression with Diagnostics

```python
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Fit model
X = sm.add_constant(X_predictors)  # Add intercept
model = sm.OLS(y, X).fit()

# Summary
print(model.summary())

# Check multicollinearity (VIF)
vif_data = pd.DataFrame()
vif_data["Variable"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
print(vif_data)

# Check assumptions
residuals = model.resid
fitted = model.fittedvalues

# Residual plots
import matplotlib.pyplot as plt
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Residuals vs fitted
axes[0, 0].scatter(fitted, residuals, alpha=0.6)
axes[0, 0].axhline(y=0, color='r', linestyle='--')
axes[0, 0].set_xlabel('Fitted values')
axes[0, 0].set_ylabel('Residuals')
axes[0, 0].set_title('Residuals vs Fitted')

# Q-Q plot
from scipy import stats
stats.probplot(residuals, dist="norm", plot=axes[0, 1])
axes[0, 1].set_title('Normal Q-Q')

# Scale-Location
axes[1, 0].scatter(fitted, np.sqrt(np.abs(residuals / residuals.std())), alpha=0.6)
axes[1, 0].set_xlabel('Fitted values')
axes[1, 0].set_ylabel('√|Standardized residuals|')
axes[1, 0].set_title('Scale-Location')

# Residuals histogram
axes[1, 1].hist(residuals, bins=20, edgecolor='black', alpha=0.7)
axes[1, 1].set_xlabel('Residuals')
axes[1, 1].set_ylabel('Frequency')
axes[1, 1].set_title('Histogram of Residuals')

plt.tight_layout()
plt.show()
```

## Bayesian T-Test

```python
import pymc as pm
import arviz as az
import numpy as np

with pm.Model() as model:
    # Priors
    mu1 = pm.Normal('mu_group1', mu=0, sigma=10)
    mu2 = pm.Normal('mu_group2', mu=0, sigma=10)
    sigma = pm.HalfNormal('sigma', sigma=10)

    # Likelihood
    y1 = pm.Normal('y1', mu=mu1, sigma=sigma, observed=group_a)
    y2 = pm.Normal('y2', mu=mu2, sigma=sigma, observed=group_b)

    # Derived quantity
    diff = pm.Deterministic('difference', mu1 - mu2)

    # Sample
    trace = pm.sample(2000, tune=1000, return_inferencedata=True)

# Summarize
print(az.summary(trace, var_names=['difference']))

# Probability that group1 > group2
prob_greater = np.mean(trace.posterior['difference'].values > 0)
print(f"P(μ₁ > μ₂ | data) = {prob_greater:.3f}")

# Plot posterior
az.plot_posterior(trace, var_names=['difference'], ref_val=0)
```

## Calculating Effect Sizes

Most effect sizes are automatically computed by pingouin:

```python
# T-test returns Cohen's d
result = pg.ttest(x, y)
d = result['cohen_d'].values[0]

# ANOVA returns partial eta-squared
aov = pg.anova(dv='score', between='group', data=df, detailed=True)
eta_p2 = aov['np2'].values[0]

# Correlation: r is already an effect size
corr = pg.corr(x, y)
r = corr['r'].values[0]
```

Confidence intervals for effect sizes (always report to show precision):

```python
import pingouin as pg

# CI for Cohen's d from the effect size and group sizes
ci = pg.compute_esci(stat=d, nx=len(group1), ny=len(group2), eftype='cohen')
print(f"d = {d:.2f}, 95% CI [{ci[0]:.2f}, {ci[1]:.2f}]")

# Or derive d directly from a t-statistic (returns a scalar in pingouin >= 0.6)
d_from_t = pg.compute_effsize_from_t(t_statistic, nx=len(group1), ny=len(group2),
                                     eftype='cohen')
```

## Power Analysis

A priori (study planning) — determine required sample size before data collection:

```python
from statsmodels.stats.power import (
    tt_ind_solve_power,
    FTestAnovaPower
)

# T-test: What n is needed to detect d = 0.5?
n_required = tt_ind_solve_power(
    effect_size=0.5,
    alpha=0.05,
    power=0.80,
    ratio=1.0,
    alternative='two-sided'
)
print(f"Required n per group: {n_required:.0f}")

# ANOVA: What n is needed to detect f = 0.25?
anova_power = FTestAnovaPower()
n_per_group = anova_power.solve_power(
    effect_size=0.25,
    ngroups=3,
    alpha=0.05,
    power=0.80
)
print(f"Required n per group: {n_per_group:.0f}")
```

Sensitivity analysis (post-study) — determine the smallest detectable effect:

```python
# With n=50 per group, what effect could we detect?
detectable_d = tt_ind_solve_power(
    effect_size=None,  # Solve for this
    nobs1=50,
    alpha=0.05,
    power=0.80,
    ratio=1.0,
    alternative='two-sided'
)
print(f"Study could detect d ≥ {detectable_d:.2f}")
```

**Note**: Post-hoc power analysis (calculating power after a study) is generally not
recommended. Use sensitivity analysis instead.

## Assumption Checks (bundled script)

```python
from scripts.assumption_checks import comprehensive_assumption_check

# Comprehensive check with visualizations
results = comprehensive_assumption_check(
    data=df,
    value_col='score',
    group_col='group',  # Optional: for group comparisons
    alpha=0.05
)
```

Targeted, individual checks:

```python
from scripts.assumption_checks import (
    check_normality,
    check_normality_per_group,
    check_homogeneity_of_variance,
    check_linearity,
    detect_outliers
)

# Example: Check normality with visualization
result = check_normality(
    data=df['score'],
    name='Test Score',
    alpha=0.05,
    plot=True
)
print(result['interpretation'])
print(result['recommendation'])
```
