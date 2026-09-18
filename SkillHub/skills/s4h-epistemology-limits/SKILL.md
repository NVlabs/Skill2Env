---
name: s4h-epistemology-limits
description: "Identifies what can't be known and why, then clarifies what can be established within those limits and reframes the question into its answerable part. Distinguishes fundamental limits (Gödel, underdetermination, observer effects), practical limits (evidence is unavailable, destroyed, or counterfactual), and conceptual limits (the question is malformed). Use when you say 'can this even be known', 'we keep investigating and it doesn't settle', 'is this question actually answerable', 'I need to know X but X might be unknowable', 'we have a hard epistemological limit here', or when investigation has been thorough but the question remains open."
---

# Epistemology: Limits

Some questions resist investigation not because we haven't tried hard enough but because there is a structural limit on what can be established. Confusing "unknown yet" with "unknowable in principle" wastes resources and produces false hope. Confusing "unknowable in principle" with "unknowable at all" is equally wrong — it forecloses what *can* be established within the limit.

This skill classifies the type of limit, identifies what can still be established within it, and reframes the question into the answerable part. The goal is not to conclude "we can't know" — it's to be precise about what kind of knowing is and isn't available here.

---

## Your Process

**Step 1: State What You're Trying to Know**
Write the question as precisely as possible. Then check: has investigation been thorough, or has the question just not been pursued rigorously? If it's the latter, this skill isn't the right one — use investigation tools first.

This skill applies when investigation has been done and the question remains open, or when you can see in advance that investigation won't settle it.

**Framing check:** Confirm the specific question and its epistemic status before continuing. State what you've identified — the actual question being examined and whether investigation has already been attempted — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific question and its investigation status]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Classify the Type of Limit**

### Fundamental Limits
Structural features of the universe or cognition that make certain knowledge impossible regardless of effort or technology:

- **Gödelian limits**: in any sufficiently complex formal system, there are true statements that cannot be proved within the system. Applies to formal domains; often misapplied metaphorically — be careful.
- **Underdetermination**: multiple theories are equally consistent with all available evidence. No amount of additional evidence of the same type can distinguish between them. Example: "which of these two models explains our data?" when both are observationally equivalent.
- **Observer effects**: the act of measurement changes the thing being measured. Strongest in quantum mechanics; appears in social science (observer effect on behavior), markets (prices change when observed), and management (metrics change what they measure).
- **Counterfactual unavailability**: we can't know what would have happened in the counterfactual world — what would have happened if we hadn't acquired that company, if we had launched six months earlier. The counterfactual world didn't occur.

### Practical Limits
The knowledge is in principle available, but the evidence is inaccessible:

- **Evidence destroyed**: records don't exist, memory has faded, the relevant period is over
- **Privacy barriers**: the information exists but can't be accessed
- **Cost**: investigation is possible but prohibitively expensive relative to the value of knowing
- **Speed**: by the time we could know, the decision will have been made
- **Sampling limits**: the relevant population is too small or inaccessible to draw reliable conclusions

### Conceptual Limits
The question is malformed in a way that makes it unanswerable:

- **Category errors**: the question applies a concept to a domain where it doesn't apply ("what does blue smell like?"; "what's the purpose of the universe?")
- **Loaded presuppositions**: the question contains a false assumption that makes it unanswerable as posed ("when did you stop distorting the data?" presupposes you did)
- **Vagueness**: the question is too ambiguous to have a determinate answer — multiple interpretations would get different answers ("is our culture good?")
- **Infinite regress**: answering the question requires answering another of the same form, indefinitely

**Step 3: Identify What Can Still Be Established**
A limit closes off one avenue of knowing but rarely forecloses all of them. For each type of limit, ask:
- What *can* be known, even if not the exact thing sought?
- What proxies or indicators are available?
- What bounds can be placed on the unknown? (Even if you can't know the exact answer, can you establish a range?)
- What related question can be answered that would inform the original?

**Step 4: Reframe the Question**
Translate the original unanswerable question into the best answerable version. This is the key deliverable — not "we can't know," but "here's what we *can* know, and here's why that's the right question to be asking."

Good reframes:
- Narrow the scope: "not 'did this cause X?' but 'what is the probability range consistent with the evidence?'"
- Shift from fact to bound: "not 'what will happen?' but 'what's the worst-case we should plan for?'"
- Shift from cause to correlation: "not 'why do customers churn?' but 'what behaviors correlate with churn?'"
- Shift from certainty to decision-relevance: "not 'is this true?' but 'is this true enough to act on?'"

**Step 5: Assess the Limit's Practical Significance**
Does the limit actually matter for the decision at hand? Sometimes what seems like an important question is irrelevant to the choice being made. "We can't know exactly why churn increased" doesn't matter if any of the plausible explanations point to the same intervention.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Classify the limit, identify what can be established, produce reframed question
  - **Limit type only** — Just classify what kind of limit this is and why
  - **Reframe only** — Assume there's a limit; go straight to the best answerable version
  - **Refine the question** — Sharpen what we're trying to know before starting

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

---

## Output Format

### The Question
[What is being sought — stated precisely]

### Investigation Status
**Has thorough investigation been done?** Yes / No / Partial
**If not:** [What investigation would be worth doing first]

### Limit Classification
**Type:** Fundamental / Practical / Conceptual
**Subtype:** [Underdetermination / Observer effect / Counterfactual / Destroyed evidence / Category error / etc.]
**Why this limit applies here:** [One paragraph explaining why this question runs into this specific limit]

### What Can Still Be Established
- [Knowable thing 1] — [How to establish it]
- [Knowable thing 2] — [How to establish it]
- [Bounds or proxies if direct knowledge is unavailable]

### Reframed Question
**Original:** [The unanswerable question]
**Reframed:** [The best answerable version]
**Why this is the right reframe:** [One sentence]

### Practical Significance
**Does this limit matter for the decision?** Yes / No / Partially
**Assessment:** [One paragraph — if the limit doesn't matter for the decision, say why; if it does, say what that means for how to act]

---

## Notes

Use `epistemology-epistemic-status` when the question is about calibrating confidence across multiple claims, rather than diagnosing a single unknowable. Use `epistemology-justification` when the question is whether a belief is justified, not whether the answer can be found at all. Use `probability` when the limit is practical and the right response is to quantify the remaining uncertainty rather than reframe the question.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Knowledge limits mapped. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-probability-confidence-calibration` — Calibrate confidence to reflect the limits found
  - `/s4h-creativity-assumption-excavator` — Excavate assumptions created or hidden by those limits
  - `/s4h-investigation-counter-hypothesis` — Generate alternatives that the limits may be hiding
  - **Done** — Wrap up and synthesise what we have so far
