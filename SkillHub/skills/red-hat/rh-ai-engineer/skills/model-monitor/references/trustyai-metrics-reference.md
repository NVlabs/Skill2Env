# TrustyAI Metrics Reference

Authoritative source for TrustyAIService CRD fields, Prometheus metric names, and domain-specific thresholds.

## TrustyAIService CRD

```yaml
apiVersion: trustyai.opendatahub.io/v1alpha1
kind: TrustyAIService
metadata:
  name: trustyai-service
  namespace: <namespace>
spec:
  storage:
    format: PVC          # PVC or DATABASE
    folder: /data
    size: 1Gi
  data:
    filename: data.csv
    format: CSV
  metrics:
    schedule: 5s         # metric computation interval
  replicas: 1
```

## Cluster Enablement

- **DSC path**: `spec.components.trustyai.managementState: Managed` on the `DataScienceCluster` CR
- **CRD name**: `trustyaiservices.trustyai.opendatahub.io`
- **User Workload Monitoring**: must be enabled in `openshift-monitoring/cluster-monitoring-config` ConfigMap (`enableUserWorkload: true`) for Prometheus to scrape TrustyAI metrics

## Pod Selectors

- TrustyAI service pods: `app.kubernetes.io/name=trustyai-service`
- Metrics endpoint: `/q/metrics` (Quarkus-style)

## Prometheus Metric Names and Labels

### Bias Metrics

| Metric | Labels | Description |
|--------|--------|-------------|
| `trustyai_spd` | `model`, `protected`, `outcome`, `privileged`, `unprivileged` | Statistical Parity Difference |
| `trustyai_dir` | `model`, `protected`, `outcome`, `privileged`, `unprivileged` | Disparate Impact Ratio |

### Drift Metrics

| Metric | Labels | Description |
|--------|--------|-------------|
| `trustyai_meanshift` | `model`, `feature` | Mean shift detection |
| `trustyai_fouriermmd` | `model`, `feature` | Fourier MMD distribution comparison |
| `trustyai_kstest` | `model`, `feature` | Kolmogorov-Smirnov statistic (D) |
| `trustyai_jensenshannon` | `model`, `feature` | Jensen-Shannon divergence |

## Recommended Thresholds

| Metric | Fair Value | Default Threshold | Alert When |
|--------|-----------|-------------------|------------|
| SPD | 0 | ±0.1 | \|SPD\| > 0.1 |
| DIR | 1.0 | 0.8–1.2 | DIR < 0.8 or DIR > 1.2 |
| MeanShift | 0 | 0.1 | value > 0.1 |
| FourierMMD | 0 | 0.05 | value > 0.05 |
| KS-Test (D) | 0 | 0.1 | value > 0.1 |
| Jensen-Shannon | 0 | 0.1 | value > 0.1 |

## Bias Metric ConfigMap Schema

ConfigMap name pattern: `trustyai-bias-config-[isvc-name]`

Labels: `app.kubernetes.io/part-of: trustyai`, `trustyai.opendatahub.io/target-model: [isvc-name]`

Each metric stored as a JSON entry (`spd-config.json`, `dir-config.json`):

| Field | Type | Description |
|-------|------|-------------|
| `modelId` | string | InferenceService name |
| `protectedAttribute` | string | Feature name to check for fairness |
| `favorableOutcome` | any | Model output value considered "positive" |
| `outcomeName` | string | Name of the outcome field |
| `privilegedAttribute` | any | Protected attribute value for privileged group |
| `unprivilegedAttribute` | any | Protected attribute value for unprivileged group |
| `metricName` | string | `"SPD"` or `"DIR"` |
| `thresholdDelta` | float | SPD only: alert when \|SPD\| exceeds this (default: 0.1) |
| `thresholdLower` | float | DIR only: alert when DIR below this (default: 0.8) |
| `thresholdUpper` | float | DIR only: alert when DIR above this (default: 1.2) |

## Drift Metric ConfigMap Schema

ConfigMap name pattern: `trustyai-drift-config-[isvc-name]`

Labels: same as bias ConfigMap

Single JSON entry (`drift-config.json`):

| Field | Type | Description |
|-------|------|-------------|
| `modelId` | string | InferenceService name |
| `metrics` | string[] | Subset of: `MEANSHIFT`, `FOURIERMMD`, `KSTEST`, `JENSENSHANNON` |
| `referenceTag` | string | Tag for baseline data (default: `"TRAINING"`) |
| `thresholds` | object | Map of metric name to threshold value (see Recommended Thresholds) |

## Minimum Data Requirements

- TrustyAI requires **~100 inference requests** with the protected attribute for stable bias metric computation
- Drift metrics require a **reference dataset** (training data baseline) tagged with `TRAINING` in TrustyAI storage
- Metrics will return NaN or "insufficient data" until the minimum sample size is reached
