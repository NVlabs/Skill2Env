# Remediation Plan Template

Read this reference when presenting plans for user validation.

## Part A: Upfront Planned Tasks (Before Step 0)

**When**: Before executing any step. Present immediately after the user requests remediation.

**Purpose**: Let the user validate the approach before any work begins.

**Format**:
```
## Remediation: CVE-XXXX-YYYY

**Planned tasks** (in order—use this exact order for TodoWrite/task lists; display order must match execution order):
1. Validate MCP (Lightspeed, AAP)
2. Impact analysis (assess CVE risk)
3. CVE validation (remediatable gate)
4. System context (affected systems, RHEL versions)
5. Generate playbook
6. Dry-run → User confirms → Execute
7. Verify (optional)

❓ Proceed with this plan?
- "yes" or "proceed" — I'll start with Step 0 (validate MCP)
- "abort" — Cancel
```

**Wait for user response** before invoking Step 0. Do NOT start any step until the user confirms.

---

## Part B: Execution Plan (After Step 4, Before Step 5)

**When**: After Step 4 (playbook generated) and before Step 5 (execution). The user must validate before proceeding.

## Part B Format

### 1. Summary (1–2 sentences)

```
## Remediation Plan: CVE-XXXX-YYYY

**Summary**: [One sentence describing what will happen and why.]
Example: "Remediate CVE-2026-24882 on ip-172-31-32-201 via Ansible playbook (httpd update to address CVE)."
```

### 2. Table (CVE, systems, key actions)

```
| CVE | Target Systems | Key Action |
|-----|----------------|------------|
| CVE-XXXX-YYYY | hostname-1, hostname-2 | Update package: httpd 2.4.x → 2.4.y |
```

For batch: one row per CVE or combined row if same action.

### 3. Checklist (ordered steps)

```
**Execution steps**:
☐ Step 0: Validate MCP (Lightspeed, AAP) — done
☐ Step 1: Impact analysis — done
☐ Step 2: CVE validation — done
☐ Step 3: System context — done
☐ Step 4: Generate playbook — done
☐ Step 5: Dry-run → Confirm → Execute
☐ Step 6: Verify (optional)
```

Mark completed steps as "— done". Show only remaining steps as checkboxes if preferred.

### 4. Confirm Prompt

```
❓ Confirm to proceed?

- "yes" or "proceed" — Run dry-run first, then execute
- "dry-run only" — Run dry-run only, no execution
- "abort" — Cancel remediation

Please respond with your choice.
```

**Wait for explicit user response** before invoking playbook-executor.
