---
name: rhel-deploy
description: |
  CRITICAL: When user types /rhel-deploy, use THIS skill immediately. This skill deploys applications to standalone RHEL/Fedora/CentOS systems (NOT OpenShift) using Podman containers with systemd, or native dnf builds. Handles SSH connectivity, SELinux, firewall-cmd, and systemd unit creation. Triggers: /rhel-deploy command, 'deploy to RHEL', 'deploy to Fedora', 'deploy to my server via SSH'.
model: inherit
color: yellow
license: Apache-2.0
allowed-tools: inventory__find_host_by_name vulnerability__get_system_cves planning__get_rhel_lifecycle
metadata:
   user_invocable: "true"
---

# /rhel-deploy Skill

**IMPORTANT:** This skill is for deploying to standalone RHEL/Fedora/CentOS systems via SSH. If user invoked `/rhel-deploy`, skip any OpenShift-related steps and proceed directly with SSH-based deployment.

Deploy applications to standalone RHEL systems using Podman containers or native builds with systemd service management.

## Overview

```
[Intro] → [SSH Connect] → [Analyze] → [Strategy] ──┬─→ [Container Path] ──→ [Complete]
                                                   │   (Podman + systemd)
                                                   │
                                                   └─→ [Native Path] ─────→ [Complete]
                                                       (dnf + systemd)
```

**Deployment Strategies (user chooses one):**
- **Container** - Build/pull container image, run with Podman, manage with systemd
- **Native** - Install dependencies with dnf, run application directly, manage with systemd

## Prerequisites

1. SSH access to target RHEL host with sudo privileges
2. RHEL 8+, CentOS Stream, Rocky Linux, or Fedora
3. For container deployments: Podman installed on target
4. For native deployments: Required development tools available via dnf

## When to Use This Skill

Use `/rhel-deploy` when deploying applications to standalone RHEL, Fedora, or CentOS systems via SSH. This skill handles Podman container or native dnf deployments with systemd service management, SELinux, and firewall configuration.

## Critical: Human-in-the-Loop Requirements

See [Human-in-the-Loop Requirements](docs/human-in-the-loop.md) for mandatory checkpoint behavior.

## Workflow

### Phase 0: Introduction

Present the workflow overview: Connect → Analyze → Strategy → Build/Deploy → Verify. Describe Container (Podman + systemd) vs Native (dnf + systemd) strategies. Ask: **Ready to begin?** (yes/no)

**WAIT for user confirmation before proceeding.**

### Phase 1: SSH Connection

```markdown
## Phase 1: Connecting to RHEL Host

**SSH Target Configuration:**

Please provide your RHEL host details:

| Setting | Value | Default |
|---------|-------|---------|
| Host | [required] | - |
| User | [current user] | $USER |
| Port | 22 | 22 |

Example: `user@192.168.1.100` or `deploy@myserver.example.com`

**Enter your SSH target:**
```

**Connection verification:**

```bash
ssh -o BatchMode=yes -o ConnectTimeout=10 [user]@[host] "echo 'Connection successful'"
```

If connection fails, troubleshoot: host reachability, SSH key configuration, firewall port 22.

Store `RHEL_HOST`, `RHEL_USER`, `RHEL_PORT` in session state.

### Phase 2: Target Host Analysis

```markdown
## Phase 2: Analyzing Target Host

Checking capabilities of [host]...

| Setting | Value |
|---------|-------|
| OS | [cat /etc/redhat-release] |
| Kernel | [uname -r] |
| Architecture | [uname -m] |
| Podman | [Installed v4.x / Not installed] |
| SELinux | [Enforcing / Permissive / Disabled] |
| Firewall | [Active / Inactive] |

Is this the correct target host? (yes/no)
```

**WAIT for user confirmation before proceeding.**

**Commands to gather information:**

```bash
ssh [target] "cat /etc/redhat-release"
ssh [target] "podman --version 2>/dev/null || echo 'Not installed'"
ssh [target] "getenforce"
ssh [target] "firewall-cmd --state 2>/dev/null || echo 'Not running'"
```

Store `RHEL_VERSION`, `PODMAN_AVAILABLE`, `SELINUX_STATUS`, `FIREWALL_STATUS` in session state.

### Phase 2b: Red Hat Insights Pre-Deploy Check (Optional)

**This phase runs only if the `lightspeed-mcp` server is available.** Use `ToolSearch` to check for Lightspeed MCP tools. If not available, skip silently and proceed to Phase 3.

**Step 1:** Use `find_host_by_name` with the target hostname to look up the system in Red Hat Insights.

**Step 2:** If found, use `get_system_cves` to check for critical/important CVEs on the target.

**Step 3:** Use `get_rhel_lifecycle` to verify the target RHEL version is still supported.

Append to Phase 2 output:

```markdown
**Red Hat Insights (Optional):**
| Check | Status | Details |
|-------|--------|---------|
| Registered in Insights | [Yes/No] | [system-id or "Not found"] |
| RHEL Lifecycle | [Active/Maintenance/EOL] | [end date] |
| Critical/Important CVEs | [count] | [top 3 CVE IDs] |

[If critical CVEs found:]
**WARNING:** Target system has [N] critical/important CVEs. Consider remediating before deploying.

[If RHEL version is EOL:]
**WARNING:** RHEL [version] has reached End of Life ([date]). Consider upgrading before deploying.
```

These are informational warnings only — they do not block deployment.

### Phase 3: Strategy Selection

```markdown
## Deployment Strategy

Based on your project ([language]/[framework]) and target capabilities:

| Strategy | Description | Requirements |
|----------|-------------|--------------|
| **Container** | Build image, run with Podman + systemd | Podman installed |
| **Native** | Install with dnf, run directly + systemd | Runtime packages available |

**Recommendation:** [Container/Native] because [reason]

**Which deployment strategy would you like to use?**
1. Container - Deploy using Podman
2. Native - Deploy directly on host
```

**WAIT for user confirmation before proceeding.**

**If Podman not installed and user selects Container:**
```markdown
Podman is not installed on the target. Would you like me to install it?

```bash
sudo dnf install -y podman
```

Proceed with Podman installation? (yes/no)
```

**WAIT for user confirmation before proceeding.**

Store `DEPLOYMENT_STRATEGY` in session state.

---

## CONTAINER PATH (If DEPLOYMENT_STRATEGY is "Container")

### Phase 4a-1: Image Selection

```markdown
## Container Image

**Options:**

1. **Build on target** - Transfer source, build with Podman on RHEL host
2. **Build locally and transfer** - Build here, push to registry or transfer
3. **Use existing image** - Pull from registry (e.g., quay.io, docker.io)

Which approach would you prefer?
```

**WAIT for user confirmation before proceeding.**

**For options 1 and 2 (building an image):**

If no Containerfile/Dockerfile exists in the project, delegate to `/recommend-image`:

```markdown
## Selecting Base Image

To build your container, I need to select an appropriate base image.

Invoking `/recommend-image` to get the optimal UBI image for your [language]/[framework] project...
```

Use the `BUILDER_IMAGE` output from `/recommend-image` as the base image in the Containerfile.

**For build on target:**
```bash
# Transfer source and build
rsync -avz --exclude node_modules --exclude .git ./ [target]:/tmp/[app-name]-build/
# If no Containerfile exists, generate one using BUILDER_IMAGE from /recommend-image
ssh [target] "cd /tmp/[app-name]-build && podman build -t [app-name]:latest ."
```

**For existing image:**
```bash
ssh [target] "podman pull [image-reference]"
```

### Phase 4a-2: Container Configuration

```markdown
## Container Configuration

**Container Settings:**
| Setting | Value |
|---------|-------|
| Name | [app-name] |
| Image | [image-ref] |
| Port Mapping | [host-port]:[container-port] |
| Volume Mounts | [list any persistent data paths] |
| Environment | [list env vars] |
| Run Mode | [rootless / rootful] |

**SELinux Volume Labels:** Use `:z` for shared volumes, `:Z` for private volumes. See [docs/rhel-deployment.md](docs/rhel-deployment.md) for SELinux configuration details.

Proceed with this configuration? (yes/modify/cancel)
```

**WAIT for user confirmation before proceeding.**

### Phase 4a-3: Systemd Unit Creation

```markdown
## Systemd Service Configuration

Creating systemd unit for Podman container.

**Template to use:**
- Rootful: `templates/systemd/systemd-container-rootful.service`
- Rootless: `templates/systemd/systemd-container-rootless.service`

**Variables to substitute:**
| Variable | Value |
|----------|-------|
| `${APP_NAME}` | [app-name] |
| `${PORT}` | [container-port] |
| `${IMAGE}` | [container-image] |

**Target locations:**
- Rootful: `/etc/systemd/system/[app-name].service`
- Rootless: `~/.config/systemd/user/[app-name].service`

Proceed with creating this service? (yes/no)
```

**WAIT for user confirmation before proceeding.**

**Steps to execute:**

1. Read the appropriate template from `templates/systemd/`
2. Substitute `${APP_NAME}`, `${PORT}`, `${IMAGE}` with session state values
3. Transfer the generated unit file to the target host
4. Enable and start the service

```bash
# Rootful: transfer to /etc/systemd/system/, daemon-reload, enable --now
# Rootless: transfer to ~/.config/systemd/user/, daemon-reload, enable --now, enable-linger
ssh [target] "sudo systemctl daemon-reload && sudo systemctl enable --now [app-name]"
```

### Phase 4a-4: Firewall Configuration

```markdown
## Firewall Configuration

Opening port [port] for application access.

**Commands to execute:**
```bash
# Open port permanently
sudo firewall-cmd --permanent --add-port=[port]/tcp

# Reload firewall
sudo firewall-cmd --reload

# Verify
sudo firewall-cmd --list-ports
```

Proceed with firewall configuration? (yes/skip)
```

**WAIT for user confirmation before proceeding.**

---

## NATIVE PATH (If DEPLOYMENT_STRATEGY is "Native")

### Phase 4b-1: Dependency Installation

```markdown
## Installing Dependencies

**Runtime packages for [language]:**

See [docs/rhel-deployment.md](docs/rhel-deployment.md) for the complete runtime package mapping by language and RHEL version (Node.js, Python, Java, Go, Ruby, PHP).

**Commands to execute:**
```bash
ssh [target] "sudo dnf install -y [packages]"
```

Proceed with installation? (yes/no)
```

**WAIT for user confirmation before proceeding.**

### Phase 4b-2: Application Deployment

```markdown
## Deploying Application

**Deployment location:** `/opt/[app-name]`

**Steps:**
1. Create application directory
2. Transfer source code via rsync
3. Install application dependencies
4. Set ownership and permissions
5. Configure SELinux context

```bash
ssh [target] "sudo mkdir -p /opt/[app-name]"
rsync -avz --exclude node_modules --exclude .git --exclude __pycache__ ./ [target]:/tmp/[app-name]-deploy/
ssh [target] "sudo cp -r /tmp/[app-name]-deploy/* /opt/[app-name]/"
ssh [target] "cd /opt/[app-name] && npm install --production"  # language-specific
ssh [target] "sudo chown -R [service-user]:[service-user] /opt/[app-name]"
ssh [target] "sudo semanage fcontext -a -t bin_t '/opt/[app-name](/.*)?'"
ssh [target] "sudo restorecon -Rv /opt/[app-name]"
```

Proceed with deployment? (yes/no)
```

**WAIT for user confirmation before proceeding.**

### Phase 4b-3: Native Systemd Unit

```markdown
## Systemd Service Configuration

**Template to use:** `templates/systemd/systemd-native.service`

**Variables to substitute:**
| Variable | Value | Notes |
|----------|-------|-------|
| `${APP_NAME}` | [app-name] | Application name |
| `${SERVICE_USER}` | [service-user] | User to run the service as |
| `${APP_PATH}` | /opt/[app-name] | Application install path |
| `${PORT}` | [container-port] | Application listen port |
| `${START_COMMAND}` | [see below] | Language-specific start command |

**Start commands by language:** See [docs/rhel-deployment.md](docs/rhel-deployment.md) for language-specific systemd unit templates (Node.js, Python, Java, Go).

**Target location:** `/etc/systemd/system/[app-name].service`

**Note:** The template includes security hardening (NoNewPrivileges, ProtectSystem, ProtectHome, PrivateTmp).

Proceed with creating this service? (yes/no)
```

**WAIT for user confirmation before proceeding.**

**Steps to execute:**

1. Read the template from `templates/systemd/systemd-native.service`
2. Substitute all variables with session state values
3. Transfer the generated unit file to the target host
4. Enable and start the service

### Phase 4b-4: Firewall Configuration

Same as container path - open required port with firewall-cmd.

---

## COMPLETION (Both paths converge here)

### Phase 5: Completion

```markdown
## Deployment Complete!

Your application is now running on [host].

**Application Summary:**
| Setting | Value |
|---------|-------|
| Name | [app-name] |
| Host | [host] |
| Strategy | [Container/Native] |
| Service | [app-name].service |

**Access URLs:**
| Type | URL |
|------|-----|
| HTTP | http://[host]:[port] |
| SSH | ssh [user]@[host] |

**Service Status:** [systemctl status output]

**Quick Commands:**

Show quick commands for: view logs (journalctl), restart/stop/status (systemctl), container logs (if container), and removal steps.
```

### Phase 5a: Handle Deployment Failure

If the service fails to start or is not accessible:

```markdown
## Deployment Failed

The service did not start successfully.

**Service Status:** [systemctl status output showing failure]

**Recent Errors:**
| Time | Error |
|------|-------|
| [time] | [error from journalctl] |

**Would you like me to diagnose the issue?**
1. **Debug RHEL** (`/debug-rhel`) - Full system diagnosis (systemd, journal, SELinux, firewall)
2. **Debug Container** (`/debug-container`) - Container state, logs, exit codes
3. **View full logs** - Complete journalctl output
4. **Check SELinux** - Quick SELinux denial check
5. **Check firewall** - Quick firewall port check
6. **Stop and clean up**

Select an option:
```

**WAIT for user to select an option.**

- If user selects "Debug RHEL" → Invoke `/debug-rhel` skill
- If user selects "Debug Container" → Invoke `/debug-container` skill
- After debugging → Offer to retry deployment

## Dependencies

### Required MCP Servers
- `lightspeed-mcp` (optional) - Red Hat Insights pre-deploy checks

### Related Skills
- `/debug-rhel` - systemd failures, SELinux denials, firewall blocking
- `/debug-container` - Container startup issues on RHEL host

### Reference Documentation
- [docs/rhel-deployment.md](docs/rhel-deployment.md) - Systemd templates, SELinux, firewall, runtime packages
- [docs/selinux-troubleshooting.md](docs/selinux-troubleshooting.md) - SELinux denial analysis and fixes
- [docs/debugging-patterns.md](docs/debugging-patterns.md) - Common error patterns and troubleshooting
- [docs/prerequisites.md](docs/prerequisites.md) - Required tools (ssh, podman)
