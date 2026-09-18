---
name: s4h-investigation
description: "Entry point for the investigation toolkit. Routes to the right investigation skill based on what you're trying to establish. Use when you say 'investigate', 'verify this', 'check this claim', 'where does this come from', 'is this true', 'trace the source', 'stress-test this belief', 'what's the evidence', 'could something else explain this', or want to know whether something you've heard is actually true."
---

# Investigation

Practical truth-finding methodology: tracing sources, decomposing claims, evaluating evidence, generating rival hypotheses, and triangulating across independent sources. Diagnoses what kind of investigative work is needed and routes to the right tool.

## Which tool fits

| You need to... | Tool |
|---|---|
| Trace a claim back to its origin and test how it has changed in transmission | investigation-source-trace |
| Break a complex claim into its smallest independently verifiable parts | investigation-claim-decomposition |
| Evaluate the quality, strength, and completeness of evidence | investigation-evidence-audit |
| Generate the best alternative explanations for the same observations | investigation-counter-hypothesis |
| Verify a claim across genuinely independent sources | investigation-triangulation |

## Routing Decision

- **"Where does this claim come from? Who first said this?"** → investigation-source-trace (trace origin, test source credibility, map distortion in transmission)
- **"What exactly is this claiming? What are all the sub-claims inside it?"** → investigation-claim-decomposition (decompose → classify → identify load-bearing parts)
- **"Is the evidence good? Is there enough of it? Is it the right kind?"** → investigation-evidence-audit (evidence type hierarchy, quality, completeness, conflicts of interest)
- **"Could something else explain this? Is there another interpretation?"** → investigation-counter-hypothesis (rival explanations, decisive tests)
- **"Can I verify this from multiple angles? Do independent sources agree?"** → investigation-triangulation (classify independence, map convergence/divergence)
- **Unclear** → investigation-claim-decomposition (surfaces what you're actually trying to verify, then you can route further)

## Confirm Direction

After diagnosing which tool fits, use the `AskUserQuestion` tool to confirm direction. Construct the question dynamically to include your diagnosis:

- **Question:** "My read: **[diagnosed tool]** — [one sentence on why it fits]. How would you like to proceed?"
- **Header:** "Direction"
- **Options:**
  - **Yes, run that tool** — Execute the diagnosed skill immediately using the context already provided
  - **Show all options** — List every skill in this category with one-line descriptions
  - **Run all relevant tools** — Run multiple investigation lenses on the same claim (e.g., decompose first, then audit evidence)
  - **Re-diagnose** — Revisit the situation description for a different read

Proceed based on their selection.

---

## Source Trace

*Find where a claim actually came from and test whether the origin holds.*

Trace the claim back to its earliest source: who first made it, in what context, with what evidence. Map how the claim changed as it propagated — paraphrasing, scope shifts, dropped caveats. Test the source's credibility and incentive structure. Issue a verdict on whether the original claim supports the form the claim has taken.

**Output:** Origin identification, transmission map with distortion points, source credibility assessment, verdict on whether the current claim is faithful to the original.

---

## Claim Decomposition

*Break a complex claim into its smallest independently verifiable parts.*

Surface the hidden architecture of a claim: what sub-claims are inside it, which are independently verifiable vs. assumed, and which sub-claims carry the most logical load. A claim like "the market is shifting toward X" typically has 5-8 hidden claims — direction, pace, magnitude, causation, durability, relevance — each separately falsifiable.

**Output:** Full decomposition of sub-claims, classification of each (verified/checkable/uncheckable/assumed), identification of the highest-load sub-claims, and recommended verification priorities.

---

## Evidence Audit

*Evaluate the quality, strength, and completeness of evidence for a claim.*

Apply a structured evidence quality assessment: evidence type (RCT vs. observational vs. anecdote vs. expert opinion), sample quality, methodological soundness, conflicts of interest, and what is notably absent. Uses an evidence hierarchy to locate where the current evidence sits and what stronger evidence would look like.

**Output:** Evidence inventory, type and quality classification, notable absences, conflict-of-interest flags, and an overall evidence quality verdict.

---

## Counter-Hypothesis

*Generate the best alternative explanations for the same observations.*

Take a claim and systematically generate rival explanations that fit the available evidence equally well — or better. For each rival hypothesis, ask what evidence would distinguish it from the original. Identify the decisive test: the observation or experiment that, if run, would most cleanly discriminate between explanations.

**Output:** Original claim restatement, 3-5 rival hypotheses with supporting evidence, distinguishing evidence for each, and the decisive test.

---

## Triangulation

*Verify a claim across genuinely independent sources.*

Collect candidate sources for a claim. Classify them by independence — many sources that all trace back to the same original aren't independent, they're amplification. Assess whether truly independent sources converge (claim is more reliable) or diverge (claim is contested or uncertain). Issue a triangulation verdict.

**Output:** Source list, independence classification, convergence/divergence assessment, and a reliability verdict based on the triangulation.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Investigation complete. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-logic-check` — Validate that conclusions drawn from the investigation hold
  - `/s4h-probability-confidence-calibration` — Calibrate confidence given what the investigation found
  - `/s4h-epistemology-limits` — Map the limits of what investigation can establish here
  - **Done** — Wrap up and synthesise what we have so far
