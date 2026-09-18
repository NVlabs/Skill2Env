---
name: alterlab-pyhealth
description: Develops, tests, and deploys clinical machine learning models with the PyHealth healthcare AI toolkit. Use when working with electronic health records (EHR), clinical prediction tasks (mortality, readmission, drug recommendation), medical coding systems (ICD, NDC, ATC), physiological signals (EEG, ECG), healthcare datasets (MIMIC-III/IV, eICU, OMOP), or implementing deep learning models for healthcare (RETAIN, SafeDrug, Transformer, GNN). Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read Write Edit Bash(python:*)
compatibility: "Self-contained — runs under `uv run python` with PyHealth 2.0.1 installed; no API key or account required."
metadata:
    skill-author: AlterLab
    version: "1.1.1"
---

# PyHealth: Healthcare AI Toolkit

## Overview

PyHealth is a comprehensive Python library for healthcare AI that provides specialized tools, models, and datasets for clinical machine learning. Use this skill when developing healthcare prediction models, processing clinical data, working with medical coding systems, or deploying AI solutions in healthcare settings.

> **Version gotcha (read first).** This skill targets **PyHealth 2.x** (pin `pyhealth==2.0.1`). The 2.0 rewrite changed the API in ways the wider web (and pre-2024 tutorials) get wrong:
> - **Tasks are classes you instantiate**, e.g. `MortalityPredictionMIMIC4()`, `DrugRecommendationMIMIC3()` — *not* the old snake-case `mortality_prediction_mimic4_fn` functions. Pass the instance to `dataset.set_task(task)`.
> - **Datasets take an explicit `tables=[...]`** list (e.g. `tables=["diagnoses_icd", "procedures_icd", "prescriptions"]`).
> - **Models require `label_key=`** in addition to `feature_keys=` and `mode=`. Common feature keys for EHR tasks are `"conditions"`, `"procedures"`, `"drugs"`.
> - **Metric names have no `_score` suffix**: `pr_auc`, `roc_auc`, `f1`; multilabel/drug-rec use the `*_samples` family (`jaccard_samples`, `f1_samples`, `pr_auc_samples`, `ddi`). Pass `metrics=[...]` to the **`Trainer` constructor**, and `monitor=` one of those names.
> - 2.0.1 requires **Python 3.12 or 3.13** (`>=3.12,<3.14`).
> When unsure of a class/arg name, check the current source rather than trusting older snippets.

## When to Use This Skill

Invoke this skill when:

- **Working with healthcare datasets**: MIMIC-III, MIMIC-IV, eICU, OMOP, sleep EEG data, medical images
- **Clinical prediction tasks**: Mortality prediction, hospital readmission, length of stay, drug recommendation
- **Medical coding**: Translating between ICD-9/10, NDC, RxNorm, ATC coding systems
- **Processing clinical data**: Sequential events, physiological signals, clinical text, medical images
- **Implementing healthcare models**: RETAIN, SafeDrug, GAMENet, StageNet, Transformer for EHR
- **Evaluating clinical models**: Fairness metrics, calibration, interpretability, uncertainty quantification

## Core Capabilities

PyHealth operates through a modular 5-stage pipeline optimized for healthcare AI:

1. **Data Loading**: Access 10+ healthcare datasets with standardized interfaces
2. **Task Definition**: Apply 20+ predefined clinical prediction tasks or create custom tasks
3. **Model Selection**: Choose from 33+ models (baselines, deep learning, healthcare-specific)
4. **Training**: Train with automatic checkpointing, monitoring, and evaluation
5. **Deployment**: Calibrate, interpret, and validate for clinical use

PyHealth 2.x uses a **polars-backed** data layer for fast, memory-efficient processing of large EHR tables.

## Quick Start Workflow

```python
from pyhealth.datasets import MIMIC4Dataset, split_by_patient, get_dataloader
from pyhealth.tasks import MortalityPredictionMIMIC4
from pyhealth.models import Transformer
from pyhealth.trainer import Trainer

# 1. Load dataset (declare the tables you need) and set the task (a class instance)
dataset = MIMIC4Dataset(
    root="/path/to/data",
    tables=["diagnoses_icd", "procedures_icd", "prescriptions"],
)
sample_dataset = dataset.set_task(MortalityPredictionMIMIC4())

# 2. Split data by patient (no leakage across splits)
train, val, test = split_by_patient(sample_dataset, [0.7, 0.1, 0.2])

# 3. Create data loaders
train_loader = get_dataloader(train, batch_size=64, shuffle=True)
val_loader = get_dataloader(val, batch_size=64, shuffle=False)
test_loader = get_dataloader(test, batch_size=64, shuffle=False)

# 4. Initialize and train (feature_keys + label_key + mode all required)
model = Transformer(
    dataset=sample_dataset,
    feature_keys=["conditions", "procedures", "drugs"],
    label_key="mortality",
    mode="binary",
    embedding_dim=128,
)

trainer = Trainer(model=model, metrics=["pr_auc", "roc_auc", "f1"])  # device auto-detected
trainer.train(
    train_dataloader=train_loader,
    val_dataloader=val_loader,
    epochs=50,
    monitor="pr_auc",            # AUPRC — robust for the rare-mortality class
    monitor_criterion="max",
)

# 5. Evaluate (uses the metrics passed to the Trainer)
results = trainer.evaluate(test_loader)
```

## Detailed Documentation

This skill includes comprehensive reference documentation organized by functionality. Read specific reference files as needed:

### 1. Datasets and Data Structures

**File**: `references/datasets.md`

**Read when:**
- Loading healthcare datasets (MIMIC, eICU, OMOP, sleep EEG, etc.)
- Understanding Event, Patient, Visit data structures
- Processing different data types (EHR, signals, images, text)
- Splitting data for training/validation/testing
- Working with SampleDataset for task-specific formatting

**Key Topics:**
- Core data structures (Event, Patient, Visit)
- 10+ available datasets (EHR, physiological signals, imaging, text)
- Data loading and iteration
- Train/val/test splitting strategies
- Performance optimization for large datasets

### 2. Medical Coding Translation

**File**: `references/medical_coding.md`

**Read when:**
- Translating between medical coding systems
- Working with diagnosis codes (ICD-9-CM, ICD-10-CM, CCS)
- Processing medication codes (NDC, RxNorm, ATC)
- Standardizing procedure codes (ICD-9-PROC, ICD-10-PROC)
- Grouping codes into clinical categories
- Handling hierarchical drug classifications

**Key Topics:**
- InnerMap for within-system lookups
- CrossMap for cross-system translation
- Supported coding systems (ICD, NDC, ATC, CCS, RxNorm)
- Code standardization and hierarchy traversal
- Medication classification by therapeutic class
- Integration with datasets

### 3. Clinical Prediction Tasks

**File**: `references/tasks.md`

**Read when:**
- Defining clinical prediction objectives
- Using predefined tasks (mortality, readmission, drug recommendation)
- Working with EHR, signal, imaging, or text-based tasks
- Creating custom prediction tasks
- Setting up input/output schemas for models
- Applying task-specific filtering logic

**Key Topics:**
- 20+ predefined clinical tasks
- EHR tasks (mortality, readmission, length of stay, drug recommendation)
- Signal tasks (sleep staging, EEG analysis, seizure detection)
- Imaging tasks (COVID-19 chest X-ray classification)
- Text tasks (medical coding, specialty classification)
- Custom task creation patterns

### 4. Models and Architectures

**File**: `references/models.md`

**Read when:**
- Selecting models for clinical prediction
- Understanding model architectures and capabilities
- Choosing between general-purpose and healthcare-specific models
- Implementing interpretable models (RETAIN, AdaCare)
- Working with medication recommendation (SafeDrug, GAMENet)
- Using graph neural networks for healthcare
- Configuring model hyperparameters

**Key Topics:**
- 33+ available models
- General-purpose: Logistic Regression, MLP, CNN, RNN, Transformer, GNN
- Healthcare-specific: RETAIN, SafeDrug, GAMENet, StageNet, AdaCare
- Model selection by task type and data type
- Interpretability considerations
- Computational requirements
- Hyperparameter tuning guidelines

### 5. Data Preprocessing

**File**: `references/preprocessing.md`

**Read when:**
- Preprocessing clinical data for models
- Handling sequential events and time-series data
- Processing physiological signals (EEG, ECG)
- Normalizing lab values and vital signs
- Preparing labels for different task types
- Building feature vocabularies
- Managing missing data and outliers

**Key Topics:**
- 15+ processor types
- Sequence processing (padding, truncation)
- Signal processing (filtering, segmentation)
- Feature extraction and encoding
- Label processors (binary, multi-class, multi-label, regression)
- Text and image preprocessing
- Common preprocessing workflows

### 6. Training and Evaluation

**File**: `references/training_evaluation.md`

**Read when:**
- Training models with the Trainer class
- Evaluating model performance
- Computing clinical metrics
- Assessing model fairness across demographics
- Calibrating predictions for reliability
- Quantifying prediction uncertainty
- Interpreting model predictions
- Preparing models for clinical deployment

**Key Topics:**
- Trainer class (train, evaluate, inference)
- Metrics for binary, multi-class, multi-label, regression tasks
- Fairness metrics for bias assessment
- Calibration methods (Platt scaling, temperature scaling)
- Uncertainty quantification (conformal prediction, MC dropout)
- Interpretability tools (attention visualization, SHAP, Chefer relevance via `pyhealth.interpret.methods.CheferRelevance`)
- Complete training pipeline example

## Installation

```bash
uv pip install "pyhealth==2.0.1"
```

**Requirements (PyHealth 2.0.1):**
- Python **3.12 or 3.13** (`>=3.12,<3.14`) — note this machine's default `uv` Python is 3.14, which is *outside* the supported range; create the env with `uv venv --python 3.13` for PyHealth work.
- PyTorch (pulled in as a dependency)
- NumPy, pandas, polars, scikit-learn

## Common Use Cases

### Use Case 1: ICU Mortality Prediction

**Objective**: Predict patient mortality in intensive care unit

**Approach:**
1. Load MIMIC-IV dataset → Read `references/datasets.md`
2. Apply mortality prediction task → Read `references/tasks.md`
3. Select interpretable model (RETAIN) → Read `references/models.md`
4. Train and evaluate → Read `references/training_evaluation.md`
5. Interpret predictions for clinical use → Read `references/training_evaluation.md`

### Use Case 2: Safe Medication Recommendation

**Objective**: Recommend medications while avoiding drug-drug interactions

**Approach:**
1. Load EHR dataset (MIMIC-IV or OMOP) → Read `references/datasets.md`
2. Apply drug recommendation task → Read `references/tasks.md`
3. Use SafeDrug model with DDI constraints → Read `references/models.md`
4. Preprocess medication codes → Read `references/medical_coding.md`
5. Evaluate with multi-label metrics → Read `references/training_evaluation.md`

### Use Case 3: Hospital Readmission Prediction

**Objective**: Identify patients at risk of 30-day readmission

**Approach:**
1. Load multi-site EHR data (eICU or OMOP) → Read `references/datasets.md`
2. Apply readmission prediction task → Read `references/tasks.md`
3. Handle class imbalance in preprocessing → Read `references/preprocessing.md`
4. Train Transformer model → Read `references/models.md`
5. Calibrate predictions and assess fairness → Read `references/training_evaluation.md`

### Use Case 4: Sleep Disorder Diagnosis

**Objective**: Classify sleep stages from EEG signals

**Approach:**
1. Load sleep EEG dataset (SleepEDF, SHHS) → Read `references/datasets.md`
2. Apply sleep staging task → Read `references/tasks.md`
3. Preprocess EEG signals (filtering, segmentation) → Read `references/preprocessing.md`
4. Train CNN or RNN model → Read `references/models.md`
5. Evaluate per-stage performance → Read `references/training_evaluation.md`

### Use Case 5: Medical Code Translation

**Objective**: Standardize diagnoses across different coding systems

**Approach:**
1. Read `references/medical_coding.md` for comprehensive guidance
2. Use CrossMap to translate between ICD-9, ICD-10, CCS
3. Group codes into clinically meaningful categories
4. Integrate with dataset processing

### Use Case 6: Clinical Text to ICD Coding

**Objective**: Automatically assign ICD codes from clinical notes

**Approach:**
1. Load MIMIC-III with clinical text → Read `references/datasets.md`
2. Apply ICD coding task → Read `references/tasks.md`
3. Preprocess clinical text → Read `references/preprocessing.md`
4. Use TransformersModel (ClinicalBERT) → Read `references/models.md`
5. Evaluate with multi-label metrics → Read `references/training_evaluation.md`

## Best Practices

### Data Handling

1. **Always split by patient**: Prevent data leakage by ensuring no patient appears in multiple splits
   ```python
   from pyhealth.datasets import split_by_patient
   train, val, test = split_by_patient(dataset, [0.7, 0.1, 0.2])
   ```

2. **Check dataset statistics**: Understand your data before modeling
   ```python
   print(dataset.stats())  # Patients, visits, events, code distributions
   ```

3. **Use appropriate preprocessing**: Match processors to data types (see `references/preprocessing.md`)

### Model Development

1. **Start with baselines**: Establish baseline performance with simple models
   - Logistic Regression for binary/multi-class tasks
   - MLP for initial deep learning baseline

2. **Choose task-appropriate models**:
   - Interpretability needed → RETAIN, AdaCare
   - Drug recommendation → SafeDrug, GAMENet
   - Long sequences → Transformer
   - Graph relationships → GNN

3. **Monitor validation metrics**: Use appropriate metrics for task and handle class imbalance. PyHealth metric strings (pass to `Trainer(metrics=[...])` / `monitor=`):
   - Binary: `roc_auc`, `pr_auc` (prefer `pr_auc` for rare events), `f1`, `accuracy`
   - Multi-class: `f1_macro`, `f1_weighted`, `accuracy`, `cohen_kappa`
   - Multi-label / drug-rec: `jaccard_samples`, `f1_samples`, `pr_auc_samples`, `ddi`
   - Regression: `mae`, `mse`, `r2`

### Clinical Deployment

1. **Calibrate predictions**: Ensure probabilities are reliable (see `references/training_evaluation.md`)

2. **Assess fairness**: Evaluate across demographic groups to detect bias

3. **Quantify uncertainty**: Provide confidence estimates for predictions

4. **Interpret predictions**: Use attention weights, SHAP, or Chefer relevance for clinical trust

5. **Validate thoroughly**: Use held-out test sets from different time periods or sites

## Limitations and Considerations

### Data Requirements

- **Large datasets**: Deep learning models require sufficient data (thousands of patients)
- **Data quality**: Missing data and coding errors impact performance
- **Temporal consistency**: Ensure train/test split respects temporal ordering when needed

### Clinical Validation

- **External validation**: Test on data from different hospitals/systems
- **Prospective evaluation**: Validate in real clinical settings before deployment
- **Clinical review**: Have clinicians review predictions and interpretations
- **Ethical considerations**: Address privacy (HIPAA/GDPR), fairness, and safety

### Computational Resources

- **GPU recommended**: For training deep learning models efficiently
- **Memory requirements**: Large datasets may require 16GB+ RAM
- **Storage**: Healthcare datasets can be 10s-100s of GB

## Troubleshooting

### Common Issues

**ImportError for dataset**:
- Ensure dataset files are downloaded and path is correct
- Check PyHealth version compatibility

**Out of memory**:
- Reduce batch size
- Reduce sequence length (`max_seq_length`)
- Use gradient accumulation
- Process data in chunks

**Poor performance**:
- Check class imbalance and use appropriate metrics (`pr_auc` vs `roc_auc`)
- Verify preprocessing (normalization, missing data handling)
- Increase model capacity or training epochs
- Check for data leakage in train/test split

**Slow training**:
- Use GPU (`device="cuda"`)
- Increase batch size (if memory allows)
- Reduce sequence length
- Use more efficient model (CNN vs Transformer)

### Getting Help

- **Documentation**: https://pyhealth.readthedocs.io/
- **GitHub Issues**: https://github.com/sunlabuiuc/PyHealth/issues
- **Examples/notebooks**: https://github.com/sunlabuiuc/PyHealth/tree/master/examples

## Example: Complete Workflow

```python
# Complete mortality prediction pipeline
from pyhealth.datasets import MIMIC4Dataset, split_by_patient, get_dataloader
from pyhealth.tasks import MortalityPredictionMIMIC4
from pyhealth.models import RETAIN
from pyhealth.trainer import Trainer

# 1. Load dataset (declare the tables the task needs)
print("Loading MIMIC-IV dataset...")
dataset = MIMIC4Dataset(
    root="/data/mimic4",
    tables=["diagnoses_icd", "procedures_icd", "prescriptions"],
)
print(dataset.stats())

# 2. Define task (instantiate the task class)
print("Setting mortality prediction task...")
sample_dataset = dataset.set_task(MortalityPredictionMIMIC4())
print(f"Generated {len(sample_dataset)} samples")

# 3. Split data (by patient to prevent leakage)
print("Splitting data...")
train_ds, val_ds, test_ds = split_by_patient(
    sample_dataset, ratios=[0.7, 0.1, 0.2], seed=42
)

# 4. Create data loaders
train_loader = get_dataloader(train_ds, batch_size=64, shuffle=True)
val_loader = get_dataloader(val_ds, batch_size=64)
test_loader = get_dataloader(test_ds, batch_size=64)

# 5. Initialize interpretable model (label_key is required)
print("Initializing RETAIN model...")
model = RETAIN(
    dataset=sample_dataset,
    feature_keys=["conditions", "procedures", "drugs"],
    label_key="mortality",
    mode="binary",
    embedding_dim=128,
)

# 6. Train model
print("Training model...")
import torch
trainer = Trainer(
    model=model,
    metrics=["accuracy", "pr_auc", "roc_auc", "f1"],
)
trainer.train(
    train_dataloader=train_loader,
    val_dataloader=val_loader,
    epochs=50,
    optimizer_class=torch.optim.Adam,
    optimizer_params={"lr": 1e-3, "weight_decay": 1e-5},
    monitor="pr_auc",          # Use AUPRC for the imbalanced (rare-mortality) outcome
    monitor_criterion="max",
)

# 7. Evaluate on test set (uses the metrics passed to the Trainer)
print("Evaluating on test set...")
test_results = trainer.evaluate(test_loader)

print("\nTest Results:")
for metric, value in test_results.items():
    print(f"  {metric}: {value:.4f}")

# 8. Get predictions for analysis.
# inference() returns (y_true, y_prob, loss) by default; requesting extras
# extends the tuple to (y_true, y_prob, loss, additional_outputs, patient_ids).
y_true, y_prob, loss, extra, patient_ids = trainer.inference(
    test_loader,
    additional_outputs=["attention_weights"],
    return_patient_ids=True,
)

# 9. Flag the highest-risk patient
positive_prob = y_prob if y_prob.ndim == 1 else y_prob[..., -1]
high_risk_idx = int(positive_prob.argmax())
print(f"\nHighest-risk patient: {patient_ids[high_risk_idx]}")
print(f"Risk score: {float(positive_prob[high_risk_idx]):.3f}")

# 10. Feature-level interpretation via Chefer relevance (works on attention models)
from pyhealth.interpret.methods import CheferRelevance
relevance = CheferRelevance(model)
one = get_dataloader(test, batch_size=1, shuffle=False)
scores = relevance.get_relevance_matrix(**next(iter(one)))
for feature_key, rel in scores.items():
    print(f"{feature_key}: top tokens -> {rel[0].topk(5).indices.tolist()}")

# 11. Save the trained model
trainer.save("./models/mortality_retain_final.pt")
print("\nModel saved successfully!")
```

## Resources

For detailed information on each component, refer to the comprehensive reference files in the `references/` directory:

- **datasets.md**: Data structures, loading, and splitting (4,500 words)
- **medical_coding.md**: Code translation and standardization (3,800 words)
- **tasks.md**: Clinical prediction tasks and custom task creation (4,200 words)
- **models.md**: Model architectures and selection guidelines (5,100 words)
- **preprocessing.md**: Data processors and preprocessing workflows (4,600 words)
- **training_evaluation.md**: Training, metrics, calibration, interpretability (5,900 words)

**Total comprehensive documentation**: ~28,000 words across modular reference files.

