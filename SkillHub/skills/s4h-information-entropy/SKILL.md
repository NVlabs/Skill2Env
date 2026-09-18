---
name: s4h-information-entropy
description: "Measures uncertainty, surprise, and information content using Shannon entropy. Use when asked 'how much information does this actually contain', 'how uncertain is this source', 'is this result surprising', 'what should I update on', 'where is the real information in this dataset', or when you need to distinguish high-information from low-information inputs."
---

# Information: Entropy

In 1948, Claude Shannon defined information in terms of surprise. The information content of a message is the degree to which it reduces your uncertainty. A message you could have predicted perfectly carries zero information — it tells you nothing you didn't already know. A completely unexpected message carries maximum information. Shannon called this quantity entropy, borrowing the term from thermodynamics: like physical entropy, it measures disorder and unpredictability.

Shannon entropy is defined as H = −∑ p(x) log₂ p(x) across all possible outcomes. The maximum entropy of a source is achieved when all outcomes are equally likely — pure unpredictability. Minimum entropy is achieved when one outcome is certain — pure predictability. Applied practically: a quarterly report that always says roughly the same thing carries low entropy. A dataset where any measurement could be anything carries high entropy. Neither extreme is ideal — maximum entropy is overwhelming, minimum entropy is uninformative.

Norbert Wiener extended this framework through cybernetics to argue that information is what distinguishes organisation from chaos in any self-regulating system. A thermostat carries information about temperature; the information is what allows the system to maintain order. Wiener's key insight: the entropic arrow runs toward decay unless information is actively used to correct it. Systems without good information channels become entropic — they drift.

Andrei Kolmogorov gave entropy a computational interpretation: the algorithmic complexity of a string is the length of the shortest program that can generate it. A truly random sequence cannot be compressed — it has maximum Kolmogorov complexity. A highly ordered sequence can be compressed to a short description — it has low complexity. The two frameworks — Shannon's probabilistic entropy and Kolmogorov's algorithmic complexity — converge: low-entropy sources are compressible; high-entropy sources are not.

The practical application is calibrating attention and weight. When a source has low entropy (high predictability), each new message from it should update you very little. When a source has high entropy (high surprise rate), each new message carries real information and deserves genuine engagement. Most people give equal attention to all messages regardless of their information content — this is the calibration error this skill corrects.

---

## Your Process

**Step 1: Identify the Source and the Question**
Name the source being analysed (a data series, a person, a research domain, a sensor, a communication channel, a market) and the question the source is being asked to answer. Entropy is always relative to a question — the same source may be high-entropy with respect to one question and low-entropy with respect to another.

**Framing check:** Confirm the source and the question before continuing. State what you've identified in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the source and what question it's being used to answer]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Assess the Probability Distribution**
What are the possible outputs of this source, and how likely is each? You don't need precise numbers — a qualitative assessment of the distribution shape is enough:

- **Near-uniform distribution (high entropy):** all outcomes roughly equally likely. Every message is potentially surprising. High information content per message.
- **Peaked distribution (low entropy):** most probability mass on a few outcomes. Messages are usually predictable. Low information content per typical message.
- **Fat-tailed distribution:** most messages are predictable, but rare messages are very surprising — and the surprises carry most of the information.
- **Prior-dependent:** entropy relative to a naive prior may be high, but relative to a well-informed prior it may be low. Establish whose prior is being used.

**Step 3: Identify High-Information vs. Low-Information Elements**
Within the source, which specific elements carry the most information? Apply the entropy framework:
- What is expected and therefore carries little information?
- What is unexpected and therefore carries substantial information?
- Where is the distribution non-uniform in ways that weren't anticipated?
- What are the absence-of-information signals — things that were expected but didn't appear?

**Before proceeding:** Surface the high-information elements for confirmation before weighting analysis. Use `AskUserQuestion`:
- **Question:** "I've identified [N] high-information elements in this source. Before I assess their implications, does this map match your sense of where the real content is?"
- **Header:** "Information content"
- **Options:**
  - **Yes — proceed** — the identification looks right
  - **I'd emphasise something different** — user will identify a different high-information element
  - **Add context that would change the prior** — user will provide it

**Step 4: Assess Calibration**
Is attention and weight currently being allocated according to information content? Common miscalibrations:
- **Attending to low-entropy signals:** treating predictable outputs as informative — confirmation bias at the information level
- **Underweighting high-entropy surprises:** dismissing surprising results as noise rather than updating on them
- **Treating all sources as equally informative:** failing to distinguish sources by their entropy profiles
- **Ignoring base rates:** assessing how surprising a result is without correctly accounting for the prior — overweighting rare-but-expected, underweighting common-but-important

**Step 5: Recommend an Entropy-Calibrated Weighting**
Given the entropy analysis, specify how attention and update weight should be allocated:
- Which inputs deserve genuine updating (high information content)
- Which inputs can be processed routinely (low information content, expected)
- Which absence-of-signal cases should be treated as informative
- Whether the source itself needs to be restructured to raise or lower entropy depending on the goal

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what source is being analysed, what the entropy question is, and what the calibration problem is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps with full entropy assessment and calibration recommendations
  - **Key findings only** — Which elements are high-information and what to update on
  - **Specific focus** — Zoom in on one element: the distribution assessment, the high-information identification, or the calibration audit
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Source:** [What is being analysed]
**Question being asked of the source:** [What the source is being used to answer]

**Entropy Profile**

| Element / Signal | Predictability | Information Content | Notes |
|---|---|---|---|
| [element] | High / Medium / Low | Low / Medium / High | [e.g., "fat-tail risk", "prior-dependent", "absence informative"] |

**Overall Entropy Assessment:** [High / Medium / Low entropy source — what this means for how much each new message should update you]

**High-Information Elements:**
[Bulleted list of the specific signals, results, or messages that carry genuine information content and deserve real attention]

**Low-Information Elements:**
[What is predictable, expected, and should not substantially update the picture]

**Absence-of-Information Signals:**
[Things that were expected but didn't appear — and what their absence means]

**Calibration Audit:**
[Where is attention currently miscalibrated — attending to low-entropy signals, or dismissing high-entropy ones?]

**Recommended Entropy-Calibrated Weighting:**
[Specific guidance on where to direct attention and update weight]

---

## Notes

Entropy analysis works best when you have enough history or context to estimate the probability distribution of the source. For genuinely novel sources where there is no prior distribution to estimate, the tool is less precise — but you can still reason about the shape of the distribution (what would be expected vs. surprising, given any available context).

Shannon entropy and Kolmogorov complexity converge in the important cases: low-entropy sources are compressible, which means `/s4h-information-compression` and this skill are natural partners. Having identified which elements carry real information content (entropy analysis), you can then ask how to represent them with minimum description length (compression).

The nearest-neighbour trap is conflating high entropy with high value. A high-entropy source is unpredictable and surprising — but surprising outputs can be noise as well as signal. Use `/s4h-information-signal-noise` to determine whether high-entropy variation is genuine signal or random noise before updating heavily on it.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Entropy assessed. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-information-signal-noise` — Verify whether high-entropy elements are signal or noise before updating
  - `/s4h-probability-base-rate-anchoring` — Anchor the surprise assessment against correct base rates
  - `/s4h-epistemology-epistemic-status` — Map how much the high-information elements should actually update your beliefs
  - **Done** — Wrap up and synthesise what we have so far
