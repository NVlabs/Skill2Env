---
name: model-monitor
description: |
  Configure TrustyAI model monitoring for bias detection and data drift on deployed InferenceServices.

  Use when:
  - "Monitor my model for bias"
  - "Set up drift detection on my inference endpoint"
  - "Configure TrustyAI for my deployed model"
  - "Check if my model has fairness issues"
  - "I need SPD / DIR metrics for my model"

  Handles TrustyAIService deployment, bias metric configuration (SPD, DIR), drift metric configuration (MeanShift, FourierMMD, KS-Test, Jensen-Shannon), threshold tuning, and monitoring validation.

  NOT for deploying models (use /model-deploy first).
  NOT for input/output content safety guardrails (use /guardrails-config).
  NOT for infrastructure-level observability (use /ai-observability).
model: inherit
color: blue
license: Apache-2.0
allowed-tools: resources_get resources_list resources_create_or_update pods_list pods_log events_list list_inference_services get_inference_service list_data_science_projects execute_promql
---

# /model-monitor Skill

## Prerequisites

**Required MCP Server**: `openshift` ([OpenShift MCP Server](https://github.com/openshift/openshift-mcp-server))

**Required MCP Tools** (from openshift):
- `resources_get` (from openshift) - Get TrustyAIService CR status, check CRD availability
- `resources_list` (from openshift) - List TrustyAIService instances, check CRD existence
- `resources_create_or_update` (from openshift) - Create/update TrustyAIService CR, metric configuration ConfigMaps
- `pods_list` (from openshift) - Verify TrustyAI pods are running
- `pods_log` (from openshift) - Retrieve TrustyAI pod logs for troubleshooting
- `events_list` (from openshift) - Check events for TrustyAI deployment issues
- `prometheus_query` (from openshift) - Query TrustyAI metrics (trustyai_spd, trustyai_dir, drift metrics)

**Preferred MCP Server**: `rhoai` ([RHOAI MCP Server](https://github.com/opendatahub-io/rhoai-mcp)) — used when available, automatic OpenShift fallback on failure

**Preferred MCP Tools** (from rhoai):
- `list_inference_services` - List deployed models to identify monitoring targets
- `get_inference_service` - Get InferenceService details (model format, runtime, status)
- `list_data_science_projects` - Validate namespace is an RHOAI Data Science Project

**Optional MCP Server**: `ai-observability` ([AI Observability MCP](https://github.com/rh-ai-quickstart/ai-observability-summarizer))

**Optional MCP Tools** (from ai-observability):
- `execute_promql` - Custom PromQL queries for TrustyAI metrics validation

**Common prerequisites** (KUBECONFIG, OpenShift+RHOAI cluster, KServe, verification protocol): See [skill-conventions.md](../references/skill-conventions.md).

**Fallback templates**: See [openshift-fallback-templates.md](../references/openshift-fallback-templates.md) for OpenShift YAML templates used when RHOAI tools are unavailable.

**Additional cluster requirements**:
- TrustyAI operator enabled in the DataScienceCluster CR
- At least one deployed InferenceService to monitor (via `/model-deploy`)
- User Workload Monitoring enabled in OpenShift (for TrustyAI metrics scraping)

## When to Use This Skill

**Use this skill when you need to:**
- Set up bias monitoring (SPD, DIR) for a deployed model
- Configure data drift detection on inference data streams
- Deploy a TrustyAIService instance in a namespace
- Check whether monitoring is active and metrics are flowing

**Do NOT use this skill when:**
- You need to deploy a model first (use `/model-deploy`)
- You need LLM input/output content safety guardrails (use `/guardrails-config`)
- You want infrastructure-level performance metrics (use `/ai-observability`)
- You need to troubleshoot a failed model deployment (use `/debug-inference`)

## Workflow

### Step 1: Verify TrustyAI Operator Installation

**MCP Tool**: `resources_list` (from openshift)

**Parameters**:
- `apiVersion`: `"apiextensions.k8s.io/v1"` - REQUIRED
- `kind`: `"CustomResourceDefinition"` - REQUIRED

Check for the presence of `trustyaiservices.trustyai.opendatahub.io` CRD. This is a hard prerequisite — nothing in this skill works without it.

**Error Handling**:
- If CRD not found: Report that TrustyAI must be enabled in the DataScienceCluster CR with `spec.components.trustyai.managementState: Managed`. Offer options: (1) Show enablement instructions, (2) Abort. **WAIT for user decision.**

### Step 2: Gather Monitoring Requirements

**Ask the user for:**
- **Target model**: Which InferenceService to monitor (name or "list all")
- **Namespace**: Target namespace
- **Monitoring type**: Bias detection, drift detection, or both
- **For bias monitoring**: protected attribute, favorable outcome, privileged/unprivileged group values
- **For drift monitoring**: which drift metrics to enable (default: all)

If user is unsure about target model, use `list_inference_services` (from rhoai) to present available models.

**MCP Tool**: `list_inference_services` (from rhoai)

**Parameters**:
- `namespace`: user-specified namespace - REQUIRED
- `verbosity`: `"standard"` - OPTIONAL

**If rhoai unavailable or returns error**: Use `resources_list` (from openshift) with `apiVersion: serving.kserve.io/v1beta1`, `kind: InferenceService`, `namespace: [namespace]`.

To validate namespace is a Data Science Project when `list_data_science_projects` (from rhoai) is unavailable: Use `resources_list` (from openshift) with `apiVersion: v1`, `kind: Namespace`, `labelSelector: opendatahub.io/dashboard=true`.

To get InferenceService details when `get_inference_service` (from rhoai) is unavailable: Use `resources_get` (from openshift) with `apiVersion: serving.kserve.io/v1beta1`, `kind: InferenceService`, `name: [name]`, `namespace: [namespace]`. Extract status from `.status.conditions`.

**Important**: TrustyAI payload logging requires **Knative/Serverless** deployment mode. In RawDeployment mode, inference data does not reach TrustyAI for bias/drift analysis. If the InferenceService uses `serving.kserve.io/deploymentMode: RawDeployment`, warn the user that payload logging will not work and suggest switching to Serverless mode if Knative is available.

Present configuration summary for confirmation. **WAIT for user to confirm or modify.**

### Step 3: Check/Create TrustyAIService in Namespace

**Document Consultation** (read before configuring TrustyAI):
1. **Action**: Read [trustyai-metrics-reference.md](references/trustyai-metrics-reference.md) using the Read tool to understand CRD spec fields, metric names, and thresholds
2. **Output to user**: "I consulted [trustyai-metrics-reference.md](references/trustyai-metrics-reference.md) to understand TrustyAI CRD specifications."

**MCP Tool**: `resources_get` (from openshift)

**Parameters**:
- `apiVersion`: `"trustyai.opendatahub.io/v1alpha1"` - REQUIRED
- `kind`: `"TrustyAIService"` - REQUIRED
- `namespace`: target namespace - REQUIRED
- `name`: `"trustyai-service"` - REQUIRED

**If TrustyAIService exists and is Ready:** Proceed to Step 5.

**If TrustyAIService exists but NOT Ready:** Check pod status (Step 4). **WAIT for user decision.**

**If TrustyAIService does NOT exist:** Construct TrustyAIService manifest using the CRD spec from [trustyai-metrics-reference.md](references/trustyai-metrics-reference.md). Key values: name=`trustyai-service`, storage PVC 1Gi, CSV format, 5s schedule.

Display the manifest to the user. Ask: "Proceed with creating this TrustyAIService? (yes/no/modify)"

**WAIT for explicit confirmation.**

**MCP Tool**: `resources_create_or_update` (from openshift)

**Parameters**:
- `manifest`: the TrustyAIService YAML manifest as JSON string - REQUIRED

**Error Handling**:
- If RBAC error -> Report insufficient permissions
- If quota error -> Report resource quota exceeded

### Step 4: Verify TrustyAI Pods Are Running

**MCP Tool**: `pods_list` (from openshift)

**Parameters**:
- `namespace`: target namespace - REQUIRED
- `labelSelector`: `"app.kubernetes.io/name=trustyai-service"` - REQUIRED

Verify at least one TrustyAI pod is in Running state. Report pod status.

**If pods not ready** (Pending, CrashLoopBackOff, etc.):

Use `pods_log` and `events_list` (from openshift) to diagnose. Present findings and options: (1) View full logs, (2) Check events, (3) Delete and recreate TrustyAIService, (4) Abort. **WAIT for user decision. NEVER auto-delete TrustyAIService.**

### Step 5: Configure Bias Metrics

**Condition**: Only when monitoring type includes bias detection.

Create ConfigMap `trustyai-bias-config-[isvc-name]` with SPD and DIR configurations using the field schema from [trustyai-metrics-reference.md](references/trustyai-metrics-reference.md). Populate `modelId`, `protectedAttribute`, `favorableOutcome`, `outcomeName`, `privilegedAttribute`, `unprivilegedAttribute` with user-provided values from Step 1. Use default thresholds (SPD ±0.1, DIR 0.8–1.2) unless user specifies otherwise.

**MCP Tool**: `resources_create_or_update` (from openshift)

**Parameters**:
- `manifest`: ConfigMap YAML manifest as JSON string - REQUIRED

Display manifest to user with threshold explanation. **Ask**: "Proceed with these bias metric configurations? (yes/no/modify)"

**WAIT for explicit confirmation.**

### Step 6: Configure Drift Metrics

**Condition**: Only when monitoring type includes drift detection.

Create ConfigMap `trustyai-drift-config-[isvc-name]` using the drift schema from [trustyai-metrics-reference.md](references/trustyai-metrics-reference.md). Include selected metrics (default: MEANSHIFT, FOURIERMMD, KSTEST, JENSENSHANNON) with recommended thresholds from the reference doc.

**MCP Tool**: `resources_create_or_update` (from openshift)

**Parameters**:
- `manifest`: ConfigMap YAML manifest as JSON string - REQUIRED

Display manifest to user. **Ask**: "Proceed with these drift metric configurations? (yes/no/modify)"

**WAIT for explicit confirmation.**

### Step 7: Validate Monitoring Is Active

Wait 30-60 seconds after configuration, then verify metrics are being produced.

**MCP Tool**: `prometheus_query` (from openshift) or `execute_promql` (from ai-observability)

**Parameters**:
- `query`: `"trustyai_spd{model=\"[isvc-name]\"}"` - REQUIRED (for bias)
- `query`: `"trustyai_meanshift{model=\"[isvc-name]\"}"` - REQUIRED (for drift)

**If metrics are present**: Report current values and confirm monitoring is active.

**If metrics are NOT present**: Expected if no inference requests have been made yet. Inform user that ~100 requests are needed for stable bias metrics per [trustyai-metrics-reference.md](references/trustyai-metrics-reference.md).

### Step 8: Summary and Next Steps

Present summary showing: TrustyAI status, configured metrics with thresholds, PromQL queries for dashboards (from [trustyai-metrics-reference.md](references/trustyai-metrics-reference.md)), and next steps (`/ai-observability`, `/guardrails-config`).

## Common Issues

For common issues (GPU scheduling, OOMKilled, image pull errors, RBAC), see [common-issues.md](../references/common-issues.md).

### Issue 1: TrustyAI Pod CrashLoopBackOff

**Error**: TrustyAI pod restarts repeatedly with storage-related errors

**Cause**: PVC for TrustyAI data storage cannot be provisioned, or the storage class is unavailable.

**Solution:**
1. Check PVC status: `resources_list` for PVCs in namespace with TrustyAI labels
2. Verify a default StorageClass exists: `resources_list` for StorageClass
3. If no default StorageClass, specify one in the TrustyAIService CR `spec.storage.storageClass`
4. Check pod logs for specific storage errors

### Issue 2: No Metrics Appearing in Prometheus

**Error**: PromQL queries return empty results even after inference requests

**Cause**: User Workload Monitoring is not enabled, or the TrustyAI ServiceMonitor is missing.

**Solution:**
1. Verify User Workload Monitoring is enabled: check `cluster-monitoring-config` ConfigMap in `openshift-monitoring` namespace for `enableUserWorkload: true`
2. Check that a ServiceMonitor exists for TrustyAI: `resources_list` for ServiceMonitor in the namespace
3. Verify TrustyAI pods expose the `/q/metrics` endpoint

### Issue 3: Bias Metrics Show Insufficient Data

**Error**: SPD/DIR metrics return NaN or insufficient data warnings

**Cause**: Not enough inference requests with the protected attribute. TrustyAI requires ~100 requests for stable metrics.

**Solution:**
1. Send more inference requests with varied protected attribute values
2. Ensure the inference payload includes the protected attribute field
3. Verify the `protectedAttribute` field name matches the model's input schema exactly

## Dependencies

### MCP Tools
See [Prerequisites](#prerequisites) for the complete list of required and optional MCP tools.

### Related Skills
- `/model-deploy` - Deploy the InferenceService before configuring monitoring
- `/debug-inference` - Troubleshoot issues found by monitoring alerts
- `/ai-observability` - Infrastructure-level performance metrics (complements TrustyAI fairness metrics)
- `/guardrails-config` - Add content safety guardrails to the monitored model

### Reference Documentation
- [trustyai-metrics-reference.md](references/trustyai-metrics-reference.md) - TrustyAI CRD specs, Prometheus metric names, ConfigMap schemas, and threshold guidance

## Critical: Human-in-the-Loop Requirements

See [skill-conventions.md](../references/skill-conventions.md) for general HITL and security conventions.

**Skill-specific checkpoints:**
- After gathering requirements (Step 2): confirm monitoring configuration
- Before creating TrustyAIService (Step 3): display manifest, confirm creation
- On TrustyAI pod failure (Step 4): present diagnostic options, wait for user decision
- Before configuring bias metrics (Step 5): confirm metric parameters and thresholds
- Before configuring drift metrics (Step 6): confirm metric parameters and thresholds
- **NEVER** auto-delete TrustyAIService or metric configurations
- **NEVER** modify fairness thresholds without explicit user confirmation
