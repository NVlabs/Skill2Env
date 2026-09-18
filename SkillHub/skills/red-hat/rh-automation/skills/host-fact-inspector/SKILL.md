---
name: host-fact-inspector
description: |
  Correlate job failures with host system facts to determine platform drift and resource issues.

  Use when:
  - After job failure analysis identifies affected hosts
  - "Check the system facts for failed hosts"
  - "Is the host healthy?", "Check disk space on server-01"
  - "Why is the service failing on this host?"

  NOT for: analyzing job events (use job-failure-analyzer first) or resolution guidance (use resolution-advisor after).
model: inherit
color: blue
license: Apache-2.0
allowed-tools: hosts_list hosts_variable_data_retrieve
---

# Host Fact Inspector

## Prerequisites

**Required MCP Servers**:
- `aap-mcp-inventory-management` - Host details and variable data

**Verification**: Run the `aap-mcp-validator` skill with `aap-mcp-inventory-management` before proceeding.

## When to Use This Skill

Use this skill when:
- After `job-failure-analyzer` has identified which hosts and errors are involved
- User asks about host system state in the context of a failure
- As part of the forensic-troubleshooter workflow (Step 2)
- User asks to check host health or resource status

Do NOT use when:
- Analyzing job events (use `job-failure-analyzer` first)
- Getting resolution recommendations (use `resolution-advisor` after this skill)
- Executing jobs on hosts (use `execution-risk-analyzer` + `governed-job-launcher`)

## Workflow

### Step 1: Consult Troubleshooting Documentation

**CRITICAL**: Document consultation MUST happen BEFORE any MCP tool invocations.

**Document Consultation** (REQUIRED - Execute FIRST):
1. **Action**: Read [job-troubleshooting.md](docs/aap/job-troubleshooting.md) using the Read tool to understand the host fact correlation table and error-to-fact mapping
2. **Output to user**: "I consulted [job-troubleshooting.md](docs/aap/job-troubleshooting.md) to understand which host facts correlate with the identified failure patterns."

### Step 2: Look Up Affected Hosts

From the `job-failure-analyzer` output, identify the hostnames that experienced failures.

**MCP Tool**: `hosts_list` (from aap-mcp-inventory-management)
**Parameters**:
- `search`: `"<hostname_from_failure_analysis>"`
- `page_size`: `10`

Extract the host `id` from the results.

### Step 3: Retrieve Host Facts

**MCP Tool**: `hosts_variable_data_retrieve` (from aap-mcp-inventory-management)
**Parameters**:
- `id`: `"<host_id>"`
- `format`: `"json"`

This returns host variables which may include cached Ansible facts from the last `gather_facts` run.

### Step 4: Correlate Facts with Failure

Using the correlation table from job-troubleshooting.md, check the relevant facts based on the error pattern identified by `job-failure-analyzer`:

| Error Pattern | Host Fact to Check | What to Look For |
|---|---|---|
| "No space left on device" | `ansible_mounts[].size_available` | Disk utilization > 90% |
| "Unable to start service" | `ansible_service_mgr` | systemd vs sysvinit mismatch |
| Package not found | `ansible_distribution`, `ansible_distribution_version` | Wrong OS version for package |
| "Permission denied" | `ansible_user_id`, `ansible_become` | Privilege escalation not configured |
| "Connection timed out" | `ansible_default_ipv4` | Network misconfiguration |
| "Module not found" | `ansible_python_version` | Missing Python dependency |
| Out of memory | `ansible_memtotal_mb`, `ansible_memfree_mb` | Insufficient memory |

### Step 5: Generate Host Correlation Report

**Output format**:

```
## Host Fact Correlation: [hostname]

**Host ID**: [id]
**Last Facts Gathered**: [timestamp if available]

### System Profile
| Fact | Value |
|---|---|
| OS | [ansible_distribution] [ansible_distribution_version] |
| Kernel | [ansible_kernel] |
| Python | [ansible_python_version] |
| Service Manager | [ansible_service_mgr] |
| Total Memory | [ansible_memtotal_mb] MB |
| Available Memory | [ansible_memfree_mb] MB |

### Correlation with Failure

**Error**: "[error_message from failure analysis]"
**Relevant fact**: [fact_name] = [value]
**Correlation**: [Does this fact explain the failure?]

### Assessment

[Platform drift / Resource issue / Configuration gap / No correlation found]

Per Red Hat's *Troubleshooting Guide*: "[relevant guidance from job-troubleshooting.md]"
```

### Caveat: Stale Facts

Per job-troubleshooting.md: "Cached facts may be stale. If facts were gathered during a previous job run, they reflect the state at that time, not necessarily now."

If facts appear stale or missing, report this: "Host facts may not be current. For authoritative system state, consider running a fact-gathering job on this host."

## Dependencies

### Required MCP Servers
- `aap-mcp-inventory-management` - Host data and facts

### Required MCP Tools
- `hosts_list` (from inventory-management) - Look up host by name
- `hosts_variable_data_retrieve` (from inventory-management) - Retrieve host variables/facts

### Related Skills
- `job-failure-analyzer` - MUST run before this skill to identify affected hosts
- `resolution-advisor` - Next step: resolution recommendations based on correlation
- `execution-summary` - Audit trail

### Reference Documentation
- [job-troubleshooting.md](docs/aap/job-troubleshooting.md) - Host fact correlation table

## Example Usage

**User**: "Check the system facts for the host that failed in Job #4451"

**Agent**:
1. Reads job-troubleshooting.md
2. Reports: "I consulted job-troubleshooting.md to understand which host facts correlate with package installation failures."
3. Looks up host "web-prod-01" via `hosts_list`
4. Retrieves facts via `hosts_variable_data_retrieve`
5. Finds: `ansible_distribution: "CentOS"`, `ansible_distribution_version: "9"` -- package name is valid for CentOS 9
6. Checks disk: `ansible_mounts[0].size_available: 52428800` -- sufficient
7. Reports: "No host fact correlation found for the package error. This appears to be a code issue (wrong package name) rather than a platform issue."
