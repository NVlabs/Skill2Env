---
name: governance-assessor
description: |
  Orchestrates AAP governance readiness assessments -- full platform audit or scoped to specific domains.

  Assesses 7 governance domains + 1 bonus:
  1. Workflow Governance (approval gates, workflow coverage)
  2. Notification Coverage (failure alerting, notification bindings)
  3. Access Control / RBAC (teams, roles, least privilege)
  4. Credential Security (separation of duties, credential hygiene)
  5. Execution Environments (custom EEs, image provenance)
  6. Workload Isolation (instance groups, capacity separation)
  7. Audit Trail (activity stream, change tracking)
  Bonus: External Authentication (LDAP, SAML, SSO)

  Use when:
  - Full: "Is my AAP ready for production?", "Audit my platform governance"
  - Scoped: "Assess my credentials setup", "Check my RBAC", "How are my notifications?"
  - "What should I fix before executing jobs?"
  - Any question about specific AAP governance domains above

  NOT for job execution (use governance-executor) or troubleshooting (use forensic-troubleshooter).
model: inherit
color: red
license: Apache-2.0
allowed-tools: job_templates_list workflow_job_templates_list inventories_list hosts_list notification_templates_list execution_environments_list notification_templates_create execution_environments_create credentials_list credential_types_list credentials_create instance_groups_list activity_stream_list instance_groups_create users_list teams_list role_user_assignments_list role_team_assignments_list authenticators_list teams_create role_user_assignments_create authenticators_create
---

# Governance Assessor

## Prerequisites

**Required MCP Servers**: All 6 AAP MCP servers for full assessment; subset for scoped assessment (validated in Step 1)
**Required Skills**: `aap-mcp-validator`, `governance-readiness-assessor`, `execution-summary`

## When to Use This Skill

Use this skill when:
- User asks to assess or audit their AAP platform's governance readiness (full assessment)
- User asks about a specific governance area: credentials, RBAC, workflows, notifications, execution environments, instance groups, audit trail, or authentication (scoped assessment)
- User asks if their AAP is ready for production execution
- User asks what needs to be improved in their AAP setup
- Before a first production execution (optional pre-flight check)

Do NOT use when:
- User wants to execute a job (use `governance-executor` skill)
- User wants to troubleshoot a failed job (use `forensic-troubleshooter` skill)
- User only wants MCP connectivity check (use `aap-mcp-validator` skill directly)

## Workflow

### 1. Validate MCP Connectivity

**Invoke the aap-mcp-validator skill**:
- **Full assessment**: Validate all 6 AAP MCP servers
- **Scoped assessment**: Validate only the MCP servers needed for the requested domains
- If any required server fails: report and stop

### 2. Run Governance Readiness Assessment

**Invoke the governance-readiness-assessor skill** (the skill determines scope from the user's request):
- **Full assessment**: Queries all 6 MCP servers across 7 domains + 1 bonus domain
- **Scoped assessment**: Queries only the servers for requested domains, plus minimal queries for cross-domain correlation
- The skill reads governance-readiness.md
- **Adapts depth**: When initial assessment reveals PASS, performs follow-up queries to verify (e.g., notification templates exist but are they bound to anything? Credentials exist but are they shared across environments?)
- **Correlates across domains**: Identifies compound risks (e.g., no teams + credentials = user-scoped credentials; no workflows + no notifications = invisible failures)
- **Calibrates severity**: Checks inventory scale to frame findings appropriately (lab vs enterprise)
- Produces the structured Governance Readiness Report with Red Hat citations per domain, compound risk analysis, and prioritized fix order

**Document Consultation** (performed by the skill):
The governance-readiness-assessor skill reads [governance-readiness.md](docs/aap/governance-readiness.md) and reports its consultation.

### 3. Present Report and Offer Remediation

Present the full report to the user including:
- Per-domain findings (with any depth-query adjustments)
- Compound Risk Analysis section (cross-domain correlations)
- Recommended Fix Order (prioritized by dependency chain)

For any GAP or WARN findings, offer to remediate using MCP write tools where available, starting with the highest-priority gap per the dependency chain.

**Human Confirmation** (REQUIRED):
Before creating or modifying any AAP resource:
- Display the planned change
- Ask: "Should I create/modify this resource to address the gap?"
- Wait for explicit user confirmation

### 4. Generate Execution Summary

**Invoke the execution-summary skill**:
- Generate audit trail showing documents consulted, MCP tools used, governance findings

## Dependencies

### Required Skills
- `aap-mcp-validator` - MCP server validation
- `governance-readiness-assessor` - 7-domain assessment
- `execution-summary` - Audit trail

### Required MCP Servers
- All 6 AAP MCP servers

### Required MCP Tools
- None; delegated to sub-skill (`governance-readiness-assessor`).

### Related Skills
- `governance-executor` - Follow-up: governed execution after assessment passes
- `forensic-troubleshooter` - Follow-up: investigate failures found during assessment

### Reference Documentation
- [governance-readiness.md](docs/aap/governance-readiness.md) - 7-domain assessment framework

### Sample Reports
- [sample-full-assessment.md](references/sample-full-assessment.md) - Full 7+1 domain assessment with compound risk analysis
- [sample-scoped-assessment.md](references/sample-scoped-assessment.md) - Scoped assessment (Credentials + RBAC) with cross-domain correlation

## Example Usage

### Example 1: Full Platform Assessment

**User**: "Is my AAP ready for production?"

**Agent**:

1. Validates all 6 MCP servers via aap-mcp-validator
2. Invokes governance-readiness-assessor (full scope: all 7+1 domains)
   - Domain 1 (Workflows): GAP -- no workflow job templates found
   - Domain 2 (Notifications): WARN -- templates exist but not bound to jobs
   - Domain 3 (RBAC): GAP -- no teams, only user-level assignments
   - Domain 4 (Credentials): PASS
   - Domain 5 (EEs): PASS
   - Domain 6 (Workload Isolation): PASS -- single instance group but lab scale
   - Domain 7 (Audit Trail): PASS
   - Bonus (Auth): WARN -- local-only authentication
   - Compound: No workflows + no notifications = highest-risk combination
3. Presents full report with Red Hat citations per domain
4. Offers remediation: "Create a team for automation operators? (Fixes Domain 3)"
5. Invokes execution-summary with audit trail

### Example 2: Scoped Assessment

**User**: "Check my RBAC and credentials setup"

**Agent**:

1. Validates `aap-mcp-user-management` and `aap-mcp-security-compliance`
2. Invokes governance-readiness-assessor scoped to Domains 3 + 4
3. Presents scoped report: RBAC findings + Credential findings + cross-correlation
4. Offers: "Would you like me to run the full 7-domain assessment?"
5. Invokes execution-summary

## Critical: Human-in-the-Loop Requirements

1. **Before any remediation actions**: Display planned change, wait for approval
2. **Never auto-create resources**: Always present the assessment first, let user decide what to fix
3. **Offer skip/abort options**: User may want to see the report without acting on it
