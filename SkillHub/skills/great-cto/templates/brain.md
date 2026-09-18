# Project Brain — {project}
> 4-tier memory. SEMANTIC + PROCEDURAL are stable and injected into every agent.
> WORKING + EPISODIC are volatile and replaced each session.
> Updated by /digest, /save, and continuous-learner.

---

## SEMANTIC — Stable Facts
<!-- Promoted when a fact appears in 2+ sessions or is explicitly decided.
     These survive compaction. Do NOT replace — only append or correct. -->

### Architecture
<!-- Stack, key design decisions, why we chose X over Y -->

### Tech Choices
<!-- Language, frameworks, tooling — with rationale -->

### Constraints
<!-- Non-negotiables: perf budgets, zero-dep requirements, privacy policy -->

---

## PROCEDURAL — Repeating Workflows
<!-- Promoted when a workflow recurs 2+ times.
     These survive compaction. Each entry is a named, reusable procedure. -->

### Release procedure
<!-- How we publish: test → build → npm publish → tag → cache install -->

### Debug procedure
<!-- How to debug failing hooks, test failures, plugin install issues -->

---

## EPISODIC — Recent Sessions (last 5)
<!-- Rolling window. Oldest entry drops when 6th session is added.
     Summarised automatically by /save. -->

<!-- Add entries above this line in format:
### YYYY-MM-DD — {slug}
{1-2 sentence outcome summary}
Key decisions: {brief}
-->

---

## WORKING — Current Session
<!-- Replaced at the start of each session by SessionStart hook.
     Contains: active task, current focus, immediate blockers. -->

Active task: —
Current focus: —
Blockers: —
