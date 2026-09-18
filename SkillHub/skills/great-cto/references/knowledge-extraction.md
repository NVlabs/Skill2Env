---
name: knowledge-extraction
description: Schema for structured extraction from incidents/blocked QA/audits: feeds global pattern library that surfaces at next ARCH time
when_to_use: Crystallizing learnings via /crystallize. Read by senior-dev + project-auditor
applies_to:
  - _default
---

# Knowledge Extraction Protocol

> Schema and instructions for structured knowledge extraction after resolved incidents,
> blocked QA runs, and completed audits. Extracted knowledge feeds the global pattern
> library (`~/.great_cto/global-patterns/`) and drives agent evolution via `/crystallize`.
>
> **Privacy rule:** KE files and GP files never contain project names, client names,
> URLs, credentials, or any data that could identify a specific system. Use generic
> technology descriptors only (e.g., "PostgreSQL datasource", not "client-db-prod").

---

## When to extract

| Agent | Trigger condition |
|-------|------------------|
| `l3-support` | Incident resolved AND `iterations > 3` OR MTTR > 2h |
| `l3-support` | Any P0 incident regardless of iteration count |
| `qa-engineer` | Test blind spot found (bug escaped QA, found in production) |
| `qa-engineer` | Advisor called more than once in a single QA run |
| `security-officer` | New vulnerability class not covered by existing checklist |
| `architect` | ADR superseded within 30 days of creation |
| `project-auditor` | Same debt category found in two consecutive audits |
| `senior-dev` | Advisor called AND root cause was absent from ARCH doc |

Extraction is **mandatory** when triggered — not optional. Write the KE file before emitting DONE.

---

## KE File Format

**Location:** `~/.great_cto/extractions/KE-<YYYY-MM-DD>-<slug>.yaml`
(local machine only — never committed to repo)

**Slug:** kebab-case description of the root cause class (technology + symptom).
Example: `datasource-null-jsondata-field` not `my-project-grafana-bug`.

```yaml
# Knowledge Extraction — written by <agent-name>
# APPEND-ONLY. If understanding evolves: create KE-<slug>-v2.yaml.
# PRIVACY: no project names, URLs, credentials, or identifying data.

ke_id: KE-<YYYY-MM-DD>-<slug>
date: <YYYY-MM-DD>
source_agent: <agent-name>
source_type: incident | qa-escape | security-gap | arch-rework | audit-recurrence

# === SYMPTOM (observable, technology-generic) ===
symptom:
  observable: >
    One sentence: what was visible to the engineer before investigation.
    Generic: mention technology, not project.
  first_signal: >
    What was the first concrete symptom that prompted investigation.
  misleading_signals:
    - "<technology behavior that looked like root cause but wasn't>"
    - "<another false lead>"

# === INVESTIGATION ===
investigation:
  iterations: <N>           # number of hypothesis-test cycles before resolution
  dead_ends:
    - tried: "<diagnostic method or tool>"
      outcome: "<why it gave a false negative or no signal>"
    - tried: "<another method>"
      outcome: "<result>"
  breakthrough: >
    One sentence: what finally revealed the root cause.
  breakthrough_tool: <tool-or-method>   # e.g., playwright-browser-console, strace, heap-dump

# === ROOT CAUSE ===
root_cause:
  mechanism: >
    Technical explanation of why the system behaved this way.
    Generic — describes the technology pattern, not the specific system.
  category: >
    One of: config-null-default | schema-migration-partial | auth-path-bypass |
    race-condition | dependency-version-mismatch | env-var-missing |
    legacy-api-field | resource-exhaustion | encoding-mismatch | other
  stack_fingerprint: "<tech1> + <tech2> + <condition>"
  # Example: "grafana + provisioning-yaml + version-upgrade"

# === RESOLUTION ===
resolution:
  fix: >
    Generic description of the fix. No project-specific values.
  verification: >
    How to confirm the fix worked. Reproducible method.
  time_to_fix_once_found: <Nm>     # minutes from root cause identification to fix
  total_investigation_time: <Nh>   # hours from incident start to root cause

# === LEARNING ===
learning:
  detection_order_next_time:
    - "<step 1: what to check first — the breakthrough tool/method>"
    - "<step 2: what to check second>"
    - "<step N: only then do the standard checks>"
  detection_method_that_worked: <method>
  detection_methods_that_failed:
    - <method-1>
    - <method-2>
  why_standard_checks_missed_it: >
    Explanation of why the normal diagnostic chain (logs, API, health check)
    gave false negatives for this class of issue.
  pattern_candidate: true | false
  pattern_applies_to:
    - <technology-1>
    - <technology-2>

# === ROUTING ===
# Either target_agent (workflow change in one agent) OR target_skill (shared reference doc).
# Use target_skill when the knowledge applies across multiple agents (e.g. a new LogQL pattern,
# a new postmortem rule, a new threat-model technique). Use target_agent when the change only
# matters for one agent's workflow (e.g. l3-support's Step 2 priority order).
target_agent: <agent-name>             # OR
target_skill: <skill-file-relative-path>  # e.g. "skills/great_cto/references/grafana-ops.md"
target_section: "<section in target file to update>"
proposed_change: >
  One paragraph: concrete change to agent workflow OR concrete addition to the skill doc.
  Example (agent): "Add Playwright browser console check as Priority 0
  in Step 2 (Check logs) for any tool that has a browser-rendered UI,
  before running API-level diagnostics."
  Example (skill): "Add LogQL pattern P-007 to grafana-ops.md → ## LogQL patterns:
  '{service=$svc} |~ \"jsonData.*null\" | line_format ...'"
mttr_reduction_estimate: "<before> → <after> (<percent>%)"
confidence: high | medium | low
```

---

## Example KE (anonymized)

```yaml
ke_id: KE-2026-04-25-datasource-null-jsondata-field
date: 2026-04-25
source_agent: l3-support
source_type: incident

symptom:
  observable: >
    Dashboard panels render empty ("No data") despite healthy DB connection
    and correct query syntax.
  first_signal: >
    Grafana panel shows no results; direct DB query returns expected rows.
  misleading_signals:
    - "Connection pool metrics show no errors"
    - "Grafana /api/ds/query returns HTTP 200"
    - "Docker container logs show no errors"

investigation:
  iterations: 8
  dead_ends:
    - tried: "PromQL/LogQL query syntax review"
      outcome: "Queries correct — not the cause"
    - tried: "curl /api/ds/query with rawSql"
      outcome: "Returns data — bypasses the frontend null check"
    - tried: "Docker container logs"
      outcome: "No errors logged — issue is browser-side only"
    - tried: "Grafana REST API datasource listing"
      outcome: "Shows datasource as healthy — does not expose jsonData.database null"
  breakthrough: >
    Playwright opened the dashboard URL with auth header and captured
    browser console.error — revealed "You do not currently have a default
    database configured for this data source" appearing only in browser JS.
  breakthrough_tool: playwright-browser-console

root_cause:
  mechanism: >
    Grafana 10 plugin reads database from jsonData.database (nested).
    Legacy provisioning YAML sets it as a top-level field (database:).
    Plugin sees null, silently drops every query on the frontend.
    Backend /api/ds/query accepts explicit rawSql so bypasses this check.
  category: legacy-api-field
  stack_fingerprint: "grafana-10 + provisioning-yaml + postgresql-plugin"

resolution:
  fix: >
    Move database field from top-level to jsonData.database in datasource
    provisioning YAML. Reload Grafana provisioning.
  verification: >
    Playwright headless: load dashboard URL with auth, assert
    console.error count = 0 and panel data row count > 0.
  time_to_fix_once_found: 5m
  total_investigation_time: 4h

learning:
  detection_order_next_time:
    - "Run Playwright browser console capture FIRST for any browser-rendered tool"
    - "Check jsonData.* fields in provisioning YAML for null values"
    - "Only then: API-level debugging"
  detection_method_that_worked: playwright-browser-console
  detection_methods_that_failed:
    - docker-logs
    - grafana-rest-api
    - curl-ds-query
    - promql-query-review
  why_standard_checks_missed_it: >
    The validation runs only in browser JavaScript (frontend plugin code).
    Backend API accepts rawSql directly, bypassing the null check.
    No server-side error is emitted — the failure is invisible to all
    server-side diagnostic tools.
  pattern_candidate: true
  pattern_applies_to:
    - grafana
    - any-browser-rendered-datasource-plugin
    - grafana-version-upgrade

target_agent: l3-support
target_section: "## Monitoring Workflow → Step 2 (Check logs) → Priority 0"
proposed_change: >
  Before running Grafana API calls: if the monitored system has a browser-rendered
  UI (Grafana, Kibana, custom dashboard), run Playwright browser console capture
  as the first diagnostic step. Browser console.error reveals issues that are
  invisible to all server-side tools (API, logs, health endpoints).
mttr_reduction_estimate: "4h → 15min (94%)"
confidence: high
```

---

## Privacy Checklist (run before saving any KE file)

```bash
# Scan KE file for private data before saving
KE_FILE="~/.great_cto/extractions/KE-<slug>.yaml"

# Forbidden patterns — must not appear in KE files
FORBIDDEN=(
  "https://"           # URLs
  "http://"
  ".grafana.net"
  ".com\|\.io\|\.net"  # domains
  "@"                  # email addresses
  "password\|secret\|token\|key\|api_key"  # credentials
  "AKIA\|sk-\|glsa_"  # specific key patterns
)

for pattern in "${FORBIDDEN[@]}"; do
  if grep -q "$pattern" "$KE_FILE" 2>/dev/null; then
    echo "PRIVACY_VIOLATION: pattern '$pattern' found in $KE_FILE"
    echo "Replace with generic technology descriptor before saving"
  fi
done
```

If any violation found → do NOT save the KE file. Rewrite the offending fields with generic language.

---

## From KE to GP (the crystallize step)

After writing the KE file, the agent emits:

```
KE_WRITTEN: ~/.great_cto/extractions/KE-<slug>.yaml
confidence=high | iterations=8 | target=l3-support
Run /crystallize to review and promote to global pattern.
```

`/crystallize` reads all KE files, generates proposals, and presents them for CTO approval.
See `commands/crystallize.md` for the full workflow.
