---
name: ds-project-setup
description: |
  Create and configure Data Science Projects on OpenShift AI with namespace setup, S3 data connections, pipeline server, and model serving enablement.

  Use when:
  - "Create a data science project"
  - "Set up a new namespace for ML work"
  - "Add an S3 data connection to my project"
  - "Configure the pipeline server"
  - "Enable model serving on my project"

  Bootstraps an RHOAI Data Science Project with proper labels, data connections, pipeline infrastructure, and model serving configuration.

  NOT for deploying models (use /model-deploy).
  NOT for creating workbenches (use /workbench-manage).
  NOT for managing pipelines after setup (use /pipeline-manage).
color: green
model: inherit
metadata:
  author: "Red Hat Ecosystem Engineering"
  version: "1.0"
license: Apache-2.0
allowed-tools: resources_get resources_list resources_create_or_update list_data_science_projects create_data_science_project get_project_details get_project_status create_s3_data_connection list_data_connections get_pipeline_server set_model_serving_mode
---

# /ds-project-setup Skill

Bootstrap a Red Hat OpenShift AI Data Science Project from scratch. Creates a namespace with RHOAI dashboard labels, configures S3-compatible data connections, sets up the pipeline server with external storage, and enables model serving on the project.

## Prerequisites

**Required MCP Server**: `openshift` ([OpenShift MCP Server](https://github.com/openshift/openshift-mcp-server))

**Required MCP Tools** (from openshift):
- `resources_get` - Inspect namespace labels, LimitRange, ResourceQuota, DSPA status
- `resources_list` - List namespaces, Secrets, PVCs (OpenShift fallback for RHOAI tools)
- `resources_create_or_update` - Create namespaces, Secrets, DSPA CRs (OpenShift fallback and primary for pipeline server)

**Preferred MCP Server**: `rhoai` ([RHOAI MCP Server](https://github.com/opendatahub-io/rhoai-mcp)) — used when available, automatic OpenShift fallback on failure

**Preferred MCP Tools** (from rhoai):
- `list_data_science_projects` - List existing RHOAI projects to check for duplicates
- `create_data_science_project` - Create namespace with RHOAI labels and dashboard integration
- `get_project_details` - Verify project creation and inspect configuration. **Note**: use `name` parameter, not `namespace`.
- `get_project_status` - Get comprehensive project status including components
- `create_s3_data_connection` - Create S3-compatible data connection secret
- `list_data_connections` - List existing data connections in the project
- `get_pipeline_server` - Check pipeline server configuration
- `set_model_serving_mode` - Enable single-model or multi-model serving

Note: `create_pipeline_server` is intentionally excluded — it constructs invalid DSPA manifests. Pipeline server creation always uses OpenShift direct.

**Common prerequisites** (KUBECONFIG, OpenShift+RHOAI cluster, verification protocol): See [skill-conventions.md](../references/skill-conventions.md).

**Fallback templates**: See [openshift-fallback-templates.md](../references/openshift-fallback-templates.md) for OpenShift YAML templates used when RHOAI tools are unavailable.

**Additional cluster requirements**:
- Cluster admin or namespace creation privileges for the user

## When to Use This Skill

**Use this skill when you need to:**
- Create a new Data Science Project namespace for an ML team
- Add S3 data connections to an existing project
- Configure the pipeline server on a project
- Enable or change the model serving mode (single vs multi-model)
- Bootstrap a complete project environment before deploying models or workbenches

**Do NOT use this skill when:**
- You want to deploy a model (use `/model-deploy`)
- You need to create a notebook workbench (use `/workbench-manage`)
- You need to manage pipeline runs (use `/pipeline-manage`)
- You need to configure a custom serving runtime (use `/serving-runtime-config`)

## Workflow

### Step 1: Gather Requirements

**Ask the user for the project name first:**
- **Project name**: DNS-compatible name for the namespace (lowercase, no spaces, max 63 chars)

**Immediately check if the project name already exists:**

**MCP Tool**: `list_data_science_projects` (from rhoai)

**Parameters**: none

- If project **exists**: Report to user and offer options: "Project `[name]` already exists. Would you like to: (a) configure additional components on it, or (b) choose a different name?" **WAIT for user decision.** If user chooses (a), skip Step 2 and proceed to optional configuration steps (Steps 3-5). If user chooses (b), repeat the name check.
- If project **does not exist**: Continue gathering remaining requirements below.

**If rhoai unavailable or returns error**: Use `resources_list` (from openshift) with `apiVersion: v1`, `kind: Namespace`, `labelSelector: opendatahub.io/dashboard=true`.

**Ask the user for remaining settings:**
- **Display name**: Human-readable project name for the RHOAI dashboard
- **Description**: Optional project description
- **Data connections**: Whether to configure S3 data connections (yes/no)
- **Pipeline server**: Whether to configure the pipeline server (yes/no, requires data connection)
- **Model serving mode**: "single" (default, one model per endpoint) or "multi" (multiple models per endpoint)

**Present configuration table:**

| Setting | Value |
|---------|-------|
| Project name | [name] |
| Display name | [display_name] |
| Description | [description] |
| Data connections | [yes/no] |
| Pipeline server | [yes/no] |
| Model serving mode | [single/multi] |

**WAIT for user to confirm or modify the configuration.**

### Step 2: Create Data Science Project

**MCP Tool**: `create_data_science_project` (from rhoai)

**Parameters**:
- `name`: project name from Step 1 - REQUIRED (DNS-compatible: lowercase alphanumeric and hyphens, max 63 chars)
- `display_name`: human-readable display name - REQUIRED
- `description`: project description - OPTIONAL

**If rhoai unavailable or returns error**: Use `resources_create_or_update` (from openshift) to create the Namespace with RHOAI labels. See [openshift-fallback-templates.md](../references/openshift-fallback-templates.md#data-science-project-namespace) for the YAML template.

**Verify creation:**

**MCP Tool**: `get_project_details` (from rhoai)

**Parameters**:
- `name`: the created project name - REQUIRED

Confirm the project was created with proper RHOAI labels (`opendatahub.io/dashboard: "true"`).

**If rhoai unavailable or returns error**: Use `resources_get` (from openshift) with `apiVersion: v1`, `kind: Namespace`, `name: [project-name]`. Check for label `opendatahub.io/dashboard: "true"`.

**Note**: The `get_project_details` tool requires a `name` parameter (not `namespace`). If the tool returns a parameter error, fall back to OpenShift.

**Error Handling**:
- If name already taken -> Offer alternative name or configure existing project
- If RBAC error -> Report: "Insufficient permissions to create namespaces. Contact your cluster administrator."
- If name invalid -> Report DNS naming constraints and suggest a valid name

**Output to user**: "Data Science Project `[name]` created successfully."

### Step 3: Configure Data Connections (Optional)

Skip this step if user declined data connections in Step 1.

**Ask the user for S3 connection details:**
- **Connection name**: Identifier for this data connection
- **S3 bucket**: Target bucket name
- **S3 endpoint**: S3-compatible endpoint URL (e.g., `https://s3.amazonaws.com`, MinIO endpoint)
- **Access key**: AWS access key ID or S3-compatible access key
- **Secret key**: AWS secret access key or S3-compatible secret key
- **Region**: AWS region or empty for non-AWS S3

**Display connection configuration** (credentials REDACTED):

| Setting | Value |
|---------|-------|
| Connection name | [name] |
| Bucket | [bucket] |
| Endpoint | [endpoint] |
| Access key | [first-4-chars]****  |
| Secret key | ********  |
| Region | [region] |

**WAIT for user to confirm the connection details are correct.**

**MCP Tool**: `create_s3_data_connection` (from rhoai)

**Parameters**:
- `namespace`: project name from Step 2 - REQUIRED
- `name`: connection name - REQUIRED
- `bucket`: S3 bucket name - REQUIRED
- `endpoint`: S3 endpoint URL - REQUIRED
- `access_key`: access key ID - REQUIRED
- `secret_key`: secret access key - REQUIRED
- `region`: AWS region - OPTIONAL (omit for non-AWS S3)

**If rhoai unavailable or returns error**: Use `resources_create_or_update` (from openshift) to create the Secret with S3 annotations. See [openshift-fallback-templates.md](../references/openshift-fallback-templates.md#s3-data-connection-secret) for the YAML template.

**Verify creation:**

**MCP Tool**: `list_data_connections` (from rhoai)

**Parameters**:
- `namespace`: project name - REQUIRED

Confirm the data connection appears in the list.

**If rhoai unavailable or returns error**: Use `resources_list` (from openshift) with `apiVersion: v1`, `kind: Secret`, `namespace: [namespace]`, `labelSelector: opendatahub.io/dashboard=true`. Filter results by annotation `opendatahub.io/connection-type: s3`.

**Error Handling**:
- If connection name already exists -> Ask: "Data connection `[name]` already exists. Create with a different name?"
- If RBAC error -> Report insufficient permissions to create Secrets in namespace

**Output to user**: "Data connection `[name]` created in project `[namespace]`."

**Repeat this step** if user wants to create multiple data connections.

### Step 4: Configure Pipeline Server (Optional)

Skip this step if user declined pipeline server in Step 1.

**Prerequisite check**: A data connection must exist in the project (from Step 3 or pre-existing). If no data connections exist, inform user: "Pipeline server requires an S3 data connection for artifact storage. Would you like to create one now?" and return to Step 3.

**MCP Tool**: `get_pipeline_server` (from rhoai)

**Parameters**:
- `namespace`: project name - REQUIRED

If pipeline server already exists, report its status and ask if user wants to reconfigure.

**Display pipeline server configuration:**

| Setting | Value |
|---------|-------|
| Namespace | [namespace] |
| Data connection | [data_connection_name] |

**WAIT for user to confirm pipeline server setup.**

**Pipeline Server Creation** (OpenShift direct — the `create_pipeline_server` RHOAI tool is not used because it constructs invalid DSPA manifests):

**MCP Tool**: `resources_create_or_update` (from openshift)

Create a DataSciencePipelinesApplication CR using the template from [openshift-fallback-templates.md](../references/openshift-fallback-templates.md#datasciencepipelinesapplication-dspa).

**Parameters to fill in the template:**
- `namespace`: target namespace
- `bucket`: S3 bucket name from the data connection
- `host`: S3 endpoint without protocol prefix (e.g., `minio.namespace.svc:9000`)
- `scheme`: `http` or `https`
- `secretName`: name of the S3 data connection secret created in Step 3
- `region`: AWS region or empty string for MinIO

**Verify DSPA is ready:**

**MCP Tool**: `resources_get` (from openshift)
- `apiVersion`: `datasciencepipelinesapplications.opendatahub.io/v1alpha1`, `kind`: `DataSciencePipelinesApplication`, `name`: `dspa`, `namespace`: [namespace]

Check `.status.conditions` for `Ready=True`. Poll every 15 seconds until ready or timeout (5 minutes).

**Verify creation:**

**MCP Tool**: `get_pipeline_server` (from rhoai)

**Parameters**:
- `namespace`: project name - REQUIRED

Confirm the pipeline server is configured and initializing.

**If rhoai unavailable or returns error**: Use `resources_get` (from openshift) for the DSPA CR as described above.

**Error Handling**:
- If data connection not found -> Report: "Data connection `[name]` not found in namespace. Create it first."
- If pipeline server already exists -> Ask user whether to reconfigure or keep existing
- If RBAC error -> Report insufficient permissions

**Output to user**: "Pipeline server configured in project `[namespace]` using data connection `[data_connection]`."

### Step 5: Enable Model Serving and Report

**MCP Tool**: `set_model_serving_mode` (from rhoai)

**Parameters**:
- `namespace`: project name - REQUIRED
- `mode`: "single" or "multi" - REQUIRED (default: "single")

**If rhoai unavailable or returns error**: Patch the namespace annotation via `resources_create_or_update` (from openshift). Set annotation `opendatahub.io/model-serving-mode` to `single` or `multi` on the Namespace.

**Final validation:**

**MCP Tool**: `get_project_status` (from rhoai)

**Parameters**:
- `namespace`: project name - REQUIRED

**Report project summary:**

| Component | Status |
|-----------|--------|
| Project | [name] (created / existing) |
| Data connections | [count] configured |
| Pipeline server | [configured / not configured] |
| Model serving | [single / multi] mode enabled |

**Suggest next steps:**
- `/workbench-manage` - Create a notebook workbench in this project
- `/model-deploy` - Deploy a model to this project
- `/pipeline-manage` - Create and run data science pipelines
- `/model-registry` - Register and manage models in the Model Registry

## Common Issues

### Issue 1: Project Name Already Exists

**Error**: `create_data_science_project` returns conflict error

**Cause**: A namespace with the same name already exists in the cluster, either as an RHOAI project or a regular OpenShift project.

**Solution:**
1. Use `list_data_science_projects` to check if it is an existing RHOAI project
2. If it is an RHOAI project, offer to configure additional components on it
3. If it is a regular namespace (not an RHOAI project), suggest a different name or advise converting it by adding the `opendatahub.io/dashboard: "true"` label

### Issue 2: S3 Endpoint Unreachable

**Error**: Data connection created but pipeline server or model serving cannot access storage

**Cause**: The S3 endpoint URL is malformed, unreachable from the cluster, or requires TLS configuration.

**Solution:**
1. Verify the endpoint URL format includes the protocol (`https://`)
2. For MinIO: use the internal cluster service URL (e.g., `http://minio.minio-ns.svc:9000`)
3. For AWS: use the regional endpoint (e.g., `https://s3.us-east-1.amazonaws.com`)
4. Check if the cluster has network egress restrictions that block external S3 access

### Issue 3: Pipeline Server Fails to Initialize

**Error**: Pipeline server status remains unhealthy or pods crash

**Cause**: Usually caused by an invalid data connection (wrong credentials or unreachable bucket), or insufficient cluster resources.

**Solution:**
1. Verify the data connection credentials are correct (re-create if needed)
2. Check that the S3 bucket exists and is accessible with the provided credentials
3. Check namespace ResourceQuota for pod limits
4. Review pipeline server pod logs via `pods_log` (from openshift) for specific error messages

### Issue 4: Namespace Quota Exceeded

**Error**: Resource creation fails with quota exceeded error

**Cause**: The cluster has ResourceQuota or LimitRange policies that restrict resource creation in the namespace.

**Solution:**
1. Use `resources_get` (from openshift) to inspect ResourceQuota in the namespace
2. Report the quota limits to the user
3. Suggest contacting the cluster administrator to increase quotas or clean up unused resources

## Dependencies

### MCP Tools
See [Prerequisites](#prerequisites) for the complete list of required and optional MCP tools.

### Related Skills
- `/workbench-manage` - Create notebook workbenches in the project
- `/model-deploy` - Deploy models to the project
- `/pipeline-manage` - Create and manage pipeline runs
- `/serving-runtime-config` - Configure custom serving runtimes in the project

### Reference Documentation
- [skill-conventions.md](../references/skill-conventions.md) - Shared prerequisite, HITL, and security conventions

## Example Usage

**User**: "Create a data science project called fraud-detection with an S3 connection and pipeline server"

**Skill response**: Gathers requirements, presents configuration table, creates project `fraud-detection`, configures S3 data connection (credentials redacted in display), sets up pipeline server, enables single-model serving, and reports final project status with next steps.

## Critical: Human-in-the-Loop Requirements

See [skill-conventions.md](../references/skill-conventions.md) for general HITL and security conventions.

**Skill-specific checkpoints:**
- After project name existence check (Step 1): if project exists, confirm whether to configure existing or choose new name
- After gathering all requirements (Step 1): confirm project configuration table before proceeding
- Before creating data connections (Step 3): display connection config with credentials REDACTED, confirm
- Before configuring pipeline server (Step 4): confirm data connection selection
- **NEVER** create data connections without user confirming credential details
- **NEVER** display actual S3 access keys or secret keys in output
