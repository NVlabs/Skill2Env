---
name: s4h-ethics
description: "Entry point for the ethics toolkit. Routes to the right ethical analysis skill based on your situation. Use when you say 'ethics', 'is this ethical', 'sanity check this', 'who does this affect', 'is this fair', 'something feels wrong', or want ethical reasoning applied without knowing which specific tool fits."
---

# Ethics

Applies ethical reasoning to decisions, designs, policies, and practices. Diagnoses the type and depth of ethical work needed and applies the right tool.

## Which tool fits

| You need to... | Tool |
|---|---|
| Comprehensive multi-framework council with peer review | ethics-council |
| Fast complete ethics report across all frameworks | ethics-check |
| Rapid ethical response to an active incident | ethics-crisis-triage |
| Audit a data collection or sharing decision | ethics-data-audit |
| Check an algorithm or model for bias and fairness | ethics-bias-check |
| Review a UX flow for genuine consent | ethics-consent-review |
| Quick ethical impact scan before shipping | ethics-impact-scan |
| Evaluate a vendor or supplier against ethical standards | ethics-vendor-review |

## Routing Decision

**Framing check:** Confirm the ethical situation and the parties affected before routing. State what you've identified — the actual situation being analyzed, who is affected, and what ethical tension is at stake — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the ethical situation, who is affected, and what is at stake]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

- **High-stakes decision affecting many stakeholders, wants thorough pressure-testing** → ethics-council (full council with peer review, HTML report)
- **Needs a complete ethical assessment quickly** → ethics-check (all 5 frameworks, no peer review overhead)
- **Something has already gone wrong — active incident** → ethics-crisis-triage
- **Data collection, retention, or sharing decision** → ethics-data-audit
- **Algorithm, ML model, ranking, or scoring system** → ethics-bias-check
- **Checkout flow, onboarding, consent, dark patterns** → ethics-consent-review
- **About to ship something, quick impact check** → ethics-impact-scan
- **Evaluating a third-party vendor, API, or partner** → ethics-vendor-review
- **Unclear** → ethics-check (comprehensive but lightweight — surfaces which deeper tool is needed)

## Confirm Direction

After diagnosing which tool fits, use the `AskUserQuestion` tool to confirm direction. Construct the question dynamically to include your diagnosis:

- **Question:** "My read: **[diagnosed tool]** — [one sentence on why it fits]. How would you like to proceed?"
- **Header:** "Direction"
- **Options:**
  - **Yes, run that tool** — Execute the diagnosed skill immediately using the context already provided
  - **Show all options** — List every skill in this category with one-line descriptions
  - **Quick version** — Run a lighter-weight alternative if one exists for this situation
  - **Re-diagnose** — Revisit the situation description for a different read

Proceed based on their selection.

---

## Ethics Check

*Fast comprehensive ethics report across all five frameworks.*

Run the situation through all five ethical frameworks in a single pass:

1. **Utilitarian:** Who is affected and how? Does this maximize net benefit across all parties?
2. **Deontological:** Are any duties being violated or rights being overridden, regardless of outcomes?
3. **Virtue Ethics:** What does this decision say about character? Would someone of integrity do this?
4. **Care Ethics:** Who is vulnerable or in a dependent relationship? Are we honoring those dependencies?
5. **Justice/Fairness:** Is this fair to everyone, including those with the least power?

Synthesize: where do the frameworks agree (high-confidence signal)? Where do they conflict (genuine value tension that must be owned)? Issue a verdict with a direct recommendation.

---

## Ethics Council

*Full five-advisor council with peer review — use for high-stakes decisions.*

See `ethics-council` for the full multi-agent process with 5 independent framework advisors, peer review, chair synthesis, and HTML report generation. Route here when the stakes are high enough to warrant that depth.

---

## Ethics Crisis Triage

*Rapid ethical assessment when something has already gone wrong.*

In a crisis, the instinct is to manage rather than reason. This tool forces ethical clarity under pressure. Apply a rapid three-layer assessment: (1) Immediate harm — who is being harmed right now, and what stops it fastest? (2) Accountability — what transparency is owed, and to whom? (3) Response ethics — which response options themselves create new ethical problems? Crisis responses that cut ethical corners tend to create second crises.

**Output:** Immediate harm assessment, accountability obligations, ethically viable response options, and what to avoid.

---

## Ethics Data Audit

*Audit a data decision against ethical standards.*

Goes beyond legal compliance. Assess: (1) Necessity — is collecting this data actually required for the stated purpose? (2) Proportionality — is the scope of collection proportional to the benefit? (3) Consent — do people meaningfully understand and agree to this? (4) Harm potential — what's the worst realistic use or breach? (5) Retention — how long is too long?

**Output:** Data practice assessment across all five dimensions, with specific changes that would make the practice clearly ethical.

---

## Ethics Bias Check

*Evaluates an algorithm or model for discriminatory patterns.*

Assess the system against protected characteristics: does it produce systematically different outcomes for different groups? If so: is the difference justified by legitimate criteria, or does it reflect historical bias in training data? Apply four fairness standards: equal treatment, equal outcome, individual fairness, and counterfactual fairness. Flag which standard is being violated and by what mechanism.

**Output:** Fairness assessment per standard, identified disparate impacts, root cause of bias, and mitigation recommendations.

---

## Ethics Consent Review

*Reviews a UX flow for genuine consent.*

Genuine consent is informed, voluntary, and meaningful — not just legally checkboxed. Evaluate the flow: Can users meaningfully understand what they're agreeing to? Are they under pressure (dark patterns, urgency, buried choices)? Is opting out as easy as opting in? Would a user feel deceived after the fact?

**Output:** Consent quality assessment, specific dark patterns identified, and changes needed for consent to be genuine.

---

## Ethics Impact Scan

*Quick pre-ship ethical impact assessment.*

Before committing, surface: who benefits from this? Who bears costs or risk? At what scale? Are the costs and benefits distributed fairly? Are any harms irreversible? This is a lightweight check that takes minutes — the goal is to catch obvious ethical problems before they become embedded in shipped product.

**Output:** Benefit/harm map, distribution assessment, irreversibility flags, and a go/no-go recommendation with conditions.

---

## Ethics Vendor Review

*Evaluates a third-party against ethical standards.*

Assess across five domains: (1) Labor practices — how are workers treated in the supply chain? (2) Data handling — how do they use data about you and your users? (3) Business model — does their incentive structure align with your values? (4) Environmental impact, (5) Political/social alignment — do their positions or practices conflict with stated values? A vendor whose practices conflict with your values makes your product complicit.

**Output:** Vendor assessment across all five domains, red flags, and a recommendation on whether to proceed.
