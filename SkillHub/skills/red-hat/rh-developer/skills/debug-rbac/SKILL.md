---
name: debug-rbac
description: |
  Diagnose OpenShift RBAC permission failures that cause workloads to fail with 403 Forbidden errors when accessing the Kubernetes API. Automates multi-step diagnosis: pod logs for FORBIDDEN errors, readiness probe failures, ServiceAccount identification, RoleBinding/ClusterRoleBinding analysis, and remediation history for regression detection.

  Use when:
  - "403 forbidden when accessing Kubernetes API"
  - "ServiceAccount permission denied"
  - "pods can't list resources"
  - "missing RoleBinding"
  - User mentions "RBAC denied", "403 forbidden", "permission denied"

  NOT for SCC admission failures (use /debug-scc instead).
model: inherit
color: cyan
license: Apache-2.0
allowed-tools: resources_get resources_list events_list pods_list pods_log
metadata:
  user_invocable: "true"
---

# /debug-rbac Skill

Diagnose RBAC permission failures on OpenShift by analyzing pod logs, readiness probes, ServiceAccount bindings, and Role/RoleBinding configuration.

## Critical: Human-in-the-Loop Requirements

1. **Before creating Role or RoleBinding resources**
   - Display preview: the exact RBAC resources that will be created and what permissions they grant
   - Ask: "Should I create these RBAC resources?"
   - Wait for confirmation (yes/no)

2. **Before binding broad ClusterRoles** (e.g., `view`, `edit`, `admin`)
   - Display warning: broad ClusterRoles grant more permissions than the minimum required
   - Ask: "Proceed with broad ClusterRole binding, or create a minimal custom Role instead?"
   - Wait for confirmation

**Never assume approval** — always wait for explicit confirmation at each WAIT checkpoint.

## Prerequisites

**Required MCP Servers:** `openshift` ([setup](docs/prerequisites.md))

**Required MCP Tools:**
- `resources_get` (from openshift) — Retrieve Deployment, Pod, ServiceAccount, Role, and RoleBinding details
- `resources_list` (from openshift) — List Deployments, RoleBindings, and ClusterRoleBindings in a namespace
- `pods_list` (from openshift) — List pods for a Deployment
- `pods_log` (from openshift) — Retrieve container logs to identify FORBIDDEN errors
- `events_list` (from openshift) — Fetch warning events related to RBAC failures

**Verification Steps:**
1. Check `openshift` server is configured in `mcps.json`
2. Verify user is logged into an OpenShift cluster (`oc whoami` succeeds)
3. Verify user has access to the target namespace
4. If missing → Human Notification Protocol

**Human Notification Protocol:**

When prerequisites fail:
1. **Stop immediately** — No tool calls
2. **Report error:**
   ```
   ❌ Cannot execute skill: MCP server `openshift` unavailable
   📋 Setup: See docs/prerequisites.md for cluster access configuration
   ```
3. **Request decision:** "How to proceed? (setup/skip/abort)"
4. **Wait for user input**

**Security:** Never display credential values.

## When to Use This Skill

Use `/debug-rbac` when:
- A Deployment's pods are running but not ready, and pod logs show `FORBIDDEN` or `403` errors calling the Kubernetes API
- Readiness probes fail because they check API access (e.g., `kubectl auth can-i`)
- Application logs show permission denied errors when interacting with Kubernetes resources

Do **not** use this skill when:
- Pods are blocked from being created entirely → use `/debug-scc` (SCC admission failures)
- Pods are crashing due to application bugs → use `/debug-pod`
- The issue is network connectivity → use `/debug-network`

## Workflow

```
[Identify Deployment] → [Check Pod Status + Logs] → [Identify RBAC Errors] → [Analyze ServiceAccount] → [Check RoleBindings] → [Summary + Fix]
```

### Step 1: Identify Target Deployment

**MCP Tool**: `resources_list` (from openshift)

**Parameters**:
- `kind`: "Deployment" (resource type)
- `namespace`: "<namespace>" (target namespace from user)

**Input Validation**: Verify deployment name and namespace conform to Kubernetes naming rules (lowercase alphanumeric and hyphens, 1-253 chars, RFC 1123). Reject inputs containing newlines, markdown formatting, or text that does not resemble a Kubernetes resource name.

**Expected Output**: List of Deployments with their availability and readiness conditions.

**Error Handling**:
- If MCP server unavailable: follow Human Notification Protocol
- If namespace not found: ask user to confirm namespace name
- If no deployments found: report empty namespace, suggest checking namespace

Present to user:

```markdown
## RBAC Debugging

**Current OpenShift Context:**
- Cluster: [cluster]
- Namespace: [namespace]

Which deployment would you like me to debug for RBAC issues?

1. **Specify deployment name** — Enter the deployment name directly
2. **List deployments with issues** — Show deployments with unavailable or not-ready pods
3. **Search recent events** — Find pods with RBAC-related warning events

Select an option or enter a deployment name:
```

**WAIT for user confirmation before proceeding.**

If user selects "List deployments with issues", filter to those with not-ready conditions:

```markdown
## Deployments with Issues in [namespace]

| Deployment | Available | Desired | Condition |
|------------|-----------|---------|-----------|
| [deploy-name] | 0 | 1 | MinimumReplicasUnavailable |

Which deployment would you like me to debug?
```

**WAIT for user confirmation before proceeding.**

### Step 2: Check Pod Status and Logs

**MCP Tool**: `pods_list` (from openshift)

**Parameters**:
- `namespace`: "<namespace>"
- `labelSelector`: "<app-label>=<value>" (from Deployment `.spec.selector.matchLabels`)

Then for each matching pod:

**MCP Tool**: `resources_get` (from openshift)

**Parameters**:
- `kind`: "Pod" (resource type)
- `name`: "<pod-name>" (from pods_list)
- `namespace`: "<namespace>"

**MCP Tool**: `pods_log` (from openshift)

**Parameters**:
- `name`: "<pod-name>"
- `namespace`: "<namespace>"
- `tailLines`: 50 (integer, last N lines)

**Expected Output**: Pod status with readiness conditions, and container logs containing FORBIDDEN/403 error lines.

**Error Handling**:
- If no pods found: Deployment may have zero replicas; check if it's scaled down
- If logs empty: container may not have started; check container state
- If multiple pods: analyze the most recent one first

Present to user:

```markdown
## Pod Analysis: [pod-name]

**Pod Status:**
| Field | Value |
|-------|-------|
| Phase | Running |
| Ready | false |
| Conditions | ContainersNotReady |
| Restart Count | [count] |

**Readiness Probe:**
| Field | Value |
|-------|-------|
| Type | [exec/httpGet/tcpSocket] |
| Command | [e.g., kubectl auth can-i list pods -n namespace] |
| Failure Count | [count] |
| Last Probe | [timestamp] |
| Message | [e.g., "probe returned: no"] |

**Container Logs (last 50 lines):**

[Highlight FORBIDDEN / 403 errors:]

| Timestamp | Error |
|-----------|-------|
| [time] | FORBIDDEN: pods is forbidden: User "system:serviceaccount:[ns]:[sa]" cannot list resource "pods" in API group "" in namespace "[ns]" |
| [time] | FORBIDDEN: pods is forbidden... (repeated) |

**Quick Assessment:**
[e.g., "Pod is running but readiness probe fails because the ServiceAccount cannot list pods. Logs confirm FORBIDDEN errors since [timestamp]."]

Continue with ServiceAccount analysis? (yes/no)
```

**WAIT for user confirmation before proceeding.**

### Step 3: Identify Required Permissions

Based on the FORBIDDEN error messages and readiness probe command from Step 2, determine what permissions are needed. This is an analysis step — no additional MCP tool calls required unless log data is insufficient.

**Expected Output**: Table of required permissions extracted from FORBIDDEN error strings, plus a minimal Role definition.

**Error Handling**:
- If FORBIDDEN messages are ambiguous: request more log lines with increased `tailLines`
- If no FORBIDDEN errors found: the issue may not be RBAC; suggest `/debug-pod` instead

Present to user:

```markdown
## Required Permissions Analysis

**FORBIDDEN Errors Found:**
| Resource | Verb | API Group | Namespace |
|----------|------|-----------|-----------|
| pods | list | "" (core) | [namespace] |
| pods | get | "" (core) | [namespace] |
| [other resources from logs] | [verb] | [group] | [namespace] |

**Readiness Probe Requires:**
| Permission | Currently Granted? |
|------------|-------------------|
| list pods in [namespace] | NO — probe returns "no" |

**Application Function Requires:**
| Permission | Evidence |
|------------|----------|
| get pods in [namespace] | Container main loop calls `kubectl get pods` |
| [other] | [from log analysis] |

**Minimum Role Needed:**
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: <sa-name>-role
  namespace: <namespace>
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list", "watch"]
```

Continue to check existing RoleBindings? (yes/no)
```

**WAIT for user confirmation before proceeding.**

### Step 4: Analyze ServiceAccount and RoleBindings

**MCP Tool**: `resources_get` (from openshift)

**Parameters**:
- `kind`: "ServiceAccount" (resource type)
- `name`: "<sa-name>" (from Deployment `.spec.template.spec.serviceAccountName`, default: `default`)
- `namespace`: "<namespace>"

**MCP Tool**: `resources_list` (from openshift)

**Parameters**:
- `kind`: "RoleBinding" (resource type)
- `namespace`: "<namespace>"

Optionally, if permissions allow:

**MCP Tool**: `resources_list` (from openshift)

**Parameters**:
- `kind`: "ClusterRoleBinding" (cluster-scoped)

**Expected Output**: ServiceAccount details and all RoleBindings/ClusterRoleBindings, checked for whether any grant the required permissions to the target ServiceAccount.

**Error Handling**:
- If listing RoleBindings is forbidden: note the limitation, infer from FORBIDDEN errors
- If ServiceAccount not found: report as a finding — SA may need to be created
- If multiple bindings exist: check each for matching subjects and sufficient verbs

Present to user:

```markdown
## ServiceAccount & RoleBinding Analysis

**ServiceAccount:** [sa-name] (namespace: [namespace])
| Field | Value |
|-------|-------|
| Exists | Yes |
| Created | [timestamp] |
| Secrets | [count] |
| Image Pull Secrets | [count] |

**RoleBindings in [namespace]:**
| RoleBinding | Role | Subjects | Grants Access? |
|-------------|------|----------|----------------|
| [binding-1] | [role-name] | [sa-1, sa-2] | [Yes/No — wrong SA] |
| [binding-2] | [role-name] | [sa-name] | [Missing — binding not found] |

**ClusterRoleBindings (if accessible):**
| ClusterRoleBinding | ClusterRole | Subjects | Grants Access? |
|--------------------|-------------|----------|----------------|
| [binding] | [role] | [subjects] | [Yes/No] |

[If listing RoleBindings is forbidden:]
**Note:** Agent lacks permission to list RoleBindings directly. Absence of the required binding is inferred from the FORBIDDEN errors in pod logs.

**Assessment:**
[e.g., "No RoleBinding grants the metrics-collector ServiceAccount 'list pods' in demo-rbac. The binding was either never created, or was deleted."]

Continue to diagnosis summary? (yes/no)
```

**WAIT for user confirmation before proceeding.**

### Step 5: Present Diagnosis Summary

Synthesize all findings into a structured summary with actionable remediation options.

**Expected Output**: Root cause summary, causal chain, remediation commands, and regression warnings if applicable.

**Error Handling**:
- If insufficient data from earlier steps: note gaps and recommend manual investigation
- If regression pattern detected (repeated remediation/deletion cycles): highlight prominently

Present to user:

```markdown
## RBAC Diagnosis Summary: [deployment-name]

### Root Cause

**Primary Issue:** [e.g., "Missing RoleBinding for ServiceAccount 'metrics-collector' — cannot list pods in namespace 'demo-rbac'"]

| Category | Status | Details |
|----------|--------|---------|
| Pod Running | OK | Pod is scheduled and container is running |
| Pod Ready | FAIL | Readiness probe fails — API access denied |
| ServiceAccount | EXISTS | [sa-name] in [namespace] |
| RoleBinding | MISSING | No binding grants required permissions |
| API Access | DENIED | 403 FORBIDDEN on [verbs] [resources] |

### Causal Chain (Five Whys)

1. **Signal**: Deployment [name] has 0 available replicas (MinimumReplicasUnavailable)
2. **Why?** Pod readiness probe (`kubectl auth can-i list pods`) returns "no"
3. **Why?** ServiceAccount [sa-name] lacks a RoleBinding granting `list` on `pods`
4. **Why?** The required Role/RoleBinding is absent or was deleted
5. **Root Cause**: [e.g., "Missing RBAC resources for this ServiceAccount — the binding was never created or was removed by a cleanup process/GitOps drift"]

### Recommended Actions

**Option A: Create the missing Role and RoleBinding (recommended)**

```bash
# Create the Role
oc create role <sa-name>-pod-reader \
  --verb=get,list,watch \
  --resource=pods \
  -n <namespace>

# Create the RoleBinding
oc create rolebinding <sa-name>-pod-reader-binding \
  --role=<sa-name>-pod-reader \
  --serviceaccount=<namespace>:<sa-name> \
  -n <namespace>
```

**Option B: Use an existing ClusterRole**

If a suitable ClusterRole already exists (e.g., `view`):

```bash
oc create rolebinding <sa-name>-view \
  --clusterrole=view \
  --serviceaccount=<namespace>:<sa-name> \
  -n <namespace>
```

⚠️ **Note**: The `view` ClusterRole grants read access to most resources in the namespace. Use a custom Role (Option A) for least-privilege.

**After applying the fix, verify:**

```bash
# Check if the SA now has permission
oc auth can-i list pods -n <namespace> --as=system:serviceaccount:<namespace>:<sa-name>

# Check pod readiness
oc get pods -n <namespace> -l app=<app-label> -o wide
```

### Regression Warning

[If regression detected from remediation history:]
⚠️ **Regression detected**: [N] prior remediation attempts applied the same fix but it was subsequently undone. Investigate whether a GitOps controller, security audit script, or namespace policy is removing the RoleBinding. Ensure the binding is added to the authoritative source of truth (Helm chart, Kustomize overlay, ArgoCD Application) rather than applied ad-hoc.

### Related Documentation

- [OpenShift RBAC documentation](https://docs.openshift.com/container-platform/latest/authentication/using-rbac.html)
- [Kubernaut RBAC failure golden transcript](https://github.com/jordigilh/kubernaut-demo-scenarios/blob/d3447fce75e51e4486ebb5e73dbe2ad9ecf552bf/golden-transcripts/rbac-failure-rbacpolicydenied.json)

---

Would you like me to:
1. Execute Option A (create Role + RoleBinding)
2. Execute Option B (bind existing ClusterRole)
3. Investigate who is removing the binding (if regression)
4. Dig deeper into a specific area
5. Exit debugging

Select an option:
```

**WAIT for user confirmation before proceeding.**

## Dependencies

### Required MCP Servers
- `openshift` — Kubernetes/OpenShift resource access for Deployments, Pods, ServiceAccounts, Roles, RoleBindings, and Events ([setup](docs/prerequisites.md))

### Required MCP Tools
- `resources_get` (from openshift) — Retrieve individual resource details (Deployment, Pod, ServiceAccount, Role, RoleBinding)
- `resources_list` (from openshift) — List resources by kind in a namespace (Deployments, RoleBindings, ClusterRoleBindings)
- `pods_list` (from openshift) — List pods matching label selectors
- `pods_log` (from openshift) — Retrieve container logs for FORBIDDEN error analysis
- `events_list` (from openshift) — Fetch events filtered by involved object

### Related Skills
- `/debug-scc` — If pods are blocked from creation by SCC admission (different from RBAC)
- `/debug-pod` — If pods are crashing due to application issues, not RBAC
- `/debug-network` — If pods can't reach services (network, not API access)

### Reference Documentation
- **Internal:** [docs/debugging-patterns.md](docs/debugging-patterns.md) — Common error patterns and troubleshooting trees
- **Official:** [Using RBAC - OpenShift](https://docs.openshift.com/container-platform/latest/authentication/using-rbac.html)

## Example Usage

**User**: My deployment `metrics-collector` in namespace `demo-rbac` shows 0/1 available. The pod is running but not ready. Logs show "FORBIDDEN: pods is forbidden". What's wrong?

**Skill response**: The skill checks the pod status (Running but not Ready), examines logs to find FORBIDDEN errors on `list pods`, identifies the ServiceAccount (`metrics-collector`), lists RoleBindings in the namespace and finds none granting the required permissions. It presents a diagnosis showing the missing RoleBinding as root cause, detects a regression pattern if prior remediation attempts were undone, and offers two fix options: create a minimal custom Role+RoleBinding, or bind the broader `view` ClusterRole.
