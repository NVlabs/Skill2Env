---
name: execution-summary
description: |
  Generate concise execution audit reports tracking documents consulted, MCP tools used, decisions made, and outcomes.

  Use when:
  - "Generate execution summary"
  - "Create execution report"
  - "Show workflow audit trail"
  - After completing any governance workflow (assessment, execution, troubleshooting)

  NOT for: starting a new workflow (use the appropriate skill instead).
model: inherit
color: green
license: Apache-2.0
allowed-tools:
---

# Execution Summary

## Prerequisites

**Required MCP Servers**: None (this skill summarizes the actions already taken)

## When to Use This Skill

Use this skill when:
- After completing a governance assessment workflow
- After completing a governed execution
- After completing forensic troubleshooting
- User asks for an execution summary or audit trail
- As the final step in any agent workflow

Do NOT use when:
- Starting a new workflow (use the appropriate agent or skill)
- During a workflow (generate summary only at the end)

## Workflow

### Step 1: Collect Execution Data

Review the current conversation/session to extract:

1. **Documents Consulted**: Which `.md` files were read using the Read tool, and what topic they informed
2. **MCP Tools Invoked**: Which MCP tools were called, with which parameters, and what they returned (summary, not raw data)
3. **Decisions Made**: What governance decisions were made based on document knowledge (risk classification, PASS/GAP/WARN, classification type)
4. **Human Interactions**: What approvals were requested and what the user decided
5. **Outcomes**: Final results of the workflow

### Step 2: Generate Structured Report

**Output format**:

```
## Execution Summary

**Workflow**: [Assessment / Execution / Troubleshooting]
**Initiated**: [timestamp]
**Duration**: [time span]
**Status**: [Completed / Partially Completed / Aborted]

---

### Documents Consulted

| Document | Topic | Citation |
|---|---|---|
| [governance-readiness.md](docs/aap/governance-readiness.md) | 7-domain assessment framework | Red Hat AAP 2.5 Security Best Practices (Ch. 15), Workflows (Ch. 9), Notifications (Ch. 25) |
| [execution-governance.md](docs/aap/execution-governance.md) | Risk classification, check mode | Red Hat AAP 2.5 Job Templates (Ch. 9), Controller Best Practices |
| [job-troubleshooting.md](docs/aap/job-troubleshooting.md) | Event parsing, failure patterns | Red Hat AAP 2.6 Troubleshooting Guide |
| [error-classification.md](docs/references/error-classification.md) | Error taxonomy | Red Hat AAP 2.6 Troubleshooting Guide |

### MCP Tools Used

| Server | Tool | Purpose | Result |
|---|---|---|---|
| [server] | [tool_name] | [what it was used for] | [summary of result] |

### Governance Decisions

| Decision | Basis | Outcome |
|---|---|---|
| [e.g., "Classified Production as CRITICAL risk"] | [e.g., "Per execution-governance.md: inventory name contains 'prod'"] | [e.g., "Check mode required before execution"] |

### Human Interactions

| Prompt | User Decision | Timestamp |
|---|---|---|
| [e.g., "Proceed with full execution?"] | [e.g., "Approved"] | [time] |

### Outcome

[Final result of the workflow]

---

**Audit Note**: All governance decisions in this workflow are traceable to official Red Hat documentation as cited in the Documents Consulted section.
```

## Dependencies

### Required MCP Servers
- None

### Required MCP Tools
- None (this skill summarizes actions already taken)

### Related Skills
- All other skills (this skill summarizes their execution)

### Reference Documentation
- All docs consulted during the workflow being summarized

## Example Usage

**User**: "Generate an execution summary for the job we just ran"

**Agent** produces a structured summary showing: execution-governance.md was consulted (citing Red Hat Ch. 9 and Ch. 15), `job_templates_launch_create` was called twice (check mode + full run), risk was classified as CRITICAL (based on inventory name "Production"), user approved after check mode passed, and the execution succeeded on 1 host with 3 changes.
