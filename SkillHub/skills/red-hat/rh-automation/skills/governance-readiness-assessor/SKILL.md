---
name: governance-readiness-assessor
description: |
  Assess AAP platform governance readiness -- full 7-domain audit or scoped to specific domains.

  Use when:
  - Full assessment: "Is my AAP ready for production?", "Audit my platform governance"
  - Scoped assessment: "Assess my credentials setup", "Check my RBAC", "How are my notifications configured?"
  - "What should I fix before executing jobs?"
  - "Assess my AAP configuration"
  - Any question about a specific governance domain (credentials, RBAC, workflows, notifications, EEs, instance groups, audit, auth)

  NOT for: executing jobs (use governance-executor) or troubleshooting failures (use forensic-troubleshooter).
model: inherit
color: red
license: Apache-2.0
allowed-tools: workflow_job_templates_list job_templates_list notification_templates_list execution_environments_list notification_templates_create execution_environments_create users_list teams_list role_user_assignments_list role_team_assignments_list authenticators_list teams_create role_user_assignments_create authenticators_create credentials_list credential_types_list credentials_create instance_groups_list activity_stream_list instance_groups_create inventories_list hosts_list
---

# Governance Readiness Assessor

## Prerequisites

**Required MCP Servers**: All 6 AAP MCP servers
- `aap-mcp-job-management`
- `aap-mcp-inventory-management`
- `aap-mcp-configuration`
- `aap-mcp-security-compliance`
- `aap-mcp-system-monitoring`
- `aap-mcp-user-management`

**Verification**: Run the `aap-mcp-validator` skill with all 6 servers before proceeding.

## When to Use This Skill

Use this skill when:
- **Full assessment**: User asks to assess or audit AAP governance readiness, or asks if AAP is ready for production
- **Scoped assessment**: User asks about a specific governance area:
  - "Assess my credentials setup" → Domain 4 (Credential Security)
  - "Check my RBAC" / "How are my users and teams configured?" → Domain 3 (Access Control)
  - "Are my notifications configured properly?" → Domain 2 (Notification Coverage)
  - "Do I have workflows set up?" → Domain 1 (Workflow Governance)
  - "Check my execution environments" → Domain 5 (Execution Environments)
  - "Assess workload isolation" → Domain 6 (Workload Isolation)
  - "Is my audit trail working?" → Domain 7 (Audit Trail)
  - "Check my authentication setup" → Bonus (External Authentication)
  - Combinations: "Assess my credentials and RBAC" → Domains 3 + 4
- Before a first production execution (as part of governance-assessor workflow)
- User asks what needs to be fixed in their AAP configuration

Do NOT use when:
- User wants to execute a specific job (use `execution-risk-analyzer` + `governed-job-launcher` skills)
- User wants to troubleshoot a failed job (use `job-failure-analyzer` skill)
- User only wants MCP connectivity validation (use `aap-mcp-validator` skill)

## Workflow

### Step 1: Consult Governance Readiness Documentation

**CRITICAL**: Document consultation MUST happen BEFORE any MCP tool invocations.

**Document Consultation** (REQUIRED - Execute FIRST):
1. **Action**: Read [governance-readiness.md](docs/aap/governance-readiness.md) using the Read tool to understand the 7-domain assessment framework, Red Hat source citations, decision tables, and output template
2. **Output to user**: "I consulted [governance-readiness.md](docs/aap/governance-readiness.md) to understand Red Hat's governance best practices for the 7-domain assessment framework."

### Step 1.5: Determine Assessment Scope

Analyze the user's request to determine whether this is a **full assessment** (all 7+1 domains) or a **scoped assessment** (specific domains).

**Scope Detection**:

| User Request Pattern | Domains to Assess |
|---|---|
| "assess readiness", "audit governance", "ready for production", "full assessment" | All 7 + bonus |
| "credentials", "credential setup", "secrets", "credential hygiene" | Domain 4 (Credential Security) |
| "RBAC", "users", "teams", "access control", "permissions", "roles" | Domain 3 (Access Control) |
| "notifications", "alerting", "failure notifications" | Domain 2 (Notification Coverage) |
| "workflows", "approval gates", "workflow governance" | Domain 1 (Workflow Governance) |
| "execution environments", "EEs", "container images" | Domain 5 (Execution Environments) |
| "instance groups", "workload isolation", "capacity" | Domain 6 (Workload Isolation) |
| "audit", "activity stream", "audit trail" | Domain 7 (Audit Trail) |
| "authentication", "LDAP", "SAML", "SSO", "external auth" | Bonus (External Authentication) |
| Combinations (e.g., "credentials and RBAC") | Multiple specific domains |

**Rules**:
- If scope is ambiguous, default to **full assessment**
- For scoped assessments, still validate only the MCP servers needed for the requested domains
- For scoped assessments, still perform cross-domain correlation IF the assessed domains participate in any correlation pattern (e.g., assessing credentials alone still triggers the RBAC+Credentials correlation check by querying enough RBAC data to determine if teams exist)
- Always tell the user what scope was detected: "You asked about credentials -- I'll assess Domain 4 (Credential Security) and check for related cross-domain impacts."

### Step 2: Query MCP Servers (Scoped or Full)

**For full assessment**: Execute all queries below in parallel where possible.
**For scoped assessment**: Execute only the queries for the requested domains. However, if the requested domains participate in a cross-domain correlation pattern (see Step 5), also execute the minimal queries needed for that correlation (e.g., assessing credentials alone should also query `teams_list` to check if the RBAC+Credentials correlation applies).

**Domain 1 - Workflow Governance**:

**MCP Tool**: `workflow_job_templates_list` (from aap-mcp-job-management)
**Parameters**:
- `page_size`: `100`

**MCP Tool**: `job_templates_list` (from aap-mcp-job-management)
**Parameters**:
- `page_size`: `100`

**Domain 2 - Notification Coverage**:

**MCP Tool**: `notification_templates_list` (from aap-mcp-configuration)
**Parameters**:
- `page_size`: `100`

**Domain 3 - Access Control (RBAC)**:

**MCP Tool**: `users_list` (from aap-mcp-user-management)
**Parameters**:
- `page_size`: `100`

**MCP Tool**: `teams_list` (from aap-mcp-user-management)
**Parameters**:
- `page_size`: `100`

**MCP Tool**: `role_user_assignments_list` (from aap-mcp-user-management)
**Parameters**:
- `page_size`: `100`

**MCP Tool**: `role_team_assignments_list` (from aap-mcp-user-management)
**Parameters**:
- `page_size`: `100`

**Domain 4 - Credential Security**:

**MCP Tool**: `credentials_list` (from aap-mcp-security-compliance)
**Parameters**:
- `page_size`: `100`

**MCP Tool**: `credential_types_list` (from aap-mcp-security-compliance)
**Parameters**:
- `page_size`: `100`

**Domain 5 - Execution Environments**:

**MCP Tool**: `execution_environments_list` (from aap-mcp-configuration)
**Parameters**:
- `page_size`: `100`

**Domain 6 - Workload Isolation**:

**MCP Tool**: `instance_groups_list` (from aap-mcp-system-monitoring)
**Parameters**:
- `page_size`: `100`

**Domain 7 - Audit Trail**:

**MCP Tool**: `activity_stream_list` (from aap-mcp-system-monitoring)
**Parameters**:
- `page_size`: `10`

**Bonus - External Authentication**:

**MCP Tool**: `authenticators_list` (from aap-mcp-user-management)
**Parameters**:
- `page_size`: `100`

### Step 3: Assess Each Domain (with Mandatory Red Hat Citations)

For EACH assessed domain (all 7+1 for full assessment, or the scoped domains), follow the assessment pattern from governance-readiness.md.

**MANDATORY CITATION RULE**: Every single domain finding MUST include:
1. The **Red Hat source document name** (e.g., "Configuring Automation Execution")
2. The **specific chapter and section** (e.g., "Ch. 15, Sec. 15.1.4")
3. A **direct quote** from the Red Hat documentation
4. The **recommendation** must reference the Red Hat source again

A finding without a Red Hat citation is incomplete. Every assessment criterion and recommendation must trace to official Red Hat documentation.

**Output format per domain** (MANDATORY -- do not deviate):

```
### Domain [N]: [Name] — [PASS/GAP/WARN]

Per Red Hat's *[Source Document Title]* ([Chapter/Section]):
> "[Direct quote from Red Hat documentation]"

**Finding**: [What the MCP query revealed -- specific numbers, names, counts]
**Status**: [PASS / GAP / WARN] -- [one-line rationale from decision table]
**Recommendation**: Per Red Hat's *[Source]* ([Chapter/Section]): [specific action to take]
**Source URL**: [full URL to the Red Hat documentation page]
```

**Citation verification checklist** (self-check before outputting each domain):
- [ ] Does this finding include a direct Red Hat quote?
- [ ] Does the recommendation cite a specific Red Hat source (not just "Red Hat recommends")?
- [ ] Is the chapter/section number included (not just the document title)?
- [ ] Would someone reading this output know exactly which Red Hat doc page to visit?

**For scoped assessments**: Apply the same citation rigor. Even if assessing a single domain, the output must include the full Red Hat source attribution.

### Step 4: Adaptive Depth Queries (Scenario-Driven)

After the initial per-domain assessment, perform follow-up queries based on what was discovered. These are NOT executed for every assessment -- they fire only when specific conditions are met, adapting the assessment to the scenario.

Per the "Adaptive Depth Queries" section of governance-readiness.md:

**4a. If Domain 2 (Notifications) is PASS**: Verify notification templates are actually bound to job templates, not just existing unused. Query `job_templates_list` and check notification association fields. If all templates have empty notification bindings, **downgrade Domain 2 to WARN**.

**4b. If Domain 4 (Credentials) is PASS (multiple credentials)**: Check if the same credential is shared across templates targeting different inventories. Query `job_templates_list` and compare credential fields. If one credential spans dev and prod templates, **downgrade Domain 4 to WARN** with a separation-of-duties finding.

**4c. If Domain 3 (RBAC) is PASS (teams exist)**: Check whether team role assignments follow least privilege. Query `role_team_assignments_list` in detail. If any team has Admin-level access on organization-wide scope, **downgrade Domain 3 to WARN**.

**4d. Scale Calibration (always)**: Query `inventories_list` and `hosts_list` to determine environment scale. Calibrate severity framing: small lab (< 5 hosts, dev-only) vs enterprise (> 50 hosts, production inventories). Include the calibration context in the report preamble.

### Step 5: Cross-Domain Correlation

After all domains are assessed (including depth adjustments from Step 4), check for compound risks per the "Cross-Domain Correlation" section of governance-readiness.md:

**5a. RBAC GAP + Credentials exist**: Flag that without teams, credentials are necessarily user-scoped. Recommend fixing RBAC first.

**5b. No Workflows GAP + No Notifications GAP**: Flag the highest-risk combination -- no governance controls AND no visibility on production failures.

**5c. Single Instance Group + production and dev inventories**: Flag shared execution capacity between production and development workloads.

**5d. Multiple superusers + local-only auth**: Flag that superuser accounts without MFA/external auth have maximum blast radius.

Include compound findings in the report as a dedicated section AFTER the domain-by-domain findings.

### Step 6: Generate Summary Report

**For full assessment**: Produce the complete Governance Readiness Report following the output template in governance-readiness.md. Include:

1. Assessment date and AAP instance identifier
2. Scale calibration context (lab vs enterprise)
3. Per-domain findings with Red Hat citations (reflecting any depth-query adjustments from Step 4)
4. Compound Risk Analysis section (from Step 5 cross-correlation)
5. Summary table with all domain statuses
6. Overall score: X PASS, Y WARN, Z GAP out of 8 domains
7. **Recommended Fix Order** -- prioritized by dependency chain per governance-readiness.md
8. **Sources consulted** -- list all Red Hat documentation URLs referenced in the report

**For scoped assessment**: Produce a focused report for the requested domains:

1. Assessment date, scope statement ("Assessing: Credential Security"), and AAP instance
2. Scale calibration context
3. Per-domain findings for the scoped domains only (same mandatory citation format)
4. Depth-query results if triggered
5. Cross-domain correlations that involve the assessed domains (if any)
6. Status summary for assessed domains
7. **Sources consulted** -- list Red Hat documentation URLs referenced
8. Offer: "Would you like me to run the full 7-domain assessment for complete coverage?"

### Step 7: Offer Remediation

For any domains with GAP or WARN status, offer to remediate using MCP write tools where available:

| Domain | Remediation Available via MCP? | Tool |
|---|---|---|
| Workflow Governance | No (manual) | N/A |
| Notification Coverage | **Yes** | `notification_templates_create` |
| Access Control (RBAC) | **Yes** | `teams_create`, `role_user_assignments_create` |
| Credential Security | **Yes** | `credentials_create` |
| Execution Environments | **Yes** | `execution_environments_create` |
| Workload Isolation | **Yes** | `instance_groups_create` |
| Audit Trail | No (automatic) | N/A |
| External Authentication | **Yes** | `authenticators_create` |

**Human-in-the-Loop**: Before creating or modifying any resource, present the planned change and ask for explicit user approval.

## Dependencies

### Required MCP Servers
- `aap-mcp-job-management` - Workflow and job template data
- `aap-mcp-inventory-management` - Inventory data
- `aap-mcp-configuration` - Notifications, EEs, settings
- `aap-mcp-security-compliance` - Credentials and credential types
- `aap-mcp-system-monitoring` - Instance groups and activity stream
- `aap-mcp-user-management` - Users, teams, roles, authenticators

### Required MCP Tools
- `workflow_job_templates_list`, `job_templates_list` (from job-management)
- `notification_templates_list` (from configuration)
- `execution_environments_list` (from configuration)
- `users_list`, `teams_list`, `role_user_assignments_list`, `role_team_assignments_list`, `authenticators_list` (from user-management)
- `credentials_list`, `credential_types_list` (from security-compliance)
- `instance_groups_list`, `activity_stream_list` (from system-monitoring)

### Related Skills
- `aap-mcp-validator` - Prerequisite: validate all 6 servers first
- `execution-summary` - Generate audit trail after assessment

### Reference Documentation
- [governance-readiness.md](docs/aap/governance-readiness.md) - The 7-domain assessment reference

## Critical: Human-in-the-Loop Requirements

This skill requires explicit user confirmation at the following steps:

1. **Before Remediation Actions**
   - Display the planned change (e.g., "Create team 'automation-operators'")
   - Ask: "Should I create this resource to address the gap?"
   - Wait for explicit user confirmation

2. **Never auto-remediate**: Always present findings first and wait for user decision on remediation

## Example Usage

### Example 1: Full Assessment

**User**: "Assess my AAP platform's governance readiness"

**Agent**:

1. Reads governance-readiness.md
2. Scope detection: full assessment (all 7+1 domains)
3. Validates all 6 MCP servers via aap-mcp-validator
4. Queries each server (Step 2)
5. Assesses each domain -- every finding includes Red Hat quote, chapter/section, and source URL
6. **Adapts**: Notifications exist but aren't bound to any templates → downgrades Domain 2 from PASS to WARN
7. **Adapts**: Only 3 hosts in a single dev inventory → calibrates severity
8. **Correlates**: No workflows AND no notifications → compound risk flagged
9. Produces full report with Red Hat sources list at the bottom
10. Offers remediation, starting with highest-priority gap

### Example 2: Scoped Assessment

**User**: "Can you assess my credentials setup in the AAP?"

**Agent**:

1. Reads governance-readiness.md (specifically Domain 4: Credential Security)
2. Scope detection: **Domain 4 (Credential Security)**. Also queries minimal RBAC data for cross-correlation.
3. Reports: "You asked about credentials -- I'll assess Domain 4 (Credential Security) and check for related cross-domain impacts."
4. Validates `aap-mcp-security-compliance` and `aap-mcp-user-management` (for correlation)
5. Queries `credentials_list`, `credential_types_list`, and `teams_list` (for correlation)
6. Assesses with Red Hat citations:

   ```
   ### Domain 4: Credential Security — WARN

   Per Red Hat's *Configuring Automation Execution* (Ch. 15, Sec. 15.1.5):
   > "Enforce separation of duties...different credentials for different pieces of automation."

   **Finding**: Found 2 credentials, both of type "Machine." Credential "ssh-key" (ID: 3) is used across both dev and production job templates.
   **Status**: WARN -- credentials exist but lack separation of duties
   **Recommendation**: Per Red Hat's *Security Best Practices* (Ch. 15, Sec. 15.1.5): Create separate credentials per environment.
   **Source URL**: https://docs.redhat.com/en/.../configuring_automation_execution/controller-security-best-practices
   ```

7. **Correlates**: Checks RBAC -- no teams exist → flags compound: "Without teams, credentials are necessarily user-scoped (Ch. 15, Sec. 15.1.4). Fix RBAC first to enable team-scoped credential management."
8. Offers: "Would you like me to run the full 7-domain assessment for complete coverage?"
