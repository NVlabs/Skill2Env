# Distribution Selection Guide

Quick chooser for priors and likelihoods. For the full distribution catalog, see `references/distributions.md`.

## For Priors

**Scale parameters** (σ, τ):
- `pm.HalfNormal('sigma', sigma=1)` - Default choice
- `pm.Exponential('sigma', lam=1)` - Alternative
- `pm.Gamma('sigma', alpha=2, beta=1)` - More informative

**Unbounded parameters**:
- `pm.Normal('theta', mu=0, sigma=1)` - For standardized data
- `pm.StudentT('theta', nu=3, mu=0, sigma=1)` - Robust to outliers

**Positive parameters**:
- `pm.LogNormal('theta', mu=0, sigma=1)`
- `pm.Gamma('theta', alpha=2, beta=1)`

**Probabilities**:
- `pm.Beta('p', alpha=2, beta=2)` - Weakly informative
- `pm.Uniform('p', lower=0, upper=1)` - Non-informative (use sparingly)

**Correlation matrices**:
- `pm.LKJCorr('corr', n=n_vars, eta=2)` - eta=1 uniform, eta>1 prefers identity

## For Likelihoods

**Continuous outcomes**:
- `pm.Normal('y', mu=mu, sigma=sigma)` - Default for continuous data
- `pm.StudentT('y', nu=nu, mu=mu, sigma=sigma)` - Robust to outliers

**Count data**:
- `pm.Poisson('y', mu=lambda)` - Equidispersed counts
- `pm.NegativeBinomial('y', mu=mu, alpha=alpha)` - Overdispersed counts
- `pm.ZeroInflatedPoisson('y', psi=psi, mu=mu)` - Excess zeros

**Binary outcomes**:
- `pm.Bernoulli('y', p=p)` or `pm.Bernoulli('y', logit_p=logit_p)`

**Categorical outcomes**:
- `pm.Categorical('y', p=probs)`

See `references/distributions.md` for the comprehensive distribution reference.
