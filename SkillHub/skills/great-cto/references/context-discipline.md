# Context discipline — keep the working window sharp

> Source: community Claude Code best-practice (Boris Cherny / Dex / Thariq) + Anthropic
> long-context guidance. Loaded by `coordinator` (and any agent running long/parallel work).

Model intelligence degrades as the context fills — long before the hard limit. great_cto
already isolates via subagents; this codifies *when* and *how* to protect the window so
long runs don't quietly get dumber.

## The budget

- **Dumb zone ≈ 40%.** Quality starts slipping past ~40% of the window; experienced
  operators keep sensitive work under ~30%. Treat 40% as a soft ceiling, not the limit.
- **Rot threshold ≈ 300–400k tokens** even on a 1M-token model — don't drift past it for
  work that must be correct (architecture, migrations, security review).

## Rules for agents & the coordinator

1. **Isolate reads in subagents.** File reads, greps, broad codebase sweeps, and dead-end
   exploration go to a child agent — only the *conclusion* returns to the parent. This is the
   single biggest lever; great_cto's `Explore`/subagent pattern exists for exactly this.
2. **Compact with intent, not on autopilot.** Prefer `/compact <hint>` (name what to keep —
   the task, the decision, the open gate) over silent auto-compaction, which discards
   unpredictably. Write a "summarize from here" handoff note before compacting.
3. **Rewind over correct.** When an attempt goes wrong, `/rewind` (or double-Esc) to the last
   good point instead of pouring corrections into the window — corrections cost context and
   leave the failed path as noise.
4. **New task → new session.** Genuinely new work gets a fresh session; only truly related
   work should reuse context. Long-running great_cto pipelines persist state in
   `ARCH-{slug}.md` / `HANDOFF.md` / Beads, so a fresh session re-grounds cheaply.
5. **Scale the window to the task.** Trivial changes don't need the full pipeline loaded
   (mirrors the triage gate); don't pull the whole archetype pack for a one-line fix.

## So-what

A coordinator that respects this dispatches reads to subagents, compacts deliberately, and
re-grounds from artifacts — instead of running a single ever-growing window into the dumb
zone. Pairs with `phases.md` (what to load per phase) and the three-state completion contract.
