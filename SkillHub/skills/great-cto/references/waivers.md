---
name: waivers
description: Waiver protocol: silent gate-skips become tracked debt with explicit time-boxed WAIVER-<id>.md + follow-up task — no silent bypass
when_to_use: Hotfix shipping with skipped gates. Read by security-officer + architect
applies_to:
  - _default
---

# Waivers — Reference

> **Silent skip becomes tracked debt.** When CTO says "skip security gate for this hotfix," the agent refuses to proceed silently — it demands an explicit, time-boxed WAIVER artifact with a follow-up task.

## File: `docs/waivers/WAIVER-<id>.md` (one file per waiver)

Per-waiver files make the audit trail clean: each waiver is its own append-only timeline. When a waiver is resolved (follow-up task closed), the file moves to `docs/waivers/closed/`.

## Schema

```markdown
# WAIVER-042 — Skip gate:compliance for P0 hotfix

**Approved by:** CTO
**Approved at:** 2026-04-18T15:30Z
**Expires:** 2026-05-01 (14 days)
**Gate(s) skipped:** gate:compliance
**Reason:** P0 hotfix for payment failure, needs ship in 30 min
**Waiver type:** emergency | hotfix | planned-debt | dependency-external
**Follow-up task:** SEC-AUDIT-042 (Beads task, priority 1, linked)

**Verification** — CTO confirmation observed in session:
> "skip security this time, we'll audit after ship"
> — CTO, 2026-04-18T15:29Z

---

**Status updates (append-only)**:
- 2026-04-18T15:30Z | created — CTO approval in chat
- 2026-04-19T10:00Z | SEC-AUDIT-042 started
```

## ID scheme

`WAIVER-<zero-padded-3-digit>`. Next ID = max existing + 1. Same pattern as RISK-REGISTER.

## Enforcement rules

### When an agent detects "skip gate X" intent

1. Agent asks CTO **explicitly**:
   ```
   You requested to skip gate:X. To proceed, I need a WAIVER artifact.
   Reason for skip (required): ______
   Follow-up action (required): what will address this after we ship?
   Expiry (max 14 days, or 48h for emergency): ______
   ```
2. If CTO replies with all 3 → agent creates `docs/waivers/WAIVER-XXX.md`, creates Beads follow-up task, proceeds with gate skip.
3. If CTO refuses to provide reason/follow-up → agent refuses to skip.

### Emergency sub-type

Short-form: `waiver type: emergency`, max 48h expiry, required incident link:
```
**Incident link:** INCIDENT-LOG entry 2026-04-18T14:22Z
```

Everything else stays the same.

## Expiry handling

- `expires` field is authoritative
- `/digest` scans `docs/waivers/*.md`, compares `expires` to now
- Expired waiver with open follow-up → surfaces in `/inbox` as:
  ```
  ⚠ WAIVER-042 EXPIRED — follow-up SEC-AUDIT-042 still open (14d overdue)
  ```
- CTO options: close follow-up task → auto-moves waiver to closed/; OR extend expiry (creates new status line, not new file)

## Closure

Waiver closes when **follow-up task** closes (Beads `bd show` shows closed). `/digest` moves file:
```bash
mv docs/waivers/WAIVER-042.md docs/waivers/closed/WAIVER-042.md
```

## Repeat-waiver pattern detection

Same gate skipped 3+ times in 90 days → `/digest` quarterly flags:
```
PATTERN: gate:compliance skipped 4× in last 90d (WAIVER-038, 042, 051, 057)
→ Consider process change: are compliance checks too slow? too brittle?
```

This feeds into Q-review (v1.0.75) as a "process debt" signal.

## Audit trail

- All waivers (active + closed) stay in git history
- Closed waivers include final resolution note at bottom:
  ```
  **Resolved**: SEC-AUDIT-042 closed 2026-04-29. No findings.
  ```

## Consumers

- `security-officer` — enforces waiver for gate:compliance skip
- `devops` — enforces for gate:ship skip
- `/inbox` — shows active + expired
- `/digest` — expired detection + pattern analysis
- Q-review (v1.0.75) — process-debt signal from repeat patterns
