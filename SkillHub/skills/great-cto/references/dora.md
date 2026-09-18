---
name: dora
description: DORA Four Keys reference: deployment frequency, lead time for changes, change failure rate, MTTR — definitions, instrumentation, baseline benchmarks
when_to_use: Setting up DevOps metrics. Read by devops + architect for engineering health signals
applies_to:
  - _default
---

# DORA — reference

Five metrics that, taken together, predict engineering health better than any single dashboard. Read by `architect` and `qa-engineer` whenever Change Failure Rate spikes. The fifth — Deployment Rework Rate — was added to the DORA model in 2024.

## The five numbers

| Metric | Formula in great_cto | 2024 elite threshold |
|---|---|---|
| **Deployment Frequency** | count(`.great_cto/deploys.log` lines in window) / period | multi-daily |
| **Lead Time for Changes** | median(bd `closed_at - created_at`) for tasks labelled `feature` or `release` | < 24 h |
| **Change Failure Rate** | count(`docs/postmortems/PM-*.md` mtime in window) / count(deploys in window) | < 5 % |
| **MTTR** | median(`MTTR:` minutes from PM headers in window) | minutes |
| **Deployment Rework Rate** | count(deploys where `kind ∈ {hotfix, rollback, patch}`) / count(deploys) | < 10 % |

Run: `/dora [period_days]` (default 30).
Weekly snapshot is included automatically in `/digest`.

### Why five, not four

The classic four measure **what went out and how reliably**. They don't distinguish between a deploy that delivers value and a deploy that cleans up yesterday's mess. A team doing ten deploys a week, six of them hotfixes, looks great on DF and MTTR but is actually burning capacity. Rework Rate surfaces that hidden cost — the 2024 DORA report flagged it as the single best predictor of "feels fast but isn't shipping."

In great_cto, `devops` tags each deploy with a `kind` field:

- `feature` — planned value delivery (default)
- `hotfix` — unplanned fix for a production defect (triggered by `hotfix/*` or `fix/*` branches)
- `rollback` — reversion of a prior bad deploy (triggered by revert commits or Checkpoint C decision)
- `patch` — small unplanned fix that isn't a P0/P1 hotfix (e.g. config correction)

Only `feature` deploys count toward "real throughput."

## The Ostrovok pattern (read before acting on a CFR spike)

A team at Ostrovok (booking platform) saw incidents climbing and assumed the cause was code quality. They wrote more tests, slowed down reviews, and saw no improvement. When they finally measured DORA, the data showed Lead Time was 2 weeks — not a quality problem, a **release latency** problem. Long-lived branches were merging stale code that broke under newer assumptions. Automating the release pipeline cut Lead Time to 2 days, and incidents fell on their own.

**Rule for architect and qa-engineer:** when CFR rises, **do not jump to "more tests" or "stricter review."** Look at Lead Time first.

| What you see | Likely cause | Action |
|---|---|---|
| CFR ↑, LT ↑ | Release latency producing stale merges | Automate release pipeline. Don't add gates. |
| CFR ↑, LT stable | Real code-quality regression | Tighten code-review or add specific tests for failing area. |
| CFR ↑, MTTR ↑ | Detection or rollback weakness | Improve observability + automate rollback. |
| CFR stable, MTTR ↑ | Incident response weakness | Improve runbooks and on-call coverage. |

## The loop, not the dashboard

Ostrovok's headline result was **−40 to −80% incidents in one year**. The metrics did not cause that — the loop did:

1. Measure (`/digest`)
2. Identify the bottleneck (one of the four)
3. Automate the bottleneck (not the symptom)
4. Re-measure to confirm

A dashboard nobody acts on is decoration. The CFR signal in `/inbox` exists so the loop fires automatically.

## Gaming the metrics (watch for these in your own team)

Metrics become lies the moment a team optimises for the number instead of the process. The 2024 DORA report lists four common manipulations — `/digest` runs automated guards against the two most detectable ones, but architect should watch for all four:

| Manipulation | What it looks like | How to catch it |
|---|---|---|
| **Empty-deploy inflation** | DF climbs but Rework Rate climbs with it. Team is counting config nudges or CI re-runs as "deploys." | `/digest` guard 1 (DF and Rework both up >10%). Also: spot-check `deploys.log` for same-version duplicates. |
| **Task fragmentation** | Lead Time drops sharply without any process change. Team is splitting one story into five tickets so each closes faster. | Compare median LT to a random sample of PRs: does the code delta actually match the ticket size? |
| **Incident-definition narrowing** | CFR drops >30% in one window with no corresponding LT or MTTR change. Team quietly stopped calling degradations "incidents." | `/digest` guard 2 (CFR drop >30%). Also: compare PM count to support-ticket escalations. |
| **Rework hidden in features** | Rework Rate is suspiciously low but postmortems keep citing "regression of last week's change." Team is bundling hotfixes into the next feature branch. | Grep postmortems for "regression" + check whether the fixing deploy was tagged `feature` vs `hotfix`. |

**The honest posture:** low DF with clean CFR is a better signal than high DF with rising Rework. Don't game your way up the elite ladder — the loop (measure → find bottleneck → automate → re-measure) is what produces the −40 to −80% incident reduction, not the numbers themselves.

## Anti-patterns to refuse

- "We need stricter QA" — only valid if CFR ↑ and LT stable.
- "We need a release freeze" — valid as a short pause, never as a strategy.
- "Engineer X causes most incidents" — DORA is a system metric, not a person metric.
- "Let's not measure CFR because deploys are rare" — that *is* the measurement; low DF is itself the finding.

## Source artefacts

- `.great_cto/deploys.log` — appended by `devops` agent on every production deploy (since v1.0.87; `kind` column added in v1.0.92)
- `docs/postmortems/PM-*.md` — written by `l3-support` on every P0/P1
- `.great_cto/lessons.md` — one-liner crystallized lessons (since v1.0.86)
- `.great_cto/dora-baseline.log` — local trend log, appended on every `/digest` run

If `deploys.log` is empty, `/digest` reports `NO_DATA` and points at the source of truth, rather than fabricating numbers.
