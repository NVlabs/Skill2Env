---
name: alterlab-timesfm
description: Zero-shot univariate time-series forecasting with Google's TimesFM foundation model, producing point forecasts and prediction intervals from CSV/DataFrame/array inputs, with a preflight system checker for RAM/GPU. Use to forecast any univariate series (sales, sensors, energy, vitals, weather) without training a custom model. Part of the AlterLab Academic Skills suite.
allowed-tools: Read Write Edit Bash
license: Apache-2.0
compatibility: No API key required. Runs locally via `uv run python`; requires the timesfm Python package (downloads the TimesFM model weights on first use; GPU optional).
metadata:
  skill-author: AlterLab
  version: "1.0.0"
---

# TimesFM Forecasting

## Overview

TimesFM (Time Series Foundation Model) is a pretrained decoder-only foundation model
developed by Google Research for time-series forecasting. It works **zero-shot** — feed it
any univariate time series and it returns point forecasts with calibrated quantile
prediction intervals, no training required.

This skill wraps TimesFM for safe, agent-friendly local inference. It includes a
**mandatory preflight system checker** that verifies RAM, GPU memory, and disk space
before the model is ever loaded so the agent never crashes a user's machine.

> **Key numbers**: TimesFM 2.5 uses 200M parameters (~800 MB on disk, ~1.5 GB in RAM on
> CPU, ~1 GB VRAM on GPU). The archived v1/v2 500M-parameter model needs ~32 GB RAM.
> Always run the system checker first.

## When to Use This Skill

Use this skill when:

- Forecasting **any univariate time series** (sales, demand, sensor, vitals, price, weather)
- You need **zero-shot forecasting** without training a custom model
- You want **probabilistic forecasts** with calibrated prediction intervals (quantiles)
- You have time series of **any length** (the model handles 1–16,384 context points)
- You need to **batch-forecast** hundreds or thousands of series efficiently
- You want a **foundation model** approach instead of hand-tuning ARIMA/ETS parameters

Do **not** use this skill when:

- You need classical statistical models with coefficient interpretation → use `statsmodels`
- You need time series classification or clustering → use `aeon`
- You need multivariate vector autoregression or Granger causality → use `statsmodels`
- Your data is tabular (not temporal) → use `scikit-learn`

> **Note on Anomaly Detection**: TimesFM does not have built-in anomaly detection, but you can
> use the **quantile forecasts as prediction intervals** — values outside the 80% CI (q10–q90)
> are statistically unusual. See the `examples/anomaly-detection/` directory for a full example.

## ⚠️ Mandatory Preflight: System Requirements Check

**CRITICAL — ALWAYS run the system checker before loading the model for the first time.**

```bash
python scripts/check_system.py
```

This script checks:

1. **Available RAM** — warns if below 4 GB, blocks if below 2 GB
2. **GPU availability** — detects CUDA/MPS devices and VRAM
3. **Disk space** — verifies room for the ~800 MB model download
4. **Python version** — requires 3.10+
5. **Existing installation** — checks if `timesfm` and `torch` are installed

> **Note:** Model weights are **NOT stored in this repository**. TimesFM weights (~800 MB)
> download on-demand from HuggingFace on first use and cache in `~/.cache/huggingface/`.
> The preflight checker ensures sufficient resources before any download begins.

```mermaid
flowchart TD
    accTitle: Preflight System Check
    accDescr: Decision flowchart showing the system requirement checks that must pass before loading TimesFM.

    start["🚀 Run check_system.py"] --> ram{"RAM ≥ 4 GB?"}
    ram -->|"Yes"| gpu{"GPU available?"}
    ram -->|"No (2-4 GB)"| warn_ram["⚠️ Warning: tight RAM<br/>CPU-only, small batches"]
    ram -->|"No (< 2 GB)"| block["🛑 BLOCKED<br/>Insufficient memory"]
    warn_ram --> disk
    gpu -->|"CUDA / MPS"| vram{"VRAM ≥ 2 GB?"}
    gpu -->|"CPU only"| cpu_ok["✅ CPU mode<br/>Slower but works"]
    vram -->|"Yes"| gpu_ok["✅ GPU mode<br/>Fast inference"]
    vram -->|"No"| cpu_ok
    gpu_ok --> disk{"Disk ≥ 2 GB free?"}
    cpu_ok --> disk
    disk -->|"Yes"| ready["✅ READY<br/>Safe to load model"]
    disk -->|"No"| block_disk["🛑 BLOCKED<br/>Need space for weights"]

    classDef ok fill:#dcfce7,stroke:#16a34a,stroke-width:2px,color:#14532d
    classDef warn fill:#fef9c3,stroke:#ca8a04,stroke-width:2px,color:#713f12
    classDef block fill:#fee2e2,stroke:#dc2626,stroke-width:2px,color:#7f1d1d
    classDef neutral fill:#f3f4f6,stroke:#6b7280,stroke-width:2px,color:#1f2937

    class ready,gpu_ok,cpu_ok ok
    class warn_ram warn
    class block,block_disk block
    class start,ram,gpu,vram,disk neutral
```

### Hardware Requirements by Model Version

| Model | Parameters | RAM (CPU) | VRAM (GPU) | Disk | Context |
| ----- | ---------- | --------- | ---------- | ---- | ------- |
| **TimesFM 2.5** (recommended) | 200M | ≥ 4 GB | ≥ 2 GB | ~800 MB | up to 16,384 |
| TimesFM 2.0 (archived) | 500M | ≥ 16 GB | ≥ 8 GB | ~2 GB | up to 2,048 |
| TimesFM 1.0 (archived) | 200M | ≥ 8 GB | ≥ 4 GB | ~800 MB | up to 2,048 |

> **Recommendation**: Always use TimesFM 2.5 unless you have a specific reason to use an
> older checkpoint. It is smaller, faster, and supports 8× longer context.

## 🔧 Installation

### Step 1: Verify System (always first)

```bash
python scripts/check_system.py
```

### Step 2: Install TimesFM

```bash
# Using uv (recommended by this repo)
uv pip install timesfm[torch]

# Or using pip
pip install timesfm[torch]

# For JAX/Flax backend (faster on TPU/GPU)
uv pip install timesfm[flax]
```

### Step 3: Install PyTorch for Your Hardware

```bash
# CUDA 12.1 (NVIDIA GPU)
pip install torch>=2.0.0 --index-url https://download.pytorch.org/whl/cu121

# CPU only
pip install torch>=2.0.0 --index-url https://download.pytorch.org/whl/cpu

# Apple Silicon (MPS)
pip install torch>=2.0.0  # MPS support is built-in
```

### Step 4: Verify Installation

```python
import timesfm
import numpy as np
print(f"TimesFM version: {timesfm.__version__}")
print("Installation OK")
```

## 🎯 Quick Start

### Minimal Example (5 Lines)

```python
import torch, numpy as np, timesfm

torch.set_float32_matmul_precision("high")

model = timesfm.TimesFM_2p5_200M_torch.from_pretrained(
    "google/timesfm-2.5-200m-pytorch"
)
model.compile(timesfm.ForecastConfig(
    max_context=1024, max_horizon=256, normalize_inputs=True,
    use_continuous_quantile_head=True, force_flip_invariance=True,
    infer_is_positive=True, fix_quantile_crossing=True,
))

point, quantiles = model.forecast(horizon=24, inputs=[
    np.sin(np.linspace(0, 20, 200)),  # any 1-D array
])
# point.shape == (1, 24)        — median forecast
# quantiles.shape == (1, 24, 10) — 10th–90th percentile bands
```

### Forecast from CSV

```python
import pandas as pd, numpy as np

df = pd.read_csv("monthly_sales.csv", parse_dates=["date"], index_col="date")

# Convert each column to a list of arrays
inputs = [df[col].dropna().values.astype(np.float32) for col in df.columns]

point, quantiles = model.forecast(horizon=12, inputs=inputs)

# Build a results DataFrame
for i, col in enumerate(df.columns):
    last_date = df[col].dropna().index[-1]
    future_dates = pd.date_range(last_date, periods=13, freq="MS")[1:]
    forecast_df = pd.DataFrame({
        "date": future_dates,
        "forecast": point[i],
        "lower_80": quantiles[i, :, 1],  # q10 — lower bound of 80% PI
        "upper_80": quantiles[i, :, 9],  # q90 — upper bound of 80% PI
    })
    print(f"\n--- {col} ---")
    print(forecast_df.to_string(index=False))
```

### Forecast with Covariates (XReg)

TimesFM 2.5+ supports exogenous variables through `forecast_with_covariates()`. Requires `timesfm[xreg]`.

```python
# Requires: uv pip install timesfm[xreg]
point, quantiles = model.forecast_with_covariates(
    inputs=inputs,
    dynamic_numerical_covariates={"price": price_arrays},
    dynamic_categorical_covariates={"holiday": holiday_arrays},
    static_categorical_covariates={"region": region_labels},
    xreg_mode="xreg + timesfm",  # or "timesfm + xreg"
)
```

| Covariate Type | Description | Example |
| -------------- | ----------- | ------- |
| `dynamic_numerical` | Time-varying numeric | price, temperature, promotion spend |
| `dynamic_categorical` | Time-varying categorical | holiday flag, day of week |
| `static_numerical` | Per-series numeric | store size, account age |
| `static_categorical` | Per-series categorical | store type, region, product category |

**XReg Modes:**
- `"xreg + timesfm"` (default): TimesFM forecasts first, then XReg adjusts residuals
- `"timesfm + xreg"`: XReg fits first, then TimesFM forecasts residuals

> See `examples/covariates-forecasting/` for a complete example with synthetic retail data.

### Anomaly Detection (via Quantile Intervals)

TimesFM does not have built-in anomaly detection, but the **quantile forecasts naturally provide
prediction intervals** that can detect anomalies:

```python
point, q = model.forecast(horizon=H, inputs=[values])

# 80% prediction interval
lower_80 = q[0, :, 1]  # 10th percentile
upper_80 = q[0, :, 9]  # 90th percentile

# Detect anomalies: values outside the 80% CI
actual = test_values  # your holdout data
anomalies = (actual < lower_80) | (actual > upper_80)

# Severity levels
is_warning = (actual < q[0, :, 2]) | (actual > q[0, :, 8])  # outside 60% CI
is_critical = anomalies  # outside 80% CI
```

| Severity | Condition | Interpretation |
| -------- | --------- | -------------- |
| **Normal** | Inside 60% CI | Expected behavior |
| **Warning** | Outside 60% CI | Unusual but possible |
| **Critical** | Outside 80% CI | Statistically rare (< 20% probability) |

> See `examples/anomaly-detection/` for a complete example with visualization.

## 📊 Output, Config & Workflows

The output structure and full `ForecastConfig` reference are in
**[`references/output_and_config.md`](references/output_and_config.md)**.

> **Critical:** `quantile_forecast` has shape `(batch, horizon, 10)`. Index 0 is the **mean**;
> q10 = index 1, q50 (median) = index 5, q90 = index 9. The 80% PI is `q[:,:,1]`–`q[:,:,9]`.

Copy-paste workflows (single-series, batch, accuracy evaluation), GPU/memory performance
tuning, and integration with `statsmodels` / `matplotlib` / EDA are in
**[`references/workflows.md`](references/workflows.md)**.


## 📚 Scripts

- **`scripts/check_system.py`** — mandatory preflight checker; run before first model load. Reports RAM/GPU/disk/Python/install status and a recommended `per_core_batch_size`.
- **`scripts/forecast_csv.py`** — end-to-end CSV forecasting with automatic system check:
  ```bash
  python scripts/forecast_csv.py input.csv --horizon 24 \
      --date-col date --value-cols sales,revenue --output forecasts.csv
  ```

## 📖 Reference Documentation

Detailed guides in `references/`:

| File | Contents |
| ---- | -------- |
| [`references/output_and_config.md`](references/output_and_config.md) | Output shapes, quantile index map, full `ForecastConfig` parameter reference |
| [`references/workflows.md`](references/workflows.md) | Single/batch/eval workflows, GPU & memory tuning, statsmodels/matplotlib/EDA integration |
| [`references/pitfalls_and_validation.md`](references/pitfalls_and_validation.md) | Common pitfalls, quality checklist, known mistakes, regression-baseline validation |
| [`references/system_requirements.md`](references/system_requirements.md) | Hardware tiers, GPU/CPU selection, memory estimation formulas |
| [`references/api_reference.md`](references/api_reference.md) | Full `from_pretrained` options, API surface, output shapes |
| [`references/data_preparation.md`](references/data_preparation.md) | Input formats, NaN handling, CSV loading, covariate setup |

> **Before declaring any task done**, run the quality checklist and review the common
> pitfalls/mistakes in [`references/pitfalls_and_validation.md`](references/pitfalls_and_validation.md)
> — especially the quantile index off-by-one and `infer_is_positive` for negative series.

## Model Versions

```mermaid
timeline
    accTitle: TimesFM Version History
    accDescr: Timeline of TimesFM model releases showing parameter counts and key improvements.

    section 2024
        TimesFM 1.0 : 200M params, 2K context, JAX only
        TimesFM 2.0 : 500M params, 2K context, PyTorch + JAX
    section 2025
        TimesFM 2.5 : 200M params, 16K context, quantile head, no frequency indicator
```

| Version | Params | Context | Quantile Head | Frequency Flag | Status |
| ------- | ------ | ------- | ------------- | -------------- | ------ |
| **2.5** | 200M | 16,384 | ✅ Continuous (30M) | ❌ Removed | **Latest** |
| 2.0 | 500M | 2,048 | ✅ Fixed buckets | ✅ Required | Archived |
| 1.0 | 200M | 2,048 | ✅ Fixed buckets | ✅ Required | Archived |

**Hugging Face checkpoints:**

- `google/timesfm-2.5-200m-pytorch` (recommended)
- `google/timesfm-2.5-200m-flax`
- `google/timesfm-2.0-500m-pytorch` (archived)
- `google/timesfm-1.0-200m-pytorch` (archived)

## Resources

- **Paper**: [A Decoder-Only Foundation Model for Time-Series Forecasting](https://arxiv.org/abs/2310.10688) (ICML 2024)
- **Repository**: https://github.com/google-research/timesfm
- **Hugging Face**: https://huggingface.co/collections/google/timesfm-release-66e4be5fdb56e960c1e482a6
- **Google Blog**: https://research.google/blog/a-decoder-only-foundation-model-for-time-series-forecasting/
- **BigQuery Integration**: https://cloud.google.com/bigquery/docs/timesfm-model

## Examples

Three fully-working reference examples live in `examples/`. Use them as ground truth for correct API usage and expected output shape.

| Example | Directory | What It Demonstrates | When To Use It |
| ------- | --------- | -------------------- | -------------- |
| **Global Temperature Forecast** | `examples/global-temperature/` | Basic `model.forecast()` call, CSV -> PNG -> GIF pipeline, 36-month NOAA context | Starting point; copy-paste baseline for any univariate series |
| **Anomaly Detection** | `examples/anomaly-detection/` | Two-phase detection: linear detrend + Z-score on context, quantile PI on forecast; 2-panel viz | Any task requiring outlier detection on historical + forecasted data |
| **Covariates (XReg)** | `examples/covariates-forecasting/` | `forecast_with_covariates()` API (TimesFM 2.5), covariate decomposition, 2x2 shared-axis viz | Retail, energy, or any series with known exogenous drivers |

### Running the Examples

```bash
# Global temperature (no TimesFM 2.5 needed)
cd examples/global-temperature && python run_forecast.py && python visualize_forecast.py

# Anomaly detection (uses TimesFM 1.0)
cd examples/anomaly-detection && python detect_anomalies.py

# Covariates (API demo -- requires TimesFM 2.5 + timesfm[xreg] for real inference)
cd examples/covariates-forecasting && python demo_covariates.py
```

### Expected Outputs

| Example | Key output files | Acceptance criteria |
| ------- | ---------------- | ------------------- |
| global-temperature | `output/forecast_output.json`, `output/forecast_visualization.png` | `point_forecast` has 12 values; PNG shows context + forecast + PI bands |
| anomaly-detection | `output/anomaly_detection.json`, `output/anomaly_detection.png` | Sep 2023 flagged CRITICAL (z >= 3.0); >= 2 forecast CRITICAL from injected anomalies |
| covariates-forecasting | `output/sales_with_covariates.csv`, `output/covariates_data.png` | CSV has 108 rows (3 stores x 36 weeks); stores have **distinct** price arrays |

## Quality, Mistakes & Validation

Before declaring any task done, run the post-task **quality checklist**, review the
**known mistakes** (quantile off-by-one, covariate-horizon coverage, residual-based anomaly
detection, etc.), and run the **regression-baseline verification** snippets — all in
**[`references/pitfalls_and_validation.md`](references/pitfalls_and_validation.md)**.

