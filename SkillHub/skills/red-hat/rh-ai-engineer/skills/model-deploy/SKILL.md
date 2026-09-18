---
name: model-deploy
description: |
  Deploy AI/ML models on OpenShift AI using KServe with vLLM, NVIDIA NIM, or Caikit+TGIS runtimes.

  Use when:
  - "Deploy Llama 3 on my cluster"
  - "Set up a vLLM inference endpoint"
  - "Deploy a model with NIM"
  - "Create an InferenceService for Granite"
  - "I need to serve a model on OpenShift AI"

  Handles runtime selection, GPU validation, InferenceService CR creation, and rollout monitoring.

  NOT for NIM platform setup (use /nim-setup first).
  NOT for custom runtime creation (use /serving-runtime-config).
model: inherit
color: green
license: Apache-2.0
allowed-tools: resources_get resources_list resources_create_or_update pods_list pods_log events_list deploy_model list_inference_services get_inference_service get_model_endpoint list_serving_runtimes list_data_science_projects list_data_connections get_gpu_info get_deployment_info analyze_vllm
---

# /model-deploy Skill

Deploy AI/ML models on Red Hat OpenShift AI using KServe. Supports vLLM, NVIDIA NIM, and Caikit+TGIS serving runtimes. Handles runtime selection, hardware profile lookup (with live doc fallback), GPU pre-flight checks, InferenceService CR creation, rollout monitoring, and post-deployment validation.

## Prerequisites

**Required MCP Server**: `openshift` ([OpenShift MCP Server](https://github.com/openshift/openshift-mcp-server))

**Required MCP Tools** (from openshift):
- `resources_get` - Check NIM Account CR, LimitRange, GPU node taints, InferenceService status
- `resources_list` - Check Knative availability, GPU nodes, existing deployments, ServingRuntimes
- `resources_create_or_update` - Create/patch InferenceService, add tolerations (OpenShift fallback)
- `pods_list` - Check predictor pod status during rollout
- `pods_log` - Retrieve pod logs for debugging
- `events_list` - Check events for errors

**Preferred MCP Server**: `rhoai` ([RHOAI MCP Server](https://github.com/opendatahub-io/rhoai-mcp)) — used when available, automatic OpenShift fallback on failure

**Preferred MCP Tools** (from rhoai):
- `deploy_model` - Create InferenceService with high-level parameters (no YAML construction needed). **Known limitation**: does not support tolerations or NIM-specific env vars — see fallback patterns below.
- `list_inference_services` - List deployed models with structured status data
- `get_inference_service` - Get detailed model deployment status (conditions, endpoint, ready state)
- `get_model_endpoint` - Get inference endpoint URL directly
- `list_serving_runtimes` - List available runtimes including platform templates with supported model formats
- `list_data_science_projects` - Discover RHOAI projects for namespace validation
- `list_data_connections` - Verify model storage access (S3 data connections)

**Optional MCP Server**: `ai-observability` ([AI Observability MCP](https://github.com/rh-ai-quickstart/ai-observability-summarizer))

**Optional MCP Tools** (from ai-observability):
- `get_gpu_info` - Pre-flight GPU inventory check
- `get_deployment_info` - Post-deployment validation
- `analyze_vllm` - Verify metrics are flowing after deployment

**Common prerequisites** (KUBECONFIG, OpenShift+RHOAI cluster, KServe, verification protocol): See [skill-conventions.md](../references/skill-conventions.md).

**Fallback templates**: See [openshift-fallback-templates.md](../references/openshift-fallback-templates.md) for OpenShift YAML templates used when RHOAI tools are unavailable.

**Additional cluster requirements**:
- For NIM runtime: NIM platform set up via `/nim-setup`
- For vLLM/NIM: NVIDIA GPU nodes available in the cluster

## When to Use This Skill

**Use this skill when you need to:**
- Deploy an AI/ML model on OpenShift AI (KServe InferenceService)
- Set up vLLM, NIM, or Caikit+TGIS inference endpoints
- Look up hardware profiles and GPU requirements for a model
- Perform pre-flight validation before model deployment (GPU availability, namespace readiness, LimitRange conflicts)

**Do NOT use this skill when:**
- You need to set up the NIM platform first (use `/nim-setup`)
- You need to create or customize a ServingRuntime (use `/serving-runtime-config`)
- You need to troubleshoot a failed or slow deployment (use `/debug-inference`)
- You need to analyze model performance or GPU metrics (use `/ai-observability`)

## Workflow

### Step 1: Gather Target and Validate Environment

Collect the deployment target from the user, then immediately validate the environment before gathering remaining details.

**Ask the user for:**
- **Model name**: Which model to deploy (e.g., "Llama 3.1 8B", "Granite 3.1 8B")
- **Namespace**: Target namespace (must have model serving enabled)
- **Model source**: Where the model weights are stored (S3, OCI registry, PVC, NGC for NIM, or artifact URI from `/model-registry`)
- **Deployment mode**: Serverless (Knative, default) or RawDeployment

**Pre-flight Environment Validation**:

**CRITICAL**: Run these checks BEFORE gathering remaining deployment details to avoid wasted configuration effort.

Read [model-deploy-preflight-checklist.md](references/model-deploy-preflight-checklist.md) for the full pre-flight protocol. The checklist validates:
- Namespace is an RHOAI Data Science Project
- Model storage access (S3 data connections)
- Deployment mode support (Knative availability)
- Namespace resource constraints (LimitRange conflicts with KServe sidecars)
- GPU node taints (auto-generate tolerations)
- Existing deployments (reference configuration)
- Model source accessibility (OCI registry entitlements)

**If rhoai unavailable or returns error**: Use `resources_list` (from openshift) with `apiVersion: v1`, `kind: Namespace`, `labelSelector: opendatahub.io/dashboard=true` to find RHOAI projects.

**Present pre-flight results** in a summary table and note any adjustments made. **WAIT for user confirmation if significant changes were needed** (e.g., deployment mode switch, resource adjustments, tolerations added).

### Step 2: Gather Deployment Details

After the environment is validated, collect remaining deployment configuration. Use pre-flight findings to inform defaults (e.g., if Knative is unavailable, default to RawDeployment).

**Ask the user for:**
- **Runtime preference**: vLLM (default), NIM, or Caikit+TGIS (auto-detect if not specified)
- **Model source**: Where the model weights are stored (S3, OCI registry, PVC, or NGC for NIM)
- **Deployment mode**: Serverless (Knative, default) or RawDeployment

**Present configuration table for review:**

| Setting | Value | Source |
|---------|-------|--------|
| Model | [model-name] | user input (Step 1) |
| Runtime | [to be determined in Step 3] | auto-detect / user input |
| Namespace | [namespace] | user input (Step 1) |
| Model Source | [source-uri] | user input |
| Deployment Mode | [Serverless/RawDeployment] | user input / default (informed by pre-flight) |

**WAIT for user to confirm or modify these settings.**

### Step 3: Determine Runtime

**Document Consultation** (read before selecting runtime):
1. **Action**: Read [supported-runtimes.md](docs/references/supported-runtimes.md) using the Read tool to understand runtime capabilities and selection criteria
2. **Output to user**: "I consulted [supported-runtimes.md](docs/references/supported-runtimes.md) to understand runtime capabilities."

**Runtime Selection Logic:**

- User explicitly requested a runtime -> Use that runtime
- Model available in NGC NIM catalog -> Suggest NIM (with vLLM as fallback)
- Model is a standard open-source LLM (HuggingFace-compatible) -> Default to vLLM
- Model is in Caikit format -> Caikit+TGIS
- None of the above -> Suggest custom runtime via `/serving-runtime-config`

**Present recommendation** with rationale. **WAIT for user confirmation.**

### Step 4: Look Up Model Hardware Profile

**Document Consultation** (read before determining hardware requirements):
1. **Action**: Read [known-model-profiles.md](docs/references/known-model-profiles.md) using the Read tool to find hardware profile for the requested model
2. **Output to user**: "I consulted [known-model-profiles.md](docs/references/known-model-profiles.md) to find hardware requirements for [model-name]."

**If model IS in known-model-profiles.md:**
- Extract: GPU count, GPU type, VRAM, key vLLM args
- Present to user

**If model is NOT in known-model-profiles.md -> Trigger live doc lookup:**
1. **Action**: Read [live-doc-lookup.md](../references/live-doc-lookup.md) using the Read tool for the lookup protocol
2. **Output to user**: "Model [model-name] is not in my cached profiles. I'll look up its hardware requirements."
3. Use **WebFetch** tool to retrieve specs from:
   - For NIM models: `https://build.nvidia.com/models` or `https://docs.nvidia.com/nim/large-language-models/latest/supported-models.html`
   - For other models: `https://docs.redhat.com/en/documentation/red_hat_openshift_ai_cloud_service/1`
4. Extract: GPU requirements, model-specific args, known issues
5. **Output to user**: "I looked up [model-name] on [source] to confirm its hardware requirements: [summary]"

**Present hardware requirements** in a table (GPUs, VRAM, Key Args).

### Step 5: Pre-flight GPU Check (Optional)

**Condition**: Only if `ai-observability` MCP server is available.

**MCP Tool**: `get_gpu_info` (from ai-observability)

Compare available GPUs against model requirements from Step 4:
- If sufficient GPUs available -> Report match and proceed
- If insufficient -> Warn user with options: smaller model, quantized version, different cluster, or proceed at user's risk

**If ai-observability not available**: Skip with note: "GPU pre-flight check skipped (ai-observability MCP not configured)."

### Step 6: Verify NIM Platform (NIM Runtime Only)

**Condition**: Only when the selected runtime is NIM.

**MCP Tool**: `resources_get` (from openshift)

**Parameters**:
- `apiVersion`: `"nim.opendatahub.io/v1alpha1"` - REQUIRED
- `kind`: `"Account"` - REQUIRED
- `namespace`: target namespace - REQUIRED
- `name`: `"nim-account"` - REQUIRED

**If Account CR not found or not ready:**
Offer options: (1) Run `/nim-setup` now, (2) Switch to vLLM, (3) Abort. **WAIT for user decision.**

### Step 7: Select ServingRuntime and Prepare Deployment Parameters

**Verify available ServingRuntimes:**

**MCP Tool**: `list_serving_runtimes` (from rhoai)

**Parameters**:
- `namespace`: target namespace - REQUIRED
- `include_templates`: `true` - REQUIRED (shows both existing runtimes and platform templates)

The response shows existing runtimes and available templates with their supported model formats and `requires_instantiation` flag.

**If rhoai unavailable or returns error**: Use `resources_list` (from openshift) with `apiVersion: serving.kserve.io/v1alpha1`, `kind: ServingRuntime`, `namespace: [target]` to list namespace runtimes, and `kind: ClusterServingRuntime` for platform templates. Filter by label `opendatahub.io/dashboard=true`.

If the needed runtime shows `requires_instantiation: true`, it must first be instantiated via `/serving-runtime-config` or the rhoai `create_serving_runtime` tool.

Use the runtime list to select the correct `runtime` name for the deployment.

**Prepare deployment parameters** from Steps 1-4 and environment data from Step 1:

| Parameter | Value | Source |
|-----------|-------|--------|
| `name` | [model-deployment-name] | user input (DNS-compatible) |
| `namespace` | [namespace] | user input |
| `runtime` | [serving-runtime-name] | selected from `list_serving_runtimes` (Step 7) |
| `model_format` | [vLLM/pytorch/onnx/caikit/etc.] | runtime selection |
| `storage_uri` | [model-source-uri] | user input (prefer `hf://` for public models) |
| `gpu_count` | [gpu-count] | from hardware profile (Step 4) |
| `cpu_request` | [cpu] | from profile, adjusted for LimitRange |
| `memory_request` | [memory] | from profile, adjusted for LimitRange |
| `min_replicas` | [1] | default 1 (0 for scale-to-zero) |
| `max_replicas` | [1] | default 1 |

**Model sizing guide** for LLMs:
- 7B models: 1x 24GB GPU (e.g., A10G) or 1x 16GB GPU with quantization
- 13B models: 2x 24GB GPUs
- 70B models: 4+ 80GB GPUs (A100/H100) or quantized on fewer GPUs

**Scale-to-zero note**: Setting `min_replicas=0` saves resources but introduces cold start latency (30s-2min for model loading).

### Step 8: User Review and Confirmation

**Display the deployment parameters table** and a configuration summary to the user.

**Ask**: "Proceed with deploying this model? (yes/no/modify)"

**WAIT for explicit confirmation.**

- If **yes** -> Proceed to Step 9
- If **no** -> Abort
- If **modify** -> Ask what to change, update parameters, return to this step

### Step 9: Deploy Model

**MCP Tool**: `deploy_model` (from rhoai)

**Parameters**:
- `name`: deployment name (DNS-compatible) - REQUIRED
- `namespace`: target namespace - REQUIRED
- `runtime`: serving runtime name from Step 7 - REQUIRED
- `model_format`: model format string (e.g., `"vLLM"`, `"pytorch"`, `"onnx"`) - REQUIRED
- `storage_uri`: model location (e.g., `"hf://ibm-granite/granite-3.1-2b-instruct"`, `"s3://bucket/path"`, `"pvc://pvc-name/path"`) - REQUIRED
- `display_name`: human-readable display name - OPTIONAL
- `min_replicas`: minimum replicas (default: 1, 0 for scale-to-zero) - OPTIONAL
- `max_replicas`: maximum replicas (default: 1) - OPTIONAL
- `cpu_request`: CPU request per replica (default: `"1"`) - OPTIONAL
- `cpu_limit`: CPU limit per replica (default: `"2"`) - OPTIONAL
- `memory_request`: memory request per replica (default: `"4Gi"`) - OPTIONAL
- `memory_limit`: memory limit per replica (default: `"8Gi"`) - OPTIONAL
- `gpu_count`: number of GPUs per replica (default: 0) - OPTIONAL

**Note**: For NIM deployments, ensure the NGC API key secret is referenced. If `deploy_model` does not support NIM-specific env vars, fall back to `resources_create_or_update` (from openshift) with a NIM InferenceService YAML that includes `spec.predictor.env` referencing the `ngc-api-key` secretKeyRef.

#### GPU Toleration Handling

After `deploy_model` succeeds (or after creating InferenceService via OpenShift fallback), check if GPU tolerations are needed:

**MCP Tool**: `resources_list` (from openshift)
- `apiVersion`: `v1`, `kind`: `Node`, `labelSelector`: `nvidia.com/gpu.present=true`

If GPU nodes have taints (check `.spec.taints[]`), patch the InferenceService to add matching tolerations:

**MCP Tool**: `resources_create_or_update` (from openshift)

Add tolerations to `spec.predictor.tolerations` matching the discovered taints. Common GPU taints include:
- `nvidia.com/gpu` (Exists/NoSchedule)
- `ai-app=true` (Equal/NoSchedule)
- `ai-node=big` (Equal/NoSchedule)

After patching, delete the stuck Pending pod to force rescheduling with the new tolerations.

See [openshift-fallback-templates.md](../references/openshift-fallback-templates.md#toleration-post-deploy-patch) for the complete pattern.

#### NIM Deployment via OpenShift

When deploying with NIM runtime and `deploy_model` does not support NIM-specific env vars (NGC_API_KEY secretKeyRef, NIM_MAX_MODEL_LEN, image pull secrets):

Use `resources_create_or_update` (from openshift) with the NIM InferenceService template from [openshift-fallback-templates.md](../references/openshift-fallback-templates.md#inferenceservice-nim).

**Key NIM-specific fields:**
- `spec.predictor.containers[0].env` with NGC_API_KEY from secretKeyRef
- `spec.predictor.imagePullSecrets` referencing `ngc-image-pull-secret`
- Use a specific image tag (e.g., `1.8.3`) — the `latest` tag may have CUDA driver incompatibility
- Set `NIM_MAX_MODEL_LEN` to prevent KV cache OOM (use `16384` for T4 GPUs)

**Error Handling**:
- If namespace not found -> Report error, suggest creating namespace or using `/ds-project-setup`
- If ServingRuntime not found -> Report error, verify runtime name, suggest `/serving-runtime-config`
- If quota exceeded -> Report error, suggest reducing resource requests
- If RBAC error -> Report insufficient permissions

### Step 10: Monitor Rollout

Poll InferenceService status until ready or timeout (10 minutes).

**MCP Tool**: `get_inference_service` (from rhoai)
- `name`: deployment name, `namespace`: target namespace, `verbosity`: `"full"`

**If rhoai unavailable or returns error**: Use `resources_get` (from openshift) with `apiVersion: serving.kserve.io/v1beta1`, `kind: InferenceService`, `name: [model-name]`, `namespace: [namespace]`. Check `.status.conditions` for `Ready=True`.

Check the Ready condition and status. Repeat every 15-30 seconds until Ready=True or timeout.

**Check predictor pod status:**

**MCP Tool**: `pods_list` (from openshift)
- `namespace`: target namespace, `labelSelector`: `"serving.kserve.io/inferenceservice=[model-name]"`

Show deployment progress tracking: Pod Scheduled, Image Pulled, Container Started, Model Loaded, Ready. Include pod name, status, and restart count.

**On failure:** Check pod logs (`pods_log`) and events (`events_list`) for diagnostics. Present options: (1) View full pod logs, (2) Check namespace events, (3) Invoke `/debug-inference`, (4) Delete and retry, (5) Continue waiting. **WAIT for user decision. NEVER auto-delete failed deployments.**

### Step 11: Deployment Complete

**Get endpoint URL:**

**MCP Tool**: `get_model_endpoint` (from rhoai)
- `name`: deployment name, `namespace`: target namespace

**If rhoai unavailable or returns error**: Extract endpoint from `resources_get` (from openshift) on the InferenceService — the URL is in `.status.url`.

**Report success** showing: model name, runtime, namespace, GPUs, inference endpoint URL, API type (OpenAI-compatible REST), and next steps (`/ai-observability`, `/model-monitor`, `/guardrails-config`).

**Provide test commands** based on runtime:
- **vLLM (OpenAI-compatible)**: `curl -X POST [endpoint]/v1/completions -H "Content-Type: application/json" -d '{"model":"[model-name]","prompt":"Hello","max_tokens":100}'`
- **KServe v2**: `curl -X POST [endpoint]/v2/models/[model-name]/infer -H "Content-Type: application/json" -d '{"inputs":[...]}'`

**Post-deployment validation** (if ai-observability MCP available):
- `get_deployment_info` to confirm model appears in monitoring
- `analyze_vllm` with a short time range to verify initial metrics are flowing
- Report findings to user

## Common Issues

For common issues (GPU scheduling, OOMKilled, image pull errors, RBAC), see [common-issues.md](../references/common-issues.md).

### Issue 1: InferenceService Stuck in "Unknown"

**Error**: InferenceService `status.conditions` shows "Unknown" state

**Cause**: ServingRuntime not found in the namespace, or model serving platform not enabled.

**Solution:**
1. Verify ServingRuntime exists: `resources_list` for `servingruntimes` in namespace
2. Ensure model serving is enabled: namespace has label `opendatahub.io/dashboard: "true"`
3. Check the runtime name in the InferenceService matches an available ServingRuntime
4. If no matching runtime, use `/serving-runtime-config` to create one

### Issue 2: Model Download Timeout

**Error**: Pod starts but times out while downloading model weights from S3 or OCI registry

**Cause**: Large model size combined with slow network connection to storage.

**Solution:**
1. Add `serving.knative.dev/progress-deadline` annotation with a longer timeout (e.g., `"1800s"`)
2. Verify S3/storage credentials are valid
3. Consider using a PVC with pre-downloaded model weights instead
4. Check network connectivity between the pod and storage endpoint

### Issue 3: LimitRange Conflicts with KServe Sidecars

**Error**: Pod rejected with `minimum cpu usage per Container is 50m, but request is 10m` or `minimum memory usage per Container is 64Mi, but request is 15Mi`

**Cause**: The namespace has a LimitRange with minimum resource constraints that exceed the hardcoded resource requests of KServe-injected sidecar containers (oauth-proxy, queue-proxy, or modelcar containers request 10m CPU / 15Mi memory). These sidecar resource values cannot be controlled through the InferenceService spec.

**Solution:**
1. Check LimitRange: `resources_list` for `LimitRange` in the namespace
2. If LimitRange minimum CPU > 10m or minimum memory > 15Mi, the LimitRange must be adjusted
3. Options: (a) Lower LimitRange minimums to accommodate sidecars (min CPU ≤ 10m, min memory ≤ 15Mi), (b) Remove the LimitRange entirely, (c) Deploy in a different namespace without restrictive LimitRanges
4. **Prevention**: Step 1 pre-flight validation now checks for this conflict before deployment

### Issue 4: GPU Node Taints Prevent Scheduling

**Error**: Pod stuck in Pending with events showing `node(s) had untolerated taint {ai-app: true}` or similar custom taint messages, while also showing `Insufficient nvidia.com/gpu` on remaining nodes

**Cause**: GPU nodes are tainted with custom taints (e.g., `ai-app=true:NoSchedule`) to reserve them for AI workloads. The InferenceService predictor pod does not have matching tolerations, so it cannot be scheduled on GPU nodes.

**Solution:**
1. Identify GPU node taints: `resources_get` for GPU nodes, check `.spec.taints`
2. Add matching tolerations to the InferenceService predictor spec:
   ```yaml
   spec:
     predictor:
       tolerations:
         - key: "ai-app"
           operator: "Equal"
           value: "true"
           effect: "NoSchedule"
   ```
3. **Prevention**: Step 1 pre-flight validation now auto-discovers GPU node taints and generates tolerations

### Issue: Pod Stuck Pending Due to GPU Node Taints

**Error**: Pod shows "0/N nodes are available: node(s) had untolerated taint" in events

**Cause**: `deploy_model` does not support tolerations. GPU nodes in production clusters are almost always tainted.

**Solution**: Patch InferenceService with tolerations matching the GPU node taints, then delete the stuck pod. See [common-issues.md](../references/common-issues.md#deploy-model-missing-gpu-tolerations) for details.

### Issue: NIM CUDA Driver Incompatibility

**Error**: NIM container crashes with error code 803 or CUDA-related errors

**Cause**: The `latest` NIM image tag may bundle a CUDA version incompatible with the GPU node's driver.

**Solution**: Pin NIM image to a specific tag compatible with the cluster's GPU driver version (e.g., `1.8.3` for T4 nodes with older drivers). Check the NVIDIA NIM release notes for driver compatibility.

### Issue: Stale ReplicaSets After InferenceService Patch

**Error**: Multiple ReplicaSets exist after patching the InferenceService (e.g., adding tolerations), causing duplicate Pending pods

**Cause**: Each InferenceService spec change triggers a new ReplicaSet. Old ReplicaSets are not automatically cleaned up.

**Solution**: Scale down stale ReplicaSets to 0 replicas via `resources_create_or_update` (from openshift), or delete them. Identify the current ReplicaSet by checking which one has the latest creation timestamp.

## Dependencies

### MCP Tools
See [Prerequisites](#prerequisites) for the complete list of required and optional MCP tools.

### Related Skills
- `/nim-setup` - Prerequisite for NIM runtime deployments
- `/debug-inference` - Troubleshoot InferenceService failures
- `/ai-observability` - Analyze deployed model performance
- `/serving-runtime-config` - Create custom ServingRuntime CRs
- `/ds-project-setup` - Create a namespace with model serving enabled
- `/model-registry` - Get artifact URIs for registered model versions to deploy
- `/model-monitor` - Configure bias and drift monitoring after deployment
- `/guardrails-config` - Add content safety guardrails to LLM deployments

### Reference Documentation
- [known-model-profiles.md](docs/references/known-model-profiles.md) - Hardware profiles for common models
- [supported-runtimes.md](docs/references/supported-runtimes.md) - Runtime capabilities and selection criteria
- [live-doc-lookup.md](../references/live-doc-lookup.md) - Protocol for fetching specs for unknown models

## Critical: Human-in-the-Loop Requirements

See [skill-conventions.md](../references/skill-conventions.md) for general HITL and security conventions.

**Skill-specific checkpoints:**
- After pre-flight validation (Step 1): confirm if significant adjustments were needed (deployment mode, tolerations, resource changes)
- After gathering deployment details (Step 2): confirm configuration table
- After runtime selection (Step 3): confirm runtime choice
- User review before deploy_model (Step 8): confirm deployment parameters
- On deployment failure (Step 10): present diagnostic options, wait for user decision
- **NEVER** auto-delete failed deployments or auto-select runtimes without confirmation

## Example Usage

See [model-deploy examples](docs/examples/model-deploy.md) for complete deployment walkthroughs (vLLM and NIM).
