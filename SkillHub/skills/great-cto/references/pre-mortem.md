---
name: pre-mortem
description: Pre-mortem template: forward-looking failure analysis BEFORE risky work starts — distinct from ADR (decision), postmortem (past), threat model (adversarial)
when_to_use: Risky changes (large/enterprise + web3/iot-embedded/regulated). Read by architect before finalising ARCH
applies_to:
  - web3
  - iot-embedded
  - regulated
  - fintech
---

# Pre-mortem — Reference

> Forward-looking failure analysis. Run *before* risky work starts — not after something breaks. Distinct from ADR (decision rationale), postmortem (past incident), and threat model (adversarial security).

## When to trigger

architect runs a pre-mortem as part of ARCH when any of these apply:

- `project_size: large` or `enterprise` → always
- `archetype` is `web3`, `iot-embedded`, or `regulated` → always
- `risk: high` is set in PROJECT.md or passed via `/start "..." risk=high`
- Estimated monthly runtime cost > $500 (proxy for "ambitious system")
- CTO flags the feature as "hard to reverse once shipped"

Override: CTO can pass `pre-mortem: skip` in `/start` args or ARCH prompt to suppress for small changes in otherwise-triggered repos.

## File

`docs/pre-mortems/PRE-<slug>.md` — one file per pre-mortem. Slug matches the ARCH doc or feature name.

## Schema

```markdown
# PRE-<slug> — Pre-mortem (<date>)

## Scenario
It's <future-date, ~6 months post-ship>. <Feature> launched on <planned-ship-date>.
It's now considered a failure. What happened?

## Failure modes (brainstorm — at least 5, don't stop at 2 obvious ones)
1. <mode 1 — specific, not "things went wrong">
2. <mode 2>
3. <mode 3>
4. <mode 4>
5. <mode 5>
...

## Ranked by probability × impact
| # | Prob (L/M/H) | Impact (L/M/H) | Score |
|---|--------------|----------------|-------|
| 1 | M | H | 6 |
| 5 | H | H | 9 |
| 2 | M | H | 6 |

(Score: L=1, M=2, H=3, Score = Prob × Impact.)

## Early warning signs (to monitor)
- <signal 1 — specific metric, log pattern, or user complaint>
- <signal 2>

## Mitigations (map to gates)
| Failure mode | Mitigation | Gate |
|--------------|-----------|------|
| #1 <name> | <concrete action> | gate:qa / gate:compliance / gate:ship |
| #5 <name> | <concrete action> | gate:qa |

## Risks added to register
- R-NNN: <risk title> (<prob>, <impact>, source: PRE-<slug> #N)

## Post-ship review (fill after 90 days)
_[To be filled by architect at <ship-date + 90d>]_
- Realized: <which scenarios actually happened>
- Mitigated: <which mitigations worked>
- Missed: <incidents not in the brainstorm — feed brain.md for next pre-mortem>
- New risks discovered: <delta to register>
```

## Brainstorming prompts (for architect)

Surface non-obvious scenarios by asking these in order:

1. **Technical**: What breaks if load is 10× expected? 100×? If the primary database is unreachable for 30 min? If a dependency has an unannounced breaking change?
2. **Integration**: What if the third-party service we depend on has an outage during peak load? A silent API change? A rate-limit tightening?
3. **Data**: What if our schema assumption is wrong (nulls, encodings, time zones)? What if early-customer data is dirty?
4. **Human**: What if the on-call engineer has never seen this system? What if the runbook is out of date?
5. **Compliance / legal**: What if a regulator in a new market requires X we didn't build? What if a data-retention window is wrong?
6. **Adoption**: What if users ignore the happy path and do something we didn't design for? What if power users abuse the feature in ways that degrade it for everyone?

**Stop conditions**: at least 5 scenarios; at least one from each of Technical / Integration / Data; at least one scenario the CTO didn't already bring up.

## Integration

- **architect**: generates PRE-*.md before finalizing ARCH; embeds ranked mitigations into ARCH "Risks" section; adds high-scoring scenarios as R- entries via risk register.
- **security-officer**: when running gate:compliance or gate:security, reads the matching PRE-*.md and verifies that each "mitigation → gate" mapping is actually enforceable at that gate. If a mitigation is marked gate:qa but no test exists, CSO flags it.
- **`/digest` (quarterly)**: for every PRE-*.md with a ship date > 90 days ago and no filled post-ship review, prompts architect to complete it.

## Post-ship review — why it matters

The post-review closes the learning loop. Scenarios that *didn't* happen teach us what pre-mortem signal was noise. Scenarios that happened *and weren't in the brainstorm* get written to `.great_cto/brain.md` as prompts for next pre-mortem ("last time we missed X — look for it now").

## Consumers

- `architect` — writes at ARCH time; updates post-ship review
- `security-officer` — reads for mitigation-to-gate verification
- `/digest` — quarterly review reminder
- Risk register — sink for high-scoring scenarios
- Q-review (v1.0.75) — reviews realized vs predicted failure modes

## Not in scope (deliberately)

- Real-time chaos engineering — pre-mortem is paper exercise, not fault injection
- Security threat modeling — overlap exists but CSO's threat model is adversarial; pre-mortem is neutral
- Replacing postmortems — postmortems stay as incident record; pre-mortem is the anticipation counterpart
