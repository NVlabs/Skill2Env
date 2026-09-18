---
name: quarterly-review
description: Quarterly architecture review: step-back synthesis across ADRs/debt/god-nodes/drift — not the weekly /digest, the strategic ritual
when_to_use: Quarterly review cadence. Read by /digest Q[1-4] and architect
applies_to:
  - _default
---

# Quarterly architecture review — Reference

> Weekly `/digest` updates brain.md continuously. But there's no **step-back ritual**: which ADRs conflict, what debt has lived > 90 days, where did we drift from plan, how did god-nodes evolve. Q-review is that ritual — synthesizer across every artifact the v1.0.71–v1.0.74 releases produce.

## Output location

`docs/architecture/ARCH-REVIEW-<YEAR>-Q<N>.md` — one file per quarter, generated **in draft status**. CTO reviews and edits before treating as final. The draft marker (first line: `> Draft — generated <date> — CTO review required`) is removed when the CTO finalizes.

## Trigger

- **Scheduled**: 1st of Jan / Apr / Jul / Oct at 10:00 local — registered in scheduled-tasks by `/start` for projects with `project_size: medium` or larger
- **Manual**: `/digest Q2 architecture` (explicit quarter) or `/digest architecture` (current quarter to date)

## Inputs (consumes every v1.0.71–v1.0.74 artifact)

| Source | What's extracted |
|--------|------------------|
| `docs/decisions/ADR-*.md` | Added / modified / superseded in the quarter; conflicts |
| `docs/rfcs/RFC-*.md` | Posted / accepted / rejected / in progress |
| `.great_cto/brain.md` | Current synthesis; diff vs `.great_cto/brain-Q<N-1>-snapshot.md` |
| `.great_cto/CODEBASE.md` | God-nodes (top-N by inbound imports); delta vs prior quarter |
| `docs/reliability/INCIDENT-LOG.md` | Recurring causes (3+ within 90d) |
| `docs/risks/RISK-REGISTER.md` | Active risks by tier; aging; unassigned |
| `docs/pre-mortems/PRE-*.md` | Post-ship reviews due; realized vs predicted |
| `docs/waivers/WAIVER-*.md` | Unresolved beyond expiry |
| `docs/deprecations/DEPRECATION-CALENDAR.md` | EOLs in the next quarter; untracked migrations |
| `.great_cto/cost-actual.log` (if present) | Services > 20% over estimate |
| Beads `bd list --status open` aged > 90d | Aged tech debt |

## Output structure

```markdown
# Architecture Review — <YEAR>-Q<N>

> Draft — generated <date> — CTO review required

## Decisions Landscape
- ADRs: <added> added, <superseded> superseded, <conflict-count> conflict(s) → action
- RFCs: <posted> posted, <accepted> accepted, <rejected> rejected, <in-progress> in progress

## Drift Analysis
Planned in Q<N-1> retro:
- <item> (<%done>, <blocker if any>)
- ...

Recommendation: <concrete step — update ADR-NNN / re-scope / accept slip>.

## God Nodes Evolution
- `<path>`: <delta> imports (<old> → <new>) — <one-line interpretation>
- New entrant top-10: `<path>` (<N> imports) — <why it appeared> — <recommendation>

## Aged Tech Debt (> 90d open)
- <beads-id> <title> (aged <N>d, severity <M/H>) — <register link if any>
- <count> similar → recommendation: debt-sprint OR waive explicitly

## Active Risks Summary
From RISK-REGISTER:
- <N> H×H risks, <M> H×M, <K> M×M → top-5 tracked, <P> in progress, <Q> unowned → ASSIGN

## Unresolved Waivers
- <WAIVER-id> expired <N>d ago → follow-up <task-id> still <status> — ESCALATE

## Pre-mortem Post-Reviews Due
- <PRE-slug>: <ship-age>d post-launch — has anything from the list realized?

## Reliability Summary (from v1.0.72)
- SLIs at WARN / EXHAUSTED during quarter: <list>
- Stability-plan weeks triggered: <count>
- Recurring incident causes: <top 3>

## Cost Drift (from v1.0.74, if actuals wired)
- Services > 20% over estimate: <list>

## Deprecations on the Horizon
- EOL within <N> quarters: <list>
- Untracked (no migration plan): <list>

## Recommendations for Q<N+1>
1. <concrete action — split / debt-sprint / re-scope>
2. ...
3. ...
```

## Synthesizer rules

**Rule 1 — synthesizer, not writer.** Same principle as board narrative: every line traces to a file in the repo. If the source is absent, the section is absent (not fabricated).

**Rule 2 — draft, not final.** The file always opens with `> Draft — generated ...` marker. CTO removes after review. Subsequent `/digest` runs that would regenerate the same quarter check for the marker and refuse to overwrite a finalized review.

**Rule 3 — snapshot at start of quarter.** First time `/digest` runs in a new quarter, it saves `.great_cto/brain-Q<N>-snapshot.md = cp .great_cto/brain.md`. This enables the "brain.md diff vs 90 days ago" analysis in subsequent Q-reviews.

**Rule 4 — recommendations cite evidence.** Every recommendation in the final section refers back to a source: "Split router.ts — coupling threshold hit (ADR-025 draft + god-nodes delta 25→29)".

**Rule 5 — small-project skip.** Projects with zero ARCH docs, fewer than 5 ADRs, or solo (`team-size: 1`) skip Q-review generation entirely — it's an artifact for structured teams, not for every repo.

**Rule 6 — massive-review summarization.** If > 50 ADRs / RFCs modified in the quarter, summarize by theme rather than listing each one-by-one. Themes detected by `awk`-grouping on first H1/H2 keyword.

## Integration

- `/digest` learns a new flag: `architecture`. Combine with period arg: `/digest Q2 architecture`. Conflict with `board` flag is OK — CTO can request both: `/digest Q2 board architecture` generates both outputs (separate files).
- `/start` registers a scheduled task for `project_size: medium` or larger: `cron 0 10 1 1,4,7,10 * /digest architecture`
- Dream cycle in `/digest` still runs (updates brain.md); Q-review reads brain.md as input, doesn't replace dream cycle

## Consumers

- CTO (primary audience)
- architect (reads recommendations; drafts follow-up ADRs)
- Board narrative — pulls from Q-review for the "Risks on the horizon" section when both run

## Not in scope (deliberately)

- Replacing ADRs — Q-review surfaces conflicts and aged debt; ADR writes remain the work product
- Replacing postmortems — Q-review references incident patterns; individual postmortems still written per-incident
- Auto-executing recommendations — every recommendation stays advisory until CTO converts into Beads tasks or ADRs
