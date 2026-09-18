---
name: model-registry
description: |
  Register, version, and manage ML models in the OpenShift AI Model Registry. Browse the Model Catalog, track model metadata, and promote models across environments.

  Use when:
  - "Register a new model in the registry"
  - "List registered models"
  - "What versions exist for my model?"
  - "Promote a model from dev to production"
  - "Show model artifacts and storage URIs"

  Handles model registration, versioning, metadata management, artifact tracking, and cross-environment promotion.

  NOT for deploying models (use /model-deploy).
  NOT for model performance monitoring (use /ai-observability).
color: cyan
model: inherit
license: Apache-2.0
allowed-tools: resources_create_or_update resources_get resources_list list_registered_models get_registered_model list_model_versions get_model_version get_model_artifacts get_model_benchmarks get_catalog_model_artifacts list_data_science_projects list_data_connections
---

# /model-registry Skill

Register, version, and manage ML models in the Red Hat OpenShift AI Model Registry. Supports browsing the Model Catalog, listing registered models with versions and artifacts, registering new models, creating model versions with storage URIs, promoting models across environments (dev -> staging -> prod), and deploying registered model versions via `/model-deploy`.

## Prerequisites

**Required MCP Server**: `openshift` ([OpenShift MCP Server](https://github.com/openshift/openshift-mcp-server))

**Required MCP Tools** (from openshift):
- `resources_create_or_update` (from openshift) - Create RegisteredModel, ModelVersion, and ModelArtifact resources
- `resources_get` (from openshift) - Inspect Model Registry instance and CRs
- `resources_list` (from openshift) - List Model Registry instances and resources

**Preferred MCP Server**: `rhoai` ([RHOAI MCP Server](https://github.com/opendatahub-io/rhoai-mcp)) — used when available, automatic OpenShift fallback on failure

**Preferred MCP Tools** (from rhoai):
- `list_registered_models` - List registered models with pagination, auto-detects Registry vs Catalog
- `get_registered_model` - Get model details by ID, optionally with all versions
- `list_model_versions` - List versions of a registered model with pagination
- `get_model_version` - Get specific version details (state, author, custom properties)
- `get_model_artifacts` - Get artifacts (storage URIs) for a model version
- `get_model_benchmarks` - Get benchmark data (latency, throughput, GPU memory)
- `get_catalog_model_artifacts` - Get artifacts from Model Catalog entries
- `list_data_science_projects` - Validate namespace is an RHOAI Data Science Project
- `list_data_connections` - Verify S3 data connections exist in target namespace (for promotion)

**Common prerequisites** (KUBECONFIG, OpenShift+RHOAI cluster, verification protocol): See [skill-conventions.md](../references/skill-conventions.md).

**Fallback templates**: See [openshift-fallback-templates.md](../references/openshift-fallback-templates.md) for OpenShift YAML templates used when RHOAI tools are unavailable.

**Important**: Model Registry RHOAI tools may fail with DNS/connection errors because the RHOAI MCP server runs outside the cluster and cannot resolve internal service DNS names. If this happens:
1. Check if an external Route exists: `resources_list` (from openshift) Routes in the model registry namespace
2. If no Route: set up port-forwarding — `oc port-forward svc/modelregistry-sample 8085:8085 -n rhoai-model-registries`
3. For registry CRUD: use `resources_create_or_update` / `resources_get` / `resources_list` via OpenShift MCP for RegisteredModel, ModelVersion, and ModelArtifact CRs

**Additional cluster requirements**:
- Model Registry operator installed and a ModelRegistry instance deployed in the cluster
- For cross-environment promotion: Model Registry instances in both source and target namespaces

## When to Use This Skill

**Use this skill when you need to:**
- Browse the RHOAI Model Catalog for available models
- List registered models and their versions in a project
- View model artifacts, storage URIs, and benchmark data
- Register a new model in the Model Registry
- Create a new version of an existing registered model
- Promote a model from one environment to another (dev -> staging -> prod)
- Deploy a specific registered model version (delegates to `/model-deploy`)

**Do NOT use this skill when:**
- You want to deploy a model for inference (use `/model-deploy`)
- You need to monitor model performance after deployment (use `/ai-observability`)
- You need to create a Data Science Project (use `/ds-project-setup`)
- You need to debug a failed model deployment (use `/debug-inference`)

## Workflow

### Step 1: Determine Intent

Ask the user what they want to do: **Browse** catalog, **List** models, **View** details/versions, **Register** model, **Create version**, **Promote** across envs, **Deploy** from registry.

Ask for the target namespace (required except for catalog browsing). Validate via `list_data_science_projects` (from rhoai). If invalid, suggest `/ds-project-setup`.

**If rhoai unavailable or returns error**: Use `resources_list` (from openshift) with `apiVersion: v1`, `kind: Namespace`, `labelSelector: opendatahub.io/dashboard=true` to validate namespace is a Data Science Project.

Route: Browse/List -> Step 2, View -> Step 3, Register -> Step 4, Version -> Step 5, Promote -> Step 6, Deploy -> Step 7.

### Step 2: Browse Model Catalog / List Registered Models

For catalog browsing, use `resources_list` (from openshift) with the appropriate catalog source CRD to show available sources.

**MCP Tool**: `list_registered_models` (from rhoai)

**Parameters**:
- `source_label`: catalog source filter (e.g., `"Red Hat AI validated"`) - OPTIONAL (Model Catalog only)
- `limit`: number of models to return - OPTIONAL
- `verbosity`: `"standard"` or `"minimal"` - OPTIONAL

**If rhoai unavailable or returns error**: Use `resources_list` (from openshift) with `apiVersion: modelregistry.opendatahub.io/v1alpha1`, `kind: RegisteredModel`.

For catalog model artifacts, use `get_catalog_model_artifacts` (from rhoai) with `model_name` (REQUIRED).

**Error Handling**:
- If Model Registry not installed -> Guide user to install the Model Registry operator via OperatorHub

### Step 3: View Model Details and Versions

Use `get_registered_model` (from rhoai) with `model_id` and `include_versions=true` to get model details with version summary.

**If rhoai unavailable or returns error**: Use `resources_get` (from openshift) with `apiVersion: modelregistry.opendatahub.io/v1alpha1`, `kind: RegisteredModel`, `name: [name]`, `namespace: [namespace]`.

For version listing, use `list_model_versions` (from rhoai) with `model_id` (REQUIRED).

**If rhoai unavailable or returns error**: Use `resources_list` (from openshift) with `apiVersion: modelregistry.opendatahub.io/v1alpha1`, `kind: ModelVersion`.

For specific version details: `get_model_version` (from rhoai) with `version_id` (REQUIRED).

For artifacts (storage URIs): `get_model_artifacts` (from rhoai) with `version_id` (REQUIRED).

For benchmarks (optional): `get_model_benchmarks` (from rhoai) with `model_name` (REQUIRED), optionally `version_name` and `gpu_type` filter.

### Step 4: Register a New Model

**Gather from user:** model name, description, owner, and optional custom properties (framework, task type, metadata key-value pairs).

Present configuration for review. **WAIT for user confirmation.**

**Check for Model Registry instance** via `resources_list` (from openshift):

**Parameters**:
- `apiVersion`: `"modelregistry.opendatahub.io/v1alpha1"` - REQUIRED
- `kind`: `"ModelRegistry"` - REQUIRED

**Create the registered model** via `resources_create_or_update` (from openshift):

**Parameters**:
- `resource`: RegisteredModel CR (apiVersion: `modelregistry.opendatahub.io/v1alpha1`, kind: `RegisteredModel`) with `spec.name`, `spec.description`, `spec.owner`, `spec.customProperties` - REQUIRED

**Error Handling**:
- If name already exists -> Offer: (a) create a new version, or (b) choose a different name
- If ModelRegistry not found -> Guide to install the operator via OperatorHub

### Step 5: Create Model Version

**Gather from user:** parent model (name or ID), version name, description, storage URI (`s3://`, `pvc://`, or `hf://`), model format (`pytorch`, `onnx`, `safetensors`), and optional custom properties.

Resolve parent model ID via `list_registered_models` (from rhoai) if user provided a name.

Present configuration for review. **WAIT for user confirmation.**

**Create model version** via `resources_create_or_update` (from openshift):

**Parameters**:
- `resource`: ModelVersion CR (apiVersion: `modelregistry.opendatahub.io/v1alpha1`, kind: `ModelVersion`) with `spec.registeredModelId`, `spec.name`, `spec.description`, `spec.customProperties` - REQUIRED

**Create model artifact** (linked to version) via `resources_create_or_update` (from openshift):

**Parameters**:
- `resource`: ModelArtifact CR (apiVersion: `modelregistry.opendatahub.io/v1alpha1`, kind: `ModelArtifact`) with `spec.modelVersionId`, `spec.uri`, `spec.modelFormatName` - REQUIRED

**Error Handling**:
- If parent model not found -> Suggest registering the model first (Step 4)

### Step 6: Promote Model Across Environments

**Gather from user:** source model (name/ID), source version (default: latest), source namespace, target namespace.

Validate both namespaces via `list_data_science_projects` (from rhoai).

Read source model details using `get_registered_model`, `get_model_version`, and `get_model_artifacts` (all from rhoai).

Check target namespace has a Model Registry via `resources_list` (from openshift) with apiVersion `modelregistry.opendatahub.io/v1alpha1`, kind `ModelRegistry`.

**IMPORTANT**: If the storage URI uses PVC storage local to the source namespace, warn the user it will not be accessible from the target. Recommend S3 for cross-namespace promotion.

Present promotion summary (source, target, storage URI, format, metadata). **WAIT for user confirmation.**

Execute promotion by registering model and version in the target namespace using Steps 4 and 5 procedures.

Offer next steps: `/model-deploy` to deploy the promoted model.

**Error Handling**:
- If target namespace missing -> Suggest `/ds-project-setup`
- If PVC-based storage URI -> Warn about cross-namespace inaccessibility

### Step 7: Deploy a Registered Model Version

If model/version not already identified, use `list_registered_models` and `list_model_versions` (from rhoai) for user selection.

Extract storage URI and format from `get_model_artifacts` (from rhoai) with `version_id` (REQUIRED).

Delegate to `/model-deploy` with the extracted storage URI and model format.

## Common Issues

### Issue 1: Model Registry Not Installed
**Cause**: Model Registry operator not installed or no ModelRegistry instance created.
**Solution**: Check via `resources_list` (from openshift) for `ModelRegistry` CRs. If missing, install via OperatorHub.

### Issue 2: Model Registry Unreachable from MCP

**Error**: RHOAI MCP tools for model registry return connection errors or 404

**Cause**: The RHOAI MCP server runs outside the cluster and cannot resolve cluster-internal DNS. External routes may also be behind an OAuth proxy.

**Solution**: See [common-issues.md](../references/common-issues.md#model-registry-internal-dns-unreachable) for port-forwarding and Route-based solutions.

### Issue 3: Artifact Storage Inaccessible During Promotion
**Cause**: PVC-based storage is namespace-local; S3 credentials may not exist in the target namespace.
**Solution**: For S3, verify data connection exists in target namespace via `list_data_connections`. For PVCs, recommend migrating to S3 for cross-namespace portability.

## Dependencies

### MCP Tools
See [Prerequisites](#prerequisites) for the complete list of required MCP tools.

### Related Skills
- `/model-deploy` - Deploy a registered model version for inference
- `/ds-project-setup` - Create a Data Science Project with Model Registry access
- `/ai-observability` - Monitor deployed model performance and benchmarks
- `/debug-inference` - Troubleshoot deployed model issues
- `/pipeline-manage` - Automate model training and registration pipelines

### Reference Documentation
- [skill-conventions.md](../references/skill-conventions.md) - Shared prerequisite, HITL, and security conventions

## Critical: Human-in-the-Loop Requirements

See [skill-conventions.md](../references/skill-conventions.md) for general HITL and security conventions.

**Skill-specific checkpoints:**
- Before registering a model (Step 4): display metadata table, confirm
- Before creating a version (Step 5): display version config table, confirm
- Before promoting across environments (Step 6): display promotion summary with source/target details, warn about storage accessibility, confirm
- If model name already exists (Step 4): confirm whether to create a version or use a different name
- **NEVER** auto-register models or auto-promote across environments without confirmation
- **NEVER** display credential values from data connections or storage secrets

## Example Usage

**User**: "Register a new model called sentiment-analyzer and create version v1.0 with weights stored at s3://ml-models/sentiment/v1"

**Skill response**: Gathers metadata, presents registration table for confirmation, creates RegisteredModel CR, then gathers version details, presents version config for confirmation, creates ModelVersion and ModelArtifact CRs, reports success.
