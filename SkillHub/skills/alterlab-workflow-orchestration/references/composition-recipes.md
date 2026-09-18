# Composition Recipes — Wiring AlterLab Skills into Workflows (P1–P5)

Five worked recipes, one per pattern in SKILL.md. Each gives a copyable
delegation prompt, the subagent mechanism it uses, and the real AlterLab skills
it composes. Orchestration mechanics are verified in
`references/claude-orchestration-primitives.md`. The skills referenced here are
real and present in this suite:

- `alterlab-research-pipeline` — packaged 9-stage research→write→review flow
- `alterlab-deep-research` — multi-agent research / lit-review / fact-check
- `alterlab-citation-verifier` — existence-check citations against scholarly APIs
- `alterlab-paper-reviewer` — 5-reviewer panel (core)
- `alterlab-peer-review` — peer-review skill (writing-tools)

## Table of Contents

- [P1 — Parallel fan-out: batch citation verification](#p1--parallel-fan-out-batch-citation-verification)
- [P2 — Sequential pipeline: custom research→verify→review chain](#p2--sequential-pipeline-custom-researchverifyreview-chain)
- [P3 — Judge panel: independent reviewer subagents](#p3--judge-panel-independent-reviewer-subagents)
- [P4 — Adversarial verification: produce then break](#p4--adversarial-verification-produce-then-break)
- [P5 — Loop until clean: revise→re-review cycle](#p5--loop-until-clean-reviserereview-cycle)
- [Scripting it with the Agent SDK](#scripting-it-with-the-agent-sdk)
- [Anti-patterns](#anti-patterns)

---

## P1 — Parallel fan-out: batch citation verification

**Mechanism**: parallel subagents (one per independent input). **Composes**:
`alterlab-citation-verifier`.

When inputs are independent, dispatch one worker per input so each verbose API
session stays in its own context window, then merge.

```text
I have 4 chapter reference lists (chapter1.bib … chapter4.bib). Verify them in
parallel using separate subagents — each subagent runs the
alterlab-citation-verifier skill over exactly one .bib file and returns only its
per-entry verdict table. When all four finish, merge the tables into one
manuscript-wide report and flag every TF / IH / SH entry across all chapters.
Do not start any chapter's analysis until the inputs are split.
```

Optionally pin the worker as a reusable subagent definition
(`.claude/agents/cite-checker.md`):

```markdown
---
name: cite-checker
description: Existence-checks one bibliography file against scholarly APIs. Use proactively when verifying references in parallel.
tools: Read, Bash, WebFetch, WebSearch
model: inherit
skills:
  - alterlab-citation-verifier
---

Run the alterlab-citation-verifier workflow over the single bibliography file
named in the task. Return ONLY the per-entry verdict table — no preamble.
```

Stop condition: every input has a verdict; merge is a single table. This honors
the docs' rule that parallel research "works best when the research paths don't
depend on each other."

## P2 — Sequential pipeline: custom research→verify→review chain

**Mechanism**: subagent chaining (each stage's summary feeds the next).
**Composes**: `alterlab-deep-research` → `alterlab-citation-verifier` →
`alterlab-peer-review`.

> First check whether `alterlab-research-pipeline` already covers the need — it
> packages research→write→integrity→review→revise. Use this custom chain only
> when the user's flow differs (e.g. they bring their own draft, or want
> verification *between* synthesis and review).

```text
Build a 3-stage pipeline on the topic "micro-credentials in vocational
education", carrying forward only each stage's summary:
1. Use alterlab-deep-research in lit-review mode to produce a thematic synthesis
   + annotated bibliography.
2. Chain that bibliography into alterlab-citation-verifier; existence-check every
   entry and drop or flag anything that is NOT_FOUND.
3. Pass the verified synthesis to alterlab-peer-review for a section-by-section
   critique with a revise/accept recommendation.
Report the three summaries plus a final go/no-go.
```

Each handoff passes only the relevant artifact (synthesis, verdict table,
critique), not the full transcript — subagents start fresh, so the delegation
prompt must carry the needed context.

## P3 — Judge panel: independent reviewer subagents

**Mechanism**: parallel subagents (independent contexts) + a synthesis step.
**Composes**: `alterlab-paper-reviewer` and/or `alterlab-peer-review`.

`alterlab-paper-reviewer` already simulates a 5-reviewer panel **inside one
context**. Use this pattern instead when independence matters — separate agents
that cannot anchor on each other's opinions.

```text
Review manuscript.pdf with an independent panel. Spawn three separate reviewer
subagents, each working from the paper alone with no knowledge of the others:
- Reviewer A: methodology and statistics rigor
- Reviewer B: domain contribution and novelty
- Reviewer C: reproducibility (data/code availability, reporting standards)
Each returns an independent verdict + top-3 issues. Then synthesize a single
editorial decision that explicitly notes where the three agree and disagree.
```

Why independent agents: running all three in one context lets the first opinion
anchor the others. For a panel that should also **debate**, escalate to an agent
team (P4). Keep each reviewer read-only (`tools: Read, Grep, Glob`) so none can
edit the manuscript.

## P4 — Adversarial verification: produce then break

**Mechanism**: a fresh skeptic subagent per claim; or an agent team for sustained
debate. **Composes**: `alterlab-citation-verifier` (claim-faithfulness) +
`alterlab-deep-research` (fact-check mode).

The single highest-value integrity pattern: the producer and the verifier must be
**different agents** so the verifier has no stake in the claim being true.

Subagent form (per-claim skeptic):

```text
Extract the three headline empirical claims from my draft. For EACH claim, spawn
a skeptic subagent whose only job is to disprove it:
- search for disconfirming evidence (alterlab-deep-research fact-check mode), and
- check the cited source actually supports the claim, not just that it exists
  (alterlab-citation-verifier claim-faithfulness).
Report each claim as SURVIVES or BREAKS with the evidence. Treat "real citation"
and "citation supports the claim" as separate questions.
```

Agent-team form (debate), gated behind
`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`:

```text
Create an agent team of 3 teammates to stress-test my draft's central argument.
Each teammate adopts a competing interpretation of the evidence and they talk to
each other to try to disprove each other's reading, like a scientific debate.
Converge on which interpretation the evidence actually supports and write the
consensus (and any unresolved disagreement) to a findings doc.
```

This mirrors the docs' competing-hypotheses example verbatim in structure. Agent
teams cost significantly more tokens — reserve for high-stakes claims.

## P5 — Loop until clean: revise→re-review cycle

**Mechanism**: bounded validator→fix→repeat loop in the main conversation.
**Composes**: `alterlab-paper-reviewer` (or `alterlab-peer-review`), plus the
revision step.

```text
Run a bounded revision loop on draft.md:
1. alterlab-paper-reviewer produces reviewer comments.
2. Revise the draft to address every actionable comment.
3. Re-review ONLY the previously-flagged items (verification pass).
4. Repeat from step 2 until there are zero unresolved comments OR after at most
   3 rounds.
Then stop and report: rounds taken, comments resolved, and any residual issues
you could not fix. Do not loop indefinitely.
```

Two non-negotiables: an explicit **success gate** (zero unresolved comments) AND a
**max-iteration cap** (3 rounds). Open loops burn context and tokens. The same
shape works for verify→fix→re-verify until a bibliography is 100% resolvable.

## Scripting it with the Agent SDK

To run P1/P3 in CI or a batch job, the Python Agent SDK (`claude-agent-sdk`,
Python 3.10+) expresses the same delegation. `query()` runs the agent loop; the
`agents` option defines the workers; `"Agent"` in `allowed_tools` auto-approves
delegation. (Per-skill skill-loading is configured via your `.claude/` settings,
which the SDK loads by default.)

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

async def main():
    async for message in query(
        prompt=(
            "Review manuscript.pdf with an independent panel: a methodology "
            "reviewer, a domain reviewer, and a reproducibility reviewer, each "
            "working from the paper alone. Then synthesize one editorial decision."
        ),
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Glob", "Grep", "Agent"],
            agents={
                "methodology-reviewer": AgentDefinition(
                    description="Reviews methodology and statistical rigor only.",
                    prompt="Critique methods and statistics. Report a verdict + top-3 issues.",
                    tools=["Read", "Grep", "Glob"],
                ),
                "domain-reviewer": AgentDefinition(
                    description="Reviews domain contribution and novelty only.",
                    prompt="Assess contribution and novelty. Report a verdict + top-3 issues.",
                    tools=["Read", "Grep", "Glob"],
                ),
                "repro-reviewer": AgentDefinition(
                    description="Reviews reproducibility and reporting standards only.",
                    prompt="Check data/code availability and reporting. Report a verdict + top-3 issues.",
                    tools=["Read", "Grep", "Glob"],
                ),
            },
        ),
    ):
        if hasattr(message, "result"):
            print(message.result)

asyncio.run(main())
```

TypeScript is equivalent via `@anthropic-ai/claude-agent-sdk` (`query({ prompt,
options: { allowedTools, agents } })`). Capture `session_id` from the `init`
system message and pass `resume=session_id` to continue a multi-turn pipeline.

## Anti-patterns

- **Rebuilding a packaged skill.** If the user wants research→write→review, use
  `alterlab-research-pipeline`; don't hand-wire the whole chain.
- **Producer = verifier.** Adversarial verification only works when a fresh agent
  checks the claim (P4). Self-checking re-confirms the original bias.
- **Unbounded loops.** Always pair a success gate with a max-iteration cap (P5).
- **Over-parallelizing dependent work.** Parallel fan-out needs independent
  inputs; chained stages must run sequentially.
- **Fat handoffs.** Pass each stage's summary, not the entire transcript —
  subagents start fresh and the delegation prompt is the channel.
- **Reaching for agent teams by default.** They cost significantly more tokens;
  use subagents unless the workers genuinely need to message each other.
