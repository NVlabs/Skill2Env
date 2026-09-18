# PyHealth Training, Evaluation, and Interpretability

## Overview

PyHealth provides comprehensive tools for training models, evaluating predictions, ensuring model reliability, and interpreting results for clinical applications.

## Trainer Class

### Core Functionality

The `Trainer` class manages the complete model training and evaluation workflow with PyTorch integration.

**Initialization:**
```python
from pyhealth.trainer import Trainer

trainer = Trainer(
    model=model,                          # PyHealth model
    metrics=["pr_auc", "roc_auc", "f1"],  # metrics computed by evaluate()
    # device is auto-detected; pass device="cpu"/"cuda" to override
)
```

The metric list you pass here is what `evaluate()` reports and what `monitor=` can reference during training.

### Training

**train() method**

Trains models with comprehensive monitoring and checkpointing.

**Parameters:**
- `train_dataloader`: Training data loader
- `val_dataloader`: Validation data loader (optional)
- `epochs`: Number of training epochs
- `optimizer_class`: Optimizer **class** (e.g. `torch.optim.Adam`, `torch.optim.AdamW`)
- `optimizer_params`: Dict of optimizer kwargs (e.g. `{"lr": 1e-3, "weight_decay": 1e-5}`)
- `monitor`: Metric to monitor — one of the names passed to `Trainer(metrics=...)`, e.g. `"pr_auc"`
- `monitor_criterion`: "max" or "min"

**Usage:**
```python
import torch

trainer.train(
    train_dataloader=train_loader,
    val_dataloader=val_loader,
    epochs=50,
    optimizer_class=torch.optim.Adam,
    optimizer_params={"lr": 1e-3, "weight_decay": 1e-5},
    monitor="pr_auc",
    monitor_criterion="max",
)
```

**Training Features:**

1. **Automatic Checkpointing**: Saves best model based on monitored metric

2. **Early Stopping**: Stops training if no improvement

3. **Gradient Clipping**: Prevents exploding gradients

4. **Progress Tracking**: Displays training progress and metrics

5. **Multi-GPU Support**: Automatic device placement

### Inference

**inference() method**

Performs predictions on datasets.

**Parameters:**
- `dataloader`: Data loader for inference
- `additional_outputs`: List of additional outputs to return
- `return_patient_ids`: Return patient identifiers

**Usage:**
```python
# Default: returns a 3-tuple
y_true, y_prob, loss = trainer.inference(test_loader)

# With extras: returns a 5-tuple (order matters)
y_true, y_prob, loss, additional_outputs, patient_ids = trainer.inference(
    test_loader,
    additional_outputs=["attention_weights"],
    return_patient_ids=True,
)
```

**Returns (tuple, not a dict):**
- `y_true`: Ground truth labels (array)
- `y_prob`: Predicted probabilities (array)
- `loss` / `mean_loss`: Mean loss over the dataset
- `additional_outputs`: Dict of requested extras (only if `additional_outputs=` given)
- `patient_ids`: Patient identifiers (only if `return_patient_ids=True`)

### Evaluation

**evaluate() method**

Computes comprehensive evaluation metrics.

**Parameters:**
- `dataloader`: Data loader for evaluation

`evaluate()` uses the metric list set on the `Trainer` (`Trainer(metrics=[...])`) — it does **not** take a `metrics=` argument. To compute metrics ad hoc, call the metric function directly on `inference()` outputs.

**Usage:**
```python
# Uses metrics passed to Trainer(...)
results = trainer.evaluate(test_loader)
print(results)
# e.g. {'pr_auc': 0.78, 'roc_auc': 0.82, 'f1': 0.73}

# Or compute metrics manually from predictions
from pyhealth.metrics.binary import binary_metrics_fn

y_true, y_prob, loss = trainer.inference(test_loader)
binary_metrics_fn(y_true, y_prob, metrics=["pr_auc", "roc_auc", "f1"])
```

### Checkpoint Management

**save() method**
```python
trainer.save("./models/best_model.pt")
```

**load() method**
```python
trainer.load("./models/best_model.pt")
```

## Evaluation Metrics

### Binary Classification Metrics

**Available metric strings:**
- `accuracy`: Overall accuracy
- `f1`: F1 score
- `precision_recall_f1` / `precision` / `recall`
- `roc_auc`: Area under ROC curve
- `pr_auc`: Area under precision-recall curve
- `cohen_kappa`: Inter-rater reliability

(Strings have no `_score` suffix.)

**Usage:**
```python
from pyhealth.metrics.binary import binary_metrics_fn

# Note: arg is y_prob (predicted probabilities), not thresholded y_pred
metrics = binary_metrics_fn(
    y_true=labels,
    y_prob=probabilities,
    metrics=["accuracy", "f1", "pr_auc", "roc_auc"],
)
```

**Threshold Selection:**
```python
# Default threshold: 0.5
predictions_binary = (predictions > 0.5).astype(int)

# Optimal threshold by F1
from sklearn.metrics import f1_score
thresholds = np.arange(0.1, 0.9, 0.05)
f1_scores = [f1_score(y_true, (y_pred > t).astype(int)) for t in thresholds]
optimal_threshold = thresholds[np.argmax(f1_scores)]
```

**Best Practices:**
- **Use AUROC**: Overall model discrimination
- **Use AUPRC**: Especially for imbalanced classes
- **Use F1**: Balance precision and recall
- **Report confidence intervals**: Bootstrap resampling

### Multi-Class Classification Metrics

**Available metric strings:**
- `accuracy`: Overall accuracy
- `f1_macro`: Unweighted mean F1 across classes
- `f1_micro`: Global F1 (total TP, FP, FN)
- `f1_weighted`: Weighted mean F1 by class frequency
- `cohen_kappa`: Multi-class kappa

**Usage:**
```python
from pyhealth.metrics.multiclass import multiclass_metrics_fn

metrics = multiclass_metrics_fn(
    y_true=labels,
    y_prob=probabilities,
    metrics=["accuracy", "f1_macro", "f1_weighted"],
)
```

**Per-Class Metrics:**
```python
from sklearn.metrics import classification_report

print(classification_report(y_true, y_pred,
    target_names=["Wake", "N1", "N2", "N3", "REM"]))
```

**Confusion Matrix:**
```python
from sklearn.metrics import confusion_matrix
import seaborn as sns

cm = confusion_matrix(y_true, y_pred)
sns.heatmap(cm, annot=True, fmt='d')
```

### Multi-Label Classification Metrics

**Available metric strings** (the `*_samples` family is the per-example average used for drug recommendation):
- `jaccard_samples`: Sample-averaged Jaccard (intersection over union)
- `f1_samples`: Sample-averaged F1
- `pr_auc_samples`: Sample-averaged AUPRC
- `hamming_loss`: Fraction of incorrect labels
- `ddi`: Drug-drug interaction rate (drug-rec models)

**Usage:**
```python
from pyhealth.metrics.multilabel import multilabel_metrics_fn

# y_prob: [n_samples, n_labels] probability matrix
metrics = multilabel_metrics_fn(
    y_true=label_matrix,
    y_prob=prob_matrix,
    metrics=["jaccard_samples", "f1_samples", "pr_auc_samples"],
)
```

**Drug Recommendation Metrics:**
```python
# Jaccard similarity (intersection/union)
jaccard = len(set(true_drugs) & set(pred_drugs)) / len(set(true_drugs) | set(pred_drugs))

# Precision@k: Precision for top-k predictions
def precision_at_k(y_true, y_pred, k=10):
    top_k_pred = y_pred.argsort()[-k:]
    return len(set(y_true) & set(top_k_pred)) / k
```

### Regression Metrics

**Available metric strings:**
- `mae`: Mean absolute error
- `mse`: Mean squared error
- `rmse`: Root mean squared error
- `r2`: Coefficient of determination

**Usage:**
```python
from pyhealth.metrics.regression import regression_metrics_fn

metrics = regression_metrics_fn(
    y_true=true_values,
    y_prob=predictions,
    metrics=["mae", "rmse", "r2"],
)
```

**Percentage Error Metrics:**
```python
# Mean Absolute Percentage Error
mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100

# Median Absolute Percentage Error (robust to outliers)
medape = np.median(np.abs((y_true - y_pred) / y_true)) * 100
```

### Fairness Metrics

**Purpose:** Assess model bias across a protected vs. unprotected group.

**`pyhealth.metrics.fairness.fairness_metrics_fn`** — available metric strings:
- `disparate_impact`: Ratio of favorable-outcome rates (protected / unprotected)
- `statistical_parity_difference`: Difference in favorable-outcome rates

**Signature:** `fairness_metrics_fn(y_true, y_prob, sensitive_attributes, favorable_outcome=1, metrics=[...], threshold=0.5)` where `sensitive_attributes` is a 0/1 array (1 = protected group).

**Usage:**
```python
from pyhealth.metrics.fairness import fairness_metrics_fn

# sensitive_attributes: 1 for the protected group, 0 otherwise
fairness_results = fairness_metrics_fn(
    y_true=labels,
    y_prob=probabilities,
    sensitive_attributes=protected_mask,
    favorable_outcome=1,
    metrics=["disparate_impact", "statistical_parity_difference"],
)
```

**Example:**
```python
# Evaluate fairness across gender
male_mask = (demographics == "male")
female_mask = (demographics == "female")

male_tpr = recall_score(y_true[male_mask], y_pred[male_mask])
female_tpr = recall_score(y_true[female_mask], y_pred[female_mask])

tpr_disparity = abs(male_tpr - female_tpr)
print(f"TPR disparity: {tpr_disparity:.3f}")
```

## Calibration and Uncertainty Quantification

### Model Calibration

**Purpose:** Ensure predicted probabilities match actual frequencies

**Calibration Plot:**
```python
from sklearn.calibration import calibration_curve
import matplotlib.pyplot as plt

fraction_of_positives, mean_predicted_value = calibration_curve(
    y_true, y_prob, n_bins=10
)

plt.plot(mean_predicted_value, fraction_of_positives, marker='o')
plt.plot([0, 1], [0, 1], linestyle='--', label='Perfect calibration')
plt.xlabel('Mean predicted probability')
plt.ylabel('Fraction of positives')
plt.legend()
```

**Expected Calibration Error (ECE):**
```python
def expected_calibration_error(y_true, y_prob, n_bins=10):
    """Compute ECE"""
    bins = np.linspace(0, 1, n_bins + 1)
    bin_indices = np.digitize(y_prob, bins) - 1

    ece = 0
    for i in range(n_bins):
        mask = bin_indices == i
        if mask.sum() > 0:
            bin_accuracy = y_true[mask].mean()
            bin_confidence = y_prob[mask].mean()
            ece += mask.sum() / len(y_true) * abs(bin_accuracy - bin_confidence)

    return ece
```

**Calibration Methods:**

1. **Platt Scaling**: Logistic regression on validation predictions
```python
from sklearn.linear_model import LogisticRegression

calibrator = LogisticRegression()
calibrator.fit(val_predictions.reshape(-1, 1), val_labels)
calibrated_probs = calibrator.predict_proba(test_predictions.reshape(-1, 1))[:, 1]
```

2. **Isotonic Regression**: Non-parametric calibration
```python
from sklearn.isotonic import IsotonicRegression

calibrator = IsotonicRegression(out_of_bounds='clip')
calibrator.fit(val_predictions, val_labels)
calibrated_probs = calibrator.predict(test_predictions)
```

3. **Temperature Scaling**: Scale logits before softmax
```python
def find_temperature(logits, labels):
    """Find optimal temperature parameter"""
    from scipy.optimize import minimize

    def nll(temp):
        scaled_logits = logits / temp
        probs = torch.softmax(scaled_logits, dim=1)
        return F.cross_entropy(probs, labels).item()

    result = minimize(nll, x0=1.0, method='BFGS')
    return result.x[0]

temperature = find_temperature(val_logits, val_labels)
calibrated_logits = test_logits / temperature
```

### Uncertainty Quantification

**Conformal Prediction:**

Provide prediction sets with guaranteed coverage.

**Usage:**
```python
from pyhealth.metrics import prediction_set_metrics_fn

# Calibrate on validation set
scores = 1 - val_predictions[np.arange(len(val_labels)), val_labels]
quantile_level = np.quantile(scores, 0.9)  # 90% coverage

# Generate prediction sets on test set
prediction_sets = test_predictions > (1 - quantile_level)

# Evaluate
metrics = prediction_set_metrics_fn(
    y_true=test_labels,
    prediction_sets=prediction_sets,
    metrics=["coverage", "average_size"]
)
```

**Monte Carlo Dropout:**

Estimate uncertainty through dropout at inference.

```python
def predict_with_uncertainty(model, dataloader, num_samples=20):
    """Predict with uncertainty using MC dropout"""
    model.train()  # Keep dropout active

    predictions = []
    for _ in range(num_samples):
        batch_preds = []
        for batch in dataloader:
            with torch.no_grad():
                output = model(batch)
                batch_preds.append(output)
        predictions.append(torch.cat(batch_preds))

    predictions = torch.stack(predictions)
    mean_pred = predictions.mean(dim=0)
    std_pred = predictions.std(dim=0)  # Uncertainty

    return mean_pred, std_pred
```

**Ensemble Uncertainty:**

```python
# Train multiple models
models = [train_model(seed=i) for i in range(5)]

# Predict with ensemble
ensemble_preds = []
for model in models:
    pred = model.predict(test_data)
    ensemble_preds.append(pred)

mean_pred = np.mean(ensemble_preds, axis=0)
std_pred = np.std(ensemble_preds, axis=0)  # Uncertainty
```

## Interpretability

### Attention Visualization

**For Transformer and RETAIN models:**

```python
# Get attention weights during inference
outputs = trainer.inference(
    test_loader,
    additional_outputs=["attention_weights"]
)

attention = outputs["attention_weights"]

# Visualize attention for sample
import matplotlib.pyplot as plt
import seaborn as sns

sample_idx = 0
sample_attention = attention[sample_idx]  # [seq_length, seq_length]

sns.heatmap(sample_attention, cmap='viridis')
plt.xlabel('Key Position')
plt.ylabel('Query Position')
plt.title('Attention Weights')
plt.show()
```

**RETAIN Interpretation:**

```python
# RETAIN provides visit-level and feature-level attention
visit_attention = outputs["visit_attention"]  # Which visits are important
feature_attention = outputs["feature_attention"]  # Which features are important

# Find most influential visit
most_important_visit = visit_attention[sample_idx].argmax()

# Find most influential features in that visit
important_features = feature_attention[sample_idx, most_important_visit].argsort()[-10:]
```

### Feature Importance

**Permutation Importance:**

```python
from sklearn.inspection import permutation_importance

def get_predictions(model, X):
    return model.predict(X)

result = permutation_importance(
    model, X_test, y_test,
    n_repeats=10,
    scoring='roc_auc'
)

# Sort features by importance
indices = result.importances_mean.argsort()[::-1]
for i in indices[:10]:
    print(f"{feature_names[i]}: {result.importances_mean[i]:.3f}")
```

**SHAP Values:**

```python
import shap

# Create explainer
explainer = shap.DeepExplainer(model, train_data)

# Compute SHAP values
shap_values = explainer.shap_values(test_data)

# Visualize
shap.summary_plot(shap_values, test_data, feature_names=feature_names)
```

### Chefer Relevance (PyHealth's built-in attention interpretability)

PyHealth ships the Chefer relevance method for attention-based models (e.g. `Transformer`). The class is `CheferRelevance` in `pyhealth.interpret.methods`; call `get_relevance_matrix(**batch)` on a single-sample batch.

```python
from pyhealth.interpret.methods import CheferRelevance
from pyhealth.datasets import get_dataloader

relevance = CheferRelevance(model)

# One sample at a time (batch_size=1)
loader = get_dataloader(test_dataset, batch_size=1, shuffle=False)
batch = next(iter(loader))

scores = relevance.get_relevance_matrix(**batch)  # dict: feature_key -> relevance tensor
for feature_key, rel in scores.items():
    top_tokens = rel[0].topk(5).indices
    print(f"{feature_key}: top-5 tokens -> {top_tokens.tolist()}")
```

## Complete Training Pipeline Example

```python
import torch
from pyhealth.datasets import MIMIC4Dataset, split_by_patient, get_dataloader
from pyhealth.tasks import MortalityPredictionMIMIC4
from pyhealth.models import Transformer
from pyhealth.trainer import Trainer

# 1. Load and prepare data
dataset = MIMIC4Dataset(
    root="/path/to/mimic4",
    tables=["diagnoses_icd", "procedures_icd", "prescriptions"],
)
sample_dataset = dataset.set_task(MortalityPredictionMIMIC4())

# 2. Split data by patient
train_data, val_data, test_data = split_by_patient(
    sample_dataset, [0.7, 0.1, 0.2]
)

# 3. Create data loaders
train_loader = get_dataloader(train_data, batch_size=64, shuffle=True)
val_loader = get_dataloader(val_data, batch_size=64, shuffle=False)
test_loader = get_dataloader(test_data, batch_size=64, shuffle=False)

# 4. Initialize model
model = Transformer(
    dataset=sample_dataset,
    feature_keys=["conditions", "procedures", "drugs"],
    label_key="mortality",
    mode="binary",
    embedding_dim=128,
    num_layers=2,
    dropout=0.3,
)

# 5. Train model
trainer = Trainer(model=model, metrics=["accuracy", "pr_auc", "roc_auc", "f1"])
trainer.train(
    train_dataloader=train_loader,
    val_dataloader=val_loader,
    epochs=50,
    optimizer_class=torch.optim.Adam,
    optimizer_params={"lr": 1e-3, "weight_decay": 1e-5},
    monitor="pr_auc",
    monitor_criterion="max",
)

# 6. Evaluate on test set (uses the Trainer's metric list)
test_results = trainer.evaluate(test_loader)
print("Test Results:")
for metric, value in test_results.items():
    print(f"{metric}: {value:.4f}")

# 7. Get predictions for analysis (tuple unpacking)
y_true, y_prob, loss = trainer.inference(test_loader)

# 8. Calibration analysis
from sklearn.calibration import calibration_curve

positive_prob = y_prob if y_prob.ndim == 1 else y_prob[..., -1]
fraction_pos, mean_pred = calibration_curve(y_true, positive_prob, n_bins=10)
ece = expected_calibration_error(y_true, positive_prob)
print(f"Expected Calibration Error: {ece:.4f}")

# 9. Save final model
trainer.save("./models/mortality_transformer_final.pt")
```

## Best Practices

### Training

1. **Monitor multiple metrics**: Track both loss and task-specific metrics
2. **Use validation set**: Prevent overfitting with early stopping
3. **Gradient clipping**: Stabilize training (max_grad_norm=5.0)
4. **Learning rate scheduling**: Reduce LR on plateau
5. **Checkpoint best model**: Save based on validation performance

### Evaluation

1. **Use task-appropriate metrics**: AUROC/AUPRC for binary, macro-F1 for imbalanced multi-class
2. **Report confidence intervals**: Bootstrap or cross-validation
3. **Stratified evaluation**: Report metrics by subgroups
4. **Clinical metrics**: Include clinically relevant thresholds
5. **Fairness assessment**: Evaluate across demographic groups

### Deployment

1. **Calibrate predictions**: Ensure probabilities are reliable
2. **Quantify uncertainty**: Provide confidence estimates
3. **Monitor performance**: Track metrics in production
4. **Handle distribution shift**: Detect when data changes
5. **Interpretability**: Provide explanations for predictions
