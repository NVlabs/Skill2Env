---
name: debug-network
description: |
  Diagnose OpenShift service connectivity issues including DNS resolution, service endpoints, route ingress, and network policies. Automates multi-step diagnosis: service endpoint verification, pod selector matching, route status, and network policy analysis. Use this skill when services can't communicate, routes return 503/502 errors, or external access fails. Triggers on /debug-network command or phrases like "can't reach service", "route returning 503", "pods can't communicate", "no endpoints".
model: inherit
color: cyan
license: Apache-2.0
allowed-tools: resources_list resources_get pods_list
metadata:
  user_invocable: "true"
---

# /debug-network Skill

Diagnose OpenShift service connectivity issues by automatically checking endpoints, routes, network policies, and pod readiness.

## Prerequisites

Before running this skill:
1. User is logged into OpenShift cluster
2. User has access to the target namespace
3. Service, Route, or application name is known

## When to Use This Skill

Use this skill when services cannot communicate, routes return 503/502 errors, or external access fails. It automates checking service endpoints, pod selector matching, route status, and network policy analysis to pinpoint connectivity issues.

## Critical: Human-in-the-Loop Requirements

See [Human-in-the-Loop Requirements](docs/human-in-the-loop.md) for mandatory checkpoint behavior.

## Workflow

### Step 1: Identify Target Service

```markdown
## Network Debugging

**Current OpenShift Context:**
- Cluster: [cluster]
- Namespace: [namespace]

What connectivity issue would you like me to debug?

1. **Service connectivity** - Internal service-to-service communication
2. **Route/Ingress** - External access to application
3. **Specify service name** - Debug a specific service
4. **List services** - Show services in current namespace

Select an option or enter a service name:
```

**WAIT for user response.** Do NOT proceed until user identifies the target.

If user selects "List services":
Use kubernetes MCP `resources_list` for services:

```markdown
## Services in [namespace]

| Service | Type | Cluster IP | Ports | Endpoints |
|---------|------|------------|-------|-----------|
| [app-service] | ClusterIP | [ip] | [8080/TCP] | [2 ready] |
| [db-service] | ClusterIP | [ip] | [5432/TCP] | [0 - no endpoints!] |
| [api-service] | ClusterIP | [ip] | [3000/TCP] | [1 ready] |

Which service would you like me to debug?
```

**WAIT for user to select a service.**

### Step 2: Check Service and Endpoints

Use kubernetes MCP `resources_get` for Service and Endpoints:

```markdown
## Service Analysis: [service-name]

**Service Configuration:**
| Field | Value |
|-------|-------|
| Type | [ClusterIP/NodePort/LoadBalancer] |
| Cluster IP | [ip] |
| Ports | [port-mappings] |
| Selector | [label-selector] |

**Endpoints:**
| Subset | Addresses | Ports | Status |
|--------|-----------|-------|--------|
| [subset] | [pod-ip-1, pod-ip-2] | [port] | [Ready] |

[If no endpoints:]
**WARNING: Service has NO endpoints!**

This means no pods match the service selector, or matching pods are not ready.

**Service Selector:** `app=[value], tier=[value]`

**Quick Assessment:**
[Based on endpoints status, provide initial assessment]

Continue with pod analysis? (yes/no)
```

**WAIT for user confirmation before proceeding.**

### Step 3: Verify Backend Pods

Use kubernetes MCP `pods_list` with label selector matching service:

```markdown
## Backend Pods for Service: [service-name]

**Service Selector:** `[selector-labels]`

**Matching Pods:**
| Pod | Status | Ready | IP | Node |
|-----|--------|-------|-----|------|
| [pod-1] | Running | 1/1 | [ip] | [node] |
| [pod-2] | Running | 0/1 | [ip] | [node] |
| [pod-3] | CrashLoopBackOff | 0/1 | [ip] | [node] |

**Readiness Analysis:**
| Pod | Readiness Probe | Last Check | Status |
|-----|-----------------|------------|--------|
| [pod-1] | HTTP GET :8080/ | [time] | Passing |
| [pod-2] | HTTP GET :8080/ | [time] | Failing - Connection refused |
| [pod-3] | HTTP GET :8080/ | [time] | Failing - Container not running |

[If selector mismatch:]
**WARNING: Label Mismatch Detected!**

Service selector: `app=myapp`
Pod labels: `app=my-app` (hyphen difference!)

**Issues Found:**
- [Issue 1 - e.g., "Pod [pod-2] failing readiness probe - application not listening on port 8080"]
- [Issue 2 - e.g., "Pod [pod-3] is in CrashLoopBackOff - run /debug-pod for details"]

Continue to check Route? (yes/no/skip)
```

**WAIT for user confirmation before proceeding.**

### Step 4: Check Route Status

Use kubernetes MCP `resources_get` for Route:

```markdown
## Route Analysis: [route-name]

**Route Configuration:**
| Field | Value |
|-------|-------|
| Host | [hostname] |
| Path | [path or "/"] |
| TLS Termination | [edge/passthrough/reencrypt/none] |
| Insecure Policy | [Redirect/Allow/None] |
| Target Service | [service-name] |
| Target Port | [port-name or port-number] |
| Weight | [100] |

**Route Status:**
| Condition | Status | Reason | Message |
|-----------|--------|--------|---------|
| Admitted | [True/False] | [reason] | [message] |

[If not admitted:]
**WARNING: Route NOT admitted by router!**

**Ingress Status:**
| Router | Admitted | Host | Conditions |
|--------|----------|------|------------|
| [default] | [True/False] | [host] | [conditions] |

**TLS Configuration:**
| Setting | Value |
|---------|-------|
| Certificate | [Provided/Default/None] |
| Key | [Provided/None] |
| CA Certificate | [Provided/None] |
| Destination CA | [Provided/None] (for reencrypt) |

**Issues Found:**
- [Issue 1 - e.g., "Route not admitted - hostname conflicts with existing route"]
- [Issue 2 - e.g., "TLS termination is 'passthrough' but backend is HTTP only"]

Continue to check Network Policies? (yes/no/skip)
```

**WAIT for user confirmation before proceeding.**

### Step 5: Analyze Network Policies

Use kubernetes MCP `resources_list` for NetworkPolicy:

```markdown
## Network Policy Analysis

**NetworkPolicies in [namespace]:**
| Policy | Pod Selector | Ingress Rules | Egress Rules |
|--------|--------------|---------------|--------------|
| [policy-1] | app=myapp | [2 rules] | [Allow all] |
| [policy-2] | tier=backend | [1 rule] | [1 rule] |
| [default-deny] | {} (all pods) | [Deny all] | [Allow all] |

**Policies Affecting [service-name] Pods:**

**Policy: [policy-name]**
```yaml
ingress:
- from:
  - podSelector:
      matchLabels:
        app: frontend
  ports:
  - port: 8080
    protocol: TCP
```

**Analysis:**
- Pods with `app=myapp` only accept traffic from pods with `app=frontend`
- Traffic from other namespaces is BLOCKED
- Traffic on ports other than 8080 is BLOCKED

**Potential Blocking:**
- [Issue 1 - e.g., "Source pods have label 'app=web' but policy requires 'app=frontend'"]
- [Issue 2 - e.g., "Cross-namespace traffic blocked - no namespaceSelector in policy"]

Continue to diagnosis summary? (yes/no)
```

**WAIT for user confirmation before proceeding.**

### Step 6: Present Diagnosis Summary

```markdown
## Network Diagnosis Summary: [service-name]

### Connectivity Path

```
[Source] → [Service] → [Endpoints] → [Pod]
   OK   →    OK     →   [STATUS]  → [STATUS]

[External] → [Route] → [Router] → [Service] → [Pod]
    OK    →   OK    →   OK     →    OK     → [STATUS]
```

### Root Cause

**Primary Issue:** [Categorized root cause]

| Component | Status | Details |
|-----------|--------|---------|
| Service | [OK/FAIL] | [details] |
| Endpoints | [OK/FAIL] | [count] ready |
| Pod Readiness | [OK/FAIL] | [X/Y] pods ready |
| Route | [OK/FAIL] | [details] |
| Network Policy | [OK/WARN] | [details] |
| DNS | [OK/FAIL] | [details] |

### Detailed Findings

**[Category 1: e.g., No Endpoints]**
- Problem: [specific problem - e.g., "Service selector doesn't match any pods"]
- Evidence: [selector vs pod labels]
- Impact: [all traffic to service fails]

**[Category 2: e.g., Readiness Probe Failing]**
- Problem: [specific problem]
- Evidence: [probe configuration and failure reason]
- Impact: [pod removed from endpoints]

### Recommended Actions

1. **[Action 1]** - [description]
   ```bash
   [command to fix - e.g., oc label pod myapp-xxx app=myapp --overwrite]
   ```

2. **[Action 2]** - [description]
   ```bash
   [command to fix - e.g., oc patch svc myapp -p '{"spec":{"selector":{"app":"my-app"}}}']
   ```

3. **[Action 3]** - [description]

### Test Connectivity

After fixing, verify with:
```bash
# Test internal connectivity from another pod
oc run test-curl --rm -i --tty --image=curlimages/curl -- \
  curl -v http://[service-name].[namespace].svc.cluster.local:[port]

# Test route externally
curl -v https://[route-host]

# Check endpoints
oc get endpoints [service-name] -n [namespace]
```

---

Would you like me to:
1. Execute one of the recommended fixes
2. Test connectivity from a debug pod
3. Debug specific pods (/debug-pod)
4. Check DNS resolution
5. Exit debugging

Select an option:
```

**WAIT for user to select next action.**

## Common Connectivity Issues

For detailed diagnosis and fix tables covering service, route, and network policy issues, see [docs/debugging-patterns.md](docs/debugging-patterns.md).

## Dependencies

### Required MCP Servers
- `openshift` - Kubernetes/OpenShift resource access for services, routes, endpoints, and network policies

### Related Skills
- `/debug-pod` - To debug specific backend pods
- `/deploy` - To fix and redeploy the service

### Reference Documentation
- [docs/debugging-patterns.md](docs/debugging-patterns.md) - Common error patterns
- [docs/prerequisites.md](docs/prerequisites.md) - Required tools (oc), cluster access verification
