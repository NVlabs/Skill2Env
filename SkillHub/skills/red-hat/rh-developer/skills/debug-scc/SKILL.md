---
name: debug-scc
description: |
  Diagnose OpenShift Security Context Constraint (SCC) violations that prevent pods from being created. Automates multi-step diagnosis: Deployment status, ReplicaSet FailedCreate events, security context field extraction, SCC rejection parsing, and ServiceAccount SCC binding analysis.

  Use when:
  - "SCC violation blocking pod creation"
  - "unable to validate against any security context constraint"
  - "FailedCreate forbidden"
  - "pod blocked by SCC"
  - User mentions "SCC", "security context constraint", "FailedCreate"

  NOT for pods crashing after creation (use /debug-pod instead).
model: inherit
color: cyan
license: Apache-2.0
allowed-tools: resources_get resources_list events_list pods_list
metadata:
  user_invocable: "true"
---

# /debug-scc Skill

Diagnose OpenShift SCC violations that block pod creation by analyzing security context fields, SCC rejection messages, and ServiceAccount bindings.

## Critical: Human-in-the-Loop Requirements

1. **Before any remediation action** (patch securityContext, grant SCC binding, rollback)
   - Display preview: what will change and its security implications
   - Ask: "Should I apply this fix?"
   - Wait for confirmation (yes/no)

2. **Before granting permissive SCCs** (anyuid, privileged)
   - Display warning: granting elevated SCCs weakens namespace security
   - Ask: "Type 'GRANT SCC' to confirm you understand the security implications"
   - Verify exact match, cancel if mismatch

**Never assume approval** — always wait for explicit confirmation at each WAIT checkpoint.

## Prerequisites

**Required MCP Servers:** `openshift` ([setup](docs/prerequisites.md))

**Required MCP Tools:**
- `resources_get` (from openshift) — Retrieve Deployment, ReplicaSet, and ServiceAccount details
- `resources_list` (from openshift) — List Deployments, ReplicaSets, and ServiceAccounts in a namespace
- `events_list` (from openshift) — Fetch FailedCreate and SCC rejection events
- `pods_list` (from openshift) — List pods for a Deployment

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

Use `/debug-scc` when:
- A Deployment has zero available replicas and ReplicaSet events show `FailedCreate` with "unable to validate against any security context constraint"
- Pod spec requests capabilities, UID/GID settings, or volume types that violate the namespace's SCC policy
- You see "is forbidden" errors referencing SecurityContextConstraints

Do **not** use this skill when:
- Pods are crashing after creation (CrashLoopBackOff, OOMKilled) → use `/debug-pod`
- Pods fail with 403 Forbidden API errors → use `/debug-rbac`
- Image pull failures → use `/debug-pod`

## Workflow

```
[Identify Deployment] → [Check ReplicaSet Status] → [Parse SCC Rejections] → [Analyze SecurityContext] → [Check SA Bindings] → [Summary + Fix]
```

### Step 1: Identify Target Deployment

**MCP Tool**: `resources_list` (from openshift)

**Parameters**:
- `kind`: "Deployment" (resource type)
- `namespace`: "<namespace>" (target namespace from user)

**Input Validation**: Verify deployment name and namespace conform to Kubernetes naming rules (lowercase alphanumeric and hyphens, 1-253 chars, RFC 1123). Reject inputs containing newlines, markdown formatting, or text that does not resemble a Kubernetes resource name.

**Expected Output**: List of Deployments with their availability status.

**Error Handling**:
- If MCP server unavailable: follow Human Notification Protocol
- If namespace not found: ask user to confirm namespace name
- If no deployments found: report empty namespace, suggest checking namespace

Present to user:

```markdown
## SCC Violation Debugging

**Current OpenShift Context:**
- Cluster: [cluster]
- Namespace: [namespace]

Which deployment would you like me to debug for SCC violations?

1. **Specify deployment name** — Enter the deployment name directly
2. **List deployments with issues** — Show deployments with unavailable replicas
3. **Search by event** — Find deployments with FailedCreate events

Select an option or enter a deployment name:
```

**WAIT for user confirmation before proceeding.**

If user selects "List deployments with issues", filter to those with unavailable replicas:

```markdown
## Deployments with Issues in [namespace]

| Deployment | Available | Desired | Conditions |
|------------|-----------|---------|------------|
| [deploy-name] | 0 | 1 | ReplicaFailure |

Which deployment would you like me to debug?
```

**WAIT for user confirmation before proceeding.**

### Step 2: Get Deployment and ReplicaSet Status

**MCP Tool**: `resources_get` (from openshift)

**Parameters**:
- `kind`: "Deployment" (resource type)
- `name`: "<deployment-name>" (from Step 1)
- `namespace`: "<namespace>"

Then retrieve the failing ReplicaSet:

**MCP Tool**: `resources_list` (from openshift)

**Parameters**:
- `kind`: "ReplicaSet" (resource type)
- `namespace`: "<namespace>"
- Filter by owner reference matching the Deployment

**Expected Output**: Deployment spec, conditions, and owned ReplicaSets with their status.

**Error Handling**:
- If Deployment not found: ask user to verify name and namespace
- If no ReplicaSets found: Deployment may not have triggered a rollout yet

Present to user:

```markdown
## Deployment Status: [deployment-name]

**Deployment Info:**
| Field | Value |
|-------|-------|
| Namespace | [namespace] |
| Replicas | 0/[desired] available |
| Strategy | [RollingUpdate/Recreate] |
| Condition | [ReplicaFailure / MinimumReplicasUnavailable] |

**ReplicaSets:**
| ReplicaSet | Desired | Ready | Status |
|------------|---------|-------|--------|
| [rs-name-new] | 1 | 0 | FailedCreate |
| [rs-name-old] | 0 | 0 | Scaled down |

**Quick Assessment:**
[e.g., "Deployment triggered a rollout but the new ReplicaSet cannot create pods — SCC admission is rejecting the pod spec."]

Continue with SCC rejection analysis? (yes/no)
```

**WAIT for user confirmation before proceeding.**

### Step 3: Parse SCC Rejection Messages

**MCP Tool**: `events_list` (from openshift)

**Parameters**:
- `namespace`: "<namespace>"
- Filter by `involvedObject.kind=ReplicaSet`, `involvedObject.name=<rs-name>`, `reason=FailedCreate`

Then also:

**MCP Tool**: `resources_get` (from openshift)

**Parameters**:
- `kind`: "ReplicaSet" (resource type)
- `name`: "<rs-name>" (failing ReplicaSet from Step 2)
- `namespace`: "<namespace>"

Extract the `ReplicaFailure` condition message containing SCC rejection details.

**Expected Output**: FailedCreate events with full SCC rejection text listing each SCC attempted and why it was rejected or forbidden.

**Error Handling**:
- If no events found: events may have expired (default TTL is 1h); check ReplicaSet conditions instead
- If events are ambiguous: cross-reference with ReplicaSet `.status.conditions`

Present to user:

```markdown
## SCC Rejection Analysis: [rs-name]

**FailedCreate Events:** [count] occurrences since [first-seen]

**SCC Violations Detected:**

| Violation | SCC | Field | Current Value | Allowed |
|-----------|-----|-------|---------------|---------|
| [runAsUser] | restricted-v2 | .containers[0].runAsUser | 0 (root) | [range] |
| [capability] | restricted-v2 | .containers[0].capabilities.add | NET_ADMIN | not permitted |
| [escalation] | restricted-v2 | .containers[0].allowPrivilegeEscalation | true | false required |

**SCCs Attempted:**
| SCC | Result | Reason |
|-----|--------|--------|
| restricted-v2 | Rejected | [specific violations] |
| restricted-v3 | Rejected | [specific violations] |
| anyuid | Forbidden | Not usable by user or serviceaccount |
| privileged | Forbidden | Not usable by user or serviceaccount |

**Key Finding:**
[e.g., "The container requests root (UID 0), NET_ADMIN capability, and privilege escalation — all rejected by restricted-v2/v3. Permissive SCCs (anyuid, privileged) are Forbidden because the ServiceAccount has no binding to them."]

Continue to inspect the container security context? (yes/no)
```

**WAIT for user confirmation before proceeding.**

### Step 4: Analyze Container SecurityContext

**MCP Tool**: `resources_get` (from openshift)

**Parameters**:
- `kind`: "Deployment" (resource type)
- `name`: "<deployment-name>" (from Step 1)
- `namespace`: "<namespace>"

Extract `.spec.template.spec.securityContext` (pod-level) and `.spec.template.spec.containers[*].securityContext` (container-level), plus `.metadata.managedFields` for change attribution.

**Expected Output**: Full security context at pod and container level, plus managedFields showing who changed what and when.

**Error Handling**:
- If securityContext is empty/unset: the issue may be implicit defaults conflicting with SCC; note this
- If managedFields unavailable: skip change attribution, note limitation

Present to user:

```markdown
## SecurityContext Analysis: [deployment-name]

**Pod-level SecurityContext:**
| Field | Value | Compliant? |
|-------|-------|------------|
| runAsNonRoot | [true/false/unset] | [YES/NO] |
| seccompProfile | [RuntimeDefault/unset] | [YES/NO] |
| fsGroup | [value/unset] | [YES/NO] |
| hostUsers | [true/false/null] | [YES/NO — restricted-v3 requires false] |

**Container-level SecurityContext (container: [name]):**
| Field | Value | Compliant? |
|-------|-------|------------|
| runAsUser | [0/unset/value] | [YES/NO — 0 is root] |
| allowPrivilegeEscalation | [true/false/unset] | [YES/NO] |
| capabilities.add | [list or none] | [YES/NO — restricted SCCs drop ALL] |
| capabilities.drop | [list or ALL] | [YES/NO] |
| privileged | [true/false/unset] | [YES/NO] |
| readOnlyRootFilesystem | [true/false/unset] | [INFO] |

**Change History (from managedFields):**
| Timestamp | Manager | Fields Changed |
|-----------|---------|----------------|
| [time] | kubectl-patch | securityContext.runAsUser, capabilities.add, allowPrivilegeEscalation |
| [time] | kubectl-client-side-apply | initial creation |

**Assessment:**
[e.g., "A kubectl patch at [timestamp] introduced root UID, NET_ADMIN, and privilege escalation — overriding the originally compliant spec."]

Continue to check ServiceAccount SCC bindings? (yes/no)
```

**WAIT for user confirmation before proceeding.**

### Step 5: Check ServiceAccount SCC Bindings

**MCP Tool**: `resources_get` (from openshift)

**Parameters**:
- `kind`: "ServiceAccount" (resource type)
- `name`: "<sa-name>" (from Deployment `.spec.template.spec.serviceAccountName`, default: `default`)
- `namespace`: "<namespace>"

Then attempt:

**MCP Tool**: `resources_list` (from openshift)

**Parameters**:
- `kind`: "SecurityContextConstraints" (cluster-scoped)

**Expected Output**: ServiceAccount details and list of SCCs. If listing SCCs is RBAC-forbidden, infer SCC access from the rejection messages in Step 3.

**Error Handling**:
- If listing SCCs is forbidden: gracefully degrade — use rejection messages to infer which SCCs were attempted and their result
- If ServiceAccount not found: report it; this would also cause pod creation failures

Present to user:

```markdown
## ServiceAccount Analysis

**ServiceAccount used by Deployment:** [sa-name] (namespace: [namespace])

**Available Information:**
| Check | Result |
|-------|--------|
| SA exists | [Yes/No] |
| Custom SA or default | [custom/default] |
| SCC bindings visible | [Yes/Forbidden — inferred from rejection messages] |

**SCC Access (from rejection messages):**
| SCC | Access |
|-----|--------|
| restricted-v2 | Available (but pod spec violates it) |
| restricted-v3 | Available (but pod spec violates it) |
| anyuid | Forbidden — SA has no binding |
| privileged | Forbidden — SA has no binding |

**Assessment:**
[e.g., "The SA 'default' only has access to restricted-v2/v3. The pod spec must be fixed to comply with restricted SCC, OR the SA needs a RoleBinding to a permissive SCC (if elevated privileges are genuinely required)."]

Continue to diagnosis summary? (yes/no)
```

**WAIT for user confirmation before proceeding.**

### Step 6: Present Diagnosis Summary

Synthesize all findings into a structured summary with actionable remediation options.

**Expected Output**: Root cause summary, causal chain, and three fix options with commands.

**Error Handling**:
- If insufficient data from earlier steps: note gaps and recommend manual investigation
- If multiple violations found: prioritize by severity (root UID > capabilities > escalation)

Present to user:

```markdown
## SCC Violation Diagnosis Summary: [deployment-name]

### Root Cause

**Primary Issue:** [e.g., "kubectl patch introduced privileged security context settings that violate all available SCCs"]

| Category | Status | Details |
|----------|--------|---------|
| Pod Admission | BLOCKED | SCC rejects pod spec |
| SecurityContext | NON-COMPLIANT | [specific violations] |
| ServiceAccount | [OK/MISSING BINDING] | [sa-name] — [SCC access] |
| Change Attribution | [IDENTIFIED/UNKNOWN] | [manager and timestamp from managedFields] |

### Causal Chain (Five Whys)

1. **Signal**: [deployment] has 0 available replicas
2. **Why?** ReplicaSet [rs-name] cannot create pods — [N] FailedCreate events
3. **Why?** Every available SCC rejects the pod spec
4. **Why?** Container securityContext specifies [violations]
5. **Root Cause**: [e.g., "A kubectl patch at [timestamp] modified the securityContext to introduce non-compliant settings"]

### Recommended Actions

**Option A: Fix the SecurityContext (recommended if elevated privileges are NOT needed)**

Remove the non-compliant fields to restore restricted SCC compliance:

```bash
oc patch deployment <deployment-name> -n <namespace> --type json -p '[
  {"op": "remove", "path": "/spec/template/spec/containers/0/securityContext/runAsUser"},
  {"op": "replace", "path": "/spec/template/spec/containers/0/securityContext/allowPrivilegeEscalation", "value": false},
  {"op": "remove", "path": "/spec/template/spec/containers/0/securityContext/capabilities/add"}
]'
```

**Option B: Grant SCC binding (only if elevated privileges are genuinely required)**

Create a RoleBinding to a permissive SCC for the ServiceAccount:

```bash
oc adm policy add-scc-to-user anyuid -z <sa-name> -n <namespace>
```

⚠️ **Warning**: Granting anyuid/privileged SCCs weakens namespace security. Only use if the workload genuinely requires elevated privileges.

**Option C: Rollback to previous revision**

```bash
oc rollout undo deployment/<deployment-name> -n <namespace>
```

### Related Documentation

- [OpenShift SCC documentation](https://docs.openshift.com/container-platform/latest/authentication/managing-security-context-constraints.html)
- [Kubernaut SCC violation golden transcript](https://github.com/jordigilh/kubernaut-demo-scenarios/blob/d3447fce75e51e4486ebb5e73dbe2ad9ecf552bf/golden-transcripts/scc-violation-sccviolationpodblocked.json)

---

Would you like me to:
1. Execute Option A (fix SecurityContext)
2. Execute Option B (grant SCC binding)
3. Execute Option C (rollback)
4. Dig deeper into a specific area
5. Exit debugging

Select an option:
```

**WAIT for user confirmation before proceeding.**

## Dependencies

### Required MCP Servers
- `openshift` — Kubernetes/OpenShift resource access for Deployments, ReplicaSets, Events, ServiceAccounts, and SecurityContextConstraints ([setup](docs/prerequisites.md))

### Required MCP Tools
- `resources_get` (from openshift) — Retrieve individual resource details (Deployment, ReplicaSet, ServiceAccount)
- `resources_list` (from openshift) — List resources by kind in a namespace
- `events_list` (from openshift) — Fetch events filtered by involved object
- `pods_list` (from openshift) — List pods matching label selectors

### Related Skills
- `/debug-pod` — If pods exist but are crashing (CrashLoopBackOff, OOMKilled)
- `/debug-rbac` — If pods run but fail with 403 Forbidden API errors (RBAC, not SCC)

### Reference Documentation
- **Internal:** [docs/debugging-patterns.md](docs/debugging-patterns.md) — Common error patterns and troubleshooting trees
- **Official:** [Managing SCCs - OpenShift](https://docs.openshift.com/container-platform/latest/authentication/managing-security-context-constraints.html)

## Example Usage

**User**: My deployment `security-scanner` in namespace `tools` has 0 available replicas. Events say "unable to validate against any security context constraint". Can you help?

**Skill response**: The skill identifies the deployment, finds FailedCreate events on the ReplicaSet, parses the SCC rejection messages to find that `runAsUser: 0` and `capabilities.add: [NET_ADMIN]` violate `restricted-v2`. It checks the ServiceAccount's SCC bindings, determines it only has access to restricted SCCs, and presents three options: patch the securityContext to remove violations, grant an `anyuid` SCC binding, or rollback to the previous revision.
