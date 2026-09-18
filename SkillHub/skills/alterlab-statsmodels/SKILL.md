---
name: alterlab-statsmodels
description: Statistical modeling in Python with statsmodels — OLS, GLM, mixed models, and ARIMA with detailed diagnostics, residuals, and inference. Use when fitting specific model classes for econometrics, time series, or rigorous inference with coefficient tables and confidence intervals. For guided statistical test selection with APA reporting prefer statistical-analysis. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read Write Edit Bash(python:*) Bash(uv:*)
compatibility: No API key required. Runs locally via `uv run python`; requires the statsmodels Python package.
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# Statsmodels: Statistical Modeling and Econometrics

## Overview

Statsmodels is Python's premier library for statistical modeling, providing tools for estimation, inference, and diagnostics across a wide range of statistical methods. Apply this skill for rigorous statistical analysis, from simple linear regression to complex time series models and econometric analyses.

## When to Use This Skill

This skill should be used when:
- Fitting regression models (OLS, WLS, GLS, quantile regression)
- Performing generalized linear modeling (logistic, Poisson, Gamma, etc.)
- Analyzing discrete outcomes (binary, multinomial, count, ordinal)
- Conducting time series analysis (ARIMA, SARIMAX, VAR, forecasting)
- Running statistical tests and diagnostics
- Testing model assumptions (heteroskedasticity, autocorrelation, normality)
- Detecting outliers and influential observations
- Comparing models (AIC/BIC, likelihood ratio tests)
- Estimating causal effects
- Producing publication-ready statistical tables and inference

## Quick Start

Copy-paste starting points for OLS, logistic regression, ARIMA, GLM/Poisson, and the R-style formula API are in `references/quickstart_examples.md`. Core rule: always `sm.add_constant()` for an intercept unless you deliberately want none.

## Core Statistical Modeling Capabilities

### 1. Linear Regression Models

Comprehensive suite of linear models for continuous outcomes with various error structures.

**Available models:**
- **OLS**: Standard linear regression with i.i.d. errors
- **WLS**: Weighted least squares for heteroskedastic errors
- **GLS**: Generalized least squares for arbitrary covariance structure
- **GLSAR**: GLS with autoregressive errors for time series
- **Quantile Regression**: Conditional quantiles (robust to outliers)
- **Mixed Effects**: Hierarchical/multilevel models with random effects
- **Recursive/Rolling**: Time-varying parameter estimation

**Key features:**
- Comprehensive diagnostic tests
- Robust standard errors (HC, HAC, cluster-robust)
- Influence statistics (Cook's distance, leverage, DFFITS)
- Hypothesis testing (F-tests, Wald tests)
- Model comparison (AIC, BIC, likelihood ratio tests)
- Prediction with confidence and prediction intervals

**When to use:** Continuous outcome variable, want inference on coefficients, need diagnostics

**Reference:** See `references/linear_models.md` for detailed guidance on model selection, diagnostics, and best practices.

### 2. Generalized Linear Models (GLM)

Flexible framework extending linear models to non-normal distributions.

**Distribution families:**
- **Binomial**: Binary outcomes or proportions (logistic regression)
- **Poisson**: Count data
- **Negative Binomial**: Overdispersed counts
- **Gamma**: Positive continuous, right-skewed data
- **Inverse Gaussian**: Positive continuous with specific variance structure
- **Gaussian**: Equivalent to OLS
- **Tweedie**: Flexible family for semi-continuous data

**Link functions:**
- Logit, Probit, Log, Identity, Inverse, Sqrt, CLogLog, Power
- Choose based on interpretation needs and model fit

**Key features:**
- Maximum likelihood estimation via IRLS
- Deviance and Pearson residuals
- Goodness-of-fit statistics
- Pseudo R-squared measures
- Robust standard errors

**When to use:** Non-normal outcomes, need flexible variance and link specifications

**Reference:** See `references/glm.md` for family selection, link functions, interpretation, and diagnostics.

### 3. Discrete Choice Models

Models for categorical and count outcomes.

**Binary models:**
- **Logit**: Logistic regression (odds ratios)
- **Probit**: Probit regression (normal distribution)

**Multinomial models:**
- **MNLogit**: Unordered categories (3+ levels)
- **Conditional Logit**: Choice models with alternative-specific variables
- **Ordered Model**: Ordinal outcomes (ordered categories)

**Count models:**
- **Poisson**: Standard count model
- **Negative Binomial**: Overdispersed counts
- **Zero-Inflated**: Excess zeros (ZIP, ZINB)
- **Hurdle Models**: Two-stage models for zero-heavy data

**Key features:**
- Maximum likelihood estimation
- Marginal effects at means or average marginal effects
- Model comparison via AIC/BIC
- Predicted probabilities and classification
- Goodness-of-fit tests

**When to use:** Binary, categorical, or count outcomes

**Reference:** See `references/discrete_choice.md` for model selection, interpretation, and evaluation.

### 4. Time Series Analysis

Comprehensive time series modeling and forecasting capabilities.

**Univariate models:**
- **AutoReg (AR)**: Autoregressive models
- **ARIMA**: Autoregressive integrated moving average
- **SARIMAX**: Seasonal ARIMA with exogenous variables
- **Exponential Smoothing**: Simple, Holt, Holt-Winters
- **ETS**: Innovations state space models

**Multivariate models:**
- **VAR**: Vector autoregression
- **VARMAX**: VAR with MA and exogenous variables
- **Dynamic Factor Models**: Extract common factors
- **VECM**: Vector error correction models (cointegration)

**Advanced models:**
- **State Space**: Kalman filtering, custom specifications
- **Regime Switching**: Markov switching models
- **ARDL**: Autoregressive distributed lag

**Key features:**
- ACF/PACF analysis for model identification
- Stationarity tests (ADF, KPSS)
- Forecasting with prediction intervals
- Residual diagnostics (Ljung-Box, heteroskedasticity)
- Granger causality testing
- Impulse response functions (IRF)
- Forecast error variance decomposition (FEVD)

**When to use:** Time-ordered data, forecasting, understanding temporal dynamics

**Reference:** See `references/time_series.md` for model selection, diagnostics, and forecasting methods.

### 5. Statistical Tests and Diagnostics

Extensive testing and diagnostic capabilities for model validation.

**Residual diagnostics:**
- Autocorrelation tests (Ljung-Box, Durbin-Watson, Breusch-Godfrey)
- Heteroskedasticity tests (Breusch-Pagan, White, ARCH)
- Normality tests (Jarque-Bera, Omnibus, Anderson-Darling, Lilliefors)
- Specification tests (RESET, Harvey-Collier)

**Influence and outliers:**
- Leverage (hat values)
- Cook's distance
- DFFITS and DFBETAs
- Studentized residuals
- Influence plots

**Hypothesis testing:**
- t-tests (one-sample, two-sample, paired)
- Proportion tests
- Chi-square tests
- Non-parametric tests (Mann-Whitney, Wilcoxon, Kruskal-Wallis)
- ANOVA (one-way, two-way, repeated measures)

**Multiple comparisons:**
- Tukey's HSD
- Bonferroni correction
- False Discovery Rate (FDR)

**Effect sizes and power:**
- Cohen's d, eta-squared
- Power analysis for t-tests, proportions
- Sample size calculations

**Robust inference:**
- Heteroskedasticity-consistent SEs (HC0-HC3)
- HAC standard errors (Newey-West)
- Cluster-robust standard errors

**When to use:** Validating assumptions, detecting problems, ensuring robust inference

**Reference:** See `references/stats_diagnostics.md` for comprehensive testing and diagnostic procedures.

## Formula API, Model Selection, Workflows

- **R-style formula API** (`smf.ols`, `smf.logit`, `smf.poisson`, interactions, `C()`, `I()`) → `references/quickstart_examples.md`.
- **Model selection and comparison** (AIC/BIC tables, likelihood ratio test for nested models, k-fold cross-validation) → `references/model_selection.md`.
- **Best practices, end-to-end workflows (OLS, logistic, count, time series), and common pitfalls** → `references/workflows_and_practices.md`.

## Routing Guidance

- Linear/continuous outcome, inference + diagnostics → Capability 1 + `references/linear_models.md`.
- Non-normal outcome, flexible link/variance → Capability 2 + `references/glm.md`.
- Binary, categorical, or count outcome → Capability 3 + `references/discrete_choice.md`.
- Time-ordered data, forecasting → Capability 4 + `references/time_series.md`.
- Validating assumptions, testing, robust inference → Capability 5 + `references/stats_diagnostics.md`.
- Choosing between candidate models → `references/model_selection.md`.

## References Index

- `references/quickstart_examples.md` — copy-paste OLS / Logit / ARIMA / GLM examples and the R-style formula API.
- `references/linear_models.md` — OLS, WLS, GLS, GLSAR, quantile, mixed effects, recursive/rolling; diagnostics, influence, robust SEs, hypothesis testing.
- `references/glm.md` — all distribution families, link functions, interpretation, pseudo R-squared, residual analysis.
- `references/discrete_choice.md` — binary (Logit/Probit), multinomial, count (Poisson/NB/ZIP/ZINB/hurdle), ordinal, marginal effects.
- `references/time_series.md` — AR/ARIMA/SARIMAX/ETS, VAR/VARMAX/dynamic factor, state space, stationarity, forecasting, Granger/IRF/FEVD.
- `references/stats_diagnostics.md` — residual diagnostics, influence/outliers, parametric and non-parametric tests, ANOVA, multiple comparisons, robust covariances, power/effect sizes.
- `references/model_selection.md` — AIC/BIC comparison, likelihood ratio test, cross-validation.
- `references/workflows_and_practices.md` — best practices, end-to-end workflows, common pitfalls, search patterns, official docs links.

