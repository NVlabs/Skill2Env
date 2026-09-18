---
name: onboarding
description: Auto-generated onboarding doc: synthesised from existing artefacts (PROJECT.md, ARCH-*, RFC-*, RUNBOOK-*) — not a hand-written wiki that goes stale
when_to_use: New engineer joining. Read by project-auditor when generating /onboarding
applies_to:
  - _default
---

# Onboarding — Reference

> One artifact, two-hour read, real context. Synthesized from artifacts the project already produces — not a hand-written wiki that goes stale.

## Philosophy

A new engineer shouldn't need 2 weeks of calendar blocking to ramp. The information already exists in brain.md, CODEBASE.md, OWNERSHIP.md, and ADRs — it's just scattered. `docs/onboarding/README.md` **synthesizes** these into a linear read.

Regenerated automatically — no manual drift.

## File

`docs/onboarding/README.md` — single file, auto-regenerated monthly.

## When

- **Generate** (first time): `/audit` creates it if missing and `team-size ≥ 2`
- **Regenerate**: `/digest` rewrites it on the first digest of each month
- **Skip**: `team-size: 1` — solo founder doesn't need onboarding for themselves

## Schema

```markdown
# Onboarding — <project>

> Read this first. Generated <YYYY-MM-DD>. Next regeneration: <YYYY-MM-DD + 30d>.

## What we're building
<1 paragraph synthesized from .great_cto/brain.md "Project" section — essence, not feature list>

## Key architectural decisions
<Top 10 most-referenced ADRs, each as one line:>
- **ADR-003**: Use Postgres for OLTP, ClickHouse for OLAP — <why in 10 words>
- **ADR-012**: Deprecate framework X in favor of Y — <why in 10 words>
- ...

## Where the code lives
<From CODEBASE.md "God nodes" — files with highest downstream import count:>
- `services/api/router.ts` — HTTP entry, 29 downstream imports
- `libs/trading/engine.ts` — core domain logic, 12 imports
- ...

## Who owns what
<From OWNERSHIP.md — per-path team/TL/channel:>
- Backend: @alex / team-core / #eng-core
- Mobile: @kate / team-mobile / #eng-mobile

## What to avoid
<From brain.md "What has failed" section — recurring anti-patterns:>
- Don't import from `legacy/` — being deprecated (ADR-011)
- Don't write raw SQL — use ORM (ADR-003)

## How to ship
- Describe feature → `/start` → 2 approvals → done
- See commands section in [README.md](../../README.md)

## Common tasks (runbooks)
<List of docs/runbooks/*.md if present:>
- Deploy to staging: `docs/runbooks/deploy-staging.md`
- Roll back a release: `docs/runbooks/rollback.md`

## Current focus
<Top 5 open Beads tasks at priority 0 or 1:>
- P0: <title> — <id>
- ...

## People to ping
<From OWNERSHIP.md "Escalation" section or synthesized defaults:>
- Architecture questions: @<TL>
- Security compliance: @<CSO-owner>
- Deploy issues: @<ops-owner>
```

## Data sources

| Section | Source |
|---------|--------|
| What we're building | `.great_cto/brain.md` "Project" synthesis |
| Key architectural decisions | Top-N referenced ADRs in `docs/decisions/DECISION-LOG.md` |
| Where the code lives | `.great_cto/CODEBASE.md` god-nodes (highest inbound-import count) |
| Who owns what | `.great_cto/OWNERSHIP.md` per-path rows |
| What to avoid | `.great_cto/brain.md` "What has failed" / "What slowed down" |
| How to ship | static — refers to project README |
| Common tasks | `ls docs/runbooks/*.md` |
| Current focus | `bd list --priority 0 --priority 1 --status open \| head -5` |
| People to ping | `.great_cto/OWNERSHIP.md` Escalation + TL columns |

## Regeneration rules

- Skip sections whose source file doesn't exist yet (don't fabricate — write placeholder "not yet populated — expect after first ARCH")
- If multiple sources disagree (e.g. ADR says X, brain.md says Y), **flag** the inconsistency in the onboarding file as "⚠ conflict — see Q-review" rather than silently picking one
- Never overwrite hand edits: if the first line is not the auto-generated date marker, skip regeneration and report to CTO

## Integration

- **project-auditor**: responsible for the synthesis quality — reads source files, applies the schema, writes the file. Invoked by `/audit` (first creation) and `/digest` (monthly refresh).
- **`/audit`**: creates the file on first run if `team-size ≥ 2`; advisory finding if source files are missing
- **`/digest` (monthly, first run of each month)**: invokes regeneration; reports "onboarding refreshed" in the digest output

## Consumers

- New engineers (primary audience)
- `/inbox` — shows "Onboarding regenerated <days-ago>d ago" in team section if team-size ≥ 5
- Q-review (v1.0.75) — surfaces inconsistencies flagged during synthesis

## Not in scope (deliberately)

- Tutorial content — onboarding points to runbooks, doesn't replace them
- Video / interactive — file-only, greppable, diffable
- Per-role onboarding (backend vs mobile) — single doc, role-specific runbooks linked from it
