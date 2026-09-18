---
name: debug-pipeline
description: |
  Diagnose OpenShift Pipelines (Tekton) CI/CD failures including PipelineRun failures, TaskRun step errors, workspace/PVC binding issues, and authentication problems. Automates multi-step diagnosis: PipelineRun status, failed TaskRun analysis, step container logs, and related resource checks. Use this skill when pipelines fail, hang, or produce unexpected results. Triggers on /debug-pipeline command or phrases like "pipeline failed", "PipelineRun error", "TaskRun failed", "tekton error", "pipeline stuck", "pipeline timeout".
model: inherit
color: cyan
license: Apache-2.0
allowed-tools: resources_list resources_get pods_log
metadata:
  user_invocable: "true"
---

# /debug-pipeline Skill

Diagnose OpenShift Pipelines (Tekton) CI/CD failures by automatically gathering PipelineRun status, failed TaskRun details, step container logs, and related resources.

## Prerequisites

Before running this skill:
1. User is logged into OpenShift cluster
2. User has access to the target namespace
3. OpenShift Pipelines operator is installed on the cluster
4. PipelineRun name is known (or can be identified from recent runs)

### Tekton CRD Access via MCP

Tekton resources are standard Kubernetes CRDs. Use the generic MCP tools with these parameters:

| Resource | kind | apiVersion |
|----------|------|------------|
| PipelineRun | `PipelineRun` | `tekton.dev/v1` |
| TaskRun | `TaskRun` | `tekton.dev/v1` |
| Pipeline | `Pipeline` | `tekton.dev/v1` |
| Task | `Task` | `tekton.dev/v1` |
| ClusterTask | `ClusterTask` | `tekton.dev/v1beta1` |
| EventListener | `EventListener` | `triggers.tekton.dev/v1beta1` |
| TriggerTemplate | `TriggerTemplate` | `triggers.tekton.dev/v1beta1` |
| TriggerBinding | `TriggerBinding` | `triggers.tekton.dev/v1beta1` |

## When to Use This Skill

Use this skill when OpenShift Pipelines (Tekton) fail, hang, or produce unexpected results. It diagnoses PipelineRun failures, TaskRun step errors, workspace/PVC binding issues, and authentication problems by analyzing run status, step container logs, and related resources.

## Critical: Human-in-the-Loop Requirements

See [Human-in-the-Loop Requirements](docs/human-in-the-loop.md) for mandatory checkpoint behavior.

## Workflow

### Step 1: Identify Target PipelineRun

```markdown
## Pipeline Debugging

**Current OpenShift Context:**
- Cluster: [cluster]
- Namespace: [namespace]

Which PipelineRun would you like me to debug?

1. **Specify PipelineRun name** - Enter the PipelineRun name directly
2. **List failed PipelineRuns** - Show recent failed PipelineRuns in current namespace
3. **From Pipeline** - Debug latest run of a specific Pipeline

Select an option or enter a PipelineRun name:
```

**WAIT for user confirmation before proceeding.**

If user selects "List failed PipelineRuns":
Use kubernetes MCP `resources_list` with kind `PipelineRun`, filter by Failed status:

```markdown
## Recent Failed PipelineRuns in [namespace]

| PipelineRun | Pipeline | Status | Started | Duration |
|-------------|----------|--------|---------|----------|
| [run-name] | [pipeline] | Failed | [timestamp] | [duration] |

Which PipelineRun would you like me to debug?
```

**WAIT for user to select a PipelineRun.**

### Step 2: Get PipelineRun Status Overview

Use kubernetes MCP `resources_get` for the PipelineRun:

```markdown
## PipelineRun Status: [pipelinerun-name]

**PipelineRun Info:**
| Field | Value |
|-------|-------|
| Pipeline | [pipeline-name] |
| Status | [Succeeded/Failed/Running/Cancelled] |
| Started | [timestamp] |
| Completed | [timestamp or "Still running"] |
| Duration | [duration] |

**Parameters:**
| Name | Value |
|------|-------|
| [param-name] | [param-value] |

**TaskRun Status:**
| Task | TaskRun | Status | Duration |
|------|---------|--------|----------|
| [task-1] | [taskrun-1] | Succeeded | [duration] |
| [task-2] | [taskrun-2] | **Failed** | [duration] |
| [task-3] | [taskrun-3] | Skipped | - |

**Quick Assessment:**
[Based on status conditions - e.g., "PipelineRun failed because TaskRun 'build' failed at step 'build-push'"]

Continue with failed TaskRun analysis? (yes/no)
```

**WAIT for user confirmation before proceeding.**

### Step 3: Analyze Failed TaskRun(s)

Use kubernetes MCP `resources_get` for each failed TaskRun:

```markdown
## Failed TaskRun: [taskrun-name]

**TaskRun Info:**
| Field | Value |
|-------|-------|
| Task | [task-name] |
| Pod | [taskrun-name]-pod |
| Status | [Failed] |
| Reason | [reason from conditions] |

**Step Status:**
| Step | Container | Status | Exit Code | Reason |
|------|-----------|--------|-----------|--------|
| [step-1] | step-[step-1] | Completed | 0 | - |
| [step-2] | step-[step-2] | **Terminated** | [code] | [reason] |
| [step-3] | step-[step-3] | - | - | Skipped |

**Workspace Bindings:**
| Workspace | Type | Resource | Status |
|-----------|------|----------|--------|
| [shared-workspace] | PVC | [pvc-name] | [Bound/Pending] |
| [output] | EmptyDir | - | OK |

**Issues Found:**
- [Issue 1 - e.g., "Step 'build-push' failed with exit code 1"]

Continue to view step logs? (yes/no)
```

**Note:** Tekton names step containers as `step-<step-name>` in the TaskRun pod. Use this convention with `pods_log`.

**WAIT for user confirmation before proceeding.**

### Step 4: Get TaskRun Pod Logs

Use kubernetes MCP `pods_log` for the TaskRun pod, targeting the failed step container (`step-<step-name>`):

```markdown
## Step Logs: [step-name] (Pod: [taskrun-name]-pod)

**Failed Step Container:** `step-[step-name]`

```
[log output from the failed step container]
```

**Log Analysis:**

**Errors Found:**
- Line [X]: [error description]

Continue to check related resources? (yes/no)
```

**WAIT for user confirmation before proceeding.**

### Step 5: Check Related Resources

Check resources that could cause pipeline failures:

```markdown
## Related Resources Analysis

**ServiceAccount:**
| Field | Value | Status |
|-------|-------|--------|
| Name | [sa-name] | [OK] |
| Image Pull Secrets | [secrets] | [OK/MISSING] |
| Linked Secrets | [secrets] | [OK/MISSING] |

**Workspaces/PVCs:**
| PVC | Status | Access Mode | Storage |
|-----|--------|-------------|---------|
| [pvc-name] | [Bound/Pending] | [RWO/RWX] | [size] |

**Secrets:**
| Secret | Type | Referenced By | Status |
|--------|------|---------------|--------|
| [git-creds] | kubernetes.io/basic-auth | git-clone task | [OK/MISSING] |
| [registry-creds] | kubernetes.io/dockerconfigjson | push task | [OK/MISSING] |

**Pipeline/Task Definitions:**
| Resource | Exists | Issues |
|----------|--------|--------|
| Pipeline [name] | [Yes/No] | [none / param mismatch] |
| Task [name] | [Yes/No] | [none / not found] |

[If triggered by EventListener:]
**EventListener:**
| Field | Value | Status |
|-------|-------|--------|
| Name | [el-name] | [Running/NotRunning] |
| TriggerTemplate | [tt-name] | [OK/MISSING] |
| TriggerBinding | [tb-name] | [OK/MISSING] |

**Issues Found:**
- [Issue 1]

Continue to full diagnosis summary? (yes/no)
```

**WAIT for user confirmation before proceeding.**

### Step 6: Present Diagnosis Summary

```markdown
## Diagnosis Summary: [pipelinerun-name]

### Root Cause

**Primary Issue:** [Categorized root cause]

| Category | Status | Details |
|----------|--------|---------|
| Pipeline Definition | [OK/FAIL] | [details] |
| TaskRun Execution | [OK/FAIL] | [details] |
| Step Container | [OK/FAIL] | [details] |
| Workspace/PVC | [OK/FAIL] | [details] |
| Authentication | [OK/FAIL] | [details] |
| Resources/Quota | [OK/FAIL] | [details] |

### Detailed Findings

**[Category: e.g., Authentication]**
- Problem: [specific problem]
- Evidence: [from logs/events]
- Impact: [effect on pipeline]

### Recommended Actions

1. **[Action 1]** - [description]
   ```bash
   [command to fix]
   ```

2. **[Action 2]** - [description]
   ```bash
   [command to fix]
   ```

### Retry PipelineRun

After fixing the issue:
```bash
# Rerun using the same PipelineRun spec
oc create -f <(oc get pipelinerun [name] -n [namespace] -o json | jq 'del(.metadata.resourceVersion, .metadata.uid, .metadata.creationTimestamp, .status) | .metadata.name = .metadata.name + "-retry"') -n [namespace]

# Or using tkn CLI (if available)
tkn pipeline start [pipeline-name] --use-pipelinerun [pipelinerun-name] -n [namespace]
```

---

Would you like me to:
1. Execute one of the recommended fixes
2. Retry the PipelineRun
3. Debug the TaskRun pod directly (/debug-pod)
4. View Pipeline or Task definition
5. Exit debugging

Select an option:
```

**WAIT for user to select next action.**

## Pipeline Failure Reference

For failure categories, error patterns, and troubleshooting decision trees, see [docs/debugging-patterns.md](docs/debugging-patterns.md) (sections: Pipeline/Tekton Failure Patterns, Common Tekton Error Messages).

## Dependencies

### Required MCP Servers
- `openshift` - Kubernetes/OpenShift resource access for PipelineRuns, TaskRuns, and Tekton CRDs

### Related Skills
- `/debug-pod` - To debug TaskRun pods directly
- `/debug-build` - If the pipeline uses OpenShift Build tasks
- `/debug-network` - If pipeline tasks fail due to network issues
- `/validate-environment` - To verify OpenShift and pipeline operator setup

### Reference Documentation
- [docs/debugging-patterns.md](docs/debugging-patterns.md) - Common error patterns and pipeline troubleshooting trees
- [docs/prerequisites.md](docs/prerequisites.md) - Required tools (oc), cluster access verification
