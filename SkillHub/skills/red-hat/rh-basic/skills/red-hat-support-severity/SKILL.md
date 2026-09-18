---
name: red-hat-support-severity
description: Help determine the correct severity level for a Red Hat support ticket, explain SLAs, and guide what information to include.
license: Apache-2.0
user_invocable: true
model: inherit
color: cyan
allowed-tools: cve-detail
---

# Red Hat Support Ticket Severity Helper

Extract from the user's message: product, what is happening, production vs dev/test, whether the system is completely down, whether a workaround exists, whether a CVE is involved. If environment type or outage status is unclear, ask before proceeding.

## Prerequisites

None.

## When to Use This Skill

When the user needs to determine the correct severity for a Red Hat support ticket.

## Workflow

1. Extract product, outage status, workaround availability, and CVE involvement from the user message.
2. Map situation to Sev 1–4 using the decision table below.
3. Return severity, SLA, and ticket preparation guidance.

## Dependencies

- `red-hat-security` MCP (optional): used for CVE severity lookup when a CVE is mentioned.

## Severity Decision

| Situation | Severity |
|---|---|
| Production down, business halted, no workaround | Sev 1 -- Critical |
| Production severely impaired, no workaround | Sev 2 -- High |
| Partial loss or workaround exists in production; significant dev/test impact | Sev 3 -- Medium |
| Minor issue, informational question, low dev/test impact | Sev 4 -- Low |

CVE adjustment: If a CVE is mentioned, call `cve-mcp -> cve-detail`. A Critical or Important CVE with a known exploit on an unpatched production system that is not fully down -> recommend Sev 2, not Sev 3.

## SLA Reference

| Severity | Premium -- initial response | Standard -- initial response | 24x7 |
|---|---|---|---|
| Sev 1 | 1 hour | 1 business hour | Premium: yes; Standard: business hours only |
| Sev 2 | 2 hours | 4 business hours | Must explicitly request when filing |
| Sev 3 | 4 business hours | 1 business day | No |
| Sev 4 | 1 business day | 2 business days | No |

SLAs are measured from case submission. For Sev 1/2, following up with a phone call reduces actual response time.

## Output

```
## Support Ticket Recommendation

**Recommended Severity:** Severity X -- [Critical / High / Medium / Low]

**Why:** [1-2 sentences connecting the user's situation to the severity criteria.]

**SLA -- what to expect:**

| | Premium | Standard |
|---|---|---|
| Initial response | [X] | [X] |
| 24x7 | [yes / no / must request] | [yes / no] |

**What to include in your ticket:**
- Product name and version
- Exact error messages or output
- Steps to reproduce or timeline of events
- Clear business impact statement (what is stopped or degraded, for how long)
- Any workaround you have tried
- [If RHEL, OCP, AAP, or Satellite: attach diagnostic data -- run `/red-hat-diagnostics` for commands]

**Filing tip:** [Sev 1/2 only: "Submit online, then immediately call your regional Red Hat support number. For Sev 2, explicitly request 24x7 coverage if needed outside business hours."]
```

Write for a sysadmin who needs to act now. If CVE lookup returns a severity, state it briefly ("Red Hat rates this CVE as Critical") and explain how it factored into the recommendation. Do not reproduce the full CVE explainer output.
