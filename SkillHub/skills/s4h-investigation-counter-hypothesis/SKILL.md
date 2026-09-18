---
name: s4h-investigation-counter-hypothesis
description: "Generates the best alternative explanations for the same observations. Use when you have a claim or explanation and want to know whether something else could explain the evidence just as well — 'could there be another explanation', 'what else could cause this', 'am I sure this isn't something else', 'steel-man the alternative', 'what would a skeptic say', 'rival hypotheses'."
---

# Investigation: Counter-Hypothesis

The confirmation trap is automatic: once we have an explanation, we look for evidence that supports it and stop looking for evidence that would support alternatives. Counter-hypothesis generation is the structural antidote. The process is not to argue against your explanation — it is to seriously generate the best competing explanations and then ask: given all the evidence, which hypothesis should I actually believe? The decisive test — the observation that, if run, would most clearly discriminate between hypotheses — is the product.

---

## Your Process

**Step 1: State the Hypothesis Under Investigation**
Write out the claim or explanation you are currently working with:
- What is being explained? (The observations, pattern, or outcome)
- What does the hypothesis assert is causing, driving, or explaining it?
- What evidence is currently cited in support?

**Framing check:** Confirm the specific hypothesis before continuing. State what you've identified — the claim being tested, what it purports to explain, and what evidence is cited for it — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the hypothesis, the observations it explains, and the key evidence]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Generate Rival Hypotheses**
Generate rival alternative explanations that could account for the same observations using all the strategies below. Then show the complete generated set to the user before narrowing.

**Before narrowing:** Show all generated rivals to the user first. Use `AskUserQuestion`:
- **Question:** "I've identified [N] rival hypotheses. Before I select the most significant 3–5 to develop fully, are there any you'd flag as especially important, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific rival to include
  - **Add a missing one** — user will describe it

Then narrow to 3–5 rivals. Each developed rival hypothesis should:
- Be internally coherent (not obviously impossible)
- Account for at least the core observations
- Be genuinely different — not just the original hypothesis with a small tweak

Strategies for generating rivals:
- **Reverse causation:** Could the direction of causation be inverted? (A causes B vs. B causes A)
- **Common cause:** Could A and B both be caused by a third factor C?
- **Selection bias:** Could the sample or cases you're seeing be unrepresentative in a way that creates an apparent pattern?
- **Measurement artifact:** Could the pattern be an artifact of how data was collected, rather than a real phenomenon?
- **Coincidence / base rates:** Could the observed pattern be expected by chance given the base rates?
- **Confound:** Is a known third variable correlated with the proposed cause?
- **Mechanism change:** Has the mechanism you're assuming actually changed (different era, different population)?
- **Definitional:** Is the effect only visible because of how terms are defined?

Do not construct straw man rivals. Generate the most serious version of each alternative.

**Step 3: Assess Evidence Fit for Each Rival**
For each rival hypothesis:
- What evidence supports it?
- Does it explain the observations as well as the original hypothesis? Better? Worse?
- What would have to be true for this rival to be correct?
- Are there observations that the rival explains but the original does not?

**Step 4: Identify the Discriminating Evidence**
For each pair of hypotheses (original vs. rival), ask: what single observation or piece of evidence would most cleanly rule one out?
- The discriminating evidence is the observation that is:
  - Predicted by one hypothesis
  - Not predicted (or actively contradicted) by the other
  - Feasible to obtain

If you already have this evidence, apply it. If you don't, name what investigation would produce it.

**Step 5: Identify the Decisive Test**
Across all rivals, identify the single test that would do the most work:
- Which test, if run, would most efficiently narrow the field of credible hypotheses?
- Can this test actually be run? If not, is there a feasible proxy?

**Step 6: Rank Current Credibility**
Given all available evidence — including evidence for rivals — how does each hypothesis rank? Do not default to your original hypothesis unless the evidence genuinely favors it.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — All steps: state hypothesis, generate rivals, assess evidence fit, identify discriminating evidence, decisive test, credibility ranking
  - **Generate rivals only** — List alternative explanations with brief evidence fit; skip discriminating evidence analysis
  - **Decisive test focus** — Identify what test would most clearly discriminate between the main hypothesis and the best rival
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

---

## Output Format

### Hypothesis Under Investigation
**Observations to explain:** [What we're trying to account for]
**Current hypothesis:** [The explanation being tested]
**Evidence currently supporting it:** [What is cited in its favor]

### Rival Hypotheses

**Rival 1: [Name/Description]**
- What it claims: [The alternative explanation]
- Evidence that supports it: [What this hypothesis can account for]
- Evidence that challenges it: [What it struggles to explain]
- What would have to be true: [Its key premise]

**Rival 2: [Name/Description]**
[Same structure]

[Repeat for 3-5 rivals]

### Discriminating Evidence

| Hypothesis A | Hypothesis B | Discriminating Evidence | Status |
|---|---|---|---|
| Original | Rival 1 | [Observation that distinguishes them] | [Have it / Need to find it] |
| Original | Rival 2 | [Observation that distinguishes them] | [Have it / Need to find it] |

### Decisive Test
**Test:** [The single investigation that would do the most work]
**What it would show:** [How it discriminates between hypotheses]
**Feasibility:** [Can it be run? If not, what's the best proxy?]

### Current Credibility Ranking
1. **[Hypothesis]** — [Why it currently has most evidential support]
2. **[Hypothesis]** — [Why it's a serious contender]
3. **[Hypothesis]** — [Why it's less credible but not ruled out]

**The live question:** [What remains genuinely uncertain and what evidence would resolve it]

---

## Notes

Counter-hypothesis generation is not devil's advocacy. The goal is not to argue for an alternative but to seriously evaluate whether the evidence discriminates between competing explanations. Use investigation-evidence-audit to evaluate the strength of the evidence cited for the original hypothesis. Use logic-argument-validation to check whether the inference from evidence to hypothesis is valid. Counter-hypothesis is specifically about rival explanations — not about whether the evidence is good, but about whether it uniquely supports one interpretation.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Counter-hypotheses generated. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-investigation-evidence-audit` — Audit evidence for and against each hypothesis
  - `/s4h-probability-scenario-weighting` — Weight competing hypotheses by probability
  - `/s4h-investigation-triangulation` — Triangulate across hypotheses to find what holds
  - **Done** — Wrap up and synthesise what we have so far
