---
name: playbook-generator
description: |
  **CRITICAL**: This skill ONLY GENERATES playbooks. It does NOT EXECUTE them. For execution, use /playbook-executor skill.

  Generate production-ready Ansible remediation playbooks for CVE vulnerabilities with Red Hat best practices, error handling, and Kubernetes safety patterns.

  Use when:
  - "Generate a remediation playbook for CVE-X"
  - "Create playbook for these CVEs"
  - "Get remediation playbook from Lightspeed"

  This skill calls the MCP tool (remediations__create_vuln_playbook) and returns the playbook **AS IS**. Do NOT modify, enhance, or add to the generated playbook. Any change requires explicit user validation first.

  **IMPORTANT**: 
  - ALWAYS use this skill instead of calling create_vulnerability_playbook directly
  - NEVER execute playbooks using ansible-playbook CLI
  - ALWAYS delegate execution to /playbook-executor skill
model: inherit
color: yellow
license: Apache-2.0
allowed-tools: remediations__create_vuln_playbook
---

# Ansible Playbook Generator Skill

This skill generates Ansible remediation playbooks for CVE vulnerabilities, applying Red Hat best practices, RHEL-specific patterns, and Kubernetes safety considerations.

**Integration with Remediation Skill**: The `/remediation` skill orchestrates this skill as part of its Step 4 (Generate Playbook) workflow. For standalone playbook generation, you can invoke this skill directly.

## When to Use This Skill

**🚨 CRITICAL SCOPE LIMITATION**: This skill **ONLY GENERATES** playbooks. It does **NOT EXECUTE** them.

**Use this skill directly when you need**:
- Generate a remediation playbook for a specific CVE
- Create batch remediation playbooks for multiple CVEs
- Get a remediation playbook from Red Hat Lightspeed (returned unmodified)
- Standalone playbook generation without full remediation workflow

**Do NOT use this skill when you need**:
- "Create playbook and execute it" → Use `/remediation` skill (orchestrates this skill + playbook-executor)
- "Remediate CVE-X" (full workflow) → Use `/remediation` skill
- Execute playbooks → Use `/playbook-executor` skill instead
- Run ansible-playbook CLI → Use `/playbook-executor` skill via AAP MCP
- Monitor job execution → Use `/playbook-executor` skill instead

**Use the `/remediation` skill when you need**:
- End-to-end CVE remediation (analysis → validation → playbook → execution → verification)
- Integrated impact analysis before playbook generation
- System context gathering and remediation strategy determination
- Execution guidance and verification workflows

**How they work together**: 
1. The `/remediation` skill orchestrates this skill after gathering system context
2. This skill generates the optimized playbook
3. The remediation skill then invokes `/playbook-executor` for execution via AAP MCP
4. Finally, `/remediation-verifier` confirms success

## Workflow

**🚨 Tool Failure Rule**: If `create_vulnerability_playbook` (or `create_vuln_playbook`) fails, STOP. Present options (retry / generate from knowledge with user confirmation / exit). Never auto-generate from your knowledge.

### 1. Playbook Generation (MCP Tool)

**MCP Tool**: `create_vulnerability_playbook` or `remediations__create_vulnerability_playbook` (from lightspeed-mcp)

**Parameters** (tool may use `cve_ids`/`cves` and `system_ids`/`uuids`—check tool schema):
- `cves` or `cve_ids`: Array of CVE identifiers
  - Example: `["CVE-2024-1234"]`
  - Format: CVE-YYYY-NNNNN strings
- `uuids` or `system_ids`: Array of system UUIDs from Red Hat Lightspeed inventory
  - Example: `["uuid-1", "uuid-2"]`
  - Format: UUID strings (get from system-context skill)
- `playbook_name`: Name for the playbook (if required by tool)

**Expected Output**: Ansible playbook YAML from Red Hat Lightspeed.

**CRITICAL — Return AS IS**: You MUST return the playbook exactly as the MCP tool provides it. Do NOT add pre-flight checks, backups, service restarts, audit logging, or any other modifications. The MCP tool description states: "Don't process the playbook. You MUST return the YAML as is." Any enhancement requires explicit user approval—offer modifications only after user requests them.

#### When MCP Tool Fails (REQUIRED Error Handling)

**🚨 CRITICAL**: When `create_vulnerability_playbook` (or `remediations__create_vulnerability_playbook`) returns an error, you MUST NOT generate a playbook from your own knowledge. Stop and present options to the user.

**If the tool returns error** (e.g., "Unhandled error", timeout, 500, connection failure):

1. **Report the failure** to the user with the error message
2. **Present these options** and wait for explicit user choice:

```
❌ Red Hat Lightspeed playbook generation failed: [error message]

**Next steps** (choose one):

(A) **Retry** - Try the MCP tool again (may succeed if transient)
(B) **Generate from knowledge** - Create a playbook using documentation templates (⚠️ NOT from Red Hat Lightspeed; requires your explicit approval)
(C) **Exit** - Stop playbook generation; user can retry later or use manual remediation

❓ Reply with A, B, or C:
```

3. **Execute based on user choice**:
   - **A (Retry)**: Call the MCP tool again. If it fails again, present options again (limit retries to 2; after 2 failures, present B and C only)
   - **B (Generate from knowledge)**: ONLY proceed if user explicitly chose B. Use documentation (cve-remediation-templates.md, package-management.md) to build a playbook. Add disclaimer: "Generated from documentation templates—Red Hat Lightspeed API was unavailable. Review carefully before execution."
   - **C (Exit)**: Stop. Do not generate any playbook. Suggest: "You can retry later when Lightspeed MCP is available, or create a manual remediation playbook."

**NEVER** auto-generate a playbook from your knowledge when the tool fails without explicit user confirmation for option B.

### 5. Return Playbook AS IS (No Modifications)

**CRITICAL**: Return the playbook exactly as the MCP tool provides it. Do NOT add, remove, or modify any content.

**Do NOT**:
- Add pre-flight checks (RHEL validation, subscription check)
- Add backup/snapshot creation
- Add service restart logic
- Add audit logging
- Add Kubernetes pod eviction
- Replace or wrap the MCP output with documentation templates

**If the user requests enhancements** (e.g. "add pre-flight checks", "add backup step"):
1. Show the original playbook first
2. Ask: "The playbook above is from Red Hat Lightspeed. You requested [enhancement]. Should I create a modified version with these additions? (yes/no)"
3. Only if user confirms "yes", create a modified version and show the diff
4. Require explicit approval before any modified playbook is used

### 6. Playbook Validation (Minimal)

Before returning, verify only:
- YAML is returned (the MCP tool output)
- No modifications were applied

Do NOT validate for "best practices" or add missing elements—return AS IS.

## Dependencies

### Required MCP Servers
- `lightspeed-mcp` - Red Hat Lightspeed platform access

### Required MCP Tools
- `remediations__create_vuln_playbook` (from lightspeed-mcp) - Generate remediation playbook from Red Hat Lightspeed
  - Parameters: playbook_name, cves (array), uuids (array of system UUIDs)
  - Returns: Ansible playbook YAML—**return AS IS**, do not modify

### Related Skills
- `cve-impact` - Provides CVE severity and risk assessment to inform playbook complexity
- `system-context` - Provides system inventory and deployment context for playbook targeting
- `remediation-verifier` - Verifies playbook execution success after deployment
- `playbook-executor` - Executes generated playbooks and tracks job status

### Reference Documentation
- [cve-remediation-templates.md](docs/ansible/cve-remediation-templates.md) - Ansible playbook templates for different CVE types
- [package-management.md](docs/rhel/package-management.md) - RHEL package management best practices (DNF vs YUM, reboot detection)

## Critical: Human-in-the-Loop Requirements

This skill generates code that will execute on production systems. **Explicit user confirmation is REQUIRED** before returning the playbook.

**When MCP Tool Fails** (REQUIRED):
- Do NOT generate a playbook from your own knowledge without explicit user confirmation
- Present options: (A) Retry, (B) Generate from knowledge (requires user approval), (C) Exit
- Wait for user to choose A, B, or C before proceeding
- If user chooses B: Add disclaimer that playbook was generated from documentation, not Red Hat Lightspeed

**Before Playbook Return** (REQUIRED):
1. **Display Playbook Preview**: Show complete playbook YAML to user
2. **Display Metadata**: Show CVE IDs, target systems, reboot requirements, Kubernetes considerations
3. **Ask for Confirmation**:
   ```
   ❓ Review the playbook above. This playbook will:
   - Update packages on N systems
   - Require reboot: [Yes/No]
   - Affect Kubernetes pods: [Yes/No]

   Should I provide this playbook for execution?

   Options:
   - "yes" or "proceed" - Provide playbook for execution
   - "modify" - Request changes to playbook
   - "abort" - Cancel playbook generation

   Please respond with your choice.
   ```
4. **Wait for Explicit Confirmation**: Do not provide playbook without "yes" or "proceed"

**Never assume approval** - always wait for explicit user confirmation before providing executable playbooks.

### 7. Return Playbook

**🚨 CRITICAL**: This skill **ONLY GENERATES** playbooks. It does **NOT EXECUTE** them.

**ONLY after receiving explicit user confirmation**, return the production-ready playbook with metadata:

```yaml
# Playbook metadata to return:
playbook:
  file: remediation-CVE-YYYY-NNNNN.yml
  path: playbooks/remediation/remediation-CVE-YYYY-NNNNN.yml  # Full path for playbook-executor template matching
  content: |
    [Complete YAML playbook]

  metadata:
    cve_ids: ["CVE-YYYY-NNNNN"]
    target_systems: ["uuid-1", "uuid-2"]
    rhel_versions_supported: ["7", "8", "9"]
    requires_reboot: true/false
    kubernetes_safe: true/false
    estimated_duration_minutes: 15
    risk_level: "medium"  # based on reboot requirement

  execution_notes:
    - "Test in staging environment first"
    - "Schedule maintenance window if reboot required"
    - "Ensure kubectl access if Kubernetes systems"
    - "Back up critical data before execution"
```

## Critical: Execution Handoff

**🚨 THIS SKILL DOES NOT EXECUTE PLAYBOOKS**

After generating the playbook, if the user requests execution:

❌ **WRONG** - Do NOT use `ansible-playbook` CLI:
```bash
ansible-playbook remediation.yml --check  # ❌ This skill cannot do this
```

✅ **CORRECT** - Delegate to the `/playbook-executor` skill:
```markdown
I've generated the remediation playbook. To execute it in dry-run mode, I'll invoke the playbook-executor skill:

[Invoke /playbook-executor skill with the playbook content]
```

**When user asks to execute**:
1. Save the playbook to a file (if needed for reference)
2. Invoke `/playbook-executor` skill with instruction:
   ```
   "Execute this playbook for CVE-XXXX-YYYY in dry-run mode using AAP job template [ID]. Monitor job status and report results."
   ```
3. The playbook-executor skill handles all execution via AAP MCP tools

**Never attempt to**:
- Run `ansible-playbook` command directly
- Execute playbooks via Shell/Bash tool
- Use any local Ansible execution method

**Always delegate execution to** `/playbook-executor` skill.

## Output Template

When completing playbook generation, provide output in this format:

```markdown
# Remediation Playbook Generated

## CVE Information
**CVE ID**: CVE-YYYY-NNNNN
**Target Systems**: N systems
**RHEL Versions**: 7, 8, 9
**Requires Reboot**: Yes/No
**Kubernetes Safe**: Yes/No

## Playbook Features
✓ Generated by Red Hat Lightspeed (returned AS IS, no modifications)

## Playbook File: remediation-CVE-YYYY-NNNNN.yml

```yaml
[Complete playbook YAML]
```

## Next Steps: Execution

**🔴 IMPORTANT**: Do NOT execute this playbook using `ansible-playbook` CLI.

**✅ To execute this playbook**, invoke the `/playbook-executor` skill:

```markdown
Ready to execute? The playbook-executor skill will:
1. Add this playbook to your AAP Git project
2. Create/use an AAP job template
3. Execute in dry-run mode first (if requested)
4. Launch actual execution (with your approval)
5. Monitor job status and report results

Would you like me to invoke the playbook-executor skill now?
Options:
- "yes" or "execute" - Invoke playbook-executor skill
- "dry-run first" - Execute in check mode first
- "save only" - Just save the playbook file for later
```

**Execution Flow**:
1. **This skill** → Generates playbook (DONE ✓)
2. **playbook-executor skill** → Executes via AAP MCP tools
3. **remediation-verifier skill** → Verifies success after execution

**Safety Notes**:
- Playbook is from Red Hat Lightspeed—review before execution
- No modifications were applied; user may request enhancements separately
```

## Examples

### Example 1: Simple CVE

**User Request**: "Generate playbook for CVE-2024-1234 on 5 RHEL 8 systems"

**Skill Response**:
1. Call `remediations__create_vuln_playbook` with cves, uuids, playbook_name
2. Return the playbook **exactly as received**—no modifications
3. Ask for user confirmation before handoff to playbook-executor

### Example 2: Batch CVEs

**User Request**: "Generate playbook for CVE-2024-1234, CVE-2024-5678 on 20 systems"

**Skill Response**:
1. Call `remediations__create_vuln_playbook` with multiple CVE IDs and system UUIDs
2. Return the playbook **exactly as received**—no modifications
3. Ask for user confirmation before handoff to playbook-executor

## Error Handling

**CVE has no automated remediation**:
```
CVE-YYYY-NNNNN does not have an automated remediation playbook available in Red Hat Lightspeed.

Manual remediation required:
1. Affected packages: package-name-version
2. Recommended action: dnf update package-name
3. Verification: package-name --version

Would you like me to create a manual playbook template based on Red Hat best practices?
```

**Unsupported RHEL version**:
```
Target systems include RHEL 6, which is not supported by this skill.

Supported RHEL versions: 7, 8, 9

Please filter target systems to supported versions or consult Red Hat documentation for RHEL 6 remediation guidance.
```

**Kubernetes context missing**:
```
Target systems appear to be Kubernetes nodes but kubectl access is not configured.

To generate Kubernetes-safe playbooks, ensure:
1. kubectl is installed and configured
2. Access to cluster is available
3. Appropriate RBAC permissions for node operations

Proceeding with standard playbook (without pod eviction). Add pod eviction manually if needed.
```

## Best Practices

1. **🚨 NEVER EXECUTE PLAYBOOKS** - This skill generates only. Always delegate execution to `/playbook-executor` skill
2. **🚨 RETURN AS IS** - Do NOT modify the MCP-generated playbook. No enhancements without explicit user request and approval
3. **🚨 NEVER auto-generate on tool failure** - When the MCP tool fails, present options (retry / generate from knowledge with user confirmation / exit). Do NOT silently generate from your own knowledge
4. **Require user approval** - ALWAYS get explicit confirmation before providing playbooks for execution
5. **Clear handoff** - After generation, explicitly tell user to invoke `/playbook-executor` for execution

## Tools Reference

This skill uses:
- `remediations__create_vuln_playbook` (from lightspeed-mcp) - Generate playbook from Red Hat Lightspeed. Returns YAML **as is**—do not modify.

All MCP tools are provided by the lightspeed-mcp server configured in `mcps.json`.

## Integration with Other Skills

- **cve-impact**: Provides CVE severity and risk assessment to inform playbook complexity
- **system-context**: Provides system inventory and deployment context for playbook targeting
- **remediation-verifier**: Verifies playbook execution success after deployment

**Orchestration Example** (from `/remediation` skill):
1. Agent invokes cve-impact skill → Gets risk assessment
2. Agent gathers context → Determines deployment requirements
3. Agent invokes playbook-generator skill → Generates production-ready playbook
4. Agent provides execution guidance → User deploys playbook
5. Agent invokes remediation-verifier skill → Confirms success
