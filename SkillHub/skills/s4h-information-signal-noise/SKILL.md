---
name: s4h-information-signal-noise
description: "Separates meaningful signal from background noise. Use when asked to 'find the signal', 'cut through the noise', 'what actually matters here', 'what's driving the variation', 'is this data telling us something real', or when a source is overwhelming and it's unclear what's relevant."
---

# Information: Signal–Noise

Every source is a mixture of signal and noise. Signal is the variation that carries information about what you care about. Noise is everything else — random variation, artefacts, irrelevant fluctuation, measurement error, distortion in the channel. The same data point can be signal in one context and noise in another; the same message can be clear in one medium and garbled in another.

Claude Shannon's foundational contribution was showing that signal-to-noise ratio (SNR) is a precisely definable quantity, and that a channel's capacity to transmit information is mathematically bounded by its SNR. The insight travels well beyond telecommunications. Any situation where useful information must be extracted from a noisy background has the same structure: evidence vs. noise in a research base, insight vs. artefact in a dataset, the core message vs. verbal interference in a communication, the relevant metric vs. random fluctuation in a business dashboard. This skill applies SNR thinking to find what's actually there.

Norbert Wiener's cybernetics framework added the feedback dimension: systems that can detect and suppress their own noise are more robust. The question is not just "what is the signal?" but "what is the system doing to amplify or attenuate it?"

---

## Your Process

**Step 1: Define Signal**
Before anything else, get precise about what you are trying to detect. "Signal" is not "useful information in general" — it is the specific variation or pattern that would update your picture of the thing that matters. Name the target signal explicitly: what would a perfect source of this signal look like?

**Framing check:** Confirm the target signal and the source before continuing. State what you've identified — what signal you're looking for, in what source, and why it matters — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the signal, source, and purpose]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Enumerate Noise Sources**
List every identifiable source of non-signal variation:
- **Random noise:** measurement error, sampling variance, irreducible uncertainty
- **Systematic noise (bias):** consistent distortions in one direction — selection effects, measurement bias, confounding variables
- **Channel noise:** distortion introduced in transmission — summarisation loss, translation error, compression artefacts
- **Interference:** other signals present in the same medium that are not the target — a noisy dataset with multiple confounded causes, a message with competing sub-agendas

**Before narrowing:** Show the complete enumerated noise sources before filtering. Use `AskUserQuestion`:
- **Question:** "I've identified [N] potential noise sources. Before I assess which are dominant, do any strike you as particularly important, or have I missed any?"
- **Header:** "Noise sources"
- **Options:**
  - **Proceed with your assessment** — the list looks right
  - **Add one I missed** — user will name it
  - **Remove a false positive** — user will identify what doesn't belong

**Step 3: Assess Signal-to-Noise Ratio**
For each candidate signal: how strong is it relative to the dominant noise floor? Assess whether the signal is:
- **Clearly present:** variance attributable to signal substantially exceeds noise
- **Marginal:** signal is present but difficult to distinguish from noise — requires amplification or better instrumentation
- **Undetectable:** noise is large enough that you cannot reliably distinguish whether a signal is there at all

**Step 4: Identify Amplifiers and Attenuators**
What in the current setup amplifies noise (and should be reduced)? What amplifies signal (and should be preserved or extended)?

Common amplifiers of noise: small sample sizes, aggregation across heterogeneous groups, measurement instruments not calibrated to the target, lossy channels, attention to outliers, confirmation bias in data collection.

Common amplifiers of signal: appropriate granularity, comparison to relevant baselines, replication, triangulation across independent sources, domain expertise that knows where to look.

**Step 5: Recommend a SNR Strategy**
Given the SNR assessment, specify:
- What should be foregrounded (primary signal channels)
- What should be filtered or discarded (dominant noise sources)
- What additional measurement or instrumentation would raise the SNR
- What cannot be recovered — what information has already been lost to noise in this source

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what source is being analysed, what signal you're looking for, and what the key challenge is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output: what the signal is and what the main noise sources are
  - **Specific focus** — Zoom in on one aspect: signal identification, noise enumeration, or SNR strategy
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Target Signal:** [Precise statement of what signal you're looking for and why it matters]

**Noise Inventory**

| Noise Source | Type | Estimated Impact | Reducible? |
|---|---|---|---|
| [source] | Random / Systematic / Channel / Interference | Low / Medium / High | Yes / No / Partially |

**SNR Assessment:** [Overall assessment — is the signal clearly present, marginal, or undetectable in this source?]

**Signal Amplifiers:** [What to preserve or extend]

**Noise Suppressors:** [What to filter or eliminate]

**Information Loss:** [What has already been permanently lost to noise in this source]

**Recommended SNR Strategy:** [Specific, actionable steps to raise signal quality]

---

## Notes

Signal–noise analysis presupposes you know what signal you're looking for. When you don't — when the goal is exploration rather than detection — you need a different starting point. Consider `/s4h-epistemology-knowledge-types` to clarify what kind of knowing is in play, or `/s4h-sensory-structured-observation` to open up attention before filtering it. Signal–noise is a focusing tool; it works best when the target is defined.

This skill pairs naturally with `/s4h-information-compression` (having found the signal, what's the minimum representation that preserves it?) and `/s4h-investigation-evidence-audit` (what does the evidence actually establish once noise is stripped away?).

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Signal separated from noise. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-information-compression` — Compress the signal down to its essential form
  - `/s4h-information-entropy` — Measure how much information the signal actually carries
  - `/s4h-investigation-evidence-audit` — Audit what the cleaned signal actually establishes
  - **Done** — Wrap up and synthesise what we have so far
