---
name: governance-executor
description: |
  Orchestrates governed job execution with risk analysis, check mode, approval, and rollback.

  Use when:
  - "Execute job template X", "Deploy to production", "Push to prod", "Launch job template"
  - Any execution request targeting sensitive environments
  - Job template launches requiring governance controls

  NOT for platform assessment (use governance-assessor) or troubleshooting (use forensic-troubleshooter).
model: inherit
color: red
license: Apache-2.0
allowed-tools: job_templates_list job_templates_retrieve job_templates_launch_retrieve job_templates_launch_create jobs_list jobs_retrieve jobs_job_events_list jobs_job_host_summaries_list jobs_relaunch_create workflow_job_templates_list inventories_list hosts_list notification_templates_list credentials_list instance_groups_list users_list
---

# Governance Executor

## Prerequisites

**Required MCP Servers**: `aap-mcp-job-management`, `aap-mcp-inventory-management`
**Required Skills**: `aap-mcp-validator`, `execution-risk-analyzer`, `governed-job-launcher`, `execution-summary`

## When to Use This Skill

Use this skill when:
- User asks to execute, launch, deploy, or push a job template
- User mentions production, staging, or any environment-targeted execution
- User asks to launch a specific job template by name or ID

Do NOT use when:
- User asks to assess platform readiness (use `governance-assessor` skill)
- User asks to troubleshoot a failed job (use `forensic-troubleshooter` skill)
- User asks about governance or compliance without an execution context

## Workflow

### 1. Validate MCP Connectivity

**Invoke the aap-mcp-validator skill**:
- Validate `aap-mcp-job-management` and `aap-mcp-inventory-management`
- If any server fails: report and stop

### 2. Analyze Execution Risk

**Invoke the execution-risk-analyzer skill**:
- The skill reads execution-governance.md
- Identifies the job template and classifies inventory risk (CRITICAL / HIGH / MEDIUM / LOW)
- **Adapts**: Checks job history -- flags recent failures or first-time execution
- **Adapts**: Checks template launch config -- verifies check mode and limit overrides are available
- **Adapts**: Checks notification bindings -- flags templates without failure alerting
- **Adapts**: Checks workflow coverage -- flags standalone production templates
- **Adapts**: Analyzes previous run events -- identifies shell/command module usage for check mode coverage
- Scans extra_vars for plain-text secrets
- **Adjusts risk level** based on operational signals (e.g., HIGH + never run + no check mode override → CRITICAL)
- Reports risk assessment with Red Hat citations AND operational context

**Document Consultation** (performed by the skill):
The execution-risk-analyzer skill reads [execution-governance.md](docs/aap/execution-governance.md) and reports its consultation.

**If secrets detected**: STOP. Report the finding and recommend using AAP credentials.

### 3. Execute Governed Launch

**Invoke the governed-job-launcher skill**:
- The skill reads execution-governance.md
- **Adapts to risk analyzer signals**:
  - If recent failures flagged → offers to investigate first via forensic-troubleshooter
  - If check mode not overridable → informs user and adapts execution path
  - If shell/command modules detected → provides specific dry-run coverage percentage instead of generic warning
- Applies governance controls based on adjusted risk level:
  - **CRITICAL**: Check mode → interpret with context → approve → phased rollout
  - **HIGH**: Check mode → interpret → approve → full run
  - **MEDIUM**: Confirm → full run
  - **LOW**: Execute directly
- Reports results with changed-only summary
- **Proactive post-execution**: If notifications/workflows were flagged as missing, recommends addressing those governance gaps now

**Human Confirmation** (REQUIRED for CRITICAL/HIGH):
- After check mode: "Check mode results: [summary with coverage %]. Proceed with full execution?"
- Between phases (CRITICAL): "Phase [N] succeeded. Proceed to Phase [N+1]?"
- Wait for explicit user confirmation

**If failure**: Offer rollback options via `jobs_relaunch_create`.

### 4. Generate Execution Summary

**Invoke the execution-summary skill**:
- Generate audit trail showing: risk classification basis, check mode results, approval decisions, execution outcome

## Dependencies

### Required Skills
- `aap-mcp-validator` - MCP server validation
- `execution-risk-analyzer` - Risk classification and secret scanning
- `governed-job-launcher` - Check mode, execution, rollback
- `execution-summary` - Audit trail

### Required MCP Servers
- `aap-mcp-job-management` - Job template lookup and launch
- `aap-mcp-inventory-management` - Inventory risk classification

### Required MCP Tools
- None; delegated to sub-skills (`execution-risk-analyzer`, `governed-job-launcher`).

### Related Skills
- `forensic-troubleshooter` - Follow-up if execution fails
- `governance-assessor` - Pre-execution platform readiness check

### Reference Documentation
- [execution-governance.md](docs/aap/execution-governance.md) - Risk classification, check mode, rollback

## Example Usage

### Example 1: Production Execution with Full Governance

**User**: "Execute the security patch on production"

**Agent**:

1. Validates MCP connectivity via aap-mcp-validator
2. Invokes execution-risk-analyzer:
   - Finds "Security Patch" template, identifies "Production" inventory → CRITICAL risk
   - Check mode is overridable, but last run failed → adds WARN signal
   - No failure notifications → flags governance gap
3. Reports risk analysis to user with Red Hat citations
4. Invokes governed-job-launcher:
   - Runs check mode first → presents results: "Check mode: 12 changes, 2 shell tasks skipped"
   - Asks: "Proceed with full execution?"
   - User approves → executes phased rollout (Phase 1: 25% of hosts)
   - Phase 1 succeeds → "Proceed to Phase 2?"
5. Invokes execution-summary with full audit trail

### Example 2: Low-Risk Development Execution

**User**: "Launch the dev-setup template"

**Agent**:

1. Validates MCP connectivity
2. Invokes execution-risk-analyzer: "Development" inventory → LOW risk, clear job history
3. Reports: "Low risk execution, direct execution permitted."
4. Invokes governed-job-launcher: executes directly, reports results
5. Invokes execution-summary

## Critical: Human-in-the-Loop Requirements

1. **Before full execution** (CRITICAL/HIGH risk): Present check mode results, wait for approval
2. **Between rollout phases** (CRITICAL risk): Present phase results, wait for approval
3. **Before rollback**: Present failure summary, let user choose rollback strategy
4. **Never skip check mode** for CRITICAL risk, even if user says "urgent"
