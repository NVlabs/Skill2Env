# Workflows and Best Practices

## Best Practices

### Data Preparation
1. **Always add constant**: use `sm.add_constant()` unless excluding the intercept.
2. **Check for missing values**: handle or impute before fitting.
3. **Scale if needed**: improves convergence and interpretation (not required for tree models).
4. **Encode categoricals**: use the formula API or manual dummy coding.

### Model Building
1. **Start simple**: begin with a basic model, add complexity as needed.
2. **Check assumptions**: test residuals, heteroskedasticity, autocorrelation.
3. **Use the appropriate model**: match model to outcome type (binary→Logit, count→Poisson).
4. **Consider alternatives**: if assumptions are violated, use robust methods or a different model.

### Inference
1. **Report effect sizes**: not just p-values.
2. **Use robust SEs**: when heteroskedasticity or clustering is present.
3. **Multiple comparisons**: correct when testing many hypotheses.
4. **Confidence intervals**: always report alongside point estimates.

### Model Evaluation
1. **Check residuals**: plot residuals vs fitted, Q-Q plot.
2. **Influence diagnostics**: identify and investigate influential observations.
3. **Out-of-sample validation**: test on a holdout set or cross-validate.
4. **Compare models**: AIC/BIC for non-nested, LR test for nested.

### Reporting
1. **Comprehensive summary**: use `.summary()` for detailed output.
2. **Document decisions**: note transformations and excluded observations.
3. **Interpret carefully**: account for link functions (e.g. `exp(β)` for a log link).
4. **Visualize**: plot predictions, confidence intervals, diagnostics.

## Common Workflows

### Workflow 1: Linear Regression Analysis
1. Explore data (plots, descriptives)
2. Fit initial OLS model
3. Check residual diagnostics
4. Test for heteroskedasticity, autocorrelation
5. Check for multicollinearity (VIF)
6. Identify influential observations
7. Refit with robust SEs if needed
8. Interpret coefficients and inference
9. Validate on holdout or via CV

### Workflow 2: Binary Classification
1. Fit logistic regression (Logit)
2. Check for convergence issues
3. Interpret odds ratios
4. Calculate marginal effects
5. Evaluate classification performance (AUC, confusion matrix)
6. Check for influential observations
7. Compare with alternative models (Probit)
8. Validate predictions on test set

### Workflow 3: Count Data Analysis
1. Fit Poisson regression
2. Check for overdispersion
3. If overdispersed, fit Negative Binomial
4. Check for excess zeros (consider ZIP/ZINB)
5. Interpret rate ratios
6. Assess goodness of fit
7. Compare models via AIC
8. Validate predictions

### Workflow 4: Time Series Forecasting
1. Plot series, check for trend/seasonality
2. Test for stationarity (ADF, KPSS)
3. Difference if non-stationary
4. Identify p, q from ACF/PACF
5. Fit ARIMA or SARIMAX
6. Check residual diagnostics (Ljung-Box)
7. Generate forecasts with confidence intervals
8. Evaluate forecast accuracy on test set

## Common Pitfalls to Avoid

1. **Forgetting the constant term**: always use `sm.add_constant()` unless no intercept is desired.
2. **Ignoring assumptions**: check residuals, heteroskedasticity, autocorrelation.
3. **Wrong model for outcome type**: Binary→Logit/Probit, Count→Poisson/NB, not OLS.
4. **Not checking convergence**: look for optimization warnings.
5. **Misinterpreting coefficients**: remember link functions (log, logit, etc.).
6. **Using Poisson with overdispersion**: check dispersion, use Negative Binomial if needed.
7. **Not using robust SEs**: when heteroskedasticity or clustering is present.
8. **Overfitting**: too many parameters relative to sample size.
9. **Data leakage**: fitting on test data or using future information.
10. **Not validating predictions**: always check out-of-sample performance.
11. **Comparing non-nested models with an LR test**: use AIC/BIC instead.
12. **Ignoring influential observations**: check Cook's distance and leverage.
13. **Multiple testing**: correct p-values when testing many hypotheses.
14. **Not differencing time series**: do not fit ARIMA on non-stationary data.
15. **Confusing prediction vs confidence intervals**: prediction intervals are wider.

## Searching the Reference Files

```bash
# Find information about specific models
grep -r "Quantile Regression" references/

# Find diagnostic tests
grep -r "Breusch-Pagan" references/stats_diagnostics.md

# Find time series guidance
grep -r "SARIMAX" references/time_series.md
```

## Getting Help

- Official docs: https://www.statsmodels.org/stable/
- User guide: https://www.statsmodels.org/stable/user-guide.html
- Examples: https://www.statsmodels.org/stable/examples/index.html
- API reference: https://www.statsmodels.org/stable/api.html
