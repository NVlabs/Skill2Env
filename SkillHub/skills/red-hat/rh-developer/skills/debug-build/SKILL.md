---
name: debug-build
description: |
  Diagnose OpenShift build failures including S2I builds, Docker/Podman builds, and BuildConfig issues. Automates multi-step diagnosis: BuildConfig validation, build pod logs, registry authentication, and source repository access. Use this skill when builds fail, hang, or produce unexpected results. Triggers on /debug-build command or phrases like "build failed", "S2I error", "can't pull builder image", "can't push to registry", "build timeout".
model: inherit
color: cyan
license: Apache-2.0
allowed-tools: resources_list resources_get pods_log
metadata:
  user_invocable: "true"
---

# /debug-build Skill

Diagnose OpenShift build failures by automatically gathering BuildConfig, Build status, build pod logs, and related resources.

## Prerequisites

Before running this skill:
1. User is logged into OpenShift cluster
2. User has access to the target namespace
3. Build or BuildConfig name is known (or can be identified from recent builds)

## When to Use This Skill

Use this skill when OpenShift builds fail, hang, or produce unexpected results. It diagnoses S2I builds, Docker/Podman builds, and BuildConfig issues by analyzing build pod logs, registry authentication, and source repository access.

## Critical: Human-in-the-Loop Requirements

See [Human-in-the-Loop Requirements](docs/human-in-the-loop.md) for mandatory checkpoint behavior.

## Workflow

### Step 1: Identify Target Build

```markdown
## Build Debugging

**Current OpenShift Context:**
- Cluster: [cluster]
- Namespace: [namespace]

Which build would you like me to debug?

1. **Specify build name** - Enter the build name directly (e.g., myapp-1)
2. **List failed builds** - Show recent failed builds in current namespace
3. **From BuildConfig** - Debug latest build from a specific BuildConfig

Select an option or enter a build name:
```

**WAIT for user confirmation before proceeding.**

If user selects "List failed builds":
Use kubernetes MCP `resources_list` for builds, filter by Failed phase:

```markdown
## Recent Failed Builds in [namespace]

| Build | BuildConfig | Status | Started | Duration |
|-------|-------------|--------|---------|----------|
| [app-1] | [app] | Failed | [timestamp] | [duration] |
| [app-2] | [app] | Cancelled | [timestamp] | [duration] |
| [other-1] | [other] | Failed | [timestamp] | [duration] |

Which build would you like me to debug?
```

**WAIT for user to select a build.**

### Step 2: Get Build Status Overview

Use kubernetes MCP `resources_get` to get Build details:

```markdown
## Build Status: [build-name]

**Build Info:**
| Field | Value |
|-------|-------|
| BuildConfig | [buildconfig-name] |
| Strategy | [Source/Docker/JenkinsPipeline] |
| Phase | [New/Pending/Running/Complete/Failed/Cancelled] |
| Started | [timestamp] |
| Completed | [timestamp or "Still running"] |
| Duration | [duration] |

**Build Configuration:**
| Setting | Value |
|---------|-------|
| Source Type | [Git/Binary/Dockerfile] |
| Git URL | [url] |
| Git Ref | [branch/tag] |
| Builder Image | [image:tag] |
| Output Image | [imagestream:tag] |

**Build Status:**
- Phase: [phase]
- Reason: [reason if failed]
- Message: [message if available]

**Quick Assessment:**
[Based on status, provide initial assessment - e.g., "Build failed during assemble phase - likely dependency installation issue"]

Continue with detailed analysis? (yes/no)
```

**WAIT for user confirmation before proceeding.**

### Step 3: Analyze BuildConfig

Use kubernetes MCP `resources_get` to get BuildConfig:

```markdown
## BuildConfig Analysis: [buildconfig-name]

**Source Configuration:**
| Setting | Value | Status |
|---------|-------|--------|
| Git URL | [url] | [OK/WARN: check access] |
| Git Ref | [ref] | [OK/WARN: branch not found] |
| Context Dir | [dir or "/"] | [OK] |
| Source Secret | [secret-name or "None"] | [OK/MISSING] |

**Builder Image:**
| Setting | Value | Status |
|---------|-------|--------|
| Image | [image:tag] | [OK/WARN: check exists] |
| Pull Secret | [secret-name or "None"] | [OK/MISSING] |

**Output Configuration:**
| Setting | Value | Status |
|---------|-------|--------|
| Output To | [ImageStreamTag] | [OK] |
| Push Secret | [secret-name or "None"] | [OK/MISSING] |

**Environment Variables:**
| Name | Value | Source |
|------|-------|--------|
| [VAR] | [value or "***"] | [Direct/ConfigMap/Secret] |

**Issues Found:**
- [Issue 1 - e.g., "Source secret 'github-creds' referenced but not found"]
- [Issue 2 - e.g., "Builder image uses older tag, may have compatibility issues"]

Continue to view build logs? (yes/no)
```

**WAIT for user confirmation before proceeding.**

### Step 4: Get Build Pod Logs

Use kubernetes MCP `pods_log` for the builder pod:

```markdown
## Build Logs: [build-name]

**Build Phases:**
| Phase | Status | Duration |
|-------|--------|----------|
| Fetching source | [Complete/Failed] | [duration] |
| Pulling builder image | [Complete/Failed] | [duration] |
| Assemble | [Complete/Failed] | [duration] |
| Commit | [Complete/Failed] | [duration] |
| Push | [Complete/Failed] | [duration] |

**Failed Phase: [phase-name]**

```
[Last 100 lines of build logs, focused on the failing phase]
```

**Log Analysis:**

[Analyze logs and identify errors:]

**Errors Found:**
- Line [X]: [error description - e.g., "npm ERR! 404 Not Found - package 'nonexistent@1.0.0'"]
- Line [Y]: [error description - e.g., "error: unable to resolve 'github.com/private/repo'"]

**S2I Phase Explanation:**

[For S2I builds, explain what the failed phase does:]
- **assemble**: Installs dependencies and builds application
- **commit**: Creates the final container image layer
- **push**: Pushes image to internal registry

Continue to check related resources? (yes/no)
```

**WAIT for user confirmation before proceeding.**

### Step 5: Check Related Resources

Check secrets, imagestreams, and source access:

```markdown
## Related Resources Analysis

**ImageStreams:**
| ImageStream | Tags | Last Updated | Status |
|-------------|------|--------------|--------|
| [app] | [latest, v1.0] | [timestamp] | [OK] |
| [builder] | [imported] | [timestamp] | [OK/MISSING] |

**Secrets:**
| Secret | Type | Used By | Status |
|--------|------|---------|--------|
| [source-secret] | kubernetes.io/basic-auth | Source | [OK/MISSING] |
| [push-secret] | kubernetes.io/dockerconfigjson | Output | [OK/MISSING] |

**Source Repository Access:**
[If GitHub MCP available, check if source URL is accessible]
- URL: [git-url]
- Status: [Accessible/401 Unauthorized/404 Not Found/Timeout]

**Registry Access:**
[Check if internal registry is accessible]
- Registry: image-registry.openshift-image-registry.svc:5000
- Status: [OK/Unreachable]

**Issues Found:**
- [Issue 1 - e.g., "Secret 'github-token' missing - cannot authenticate to private repo"]
- [Issue 2 - e.g., "Builder ImageStreamTag 'nodejs:18' not imported"]

Continue to full diagnosis summary? (yes/no)
```

**WAIT for user confirmation before proceeding.**

### Step 6: Present Diagnosis Summary

```markdown
## Diagnosis Summary: [build-name]

### Root Cause

**Primary Issue:** [Categorized root cause]

| Category | Status | Details |
|----------|--------|---------|
| Source Access | [OK/FAIL] | [details] |
| Builder Image | [OK/FAIL] | [details] |
| Dependencies | [OK/FAIL] | [details] |
| Build Script | [OK/FAIL] | [details] |
| Registry Push | [OK/FAIL] | [details] |

### Detailed Findings

**[Category 1: e.g., Dependency Installation]**
- Problem: [specific problem - e.g., "npm package 'lodash@99.0.0' does not exist"]
- Evidence: [from build logs]
- Impact: [build fails during assemble phase]

**[Category 2: e.g., Source Authentication]**
- Problem: [specific problem]
- Evidence: [from events/logs]
- Impact: [cannot clone repository]

### Recommended Actions

1. **[Action 1]** - [description]
   ```bash
   [command to fix - e.g., oc create secret generic github-token --from-literal=...]
   ```

2. **[Action 2]** - [description]
   ```bash
   [command to fix - e.g., oc import-image nodejs:18 --from=registry.access.redhat.com/ubi9/nodejs-18]
   ```

3. **[Action 3]** - [description]

### Retry Build

After fixing the issue:
```bash
# Start a new build
oc start-build [buildconfig-name] -n [namespace]

# Or start build with follow
oc start-build [buildconfig-name] -n [namespace] --follow
```

---

Would you like me to:
1. Execute one of the recommended fixes
2. Retry the build
3. Compare with last successful build
4. Debug the build pod (/debug-pod)
5. Exit debugging

Select an option:
```

**WAIT for user to select next action.**

## Build Failure Categories

For S2I build phase failures, common error patterns (Node.js, Python, Java), and troubleshooting decision trees, see [docs/debugging-patterns.md](docs/debugging-patterns.md).

## Dependencies

### Required MCP Servers
- `openshift` - Kubernetes/OpenShift resource access for builds, BuildConfigs, and build pod logs

### Related Skills
- `/s2i-build` - To retry build after fixing issues
- `/debug-pod` - To debug the builder pod directly
- `/deploy` - To deploy after a successful build

### Reference Documentation
- [docs/builder-images.md](docs/builder-images.md) - S2I builder image selection, version mapping
- [docs/python-s2i-entrypoints.md](docs/python-s2i-entrypoints.md) - Python APP_MODULE configuration
- [docs/debugging-patterns.md](docs/debugging-patterns.md) - Common error patterns
- [docs/prerequisites.md](docs/prerequisites.md) - Required tools (oc), cluster access verification
