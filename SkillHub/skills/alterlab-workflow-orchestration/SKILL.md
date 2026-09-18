---
name: alterlab-workflow-orchestration
description: "Composes existing AlterLab skills into multi-agent agentic workflows using current Claude Code subagent and Claude Agent SDK orchestration patterns: parallel subagent fan-out, sequential pipelines, judge panels, adversarial verification, and loop-until-clean review cycles. Maps each pattern onto real skills (alterlab-research-pipeline, alterlab-deep-research, alterlab-citation-verifier, alterlab-paper-reviewer, alterlab-peer-review) with copyable delegation prompts, agent-definition frontmatter, and SDK query() snippets. Use when the request mentions multi-agent, subagents, agent team, parallel agents, orchestration, pipeline of skills, judge panel, adversarial verification, devil's advocate, loop until clean, chaining skills, dispatching agents, or composing skills into a workflow. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Write Edit Bash
compatibility: Patterns grounded in Claude Code subagents + Claude Agent SDK (verified against code.claude.com docs, 2026-06-08); uses built-in Claude tools only; agent teams and fork mode are gated behind experimental env vars noted inline; no external API key required for the Claude Code patterns
metadata:
  skill-author: AlterLab
  version: "1.0.0"
  last_updated: "2026-06-08"
  depends_on: "alterlab-research-pipeline, alterlab-deep-research, alterlab-citation-verifier, alterlab-paper-reviewer, alterlab-peer-review"
---

# Workflow Orchestration — Compose AlterLab Skills into Multi-Agent Workflows

This skill is the orchestration layer. It does not do research, write, or review
itself — it teaches **how to wire the skills that do** into agentic workflows
using Claude Code's native subagent machinery and the Claude Agent SDK. Pick a
pattern, point it at real AlterLab skills, copy the delegation prompt.

The five patterns below are the high-leverage shapes for academic work: fan-out
**parallel** investigation, a **sequential** pipeline, a **judge panel**,
**adversarial verification**, and a **loop-until-clean** review cycle. Each is
grounded in the current docs (see `references/claude-orchestration-primitives.md`
for the verified primitives, and `references/composition-recipes.md` for full
worked recipes with copyable prompts).

## When to Use This Skill

Use this skill when the user wants to:

- Run several AlterLab skills **at once** over independent inputs (e.g. verify 4
  bibliographies, or research 3 sub-questions in parallel) and merge the results
- **Chain** skills into a pipeline where each stage hands off to the next
- Get **multiple independent perspectives** on one artifact (a judge / reviewer panel)
- **Adversarially verify** an output — one agent produces, a fresh agent tries to break it
- Iterate a **loop until a quality gate passes** (e.g. re-review until zero unresolved comments)
- Understand Claude Code subagents, agent teams, forks, or the Agent SDK well
  enough to author their own academic orchestration

### Does NOT Trigger

| Scenario | Use Instead |
|----------|-------------|
| The user wants the full research→write→review pipeline run for them | `alterlab-research-pipeline` (it already orchestrates the 9-stage flow) |
| The user wants original research / a cited report | `alterlab-deep-research` |
| The user wants one manuscript peer-reviewed | `alterlab-paper-reviewer` or `alterlab-peer-review` |
| The user wants citations existence-checked | `alterlab-citation-verifier` |
| The user asks about Claude API pricing / model ids / SDK billing | the `claude-api` skill |

This skill is for **how to compose**; the named skills are **what to compose**.
If a single existing skill already does the job end to end, defer to it.

## Verified Orchestration Primitives (Claude Code + Agent SDK)

All claims below are verified against `code.claude.com/docs` on 2026-06-08. See
`references/claude-orchestration-primitives.md` for quotes and field tables.

- **Subagents** are Markdown + YAML files in `.claude/agents/` (project) or
  `~/.claude/agents/` (user). Only `name` and `description` are required;
  optional fields include `tools`, `disallowedTools`, `model`
  (`sonnet`/`opus`/`haiku`/full id/`inherit`), `permissionMode`, `skills`, and
  `background`. Each subagent runs in its **own context window** and returns only
  a summary to the main conversation. Claude auto-delegates by matching the task
  to the subagent's `description`.
- **Subagents cannot spawn other subagents** (no nesting). For nested delegation,
  chain from the main conversation or use Skills. Built-in subagents: **Explore**
  (read-only, Haiku), **Plan** (read-only), **general-purpose** (all tools).
- **Parallel fan-out**: ask the main agent to run independent investigations "in
  parallel using separate subagents"; results return and the main agent
  synthesizes. **Chaining**: ask it to use subagent A, then pass results to
  subagent B.
- **Background vs foreground**: background subagents run concurrently and
  auto-deny prompts; foreground blocks and passes prompts through.
- **Agent teams** (experimental, `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`,
  v2.1.32+) differ from subagents: teammates have independent contexts, a shared
  task list, and **message each other directly** — ideal for adversarial debate.
  Recommended size 3–5; higher token cost.
- **Forks** (`/fork`, `CLAUDE_CODE_FORK_SUBAGENT=1`, v2.1.117+): a subagent that
  inherits the full conversation instead of starting fresh — cheap because it
  reuses the parent prompt cache.
- **Claude Agent SDK** (Python `claude-agent-sdk`, TypeScript
  `@anthropic-ai/claude-agent-sdk`) packages the same agent loop programmatically
  via `query(...)` with `ClaudeAgentOptions`/`options`; define subagents through
  the `agents` option (`AgentDefinition`), and capture/resume `session_id` for
  multi-turn state. Use it to script the patterns below in CI or batch jobs.

## The Five Patterns

### 1. Parallel fan-out (map)

When N inputs are independent, dispatch one worker per input and merge. Classic
academic uses: verify several bibliographies at once, or research distinct
sub-questions concurrently.

```text
I have 4 reference lists (one per chapter). Verify them in parallel using
separate subagents — each subagent runs the alterlab-citation-verifier skill
on one list — then merge the per-entry verdicts into one table flagging every
TF/IH/SH problem across all four chapters.
```

Why subagents: each verification floods context with API lookups you won't reuse;
isolating each in its own window keeps the main conversation clean. Best when
paths don't depend on each other (the docs' stated condition for parallel
research). See recipe P1 in `references/composition-recipes.md`.

### 2. Sequential pipeline (chain)

Stage outputs feed the next stage. The canonical academic chain — research →
write → integrity-check → review → revise — is already packaged as
`alterlab-research-pipeline`; **prefer that skill** rather than rebuilding it.
Use this pattern when you need a *custom* chain it doesn't cover, e.g.
deep-research → citation-verifier → peer-review on an externally supplied draft.

```text
Use the alterlab-deep-research skill to produce a lit-review synthesis on X,
then chain its bibliography into alterlab-citation-verifier to existence-check
every entry, then pass the verified draft to alterlab-peer-review for a
section-by-section critique. Carry forward only each stage's summary.
```

See recipe P2 in `references/composition-recipes.md`.

### 3. Judge panel (independent multi-perspective)

Several independent reviewers each apply a different lens to **one** artifact,
then a synthesizer reconciles. `alterlab-paper-reviewer` already simulates a
5-reviewer panel internally; use *this* pattern when you want the panelists to be
**genuinely separate agents** (separate contexts, no cross-contamination) — e.g.
a methodology reviewer, a domain reviewer, and a reproducibility reviewer that
must not anchor on each other.

```text
Spawn three independent reviewer subagents on this manuscript: one on
methodology, one on domain contribution, one on reproducibility/statistics.
Each works from the paper alone and reports independently; then synthesize a
single editorial decision noting where they agree and disagree.
```

Independence is the point — running them in one context lets the first opinion
anchor the rest. See recipe P3 in `references/composition-recipes.md`.

### 4. Adversarial verification (produce → break)

One agent produces a claim or result; a **fresh** agent is tasked solely with
disproving it. This is the highest-value pattern for research integrity. The
docs' competing-hypotheses agent-team example is the reference implementation:
teammates "talk to each other to try to disprove each other's theories, like a
scientific debate."

```text
Take the three headline claims in my draft. For each, spawn a skeptic subagent
whose only job is to find disconfirming evidence and check the supporting
citation actually supports the claim (via alterlab-citation-verifier). Report
any claim that survives and any that breaks.
```

For sustained debate where the skeptics challenge **each other**, escalate to an
agent team (the env var above). See recipe P4 in `references/composition-recipes.md`.

### 5. Loop until clean (validator → fix → repeat)

Iterate a fix-and-recheck cycle until a quality gate passes — bounded by a turn
cap so it terminates. Academic use: revise → re-review until zero unresolved
reviewer comments, or verify → fix → re-verify until the bibliography is 100%
resolvable.

```text
Run a revision loop: alterlab-paper-reviewer produces comments; revise the
draft to address them; re-review only the previously-flagged items; repeat
until no unresolved comments remain or after at most 3 rounds, then stop and
report the residual issues.
```

Always set an explicit stop condition AND a max-iteration cap — open loops burn
context and tokens. See recipe P5 in `references/composition-recipes.md`.

## Choosing a Mechanism

| Need | Mechanism | Why |
|------|-----------|-----|
| Isolate verbose output, get a summary back | **Subagent** | Own context window; only summary returns |
| Independent investigations, no cross-talk | **Parallel subagents** | Each explores alone; main agent synthesizes |
| Side task that needs full current context | **Fork** (`/fork`) | Inherits conversation; reuses prompt cache |
| Workers must debate / challenge each other | **Agent team** (experimental) | Shared task list + direct messaging |
| Script the workflow in CI / batch | **Agent SDK** | `query()` + `agents` option, programmatic |
| It's already one packaged flow | **Existing skill** | Don't rebuild `alterlab-research-pipeline` |

Match freedom to fragility: open-ended exploration gets prose prompts; fragile
multi-step sequences get explicit, ordered instructions and a stop condition.

## Resources

- `references/claude-orchestration-primitives.md` — verified Claude Code subagent
  + agent-team + fork + Agent SDK primitives, with field tables and doc-sourced
  quotes (load when you need exact frontmatter fields, env vars, or version gates)
- `references/composition-recipes.md` — five full worked recipes (P1–P5) mapping
  each pattern onto real AlterLab skills, with copyable delegation prompts,
  subagent-definition frontmatter, and a Python Agent SDK `query()` example
  (load when you need a complete, ready-to-run composition)

<!--
AUTHORING CHECKLIST (see CONTRIBUTING.md → Skill Quality Standards):
- name == directory name, lowercase-hyphen, no 'claude'/'anthropic'
- description: third person, leads with what + "Use when", suite label LAST, <=1024 chars (this one ~840)
- body <500 lines; reference files exist and are one level deep
- every factual orchestration claim verified against code.claude.com docs (2026-06-08)
- validate: uv run python scripts/check_spec.py --skill workflow-orchestration && uv run python scripts/audit_skills.py
-->
