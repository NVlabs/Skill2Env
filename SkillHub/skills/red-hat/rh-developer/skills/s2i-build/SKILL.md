---
name: s2i-build
description: |
  Create BuildConfig and ImageStream resources on OpenShift and trigger a Source-to-Image (S2I) build. Use this skill after /detect-project to build container images from source code on the cluster. Handles namespace verification, resource creation with user confirmation, build monitoring with log streaming, and failure recovery. Triggers on /s2i-build command. Run before /deploy.
model: inherit
color: green
license: Apache-2.0
allowed-tools: resources_list resources_create_or_update pods_log
metadata:
   user_invocable: "true"
---

# /s2i-build Skill

Create the necessary OpenShift resources (BuildConfig, ImageStream) and trigger a Source-to-Image build on the cluster.

## Prerequisites

Before running this skill, ensure:
1. User is logged into OpenShift cluster
2. Target namespace/project exists or can be created
3. Git repository URL is available (or will use binary build)

## When to Use This Skill

Use this skill after `/detect-project` to build container images from source code on OpenShift using Source-to-Image. It creates BuildConfig and ImageStream resources, triggers the build, and monitors progress with log streaming.

## Critical: Human-in-the-Loop Requirements

See [Human-in-the-Loop Requirements](docs/human-in-the-loop.md) for mandatory checkpoint behavior.

## Workflow

### Step 1: Check OpenShift Connection

Use kubernetes MCP to verify connection:

```markdown
## Checking OpenShift Connection...

**Cluster:** [cluster-url from kubeconfig]
**User:** [current user]
**Current Namespace:** [current namespace]

Is this the correct cluster and namespace for the build?
- yes - Continue
- no - Let me switch context
```

**WAIT for user confirmation before proceeding.**

### Step 2: Gather Build Information

Collect required information (from /detect-project or ask user):

```markdown
## S2I Build Configuration

I need the following information:

| Setting | Current Value | Source |
|---------|---------------|--------|
| App Name | `[name]` | [from detect-project / folder name] |
| Git URL | `[url]` | [from .git/config / needs input] |
| Git Branch | `main` | [default] |
| S2I Builder | `[image]` | [from detect-project / needs input] |
| Namespace | `[ns]` | [from current context] |

[For Python projects only - include these rows if PYTHON_ENTRY_FILE is set]
| Entry Point | `[PYTHON_ENTRY_FILE]` | [from detect-project] |
| APP_MODULE | `[PYTHON_APP_MODULE]` | [Python only - required if entry point != app.py] |
| gunicorn | [Found / Missing] | [from detect-project] |

Please confirm these values or tell me what to change.
```

**Python Entry Point Warning:**

If `PYTHON_ENTRY_FILE` is NOT `app.py` AND `PYTHON_HAS_GUNICORN` is `false`:

```markdown
## Python Configuration Issue

Your application uses `[PYTHON_ENTRY_FILE]` as entry point, but `gunicorn` is not in your requirements.

**This build will FAIL** because:
- The S2I Python builder requires `gunicorn` to use `APP_MODULE`
- Without gunicorn, it looks for `app.py` (which doesn't exist)

**Please choose:**
1. **Add gunicorn** - Add `gunicorn` to requirements.txt and retry
2. **Rename entry point** - Rename `[main.py]` to `app.py`
3. **Continue anyway** - Proceed (build will likely fail)
```

**WAIT for user confirmation before proceeding.**

**To detect Git URL:**
- Read `.git/config` and extract `[remote "origin"]` url

### Step 3: Verify Namespace

Use kubernetes MCP `resources_list` to check if namespace exists:

```markdown
## Namespace Check

Checking if namespace `[namespace]` exists...

[If exists]
Namespace `[namespace]` exists and you have access.

[If not exists]
Namespace `[namespace]` does not exist.

Would you like me to create it? (yes/no)
```

**WAIT for user confirmation before proceeding.**

If creating namespace, use `resources_create_or_update`:
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: [namespace]
```

### Step 4: Create ImageStream

Show the ImageStream that will be created:

```markdown
## Step 1 of 3: Create ImageStream

An ImageStream stores references to your built container images.

```yaml
apiVersion: image.openshift.io/v1
kind: ImageStream
metadata:
  name: [app-name]
  namespace: [namespace]
  labels:
    app: [app-name]
    app.kubernetes.io/name: [app-name]
spec:
  lookupPolicy:
    local: false
```

**Proceed with creating this ImageStream?** (yes/no)
```

**WAIT for user confirmation before proceeding.**

### Step 5: Create BuildConfig

Show the BuildConfig:

**For non-Python projects OR Python with app.py entry point:**

```markdown
## Step 2 of 3: Create BuildConfig

A BuildConfig defines how to build your application using S2I.

```yaml
apiVersion: build.openshift.io/v1
kind: BuildConfig
metadata:
  name: [app-name]
  namespace: [namespace]
  labels:
    app: [app-name]
    app.kubernetes.io/name: [app-name]
spec:
  source:
    type: Git
    git:
      uri: [git-url]
      ref: [git-branch]
  strategy:
    type: Source
    sourceStrategy:
      from:
        kind: DockerImage
        name: [builder-image]
  output:
    to:
      kind: ImageStreamTag
      name: [app-name]:latest
  triggers:
    - type: ConfigChange
    - type: ImageChange
  runPolicy: Serial
```

**This BuildConfig will:**
- Pull source from: `[git-url]` (branch: `[git-branch]`)
- Build using S2I with: `[builder-image]`
- Push result to: `[app-name]:latest` ImageStream

**Proceed with creating this BuildConfig?** (yes/no)
```

**For Python projects with non-default entry point (e.g., main.py):**

```markdown
## Step 2 of 3: Create BuildConfig

A BuildConfig defines how to build your application using S2I.

```yaml
apiVersion: build.openshift.io/v1
kind: BuildConfig
metadata:
  name: [app-name]
  namespace: [namespace]
  labels:
    app: [app-name]
    app.kubernetes.io/name: [app-name]
spec:
  source:
    type: Git
    git:
      uri: [git-url]
      ref: [git-branch]
  strategy:
    type: Source
    sourceStrategy:
      from:
        kind: DockerImage
        name: [builder-image]
      # Python S2I: Required when entry point is not app.py
      env:
        - name: APP_MODULE
          value: "[PYTHON_APP_MODULE]"  # e.g., "main:app"
  output:
    to:
      kind: ImageStreamTag
      name: [app-name]:latest
  triggers:
    - type: ConfigChange
    - type: ImageChange
  runPolicy: Serial
```

**This BuildConfig will:**
- Pull source from: `[git-url]` (branch: `[git-branch]`)
- Build using S2I with: `[builder-image]`
- Push result to: `[app-name]:latest` ImageStream

**Python Entry Point Configuration:**
- Entry point file: `[PYTHON_ENTRY_FILE]`
- APP_MODULE: `[PYTHON_APP_MODULE]`
- This tells the S2I Python builder how to start your application with gunicorn.

**Proceed with creating this BuildConfig?** (yes/no)
```

**WAIT for user confirmation before proceeding.**

### Step 6: Start Build

```markdown
## Step 3 of 3: Start Build

Resources created successfully!

| Resource | Name | Status |
|----------|------|--------|
| ImageStream | [app-name] | Created |
| BuildConfig | [app-name] | Created |

**Would you like me to start a build now?** (yes/no)

(You can also trigger builds later with: oc start-build [app-name])
```

**WAIT for user confirmation before proceeding.**

If yes, create a Build resource:
```yaml
apiVersion: build.openshift.io/v1
kind: Build
metadata:
  generateName: [app-name]-
  namespace: [namespace]
  labels:
    app: [app-name]
    buildconfig: [app-name]
  annotations:
    openshift.io/build-config.name: [app-name]
spec:
  serviceAccount: builder
  source:
    type: Git
    git:
      uri: [git-url]
      ref: [git-branch]
  strategy:
    type: Source
    sourceStrategy:
      from:
        kind: DockerImage
        name: [builder-image]
  output:
    to:
      kind: ImageStreamTag
      name: [app-name]:latest
  triggeredBy:
    - message: Manually triggered
```

### Step 7: Monitor Build

Stream build logs using kubernetes MCP `pods_log`:

```markdown
## Build Progress

**Build:** [app-name]-1
**Status:** Running
**Phase:** [current phase]

---
[Streaming build logs here]
---

[When complete]

## Build Complete!

**Build:** [app-name]-1
**Status:** Complete
**Duration:** [X]m [Y]s
**Image:** image-registry.openshift-image-registry.svc:5000/[namespace]/[app-name]:latest

**CRITICAL: Ensure the build status is 'Complete' before proceeding to deployment.**

The image is ready for deployment.
Run `/deploy` to create Deployment, Service, and Route.
```

### Step 8: Handle Build Failure

If build fails:

```markdown
## Build Failed

**Build:** [app-name]-1
**Status:** Failed
**Phase:** [phase where it failed]

**Error:**
```
[Last 20 lines of build log]
```

**Common causes for [phase] failure:**
- [relevant troubleshooting tips]

**Options:**
1. **Debug Build** (`/debug-build`) - Full build diagnosis
   - Analyzes BuildConfig, build logs, source access, registry auth
   - Identifies root cause and suggests remediation
2. View full build logs
3. Delete failed build and retry
4. Update BuildConfig and retry
5. Cancel and troubleshoot

What would you like to do?
```

- If user selects "Debug Build" → Invoke `/debug-build` skill with build name
- After debugging → Offer to retry build

## Dependencies

### Required MCP Servers
- `openshift` - Kubernetes/OpenShift resource access for BuildConfigs, ImageStreams, and build monitoring

### Related Skills
- `/debug-build` - Build failures (source access, dependencies, registry issues)
- `/deploy` - After successful build, to deploy the image

### Reference Documentation
- [docs/builder-images.md](docs/builder-images.md) - S2I builder image selection, version mapping
- [docs/python-s2i-entrypoints.md](docs/python-s2i-entrypoints.md) - Python APP_MODULE configuration, entry point troubleshooting
- [docs/debugging-patterns.md](docs/debugging-patterns.md) - Common build error patterns and troubleshooting
- [docs/prerequisites.md](docs/prerequisites.md) - Required tools (oc)
