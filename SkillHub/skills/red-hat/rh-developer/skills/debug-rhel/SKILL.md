---
name: debug-rhel
description: |
  Diagnose RHEL system issues including systemd service failures, SELinux denials, firewall blocking, and system resource problems. Automates multi-step diagnosis: journalctl log analysis, SELinux denial detection (ausearch), firewall rule inspection, and systemd unit status. Use this skill when applications fail on standalone RHEL/Fedora/CentOS hosts deployed via /rhel-deploy. Triggers on /debug-rhel command or phrases like "service won't start on RHEL", "SELinux blocking", "systemd failed", "firewall blocking".
model: inherit
color: cyan
license: Apache-2.0
allowed-tools: inventory__find_host_by_name vulnerability__get_system_cves advisor__get_active_rules advisor__get_rule_by_text_search
metadata:
  user_invocable: "true"
---

# /debug-rhel Skill

Diagnose RHEL system issues by automatically gathering systemd status, journal logs, SELinux denials, and firewall configuration.

## Overview

```
[Connect] → [Identify Service] → [systemd Status] → [Journal Logs] → [SELinux] → [Firewall] → [Summary]
```

**This skill diagnoses:**
- systemd service failures
- SELinux access denials (AVC)
- Firewall port blocking
- Permission issues
- Resource constraints

## Prerequisites

1. SSH access to target RHEL host
2. sudo privileges on the target host
3. RHEL 8+, CentOS Stream, Rocky Linux, or Fedora

## Critical: Human-in-the-Loop Requirements

See [Human-in-the-Loop Requirements](docs/human-in-the-loop.md) for mandatory checkpoint behavior.

## Note: SSH/Bash Required

This skill operates on **remote RHEL hosts** via SSH, not local MCP servers. Unlike OpenShift/Podman skills, direct Bash commands with SSH are the correct approach here since MCP servers run locally and cannot access remote systems.

## When to Use This Skill

Use `/debug-rhel` when applications fail on standalone RHEL, Fedora, or CentOS hosts. This skill automates multi-step diagnosis of systemd service failures, SELinux denials, firewall blocking, and system resource problems via SSH.

## Workflow

### Phase 1: SSH Connection

```markdown
## RHEL System Debugging

I'll help you diagnose issues on your RHEL system.

**SSH Target:**
[If RHEL_HOST in session state from /rhel-deploy:]
- Using previous connection: [user]@[host]

Is this correct? (yes/no/different host)

[If no RHEL_HOST:]
Please provide your RHEL host details:

| Setting | Value | Default |
|---------|-------|---------|
| Host | [required] | - |
| User | [current user] | $USER |
| Port | 22 | 22 |

**Enter your SSH target:**
```

**WAIT for user to confirm or provide host.**

**Connection verification:**

```bash
# Test SSH connection
ssh -o BatchMode=yes -o ConnectTimeout=10 [user]@[host] "echo 'Connection successful'"
```

If connection fails:
```markdown
**SSH Connection Failed**

Unable to connect to [host].

**Troubleshooting:**
1. Check host is reachable: `ping [host]`
2. Verify SSH key is configured: `ssh-add -l`
3. Check firewall allows SSH: port 22
4. Verify username is correct

Would you like to:
1. Try a different host
2. Get help with SSH setup
3. Exit
```

### Phase 2: Identify Target Service

```markdown
## Phase 2: Identify Service

Which service would you like me to debug?

1. **Specify service name** - Enter the systemd unit name
2. **List failed services** - Show failed services on the host
3. **From /rhel-deploy** - Debug the last deployed service

Select an option or enter a service name:
```

**WAIT for user response.**

If user selects "List failed services":

```bash
# Get failed services
ssh [user]@[host] "systemctl --failed --no-pager"
```

```markdown
## Failed Services on [host]

| Unit | Load | Active | Sub | Description |
|------|------|--------|-----|-------------|
| [myapp.service] | loaded | failed | failed | My Application |
| [other.service] | loaded | failed | failed | Other Service |

Which service would you like me to debug?
```

**WAIT for user to select a service.**

### Phase 3: Get Service Status

```bash
# Get detailed service status
ssh [user]@[host] "systemctl status [service] --no-pager -l"
```

```markdown
## Service Status: [service-name]

**Status Overview:**
| Field | Value |
|-------|-------|
| Loaded | [loaded/not-found/masked] |
| Active | [active (running)/inactive (dead)/failed] |
| Main PID | [pid or N/A] |
| Status | [status text] |
| Since | [timestamp] |

**Recent Activity:**
```
[systemctl status output - last 10 lines]
```

**Quick Assessment:**
[Based on status, provide initial assessment - e.g., "Service failed to start - exit code 1 suggests application error"]

Continue with journal logs? (yes/no)
```

**WAIT for user confirmation before proceeding.**

### Phase 4: Analyze Journal Logs

```bash
# Get service logs
ssh [user]@[host] "journalctl -u [service] -n 100 --no-pager"
```

```markdown
## Journal Logs: [service-name]

**Last 100 log entries:**
```
[journalctl output]
```

**Log Analysis:**

[Analyze logs and identify errors:]

**Errors Found:**
- [timestamp]: [error - e.g., "Permission denied: /var/data/config.yaml"]
- [timestamp]: [error - e.g., "Connection refused: localhost:5432"]
- [timestamp]: [error - e.g., "Port 8080 already in use"]

**Error Categories:**
| Category | Count | Example |
|----------|-------|---------|
| Permission | [X] | [first occurrence] |
| Connection | [Y] | [first occurrence] |
| Resource | [Z] | [first occurrence] |

Continue to check SELinux? (yes/no/skip)
```

**WAIT for user confirmation before proceeding.**

### Phase 5: Check SELinux Denials

```bash
# Check SELinux status
ssh [user]@[host] "getenforce"

# Get recent AVC denials
ssh [user]@[host] "sudo ausearch -m AVC -ts recent 2>/dev/null || echo 'No recent denials or ausearch not available'"
```

```markdown
## SELinux Analysis

**SELinux Status:** [Enforcing/Permissive/Disabled]

**Recent AVC Denials:**

[If denials found:]
| Time | Source | Target | Permission | Denied |
|------|--------|--------|------------|--------|
| [time] | [source_context] | [target_context] | [permission] | [target_file] |
| [time] | [source_context] | [target_context] | [permission] | [target_port] |

**Denial Analysis:**

**Denial 1: [description]**
- **What happened:** Process `[name]` tried to [action] on `[target]`
- **Why denied:** SELinux type `[source_type]` cannot [action] `[target_type]`
- **Impact:** [how this affects the application]

**Recommended Fixes:**

1. **Set SELinux boolean** (if applicable):
   ```bash
   sudo setsebool -P [boolean_name] on
   ```

2. **Change file context** (if file access):
   ```bash
   sudo semanage fcontext -a -t [correct_type] "[path](/.*)?"
   sudo restorecon -Rv [path]
   ```

3. **Allow port** (if port binding):
   ```bash
   sudo semanage port -a -t [port_type] -p tcp [port]
   ```

[If no denials:]
No recent SELinux denials found. SELinux is likely not the issue.

Continue to check firewall? (yes/no/skip)
```

**WAIT for user confirmation before proceeding.**

### Phase 6: Check Firewall

```bash
# Get firewall status
ssh [user]@[host] "sudo firewall-cmd --state 2>/dev/null || echo 'firewalld not running'"

# List firewall rules
ssh [user]@[host] "sudo firewall-cmd --list-all 2>/dev/null"
```

```markdown
## Firewall Analysis

**Firewall Status:** [running/not running]

**Active Zone:** [zone-name]

**Current Rules:**
| Type | Value |
|------|-------|
| Services | [ssh, http, https, ...] |
| Ports | [8080/tcp, 3000/tcp, ...] |
| Rich Rules | [count] |

**Application Port:** [detected-port from logs/config]

**Port Status:**
| Port | Protocol | Status |
|------|----------|--------|
| [8080] | TCP | [OPEN/BLOCKED] |
| [443] | TCP | [OPEN/BLOCKED] |

[If port blocked:]
**WARNING: Application port [port] is NOT open in firewall!**

**To open port:**
```bash
sudo firewall-cmd --permanent --add-port=[port]/tcp
sudo firewall-cmd --reload
```

**Or add service:**
```bash
sudo firewall-cmd --permanent --add-service=[service]
sudo firewall-cmd --reload
```

Continue to diagnosis summary? (yes/no)
```

**WAIT for user confirmation before proceeding.**

### Phase 7: Red Hat Insights Check (Optional)

**This phase runs only if the `lightspeed-mcp` server is available.** Use `ToolSearch` to check for Lightspeed MCP tools. If not available, skip this phase silently and proceed to Phase 8.

**Step 1:** Use `find_host_by_name` with the hostname from `RHEL_HOST` to look up the system in Red Hat Insights.

**Step 2:** If system found, use `get_system_cves` with the system ID to check for known CVEs affecting this system.

**Step 3:** Use `get_active_rules` to get advisor configuration recommendations. Optionally use `get_rule_by_text_search` with error text found in Phase 4 logs to find relevant advisor recommendations.

```markdown
## Red Hat Insights Check

**System in Insights:** [Found / Not registered]

[If found:]
**System Details:**
| Field | Value |
|-------|-------|
| Display Name | [hostname] |
| RHEL Version | [version] |
| Last Check-in | [timestamp] |
| Stale | [yes/no] |

**Known Vulnerabilities:**
| CVE | CVSS | Severity | Remediation |
|-----|------|----------|-------------|
| [CVE-ID] | [score] | [severity] | [Available/None] |

**Advisor Recommendations:**
| Rule | Category | Risk | Description |
|------|----------|------|-------------|
| [rule-id] | [Security/Performance/Availability/Stability] | [Critical/Important/Moderate/Low] | [description] |

[If any CVE or advisor rule matches the symptoms from earlier phases:]
**Potentially Related to Current Issue:**
- [CVE or advisor rule that matches the symptoms]

Continue to diagnosis summary? (yes/no)
```

**WAIT for user confirmation before proceeding.**

[If system not registered in Insights, just note it:]
```markdown
## Red Hat Insights Check

System [hostname] is not registered in Red Hat Insights. Skipping vulnerability and advisor checks.

Continue to diagnosis summary? (yes/no)
```

### Phase 8: Present Diagnosis Summary

```markdown
## Diagnosis Summary: [service-name] on [host]

### Root Cause

**Primary Issue:** [Categorized root cause]

| Category | Status | Details |
|----------|--------|---------|
| Service Unit | [OK/FAIL] | [loaded/enabled status] |
| Application | [OK/FAIL] | [exit code, error] |
| SELinux | [OK/BLOCKED] | [denial count] |
| Firewall | [OK/BLOCKED] | [port status] |
| Permissions | [OK/FAIL] | [file/dir issues] |
| Resources | [OK/FAIL] | [memory/cpu/disk] |
| Insights/CVE | [OK/WARN/N/A] | [CVE count or "Not registered"] |

### Detailed Findings

**[Category 1: e.g., SELinux Denial]**
- Problem: [specific problem - e.g., "httpd_t cannot bind to port 8080"]
- Evidence: [AVC denial message]
- Impact: [application cannot start]

**[Category 2: e.g., Missing Dependency]**
- Problem: [specific problem - e.g., "libpq.so.5 not found"]
- Evidence: [error from logs]
- Impact: [application crashes on startup]

### Recommended Actions

1. **[Action 1 - Highest Priority]** - [description]
   ```bash
   ssh [user]@[host] "[command]"
   ```

2. **[Action 2]** - [description]
   ```bash
   ssh [user]@[host] "[command]"
   ```

3. **[Action 3]** - [description]
   ```bash
   ssh [user]@[host] "[command]"
   ```

### Verify Fix

After applying fixes:
```bash
# Restart service
ssh [user]@[host] "sudo systemctl restart [service]"

# Check status
ssh [user]@[host] "systemctl status [service]"

# View logs
ssh [user]@[host] "journalctl -u [service] -f"
```

---

Would you like me to:
1. Execute one of the recommended fixes
2. Dig deeper into a specific area
3. Restart the service
4. View live logs
5. Exit debugging

Select an option:
```

**WAIT for user to select next action.**

For common RHEL issues (systemd exit codes, SELinux denials, firewall), see [debugging-patterns.md](docs/debugging-patterns.md) and [selinux-troubleshooting.md](docs/selinux-troubleshooting.md).

## Dependencies

### Required MCP Servers
- `lightspeed-mcp` (optional) - Red Hat Insights CVE and advisor checks in Phase 7

### Related Skills
- `/rhel-deploy` - redeploy after fixing issues
- `/debug-container` - debug Podman containers on the host

### Reference Documentation
- [docs/selinux-troubleshooting.md](docs/selinux-troubleshooting.md) - SELinux denial analysis
- [docs/rhel-deployment.md](docs/rhel-deployment.md) - RHEL deployment patterns
- [docs/debugging-patterns.md](docs/debugging-patterns.md) - Common error patterns
- [docs/prerequisites.md](docs/prerequisites.md) - Required tools and setup
