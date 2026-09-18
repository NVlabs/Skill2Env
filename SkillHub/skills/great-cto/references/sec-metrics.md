---
name: sec-metrics
description: Five security metrics: vulnerability MTTR, patch SLA, security-debt count, audit-finding closure rate, mean-time-to-detect
when_to_use: Engineering health monitoring. Read by security-officer + /sec command
applies_to:
  - _default
---

# Security metrics — reference

Five metrics that, taken together, describe the **security posture trend** of a codebase. Computed from artefacts great_cto already produces (PM-SEC, threat models, SBOM, CSO reports, dependency manifests). No new telemetry, no external scanners required.

See `skills/great_cto/references/secure-sdlc.md` for how these metrics close SSDF practice RV (respond to vulnerabilities) and support DORA Art. 15 (ongoing monitoring).

## The five numbers

| Metric | Formula in great_cto | Healthy threshold |
|---|---|---|
| **CVE MTTR** | median(resolved_at − public_advisory_at) for CVEs in last 90d | < 14 days (critical < 7d) |
| **Dependency freshness** | % of direct deps with age ≤ 180 days since their latest release | ≥ 70% |
| **Threat-model coverage** | % of features shipped in window with ARCH `## Security` section + `TM-<slug>.md` | ≥ 90% for security-critical archetypes |
| **Pentest burn-down** | open_findings / (open_findings + closed_findings_in_window), weighted by severity | trend down-and-right |
| **Secret rotation overdue** | count(secrets past `rotation_due`) | = 0 |

Run: `/sec [period_days]` (default 30). Snapshot appended to `.great_cto/sec-baseline.log`.

## Why these five

The four classic DORA metrics answer "is delivery healthy?" They don't ask "is the code getting safer or more dangerous over time?" These five fill that gap:

- **CVE MTTR** — the one security metric a CISO always asks for. If CVEs sit open for a month, no amount of threat modelling compensates.
- **Dependency freshness** — stale deps are the single largest source of exploitable vulns in modern apps (see log4shell, OpenSSL CVE-2022-3602, any left-pad-class incident). Freshness is a leading indicator, MTTR is lagging.
- **Threat-model coverage** — proxy for "is the team doing design-time security" (SSDF PW.1). Low coverage means security is bolted on, not built in.
- **Pentest burn-down** — if you're paying for pentests, finding closure rate tells you whether the team treats findings as real work or theatrical.
- **Secret rotation overdue** — the only binary metric in the set. Either you rotate on schedule or you don't.

Deliberately **not** included:

- **SAST finding count** — too noisy, too tool-dependent. A baseline diff (new findings vs. previous run) is more useful but lives in `security-officer` reports, not here.
- **Code coverage of security tests** — unfalsifiable. 100% coverage of irrelevant paths doesn't mean anything.
- **Bug-bounty submissions** — too intermittent to trend.

## Data sources

| Metric | Source |
|---|---|
| CVE MTTR | `docs/cve-log.md` — append-only log of CVEs affecting us (added by `security-officer` during `/audit` CVE scan) |
| Dependency freshness | `docs/releases/SBOM-*.json` latest entry + npm/PyPI/crates.io release timestamps (cached) |
| Threat-model coverage | `docs/architecture/ARCH-*.md` with `## Security` section + `docs/threat-models/TM-*.md` existence, filtered by features in window |
| Pentest burn-down | `docs/security/PENTEST-*.md` finding tables (added when pentests run) |
| Secret rotation | `.great_cto/secrets.md` — a register of secrets with `rotation_due:` date |

If a source is absent, the metric reports `-` (no data). Never fabricate.

## Gaming guards

Like DORA metrics, these are manipulable. `/sec` runs two automated checks:

| Manipulation | What it looks like | Detection |
|---|---|---|
| **Closing findings without fixing** | Pentest burn-down drops fast, CVE-MTTR stays flat | Finding reopen rate > 10% in 90d → flag |
| **Selective dep updates** | Freshness rises but only for tiny utility deps, not critical ones | Median age of top-10 deps by import count must match overall median within 30d |

These appear in `/sec` output as `⚠ Gaming check:` lines.

## Signals in `/inbox`

Health signals fire when any metric crosses a threshold:

| Signal | Condition |
|---|---|
| `SEC_CVE_ALERT` | ≥1 critical CVE open > 14 days |
| `SEC_FRESHNESS` | freshness < 50% or dropped > 10pp in 30d |
| `SEC_TM_GAP` | threat-model coverage < 60% for security-critical archetypes |
| `SEC_ROTATION` | ≥1 secret past rotation_due |

Pentest burn-down is trended, not alerted — a slow burn-down is a team-culture conversation, not a pager-worthy event.

## Consumers

- `/sec` — computes + displays the snapshot
- `/inbox` — surfaces alerts when thresholds trip
- `/digest` — includes the weekly security snapshot
- `security-officer` — reads this as context for per-feature reviews
- `project-auditor` — reads during `/audit` to shape archetype-specific findings
