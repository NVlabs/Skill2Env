---
name: s4h
description: "Master orchestration skill. Takes any situation in plain English, identifies the underlying goal, designs a multi-skill reasoning workflow, and executes it sequentially — feeding each skill's output into the next. Use when you say 'help me think through this', 'I need to figure out what to do', 'where do I start', or any time you want structured thinking applied end-to-end rather than routed to a single tool."
---

# Human

The master orchestration skill. You describe your situation and goal. This skill designs a tailored reasoning workflow — an ordered sequence of skills from across all 23 categories — then executes each step in sequence, feeding what each step reveals into the next. The result is compounding clarity, not a single tool's take.

---

## Your Process

### Step 1: Intake

If the user hasn't described their situation, ask:

> What are you trying to achieve? Describe the situation and what a good outcome looks like.

Wait for their response before proceeding. Aim to understand:
- **The goal**: what does success look like?
- **The obstacle**: what's making this hard?
- **The decision point**: what are they about to do, decide, or communicate?

If any of these are unclear after reading their description, ask one targeted follow-up question before designing the plan.

**Framing check:** Confirm the specific situation before continuing. State what you've identified — the goal, the obstacle, and the decision point — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the goal, obstacle, and what they're about to do or decide]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

---

### Step 2: Design the Workflow

Design an ordered sequence of 2–5 skills that together address the goal. Each skill in the sequence should serve a distinct function, and the output of each should meaningfully inform the next.

**Sequence design principles:**

- **Start with framing before analysis.** If the problem framing might be wrong, begin with `assumption-excavator` or `sensory-structured-observation` before applying analytical tools.
- **Generate before evaluating.** If options are needed, put generation skills (`creativity-alternatives`, `decision-option-mapping`, `concept-fan`) before evaluation skills (`decision-criteria-weighting`, `logic-check`, `ethics-check`).
- **Understand people before designing for them.** If the goal involves others' reactions, run `emotional-motivation-mapping` or `communication-audience-modeling` before `communication-objection-mapping` or `ethics-impact-scan`.
- **Validate before committing.** If the goal ends in a decision or action, close with a stress-test skill (`decision-premortem-analysis`, `constraint-hardness-testing`, `logic-fixer`).
- **End with synthesis when the goal is understanding.** For exploratory goals, close with a skill that produces a consolidated view (`systems-leverage-analysis`, `narrative-frame-analysis`, `aesthetic-coherence-check`).

**Common workflow patterns:**

| Goal type | Typical sequence |
|---|---|
| Make a complex decision | assumption-excavator → decision-option-mapping → decision-criteria-weighting → decision-premortem-analysis |
| Solve a stuck problem | assumption-excavator → creativity-lateral-thinking → creativity-alternatives → constraint-hardness-testing |
| Understand a human situation | emotional-motivation-mapping → social-power-mapping → communication-audience-modeling → ethics-empathy-circle |
| Communicate something difficult | communication-audience-modeling → communication-objection-mapping → communication-clarity-audit |
| Evaluate a plan or proposal | logic-check → decision-premortem-analysis → ethics-impact-scan → constraint-hardness-testing |
| Think through a strategy | systems-leverage-analysis → strategy-terrain → strategy-positioning → decision-premortem-analysis |
| Write or reshape something | writing-issues → writing-restructure → writing-tone-alignment → writing-line-editing |
| Understand a system or pattern | systems-feedback-mapping → systems-leverage-analysis → historical-precedent-analysis |

Use these as starting points. Adapt to the specific situation.

**Before narrowing:** Show the full candidate workflow to the user before committing to a sequence. Use `AskUserQuestion`:
- **Question:** "I've drafted a workflow of [N] steps. Before I lock it in, are there any steps you'd flag as especially important, any you'd cut, or any angle I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with this sequence** — the plan looks right
  - **Flag one step** — user will name a step to prioritise or adjust
  - **Add a missing angle** — user will describe a lens or skill not yet included

---

### Step 3: Present the Plan

Show the user the designed workflow before executing. Format it as an ordered list with the rationale for each step and the connection to the next:

```
Here's the plan I'd run for this:

1. **[skill-name]** — [why we start here; what it will surface]
   → feeds into step 2 by [how its output informs the next step]

2. **[skill-name]** — [what it does given step 1's output]
   → feeds into step 3 by [how its output informs the next step]

3. **[skill-name]** — [what it does given steps 1–2's output]
   [last step: what we'll have at the end]
```

Then ask: **"Run this plan, adjust it, or go straight to a specific step?"**

Use `AskUserQuestion` with:
- **Question:** "Ready to run the plan?"
- **Header:** "Direction"
- **Options:**
  - **Run the full plan** — Execute each step in sequence now
  - **Adjust the plan** — Tell me what to change before we start
  - **Skip to step [N]** — Jump directly to a specific step
  - **Just run one skill** — Pick the single most useful tool and run it now

---

### Step 4: Execute — Sequential with Chaining

Run the first skill immediately. After each skill completes, pause and use `AskUserQuestion` to offer the next move before continuing.

**Before each step (after the first), output a brief handoff:**

> **[skill-name] complete.**
> Key finding: [1–2 sentences on what this step revealed and why it matters].

Then use `AskUserQuestion` to present what to do next:

- **Question:** "What's the next move?" (adapt to what was just found — e.g. "We've surfaced 5 assumptions. What now?")
- **Header:** "Next"
- **Options:** (build dynamically — 2–3 logical next skills given what the current step revealed, plus a wrap-up option)
  - Label: `/[skill-name]`, Description: [one sentence on why this fits as a follow-on and what it will produce given the current output]
  - (repeat for each next skill, up to 3)
  - Label: "Wrap up", Description: "Synthesise what we have so far and close out"

**How to select next skill options:**

Pick skills that directly consume the current output. Ask: *given what we just learned, what's the most useful next question to answer?*

| If the current step produced… | Strong next skills |
|---|---|
| Surfaced hidden assumptions | creativity-lateral-thinking, decision-option-mapping, constraint-hardness-testing |
| A list of options | decision-criteria-weighting, probability-scenario-weighting, decision-premortem-analysis |
| A stress-test or failure map | constraint-workaround-mapping, logic-fixer, strategy-positioning |
| A map of stakeholders or motivations | communication-objection-mapping, ethics-empathy-circle, social-incentive-analysis |
| A logic or argument check | logic-fixer, ethics-check, constraint-hardness-testing |
| A systems or leverage map | strategy-positioning, resource-bottleneck-analysis, temporal-horizon-mapping |
| A creative set of directions | decision-criteria-weighting, creativity-plus-minus-interesting, constraint-hardness-testing |
| A communication or framing analysis | writing-argument, narrative-frame-analysis, communication-clarity-audit |

When the user selects a skill, run it on the situation context plus all accumulated output so far. Do not re-explain the situation from scratch — build on what prior steps established.

If the user selects "Wrap up" at any point, jump to Step 5.

---

### Step 5: Synthesize

After all steps complete, output a synthesis section:

**What the full sequence revealed:**
- List 3–5 findings that emerged from the workflow as a whole — insights that no single step showed on its own.

**The key tension or trade-off:**
- Name the central conflict the workflow exposed, if any.

**Recommended next action:**
- One concrete thing to do, decide, or communicate based on everything above.

**What to revisit:**
- If any assumption or finding in the workflow turned out to be load-bearing but uncertain, flag it here.

---

## Notes

- **The goal drives the plan, not the problem type.** The same problem ("I need to decide X") could warrant different workflows depending on whether the goal is speed, thoroughness, buy-in, or ethical grounding.
- **2–3 steps is often better than 5.** A tight two-skill sequence with strong chaining beats a sprawling five-step plan where the connections are thin.
- **Adapt as you go.** If step 2 reveals the situation is fundamentally different from what step 1 assumed, redesign the remaining steps rather than running the original plan on stale premises.
- **The handoff is the skill.** The value of this workflow is what transfers between steps. Never skip the explicit connection from one step to the next.
- **If the user just wants one skill**, use the routing logic from the original human skill — present 3–4 options, let them pick, run it. Not every situation needs orchestration.
