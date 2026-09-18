---
name: gate-health
description: Gate quality monitoring: detect rubber-stamp approvals, gates that always pass, decision-time tracking, rejection-rate analysis
when_to_use: Reviewing engineering process health. Read by /inbox + project-auditor
applies_to:
  - _default
---

# Gate Health — reference

How to tell whether your quality gates are real gates or theater. Read by `architect` when `/inbox` flags rubber-stamping, and by anyone calibrating a gate after a postmortem.

## The problem with gates

A gate that always passes is not a gate — it's a rubber stamp with extra steps. The only way to know whether a gate works is to compare its verdicts against subsequent reality (incidents, bugs found post-deploy). Without that comparison, gates degrade silently:

1. Agent gives PASS on a borderline case (no immediate consequence)
2. Threshold drifts: next borderline case feels "similar to last time"
3. Six months later, gate has implicit threshold 30pp looser than the original spec
4. First incident traces back to something the gate "passed"

`/inbox` makes this drift visible by aggregating pass-rate trends and cross-referencing PM "Agent Verdict Audit" tables.

## Healthy gate calibration

| Pass rate | Meaning | Action |
|---|---|---|
| **70–90%** | Healthy. Gate finds real issues without blocking everything. | None. |
| **> 95%** | Likely rubber-stamping. Either the work is genuinely flawless (rare) or the gate has gone slack. | Audit recent PASS verdicts against subsequent bugs/incidents. |
| **< 50%** | Gate is too strict, or noisy, or the upstream agents are producing low-quality work. | Talk to the upstream agent first. If their work is actually fine, loosen the gate. |
| **Drift +10pp upward while already at >85%** | Strongest "gate stopped working" signal. | 🔴 Re-audit the checklist. Compare to /dora CFR trend — if CFR also rising, the gate is the cause. |

The 70–90% window comes from "real engineering work has 10–30% rework rate." If your gate fails less than 10% of the time, you're not catching real problems.

## Effectiveness — the retroactive check

Pass-rate alone isn't enough. A gate could PASS 80% with the right 20% being legitimate FAILs — or it could PASS 80% by missing all the real bugs. The only honest check is:

> **For every postmortem, did the gates that fired PASS catch the bug they should have?**

Postmortems include an "Agent Verdict Audit" table:

```markdown
## Agent Verdict Audit

| Agent | Verdict | Correct? | Why |
|---|---|---|---|
| Architect (architect) | ARCH_READY | yes | scope was correct |
| QA (qa-engineer) | PASS | no | missed concurrent-write race in test plan |
| Security (security-officer) | PASS | yes | not a security issue |
```

`/inbox` parses these tables across all PMs in the window. If `qa-engineer` shows up as "Correct? = no" 4 times out of 6 audited PMs, effectiveness = 33%, and the agent's checklist is broken — not the agent.

## Anti-patterns to refuse

- **"Make the gate stricter"** — without first checking effectiveness. A 60% pass rate with 100% effectiveness is fine. Don't fix what isn't broken.
- **"Disable the gate, it's noisy"** — noisy gates often mean upstream quality dropped, not that the gate is wrong. Investigate the upstream first.
- **"Auto-approve when CTO is busy"** — defeats the entire purpose. If you need a faster path, reduce the *scope* of the gate (smaller surface area) — never the *application* of it.
- **"Add more gates to be safe"** — every gate has a cost. Two gates checking the same thing don't add safety; they just diffuse responsibility. One sharp gate beats three blunt ones.
- **"Trust the agent, it knows what it's doing"** — the entire point of postmortem audits is that agents drift and you can't tell from the verdict alone. Always audit retroactively.

## When `/inbox` flags rubber-stamping

Workflow:

1. Open the flagged agent's recent PASS verdicts (`grep PASS .great_cto/verdicts/<agent>.log | tail -10`)
2. For each, find the corresponding artefact (QA report, security review, etc.)
3. Spot-check 3 random ones — does the artefact actually justify PASS, or is it formulaic?
4. If formulaic → re-write the agent's checklist with concrete `assert`-style criteria, not vibes
5. If real → check whether the work being reviewed got easier (better senior-dev, smaller PRs). If yes, the high pass rate is genuine; raise the bar.

## When `/inbox` flags low effectiveness

Workflow:

1. Open the PMs where the agent was marked "Correct? = no"
2. Look for the common pattern in the bugs that slipped through
3. Add an explicit check for that pattern to the agent's instructions (in `agents/<agent>.md`)
4. Bump the plugin version and ship — the next pipeline run picks it up via SessionStart sync

## Source artefacts

- `.great_cto/verdicts/*.log` — append-only verdict log (per-agent or per-day format)
- `docs/postmortems/PM-*.md` — must include "Agent Verdict Audit" section for retroactive scoring
- `/inbox` — surfaces gate drift and rubber-stamping signals (fires on >85% + +10pp)
- Manual verdict inspection: `ls -t .great_cto/verdicts/ | head` then read the agent's recent logs
