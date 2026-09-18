---
name: debug-pod
description: |
  Diagnose pod failures on OpenShift including CrashLoopBackOff, ImagePullBackOff, OOMKilled, and pending pods. Automates multi-step diagnosis: pod status, events, logs (current + previous), and resource constraint analysis. Use this skill when pods are not running, restarting frequently, or stuck in non-ready states. Triggers on /debug-pod command or phrases like "my pod is crashing", "pod won't start", "CrashLoopBackOff", "ImagePullBackOff", "OOMKilled".
model: inherit
color: cyan
license: Apache-2.0
allowed-tools: pods_list resources_get events_list pods_log
metadata:
  user_invocable: "true"
---

# /debug-pod Skill

Diagnose pod failures on OpenShift by automatically gathering status, events, logs, and resource information.

## Prerequisites

Before running this skill:
1. User is logged into OpenShift cluster
2. User has access to the target namespace
3. Pod or deployment name is known (or can be identified from recent deployments)

## When to Use This Skill

Use this skill when pods are not running, restarting frequently, or stuck in non-ready states such as CrashLoopBackOff, ImagePullBackOff, OOMKilled, or Pending. It automates gathering pod status, events, logs, and resource constraints to identify the root cause.

## Critical: Human-in-the-Loop Requirements

See [Human-in-the-Loop Requirements](docs/human-in-the-loop.md) for mandatory checkpoint behavior.

## Workflow

### Step 1: Identify Target Pod

```markdown
## Pod Debugging

**Current OpenShift Context:**
- Cluster: [cluster]
- Namespace: [namespace]

Which pod would you like me to debug?

1. **Specify pod name** - Enter the pod name directly
2. **List failing pods** - Show pods with issues in current namespace
3. **From deployment** - Debug pods from a specific deployment

Select an option or enter a pod name:
```

**WAIT for user confirmation before proceeding.**

If user selects "List failing pods":
Use kubernetes MCP `pods_list` with namespace, then filter to show pods NOT in Running/Succeeded state:

```markdown
## Pods with Issues in [namespace]

| Pod | Status | Restarts | Age | Reason |
|-----|--------|----------|-----|--------|
| [pod-name] | CrashLoopBackOff | 5 | 10m | [waiting reason] |
| [pod-name-2] | ImagePullBackOff | 0 | 3m | [waiting reason] |
| [pod-name-3] | Pending | 0 | 15m | [conditions] |

Which pod would you like me to debug?
```

**WAIT for user confirmation before proceeding.**

### Step 2: Get Pod Status Overview

Use kubernetes MCP `resources_get` to get pod details:

```markdown
## Pod Status: [pod-name]

**Basic Info:**
| Field | Value |
|-------|-------|
| Namespace | [namespace] |
| Node | [node-name or "Not scheduled"] |
| Status | [phase: Pending/Running/Failed/Succeeded] |
| IP | [pod-ip or "Not assigned"] |
| Created | [timestamp] |

**Container Status:**
| Container | State | Ready | Restarts | Exit Code | Reason |
|-----------|-------|-------|----------|-----------|--------|
| [container-name] | [Waiting/Running/Terminated] | [true/false] | [count] | [code or N/A] | [reason] |

**Quick Assessment:**
[Based on status, provide initial assessment - e.g., "Pod is in CrashLoopBackOff - container keeps crashing after startup"]

Continue with detailed analysis? (yes/no)
```

**WAIT for user confirmation before proceeding.**

### Step 3: Analyze Events

Use kubernetes MCP `events_list` filtered by pod:

```markdown
## Recent Events for [pod-name]

| Time | Type | Reason | Message |
|------|------|--------|---------|
| [timestamp] | [Normal/Warning] | [reason] | [message] |
| [timestamp] | [Normal/Warning] | [reason] | [message] |
| ... |

**Event Analysis:**

[Analyze events and identify key issues:]

**Issues Found:**
- [Issue 1 - e.g., "FailedScheduling: 0/3 nodes available - insufficient memory"]
- [Issue 2 - e.g., "ImagePullBackOff: unauthorized - check image pull secrets"]

Continue to view container logs? (yes/no)
```

**WAIT for user confirmation before proceeding.**

### Step 4: Get Container Logs

Use kubernetes MCP `pods_log` for current and previous container:

```markdown
## Container Logs: [container-name]

**Current Container Logs** (last 50 lines):
```
[log output]
```

[If container has restarted, also show previous logs:]

**Previous Container Logs** (before last restart):
```
[log output from --previous]
```

**Log Analysis:**

[Analyze logs and identify errors:]

**Errors Found:**
- Line [X]: [error description - e.g., "Connection refused to database on port 5432"]
- Line [Y]: [error description - e.g., "Out of memory - heap allocation failed"]

Continue to analyze resource constraints? (yes/no)
```

**WAIT for user confirmation before proceeding.**

### Step 5: Analyze Resource Constraints

Check resource requests, limits, and actual usage:

```markdown
## Resource Analysis: [pod-name]

**Container: [container-name]**

| Resource | Request | Limit | Status |
|----------|---------|-------|--------|
| Memory | [128Mi] | [512Mi] | [OK / WARNING: OOMKilled] |
| CPU | [100m] | [500m] | [OK / WARNING: throttled] |

**Node Resources (if scheduled):**
| Resource | Allocatable | Allocated | Available |
|----------|-------------|-----------|-----------|
| Memory | [8Gi] | [7.5Gi] | [512Mi] |
| CPU | [4000m] | [3800m] | [200m] |

**Resource Issues:**
- [Issue 1 - e.g., "Container was OOMKilled - memory limit too low for application"]
- [Issue 2 - e.g., "Pod cannot be scheduled - no nodes have 2Gi available memory"]

Continue to full diagnosis summary? (yes/no)
```

**WAIT for user confirmation before proceeding.**

### Step 6: Present Diagnosis Summary

```markdown
## Diagnosis Summary: [pod-name]

### Root Cause

**Primary Issue:** [Categorized root cause]

| Category | Status | Details |
|----------|--------|---------|
| Container Start | [OK/FAIL] | [details] |
| Image Pull | [OK/FAIL] | [details] |
| Resource Scheduling | [OK/FAIL] | [details] |
| Application Health | [OK/FAIL] | [details] |
| Volume Mounts | [OK/FAIL] | [details] |

### Detailed Findings

**[Category 1: e.g., Image Pull Issues]**
- Problem: [specific problem]
- Evidence: [from events/logs]
- Impact: [how this affects the pod]

**[Category 2: e.g., Application Crash]**
- Problem: [specific problem]
- Evidence: [from logs]
- Impact: [how this affects the pod]

### Recommended Actions

1. **[Action 1]** - [description]
   ```bash
   [command to fix - e.g., oc create secret docker-registry...]
   ```

2. **[Action 2]** - [description]
   ```bash
   [command to fix - e.g., oc set resources deployment/app --limits=memory=1Gi]
   ```

3. **[Action 3]** - [description]

### Related Documentation

- [Link to relevant Red Hat KB article if applicable]
- [Link to OpenShift docs for the specific issue]

---

Would you like me to:
1. Execute one of the recommended fixes
2. Dig deeper into a specific area
3. Debug a related resource (Service, Route, ConfigMap)
4. Exit debugging

Select an option:
```

**WAIT for user confirmation before proceeding.**

For pod failure categories and exit code reference, see [debugging-patterns.md](docs/debugging-patterns.md).

## Dependencies

### Required MCP Servers
- `openshift` - Kubernetes/OpenShift resource access for pod status, events, and logs

### Related Skills
- `/debug-build` - If pod failure is due to bad image from build
- `/debug-network` - If pod is running but service connectivity fails
- `/deploy` - To redeploy after fixing issues

### Reference Documentation
- [docs/debugging-patterns.md](docs/debugging-patterns.md) - Common error patterns and troubleshooting trees
- [docs/prerequisites.md](docs/prerequisites.md) - Required tools (oc), cluster access verification
