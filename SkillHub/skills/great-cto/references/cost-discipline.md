---
name: cost-discipline
description: Cost as engineering signal: unit economics, $ per request, cost-per-feature attribution, when to refactor for cost vs functionality
when_to_use: Cost-conscious architectures (medium+ projects). Read by architect Cost Model section
applies_to:
  - _default
---

# Cost Discipline — reference

The third axis of engineering health: economics. Reliability says "does it stay up?", delivery says "do we ship?", cost says "can we afford what we just shipped?" Read by `architect` when sizing new features and by anyone responding to a `/cost` or `/inbox` cost alert.

## Why cost is a real engineering signal, not finance's problem

A feature that ships with zero P0s and 99.99% uptime but doubles the monthly cloud bill per 1k users is still a failed feature. The team just won't notice until unit economics break. Cost is a silent SLO — there's no pager when you cross a threshold, so the discipline has to come from the release process itself.

Three fundamental numbers:

1. **Run-rate** — your current steady-state burn in USD/month. This is the number the CFO asks about. Aggregated across services.
2. **Derivative** — how run-rate changes week over week. A stable-but-wrong run-rate is less dangerous than a stable-then-accelerating one.
3. **Cost-per-deploy** — how much infrastructure each feature adds, amortized. Rising cost-per-deploy means features are growing more expensive to ship.

`/cost` computes all three from `.great_cto/cost-history.log`.

## How rows land in cost-history.log

Two sources:

1. **`devops` post-deploy** (automatic) — appends an estimate row from the latest ARCH doc's "Total estimated addition" line:
   ```
   2026-04-21T10:00:00Z | api-gateway | 120 | - | arch-estimate | ARCH-stripe-subs
   ```

2. **Monthly reconcile** (manual, ~15 min) — you pull the actual bill from your cloud console and append or update rows with `source=cloud-console`:
   ```
   2026-05-01T00:00:00Z | api-gateway | - | 148 | cloud-console | monthly-reconcile
   ```

The `-` placeholder in the unused field is intentional — keeps the column grid aligned so grep/awk work.

## Monthly reconcile workflow

Once a month, budget 15 minutes:

1. Open AWS Cost Explorer / GCP Billing / Azure Cost Management (whichever applies)
2. For each service in `.great_cto/PROJECT.md` `## Stack`, read last month's actual cost
3. Append a row per service to `.great_cto/cost-history.log` with `source=cloud-console`
4. Run `/cost 90` — compare actual vs earlier estimates. Drift > 30% is the signal.

If you skip this reconcile, `/cost` still runs on estimates — but you'll never catch the cases where the team consistently estimates 2× under actual.

## Budget and headroom

Set a ceiling in `.great_cto/PROJECT.md`:

```
## Budget
monthly-budget: 2000
budget-alert-threshold: 80
```

When run-rate crosses the threshold, `/inbox` surfaces a warning with a pointer to `/cost`. When it crosses 100%, the warning becomes blocking in spirit — new feature deploys should pause until a budget conversation happens.

The alert threshold is not arbitrary. 80% is chosen so that a single bad MoM mover (say, a new service landing at ~30% of budget) doesn't immediately push you over.

## Anti-patterns to refuse

- **"We'll optimize cost later."** Later never comes. Write the estimate into the ARCH doc at design time; refuse PRs where the estimate is missing for non-trivial services.
- **"The bill is fine, it's been stable for months."** Stable in dollars ≠ stable in unit economics. If users doubled but bill stayed flat, your infra is under-provisioned. If users stayed flat but bill doubled, something leaked.
- **"Reserved instances / committed spend will fix it."** Financial instruments move the cost curve, they don't fix oversized architecture. Buying 3-year reserved on a service that shouldn't exist is worse than paying on-demand.
- **"The team is small, cost doesn't matter yet."** The habits you build at $2k/mo are the habits you have at $200k/mo. Start the reconcile loop at $100/mo.
- **"Let's ignore the top-mover alert, it's a one-off."** `/cost` only flags movers ≥ 30% MoM. If it's a one-off, appending a note explaining that (an ADR or a comment in the cost log header) is a 30-second cost. Ignoring the alert trains the process to ignore real movers later.

## When `/cost` flags a top mover

Workflow:

1. Pull the last ARCH doc that touched the flagged service — is the jump explained?
2. If yes (e.g. new feature intentionally added 2 nodes) → nothing to do, the system is working.
3. If no → open the cloud console and drill into that service's cost breakdown. The usual suspects: misconfigured autoscaler, retention-ignored logs, cross-region egress, an overnight job looping.
4. File a task in `bd` with label `cost-regression`. Don't fix inline — cost bugs without repro steps come back.

## When run-rate crosses budget threshold

Workflow:

1. Open `/cost 90` to see the 90-day curve, not just point-in-time
2. Rank services by absolute dollars, not percentage — you're looking for where the money actually is
3. Ask: for the top 3 services, is the cost justified by the traffic/value they carry? If no, that's the optimization.
4. If the top 3 are justified → the budget is too low. Either raise it via ADR with revenue justification, or cut scope on the next feature to fit.

Raising the budget is a legitimate answer. Silently going over it is not.

## Source artefacts

- `.great_cto/cost-history.log` — append-only cost log (devops + monthly reconcile)
- `.great_cto/deploys.log` — DORA deploy log (drives cost-per-deploy denominator)
- `/cost [days]` — run-rate / cost-per-deploy / WoW / top movers / headroom
- `/inbox` — cheap alerts when run-rate > threshold or a service spikes +30% MoM
- `monthly-budget` / `budget-alert-threshold` in `.great_cto/PROJECT.md` — configuration

## The full health dashboard

With v1.0.90 shipped, great_cto covers the three engineering axes:

| Axis | Command | Question answered |
|---|---|---|
| Delivery | `/digest` (DORA section) | Do we ship often and safely? |
| Reliability | `/burn` | Are we burning SLO budget faster than we should? |
| Cost | `/cost` | Can we afford what we ship? |
| Process | `/inbox` (gate drift alert) | Are our quality gates still real gates? |

One number per axis, all feeding `/inbox` for at-a-glance triage.
