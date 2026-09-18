---
name: board-narrative
description: Synthesizer rules for /digest board: connect ships to business outcomes, every sentence traces to a repo file, no marketing fluff
when_to_use: Quarterly board reports via /digest board. Read by digest command
applies_to:
  - _default
---

# Board narrative — Reference

> `/digest board` output needs to connect ships to business outcomes — not just list DORA numbers. The narrative is a **synthesizer, not a writer**: every sentence traces back to a file in the repo.

## Output location

Appends a `## Executive narrative` section to the existing board report file (`docs/board-reports/BOARD-<Y>-Q<N>.md`). Placed before the DORA metrics table, since story leads and numbers support.

## Schema

```markdown
## Executive narrative

### What we shipped (<period>)
- <ARCH slug> — <one-line business outcome>
- <RFC slug> — <one-line business outcome>
- <feature> — <one-line business outcome>

### Why it matters
<1 paragraph connecting the ships above to business outcomes. Two sentences each.
Do not add new claims here — only synthesize from ARCH "Business context" and ADR rationale.>

### Metrics that tell the story
- Deploys: <N> (<delta vs prior period>) — <one-line interpretation>
- Lead time: <p50> (<delta>) — <one-line interpretation>
- MTTR: <Nmin> (<delta>) — <one-line interpretation>

### Risks on the horizon
- R-NNN: <risk title> — <mitigation status>
- R-NNN: ...
- Budget burn: <service> at <%> reliability budget — <planned action>

### Next quarter focus
- <epic or initiative> (<artifact ref>)
- <epic> (<artifact ref>)
- <epic> (<artifact ref>)
```

## Source mapping — every line traces to a file

| Narrative section | Source |
|-------------------|--------|
| What we shipped | `docs/architecture/ARCH-*.md` modified in period; `docs/rfcs/RFC-*.md` merged in period |
| Why it matters | ARCH "Business context" section + referenced ADR rationale |
| Metrics that tell the story | Existing DORA block in `/digest` + trend calc vs prior period |
| Risks on the horizon | Top 3 active risks from `docs/risks/RISK-REGISTER.md` (H×H first, then H×M) + any `EXHAUSTED` row from `.great_cto/slo-budget-current.md` |
| Next quarter focus | Beads tasks tagged `epic:q<N+1>` (`bd list --label epic:q<N+1>`) |

## Synthesizer rules

**Rule 1 — no invention.** If the source file doesn't contain the claim, don't write it. Better to produce a shorter narrative than to hallucinate a business outcome.

**Rule 2 — cite the artifact.** Every bullet in "What we shipped" ends with `(ARCH-<slug>)` or `(RFC-<id>)` so a reader can grep the repo and read the source.

**Rule 3 — numbers with interpretation.** A metric without a one-line interpretation ("↑ 30% vs Q1 — team velocity compounding") is a missed opportunity. Interpretations must come from the delta direction + one plausible hypothesis (look for recent RFCs or ADRs in the same area).

**Rule 4 — first-quarter fallback.** With no prior period for comparison, write "Q1 baseline — trends will show next quarter" rather than fabricate deltas.

**Rule 5 — small-project fallback.** Projects without ARCH docs fall back to top-5 merged PRs by label (`gh pr list --state merged --label feature --limit 5`). The narrative shape stays the same; the source is different.

**Rule 6 — zero-risk honesty.** Empty RISK-REGISTER → "No material risks identified this quarter" (a good signal, not a suspicious one).

## Integration

- `/digest board` extends its existing output. No new command.
- Appended to the same `docs/board-reports/BOARD-<Y>-Q<N>.md` file; DORA table stays intact below the narrative.
- If narrative generation fails mid-assembly, the board report still produces the existing DORA output — narrative section is advisory, not blocking.

## Consumers

- CEO / board (primary audience)
- CTO (skims before sending to board)
- Risk register — narrative points back to R- entries; verifying their accuracy is a good pre-send check

## Not in scope (deliberately)

- Freeform "state of the company" narrative — that's the CEO's job, not the engineering report's
- Financial projections — stays in the finance function
- Team-level KPIs — per-team rollups stay in OWNERSHIP-driven reporting
