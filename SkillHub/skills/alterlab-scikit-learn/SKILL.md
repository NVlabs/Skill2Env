---
name: alterlab-scikit-learn
description: Classical machine learning in Python with scikit-learn — algorithms, preprocessing, pipelines, and best-practice reference documentation. Use when working with supervised learning (classification, regression), unsupervised learning (clustering, dimensionality reduction), model evaluation, hyperparameter tuning, feature preprocessing, or building ML pipelines. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read Write Edit Bash(python:*) Bash(uv:*)
compatibility: No API key required. Runs locally via `uv run python`; requires the scikit-learn Python package.
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# Scikit-learn

## Overview

This skill provides comprehensive guidance for machine learning tasks using scikit-learn, the industry-standard Python library for classical machine learning. Use this skill for classification, regression, clustering, dimensionality reduction, preprocessing, model evaluation, and building production-ready ML pipelines.

## Installation

```bash
# Install scikit-learn using uv
uv pip install scikit-learn

# Optional: Install visualization dependencies
uv pip install matplotlib seaborn

# Commonly used with
uv pip install pandas numpy
```

## When to Use This Skill

Use the scikit-learn skill when:

- Building classification or regression models
- Performing clustering or dimensionality reduction
- Preprocessing and transforming data for machine learning
- Evaluating model performance with cross-validation
- Tuning hyperparameters with grid or random search
- Creating ML pipelines for production workflows
- Comparing different algorithms for a task
- Working with both structured (tabular) and text data
- Need interpretable, classical machine learning approaches

## Quick Start

Minimal classification flow: stratified `train_test_split` → `StandardScaler` (fit on train only) → fit estimator → `classification_report`. For mixed numeric/categorical data, wrap preprocessing in a `ColumnTransformer` inside a `Pipeline` so it cross-validates without leakage.

**See `references/worked_examples.md`** for full copy-paste classification and mixed-data pipeline examples.

## Core Capabilities

### 1. Supervised Learning

Comprehensive algorithms for classification and regression tasks.

**Key algorithms:**
- **Linear models**: Logistic Regression, Linear Regression, Ridge, Lasso, ElasticNet
- **Tree-based**: Decision Trees, Random Forest, Gradient Boosting
- **Support Vector Machines**: SVC, SVR with various kernels
- **Ensemble methods**: AdaBoost, Voting, Stacking
- **Neural Networks**: MLPClassifier, MLPRegressor
- **Others**: Naive Bayes, K-Nearest Neighbors

**When to use:**
- Classification: Predicting discrete categories (spam detection, image classification, fraud detection)
- Regression: Predicting continuous values (price prediction, demand forecasting)

**See:** `references/supervised_learning.md` for detailed algorithm documentation, parameters, and usage examples.

### 2. Unsupervised Learning

Discover patterns in unlabeled data through clustering and dimensionality reduction.

**Clustering algorithms:**
- **Partition-based**: K-Means, MiniBatchKMeans
- **Density-based**: DBSCAN, HDBSCAN, OPTICS
- **Hierarchical**: AgglomerativeClustering
- **Probabilistic**: Gaussian Mixture Models
- **Others**: MeanShift, SpectralClustering, BIRCH

**Dimensionality reduction:**
- **Linear**: PCA, TruncatedSVD, NMF
- **Manifold learning**: t-SNE, UMAP, Isomap, LLE
- **Feature extraction**: FastICA, LatentDirichletAllocation

**When to use:**
- Customer segmentation, anomaly detection, data visualization
- Reducing feature dimensions, exploratory data analysis
- Topic modeling, image compression

**See:** `references/unsupervised_learning.md` for detailed documentation.

### 3. Model Evaluation and Selection

Tools for robust model evaluation, cross-validation, and hyperparameter tuning.

**Cross-validation strategies:**
- KFold, StratifiedKFold (classification)
- TimeSeriesSplit (temporal data)
- GroupKFold (grouped samples)

**Hyperparameter tuning:**
- GridSearchCV (exhaustive search)
- RandomizedSearchCV (random sampling)
- HalvingGridSearchCV (successive halving)

**Metrics:**
- **Classification**: accuracy, precision, recall, F1-score, ROC AUC, confusion matrix
- **Regression**: MSE, RMSE, MAE, R², MAPE
- **Clustering**: silhouette score, Calinski-Harabasz, Davies-Bouldin

**When to use:**
- Comparing model performance objectively
- Finding optimal hyperparameters
- Preventing overfitting through cross-validation
- Understanding model behavior with learning curves

**See:** `references/model_evaluation.md` for comprehensive metrics and tuning strategies.

### 4. Data Preprocessing

Transform raw data into formats suitable for machine learning.

**Scaling and normalization:**
- StandardScaler (zero mean, unit variance)
- MinMaxScaler (bounded range)
- RobustScaler (robust to outliers)
- Normalizer (sample-wise normalization)

**Encoding categorical variables:**
- OneHotEncoder (nominal categories)
- OrdinalEncoder (ordered categories)
- LabelEncoder (target encoding)

**Handling missing values:**
- SimpleImputer (mean, median, most frequent)
- KNNImputer (k-nearest neighbors)
- IterativeImputer (multivariate imputation)

**Feature engineering:**
- PolynomialFeatures (interaction terms)
- KBinsDiscretizer (binning)
- Feature selection (RFE, SelectKBest, SelectFromModel)

**When to use:**
- Before training any algorithm that requires scaled features (SVM, KNN, Neural Networks)
- Converting categorical variables to numeric format
- Handling missing data systematically
- Creating non-linear features for linear models

**See:** `references/preprocessing.md` for detailed preprocessing techniques.

### 5. Pipelines and Composition

Build reproducible, production-ready ML workflows.

**Key components:**
- **Pipeline**: Chain transformers and estimators sequentially
- **ColumnTransformer**: Apply different preprocessing to different columns
- **FeatureUnion**: Combine multiple transformers in parallel
- **TransformedTargetRegressor**: Transform target variable

**Benefits:**
- Prevents data leakage in cross-validation
- Simplifies code and improves maintainability
- Enables joint hyperparameter tuning
- Ensures consistency between training and prediction

**When to use:**
- Always use Pipelines for production workflows
- When mixing numerical and categorical features (use ColumnTransformer)
- When performing cross-validation with preprocessing steps
- When hyperparameter tuning includes preprocessing parameters

**See:** `references/pipelines_and_composition.md` for comprehensive pipeline patterns.

## Example Scripts

Two runnable end-to-end scripts ship with this skill:

```bash
python scripts/classification_pipeline.py   # mixed-data preprocessing, model comparison, GridSearchCV, evaluation, feature importance
python scripts/clustering_analysis.py        # optimal-k search, K-Means/DBSCAN/Agglomerative/GMM comparison, PCA visualization
```

**See `references/worked_examples.md`** for what each script demonstrates and standalone copy-paste versions.

## Reference Documentation

This skill includes comprehensive reference files for deep dives into specific topics:

### Quick Reference
**File:** `references/quick_reference.md`
- Common import patterns and installation instructions
- Quick workflow templates for common tasks
- Algorithm selection cheat sheets
- Common patterns and gotchas
- Performance optimization tips

### Supervised Learning
**File:** `references/supervised_learning.md`
- Linear models (regression and classification)
- Support Vector Machines
- Decision Trees and ensemble methods
- K-Nearest Neighbors, Naive Bayes, Neural Networks
- Algorithm selection guide

### Unsupervised Learning
**File:** `references/unsupervised_learning.md`
- All clustering algorithms with parameters and use cases
- Dimensionality reduction techniques
- Outlier and novelty detection
- Gaussian Mixture Models
- Method selection guide

### Model Evaluation
**File:** `references/model_evaluation.md`
- Cross-validation strategies
- Hyperparameter tuning methods
- Classification, regression, and clustering metrics
- Learning and validation curves
- Best practices for model selection

### Preprocessing
**File:** `references/preprocessing.md`
- Feature scaling and normalization
- Encoding categorical variables
- Missing value imputation
- Feature engineering techniques
- Custom transformers

### Pipelines and Composition
**File:** `references/pipelines_and_composition.md`
- Pipeline construction and usage
- ColumnTransformer for mixed data types
- FeatureUnion for parallel transformations
- Complete end-to-end examples
- Best practices

### Worked Examples
**File:** `references/worked_examples.md`
- Quick-start classification and mixed-data pipeline snippets
- Step-by-step classification model workflow
- Step-by-step clustering analysis workflow
- What each bundled example script demonstrates

### Best Practices & Troubleshooting
**File:** `references/best_practices_and_troubleshooting.md`
- Pipeline / leakage discipline, fit-on-train-only, stratified splitting
- Random-state reproducibility, metric selection, when to scale features
- Fixes for ConvergenceWarning, overfitting, and large-dataset memory errors

## Common Workflows

- **Classification model:** load data → stratified `train_test_split` → `ColumnTransformer` preprocessing inside a `Pipeline` → `GridSearchCV` tuning → `classification_report` on the held-out test set.
- **Clustering analysis:** `StandardScaler` → silhouette sweep over `k` to pick `optimal_k` → fit `KMeans` → `PCA(n_components=2)` projection for visualization.

**See `references/worked_examples.md`** for the numbered, copy-paste version of each workflow.

## Best Practices (essentials)

- Always preprocess inside a `Pipeline` (prevents leakage); fit on train only, `transform` test.
- Use `stratify=y` for classification splits; set `random_state` everywhere for reproducibility.
- Scale features for SVM/KNN/NN/PCA/regularized-linear/K-Means; tree models and Naive Bayes do not need it.
- Pick metrics for the problem: F1/accuracy on balanced data; precision/recall/ROC AUC/balanced accuracy on imbalanced data.

**See `references/best_practices_and_troubleshooting.md`** for code examples and fixes for `ConvergenceWarning`, overfitting, and large-dataset memory errors.

## Additional Resources

- Official Documentation: https://scikit-learn.org/stable/
- User Guide: https://scikit-learn.org/stable/user_guide.html
- API Reference: https://scikit-learn.org/stable/api/index.html
- Examples Gallery: https://scikit-learn.org/stable/auto_examples/index.html

