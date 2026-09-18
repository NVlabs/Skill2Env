---
name: s4h-ethics-check
description: "A fast, comprehensive ethics report on any decision, action, or situation — runs all five ethical frameworks in a single pass. Lighter than ethics-council (no peer review, no HTML report), heavier than ethics-impact-scan. Triggers: 'ethics check', 'quick ethics review', 'full ethics report', 'check this ethically', 'run an ethics check', any request for a complete ethical assessment without full council process."
---

# Ethics Check

Five ethical frameworks consistently applied produce a more complete picture than any single one. Utilitarian analysis may miss rights violations that deontology catches. Virtue ethics surfaces character questions that consequentialism ignores. Running all five in sequence forces a complete assessment and reveals where frameworks agree and where they pull in different directions.

---

## Your Process

**Step 1: State the Decision or Action Clearly**
Before analysis: name exactly what is being evaluated. A vague subject produces vague ethics. Include who does what, to whom, under what conditions.

**Framing check:** Confirm the ethical situation before continuing. State the specific decision or action being evaluated and the key parties affected in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the decision or action, who is involved, and who is affected]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Run Each Framework in Sequence**

**Utilitarian** — Net effect on wellbeing across all affected parties. Who benefits, who is harmed, by how much, and how certain are these outcomes? Does the action produce the greatest good for the greatest number? What are the second-order effects?

**Deontological** — Duties and rights. Does this action treat anyone merely as a means to an end? Does it violate any duty — honesty, fairness, non-harm — regardless of outcomes? Are any rights being overridden without adequate justification?

**Virtue Ethics** — Character and integrity. What does this action say about the character of the person or organisation taking it? Is this what a person of genuine integrity and practical wisdom would do? Does it reflect the virtues that matter in this domain?

**Care Ethics** — Relationships and vulnerability. Who is in a relationship of care or dependency here? Does the action honour those relationships? Does it adequately attend to those who are most vulnerable?

**Justice/Fairness** — Distribution and procedure. Is the distribution of benefits and burdens fair? Were affected parties included in the process? Would this decision be defensible behind a veil of ignorance — not knowing which party you would be?

**Before synthesising:** State what each framework surfaced in one sentence each. Use `AskUserQuestion`:
- **Question:** "Here's what each framework found: [one bullet per framework — Utilitarian, Deontological, Virtue Ethics, Care Ethics, Justice/Fairness]. Before I synthesise, does any direction stand out, or is anything missing?"
- **Header:** "Synthesis direction"
- **Options:**
  - **Synthesise as planned** — frameworks covered the ground
  - **Weight a direction** — user will name which framework or value thread to emphasise
  - **Add a missing angle** — user will name a dimension not yet covered

**Step 3: Synthesise**
Where do the frameworks agree? That agreement is strong ethical signal. Where do they conflict? Name the specific values in tension.

**Step 4: Recommend**
Given the synthesis: what should happen, and what conditions or safeguards matter most?

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Framework conflicts only** — Where the five frameworks disagree, not where they agree
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

### Decision or Action
[Clear statement]

### Framework Assessments

**Utilitarian**
[3–5 sentences: net effects, beneficiaries, harms, certainty, second-order effects]

**Deontological**
[3–5 sentences: duties, rights, treatment of persons, inviolable constraints]

**Virtue Ethics**
[3–5 sentences: character revealed, practical wisdom, integrity]

**Care Ethics**
[3–5 sentences: relationships at stake, vulnerability, responsiveness to those who depend on this]

**Justice / Fairness**
[3–5 sentences: distribution of benefits and burdens, procedural fairness, veil of ignorance test]

### Agreement and Conflict Summary
- **Frameworks agree:** [where multiple frameworks converge]
- **Frameworks conflict:** [where they pull in different directions — name the tension]

### Values at Stake
- [The core values in tension or at risk]

### Recommendation
[Clear recommendation with rationale — and any conditions or safeguards that change the assessment]

---

## Notes

Use ethics-council when the situation requires deeper deliberation, peer challenge between frameworks, or a formal report. Use ethics-impact-scan for a lighter first pass. This skill sits between — a complete, fast, single-pass assessment.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Ethics checked. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-ethics-council` — Run adversarial ethical peer review for deeper scrutiny
  - `/s4h-ethics-impact-scan` — Scan for affected parties the check may have missed
  - `/s4h-decision-premortem-analysis` — Stress-test the ethically-checked plan
  - **Done** — Wrap up and synthesise what we have so far
