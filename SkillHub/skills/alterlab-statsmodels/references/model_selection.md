# Model Selection and Comparison

Techniques for choosing among candidate models and validating fit.

## Information Criteria

```python
# Compare models using AIC/BIC
models = {
    'Model 1': model1_results,
    'Model 2': model2_results,
    'Model 3': model3_results
}

comparison = pd.DataFrame({
    'AIC': {name: res.aic for name, res in models.items()},
    'BIC': {name: res.bic for name, res in models.items()},
    'Log-Likelihood': {name: res.llf for name, res in models.items()}
})

print(comparison.sort_values('AIC'))
# Lower AIC/BIC indicates better model
```

## Likelihood Ratio Test (Nested Models)

```python
# For nested models (one is subset of the other)
from scipy import stats

lr_stat = 2 * (full_model.llf - reduced_model.llf)
df = full_model.df_model - reduced_model.df_model
p_value = 1 - stats.chi2.cdf(lr_stat, df)

print(f"LR statistic: {lr_stat:.4f}")
print(f"p-value: {p_value:.4f}")

if p_value < 0.05:
    print("Full model significantly better")
else:
    print("Reduced model preferred (parsimony)")
```

## Cross-Validation

```python
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error

kf = KFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = []

for train_idx, val_idx in kf.split(X):
    X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
    y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]

    # Fit model
    model = sm.OLS(y_train, X_train).fit()

    # Predict
    y_pred = model.predict(X_val)

    # Score
    rmse = np.sqrt(mean_squared_error(y_val, y_pred))
    cv_scores.append(rmse)

print(f"CV RMSE: {np.mean(cv_scores):.4f} ± {np.std(cv_scores):.4f}")
```

## Guidance

- **Non-nested models** → compare AIC/BIC (lower is better); do not use a likelihood ratio test.
- **Nested models** → likelihood ratio test (the full model must strictly contain the reduced one).
- **Predictive performance** → cross-validation or a holdout set; report RMSE/accuracy out of sample.
