# Datasets and Benchmarking

Aeon provides comprehensive tools for loading datasets and benchmarking time series algorithms.

## Dataset Loading

### Task-Specific Loaders

**Classification Datasets**:
```python
from aeon.datasets import load_classification

# Load train/test split
X_train, y_train = load_classification("GunPoint", split="train")
X_test, y_test = load_classification("GunPoint", split="test")

# Load entire dataset
X, y = load_classification("GunPoint")
```

**Regression Datasets**:
```python
from aeon.datasets import load_regression

X_train, y_train = load_regression("Covid3Month", split="train")
X_test, y_test = load_regression("Covid3Month", split="test")

# Bulk download
from aeon.datasets import download_all_regression
download_all_regression()  # Downloads Monash TSER archive
```

**Forecasting Datasets**:
```python
from aeon.datasets import load_forecasting

# Load from forecastingdata.org
y, X = load_forecasting("airline", return_X_y=True)
```

**Anomaly Detection Datasets**:
```python
from aeon.datasets import load_anomaly_detection

X, y = load_anomaly_detection("NAB_realKnownCause")
```

### File Format Loaders

**Load from .ts files**:
```python
from aeon.datasets import load_from_ts_file

X, y = load_from_ts_file("path/to/data.ts")
```

**Load from .tsf files**:
```python
from aeon.datasets import load_from_tsf_file

df, metadata = load_from_tsf_file("path/to/data.tsf")
```

**Load from ARFF files**:
```python
from aeon.datasets import load_from_arff_file

X, y = load_from_arff_file("path/to/data.arff")
```

**Load from TSV files**:
```python
from aeon.datasets import load_from_tsv_file

data = load_from_tsv_file("path/to/data.tsv")
```

**Load TimeEval CSV**:
```python
from aeon.datasets import load_from_timeeval_csv_file

X, y = load_from_timeeval_csv_file("path/to/timeeval.csv")
```

### Writing Datasets

**Write to .ts format**:
```python
from aeon.datasets import write_to_ts_file

write_to_ts_file(X, "output.ts", y=y, problem_name="MyDataset")
```

**Write to ARFF format**:
```python
from aeon.datasets import write_to_arff_file

write_to_arff_file(X, "output.arff", y=y)
```

## Built-in Datasets

Aeon includes several benchmark datasets for quick testing:

### Classification
- `ArrowHead` - Shape classification
- `GunPoint` - Gesture recognition
- `ItalyPowerDemand` - Energy demand
- `BasicMotions` - Motion classification
- And 100+ more from UCR/UEA archives

### Regression
- `Covid3Month` - COVID forecasting
- Various datasets from Monash TSER archive

### Segmentation
- Time series segmentation datasets
- Human activity data
- Sensor data collections

### Special Collections
- `RehabPile` - Rehabilitation data (classification & regression)

## Dataset Metadata

Get information about datasets:

```python
from aeon.datasets import get_dataset_meta_data

metadata = get_dataset_meta_data("GunPoint")
print(metadata)
# {'n_train': 50, 'n_test': 150, 'length': 150, 'n_classes': 2, ...}
```

## Benchmarking Tools

### Loading Published Results

Access pre-computed benchmark results:

```python
from aeon.benchmarking.results_loaders import (
    get_estimator_results,
    get_available_estimators,
)

# Get results for given estimators on given datasets (both are lists)
results = get_estimator_results(
    estimators=["ROCKET"],
    datasets=["GunPoint"],
    task="classification",
)

# Get available estimators for a learning task
estimators = get_available_estimators(task="classification")
```

### Resampling Strategies

Create reproducible train/test splits:

```python
from aeon.benchmarking.resampling import stratified_resample_data

# Pools an existing train/test split, then re-splits at the same sizes while
# preserving class proportions (use a different random_state per resample).
X_train, y_train, X_test, y_test = stratified_resample_data(
    X_train, y_train, X_test, y_test,
    random_state=42,
)
```

### Performance Metrics

Specialized metrics for time series tasks:

**Anomaly Detection Metrics**:
```python
from aeon.benchmarking.metrics.anomaly_detection import (
    range_precision,
    range_recall,
    range_f_score,
    range_roc_auc_score
)

# Range-based metrics for window detection
precision = range_precision(y_true, y_pred, alpha=0.5)
recall = range_recall(y_true, y_pred, alpha=0.5)
f1 = range_f_score(y_true, y_pred, alpha=0.5)
auc = range_roc_auc_score(y_true, y_scores)
```

**Clustering Metrics**:
```python
from aeon.benchmarking.metrics.clustering import clustering_accuracy_score

# Clustering accuracy with optimal label matching
accuracy = clustering_accuracy_score(y_true, y_pred)
```

**Segmentation Metrics**:
```python
from aeon.benchmarking.metrics.segmentation import (
    count_error,
    hausdorff_error
)

# Number of change points difference
count_err = count_error(y_true, y_pred)

# Maximum distance between predicted and true change points
hausdorff_err = hausdorff_error(y_true, y_pred)
```

### Statistical Testing

Post-hoc analysis for algorithm comparison:

```python
from aeon.benchmarking.stats import nemenyi_test, wilcoxon_test

# `results` is a (n_datasets, n_estimators) score matrix; `labels` names columns.
# Wilcoxon returns a (n_estimators, n_estimators) matrix of pairwise p-values.
p_values = wilcoxon_test(results, labels, lower_better=False)
```

## Benchmark Collections

### UCR/UEA Time Series Archives

Access to comprehensive benchmark repositories:

```python
# Classification: 112 univariate + 30 multivariate datasets
X_train, y_train = load_classification("Chinatown", split="train")

# Automatically downloads from timeseriesclassification.com
```

### Monash Forecasting Archive

```python
# Load forecasting datasets
y = load_forecasting("nn5_daily", return_X_y=False)
```

### Published Benchmark Results

Pre-computed results from major competitions:

- 2017 Univariate Bake-off
- 2021 Multivariate Classification
- 2023 Univariate Bake-off

## Workflow Example

Complete benchmarking workflow:

```python
from aeon.datasets import load_classification
from aeon.classification.convolution_based import RocketClassifier
from aeon.benchmarking.results_loaders import get_estimator_results
from sklearn.metrics import accuracy_score

# Load dataset
dataset_name = "GunPoint"
X_train, y_train = load_classification(dataset_name, split="train")
X_test, y_test = load_classification(dataset_name, split="test")

# Train model
clf = RocketClassifier(n_kernels=10000, random_state=42)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

# Evaluate
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")

# Compare with published results (nested dict: {estimator: {dataset: score}})
published = get_estimator_results(estimators=["ROCKET"], datasets=[dataset_name])
print(f"Published ROCKET accuracy: {published['ROCKET'][dataset_name]:.4f}")
```

## Best Practices

### 1. Use Standard Splits

For reproducibility, use provided train/test splits:

```python
# Good: Use standard splits
X_train, y_train = load_classification("GunPoint", split="train")
X_test, y_test = load_classification("GunPoint", split="test")

# Avoid: Creating custom splits
X, y = load_classification("GunPoint")
X_train, X_test, y_train, y_test = train_test_split(X, y)
```

### 2. Set Random Seeds

Ensure reproducibility:

```python
from aeon.benchmarking.resampling import stratified_resample_data

clf = RocketClassifier(random_state=42)
X_tr, y_tr, X_te, y_te = stratified_resample_data(
    X_train, y_train, X_test, y_test, random_state=42
)
```

### 3. Report Multiple Metrics

Don't rely on single metric:

```python
from sklearn.metrics import accuracy_score, f1_score, precision_score

accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred, average='weighted')
precision = precision_score(y_test, y_pred, average='weighted')
```

### 4. Cross-Validation

For robust evaluation on small datasets:

```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(
    clf, X_train, y_train,
    cv=5,
    scoring='accuracy'
)
print(f"CV Accuracy: {scores.mean():.4f} (+/- {scores.std():.4f})")
```

### 5. Compare Against Baselines

Always compare with simple baselines:

```python
from aeon.classification.distance_based import KNeighborsTimeSeriesClassifier

# Simple baseline: 1-NN with Euclidean distance
baseline = KNeighborsTimeSeriesClassifier(n_neighbors=1, distance="euclidean")
baseline.fit(X_train, y_train)
baseline_acc = baseline.score(X_test, y_test)

print(f"Baseline: {baseline_acc:.4f}")
print(f"Your model: {accuracy:.4f}")
```

### 6. Statistical Significance

Test if improvements are statistically significant:

```python
import numpy as np
from aeon.benchmarking.stats import wilcoxon_test

# `results`: rows = datasets, columns = estimators (here 4 datasets x 2 estimators)
results = np.array([
    [0.85, 0.83],
    [0.92, 0.90],
    [0.78, 0.76],
    [0.88, 0.86],
])
labels = ["alg1", "alg2"]

# Returns a (n_estimators, n_estimators) matrix of pairwise p-values.
p_values = wilcoxon_test(results, labels)
if p_values[0, 1] < 0.05:
    print("Difference is statistically significant")
```

## Dataset Discovery

Find datasets matching criteria:

```python
# List all available classification datasets
from aeon.datasets import get_available_datasets

datasets = get_available_datasets("classification")
print(f"Found {len(datasets)} classification datasets")

# Filter by properties
univariate_datasets = [
    d for d in datasets
    if get_dataset_meta_data(d)['n_channels'] == 1
]
```
