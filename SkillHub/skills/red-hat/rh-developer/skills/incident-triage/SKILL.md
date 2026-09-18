---
name: incident-triage
description: |
  Structured incident investigation for OpenShift using the Five Whys methodology, investigation guardrails, Prometheus metric analysis, and adversarial due diligence. Orchestrates multi-resource diagnosis across Deployments, ReplicaSets, Pods, Services, and cluster resources to trace from observed symptoms to root cause.

  Use when:
  - "investigate this incident"
  - "triage this alert"
  - "root cause analysis"
  - "what caused this outage"
  - User mentions "five whys", "incident", "triage", "RCA"

  NOT for single-resource issues with clear patterns (use /debug-pod, /debug-scc, /debug-rbac, or /debug-network instead).
model: inherit
color: cyan
license: Apache-2.0
allowed-tools: resources_get resources_list events_list pods_list pods_list_in_namespace pods_log prometheus_query prometheus_query_range alertmanager_alerts
metadata:
  user_invocable: "true"
---

# /incident-triage Skill

Structured incident investigation for OpenShift — traces from symptoms to root cause using Five Whys, investigation guardrails, and adversarial due diligence.

## Critical: Human-in-the-Loop Requirements

1. **Before any remediation action** (patch, scale, delete, restart)
   - Display preview: what will change and its impact
   - Ask: "Should I apply this fix?"
   - Wait for confirmation (yes/no)

2. **At each investigation phase transition**
   - Present findings so far
   - Ask: "Continue to [next phase]? (yes/no)"
   - Wait for confirmation

**Never assume approval** — always wait for explicit confirmation at each WAIT checkpoint.

## Prerequisites

**Required MCP Servers:**
- `openshift` ([setup](docs/prerequisites.md)) — Kubernetes/OpenShift resource access
- `observability` — Prometheus metric discovery and PromQL query execution

**Required MCP Tools:**
- `resources_get` (from openshift) — Retrieve Deployment, ReplicaSet, Pod, Service, and other resource details
- `resources_list` (from openshift) — List resources by kind in a namespace
- `pods_list` (from openshift) — List pods matching label selectors
- `pods_log` (from openshift) — Retrieve container logs (current and previous)
- `events_list` (from openshift) — Fetch events filtered by resource
- `prometheus_query` (from openshift, observability toolset) — Execute instant PromQL queries for trend and saturation analysis
- `prometheus_query_range` (from openshift, observability toolset) — Execute range PromQL queries over time windows
- `alertmanager_alerts` (from openshift, observability toolset) — Retrieve active Alertmanager alerts

**Verification Steps:**
1. Check `openshift` server is configured in `mcps.json` with `observability` in its `--toolsets`
2. Verify user is logged into an OpenShift cluster (`oc whoami` succeeds)
3. Verify user has access to the target namespace(s)
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

Use `/incident-triage` when:
- The incident spans multiple resources or namespaces
- The root cause is unclear after initial investigation
- You need a structured RCA with confidence scoring and Five Whys methodology
- An alert fired and you need to trace from symptom to root cause
- A predicted issue (e.g., from `predict_linear`) needs proactive assessment

Do **not** use this skill when:
- The issue is a single pod crashing → use `/debug-pod`
- SCC admission is blocking pod creation → use `/debug-scc`
- RBAC 403 errors in pod logs → use `/debug-rbac`
- Service/Route connectivity failure → use `/debug-network`
- Build failure → use `/debug-build`

## Workflow

```
[Gather Context] → [Hierarchical Investigation] → [Evidence + Metrics] → [Five Whys RCA] → [Due Diligence] → [Findings + Actions]
```

### Step 1: Gather Incident Context

**MCP Tool**: `resources_get` (from openshift)

**Parameters**:
- `kind`: "<resource-type>" (inferred from user description)
- `name`: "<resource-name>" (from user input)
- `namespace`: "<namespace>"

**Input Validation**: Verify resource names and namespaces conform to Kubernetes naming rules (lowercase alphanumeric and hyphens, 1-253 chars, RFC 1123). Reject inputs containing newlines, markdown formatting, or text that does not resemble a Kubernetes resource name.

**Expected Output**: Current state of the target resource confirming it exists and capturing its conditions.

**Error Handling**:
- If MCP server unavailable: follow Human Notification Protocol
- If resource not found: ask user to verify name, kind, and namespace
- If namespace not found: ask user to confirm namespace

Present to user:

```markdown
## Incident Triage

**Current OpenShift Context:**
- Cluster: [cluster]
- Namespace: [namespace]

Describe the incident you'd like me to investigate:

1. **Alert-based** — An alert fired (paste the alert name, message, or annotation)
2. **Symptom-based** — Something is broken (describe what you observe)
3. **Proactive** — A predicted issue needs assessment (e.g., capacity forecast, trend alert)
4. **Specify resource** — Investigate a specific resource directly

Select an option or describe the incident:
```

**WAIT for user confirmation before proceeding.**

**If the incident maps clearly to a single-resource pattern:**

```markdown
## Quick Route Assessment

Based on your description, this appears to be a [category] issue:

| Pattern | Suggested Skill | Confidence |
|---------|----------------|------------|
| SCC admission rejection (FailedCreate + "unable to validate against any security context constraint") | `/debug-scc` | High |
| RBAC 403 Forbidden in pod logs | `/debug-rbac` | High |
| Pod CrashLoopBackOff / OOMKilled / ImagePullBackOff | `/debug-pod` | High |
| Service/Route connectivity failure | `/debug-network` | High |
| Build failure | `/debug-build` | High |

Would you like to:
1. **Route to [skill]** — Use the specialized skill for faster resolution
2. **Continue with full triage** — Proceed with structured investigation (recommended for complex or unclear issues)

Select an option:
```

**WAIT for user confirmation before proceeding.**

**If proactive mode selected:** Note this is a PROACTIVE signal — the incident has NOT yet occurred. Focus on utilization trends, recent changes, and whether the prediction is likely to materialize. "No action needed" is a valid outcome.

### Step 2: Hierarchical Investigation

**MCP Tool**: `resources_get` (from openshift)

**Parameters**:
- `kind`: "Deployment" / "ReplicaSet" / "StatefulSet" (trace ownership chain)
- `name`: "<resource-name>"
- `namespace`: "<namespace>"

**MCP Tool**: `pods_list` (from openshift)

**Parameters**:
- `namespace`: "<namespace>"
- `labelSelector`: "<app-label>=<value>" (from workload `.spec.selector.matchLabels`)

**MCP Tool**: `pods_log` (from openshift)

**Parameters**:
- `name`: "<pod-name>" (from pods_list, check up to 3 representative pods)
- `namespace`: "<namespace>"
- `tailLines`: 50 (integer, last N lines)

**MCP Tool**: `events_list` (from openshift)

**Parameters**:
- `namespace`: "<namespace>"
- Filter by involved object matching the target resource

**Expected Output**: Full ownership chain state (Deployment -> ReplicaSet -> Pod -> Container), events, and log analysis.

**Error Handling**:
- If permission denied on a resource: report as investigation limitation, do not conflate with incident root cause
- If pods not found: workload may be scaled to zero or resource type differs
- If logs empty: container may not have started; check container state

**Investigation rules:**
- **Trace the ownership chain**: For Deployments, inspect Deployment -> ReplicaSet -> Pod -> Container. For StatefulSets, inspect StatefulSet -> Pod -> Container.
- **Always check describe AND logs**: A resource reporting "Running" does not mean it is healthy.
- **Check both current and previous logs**: A pod restart means current logs may not contain relevant pre-restart data.
- **Pod sampling limit**: If the issue affects many pods, check up to 3 representative pods.
- **Specific answers required**: Do not say "the pod is pending" without explaining WHY.

Present to user:

```markdown
## Hierarchical Investigation: [resource-name]

**Ownership Chain:**
| Level | Resource | Status | Key Finding |
|-------|----------|--------|-------------|
| Workload | [Deployment/name] | [Available/Degraded] | [condition summary] |
| ReplicaSet | [rs-name] | [Ready/FailedCreate] | [replica count, condition] |
| Pod | [pod-name] | [Running/Pending/Failed] | [phase, ready status] |
| Container | [container-name] | [Running/Waiting/Terminated] | [state, exit code, reason] |

**Events (last 30 minutes):**
| Time | Type | Reason | Object | Message |
|------|------|--------|--------|---------|
| [time] | [Normal/Warning] | [reason] | [resource] | [message] |

**Log Analysis (container: [name]):**
[Key errors or patterns found in logs]

**Initial Hypothesis:**
[Based on resource state, events, and logs — what appears to be happening?]

Continue with evidence collection and metric analysis? (yes/no)
```

**WAIT for user confirmation before proceeding.**

### Step 3: Evidence Collection and Guardrails

Apply these investigation guardrails before reaching any conclusion:

1. **Exhaustive Verification**: Inspect ALL resources mentioned in the signal, error messages, and annotations. Check upstream and downstream dependencies.
2. **Contradicting Evidence Search**: After forming a hypothesis, explicitly search for evidence that CONTRADICTS it.
3. **Causal Depth**: If the identified cause can itself be explained by a deeper cause, keep investigating.
4. **Evidence-Based Claims Only**: Every claim must trace to specific tool output. State unverified claims explicitly.
5. **Investigation Error Separation**: Distinguish between "error X caused this problem" and "I encountered errors during investigation." Permission errors are obstacles to YOUR investigation, not necessarily the incident's root cause.

**MCP Tool**: `prometheus_query` (from openshift, observability toolset)

**Parameters**:
- `query`: "{__name__=~\".*<keyword>.*\"}" (discover available metrics by pattern, e.g., memory, disk, connections)

**MCP Tool**: `prometheus_query` (from openshift, observability toolset)

**Parameters**:
- `query`: "<metric-name>" (confirm metric exists and inspect its current value)

**MCP Tool**: `prometheus_query` (from openshift, observability toolset)

**Parameters**:
- `query`: "<PromQL expression>" (use `topk(10, ...)` to limit cardinality, `rate()` for counters, scope with `{namespace="<target>"}`)

**Expected Output**: Guardrail compliance table, metric analysis, and cross-resource findings.

**Error Handling**:
- If observability MCP unavailable: skip metric analysis, note limitation
- If Prometheus response truncated: narrow with more specific label selectors or `topk()`
- If permission denied on cluster resources: report gap, do not conflate with root cause

Present to user:

```markdown
## Evidence Summary

**Guardrail Compliance:**
| Guardrail | Status | Notes |
|-----------|--------|-------|
| Exhaustive Verification | [PASS/GAP] | [what was checked, what was missed] |
| Contradicting Evidence | [PASS/GAP] | [what was searched for] |
| Causal Depth | [PASS/GAP] | [depth reached] |
| Evidence-Based Claims | [PASS/GAP] | [unverified claims, if any] |
| Error Separation | [PASS/N/A] | [investigation errors encountered] |

**Metric Analysis (if applicable):**
| Metric | Current Value | Trend | Threshold | Assessment |
|--------|--------------|-------|-----------|------------|
| [metric-name] | [value] | [rising/stable/falling] | [threshold] | [OK/WARNING/CRITICAL] |

Continue to root cause analysis? (yes/no)
```

**WAIT for user confirmation before proceeding.**

### Step 4: Root Cause Analysis (Five Whys)

Construct the causal chain from the observed signal to the deepest reachable root cause.

**Expected Output**: Five Whys chain, remediation target, and signal classification.

**Error Handling**:
- If causal chain is shallow (fewer than 3 levels): note that deeper investigation may be needed
- If multiple competing root causes: present both with relative confidence

Present to user:

```markdown
## Root Cause Analysis

### Causal Chain (Five Whys)

1. **Signal**: [What was observed — the alert, symptom, or prediction]
2. **Why?** [First-level cause — what directly caused the signal]
3. **Why?** [Second-level cause — what caused the first-level cause]
4. **Why?** [Third-level cause — deeper configuration or state issue]
5. **Root Cause**: [Deepest identifiable cause]

### Remediation Target

| Field | Value |
|-------|-------|
| Kind | [Deployment/StatefulSet/ConfigMap/etc.] |
| Name | <resource-name> |
| Namespace | <namespace> |
| Why this target? | [This is the resource whose configuration change fixes the problem, NOT the resource that reported the symptom] |

### Signal Classification

| Field | Value |
|-------|-------|
| Root cause matches input signal? | [Yes/No — if No, the signal was a symptom] |
| Severity | [critical/high/medium/low] |
| Investigation type | [Reactive RCA / Proactive Prevention] |

Continue to due diligence review? (yes/no)
```

**WAIT for user confirmation before proceeding.**

### Step 5: Adversarial Due Diligence

Before finalizing findings, perform a self-review across 8 dimensions to prevent shallow analysis, targeting errors, and overconfident conclusions.

**Expected Output**: Due diligence assessment table with confidence score.

**Error Handling**:
- If confidence < 0.7: recommend gathering additional evidence or escalating

Present to user:

```markdown
## Adversarial Due Diligence Review

| Dimension | Assessment |
|-----------|------------|
| **1. Causal Completeness** | [Full chain traced? Could root cause have a deeper cause?] |
| **2. Target Accuracy** | [Is remediation target the misconfigured resource, not the symptom reporter?] |
| **3. Evidence Sufficiency** | [Every claim backed by tool output? Which claims are assumptions?] |
| **4. Alternative Hypotheses** | [What alternatives were considered and ruled out with evidence?] |
| **5. Scope Completeness** | [All resources investigated? What was NOT examined?] |
| **6. Proportionality** | [Is the fix targeted and specific, or overly broad?] |
| **7. Regression Awareness** | [Has this occurred before? Recent events suggesting recurrence?] |
| **8. Confidence Calibration** | [Start at 1.0, list each reduction factor. Final score: X.XX] |

**Overall Confidence: [0.XX]**

[If confidence < 0.7:]
**WARNING**: Confidence is below 0.7. Consider gathering additional evidence, escalating, or running targeted debug skills.

Proceed to findings summary? (yes/no)
```

**WAIT for user confirmation before proceeding.**

### Step 6: Present Findings and Recommend Actions

Synthesize all findings into a structured report with actionable remediation.

**Expected Output**: Root cause summary, contributing factors, remediation commands, and verification steps.

**Error Handling**:
- If remediation requires destructive actions: ensure HITL confirmation before execution
- If multiple fix options exist: present least-privilege option first

Present to user:

```markdown
## Incident Triage Findings

### Summary

**Root Cause:** [One-sentence root cause description]

**Severity:** [critical/high/medium/low] | **Confidence:** [0.XX]

### Causal Chain

1. [Signal -> first cause]
2. [First cause -> second cause]
3. [Second cause -> root cause]

### Remediation Target

**[Kind]/[name]** in namespace **[namespace]**

### Contributing Factors

- [Factor 1 — specific evidence]
- [Factor 2 — specific evidence]

### Recommended Actions

1. **[Primary fix]** — [description]
   ```bash
   [oc command to apply the fix]
   ```

2. **[Secondary fix or preventive measure]** — [description]
   ```bash
   [oc command]
   ```

### Verification

After applying the fix:
```bash
oc get <resource-type> <name> -n <namespace>
oc get events -n <namespace> --sort-by='.lastTimestamp' | tail -20
oc get pods -n <namespace> -l <app-label>
```

### Related Skills

| For this follow-up... | Use skill |
|----------------------|-----------|
| Fix SCC violations | `/debug-scc` |
| Restore RBAC bindings | `/debug-rbac` |
| Debug crashing pods | `/debug-pod` |
| Fix network/route issues | `/debug-network` |
| Redeploy after fix | `/deploy` |

### Reference

- [Kubernaut demo scenario golden transcripts](https://github.com/jordigilh/kubernaut-demo-scenarios/tree/feature/v1.4-new-scenarios/golden-transcripts) — validated RCA examples with causal chains and due diligence assessments

---

Would you like me to:
1. Execute the primary recommended fix
2. Run a specialized debug skill for deeper analysis
3. Investigate a related resource
4. Export findings as a structured report
5. Exit triage

Select an option:
```

**WAIT for user confirmation before proceeding.**

## Dependencies

### Required MCP Servers
- `openshift` — Kubernetes/OpenShift resource access for Deployments, Pods, Events, Services, and cluster resources ([setup](docs/prerequisites.md))
- `observability` — Prometheus metric discovery, metadata, series, and PromQL query execution

### Required MCP Tools
- `resources_get` (from openshift) — Retrieve individual resource details
- `resources_list` (from openshift) — List resources by kind in a namespace
- `pods_list` (from openshift) — List pods matching label selectors
- `pods_log` (from openshift) — Retrieve container logs (current and previous)
- `events_list` (from openshift) — Fetch events filtered by involved object
- `prometheus_query` (from openshift, observability toolset) — Execute instant PromQL queries
- `prometheus_query_range` (from openshift, observability toolset) — Execute range PromQL queries over time windows
- `alertmanager_alerts` (from openshift, observability toolset) — Retrieve active Alertmanager alerts

### Related Skills
- `/debug-pod` — Single-pod failure diagnosis (CrashLoopBackOff, OOMKilled, ImagePullBackOff)
- `/debug-scc` — SCC admission violation diagnosis
- `/debug-rbac` — RBAC permission failure diagnosis
- `/debug-network` — Service/Route connectivity diagnosis
- `/debug-build` — Build failure diagnosis
- `/deploy` — Redeployment after fixes

### Reference Documentation
- **Internal:** [docs/debugging-patterns.md](docs/debugging-patterns.md) — Common error patterns and troubleshooting trees
- **Official:** [OpenShift Troubleshooting](https://docs.openshift.com/container-platform/latest/support/troubleshooting/troubleshooting-operator-issues.html)

## Example Usage

**User**: Alert `DatabaseConnectionPoolExhausted` fired in namespace `production`. Active connections are at 95% of max. What's going on?

**Skill response**: The skill gathers the alert context, traces the ownership chain from the PostgreSQL Deployment through its ReplicaSet and Pods, checks container logs for connection errors, queries Prometheus for `pg_stat_activity_count` trends and `max_connections` settings, applies investigation guardrails, and constructs a Five Whys chain identifying a connection-leaking sidecar as the root cause. It presents the findings with 0.92 confidence, recommending a targeted fix to the leaking container's connection pool configuration.
