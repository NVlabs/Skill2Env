---
name: remediation
description: |
  **CRITICAL**: Use this skill for ALL CVE remediation workflows. DO NOT use individual skills piecemeal for end-to-end remediation.

  Use when users request:
  - CVE remediation playbooks or security patch deployment
  - Multi-step remediation (validation → context → playbook → execution)
  - Batch remediation across multiple systems or CVEs
  - End-to-end CVE management (analysis + remediation + verification)
  - Prioritizing and remediating CVEs (not just listing them)
  - Emergency security response with immediate remediation plans

  DO NOT use for simple queries:
  - "List critical CVEs" → Use `/cve-impact` skill
  - "What's the CVSS score for CVE-X?" → Use `/cve-impact` or `/cve-validation`
  - Standalone impact analysis without remediation → Use `/cve-impact`

  This skill orchestrates 6 specialized skills (cve-impact, cve-validation, system-context, playbook-generator, playbook-executor, remediation-verifier) for complete remediation workflows.
model: inherit
color: red
metadata:
  author: "Red Hat Ecosystem Engineering"
  priority: "high"
license: Apache-2.0
allowed-tools: vulnerability__get_cves vulnerability__get_cve vulnerability__get_cve_systems vulnerability__get_system_cves inventory__find_host_by_name inventory__get_host_details remediations__create_vuln_playbook job_templates_list job_templates_retrieve projects_list job_templates_launch_retrieve jobs_retrieve jobs_stdout_retrieve jobs_job_events_list jobs_job_host_summaries_list jobs_relaunch_retrieve inventories_list hosts_list
---

# Remediation Skill

End-to-end CVE remediation workflow. Orchestrates specialized skills for validation, context gathering, playbook generation, execution, and verification.

## Prerequisites

**Required MCP Servers**: `lightspeed-mcp` (CVE data, playbook generation), `aap-mcp-job-management`, `aap-mcp-inventory-management` (execution)

**Related Skills** (this skill invokes them):
- `/mcp-lightspeed-validator` - Verify Lightspeed MCP before CVE operations
- `/mcp-aap-validator` - Verify AAP MCP before playbook execution
- `/cve-impact` - CVE risk assessment
- `/cve-validation` - CVE validation and remediation availability
- `/system-context` - System inventory and deployment context
- `/playbook-generator` - Ansible playbook generation
- `/playbook-executor` - Playbook execution via AAP
- `/remediation-verifier` - Post-remediation verification

**Verification**: See Step 0 for MCP validation. Execute `/mcp-aap-validator` before Step 5 (playbook execution) if not already validated.

## When to Use This Skill

**Use this skill when**:
- User requests CVE remediation (playbook creation, patching, deployment)
- Full workflow needed: analysis → validation → playbook → execution → verification
- Batch remediation across multiple CVEs or systems

**Do NOT use when**:
- User only wants CVE listing or impact analysis → Use `/cve-impact`
- User only wants CVE validation → Use `/cve-validation`
- User only wants playbook generation (no execution) → Use `/playbook-generator` directly

## Workflow

Execute skills in this order. **MANDATORY**: Use actual Skill tool invocations, NOT text pretending to invoke skills. **Each step must complete before the next begins**—do not start Step N+1 until Step N has returned its result.

### Upfront: Planned Tasks (Before Step 0)

**When**: Before executing any step. **Do NOT start Step 0 until the user validates the plan.**

**Action**: Present the planned task list using **Part A** of [references/01-remediation-plan-template.md](references/01-remediation-plan-template.md). Show the 7 tasks (validate MCP → impact → validate CVE → context → playbook → execute → verify) and ask "Proceed with this plan?"

**Task list ordering** (CRITICAL): If using TodoWrite or task list UI, create tasks **in workflow order** (Step 0, 1, 2, 3, 4, 5, 6). Do NOT create in completion order or random order—display order must match execution order.

**Wait for explicit user response** ("yes" or "proceed") before invoking Step 0. If "abort" → stop.

### Step 0: Validate MCP Prerequisites

**Action**: Execute `/mcp-lightspeed-validator` (and `/mcp-aap-validator` before Step 5 if executing playbooks)

**When**: Before any CVE or remediation operations. Can skip if already validated this session.

**Sequencing (MANDATORY)**: Invoke validators **one at a time**. **Do NOT proceed to Step 1 until Step 0 is complete.** Wait for each validator to return explicit results (PASSED / FAILED / PARTIAL) before moving on. "Successfully loaded skill" alone does NOT mean validation completed—you must see the actual validation outcome.

**Invocation**: Use the Skill tool for ALL sub-skill invocations (validators, cve-validation, cve-impact, system-context, playbook-generator, playbook-executor, remediation-verifier). **Do NOT use "Task Output" with the skill name as task ID**—that causes "No task found" errors (e.g. "No task found with ID: cve-validation"). See [skill-invocation.md](docs/references/skill-invocation.md).

**Handle result**: If validation fails, stop and provide setup instructions. If passed, proceed to Step 1. **If any skill invocation fails** (e.g. "No task found with ID: ..."): Proceed with a warning—do not block. Later steps will surface real errors if MCP is unavailable.

### Step 1: Impact Analysis (If Requested or Needed)

**Action**: Execute the `/cve-impact` skill

**Invoke**:
```
"Analyze CVE-XXXX-YYYY and assess its impact on affected systems"
```

**Expected**: Risk assessment, affected systems list, CVSS interpretation. Integrate into remediation planning. If user only wanted impact analysis, provide assessment and offer remediation options.

### Step 2: Validate CVE (Remediatable Gate)

**Action**: Execute the `/cve-validation` skill

**Invoke**:
```
"Validate CVE-XXXX-YYYY format, existence, and remediation availability"
```

**Expected**: Validation status including `remediation_status.automated_remediation_available` or `validation_status`.

**Remediatable Gate** (MANDATORY): Trust cve-validation skill output. Do NOT re-interpret raw get_cve response—cve-validation uses advisory_available, remediation, advisories_list (not rules[]). See [cve-validation references/01-remediation-indicators.md](../cve-validation/references/01-remediation-indicators.md).
- **If remediatable** (`remediation_available: true` or `validation_status: "valid"`): Proceed to Step 3.
- **If NOT remediatable** (`remediation_available: false` or `validation_status: "not_remediable"`):
  1. Explain: "CVE-XXXX-YYYY has no automated remediation in Red Hat Lightspeed. Execution may have no effect."
  2. Suggest alternatives: manual patching, check Red Hat errata.
  3. Offer: "Continue anyway? (yes/no)"
  4. **If user says "yes"**: Proceed to Step 3 with warning: "⚠️ Proceeding despite no automated remediation—playbook generation or execution may have no effect."
  5. **If user says "no"**: Stop. Do not proceed to Steps 3–5.

**Batch**: For multiple CVEs, validate each. Proceed only with remediatable CVEs unless user explicitly confirms to include non-remediatable ones (with same warning).

### Step 3: Gather Context

**Action**: Execute the `/system-context` skill

**Invoke**:
```
"Gather system context for CVE-XXXX-YYYY: identify affected systems, RHEL versions, and deployment environments"
```

**Expected**: Context summary with remediation strategy. Use to inform playbook generation and execution planning.

### Step 4: Generate Playbook

**Action**: Execute the `/playbook-generator` skill

**CRITICAL**: You MUST invoke `/playbook-generator`, NOT generate playbook text yourself.

**Invoke**:
```
"Generate an Ansible remediation playbook for CVE-XXXX-YYYY targeting systems [list of system UUIDs]. Apply Red Hat best practices and RHEL-specific patterns from documentation."
```

**Expected**: Ansible playbook from Red Hat Lightspeed (returned AS IS by playbook-generator—no modifications). Present to user. **The playbook-generator ONLY GENERATES**—it does NOT execute. After presenting the playbook, present the Remediation Plan for user validation (see below).

### Remediation Plan (User Validation) — MANDATORY before Step 5

**When**: After Step 4 completes. **Do NOT proceed to Step 5 until the user validates the plan.**

**Action**: Present the plan using the Summary + Table + Checklist format. **Read [references/01-remediation-plan-template.md](references/01-remediation-plan-template.md)** for the exact template.

**Format**:
1. **Summary** — 1–2 sentences: what will happen and why
2. **Table** — CVE | Target Systems | Key Action
3. **Checklist** — Ordered steps (mark completed as "— done")
4. **Confirm prompt** — "yes"/"proceed", "dry-run only", or "abort"

**Wait for explicit user response.** If "yes" or "proceed" → invoke playbook-executor. If "abort" → stop. If "dry-run only" → invoke playbook-executor with instruction to run dry-run only and stop.

### Step 5: Execute Playbook (With User Confirmation)

**Prerequisite**: Remediation Plan must be presented and user must have responded "yes" or "proceed" (or "dry-run only"). Do NOT invoke playbook-executor until plan validation is complete.

**CRITICAL**: Before execution, you MUST:
1. Have presented the Remediation Plan (summary + table + checklist)
2. Have received user confirmation ("yes", "proceed", or "dry-run only")
3. Show playbook preview and key tasks when invoking playbook-executor
4. Recommend dry-run first; wait for explicit approval before actual execution

**Action**: Execute the `/playbook-executor` skill

**Invoke** (pass playbook metadata from playbook-generator and system-context):
```
"Execute the generated playbook for CVE-XXXX-YYYY. Playbook file: [filename from playbook-generator]. Content: [in context from playbook-generator output]. Target systems: [list of system UUIDs from system-context]. Start with dry-run (check mode) if user requested it. Monitor job status until completion and report results."
```

**Git Flow path**: When playbook-executor performs Git Flow (write playbook to repo), it MUST use the absolute path for the Write tool: `<user_provided_repo_path>/playbooks/remediation/<filename>`. Never use a relative path like `test-aap-project/playbooks/...`—that causes "Error writing file" when the repo is outside the workspace.

**Expected**: playbook-executor validates AAP, matches templates, offers dry-run, executes on approval, streams progress, generates report. **Validates job log for CVE handling**—confirms from stdout that the playbook addressed the target CVE(s); reports ✓ confirmation or ⚠️ warning if no evidence found. After success, suggest verification with `/remediation-verifier`.

### Step 6: Verify Deployment (Optional)

**Action**: Execute the `/remediation-verifier` skill (if user requests verification)

**Invoke**:
```
"Verify remediation success for CVE-XXXX-YYYY on systems [list of system UUIDs]. Check CVE status, package versions, and service health."
```

**Expected**: Verification report with pass/fail. Present results to user.

## Dependencies

### Required MCP Tools
- None (orchestration skill—delegates to other skills that use MCP tools)

### Required MCP Servers
- `lightspeed-mcp` - CVE data, playbook generation
- `aap-mcp-job-management` - Job launch and monitoring
- `aap-mcp-inventory-management` - Inventory for execution

### Related Skills
- `cve-impact` - Step 1
- `cve-validation` - Step 2
- `system-context` - Step 3
- `playbook-generator` - Step 4
- `playbook-executor` - Step 5
- `remediation-verifier` - Step 6

### Reference Documentation
- [references/01-remediation-plan-template.md](references/01-remediation-plan-template.md) - Plan format for user validation
- [lightspeed-mcp-tool-failures.md](docs/references/lightspeed-mcp-tool-failures.md) - Backend errors (e.g. explain_cves), user-friendly message, workarounds
- [cve-remediation-templates.md](docs/ansible/cve-remediation-templates.md)
- [package-management.md](docs/rhel/package-management.md)

## Critical: Human-in-the-Loop Requirements

This skill requires explicit user confirmation at:

1. **Upfront Planned Tasks** (before Step 0)
   - Present the 7-task plan. Wait for "yes" or "proceed" before starting any step.
   - Do NOT invoke validators or other skills until the user confirms.

2. **Remediation Plan Validation** (before Step 5)
   - Present the plan: Summary + Table + Checklist
   - Wait for user response: "yes"/"proceed", "dry-run only", or "abort"
   - Do NOT invoke playbook-executor until the user validates the plan

3. **Before Playbook Execution (Step 5)**
   - Display playbook preview and key tasks
   - Recommend dry-run first; wait for explicit approval before actual execution

4. **Before Destructive Actions**
   - Offer dry-run (check mode) before actual execution
   - If dry-run approved, run first and show results
   - Only proceed to actual execution after user confirms

**Never assume approval**—always wait for explicit user confirmation before execution.

## MCP Tool Usage

**vulnerability__explain_cves**: Requires a valid `system_uuid` from inventory. Do NOT call it unless you have the resolved UUID from Step 3 (system-context) or Step 1 (cve-impact). Never pass `system_uuid: "undefined"` or placeholder values—this causes validation errors. For remediation availability at Step 2, use `get_cve` via cve-validation only.

**Lightspeed tool failures**: If a tool fails with a cryptic backend error (e.g. `'dnf_modules'`), do NOT retry or expose the raw error. Use workarounds from [lightspeed-mcp-tool-failures.md](docs/references/lightspeed-mcp-tool-failures.md).

## Error Handling

- **Invalid CVE**: "CVE-XXXX-YYYY is not valid or doesn't exist. Please verify the CVE ID."
- **No Remediation Available**: "CVE-XXXX-YYYY doesn't have an automated remediation playbook. Manual patching required."
- **System Not Found**: "System XXXX is not in the Lightspeed inventory. Please ensure it's registered."
- **Batch Partial Failure**: "Successfully processed X of Y CVEs. Failed: [list]. Reason: [explanations]"
- **Lightspeed tool failures** (e.g. explain_cves `'dnf_modules'`): Do NOT show raw error. Use user-friendly message and workaround from [lightspeed-mcp-tool-failures.md](docs/references/lightspeed-mcp-tool-failures.md).

## Output Format

**Single CVE**:
```
CVE-XXXX-YYYY Remediation Summary
CVSS Score: X.X (Severity)
Affected Packages: package-name-version
Ansible Playbook Generated: ✓
Target Systems: N systems
[Playbook YAML or AAP link]
[Execution instructions]
```

**Batch**:
```
Batch Remediation Summary
CVEs: CVE-A, CVE-B, CVE-C
Target Systems: N systems
Total Fixes: X package updates
[Consolidated playbook]
[Execution instructions]
```

## Important Reminders

- **Use actual tool calls**—invoke skills via Skill tool, not text. If tool use count is 0, you are doing it wrong.
- **Orchestrate skills, don't call MCP tools directly**—skills handle docs and tools.
- **Always ask for execution confirmation** before Step 5.
- **Safety**: Test in non-prod first, back up systems, schedule maintenance windows, verify after execution.
