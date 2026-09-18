# Model Comparison and Diagnostics

Code for comparing models (LOO/WAIC), diagnostic scripts, and troubleshooting common sampling issues.

## Comparing Models

Use LOO or WAIC for model comparison:

```python
from scripts.model_comparison import compare_models, check_loo_reliability

# Fit models with log_likelihood
models = {
    'Model1': idata1,
    'Model2': idata2,
    'Model3': idata3
}

# Compare using LOO
comparison = compare_models(models, ic='loo')

# Check reliability
check_loo_reliability(models)
```

**Interpretation:**
- **Δloo < 2**: Models are similar, choose simpler model
- **2 < Δloo < 4**: Weak evidence for better model
- **4 < Δloo < 10**: Moderate evidence
- **Δloo > 10**: Strong evidence for better model

**Check Pareto-k values:**
- k < 0.7: LOO reliable
- k > 0.7: Consider WAIC or k-fold CV

## Model Averaging

When models are similar, average predictions:

```python
from scripts.model_comparison import model_averaging

averaged_pred, weights = model_averaging(models, var_name='y_obs')
```

## Diagnostic Scripts

### Comprehensive Diagnostics

```python
from scripts.model_diagnostics import create_diagnostic_report

create_diagnostic_report(
    idata,
    var_names=['alpha', 'beta', 'sigma'],
    output_dir='diagnostics/'
)
```

Creates: trace plots, rank plots (mixing check), autocorrelation plots, energy plots, ESS evolution, summary statistics CSV.

### Quick Diagnostic Check

```python
from scripts.model_diagnostics import check_diagnostics

results = check_diagnostics(idata)
```

Checks R-hat, ESS, divergences, and tree depth.

## Common Issues and Solutions

### Divergences

**Symptom:** `idata.sample_stats.diverging.sum() > 0`

**Solutions:**
1. Increase `target_accept=0.95` or `0.99`
2. Use non-centered parameterization (hierarchical models)
3. Add stronger priors to constrain parameters
4. Check for model misspecification

### Low Effective Sample Size

**Symptom:** `ESS < 400`

**Solutions:**
1. Sample more draws: `draws=5000`
2. Reparameterize to reduce posterior correlation
3. Use QR decomposition for regression with correlated predictors

### High R-hat

**Symptom:** `R-hat > 1.01`

**Solutions:**
1. Run longer chains: `tune=2000, draws=5000`
2. Check for multimodality
3. Improve initialization with ADVI

### Slow Sampling

**Solutions:**
1. Use ADVI initialization
2. Reduce model complexity
3. Increase parallelization: `cores=8, chains=8`
4. Use variational inference if appropriate

## Sampling and Inference

### MCMC with NUTS

Default and recommended for most models:

```python
idata = pm.sample(
    draws=2000,
    tune=1000,
    chains=4,
    target_accept=0.9,
    random_seed=42
)
```

**Adjust when needed:**
- Divergences → `target_accept=0.95` or higher
- Slow sampling → Use ADVI for initialization
- Discrete parameters → Use `pm.Metropolis()` for discrete vars

### Variational Inference

Fast approximation for exploration or initialization:

```python
with model:
    approx = pm.fit(n=20000, method='advi')

    # Use for initialization
    start = approx.sample(return_inferencedata=False)[0]
    idata = pm.sample(start=start)
```

**Trade-offs:** much faster than MCMC, but approximate (may underestimate uncertainty). Good for large models or quick exploration.

See `references/sampling_inference.md` for the detailed sampling guide.
