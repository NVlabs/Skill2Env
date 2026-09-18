---
name: deploy
description: |
  Create Kubernetes Deployment, Service, and Route resources on OpenShift to deploy and expose an application. Use this skill after /s2i-build to make the built image accessible. Handles port detection, replica configuration, HTTPS route creation, rollout monitoring, and rollback on failure. Triggers on /deploy command when user wants to deploy a container image to OpenShift.
model: inherit
color: green
license: Apache-2.0
allowed-tools: resources_create_or_update pods_list pods_log
metadata:
  user_invocable: "true"
---

# /deploy Skill

Create Kubernetes/OpenShift resources (Deployment, Service, Route) to deploy and expose an application from a container image.

## Prerequisites

Before running this skill:
1. User is logged into OpenShift cluster
2. Container image exists (from ImageStream or external registry)
3. Target namespace exists

## When to Use This Skill

Use `/deploy` after building a container image (via `/s2i-build` or external registry) to create Deployment, Service, and Route resources on OpenShift. This skill handles port detection, replica configuration, rollout monitoring, and rollback on failure.

## Critical: Human-in-the-Loop Requirements

See [Human-in-the-Loop Requirements](docs/human-in-the-loop.md) for mandatory checkpoint behavior.

## Workflow

### Step 1: Gather Deployment Information

```markdown
## Deployment Configuration

**Current OpenShift Context:**
- Cluster: [cluster]
- Namespace: [namespace]

**Please confirm deployment settings:**

| Setting | Value | Source |
|---------|-------|--------|
| App Name | `[name]` | [from s2i-build / input] |
| Image | `[image-ref]` | [from ImageStream / input] |
| Container Port | `[port]` | [detected / needs input] |
| Replicas | `1` | [default] |
| Expose Route | `yes` | [default] |

Confirm these settings or tell me what to change.
```

**WAIT for user confirmation before proceeding.**

### Step 2: Detect Container Port

Try to detect port from project files:

1. **Dockerfile:** Look for `EXPOSE <port>` (Most accurate for container builds)
2. **Web Server Config:** Look for `listen <port>` in `nginx.conf`, `httpd.conf`, etc.
3. **Framework Defaults:**
   - **Node.js:** Look for `PORT` env var usage, common: 3000 (dev), 8080 (prod/S2I)
   - **Python:** Flask default 5000, FastAPI/Uvicorn 8000
   - **Java:** Spring Boot 8080, Quarkus 8080
   - **Go:** Common 8080
   - **Ruby Rails:** 3000

```markdown
## Port Detection

I detected port **[port]** based on:
- [reason - e.g., "PORT environment variable in package.json scripts"]

Is this correct?
- yes - Use port [port]
- no - Specify the correct port
```

**WAIT for user confirmation before proceeding.**

If unable to detect:
```markdown
## Port Required

I couldn't automatically detect the container port.

Common ports by framework:
- Node.js/Express: 3000 or 8080
- Python Flask: 5000
- Python FastAPI: 8000
- Java Spring Boot: 8080
- Go: 8080

**What port does your application listen on?**
```

### Step 3: Create Deployment

Show the Deployment manifest:

```markdown
## Step 1 of 3: Create Deployment

Read `templates/deployment.yaml.template` and substitute `${APP_NAME}`, `${NAMESPACE}`, `${PORT}`, `${REPLICAS}` with session state values.

Show the rendered YAML to user and confirm.

**Proceed with creating this Deployment?** (yes/no)
```

**WAIT for user confirmation before proceeding.**

- If user says "yes" → Use kubernetes MCP `resources_create_or_update` to apply
- If user says "no" → Ask what they would like to change
- If user wants modifications → Update the YAML and show again for confirmation

### Step 4: Create Service

```markdown
## Step 2 of 3: Create Service

Read `templates/service.yaml.template` and substitute `${APP_NAME}`, `${NAMESPACE}`, `${PORT}`.

Show the rendered YAML to user and confirm.

**Proceed with creating this Service?** (yes/no)
```

**WAIT for user confirmation before proceeding.**

- If user says "yes" → Use kubernetes MCP `resources_create_or_update` to apply
- If user says "no" → Ask what they would like to change
- If user wants modifications → Update the YAML and show again for confirmation

### Step 5: Create Route (Optional)

If user wants external exposure:

```markdown
## Step 3 of 3: Create Route

Read `templates/route.yaml.template` and substitute `${APP_NAME}`, `${NAMESPACE}`.

Show the rendered YAML to user and confirm.

**Proceed with creating this Route?** (yes/no/skip)
```

**WAIT for user confirmation before proceeding.**

- If user says "yes" → Use kubernetes MCP `resources_create_or_update` to apply
- If user says "skip" → Skip Route creation and proceed to rollout monitoring
- If user says "no" → Ask what they would like to change
- If user wants modifications → Update the YAML and show again for confirmation

### Step 6: Wait for Rollout

Monitor deployment status:

```markdown
## Deployment Rollout

Waiting for pods to be ready...

**Deployment:** [app-name]
**Desired:** [replicas]
**Ready:** [current]/[replicas]

**Pod Status:**
| Pod | Status | Ready | Restarts |
|-----|--------|-------|----------|
| [app-name]-xxx-yyy | Running | 1/1 | 0 |

[Poll until ready or timeout after 5 minutes]
```

### Step 6a: Handle Deployment Failure

If pods do not become ready within the timeout period, or pods are in error states (CrashLoopBackOff, ImagePullBackOff, Pending):

```markdown
## Deployment Failed

**Status:** Rollout did not complete successfully

**Pod Status:**
| Pod | Status | Ready | Restarts | Reason |
|-----|--------|-------|----------|--------|
| [app-name]-xxx-yyy | [CrashLoopBackOff/ImagePullBackOff/Pending] | 0/1 | [count] | [reason] |

**Events:**
| Time | Type | Message |
|------|------|---------|
| [time] | Warning | [event message] |

---

**Would you like me to diagnose the issue?**

1. **Debug Pod** - Investigate pod failures (runs `/debug-pod`)
   - Analyzes pod status, events, logs, and resource constraints
   - Identifies root cause (OOM, image pull issues, crashes, etc.)

2. **Debug Network** - Investigate connectivity issues (runs `/debug-network`)
   - Checks service endpoints, route status, network policies
   - Useful if pods are running but service is unreachable

3. **View logs manually** - Show pod logs without full diagnosis

4. **Rollback deployment** - Delete created resources and stop

5. **Continue waiting** - Wait another 5 minutes for rollout

Select an option:
```

**WAIT for user to select an option.**

- If user selects "Debug Pod" → Invoke `/debug-pod` skill with pod name
- If user selects "Debug Network" → Invoke `/debug-network` skill with service name
- If user selects "View logs" → Show pod logs using `pods_log`
- If user selects "Rollback" → Delete Deployment, Service, Route
- If user selects "Continue" → Wait another polling cycle

### Step 7: Deployment Complete

```markdown
## Deployment Complete!

**Application:** [app-name]
**Namespace:** [namespace]

**Access URLs:**
| Type | URL |
|------|-----|
| External | https://[route-host] |
| Internal | http://[app-name].[namespace].svc.cluster.local:[port] |

**Resources Created:**
| Resource | Name | Status |
|----------|------|--------|
| Deployment | [app-name] | [replicas]/[replicas] Ready |
| Service | [app-name] | Active |
| Route | [app-name] | Admitted |

**Quick Commands:**
```bash
# View logs
oc logs -f deployment/[app-name] -n [namespace]

# Scale replicas
oc scale deployment/[app-name] --replicas=3 -n [namespace]

# Restart pods
oc rollout restart deployment/[app-name] -n [namespace]

# Delete all
oc delete all -l app=[app-name] -n [namespace]
```

Your application is now live!
```

## Dependencies

### Required MCP Servers
- `openshift` - cluster resource creation and management

### Related Skills
- `/debug-pod` - Pod failures (CrashLoopBackOff, OOMKilled, ImagePullBackOff)
- `/debug-network` - Service connectivity issues (no endpoints, 503 errors)
- `/debug-build` - Build failures before deployment

### Reference Documentation
- [docs/prerequisites.md](docs/prerequisites.md) - Required tools (oc), cluster access verification
- [docs/debugging-patterns.md](docs/debugging-patterns.md) - Common error patterns and troubleshooting
