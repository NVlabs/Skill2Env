---
name: s4h-investigation-evidence-audit
description: "Evaluates the quality, strength, and completeness of evidence for a claim. Covers evidence type hierarchy, sample quality, methodological soundness, conflicts of interest, and what's notably absent. Use when you want to know how good the evidence is — 'is this evidence strong', 'evaluate the research', 'how solid is this', 'is this just one study', 'what kind of evidence supports this', 'what's missing from the evidence'."
---

# Investigation: Evidence Audit

Evidence is not a binary: there or not there. A study can exist and be worthless. Multiple sources can exist and all be downstream of the same flawed original. The question is never just "is there evidence?" but "what kind, how strong, and what's missing?" A structured evidence audit answers all three. It places the available evidence in a hierarchy, evaluates it against the claim it's supposed to support, flags conflicts of interest, and explicitly names what should exist but doesn't.

---

## Your Process

**Step 1: State the Claim and Evidence Inventory**
Write out the claim you're evaluating. List all evidence currently offered in support — each study, data point, expert opinion, case, or example. Do not filter yet: capture the full inventory.

**Framing check:** Confirm the specific claim and evidence set before continuing. State what you've identified — the precise claim being evaluated and the body of evidence offered in its support — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the claim and its evidence]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Classify by Evidence Type**
Place each piece of evidence on the evidence hierarchy. Higher tiers provide stronger warrant for causal claims:

| Tier | Evidence Type | What It Establishes |
|------|--------------|---------------------|
| 1 | Randomized controlled trial (RCT) | Causal relationship with controlled confounders |
| 2 | Pre-registered observational study | Association with reduced risk of p-hacking |
| 3 | Non-pre-registered observational / cohort study | Association; confounders possible |
| 4 | Systematic review / meta-analysis of weak studies | Aggregate of lower-quality evidence |
| 5 | Single survey or cross-sectional study | Snapshot correlation; causation not established |
| 6 | Expert opinion / consensus statement | Informed judgment; not independent evidence |
| 7 | Case study or qualitative report | Existence proof; not generalizable |
| 8 | Anecdote or testimonial | Personal experience; highly susceptible to bias |
| 9 | Assertion (no supporting evidence) | No evidential warrant |

Note: a meta-analysis of weak studies (Tier 4) does not become strong evidence by aggregation alone.

**Step 3: Evaluate Quality Within Tier**
Even within its tier, evidence varies in quality. For each key piece of evidence, assess:
- **Sample:** Is the sample size adequate? Is it representative of the population the claim applies to?
- **Methodology:** Is the design appropriate to the claim? (Surveys can't establish causation. A study of 12 people can't support a universal claim.)
- **Replication:** Has this finding been independently replicated?
- **Peer review:** Was it peer reviewed? Where was it published? (Is it pre-print vs. journal? Top venue vs. predatory journal?)
- **Recency:** Is the evidence current enough to be relevant?

**Step 4: Check for Conflicts of Interest**
For each source:
- Who funded the study or produced the evidence?
- Does the producer have a financial, ideological, or reputational stake in the finding?
- Has the evidence been independently replicated by parties without a stake in the conclusion?

Flag: **None apparent / Potential / Clear** — and note the nature of the conflict.

**Step 5: Identify Notable Absences**
This is the most important and most neglected step. Ask what evidence should exist but doesn't:
- If this claim is true, what else would we expect to see in the data? Is that present?
- Have attempts been made to find contradictory evidence? What happened?
- Is there an absence of replication for a finding that should be easy to replicate?
- Are there systematic reviews or meta-analyses that would exist if the field took this seriously?
- Is evidence from particular populations, contexts, or time periods conspicuously missing?

The absence of expected evidence is itself evidence. Name what should exist if the claim were true.

**Step 6: Assess Fit Between Evidence and Claim**
Does the evidence actually establish what the claim asserts?
- **Overgeneralization:** Does the claim assert more than the evidence covers (broader population, stronger causation, greater magnitude)?
- **Mismatch:** Does the evidence come from a different population, context, or time period than the claim applies to?
- **Causal gap:** Does observational evidence support a claim that requires causal warrant?

**Step 7: Issue an Evidence Quality Verdict**
Synthesize to an overall assessment:
- What is the overall evidence tier for this claim?
- How confident can we be in the claim given the evidence?
- What evidence would be needed to adequately support this claim?

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full audit** — All steps: inventory, classify, quality check, conflicts of interest, absences, fit assessment, verdict
  - **Type and quality only** — Classify and evaluate the evidence; skip absence mapping and fit assessment
  - **What's missing** — Focus specifically on what evidence should exist but doesn't
  - **Refine the claim** — Clarify what claim we're auditing evidence for before starting

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

---

## Output Format

### Claim Being Evaluated
[The claim, stated precisely]

### Evidence Inventory

| # | Evidence | Type (Tier) | Quality Assessment | Conflict of Interest |
|---|----------|-------------|-------------------|---------------------|
| 1 | [Description] | [Type, Tier 1-9] | [Sample, methodology, replication notes] | None / Potential / Clear — [note] |
| 2 | ... | | | |

### Notable Absences
- [What should exist if the claim is true, and doesn't]: [Why this matters]
- [Study or replication that would be expected]: [What its absence suggests]

### Fit Between Evidence and Claim
- **Overgeneralization:** [Yes / No — describe if yes]
- **Causal gap:** [Yes / No — does the evidence establish causation if the claim requires it?]
- **Population/context mismatch:** [Yes / No — describe if yes]

### Evidence Quality Verdict
**Overall evidence tier for this claim:** [Strongest tier well-represented in the evidence set]

**Confidence warranted:** Strong / Moderate / Weak / Very weak — [reasoning]

**What would adequate evidence look like:** [The study type and standard that would actually establish this claim]

---

## Notes

Use investigation-claim-decomposition first if the claim has multiple parts — you want to audit evidence for the specific load-bearing sub-claims, not the whole bundle. Use investigation-source-trace if you want to know who produced the primary evidence and how it has been interpreted downstream. Evidence audit is specifically about quality and completeness — not about finding the origin of the claim, but about whether the evidence for it is good.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Evidence audited. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-investigation-source-trace` — Trace weak or contested evidence to its origin
  - `/s4h-probability-confidence-calibration` — Calibrate confidence given the evidence quality found
  - `/s4h-logic-check` — Verify that evidence actually supports the claims it's used for
  - **Done** — Wrap up and synthesise what we have so far
