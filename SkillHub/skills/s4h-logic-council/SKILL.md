---
name: s4h-logic-council
description: "Run a reasoning problem, argument, plan, or decision through a council of 5 logical reasoning advisors who analyze it from distinct reasoning frameworks, peer-review each other, and synthesize a verdict on whether the reasoning holds. MANDATORY TRIGGERS: 'logic council this', 'run the logic council', 'pressure-test this reasoning', 'is my thinking sound'. STRONG TRIGGERS: any complex argument where the conclusion matters, a plan with non-obvious dependencies, reasoning you've invested in and want stress-tested. Use ethics-council for moral questions, llm-council for general decisions — this council is specifically for testing the soundness of reasoning itself."
---

# Logic Council

A single reviewer catches some flaws in reasoning. A council catches more — because different reasoning frameworks find different failure modes. Formal logic catches invalid inferences. Systems thinking catches missing feedback loops. Bayesian reasoning catches base-rate neglect. First principles reasoning catches assumptions dressed as facts. Adversarial logic catches the strongest counter-argument you haven't faced yet.

Run all five. Let them disagree. The synthesis tells you where your reasoning is load-bearing and where it's hollow.

---

## The Five Reasoning Frameworks

### 1. Formal Logic
Tests deductive structure. Are premises stated? Do they support the conclusion? Are necessary and sufficient conditions correctly identified? Finds: invalid inferences, unstated assumptions doing hidden work, conclusions that overreach their premises, equivocation across terms.

### 2. Systems Thinking
Treats the problem as a system with feedback loops, delays, and emergent properties. Asks: what happens over time? What non-linear effects appear at scale? What second and third-order consequences has the reasoning ignored? Finds: linear thinking applied to non-linear systems, missing feedback loops, unintended consequences, solutions that fix the proximate cause while worsening the root cause.

### 3. Bayesian Reasoning
Evaluates probabilistic claims and evidence. Asks: what are the base rates? How much should this evidence actually update our beliefs? Is confidence calibrated to evidence? Finds: base-rate neglect, overconfidence from anecdote, underweighted prior probability, failure to consider how likely the evidence would be under alternative hypotheses.

### 4. First Principles
Strips away assumptions and rebuilds from fundamentals. Asks: what do we actually know is true, vs what are we taking for granted? Is the problem framed correctly, or has the framing inherited constraints that don't belong? Finds: assumptions treated as facts, inherited framings that foreclose better solutions, analogies stretched past their breaking point.

### 5. Adversarial Logic
Steelmans the strongest counter-argument. Asks: what is the best version of the opposing case? If this reasoning is wrong, what's the most compelling reason it's wrong? Finds: the objections the reasoning hasn't faced, the cases where the conclusion fails, the evidence that would most efficiently falsify it.

**Why these five:** They create genuine tension. Formal logic and Adversarial logic both find flaws, but via different mechanisms. Systems thinking and Bayesian reasoning both deal with uncertainty, but differently. First Principles stands apart from all four — it questions whether the problem is being solved at all.

---

## How a Council Session Works

### Step 1: Frame the Reasoning

State what is being evaluated — an argument, a plan's logic, a reasoning chain, a stated conclusion and its support. Include:
1. The claim or conclusion being made
2. The premises or evidence supporting it
3. Any context needed to evaluate the reasoning

If the subject is vague, ask one clarifying question before proceeding.

**Framing check:** Confirm the argument being examined before continuing. State what you've identified — the specific claim or conclusion and the key premises supporting it — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the argument — the conclusion and its key premises]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different argument than read; incorporate the correction before proceeding

---

### Human Check-in

After framing the question, use the `AskUserQuestion` tool:

- **Question:** "How do you want to run the council?"
- **Header:** "Council scope"
- **Options:**
  - **Full council** — All 5 advisors + peer review + chair synthesis + saved transcript
  - **Chair synthesis only** — Skip advisor outputs, deliver the verdict directly
  - **Strongest objection only** — Skip all advisors and peer review, identify the single most devastating challenge to this reasoning
  - **Adjust the framing** — Revisit the question before convening

Proceed based on their selection.

---

### Step 2: Convene the Council (5 subagents in parallel)

Spawn all 5 framework advisors simultaneously.

**Subagent prompt template:**
```
You are reasoning from the [Framework Name] perspective in a Logic Council.

Your framework: [framework description — core logic, what it finds, what it prioritises]

A Logic Council has been convened on this reasoning:
---
[framed reasoning]
---

Analyze this reasoning from your framework. Where does it hold? Where does it fail? What does your framework specifically find that other approaches might miss?

Be direct and specific. Don't hedge. Lean fully into your framework — the synthesis comes later.

150–300 words. No preamble.
```

---

### Step 3: Peer Review (5 subagents in parallel)

Anonymize responses as A through E. Spawn 5 reviewers, each seeing all five.

Each reviewer answers:
1. Which response identified the most significant flaw in the reasoning? Why?
2. Which response has the biggest blind spot — what is it missing?
3. What do *all* the responses agree on? (High-confidence signal — if five different frameworks find the same problem, it's real.)

---

**Before synthesising:** State what each framework surfaced in one sentence each. Use `AskUserQuestion`:
- **Question:** "Here's what each framework found: [one bullet per framework — e.g. Formal Logic: ..., Systems Thinking: ..., Bayesian Reasoning: ..., First Principles: ..., Adversarial Logic: ...]. Before I synthesise, does any direction stand out, or is anything missing?"
- **Header:** "Synthesis direction"
- **Options:**
  - **Synthesise as planned** — frameworks covered the ground
  - **Weight [direction]** — user will name which thread to emphasise
  - **Add a missing angle** — user will name a dimension not yet covered

### Step 4: Chair Synthesis

One agent synthesizes everything into a verdict:

**LOGIC COUNCIL VERDICT**

1. **Where the frameworks agree** — reasoning failures flagged by multiple frameworks independently. These are the most reliable findings.
2. **Where the frameworks diverge** — disagreements about whether or how the reasoning fails, and why.
3. **The strongest single objection** — the most damaging finding across all five frameworks.
4. **Verdict** — does the reasoning hold? If not, where exactly does it break?
5. **What would make it sound** — the specific changes that would address the council's findings.

**Chair prompt template:**
```
You are the Chair of a Logic Council. Synthesize the work of 5 reasoning-framework advisors and their peer reviews.

The reasoning under examination:
---
[framed reasoning]
---

FRAMEWORK RESPONSES:
[de-anonymized advisor responses]

PEER REVIEWS:
[all 5 peer reviews]

Produce the verdict:

## Where the Frameworks Agree
[Findings multiple frameworks reached independently — high-confidence signals]

## Where the Frameworks Diverge
[Genuine disagreements about the reasoning's validity]

## The Strongest Single Objection
[The most damaging finding; the one that most undermines the reasoning]

## Verdict
[Does this reasoning hold? Where exactly does it break, if so?]

## What Would Make It Sound
[Specific repairs — premises to add, claims to qualify, steps to make explicit]

Be direct. The council's value is telling the person where their reasoning breaks, not reassuring them it's fine.
```

---

### Step 5: Save the Output

Save the full transcript as `logic-council-transcript-[timestamp].md`. Optionally generate an HTML report with the verdict prominent and advisor responses collapsible.

---

## Notes

- **Spawn all five in parallel.** Sequential spawning lets earlier frameworks contaminate later ones.
- **The chair can dissent.** If four frameworks find no flaw but the fifth's objection is devastating, the chair should say so.
- **Agreement across frameworks is the strongest signal.** When five different reasoning approaches all flag the same problem, that problem is real.
- For reasoning that fails the council, consider using `logic-fixer` to produce a corrected version.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Council verdict in. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-logic-fixer` — Act on the council's identified flaws
  - `/s4h-decision-criteria-weighting` — Weight decision criteria using the council's findings
  - `/s4h-ethics-council` — Add adversarial ethical peer review alongside the logical one
  - **Done** — Wrap up and synthesise what we have so far
