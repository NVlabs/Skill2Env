---
name: s4h-decision-premortem-analysis
description: "Imagines the decision has been made and failed — then diagnoses why. Breaks the commitment bias that prevents honest risk assessment after a direction is chosen. Triggers: 'pre-mortem', 'imagine this failed', 'what could go wrong', 'assume this doesn't work', 'failure mode analysis'."
---

# Decision Premortem Analysis

Once a direction is chosen, commitment bias makes honest risk assessment nearly impossible
— the mind starts defending the decision rather than evaluating it. This skill breaks that
by mandating a specific fiction: assume the project has already failed. Then ask why.
The pessimism is not optional — it is the mechanism.

---

## Your Process

**Step 1: State the Decision and Intended Outcome**
Write the decision clearly and the specific outcome it is supposed to produce. Include
the timeline and the measurable definition of success.

**Framing check:** Confirm the specific decision before continuing. State what you've identified — the actual decision being stress-tested and its intended outcome — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the decision and its intended outcome]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Project to Failure**
Enter the failure frame. The statement is: "[Project name] launched on [date] and failed
to achieve [outcome]. Here is what went wrong." Write this as if reporting a post-mortem,
not brainstorming risks. The past-tense fiction reduces defensive filtering.

**Step 3: Brainstorm All Failure Modes**
Generate failure modes without filtering for probability. Encourage pessimism. For each
failure mode, ask: how would this actually unfold? What would be the first sign? What
would make it worse?

**Step 4: Group Failures by Type**
- **Execution failures**: we had the right model of the world but did it wrong —
  timing, resourcing, coordination, quality.
- **Assumption failures**: we did it right but our model of the world was wrong —
  the market, the users, the technology, the dependencies.
- **Unknown failures**: we didn't anticipate this category of problem at all.

**Step 5: Pre-emptive Action per Top Failure Mode**
**Before narrowing:** Show the complete generated set to the user first. Use `AskUserQuestion`:
- **Question:** "I've identified [N] failure modes. Before I select the most significant by probability × severity, are there any you'd flag as especially important, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific failure mode to include
  - **Add a missing one** — user will describe it

Identify the 3-5 most significant failure modes (highest probability × severity). For
each: what single action, taken now, most reduces the probability or severity of this
failure?

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Top 3 failure modes only** — Highest probability × severity combinations, skip the full inventory
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Decision and intended outcome:**
> [Statement + timeline + measurable success definition]

**Failure modes (all generated):**

| Failure mode | Type (Execution / Assumption / Unknown) | Probability | Severity |
|-------------|----------------------------------------|-------------|----------|
| | | | |
| | | | |

**Top 3-5 failure modes with pre-emptive actions:**

| Failure mode | Why it's significant | Pre-emptive action |
|-------------|---------------------|-------------------|
| | | |
| | | |

**Assumption inventory (things that must be true for this to work):**
> [Bulleted list — these are the highest-leverage unknowns to validate early]

---

## Notes

Assumption failures are the most dangerous category because they are invisible until
something breaks. The pre-mortem's most durable output is often the assumption inventory —
which assumptions, if wrong, would make the entire direction invalid?

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Failure modes mapped. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-constraint-workaround-mapping` — Address the top failure modes with concrete workarounds
  - `/s4h-decision-criteria-weighting` — Revise decision criteria based on failure mode findings
  - `/s4h-strategy-positioning` — Adapt strategy to reduce the probability of the worst failures
  - **Done** — Wrap up and synthesise what we have so far
