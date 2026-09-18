---
name: phases
description: Phase lifecycle (planning → implementation → review → release): which agents run, which gates apply, which artefacts are required per phase
when_to_use: Phase transitions. Read by architect at /start and SessionStart hook
applies_to:
  - _default
---

# Phases

Projects move through four phases. Each phase changes **what context the SessionStart hook loads** — reducing noise and saving tokens.

## Phase table

| Phase | Loaded | Skipped | Use when |
|---|---|---|---|
| `planning` | PROJECT.md, brain.md, digest-latest | CODEBASE, HANDOFF, QA/CSO, perf | Architecture brainstorm, new feature design |
| `implementation` (default) | PROJECT.md, brain.md, CODEBASE, HANDOFF | digest, QA/CSO reports, perf | Active coding — most sessions |
| `review` | PROJECT.md, HANDOFF, latest QA report, latest CSO report | brain, CODEBASE, digest | Gate:ship review, pre-deploy check |
| `release` | PROJECT.md, HANDOFF, perf-baseline tail | brain, CODEBASE, QA/CSO | Deploy day, canary monitoring |

## Switching phase

CTO says "move to review phase" / "planning phase" / "release phase":

```bash
PHASE=<new>
if grep -q "^phase:" .great_cto/PROJECT.md; then
  sed -i.bak "s/^phase:.*/phase: $PHASE/" .great_cto/PROJECT.md && rm -f .great_cto/PROJECT.md.bak
else
  printf 'phase: %s\n' "$PHASE" >> .great_cto/PROJECT.md
fi
echo "Phase set to: $PHASE. Next SessionStart will load phase-specific context."
```

## Semantics

- Phase is **purely about context loading**. It does NOT change which agents run or what gates trigger.
- Pipeline rules come from `archetype` + `approval-level`, not from `phase`.
- **Default is `implementation`.** If `phase:` is missing from PROJECT.md, the hook falls back to `implementation` behavior. Backward compatible.

### Cache implication

Each phase produces a cache-stable SessionStart prefix. Switching phase in the middle of an active pipeline invalidates the KV-cache for the rest of the run. Switch **between** pipelines (after gate:ship closes, before the next feature starts) — not during one.

## Mental model

Think of `phase:` as a filter on the SessionStart hook output — nothing more. The same pipelines, agents, and gates run regardless of which phase is set. Phase just trims what the model sees on session start so it focuses on what matters *right now*.
