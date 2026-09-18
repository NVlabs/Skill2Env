---
name: deprecations
description: Deprecation calendar: explicit lifecycle for sunsetting frameworks/APIs/runtimes/vendors, prevents quarterly firefights from EOL surprises
when_to_use: Stack-introduction time + quarterly review. Read by architect before committing to a stack
applies_to:
  - _default
---

# Deprecation Calendar — Reference

> **Explicit lifecycle** for things we're sunsetting — frameworks, APIs, runtimes, regions, vendors. Without this, deprecation-driven emergencies become quarterly firefights.

## File: `docs/deprecations/DEPRECATION-CALENDAR.md`

Single file. Chronological (earliest EOL first). Completed deprecations archived in the same file under a "Completed" section for institutional memory.

## Schema

```markdown
# Deprecation Calendar

> What we're sunsetting, when, why, how. Updated by architect + security-officer.
> Entries sorted by EOL date ascending.

## Active

| What | EOL date | Replacement | Owner | Status | Linked |
|------|----------|-------------|-------|--------|--------|
| framework X (2.x) | 2026-12-01 | framework Y | @alex | plan ready | ADR-012, R-002 |
| API v1 `/api/v1/*` | 2027-03-01 | API v2 | @kate | migration 40% | RFC-008 |
| node 18 runtime | 2026-06-01 | node 22 | ops | testing | — |
| us-east-1 for jobs | 2026-08-01 | us-west-2 | ops | scheduled | — |

## Completed (last 12 months)

- 2026-02-01 | python 3.9 → 3.12 | migration complete, no regressions
- 2025-11-15 | legacy webhook `/hooks/old` removed | 0 callers last 30d before removal
```

## Status values

- `not-started` — logged, no owner assigned
- `scheduled` — owner + timeline set
- `testing` — replacement under validation
- `migration N%` — in progress with percentage
- `plan ready` — ADR/RFC drafted
- `waiving` — CTO accepted risk (link waiver)
- `done` — moved to Completed section

## Sources — who creates entries

| Trigger | Who | Auto/manual |
|---------|-----|-------------|
| Vendor announces EOL | security-officer (compliance review) or CTO | manual |
| architect at ARCH finds planned-use of deprecated thing | architect | auto-link, not auto-create |
| `/audit` detects dep with no releases > 24 months | `/audit` | auto-suggest entry |
| `/audit` detects runtime/framework major bumped upstream | `/audit` | auto-suggest entry |
| Forced EOL (CVE in abandoned lib, no patch) | security-officer | auto-create with `EOL: ASAP` |

## Auto-link to risks

When a deprecation entry has `EOL < 6 months remaining` AND status is not `migration N%` / `testing` / `done`:
- `/audit` auto-creates RISK-REGISTER entry linking back
- Risk priority defaults to M×H; architect may adjust

## Auto-link to vendors

When the "What" field references an external vendor:
- Cross-reference `docs/vendors/VENDOR-<slug>.md` (from v1.0.73)
- Update vendor's "EOL announced" field in their doc

## Architect warning at ARCH time

Before writing any ARCH doc, architect greps DEPRECATION-CALENDAR for technologies mentioned in the plan:
```bash
for TECH in $STACK; do
  grep -l "$TECH" docs/deprecations/DEPRECATION-CALENDAR.md && \
    echo "⚠ $TECH is deprecated — see DEPRECATION-CALENDAR"
done
```

Output goes into ARCH "Stack considerations" section:
```markdown
## Stack considerations
- ⚠ Proposed use of `framework X` — deprecated, EOL 2026-12-01 (see DEPRECATION-CALENDAR)
  → Recommend: use `framework Y` instead, or document acceptance
```

## Consumers

- architect — consults before writing ARCH, warns in "Stack considerations"
- `/audit` — detects auto-suggestions, quarterly review
- `/inbox` — shows upcoming EOLs (< 90d)
- `/digest` quarterly — EOLs < 90d in next quarter called out
- Q-review (v1.0.75) — deprecation velocity trend
