---
name: risk-register
description: Active risk register: forward-looking architectural/operational/security risks (not tasks, not postmortems), severity × likelihood × mitigation
when_to_use: Risk tracking. Read by architect at ARCH time + security-officer at audit time
applies_to:
  - _default
---

# Risk Register — Reference

> **Single active reference** for architectural, operational, and security risks. Not a backlog (tasks have done-state; risks don't). Not a postmortem (risks are *forward-looking*).

## File: `docs/risks/RISK-REGISTER.md`

Single file. Append new risks; modify existing (status, mitigation). When a risk is closed, move its entry to `docs/risks/closed/R-<id>.md` with a closing reason — **never delete from the register without archiving**.

## Schema

```markdown
# Risk Register

> Active architectural, operational, and security risks.
> Updated by agents (architect, security-officer, /digest) and CTO.
> Closed risks move to `docs/risks/closed/`.

## Scoring
- **Probability** (over 6 months): L (<10%) / M (10–50%) / H (>50%)
- **Impact**: L (minor/recoverable) / M (feature degraded or revenue at risk) / H (revenue/data loss, reputation, legal)
- **Priority** = sort by Impact desc, then Probability desc. H×H first, H×M next, M×M, etc.

## Active risks

| ID | Title | Prob | Impact | Mitigation | Owner | Status | Source | Added |
|----|-------|------|--------|------------|-------|--------|--------|-------|
| R-001 | Example: Stripe rate-limit on Black Friday | M | H | Queue + exponential retry in payment service | @alex | mitigating | ARCH-stripe-subs | 2026-03-15 |
```

## ID scheme

`R-<zero-padded-3-digit>`. Next ID = max existing + 1. Agents compute via:
```bash
NEXT_ID=$(grep -oE "^\| R-[0-9]+" docs/risks/RISK-REGISTER.md 2>/dev/null | awk -F- '{print $2}' | sort -n | tail -1)
NEXT_ID=$(printf "R-%03d" $((${NEXT_ID:-0} + 1)))
```

## Sources — who writes which risks

| Trigger | Who writes | Source tag |
|---------|------------|------------|
| Architect "Risks" section in ARCH | architect | `ARCH-<slug>` |
| Security-officer finds CVE pattern (3rd similar in 90d) | security-officer | `CSO-<id>` |
| Pre-mortem scenario not fully mitigated | architect | `PRE-<slug>` |
| INCIDENT-LOG recurring cause (same cause 3× in 30d) | `/digest` | `INC-LOG recurring` |
| Deprecation calendar EOL < 6mo and status != migrating | `/audit` | `DEPRECATION-<slug>` |
| CTO manual: "add risk: ..." in chat | manual edit | `manual` |

## Lifecycle

1. **Added** — always visible in register
2. **analysis** → mitigation being planned (ADR / RFC / task)
3. **planned** → owner + ETA set, waiting start
4. **mitigating** → work in progress
5. **accepted** → CTO-accepted residual risk (requires waiver reference)
6. **closed** → moved to `docs/risks/closed/R-<id>.md`

## Dedup rules

- Title + source duplicate → skip (don't create)
- Same cause, different wording → keyword-match on title (no LLM call); `/digest` quarterly does manual review
- Ambiguous → create new R- with `status: duplicate-candidate` for human review

## Stale detection

Entry with `added >180 days ago` and no status updates in last 90 days → `/digest` outputs `STALE RISK: review R-XXX (240d unchanged)`.

## Consumers

- `/inbox` shows top 5 by priority (H×H → M×M)
- `/audit` prepends active-risks summary
- `/digest` quarterly counts H×H risks as board-report input
- architect reads active risks before drafting new ARCH
- pre-mortem uses register as "known risks — brainstorm NEW failure modes"
