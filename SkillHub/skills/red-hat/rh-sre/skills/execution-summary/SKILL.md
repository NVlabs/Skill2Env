---
name: execution-summary
description: |
  Generates a concise report of agents, skills, tools, and documentation accessed during a workflow for audit and learning purposes.

  Use when:
  - "Generate execution summary"
  - "Create execution report"
  - "Summarize what was used"
  - "Show execution summary"
  - "What agents/skills/tools were used?"
model: haiku
color: blue
license: Apache-2.0
allowed-tools:
---

# Execution Summary Skill

Generate a concise execution report summarizing all agents, skills, tools, and documentation accessed during a workflow. Useful for audit trails, learning reviews, and workflow documentation.

## When to Use This Skill

Use this skill when:
- User requests an execution summary or report
- At the end of a remediation workflow to document what was executed
- Tracking resource usage for audit or compliance purposes
- Creating a learning record of a complex workflow
- Documenting which components contributed to a result

Do NOT use when:
- User wants detailed logs (use native logging instead)
- User wants performance metrics (use monitoring tools)
- Just listing available skills/agents (use documentation instead)

## Workflow

### Step 1: Analyze Conversation History

**Action**: Review the current conversation to identify all agents, skills, tools, and documentation used

**What to extract**:

1. **Agents invoked** - Look for agent invocations in the conversation
   - Example: Skill `remediation` (orchestration) → `rh-sre:remediation`
   - Include plugin prefix: `rh-sre:`

2. **Skills invoked** - Look for Skill tool calls
   - Example: `Skill(skill="fleet-inventory")` → `rh-sre:fleet-inventory`
   - Example: `Skill(skill="mcp-lightspeed-validator")` → `rh-sre:mcp-lightspeed-validator`
   - Include plugin prefix: `rh-sre:`

3. **MCP Tools called** - Look for MCP tool invocations
   - Example: `get_host_details` → `lightspeed-mcp:get_host_details`
   - Example: `vulnerability__get_cve` → `lightspeed-mcp:vulnerability__get_cve`
   - Example: `job_templates_launch_retrieve` → `aap-mcp-job-management:job_templates_launch_retrieve`
   - Include server prefix

4. **Documentation consulted** - Look for Read tool calls on documentation files
   - Pattern: Files under `rh-sre/docs/` or `rh-sre/skills/*/SKILL.md`
   - Extract only from `docs/` onwards
   - Example: `/path/to/rh-sre/docs/ansible/playbook-templates.md` → `docs/ansible/playbook-templates.md`
   - Example: `/path/to/rh-sre/skills/fleet-inventory/SKILL.md` → `skills/fleet-inventory/SKILL.md`
   - Include "I consulted [filename]" statements in conversation

**How to analyze**:
- Review the conversation from start to current message
- Track tool invocations in chronological order
- Deduplicate: each resource should appear only once
- Maintain original order of first appearance

### Step 2: Categorize and Deduplicate

**Action**: Organize extracted resources into categories and remove duplicates

**Categories**:
- **Agents**: Agent invocations
- **Skills**: Skill invocations
- **Tools**: MCP tool calls (group by server)
- **Docs**: Documentation files read

**Deduplication rules**:
- If an agent was invoked multiple times, list it once
- If a skill was invoked multiple times, list it once
- If a tool was called multiple times, list it once
- If a doc was read multiple times, list it once

**Sorting**:
- Within each category, maintain chronological order (order of first use)
- Do not alphabetize (preserve workflow sequence)

### Step 3: Format Output

**Action**: Generate the execution summary using the standard template

**Output template**:
```
**** EXECUTION SUMMARY START ****
Agents: <agent1>,<agent2>,...
Skills: <skill1>,<skill2>,...
Tools: <tool1>,<tool2>,...
Docs: <doc1>,<doc2>,...
**** EXECUTION SUMMARY END ****
```

**Formatting rules**:

1. **Agent names**: Include plugin prefix
   - Format: `rh-sre:agent-name`
   - Example: `rh-sre:remediation`
   - Separate with commas (no spaces): `rh-sre:remediation,rh-sre:validator`

2. **Skill names**: Include plugin prefix
   - Format: `rh-sre:skill-name`
   - Example: `rh-sre:fleet-inventory`
   - Separate with commas: `rh-sre:fleet-inventory,rh-sre:cve-impact`

3. **Tool names**: Include MCP server prefix
   - Format: `server-name:tool-name`
   - Example: `lightspeed-mcp:get_host_details`
   - Example: `aap-mcp-job-management:job_templates_list`
   - Separate with commas: `lightspeed-mcp:get_cve,lightspeed-mcp:get_host_details`

4. **Doc names**: Path from `docs/` onwards
   - Format: `docs/category/filename.md` or `skills/skill-name/SKILL.md`
   - Example: `docs/ansible/cve-remediation-templates.md`
   - Example: `skills/fleet-inventory/SKILL.md`
   - Separate with commas: `docs/ansible/playbook-templates.md,docs/insights/vulnerability-logic.md`

5. **Empty categories**: If no resources used, show "None"
   - Example: `Agents: None`

6. **Spacing**: No spaces after commas (compact format)

### Step 4: Present Summary

**Action**: Output the formatted summary to the user

**Presentation**:
```
I've generated the execution summary for this workflow:

**** EXECUTION SUMMARY START ****
Agents: None
Skills: rh-sre:remediation,rh-sre:fleet-inventory,rh-sre:cve-impact,rh-sre:playbook-generator,rh-sre:job-template-creator
Tools: lightspeed-mcp:get_host_details,lightspeed-mcp:get_cve,aap-mcp-job-management:job_templates_list
Docs: docs/ansible/cve-remediation-templates.md,docs/insights/vulnerability-logic.md,skills/fleet-inventory/SKILL.md
**** EXECUTION SUMMARY END ****

This summary shows all agents, skills, tools, and documentation used during the workflow.
```

**Additional context** (optional):
- Brief explanation of what each category represents
- Note any notable patterns (e.g., "Heavy use of Lightspeed MCP tools")
- Mention if summary is for audit/learning purposes

## Dependencies

### Required MCP Servers
None (analyzes conversation history only)

### Required MCP Tools
None (analyzes conversation history only)

### Related Skills
- None (standalone reporting skill)

### Reference Documentation
- None required (execution tracking skill)

## Example Usage

### Example 1: Simple Fleet Query Workflow

**User Request**: "Show the managed fleet, then generate execution summary"

**Workflow executed**:
1. Invoked `mcp-lightspeed-validator` skill
2. Invoked `fleet-inventory` skill
3. Called `get_host_details` MCP tool
4. Read `docs/insights/insights-api.md`

**Skill Response**:
```
I've generated the execution summary for this workflow:

**** EXECUTION SUMMARY START ****
Agents: None
Skills: rh-sre:mcp-lightspeed-validator,rh-sre:fleet-inventory
Tools: lightspeed-mcp:get_host_details
Docs: docs/insights/insights-api.md,skills/fleet-inventory/SKILL.md
**** EXECUTION SUMMARY END ****

This workflow used 2 skills, 1 MCP tool, and consulted 2 documentation files.
```

### Example 2: CVE Remediation Workflow

**User Request**: "Remediate CVE-2024-1234 on production systems, then show execution summary"

**Workflow executed**:
1. Invoked `remediation` skill
2. Remediation skill delegated to: `cve-validation`, `cve-impact`, `system-context`, `playbook-generator`, `playbook-executor` skills
3. Called multiple MCP tools: `get_cve`, `get_cve_systems`, `get_host_details`, `create_vulnerability_playbook`, `execute_playbook`
4. Read multiple docs: CVE scoring, Ansible templates, remediation verification

**Skill Response**:
```
I've generated the execution summary for this workflow:

**** EXECUTION SUMMARY START ****
Agents: None
Skills: rh-sre:remediation,rh-sre:cve-validation,rh-sre:cve-impact,rh-sre:system-context,rh-sre:playbook-generator,rh-sre:job-template-creator
Tools: lightspeed-mcp:get_cve,lightspeed-mcp:get_cve_systems,lightspeed-mcp:get_host_details,lightspeed-mcp:create_vulnerability_playbook,aap-mcp-job-management:job_templates_launch_retrieve
Docs: docs/references/cvss-scoring.md,docs/ansible/cve-remediation-templates.md,docs/insights/vulnerability-logic.md,skills/playbook-generator/SKILL.md
**** EXECUTION SUMMARY END ****

This comprehensive remediation workflow used the remediation skill that orchestrated 5 skills, invoked 5 MCP tools, and consulted 4 documentation files.
```

### Example 3: Validation Only Workflow

**User Request**: "Validate Lightspeed MCP and generate summary"

**Workflow executed**:
1. Invoked `mcp-lightspeed-validator` skill
2. No MCP tools called (connectivity test unavailable)
3. No docs consulted

**Skill Response**:
```
I've generated the execution summary for this workflow:

**** EXECUTION SUMMARY START ****
Agents: None
Skills: rh-sre:mcp-lightspeed-validator
Tools: None
Docs: None
**** EXECUTION SUMMARY END ****

This lightweight validation workflow used 1 skill with no MCP tool invocations or documentation consultation.
```

## Error Handling

### Incomplete Conversation History

**Scenario**: Conversation history is not available or truncated

**Response**:
```
⚠ Execution Summary: INCOMPLETE

Unable to generate complete summary due to limited conversation history.

Partial summary based on available context:
**** EXECUTION SUMMARY START ****
Agents: [partial list]
Skills: [partial list]
Tools: [partial list]
Docs: [partial list]
**** EXECUTION SUMMARY END ****

Note: This summary may not include all resources used earlier in the conversation.
```

### No Workflow Executed

**Scenario**: User requests summary but no workflow has been executed

**Response**:
```
ℹ️ No execution to summarize

No agents, skills, or tools have been invoked in this conversation yet.

To generate a meaningful execution summary:
1. Execute a workflow (e.g., "Show the fleet", "Remediate CVE-X")
2. Then request the execution summary

Would you like to start a workflow now?
```

### Ambiguous Resource Names

**Scenario**: Uncertain about which plugin/server a resource belongs to

**Response**:
Include the resource with a note:
```
**** EXECUTION SUMMARY START ****
Agents: None
Skills: rh-sre:remediation,rh-sre:fleet-inventory,unknown-plugin:custom-skill
Tools: lightspeed-mcp:get_cve
Docs: docs/ansible/playbook-templates.md
**** EXECUTION SUMMARY END ****

Note: "unknown-plugin:custom-skill" origin unclear - verify plugin source.
```

## Best Practices

1. **Analyze entire conversation** - Don't miss early invocations
2. **Deduplicate resources** - Each resource appears once
3. **Maintain chronological order** - Preserve workflow sequence
4. **Use exact prefixes** - `rh-sre:`, `lightspeed-mcp:`, etc.
5. **Compact format** - No spaces after commas
6. **Include all categories** - Even if "None"
7. **Extract docs from "I consulted" statements** - These indicate documentation usage
8. **Path from docs/ onwards** - Not full filesystem paths
9. **Brief explanation** - Help user understand the summary
10. **Handle edge cases gracefully** - Empty workflows, incomplete history

## Use Cases

**Audit Trail**:
- Document which components were used for compliance
- Track MCP tool access patterns
- Record skill usage for billing/metrics

**Learning & Training**:
- Show new users which resources solve specific problems
- Demonstrate skill orchestration patterns
- Illustrate skill orchestration workflows

**Troubleshooting**:
- Identify which tools were called before an error
- Trace skill invocation sequence
- Document successful workflows for reproduction

**Workflow Documentation**:
- Create records of complex remediation processes
- Document resource usage for similar future tasks
- Build a library of workflow patterns

## Integration with Other Skills

This skill complements other rh-sre skills:

**After `/remediation` skill**:
```
User: "Remediate CVE-X"
→ `/remediation` skill executes full workflow (invoked)
User: "Generate execution summary"
→ execution-summary shows complete resource usage
```

**For learning workflows**:
```
User: "Show the fleet"
→ fleet-inventory skill executes
User: "What did you use to do that?"
→ execution-summary shows skills and tools invoked
```

**For audit purposes**:
```
User: "Create playbook for CVE-X and generate audit trail"
→ Workflow executes
→ execution-summary provides compliance record
```

The summary output format is designed to be:
- **Machine-readable**: Parseable by scripts/tools
- **Human-readable**: Clear and concise for users
- **Compact**: Minimal token usage
- **Complete**: All resource categories represented
- **Auditable**: Chronological order preserved
