---
name: s4h-writing-argument
description: "Builds and repairs persuasive arguments by surfacing the warrant, auditing evidence, addressing counterarguments, and identifying rhetorical substitutes. Use when an argument has holes, the case isn't landing, or evidence isn't connecting to the claim. Triggers: 'build an argument', 'argument structure', 'the argument isn't working', 'op-ed', 'persuasive writing', 'make the case for', 'my argument has holes', 'the evidence doesn't land'."
---

# Writing: Argument

Arguments fail not in the evidence but in the warrant — the unstated principle connecting evidence to claim. The warrant is the assumption that makes the argument work. Most writers never surface it, because to them it is obvious. But the reader may be supplying a different warrant — and reaching a different conclusion from the same evidence.

The structure of every argument:
- **Claim:** What you are asserting to be true
- **Evidence:** The facts, data, examples, or observations that support it
- **Warrant:** The principle or assumption that connects the evidence to the claim

Example: "Remote workers are more productive (evidence). Therefore we should adopt a remote work policy (claim)." The warrant — "policies should be adopted when they increase productivity" — sounds obvious but is not. A reader who believes "productivity must be balanced against team cohesion and culture" will not accept the warrant, and the argument fails for them even if the evidence is strong. Making the warrant explicit forces both writer and reader to examine the actual assumption.

The second most common failure: the strongest counterargument is not addressed. An argument that doesn't engage its best objection is not a complete argument — it is a one-sided brief that any reader with reservations can dismiss. Addressing the counterargument, not to concede but to answer it, is what makes an argument persuasive rather than merely insistent.

---

## Your Process

**Step 1: Central Claim**
State the argument's claim in one sentence. Be specific: "We should adopt a four-day work week" is more specific than "Work-life balance matters." The more specific the claim, the more clearly the evidence can be evaluated against it. A claim that can't be stated specifically is often a claim that hasn't been formed yet.

**Framing check:** Confirm the specific argument before continuing. State what you've identified — the actual claim being argued and the context or piece it appears in — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific argument and its context]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different argument than read; incorporate the correction before proceeding

**Step 2: Warrant — State It Explicitly**
What principle or assumption connects the evidence to the claim? State it as a full sentence: "X is true (evidence), and because [warrant], therefore Y (claim)." Test: does the argument work if the reader doesn't share the warrant? If not, the warrant needs to be argued for — not just asserted.

**Step 3: Evidence Audit**
For each piece of evidence:
- Is it sufficient? (Is there enough of it to support the claim, or is it a single data point generalised too broadly?)
- Is it credible? (What is the source? Is it current? Is it directly relevant or analogous?)
- Does it actually support the claim? (Sometimes evidence is relevant to the topic but doesn't logically connect to the specific claim being made)
- Is anecdote being used where data is needed, or data being used where human experience would land harder?

**Step 4: Counterargument**
Identify the strongest objection to the claim — the best case that a reasonable, informed person in disagreement could make. Then assess: is this counterargument addressed in the piece? If it is not addressed, the argument has a hole that every skeptical reader will find. If it is addressed, is it addressed honestly (engaging the best version) or with a strawman (misrepresenting it to make it easy to defeat)?

**Step 5: Rhetorical Substitutes**
Flag appeals that are standing in for reasoning:
- **Appeal to authority:** "Studies show..." without naming which ones; "experts agree..." — which experts? This is not evidence; it is the *claim* that evidence exists.
- **Appeal to emotion:** Emotionally charged language or stories that produce a feeling of agreement without logical support — not wrong to use, but should not substitute for the argument.
- **Repetition as intensification:** Restating the claim more forcefully as if repetition adds proof.

These are not automatically illegitimate — emotion and authority are genuine persuasive tools. The problem is when they *substitute* for reasoning rather than support it.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Specific focus** — Zoom in on one aspect of this analysis
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

---

## Output Format

### Argument Audit

**Central Claim:** [The argument in one sentence]

**Warrant:** [Explicit statement of the connecting principle — acknowledged in the piece / reconstructed if implicit]

**Evidence Quality:**
- [Evidence piece] — Sufficient / Insufficient / Credible / Questionable / Relevant / Tangential
- [Repeat]

**Strongest Counterargument:** [The best objection to the claim] — Addressed / Not addressed / Strawmanned

**Rhetorical Substitutes:**
- [Quoted instance] — Type: [authority / emotion / repetition] — Substituting for: [what reasoning is missing]
- NONE FOUND if clean

**Verdict on Argument Strength:** [Strong / Has specific weaknesses / Weak — with diagnosis]

**Reconstruction at Full Strength:** [The argument rebuilt — claim, warrant made explicit, evidence tightened, counterargument addressed, rhetorical substitutes replaced with reasoning]

---

## Notes

- A reconstructed argument at full strength is the most useful output: it shows the writer what the argument would look like if it were complete. Often the reconstruction reveals that the warrant is actually contestable and needs its own supporting argument.
- The most useful diagnostic question: "Why should I believe that this evidence implies this claim?" The answer is the warrant. If the answer is "isn't it obvious?", the warrant is unstated.
- Pairs with `/s4h-writing-rhetoric` — rhetoric analysis examines how the argument is being made (its framing, its appeals, its assumptions); argument analysis examines whether the argument is sound.
- Pairs with `/s4h-writing-restructure` — many argument problems are structural: the claim comes too late, the counterargument is buried, the warrant appears at the end when it needs to anchor the whole.
- Pairs with `/s4h-writing-audience-calibration` — the warrant that works for one audience may not work for another; calibration includes choosing which assumptions to surface and argue for.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Argument written. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-writing-rhetoric` — Strengthen the argument with rhetorical technique
  - `/s4h-logic-argument-validation` — Validate the argument's logical structure
  - `/s4h-communication-objection-mapping` — Address objections the argument will face
  - **Done** — Wrap up and synthesise what we have so far
