---
name: s4h-epistemology-knowledge-types
description: "Maps what kind of knowing is actually in play for a claim or question. Distinguishes a priori from a posteriori knowledge; propositional (knowing that) from procedural (knowing how) from acquaintance (knowing of); and knowledge sourced from perception, inference, testimony, intuition, or memory. Use when you say 'what kind of claim is this', 'is this something we can reason our way to or do we need evidence', 'they're treating this as obvious but I don't think it is', 'is this really an empirical question', or when you need to assess what standards of justification apply before testing whether a claim is true."
---

# Epistemology: Knowledge Types

Before you can test whether a claim is justified, you need to know what kind of claim it is — because different kinds of knowing have different justification standards, different failure modes, and different evidentiary requirements. Mixing up knowledge types is a recurring source of bad reasoning: treating empirical claims as if they're matters of pure logic, treating intuitions as if they're perceptions, treating testimony as if it's first-hand knowledge.

This skill classifies the kind of knowing in play, then draws out what that classification implies for how the claim can be established or challenged.

---

## Your Process

**Step 1: Extract the Claim**
State the claim being made as precisely as possible. Strip away rhetorical packaging. What exactly is being asserted?

**Framing check:** Confirm the specific claim before continuing. State what you've identified — the actual claim being analyzed and the context in which it is being made — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific claim and context]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Classify Along the Primary Axis — A Priori vs. A Posteriori**

- **A priori** — can be known through reason alone, independent of experience. True by definition, logical necessity, or mathematical proof. Examples: "all bachelors are unmarried," "2+2=4," "if A>B and B>C then A>C."
  - Test: could this be false if the world were different? If no, it's a priori.
  - Failure mode: confusing definitional truths with empirical claims ("free markets are efficient" can be made a priori by definition, but that makes it empty rather than powerful).

- **A posteriori** — requires experience and evidence. Could be false; the world could have been otherwise. Examples: "water boils at 100°C at sea level," "this product's NPS is 42."
  - Test: would we need to investigate the world to know if it's true? If yes, it's a posteriori.
  - Failure mode: treating empirical claims as if they've been established when they've only been assumed.

**Step 3: Classify the Form of Knowing**

- **Propositional** (knowing *that*) — a fact or state of affairs. "The conversion rate dropped." "Keynes believed X." Most analytical claims are propositional. Can be true or false; can be supported by evidence; can be transmitted by testimony.

- **Procedural** (knowing *how*) — a skill or capacity. "Knowing how to ride a bicycle." "Knowing how to negotiate." Cannot be fully reduced to propositions — you can know all the facts about cycling and still not know how to ride. Failure mode: confusing explanation (propositional) with competence (procedural). Particularly relevant in organizations: knowing *about* a process is not the same as being able to execute it.

- **Acquaintance** (knowing *of*) — direct familiarity through experience. "Knowing Paris." "Knowing what grief feels like." Richer than testimony but harder to transmit. Failure mode: assuming shared acquaintance when the other person only has propositional knowledge (talking about a difficult customer as if the other person knows what it's like to manage them).

**Step 4: Classify the Source**

| Source | What it provides | Key vulnerability |
|--------|-----------------|-------------------|
| Perception | Direct sensory evidence | Observation errors, selection effects, limited perspective |
| Inference | Conclusions drawn from other knowledge | Depends on validity of chain and truth of premises |
| Testimony | Knowledge passed from others | Reliability of the source, transmission errors, motivated reporting |
| Intuition | Fast, pattern-based judgment | Hard to articulate; may encode bias; often reliable in expert domains |
| Memory | Retained past experience | Reconstructive, not reproductive; degrades; subject to post-hoc editing |

**Step 5: Assess the Epistemic Implications**

Given what kind of knowing is in play:
- What evidence is actually relevant to this claim?
- What evidence is irrelevant but being treated as relevant?
- What can this kind of knowing establish — and what does it categorically *not* establish?
- Is the person making the claim aware of the limits of their knowledge type?

**Step 6: Identify the Type Confusion (if any)**

The most common errors:
- **Treating a posteriori claims as if they were a priori** — "obviously," "of course," or "any reasonable person would agree" applied to empirical claims.
- **Treating testimony as if it were perception** — "I heard that..." treated with the same weight as "I saw that..."
- **Treating procedural knowledge as if it were propositional** — assuming that explaining a skill is equivalent to conferring it.
- **Treating intuitions as evidence** — strong feeling that X used as if it were observation of X.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full classification** — Complete all steps with the epistemic implications drawn out
  - **Type and implications only** — Classify quickly and flag what follows, skip full source analysis
  - **Identify the confusion** — Focus on what knowledge-type error is being made, skip full taxonomy
  - **Refine the claim** — Sharpen what we're analyzing before starting

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

---

## Output Format

### The Claim
[Exact claim being analyzed]

### Primary Classification
**A priori / A posteriori:** [Classification + one sentence justification]

### Form of Knowing
**Type:** Propositional / Procedural / Acquaintance
**Notes:** [Why this classification matters here]

### Source Analysis
| Source in Play | Weight Given | Assessment |
|----------------|-------------|------------|
| [Perception / Inference / Testimony / Intuition / Memory] | High / Medium / Low | [Is this appropriate? Any vulnerabilities?] |

### Epistemic Implications
**What this kind of knowing can establish:**
- [Point 1]
- [Point 2]

**What it cannot establish:**
- [Limit 1]
- [Limit 2]

### Type Confusion (if any)
**Confusion identified:** [Specific error]
**Effect on the argument:** [What this means for the claim's validity]

### Upshot
[One clear paragraph: what is the person actually dealing with here, and what follows for how they should reason about or act on this claim?]

---

## Notes

Use `epistemology-justification` when you've classified the knowledge type and now want to test whether the belief is actually justified. Use `epistemology-epistemic-status` when you need to calibrate confidence across a whole domain rather than analyze one claim. Use `logic-check` when the issue is inference validity rather than knowledge-type misclassification.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Knowledge types classified. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-epistemology-epistemic-status` — Assign epistemic status to each knowledge type
  - `/s4h-decision-criteria-weighting` — Weight decision criteria by the type and reliability of knowledge
  - `/s4h-investigation-evidence-audit` — Audit evidence quality for each knowledge type
  - **Done** — Wrap up and synthesise what we have so far
