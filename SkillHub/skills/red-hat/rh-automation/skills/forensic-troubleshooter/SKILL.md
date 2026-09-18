---
name: forensic-troubleshooter
description: |
  Orchestrates forensic analysis of failed jobs with event extraction, host correlation, and resolution advisory.

  Use when:
  - "Job #X failed", "Why did the execution fail?"
  - "Analyze the failure", "What went wrong?"
  - "Root cause analysis of job #X"

  NOT for execution (use governance-executor) or platform assessment (use governance-assessor).
model: inherit
color: yellow
license: Apache-2.0
allowed-tools: job_templates_list jobs_retrieve jobs_job_events_list jobs_job_host_summaries_list jobs_stdout_retrieve inventories_list hosts_list hosts_variable_data_retrieve notification_templates_list credentials_list instance_groups_list users_list
---

# Forensic Troubleshooter

## Prerequisites

**Required MCP Servers**: `aap-mcp-job-management`, `aap-mcp-inventory-management`
**Required Skills**: `aap-mcp-validator`, `job-failure-analyzer`, `host-fact-inspector`, `resolution-advisor`, `execution-summary`

## When to Use This Skill

Use this skill when:
- User reports a failed job and wants to understand why
- User asks for root cause analysis of a job failure
- User asks to analyze job errors or failure events
- After a governed execution fails (follow-up from governance-executor)

Do NOT use when:
- User wants to execute a job (use `governance-executor` skill)
- User wants to assess platform readiness (use `governance-assessor` skill)
- User wants to check host facts without a failure context (use `host-fact-inspector` skill directly)

## Workflow

### 1. Validate MCP Connectivity

**Invoke the aap-mcp-validator skill**:
- Validate `aap-mcp-job-management` and `aap-mcp-inventory-management`
- If any server fails: report and stop

### 2. Analyze Job Failure

**Invoke the job-failure-analyzer skill**:
- The skill reads job-troubleshooting.md
- Retrieves job status, extracts failure events, analyzes host summaries
- Classifies the failure (Platform / Code / Configuration)
- Reconstructs failure timeline
- Reports structured analysis with Red Hat citations

**Document Consultation** (performed by the skill):
The job-failure-analyzer skill reads [job-troubleshooting.md](docs/aap/job-troubleshooting.md) and reports its consultation.

### 3. Correlate with Host Facts

**Invoke the host-fact-inspector skill**:
- The skill reads job-troubleshooting.md
- Looks up affected hosts from the failure analysis
- Retrieves host variables/facts
- Correlates errors with host system state
- Reports correlation findings

**Document Consultation** (performed by the skill):
The host-fact-inspector skill reads [job-troubleshooting.md](docs/aap/job-troubleshooting.md) for correlation patterns.

### 4. Provide Resolution Advisory

**Invoke the resolution-advisor skill**:
- The skill reads error-classification.md and job-troubleshooting.md
- Determines the resolution path based on error classification and host correlation
- Provides Red Hat documentation-backed resolution steps
- Identifies related governance gaps

**Document Consultation** (performed by the skill):
The resolution-advisor skill reads [error-classification.md](docs/references/error-classification.md) and [job-troubleshooting.md](docs/aap/job-troubleshooting.md).

### 5. Generate Execution Summary

**Invoke the execution-summary skill**:
- Generate audit trail showing: documents consulted, failure classification basis, host correlations, resolution recommendations

## Dependencies

### Required Skills
- `aap-mcp-validator` - MCP server validation
- `job-failure-analyzer` - Event extraction and classification
- `host-fact-inspector` - Host fact correlation
- `resolution-advisor` - Resolution recommendations
- `execution-summary` - Audit trail

### Required MCP Servers
- `aap-mcp-job-management` - Job events and host summaries
- `aap-mcp-inventory-management` - Host facts for correlation

### Required MCP Tools
- None; delegated to sub-skills (`job-failure-analyzer`, `host-fact-inspector`).

### Related Skills
- `governance-executor` - If failure occurred during a governed execution
- `governance-assessor` - If root cause points to platform governance gaps

### Reference Documentation
- [job-troubleshooting.md](docs/aap/job-troubleshooting.md) - Event parsing, failure patterns, correlation
- [error-classification.md](docs/references/error-classification.md) - Error taxonomy and resolution paths

## Example Usage

### Example 1: Single Job Failure

**User**: "Job #4451 failed. What happened?"

**Agent**:

1. Validates MCP connectivity via aap-mcp-validator
2. Invokes job-failure-analyzer:
   - Retrieves job #4451 status: "failed"
   - Extracts failure events: `runner_on_failed` on 2 hosts
   - Classifies: Configuration error (missing variable `db_password`)
   - Reconstructs timeline with Red Hat citations
3. Invokes host-fact-inspector:
   - Looks up affected hosts: `web-prod-01`, `web-prod-02`
   - Retrieves host facts: both running RHEL 9.2, same Ansible connection settings
   - Correlates: variable `db_password` not defined in host vars or group vars
4. Invokes resolution-advisor:
   - Classification: Configuration error → variable resolution
   - Recommendation: "Define `db_password` via AAP credentials (Ch. 15, Sec. 15.1.4) rather than host vars"
5. Invokes execution-summary with full forensic audit trail

### Example 2: Post-Execution Failure Follow-Up

**User**: "The execution just failed, can you investigate?"

**Agent**:

1. Identifies the most recent failed job from `jobs_list`
2. Follows the same forensic workflow: analyze → correlate → advise
3. If related to a governed execution, links back to the execution risk analysis
