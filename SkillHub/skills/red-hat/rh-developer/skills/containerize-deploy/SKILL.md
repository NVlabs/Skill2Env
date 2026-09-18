---
name: containerize-deploy
description: |
  Complete end-to-end workflow for containerizing and deploying applications to OpenShift or standalone RHEL systems. Orchestrates /detect-project, /s2i-build, /deploy, /helm-deploy, and /rhel-deploy skills with user confirmation checkpoints at each phase. Supports S2I, Podman, Helm deployment strategies for OpenShift, and Podman/native deployments for RHEL hosts. Use this skill when user wants to go from source code to running application in one guided workflow. Supports resume after interruption and rollback on failure. Triggers on /containerize-deploy command.
model: inherit
color: green
license: Apache-2.0
allowed-tools: resources_list resources_get resources_create_or_update pods_list pods_list_in_namespace pods_log events_list get_file_contents helm_list helm_install inventory__find_host_by_name vulnerability__get_system_cves planning__get_rhel_lifecycle
metadata:
   user_invocable: "true"
---

# /containerize-deploy Skill

Provide a complete, guided workflow from local source code to running application on OpenShift or standalone RHEL systems. This skill orchestrates `/detect-project`, `/s2i-build`, `/deploy`, `/helm-deploy`, and `/rhel-deploy` with clear user checkpoints at each phase.

## Overview

```
[Intro] → [Detect] → [Target] → [Strategy] ──┬─→ [OpenShift: S2I/Podman/Helm] ──┬─→ [Complete]
                                               └─→ [RHEL: /rhel-deploy] ──────────┘
```

## When to Use This Skill

Use `/containerize-deploy` when a user wants a complete guided workflow from source code to running application on OpenShift or standalone RHEL systems. This skill orchestrates project detection, build strategy selection, and deployment with user confirmation at each phase.

## Critical: Human-in-the-Loop Requirements

See [Human-in-the-Loop Requirements](docs/human-in-the-loop.md) for mandatory checkpoint behavior.

## Workflow

### Phase 0: Introduction

Present the workflow overview and available deployment targets/strategies. Ask: **Ready to begin?** (yes/no)

**WAIT for user confirmation before proceeding.**

### Phase 1: Project Detection

Execute the `/detect-project` workflow.

**If Remote URL provided:**
Follow the "Remote Repository Strategy" path in `/detect-project`.
- Ask user to choose: Remote S2I, Remote Podman, or Clone.

**If Local Files:**
Proceed with standard detection.

```markdown
## Phase 1: Analyzing Your Project

[If Local]
Scanning project directory for language indicators...

[If Remote]
Analyzing remote repository options...

...
```

Store confirmed values in session state, including `BUILD_STRATEGY` and `HELM_CHART_DETECTED`.

### Phase 1.4: Deployment Target Selection

```markdown
## Deployment Target

Where would you like to deploy this application?

| Target | Description | Requirements |
|--------|-------------|--------------|
| **OpenShift** | Deploy to OpenShift/Kubernetes cluster | `oc login` access |
| **RHEL Host** | Deploy directly to a standalone RHEL system | SSH access to RHEL 8+ |

**Which target would you like to use?**
1. OpenShift - Deploy to current cluster
2. RHEL - Deploy to a RHEL host via SSH
```

Store `DEPLOYMENT_TARGET` in session state.

**WAIT for user confirmation before proceeding.**

**If user selects "RHEL":**
- Store `DEPLOYMENT_TARGET = "rhel"` in session state
- Delegate to `/rhel-deploy` skill with detected project info
- Pass: `APP_NAME`, `LANGUAGE`, `FRAMEWORK`, `VERSION`, `BUILDER_IMAGE`, `CONTAINER_PORT`
- The `/rhel-deploy` skill handles SSH connection, deployment strategy, and service creation
- After `/rhel-deploy` completes → Go to **Phase 8 (Completion)**

**If user selects "OpenShift":**
- Store `DEPLOYMENT_TARGET = "openshift"` in session state
- Continue to Phase 1.5 (Strategy Selection)

### Phase 1.5: Strategy Selection

If multiple deployment options are available (Helm chart detected, Dockerfile present, or standard project):

```markdown
## Deployment Strategy

Based on my analysis, you have these options:

| Strategy | Use When | Detected |
|----------|----------|----------|
| **S2I** | Standard apps, no Dockerfile needed | [Yes/No] |
| **Podman** | Custom Containerfile/Dockerfile exists | [Yes/No] |
| **Helm** | Helm chart exists or complex deployments | [Yes/No] |

**Detected in your project:**
[List what was found: language indicators, Dockerfile, Helm chart at ./chart]

**Which deployment strategy would you like to use?**
1. S2I - Build with Source-to-Image
2. Podman - Build from Containerfile/Dockerfile
3. Helm - Use existing Helm chart
4. Create Helm chart - Generate a new Helm chart for your project (if no chart exists)
```

Store `DEPLOYMENT_STRATEGY` in session state.

**WAIT for user confirmation before proceeding.**

### Phase 1.6: Image Selection (S2I/Podman only)

If user selected S2I or Podman deployment strategy, offer image selection options:

```markdown
## Image Selection

**Current recommendation:** `[builder-image]`
(Based on: [language] [version])

**Image Selection Options:**
- **quick** - Use the recommended image (good for most cases)
- **smart** - Run `/recommend-image` for tailored selection (production vs dev, security, performance)

Which option would you prefer?
```

**If user selects "smart":**
- Invoke `/recommend-image` skill with detected `LANGUAGE`, `FRAMEWORK`, `VERSION`
- Store the result in `BUILDER_IMAGE` and `IMAGE_VARIANT` session state
- Continue to Phase 2

**If user selects "quick":**
- Use the already-detected `BUILDER_IMAGE`
- Continue to Phase 2

**BRANCHING LOGIC:**
- If `DEPLOYMENT_STRATEGY` is **"S2I"** or **"Podman"** → After Phase 2, continue to **Phase 3 (S2I/Podman Path)**
- If `DEPLOYMENT_STRATEGY` is **"Helm"** → After Phase 2, go to **Phase 2-H (Helm Path)**

### Phase 1.7: Configuration Review (MANDATORY)

**This phase MUST NOT be skipped regardless of how the user responded to previous phases.**

```markdown
## Configuration Review

Before I proceed, let me confirm the deployment configuration:

**Environment Type:**
| Type | Characteristics |
|------|-----------------|
| **Development** | `latest` tags, lower resources, quick iteration |
| **Staging** | Version tags, moderate resources, testing |
| **Production** | Pinned versions, higher resources, HA-ready |

**Which environment is this deployment for?**
1. Development
2. Staging
3. Production

---

**Configuration Approach:**
| Approach | When to Use |
|----------|-------------|
| **Runtime config** | Need to change settings without rebuilding (Recommended for prod) |
| **Build-time config** | Simpler, settings baked into image (OK for dev) |

**How should environment variables be handled?**
1. Runtime (ConfigMap mount)
2. Build-time (baked into image)

---

**Resource Settings:**
| Setting | Dev Default | Prod Default |
|---------|-------------|--------------|
| Replicas | 1 | 2+ |
| CPU limit | 200m | 400m+ |
| Memory limit | 256Mi | 512Mi+ |

**Use defaults for your environment, or customize?**
1. Use defaults
2. Customize resources
```

**WAIT for user to answer ALL questions above before proceeding.**

Store: `ENVIRONMENT_TYPE`, `CONFIG_APPROACH`, `RESOURCE_PROFILE` in session state.

### Phase 2: OpenShift Connection

```markdown
## Phase 2: Connecting to OpenShift

Checking cluster connection...

**Current Context:**
| Setting | Value |
|---|---|
| Cluster | [cluster-api-url] |
| User | [username] |
| Namespace | [current-namespace] |

**Is this the correct cluster and namespace?**
- yes - Continue to build
- no - I need to change this

[If no]
**To change context:**
1. Run `oc login <new-cluster-url>` in your terminal
2. Or run `oc project <namespace>` to switch namespace
3. Then tell me to continue

**Available namespaces you have access to:**
[List first 10 namespaces/projects]

Which namespace should I deploy to?
```

Store confirmed `NAMESPACE` in session state.

---

## S2I/PODMAN PATH (If DEPLOYMENT_STRATEGY is "S2I" or "Podman")

### Phase 3: Git Repository Check

```markdown
## Git Repository

I need a Git URL for the S2I build.

**Detected from .git/config:**
- Remote: `[git-url]`
- Branch: `[current-branch]`

**Is this correct?** (yes/no)

[If no git config found]
**Please provide:**
1. Git repository URL (e.g., https://github.com/user/repo.git)
2. Branch name (default: main)
```

Store `GIT_URL` and `GIT_BRANCH` in session state.

### Phase 4: Pre-Build Summary

```markdown
## Phase 3: Build Configuration

Here's what I'll create on OpenShift:

**Target:**
- Cluster: [cluster]
- Namespace: [namespace]

**Resources to Create:**

1. **ImageStream** `[app-name]`
   - Stores built container images

2. **BuildConfig** `[app-name]`
   - Source: [git-url] (branch: [branch])
   - Builder: [builder-image]
   - Output: [app-name]:latest

---

**Would you like to see the full YAML?** (yes/no)

[If yes, show both YAML manifests]

---

**Proceed with creating these resources and starting the build?**
- yes - Create resources and start build
- modify - I need to change something
- cancel - Stop here
```

### Phase 5: Execute Build

```markdown
## Creating Build Resources...

[x] ImageStream created: [app-name]
[x] BuildConfig created: [app-name]

## Starting Build...

**Build:** [app-name]-1
**Status:** Running

---
**Build Logs:**
```
[Stream S2I build output]
```
---

[When complete]

## Build Successful!

**Build:** [app-name]-1
**Duration:** [X]m [Y]s
**Image:** [image-reference]

**CRITICAL: Wait for the build to reach 'Complete' status before proceeding.**

Continue to deployment? (yes/no)
```

### Phase 6: Pre-Deploy Summary

```markdown
## Phase 4: Deployment Configuration

**Image ready!** Now let's deploy it.

**Resources to Create:**

1. **Deployment** `[app-name]`
   - Image: [app-name]:latest
   - Replicas: 1
   - Port: [detected-port]

2. **Service** `[app-name]`
   - Internal load balancer
   - Port: [port]

3. **Route** `[app-name]`
   - External HTTPS access
   - URL: https://[app-name]-[namespace].[domain]

---

**Would you like to see the full YAML?** (yes/no)

[If yes, show all three YAML manifests]

---

**Proceed with deployment?**
- yes - Deploy the application
- modify - I need to change something
- cancel - Stop here (build artifacts preserved)
```

### Phase 7: Execute Deployment

```markdown
## Deploying Application...

[x] Deployment created: [app-name]
[x] Service created: [app-name]
[x] Route created: [app-name]

## Waiting for Rollout...

**Pod Status:**
| Pod | Status | Ready |
|-----|-----|---|
| [app-name]-xxx-yyy | Running | 1/1 |

Rollout complete!
```

**If rollout fails** (pods not ready, CrashLoopBackOff, ImagePullBackOff, etc.):

```markdown
## Deployment Failed

The deployment did not complete successfully.

**Pod Status:**
| Pod | Status | Ready | Restarts |
|-----|--------|-------|----------|
| [app-name]-xxx-yyy | [status] | 0/1 | [count] |

---

**Would you like me to diagnose the issue?**

1. **Debug Pod** (`/debug-pod`) - Investigate pod failures
2. **Debug Network** (`/debug-network`) - Check service/route connectivity
3. **Debug Build** (`/debug-build`) - Re-check build if image issues
4. **View logs manually**
5. **Rollback and stop**

Select an option:
```

- If user selects a debug option → Invoke the corresponding skill
- After debugging → Offer to retry deployment

---

## HELM PATH (If DEPLOYMENT_STRATEGY is "Helm")

### Phase 2-H: Helm Deployment

If user selected Helm in Phase 1.5, execute this path instead of Phases 3-7.

```markdown
## Helm Deployment

Switching to Helm deployment workflow...

The `/helm-deploy` skill will handle:
1. Validate the Helm chart
2. Review and customize values
3. Install/upgrade the release
4. Monitor deployment
5. Present results

Proceeding with Helm deployment...
```

**Delegate to `/helm-deploy` skill:**
- Pass `APP_NAME`, `NAMESPACE`, `HELM_CHART_PATH` from session state
- The helm-deploy skill handles chart detection, values review, and installation
- After helm-deploy completes → Go to **Phase 8 (Completion)**

**If user chose "Create Helm chart":**
- Generate chart using templates from templates/helm/
- Replace `${APP_NAME}` placeholders with detected app name
- Set `${CONTAINER_PORT}` based on detected port
- Then proceed with helm-deploy workflow

---

## COMPLETION (Both paths converge here)

### Phase 8: Completion

Present a summary including:
- Application name, namespace, language, framework
- Access URLs (external route, internal service DNS)
- Resources created with status (ImageStream, BuildConfig, Deployment, Service, Route)
- Quick commands: view logs, scale, rebuild, delete
- Next steps: open app URL, set up webhooks, add env vars, configure autoscaling

## Dependencies

### Required MCP Servers
- `openshift` - cluster resource management for OpenShift deployments

### Related Skills
- `/debug-pod` - Pod failures (CrashLoopBackOff, OOMKilled, ImagePullBackOff)
- `/debug-build` - S2I or Podman build failures
- `/debug-network` - Service connectivity issues (no endpoints, 503 errors)
- `/debug-rhel` - RHEL deployment failures (systemd, SELinux, firewall)

### Reference Documentation
- [docs/builder-images.md](docs/builder-images.md) - Language detection, S2I builder images
- [docs/image-selection-criteria.md](docs/image-selection-criteria.md) - Image variant selection, LTS timelines
- [docs/python-s2i-entrypoints.md](docs/python-s2i-entrypoints.md) - Python S2I configuration
- [docs/rhel-deployment.md](docs/rhel-deployment.md) - RHEL host deployment
- [docs/debugging-patterns.md](docs/debugging-patterns.md) - Common error patterns and troubleshooting
- [docs/prerequisites.md](docs/prerequisites.md) - All required tools by skill
