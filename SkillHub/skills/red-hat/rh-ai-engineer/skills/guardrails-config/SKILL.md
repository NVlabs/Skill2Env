---
name: guardrails-config
description: |
  Configure TrustyAI Guardrails Orchestrator for LLM input/output content safety on OpenShift AI.

  Use when:
  - "Add guardrails to my LLM endpoint"
  - "Set up content safety for my model"
  - "Configure PII detection on my inference endpoint"
  - "Block prompt injection attacks"
  - "I need a guarded endpoint for my deployed model"

  Handles GuardrailsOrchestrator CR deployment, detector configuration (content safety, PII, prompt injection, toxicity), orchestration policies, and guarded endpoint validation.

  NOT for deploying models (use /model-deploy first).
  NOT for bias/drift monitoring (use /model-monitor).
  NOT for infrastructure observability (use /ai-observability).
model: inherit
color: blue
license: Apache-2.0
allowed-tools: resources_get resources_list resources_create_or_update resources_delete pods_list pods_log events_list list_inference_services get_inference_service get_model_endpoint test_model_endpoint deploy_model list_serving_runtimes recommend_serving_runtime execute_promql analyze_vllm
---

# /guardrails-config Skill

## Prerequisites

**Required MCP Server**: `openshift` ([OpenShift MCP Server](https://github.com/openshift/openshift-mcp-server))

**Required MCP Tools** (from openshift):
- `resources_get` (from openshift) - Get GuardrailsOrchestrator CR status, ConfigMaps
- `resources_list` (from openshift) - Check GuardrailsOrchestrator CRD availability
- `resources_create_or_update` (from openshift) - Create/update GuardrailsOrchestrator CR, detector ConfigMaps
- `resources_delete` (from openshift) - Remove detector configurations (with user confirmation)
- `pods_list` (from openshift) - Verify orchestrator and detector pods are running
- `pods_log` (from openshift) - Retrieve orchestrator pod logs for troubleshooting
- `events_list` (from openshift) - Check events for deployment issues

**Preferred MCP Server**: `rhoai` ([RHOAI MCP Server](https://github.com/opendatahub-io/rhoai-mcp)) — used when available, automatic OpenShift fallback on failure

**Preferred MCP Tools** (from rhoai):
- `list_inference_services` - List deployed models to identify guardrail targets
- `get_inference_service` - Get InferenceService details (endpoint, runtime, status)
- `get_model_endpoint` - Get the model endpoint URL for orchestrator routing
- `test_model_endpoint` - Test guarded endpoint after configuration
- `deploy_model` - Deploy detector models (HuggingFace classifiers used as detectors)
- `list_serving_runtimes` - List runtimes for detector model deployment
- `recommend_serving_runtime` - Recommend runtime for detector models

**Optional MCP Server**: `ai-observability` ([AI Observability MCP](https://github.com/rh-ai-quickstart/ai-observability-summarizer))

**Optional MCP Tools** (from ai-observability):
- `execute_promql` - Query guardrails metrics (request counts, block rates)
- `analyze_vllm` - Verify guarded endpoint performance impact

**Common prerequisites** (KUBECONFIG, OpenShift+RHOAI cluster, KServe, verification protocol): See [skill-conventions.md](../references/skill-conventions.md).

**Fallback templates**: See [openshift-fallback-templates.md](../references/openshift-fallback-templates.md) for OpenShift YAML templates used when RHOAI tools are unavailable.

**Additional cluster requirements**:
- TrustyAI operator installed with guardrails support (RHOAI 2.14+)
- At least one deployed LLM InferenceService to guard (via `/model-deploy`)
- For HuggingFace detector models: GPU or CPU resources for detector inference pods

## When to Use This Skill

**Use this skill when you need to:**
- Add content safety guardrails to an LLM inference endpoint
- Configure PII detection on model inputs or outputs
- Set up prompt injection detection for a deployed LLM
- Deploy a guarded endpoint that proxies to an existing model with safety checks
- Set orchestration policies (block, warn, or passthrough)

**Do NOT use this skill when:**
- You need to deploy the underlying model first (use `/model-deploy`)
- You need bias/fairness monitoring or drift detection (use `/model-monitor`)
- You want infrastructure-level performance metrics (use `/ai-observability`)
- You need to troubleshoot a failed model deployment (use `/debug-inference`)

## Workflow

### Step 1: Verify GuardrailsOrchestrator CRD

**MCP Tool**: `resources_list` (from openshift)

**Parameters**:
- `apiVersion`: `"apiextensions.k8s.io/v1"` - REQUIRED
- `kind`: `"CustomResourceDefinition"` - REQUIRED

Check for `guardrailsorchestrators.trustyai.opendatahub.io` CRD. This is a hard prerequisite — nothing in this skill works without it.

**Error Handling**:
- If CRD not found: Report that GuardrailsOrchestrator requires RHOAI 2.14+ with TrustyAI enabled (`spec.components.trustyai.managementState: Managed`). Offer options: (1) Show enablement instructions, (2) Abort. **WAIT for user decision.**

### Step 2: Gather Guardrails Requirements

**Ask the user for:**
- **Target model**: Which InferenceService to guard (name or "list all")
- **Namespace**: Target namespace
- **Detector types needed**: content safety, PII detection, prompt injection, toxicity, hallucination, custom regex
- **Detection scope**: Input only, output only, or both (default: both)
- **Policy**: Block, warn, or passthrough

If user is unsure about target model, use `list_inference_services` (from rhoai) to present available models.

**MCP Tool**: `list_inference_services` (from rhoai)

**Parameters**:
- `namespace`: user-specified namespace - REQUIRED
- `verbosity`: `"standard"` - OPTIONAL

**If rhoai unavailable or returns error**: Use `resources_list` (from openshift) with `apiVersion: serving.kserve.io/v1beta1`, `kind: InferenceService`, `namespace: [namespace]`.

Verify the selected InferenceService is Ready:

**MCP Tool**: `get_inference_service` (from rhoai)

**Parameters**:
- `name`: selected InferenceService name - REQUIRED
- `namespace`: target namespace - REQUIRED
- `verbosity`: `"full"` - REQUIRED

**If rhoai unavailable or returns error**: Use `resources_get` (from openshift) with `apiVersion: serving.kserve.io/v1beta1`, `kind: InferenceService`, `name: [name]`, `namespace: [namespace]`. Extract status from `.status.conditions`.

**If not Ready**: Warn user and offer options: (1) Proceed anyway, (2) Invoke `/debug-inference`, (3) Abort. **WAIT for user decision.**

**MCP Tool**: `get_model_endpoint` (from rhoai)

**Parameters**:
- `name`: selected InferenceService name - REQUIRED
- `namespace`: target namespace - REQUIRED

**If rhoai unavailable or returns error**: Extract endpoint from `.status.url` of the InferenceService obtained via `resources_get` (from openshift).

Store the endpoint URL for orchestrator routing. Present configuration summary for confirmation. **WAIT for user to confirm or modify.**

### Step 3: Configure Detectors

**Document Consultation** (read before configuring detectors):
1. **Action**: Read [guardrails-detectors-reference.md](references/guardrails-detectors-reference.md) using the Read tool to understand detector types, recommended models, and configuration structure
2. **Output to user**: "I consulted [guardrails-detectors-reference.md](references/guardrails-detectors-reference.md) to understand available detector configurations."

For each selected detector type:

#### Step 3a: Content Safety Detector (if selected)

Recommended model: `ibm-granite/granite-guardian-3.1-2b` (1 GPU, ~8Gi memory) per [guardrails-detectors-reference.md](references/guardrails-detectors-reference.md).

Check if a compatible detector model is already deployed using `list_inference_services` (from rhoai). If one exists, offer to reuse it. **WAIT for user decision.**

**If rhoai unavailable or returns error**: Use `resources_list` (from openshift) with `apiVersion: serving.kserve.io/v1beta1`, `kind: InferenceService`, `namespace: [namespace]` to check for existing detector models. To list available runtimes when `list_serving_runtimes` is unavailable: Use `resources_list` (from openshift) with `apiVersion: serving.kserve.io/v1alpha1`, `kind: ServingRuntime`, `namespace: [namespace]`.

If deploying a new detector:

**MCP Tool**: `deploy_model` (from rhoai)

**Parameters**:
- `name`: `"[isvc-name]-content-detector"` (derived from target model name to avoid collisions) - REQUIRED
- `namespace`: target namespace - REQUIRED
- `runtime`: appropriate runtime from `list_serving_runtimes` - REQUIRED
- `model_format`: `"vLLM"` - REQUIRED
- `storage_uri`: `"hf://ibm-granite/granite-guardian-3.1-2b"` - REQUIRED
- `gpu_count`: `1` - OPTIONAL
- `memory_request`: `"8Gi"` - OPTIONAL

**If rhoai unavailable or returns error**: Use `resources_create_or_update` (from openshift) to create the detector InferenceService CR directly with `apiVersion: serving.kserve.io/v1beta1`, `kind: InferenceService`.

**Ask**: "Deploy the content safety detector model? This creates an additional InferenceService. (yes/no/use-existing)"

**WAIT for explicit confirmation.** Monitor deployment until Ready.

**Error Handling**:
- If deployment fails -> Suggest `/debug-inference` for the detector InferenceService
- If insufficient GPU -> Suggest CPU-only deployment or smaller detector model

#### Step 3b: PII Detection (if selected)

Uses built-in regex-based detectors (no model deployment needed). Generate appropriate regex patterns. Present patterns to user for review. **WAIT for user decision.**

#### Step 3c: Prompt Injection Detector (if selected)

For model-based detection: reuse the granite-guardian model from Step 3a (covers prompt injection). For keyword-based detection: configure patterns. **WAIT for user decision.**

#### Step 3d: Custom Regex Detector (if requested)

Collect pattern name, regex, scope, and action from user.

### Step 4: Create Detector ConfigMap

Construct ConfigMap using the orchestrator config structure from [guardrails-detectors-reference.md](references/guardrails-detectors-reference.md). Populate with detector configs from Step 3 and target model endpoint from Step 1.

**MCP Tool**: `resources_create_or_update` (from openshift)

**Parameters**:
- `manifest`: ConfigMap YAML manifest as JSON string - REQUIRED

ConfigMap name: `guardrails-config-[isvc-name]`. Labels: `app.kubernetes.io/part-of: trustyai-guardrails`, `trustyai.opendatahub.io/target-model: [isvc-name]`.

Display the full ConfigMap to user. **Ask**: "Proceed with this guardrails configuration? (yes/no/modify)"

**WAIT for explicit confirmation.**

### Step 5: Deploy GuardrailsOrchestrator CR

Construct GuardrailsOrchestrator manifest using CRD spec from [guardrails-detectors-reference.md](references/guardrails-detectors-reference.md). Key values: name=`guardrails-[isvc-name]`, orchestratorConfig=`guardrails-config-[isvc-name]`, enableBuiltInDetectors=true, enableGuardrailsGateway=true.

**MCP Tool**: `resources_create_or_update` (from openshift)

**Parameters**:
- `manifest`: GuardrailsOrchestrator YAML manifest as JSON string - REQUIRED

Display manifest to user. **Ask**: "Deploy this GuardrailsOrchestrator? (yes/no/modify)"

**WAIT for explicit confirmation.**

**Error Handling**:
- If RBAC error -> Report insufficient permissions
- If CRD not found -> Suggest enabling TrustyAI guardrails component (RHOAI 2.14+)
- If resource quota exceeded -> Report and suggest reducing replicas

### Step 6: Verify Orchestrator Deployment

**MCP Tool**: `pods_list` (from openshift)

**Parameters**:
- `namespace`: target namespace - REQUIRED
- `labelSelector`: `"app.kubernetes.io/name=guardrails-[isvc-name]"` - REQUIRED

Verify orchestrator pod is Running. Poll every 15 seconds for up to 5 minutes.

**On failure:** Use `pods_log` and `events_list` (from openshift) to diagnose. Present options: (1) View full logs, (2) Check events, (3) Delete and recreate, (4) Abort. **WAIT for user decision. NEVER auto-delete GuardrailsOrchestrator.**

**Get guarded endpoint:** Use `resources_get` (from openshift) to read the GuardrailsOrchestrator CR status (`apiVersion: trustyai.opendatahub.io/v1alpha1`, `kind: GuardrailsOrchestrator`) and extract the guarded endpoint URL.

### Step 7: Validate Guarded Endpoint

First, verify the original model still responds correctly:

**MCP Tool**: `test_model_endpoint` (from rhoai)

**Parameters**:
- `name`: the original InferenceService name - REQUIRED
- `namespace`: target namespace - REQUIRED

**If rhoai unavailable or returns error**: Note that `test_model_endpoint` only checks reachability, not actual inference. For a real inference test, use an in-cluster curl command: `curl -X POST [endpoint]/v1/completions -H 'Content-Type: application/json' -d '{"model":"[model]","prompt":"Hello","max_tokens":10}'`

Then test the **guarded endpoint** directly. The guarded endpoint is a different URL from the original — obtain it from the GuardrailsOrchestrator CR status (Step 6). If the guarded endpoint is only available cluster-internally, set up port-forwarding to the orchestrator service first:

```
oc port-forward svc/guardrails-[isvc-name] 8080:8080 -n [namespace]
```

Run a safe request against the guarded endpoint to confirm it proxies correctly, then run an unsafe request (e.g., prompt injection attempt) to verify the detectors are active. Present both results to the user with pass/fail for each test.

### Step 8: Summary and Next Steps

Present summary showing: guarded vs original endpoint URLs, active detectors table (name, type, scope, policy), usage instructions (applications should use guarded endpoint), and next steps (`/model-monitor`, `/ai-observability`).

## Common Issues

For common issues (GPU scheduling, OOMKilled, image pull errors, RBAC), see [common-issues.md](../references/common-issues.md).

### Issue 1: Detector Model Deployment Fails

**Error**: Content safety or prompt injection detector model InferenceService fails to start

**Cause**: Insufficient resources (GPU/memory) for the detector model, or runtime compatibility issues.

**Solution:**
1. Check detector model resource requirements -- classifier models are typically 2B parameters
2. Verify GPU availability for the detector model
3. Consider CPU-only deployment for smaller detector models
4. Use `/debug-inference` to troubleshoot the detector InferenceService

### Issue 2: Guarded Endpoint Returns 502/503

**Error**: Requests to the guarded endpoint return 502 Bad Gateway or 503 Service Unavailable

**Cause**: The orchestrator cannot reach the underlying model endpoint, or the detector service is down.

**Solution:**
1. Verify the original model endpoint is accessible: `test_model_endpoint` from rhoai
2. Check orchestrator pod logs for connection errors: `pods_log`
3. Verify the ConfigMap `orchestrator.target_model.endpoint` URL is correct
4. Check detector model pods are running if using model-based detectors
5. Check network policies that might block pod-to-pod communication

### Issue 3: GuardrailsOrchestrator RBAC Denied

**Error**: Cannot create `guardrailsorchestrators` resource — 403 Forbidden

**Cause**: The user lacks RBAC for the GuardrailsOrchestrator CRD, which is typically cluster-admin only.

**Solution**: Provide the user with the complete GuardrailsOrchestrator CR YAML and instruct them to ask a cluster administrator to apply it. The detectors ConfigMap (which only requires namespace `edit` role) can still be created by the skill.

### Issue 4: High Latency or False Positives

**Error**: Guarded endpoint is significantly slower than direct endpoint, or legitimate requests are blocked

**Cause**: Too many model-based detectors add latency; overly aggressive thresholds or broad regex patterns cause false positives.

**Solution:**
1. Switch policy from "block" to "warn" temporarily to audit false positives
2. Use regex-based detectors instead of model-based where possible (lower latency)
3. Reduce detector count or switch from "input+output" to single scope
4. Review orchestrator logs to identify which detector triggered
5. Re-run `/guardrails-config` with modified configuration

## Dependencies

### MCP Tools
See [Prerequisites](#prerequisites) for the complete list of required and optional MCP tools.

### Related Skills
- `/model-deploy` - Deploy the target LLM before configuring guardrails; also used to deploy detector models
- `/model-monitor` - Add bias and drift monitoring (complements safety guardrails)
- `/debug-inference` - Troubleshoot failed detector model deployments or guarded endpoint issues
- `/ai-observability` - Monitor guardrails impact on latency and throughput
- `/serving-runtime-config` - Configure custom runtime for detector models if needed

### Reference Documentation
- [guardrails-detectors-reference.md](references/guardrails-detectors-reference.md) - Detector types, recommended models, CRD specs, and configuration structure

## Critical: Human-in-the-Loop Requirements

See [skill-conventions.md](../references/skill-conventions.md) for general HITL and security conventions.

**Skill-specific checkpoints:**
- After gathering requirements (Step 2): confirm guardrails configuration
- After target model validation (Step 2): confirm if model is not Ready (proceed/debug/abort)
- Before deploying detector models (Step 3a): confirm additional InferenceService creation and resource cost
- Before creating detector ConfigMap (Step 4): display full configuration, confirm
- Before deploying GuardrailsOrchestrator (Step 5): display manifest, confirm
- On orchestrator pod failure (Step 6): present diagnostic options, wait for user decision
- **NEVER** auto-delete GuardrailsOrchestrator or detector configurations
- **NEVER** modify the original model's InferenceService or deploy detector models without explicit confirmation
