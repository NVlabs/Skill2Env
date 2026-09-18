---
name: governed-job-launcher
description: |
  Execute governed job launches with check mode, approval gates, phased rollout, and rollback.

  Use when:
  - After execution-risk-analyzer has classified the execution risk
  - "Launch with check mode first", "Run the dry run"
  - "Execute the job" (after risk analysis)
  - "Rollback the failed job"

  NOT for: risk analysis (use execution-risk-analyzer first) or troubleshooting (use job-failure-analyzer).
model: inherit
color: red
license: Apache-2.0
allowed-tools: job_templates_launch_create jobs_retrieve jobs_job_events_list jobs_job_host_summaries_list jobs_relaunch_create
---

# Governed Job Launcher

## Prerequisites

**Required MCP Servers**:
- `aap-mcp-job-management` - Job launch, monitoring, events, relaunch

**Verification**: Run the `aap-mcp-validator` skill with `aap-mcp-job-management` before proceeding.

**IMPORTANT**: This skill assumes the `execution-risk-analyzer` skill has already been executed and its risk assessment is available. Do NOT launch jobs without prior risk analysis for CRITICAL or HIGH risk targets.

## When to Use This Skill

Use this skill when:
- After `execution-risk-analyzer` has completed risk assessment
- Risk level has been determined and governance controls are known
- User has been informed of risk and is ready to proceed

Do NOT use when:
- Risk analysis hasn't been performed yet (run `execution-risk-analyzer` first)
- Troubleshooting a failed job (use `job-failure-analyzer` skill)
- Assessing platform readiness (use `governance-readiness-assessor` skill)

## Workflow

### Step 1: Consult Execution Governance Documentation

**CRITICAL**: Document consultation MUST happen BEFORE any MCP tool invocations.

**Document Consultation** (REQUIRED - Execute FIRST):
1. **Action**: Read [execution-governance.md](docs/aap/execution-governance.md) using the Read tool to understand check mode execution, interpretation, phased rollout, and rollback patterns
2. **Output to user**: "I consulted [execution-governance.md](docs/aap/execution-governance.md) to understand Red Hat's check mode behavior, rollback patterns, and phased rollout strategy."

### Step 2: Adapt Execution Strategy Based on Risk Signals

Before launching, incorporate the operational signals from the `execution-risk-analyzer` skill's report. The launcher adapts its behavior based on what was discovered:

**2a. If risk analyzer flagged recent failures**:
- Present the failure context to the user before proceeding: "The risk analyzer found that the last [N] runs of this template failed. Would you like to investigate the most recent failure first (using forensic-troubleshooter), or proceed with the execution?"
- If user wants to investigate → hand off to `forensic-troubleshooter` skill
- If user wants to proceed → continue with elevated caution

**2b. If risk analyzer flagged check mode not overridable** (`ask_job_type_on_launch: false`):
- Cannot enforce check mode at launch time
- Inform user: "This template does not allow job_type override. Check mode cannot be enforced without modifying the template. Proceeding directly to full execution with extra scrutiny."
- For CRITICAL risk: Recommend modifying the template first. If user declines, proceed but document the governance exception.

**2c. If risk analyzer flagged shell/command modules**:
- Elevate the check mode warning from generic to specific in Step 4: "This playbook uses [X] shell/command tasks that check mode will SKIP. Only [Y] of [Z] total tasks were validated in this dry run."

**2d. If risk analyzer flagged no notifications**:
- After successful execution, proactively recommend: "This template has no failure notifications. Per Red Hat's Ch. 25, consider adding failure notifications now that the execution succeeded."

**2e. If risk analyzer flagged standalone template (no workflow)**:
- For CRITICAL risk: Recommend wrapping in a workflow before proceeding. If user declines, proceed but document the governance exception.

### Step 3: Execute Based on Risk Level

#### For CRITICAL / HIGH Risk: Check Mode First

**MCP Tool**: `job_templates_launch_create` (from aap-mcp-job-management)
**Parameters**:
- `id`: `"<template_id>"`
- `requestBody`:
  - `job_type`: `"check"`
  - `diff_mode`: `true`
  - `extra_vars`: (from user/template, if any)
  - `limit`: (if scoping to specific hosts)

Per Red Hat's *Job Templates documentation* (Ch. 9): The `job_type` field supports `"check"` mode for dry-run execution, and `diff_mode` shows what would change.

**If check mode not overridable** (from Step 2b): Skip directly to full execution with elevated human-in-the-loop controls.

#### For MEDIUM Risk: Direct with Confirmation

Ask user for confirmation, then launch directly with `job_type: "run"`.

#### For LOW Risk: Direct Execution

Launch with `job_type: "run"` directly (user has already been informed by risk analyzer).

### Step 4: Monitor Job Progress

Poll job status until completion:

**MCP Tool**: `jobs_retrieve` (from aap-mcp-job-management)
**Parameters**:
- `id`: `"<job_id>"`

Poll every few seconds. Status values: `pending`, `waiting`, `running`, `successful`, `failed`, `error`, `canceled`.

### Step 5: Interpret Check Mode Results (CRITICAL/HIGH only)

After check mode completes, retrieve results:

**MCP Tool**: `jobs_job_host_summaries_list` (from aap-mcp-job-management)
**Parameters**:
- `id`: `"<check_mode_job_id>"`

**MCP Tool**: `jobs_job_events_list` (from aap-mcp-job-management)
**Parameters**:
- `id`: `"<check_mode_job_id>"`
- `page_size`: `100`

**Interpretation** (per execution-governance.md):

| Host Summary | Meaning | Action |
|---|---|---|
| `failures > 0` | Tasks would fail | **STOP** -- report failures, do NOT proceed |
| `dark > 0` | Hosts unreachable | **STOP** -- connectivity issue |
| `changed > 0`, `failures = 0` | Changes would be applied successfully | Present findings, ask for approval |
| `ok > 0`, `changed = 0` | Already in desired state | Report: "No changes needed" |

**Shell/command module warning** (adapted based on risk analyzer findings):

- **If risk analyzer detected shell/command modules** (Step 2c): Use the specific warning with task counts: "This playbook uses [X] shell/command tasks (identified from previous run analysis). These [X] tasks were SKIPPED in check mode and were NOT validated. Only [Y] of [Z] total tasks were covered by this dry run."
- **If no prior run data available**: Use generic warning: "Tasks using shell/command modules are skipped in check mode per Ansible documentation and were NOT validated."

**Output to user**:

```
## Check Mode Results — Job #[job_id]

**Status**: [successful/failed]
**Dry-Run Coverage**: [Y] of [Z] tasks validated ([percentage]%) [only if module data available from risk analyzer]

### Host Summary
| Host | OK | Changed | Failed | Unreachable | Skipped |
|---|---|---|---|---|---|
| [host] | [ok] | [changed] | [failures] | [dark] | [skipped] |

### Check Mode Findings
- [X] tasks would make changes
- [Y] tasks would fail
- [Z] tasks were skipped (shell/command — NOT validated)

### Operational Context [from risk analyzer signals]
- Job History: [last run status — clear/failed/first run]
- Notifications: [configured/not configured — silent failures if not]
- Workflow: [wrapped/standalone]

### Recommendation
[Based on results AND operational context: proceed / stop / investigate]

⚠️ [Specific or generic check mode warning based on available data]

**Proceed with full execution?** (yes/no)
```

### Step 6: Full Execution (After Approval)

#### Standard Execution (HIGH risk or below)

**MCP Tool**: `job_templates_launch_create` (from aap-mcp-job-management)
**Parameters**:
- `id`: `"<template_id>"`
- `requestBody`:
  - `job_type`: `"run"`
  - `extra_vars`: (same as check mode)

#### Phased Rollout (CRITICAL risk)

Per execution-governance.md, CRITICAL risk executions use phased rollout:

**Phase 1 - Canary**:
```json
{
  "id": "<template_id>",
  "requestBody": {
    "job_type": "run",
    "limit": "<canary_host>"
  }
}
```

Verify canary success via `jobs_job_host_summaries_list`. If `failures = 0`, proceed.

**Phase 2 - Expanded (25%)**:
```json
{
  "id": "<template_id>",
  "requestBody": {
    "job_type": "run",
    "limit": "<group>[0:25%]"
  }
}
```

Verify. If `failures = 0`, proceed.

**Phase 3 - Full Rollout**:
```json
{
  "id": "<template_id>",
  "requestBody": {
    "job_type": "run"
  }
}
```

**Health gate between phases**: Check `jobs_job_host_summaries_list` for `failures = 0` before proceeding to next phase. If ANY failures, STOP and report.

### Step 7: Post-Execution Summary

**MCP Tool**: `jobs_job_host_summaries_list` (from aap-mcp-job-management)
**Parameters**:
- `id`: `"<final_job_id>"`

Report only hosts with `changed > 0` or `failures > 0`:

```
## Execution Summary — Job #[job_id]

**Status**: [successful/failed]
**Elapsed**: [time]

### Changed Hosts
| Host | Changed | Failed |
|---|---|---|
| [host] | [changed] | [failures] |

### Result
[X] hosts changed, [Y] hosts failed, [Z] hosts unchanged.

### Proactive Recommendations [based on risk analyzer signals]
[If no notifications were flagged]: "Per Red Hat's Ch. 25, this template has no failure notifications. Now that the execution succeeded, consider adding notifications for future runs."
[If standalone template flagged]: "This template ran outside a workflow. For ongoing production use, consider wrapping it in a workflow with approval nodes."
```

### Step 8: Rollback (If Failure)

If the job fails, offer rollback options per execution-governance.md:

**Option 1 - Relaunch on failed hosts**:

**MCP Tool**: `jobs_relaunch_create` (from aap-mcp-job-management)
**Parameters**:
- `id`: `"<failed_job_id>"`
- `requestBody`:
  - `hosts`: `"failed"`
  - `credential_passwords`: `{}`

**Option 2 - Rollback playbook**: Launch a different template (if a rollback template exists).

**Option 3 - Revert to previous job**: Relaunch the last successful job.

## Dependencies

### Required MCP Servers
- `aap-mcp-job-management` - All job operations

### Required MCP Tools
- `job_templates_launch_create` (from job-management) - Launch jobs
- `jobs_retrieve` (from job-management) - Monitor progress
- `jobs_job_events_list` (from job-management) - Event details
- `jobs_job_host_summaries_list` (from job-management) - Host summaries
- `jobs_relaunch_create` (from job-management) - Rollback/relaunch

### Related Skills
- `execution-risk-analyzer` - MUST run before this skill
- `aap-mcp-validator` - Prerequisite validation
- `execution-summary` - Audit trail after launch

### Reference Documentation
- [execution-governance.md](docs/aap/execution-governance.md) - Check mode, rollback, phased rollout patterns

## Critical: Human-in-the-Loop Requirements

This skill requires explicit user confirmation at the following steps:

1. **Before Full Execution** (CRITICAL/HIGH risk)
   - Display check mode results
   - Ask: "Check mode passed. Proceed with full execution?"
   - Wait for explicit "yes" or "proceed"

2. **Between Rollout Phases** (CRITICAL risk)
   - Display phase results
   - Ask: "Phase [N] succeeded on [X] hosts. Proceed to Phase [N+1]?"
   - Wait for confirmation

3. **Before Rollback**
   - Display failure summary
   - Ask: "Job failed on [X] hosts. Choose rollback option: (1) Relaunch on failed hosts, (2) Run rollback playbook, (3) Manual investigation"
   - Wait for user choice

**Never execute without approval** for CRITICAL or HIGH risk targets.

## Example Usage

**User**: "Execute the security patch on production" (after risk analyzer identified CRITICAL risk with signals)

**Agent**:
1. Reads execution-governance.md
2. **Adapts**: Risk analyzer flagged last run failed → asks "Last run of this template failed. Investigate first or proceed?"
3. User says proceed → launches check mode: `job_type: "check"`, `diff_mode: true`
4. **Adapts**: Risk analyzer detected 2 shell tasks → reports: "Dry-run coverage: 4 of 6 tasks validated (67%). 2 shell/command tasks were SKIPPED."
5. Reports: "Check mode completed. 1 host would have 3 changes, 1 failure detected (dnf package not found). Per Ansible check mode docs, dnf contacts repos in check mode -- this failure is real."
6. Recommends: "STOP -- check mode detected a failure. Combined with the previous run failure, this template likely has a persistent issue."
7. **Proactive**: "Additionally, this template has no failure notifications (per Ch. 25) and runs standalone outside a workflow (per Ch. 9). Consider addressing these governance gaps."
