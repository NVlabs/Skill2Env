---
name: burn-rate
description: SLO burn-rate alerting reference: multi-window multi-burn-rate (5min/1h/6h/3d), why point-in-time error-budget checks fail, fast-burn vs slow-burn
when_to_use: Wiring SLO alerts in monitoring. Read by architect at ARCH time + l3-support during incidents
applies_to:
  - _default
---

# SLO Burn Rate — reference

Multi-window multi-burn-rate alerting. Catches budget exhaustion 6+ hours before it happens. Read by `architect` and `devops` when `/burn` fires.

## The problem with point-in-time SLO checks

`slo-budget-current.md` shows you "78% consumed" at the moment you read it. It doesn't tell you whether you arrived there by burning slowly over 25 days (fine, 5 days of headroom left) or by burning fast over the last 6 hours (not fine, you'll exhaust before the day ends). A single point-in-time read can't distinguish recovery from collapse.

Burn rate is the derivative. **Multi-window** burn rate compares the derivative across different time scales so you catch both fast incidents and slow drifts.

## The four numbers

| Window | Threshold | Meaning | Action |
|---|---|---|---|
| **24h** | ≥ 14.4× normal | Fast burn — incident in progress | 🔴 Page on-call. Investigate now. |
| **7d**  | ≥ 6× normal | Sustained elevated burn — silent regression | ⚠ File ticket. Stability work next sprint. |
| **30d** | ≥ 1× normal | Above sustainable rate | ℹ Review at next /digest. |
| **Projected exhaustion** | < remaining_window | Will exhaust before reset | 🔴 Pause feature deploys. |

"Normal" = burning the entire budget evenly over the SLO window. For a 30-day window with 100min budget, normal = 3.3min/day. 14.4× normal = 48min/day burn → exhaust in ~2 days.

These multipliers come from Google SRE: chosen so that pages fire on real incidents (not false positives) and tickets fire on regressions before they become incidents.

## How great_cto computes it

great_cto doesn't have real-time monitoring — by design, the data source is the manual `INCIDENT-LOG.md`. Burn rate is computed from snapshots:

1. `/digest` recomputes `slo-budget-current.md` from the incident log
2. `/digest` appends a snapshot row to `.great_cto/slo-burn-history.log`
3. `/burn` reads the snapshot series, computes deltas across 24h / 7d / 30d windows
4. `/inbox` runs the cheap version of step 3 and surfaces an alert if any service crosses threshold

The finer the cadence of `/digest`, the finer the burn-rate resolution. Default is weekly via scheduled task; running `/digest 1` daily makes 24h burn meaningful.

## Anti-patterns to refuse

- **"Alert when budget is < 10%"** — too late. The budget runs out *during* the alert window.
- **"Increase the budget so we stop alerting"** — the SLO target is a contract, not a knob to silence noise. Either fix the cause or formally lower the SLO via ADR.
- **"Treat every burn alert as a P0"** — only 24h fast-burn fires page severity. 7d and 30d are tickets.
- **"Burn rate is too noisy, disable it"** — a noisy burn alert means the SLO target doesn't match reality. Re-baseline the target or strengthen the system.

## When the alert fires

`architect` workflow on a fast-burn (24h) alert:
1. Open `docs/reliability/INCIDENT-LOG.md` — last 5 entries for the affected service
2. Look for a single dominant cause in the last 24-48h. Usually one bad deploy or one cascading dependency.
3. If found → `l3-support` runs the 4-angle bug-hunt (see `agents/l3-support.md`)
4. If diffuse → it's a real reliability regression. Stop feature deploys, schedule a stability week, write `STABILITY-PLAN-<date>.md`.

`architect` workflow on a slow-burn (7d) alert:
1. No emergency. File a ticket with the snapshot series attached.
2. Investigate during regular planning. Often the root cause is gradual: a slowly degrading dependency, a slowly leaking resource, or aggregate load growth without capacity planning.
3. Resist the urge to "just lower the SLO." That's the symptom, not the fix.

## Source artefacts

- `docs/reliability/SLO.md` — SLO targets per service (manual, owned by architect)
- `docs/reliability/INCIDENT-LOG.md` — append-only incident reality log (written by `l3-support`)
- `.great_cto/slo-budget-current.md` — point-in-time cache, recomputed by `/digest`
- `.great_cto/slo-burn-history.log` — snapshot series, appended by `/digest`, consumed by `/burn`
