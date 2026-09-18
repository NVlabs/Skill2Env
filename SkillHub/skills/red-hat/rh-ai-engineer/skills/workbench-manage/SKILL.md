---
name: workbench-manage
description: |
  Create and manage Jupyter notebook workbenches on OpenShift AI with image selection, resource configuration, PVC storage, and lifecycle management.

  Use when:
  - "Create a notebook workbench"
  - "Spin up a Jupyter environment for data science"
  - "Start / stop my workbench"
  - "What notebook images are available?"
  - "Delete a workbench I no longer need"

  Handles Notebook CR lifecycle: create with configurable images and resources, start/stop, attach storage, and delete with data loss warnings.

  NOT for deploying models (use /model-deploy).
  NOT for creating projects (use /ds-project-setup).
  NOT for managing pipelines (use /pipeline-manage).
color: blue
model: inherit
metadata:
  author: "Red Hat Ecosystem Engineering"
  version: "1.0"
license: Apache-2.0
allowed-tools: resources_get resources_list resources_create_or_update resources_delete events_list pods_list list_data_science_projects list_workbenches get_workbench create_workbench start_workbench stop_workbench delete_workbench get_workbench_url list_storage create_storage delete_storage list_data_connections
---

# /workbench-manage Skill

Create and manage Jupyter notebook workbenches on Red Hat OpenShift AI. Handles the full workbench lifecycle: listing available notebook images, creating Notebook CRs with configurable CPU/memory/GPU resources, provisioning PVC storage, starting and stopping workbenches, and deleting them with proper data loss warnings.

## Prerequisites

**Required MCP Server**: `openshift` ([OpenShift MCP Server](https://github.com/openshift/openshift-mcp-server))

**Required MCP Tools** (from openshift):
- `resources_get` - Inspect Notebook CR details, ImageStream details, check node GPU availability
- `resources_list` - List ImageStreams for notebook image discovery, list PVCs, list Notebooks
- `resources_create_or_update` - Create/update Notebook CR, PVC, patch annotations for start/stop (OpenShift fallback)
- `resources_delete` - Delete Notebook CR, PVC (OpenShift fallback for delete operations)
- `events_list` - Check pod events when workbench is stuck
- `pods_list` - Check workbench pod status

**Preferred MCP Server**: `rhoai` ([RHOAI MCP Server](https://github.com/opendatahub-io/rhoai-mcp)) — used when available, automatic OpenShift fallback on failure

**Preferred MCP Tools** (from rhoai):
- `list_data_science_projects` - Validate namespace is an RHOAI Data Science Project
- `list_workbenches` - List existing workbenches in a project
- `get_workbench` - Get workbench details (status, image, resources, storage)
- `create_workbench` - Create a new Notebook CR with image, resources, and storage
- `start_workbench` - Start a stopped workbench. **Known issue**: may fail with "Unsupported Media Type" — use annotation patch fallback.
- `stop_workbench` - Stop a running workbench. **Known issue**: may fail — use annotation patch fallback.
- `delete_workbench` - Delete a workbench. **Known issue**: may return "Dangerous operations are disabled" — use `resources_delete` fallback.
- `get_workbench_url` - Get the OAuth-protected notebook URL
- `list_storage` - List PVCs in the project
- `create_storage` - Create a PVC for workbench storage
- `delete_storage` - Delete a PVC
- `list_data_connections` - List data connections available to attach

**Common prerequisites** (KUBECONFIG, OpenShift+RHOAI cluster, verification protocol): See [skill-conventions.md](../references/skill-conventions.md).

**Fallback templates**: See [openshift-fallback-templates.md](../references/openshift-fallback-templates.md) for OpenShift YAML templates used when RHOAI tools are unavailable.

**Important**: Do NOT use `list_notebook_images` (from rhoai) — it returns incorrect hardcoded image names that cause broken deployments. Always use the ImageStream lookup pattern described below.

**Additional cluster requirements**:
- Target namespace is an RHOAI Data Science Project (label: `opendatahub.io/dashboard: "true"`)

## When to Use This Skill

**Use this skill when you need to:**
- Create a new Jupyter notebook workbench for a data scientist
- List available notebook images (PyTorch, TensorFlow, Standard Data Science, etc.)
- Start or stop an existing workbench
- List workbenches in a project and check their status
- Delete a workbench and its associated storage
- Provision persistent storage for a workbench

**Do NOT use this skill when:**
- You need to create a Data Science Project first (use `/ds-project-setup`)
- You want to deploy a model for inference (use `/model-deploy`)
- You need to manage data science pipelines (use `/pipeline-manage`)
- You need to troubleshoot a model deployment (use `/debug-inference`)

## Workflow

### Step 1: Determine Intent

**Ask the user what they want to do:**
- **Create** a new workbench
- **Start / Stop** an existing workbench
- **List** workbenches in a project
- **Delete** a workbench

**Ask for the target namespace** (required for all operations).

**Validate namespace** is a Data Science Project:

**MCP Tool**: `list_data_science_projects` (from rhoai)

**Parameters**: none

Verify the user-specified namespace appears in the project list. If not, report: "Namespace `[name]` is not an RHOAI Data Science Project. Use `/ds-project-setup` to create one."

**Route to the appropriate sub-workflow:**
- Create -> Step 2
- Start/Stop -> Step 5
- List -> Use `list_workbenches` (fallback: `resources_list` from openshift), display results, done
- Delete -> Step 6

### Step 2: Gather Configuration (Create)

**Notebook Image Discovery** (replaces `list_notebook_images` which returns incorrect names):

**Step 1**: List notebook ImageStreams:

**MCP Tool**: `resources_list` (from openshift)
- `apiVersion`: `image.openshift.io/v1`, `kind`: `ImageStream`, `namespace`: `redhat-ods-applications`, `labelSelector`: `opendatahub.io/notebook-image=true`

**Step 2**: For each ImageStream, get details:

**MCP Tool**: `resources_get` (from openshift)

Extract from each ImageStream:
- `.metadata.name` — the actual image name (e.g., `pytorch`, NOT `jupyter-pytorch-notebook`)
- `.spec.tags[].name` — available tags (e.g., `2024.1`)
- `.spec.tags[].annotations["opendatahub.io/notebook-image-name"]` — display name
- `.spec.tags[].from.name` — the full image reference to use in the Notebook CR

**Present to user** as a selection table showing Image Name, Tag, and Display Name.

See [openshift-fallback-templates.md](../references/openshift-fallback-templates.md#notebook-image-discovery-imagestream-lookup) for the complete pattern.

**Present available images** in a table:

| Image Name | Tag | Display Name |
|------------|-----|--------------|
| [name] | [tag] | [display_name] |

**Ask the user for workbench configuration:**
- **Workbench name**: DNS-compatible name (lowercase, hyphens, max 63 chars)
- **Image**: Selection from the available images list
- **CPU**: Number of CPU cores (default: 2)
- **Memory**: Memory allocation (default: 8Gi)
- **Storage size**: PVC size for persistent storage (default: 20Gi)
- **GPU** (optional): Number of GPUs to attach (e.g., 1)

**Display configuration table:**

| Setting | Value |
|---------|-------|
| Workbench name | [name] |
| Namespace | [namespace] |
| Image | [image_name] |
| CPU | [cpu] cores |
| Memory | [memory] |
| Storage | [storage_size] |
| GPU | [gpu_count or none] |

**WAIT for user to confirm or modify the configuration.**

### Step 3: Provision Storage (Create)

**Check existing storage:**

**MCP Tool**: `list_storage` (from rhoai)

**Parameters**:
- `namespace`: target namespace - REQUIRED

**If rhoai unavailable or returns error**: Use `resources_list`/`resources_create_or_update`/`resources_delete` (from openshift) for PersistentVolumeClaim resources. See [openshift-fallback-templates.md](../references/openshift-fallback-templates.md#pvc-for-workbench-storage).

If a suitable PVC already exists, ask user if they want to reuse it or create a new one.

**Create PVC for workbench storage:**

**MCP Tool**: `create_storage` (from rhoai)

**Parameters**:
- `namespace`: target namespace - REQUIRED
- `name`: PVC name (default: `[workbench-name]-storage`) - REQUIRED
- `size`: storage size from Step 2 (e.g., `"20Gi"`) - REQUIRED
- `access_mode`: `"ReadWriteOnce"` - REQUIRED (default, single-pod access)

**If rhoai unavailable or returns error**: Use `resources_list`/`resources_create_or_update`/`resources_delete` (from openshift) for PersistentVolumeClaim resources. See [openshift-fallback-templates.md](../references/openshift-fallback-templates.md#pvc-for-workbench-storage).

**Verify creation:**

**MCP Tool**: `list_storage` (from rhoai)

**Parameters**:
- `namespace`: target namespace - REQUIRED

Confirm the PVC appears and is in `Bound` or `Pending` state.

**Error Handling**:
- If PVC name already exists -> Ask: "PVC `[name]` already exists. Reuse it or create with a different name?"
- If StorageClass not available -> Report: "Default StorageClass not configured. Contact your cluster administrator."
- If quota exceeded -> Report namespace storage quota limits

### Step 4: Create Workbench (Create)

**MCP Tool**: `create_workbench` (from rhoai)

**Parameters**:
- `namespace`: target namespace - REQUIRED
- `name`: workbench name from Step 2 - REQUIRED
- `image`: selected notebook image name from Step 2 - REQUIRED
- `cpu`: CPU cores (e.g., `"2"`) - REQUIRED
- `memory`: memory allocation (e.g., `"8Gi"`) - REQUIRED
- `storage_size`: PVC storage size (e.g., `"20Gi"`) - REQUIRED

**Monitor workbench startup** by polling status:

**MCP Tool**: `get_workbench` (from rhoai)

**Parameters**:
- `namespace`: target namespace - REQUIRED
- `name`: workbench name - REQUIRED

Check until status shows the workbench is running. If status does not become ready within a reasonable polling window (3-4 checks), proceed to report current status and advise user to check back.

**Get notebook URL:**

**MCP Tool**: `get_workbench_url` (from rhoai)

**Parameters**:
- `namespace`: target namespace - REQUIRED
- `name`: workbench name - REQUIRED

**Error Handling**:
- If workbench name already exists -> Report: "Workbench `[name]` already exists. Choose a different name or manage the existing one."
- If image not found -> Re-run the ImageStream lookup pattern and suggest available alternatives
- If RBAC error -> Report insufficient permissions to create Notebook CRs
- If GPU unavailable -> Report: "Requested GPU resources not available on cluster nodes. Reduce GPU count or wait for resources."

**Report to user:**

| Detail | Value |
|--------|-------|
| Workbench | [name] |
| Status | [Running / Starting] |
| Image | [image] |
| Resources | [cpu] CPU, [memory] RAM, [gpu] GPU |
| Storage | [storage_size] |
| URL | [notebook_url] |

**Suggest next steps:**
- Access the notebook at the provided URL (OpenShift authentication required)
- Use `/ds-project-setup` to add data connections to the project
- Use `/model-deploy` when ready to deploy a trained model

### Step 5: Manage Lifecycle (Start/Stop)

**List workbenches to identify the target:**

**MCP Tool**: `list_workbenches` (from rhoai)

**Parameters**:
- `namespace`: target namespace - REQUIRED

**If rhoai unavailable or returns error**: Use `resources_list` (from openshift) with `apiVersion: kubeflow.org/v1`, `kind: Notebook`, `namespace: [namespace]`.

If user did not specify a workbench name, present the list and ask which one to manage.

**For Start:**

Confirm the workbench is currently stopped. If already running, report its URL and current status.

**MCP Tool**: `start_workbench` (from rhoai)

**Parameters**:
- `namespace`: target namespace - REQUIRED
- `name`: workbench name - REQUIRED

**If rhoai unavailable or returns error (e.g., "Unsupported Media Type")**: Patch the Notebook CR annotation via `resources_create_or_update` (from openshift) to remove the `kubeflow-resource-stopped` annotation (set to null or empty). See [openshift-fallback-templates.md](../references/openshift-fallback-templates.md#workbench-startstop-annotation-patch).

**MCP Tool**: `get_workbench_url` (from rhoai)

**Parameters**:
- `namespace`: target namespace - REQUIRED
- `name`: workbench name - REQUIRED

**Output to user**: "Workbench `[name]` started. Access it at: [url]"

**For Stop:**

**WAIT for user confirmation**: "Workbench `[name]` is currently running. Stopping it will interrupt any active sessions. Unsaved work in the notebook may be lost. Proceed? (yes/no)"

**MCP Tool**: `stop_workbench` (from rhoai)

**Parameters**:
- `namespace`: target namespace - REQUIRED
- `name`: workbench name - REQUIRED

**If rhoai unavailable or returns error**: Patch the Notebook CR via `resources_create_or_update` (from openshift) to set annotation `kubeflow-resource-stopped: "true"`. See [openshift-fallback-templates.md](../references/openshift-fallback-templates.md#workbench-startstop-annotation-patch).

**Verify state change:**

**MCP Tool**: `get_workbench` (from rhoai)

**Parameters**:
- `namespace`: target namespace - REQUIRED
- `name`: workbench name - REQUIRED

**If rhoai unavailable or returns error**: Use `resources_get` (from openshift) with `apiVersion: kubeflow.org/v1`, `kind: Notebook`, `name: [name]`, `namespace: [namespace]`.

**Output to user**: "Workbench `[name]` stopped. Persistent storage is preserved. Use `/workbench-manage` to start it again."

**Error Handling**:
- If workbench not found -> List available workbenches and ask user to select
- If already in target state -> Report current state (e.g., "Workbench is already running")

### Step 6: Delete Workbench

**Get workbench details:**

**MCP Tool**: `get_workbench` (from rhoai)

**Parameters**:
- `namespace`: target namespace - REQUIRED
- `name`: workbench name - REQUIRED

**If rhoai unavailable or returns error**: Use `resources_get` (from openshift) with `apiVersion: kubeflow.org/v1`, `kind: Notebook`, `name: [name]`, `namespace: [namespace]`.

**Display workbench details and data loss warning:**

| Detail | Value |
|--------|-------|
| Workbench | [name] |
| Status | [Running / Stopped] |
| Image | [image] |
| Storage | [pvc_name] ([size]) |

**WARNING**: Deleting this workbench will remove the Notebook CR. If the workbench is running, it will be stopped first. Any unsaved notebook work will be lost.

**Ask**: "Delete workbench `[name]`? This action cannot be undone. (yes/no)"

**WAIT for explicit confirmation.**

**MCP Tool**: `delete_workbench` (from rhoai)

**Parameters**:
- `namespace`: target namespace - REQUIRED
- `name`: workbench name - REQUIRED

**If rhoai unavailable or returns error (e.g., "Dangerous operations are disabled")**: Use `resources_delete` (from openshift) with `apiVersion: kubeflow.org/v1`, `kind: Notebook`, `name: [workbench-name]`, `namespace: [namespace]`. WAIT for user confirmation before deleting — warn about data loss.

**Associated storage cleanup** (separate confirmation):

**Ask**: "The PVC `[pvc_name]` ([size]) associated with this workbench still exists. Delete it too? WARNING: All data in this volume will be permanently lost. (yes/no)"

**WAIT for explicit confirmation.**

If user confirms PVC deletion:

**MCP Tool**: `delete_storage` (from rhoai)

**Parameters**:
- `namespace`: target namespace - REQUIRED
- `name`: PVC name - REQUIRED

**If rhoai unavailable or returns error**: Use `resources_list`/`resources_create_or_update`/`resources_delete` (from openshift) for PersistentVolumeClaim resources. See [openshift-fallback-templates.md](../references/openshift-fallback-templates.md#pvc-for-workbench-storage).

If user declines, report: "PVC `[pvc_name]` preserved. It can be reattached to a new workbench."

**Output to user**: "Workbench `[name]` deleted. [PVC deleted / PVC preserved]."

## Common Issues

For common issues (GPU scheduling, OOMKilled, image pull errors, RBAC), see [common-issues.md](../references/common-issues.md).

### Issue 1: Notebook Image Not Found

**Error**: `create_workbench` fails with image not found or image reference is invalid

**Cause**: The selected image name does not match any available notebook image, or the image registry is unreachable.

**Solution:**
1. Run the ImageStream lookup pattern to see current available images
2. Verify the exact image name (case-sensitive)
3. If no images are listed, the RHOAI operator may not have imported notebook images -- contact cluster administrator

### Issue: Workbench Created with Wrong Image (ImagePullBackOff)

**Error**: Workbench pod stuck in `ImagePullBackOff` after creation

**Cause**: The `list_notebook_images` tool returned incorrect image names (e.g., `jupyter-pytorch-notebook` instead of the actual ImageStream name `pytorch`).

**Solution**: This tool has been replaced. Use the ImageStream lookup pattern via OpenShift MCP to discover correct image names. Patch the stuck Notebook CR with the correct image reference from the ImageStream, then delete the stuck pod to force rescheduling.

See [common-issues.md](../references/common-issues.md#notebook-image-names-mismatch) for details.

### Issue 2: PVC Binding Failure

**Error**: PVC remains in `Pending` state, workbench cannot start

**Cause**: The default StorageClass does not support the requested access mode, or no StorageClass is configured.

**Solution:**
1. Check available StorageClasses via `resources_get` (from openshift) on `storageclasses.storage.k8s.io`
2. Use `ReadWriteOnce` access mode (most widely supported)
3. If `ReadWriteMany` is required, verify the StorageClass supports it (e.g., NFS, CephFS)
4. Contact cluster administrator if no StorageClass is available

### Issue 3: Workbench Stuck in Starting

**Error**: Workbench status remains in a starting/initializing state for an extended period

**Cause**: Pod scheduling issues, image pull errors, or resource constraints.

**Solution:**
1. Use `events_list` (from openshift) filtered by namespace to check for pod events
2. Common causes:
   - `ImagePullBackOff`: Image registry unreachable or credentials missing
   - `Insufficient cpu/memory`: Reduce resource requests or free up cluster resources
   - `FailedScheduling`: Node taints or affinity rules preventing scheduling
3. If GPU is requested, verify GPU nodes have available capacity

## Dependencies

### MCP Tools
See [Prerequisites](#prerequisites) for the complete list of required and optional MCP tools.

### Related Skills
- `/ds-project-setup` - Create a Data Science Project (prerequisite: namespace must exist)
- `/model-deploy` - Deploy a trained model from the workbench
- `/ai-observability` - Check GPU inventory before requesting GPU workbenches

### Reference Documentation
- [skill-conventions.md](../references/skill-conventions.md) - Shared prerequisite, HITL, and security conventions

## Example Usage

**User**: "Create a PyTorch notebook workbench in my ml-team project with 4 CPUs and a GPU"

**Skill response**: Validates `ml-team` is an RHOAI project, lists available notebook images, presents configuration table (PyTorch image, 4 CPU, 8Gi memory, 1 GPU, 20Gi storage), provisions PVC storage, creates workbench, monitors startup, and returns the notebook URL.

## Critical: Human-in-the-Loop Requirements

See [skill-conventions.md](../references/skill-conventions.md) for general HITL and security conventions.

**Skill-specific checkpoints:**
- Before creating workbench (Step 4): display full configuration table, confirm
- Before stopping a workbench (Step 5): warn about unsaved work, confirm
- Before deleting a workbench (Step 6): display details, warn about data loss, confirm
- Before deleting associated PVC (Step 6): separate confirmation with permanent data loss warning
- **NEVER** auto-delete workbenches or storage
- **NEVER** stop a running workbench without confirmation (user may have unsaved notebook work)
