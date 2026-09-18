---
name: s4h-logic-fixer
description: "Take broken reasoning — a flawed argument, contradictory spec, unsound plan, or invalid inference — diagnose exactly what's wrong, and produce a corrected version. Use when you have reasoning that doesn't hold and you want it fixed, not just critiqued. TRIGGERS: 'fix this reasoning', 'repair this argument', 'this logic is broken, fix it', 'make this argument sound', 'my reasoning is circular, help', any situation where broken reasoning needs to be made valid rather than just flagged. Pairs with logic-argument-validation (which diagnoses) and logic-council (which pressure-tests) — this skill fixes."
---

# Logic Fixer

Diagnosis without repair is incomplete. This skill takes broken reasoning and produces a corrected version — one where the premises actually support the conclusion, the hidden assumptions are made explicit, the fallacies are removed, and the argument can be defended.

The output is not a critique. It is a fixed version of what you were trying to say.

---

## Your Process

**Step 1: Diagnose before repairing**
Don't jump to a fix. First, be specific about what's broken:
- What type of failure is this? (Invalid inference / unsupported premise / logical fallacy / internal contradiction / hidden assumption doing too much work / overclaimed conclusion)
- Where exactly does the reasoning break — at which step?
- What is the argument *trying* to establish? (Separate the intent from the execution — the intent might be sound even if the argument isn't.)

**Framing check:** Confirm the argument being examined before continuing. State what you've identified — the actual argument being analyzed, the conclusion it is trying to establish, and the apparent failure type — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the argument, its intended conclusion, and what appears broken]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Classify the repair needed**
Different failure modes need different repairs:

| Failure | Repair |
|---|---|
| Unsupported premise | Add evidence, or qualify the premise |
| Overclaimed conclusion | Narrow the conclusion to what the premises actually support |
| Missing step | Make the implicit inference explicit |
| Circular reasoning | Identify the begged question; provide independent support for the conclusion |
| False dichotomy | Reframe to acknowledge the full option space |
| Invalid inference | Add the bridging premise that makes the inference valid |
| Equivocation | Disambiguate the term; use different words for different senses |
| Hidden assumption | Surface it as an explicit premise; assess whether it holds |

**Step 3: Produce the fixed version**
Rewrite the argument so that:
- Every premise is stated explicitly
- Every inference from premise to conclusion is valid
- The conclusion claims no more than the premises support
- Fallacies are removed, not just noted
- Hidden assumptions are surfaced as explicit premises (and labelled as assumptions if they're not established)

**Step 4: Note what changed and why**
Don't just hand over the fixed version without explanation. For each change:
- What was wrong
- What the fix was
- Whether the fix strengthens or narrows the original claim

If the original conclusion cannot be made to hold under any reasonable repair — because the premises are too weak or the claim is simply unsupported — say so directly rather than producing a version that technically avoids fallacies but doesn't actually establish what the author wanted to establish.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Fixed version first** — Show the corrected reasoning before explaining what was wrong
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Original reasoning:**
[The broken argument, spec, or reasoning as provided]

**Diagnosis**
| Issue | Location | Type |
|---|---|---|
| [what's broken] | [where in the argument] | [failure type] |

**Fixed Version**
[The corrected argument — written cleanly, as if it were the original. Not a tracked-changes edit, but a finished version.]

**What Changed**
| Original | Fixed | Why |
|---|---|---|
| [original claim/step] | [fixed version] | [reason] |

**Strength Assessment**
[Is the fixed argument now sound? Does it establish what the original was trying to establish, or did the repairs require narrowing the conclusion? Be honest about this.]

---

## Notes

Sometimes a broken argument can't be fixed because the conclusion isn't supportable — the premises, even repaired, don't get you there. In those cases, the honest output is: "This conclusion cannot be established with the evidence available. Here is what the available evidence *does* support." That is more useful than a technically valid argument for a weaker claim dressed up to look like the original.

The fixer's job is sound reasoning, not salvaging a predetermined conclusion.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Reasoning repaired. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-logic-check` — Verify the fix holds under full scrutiny
  - `/s4h-decision-premortem-analysis` — Stress-test the corrected plan
  - `/s4h-communication-clarity-audit` — Check the corrected reasoning is communicated clearly
  - **Done** — Wrap up and synthesise what we have so far
