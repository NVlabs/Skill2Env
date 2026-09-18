---
name: s4h-cognition-metacognition
description: "Applies thinking-about-thinking as a practical tool — monitoring comprehension, calibrating confidence, and knowing what you do not know. Use when asked 'how confident should I be about this', 'am I actually understanding this or just recognising it', 'what do I not know that I should know', 'I think I understand this but I keep getting it wrong', 'calibrate my confidence', or when the quality of reasoning on a complex problem needs to be assessed from the outside."
---

# Cognition: Metacognition

Metacognition — the capacity to think about your own thinking — is what separates competent performance from expert adaptation. John Flavell, who established metacognition as a formal field of study at Stanford in the 1970s, identified three interlocking components: **metacognitive knowledge** (what you know about cognition in general and your own cognitive patterns in particular), **metacognitive monitoring** (tracking your comprehension and reasoning in real time), and **metacognitive control** (adjusting your approach when monitoring reveals a problem). All three are necessary. Most people engage in only the first.

The deepest metacognitive failure is the illusion of knowing — the conviction that you understand something you have only recognised. Familiarity and comprehension feel identical from the inside. You've read about second-order effects; you can nod when someone mentions them; but can you predict them in a novel case? The Dunning-Kruger phenomenon is partially a metacognitive failure: the incompetent are unable to recognise their own incompetence because competence is required to accurately monitor competence. Metacognitive skill is the corrective.

This skill applies Flavell's three-component framework as a practical diagnostic. It is not a general survey of your cognitive patterns — it is a targeted assessment of your thinking quality in a specific domain or decision, right now.

---

## Your Process

**Step 1: Define the Cognitive Task**
What is the specific domain, decision, or problem where thinking quality needs to be assessed? Be concrete: "understanding how our pricing affects customer retention" is more useful than "understanding the business." The metacognitive assessment will be more accurate and actionable if it is scoped to a specific task.

**Framing check:** Confirm the specific cognitive task before continuing. State what you've identified — the domain or decision and what metacognitive dimension seems most at stake — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific domain and the metacognitive question at stake]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Assess Metacognitive Knowledge**
What do you actually know in this domain? Apply the distinction between:
- **Recognition knowledge:** can identify the concept when encountered; nod along when it's mentioned
- **Explanation knowledge:** can explain the concept in your own words to someone unfamiliar with it
- **Application knowledge:** can apply the concept accurately in novel cases without prompting
- **Generation knowledge:** can identify where the concept applies before being told to look

Map the current state of knowledge against this hierarchy. Where does recognition end and genuine comprehension begin? What is being mistaken for understanding?

**Step 3: Apply Metacognitive Monitoring**
Test comprehension in real time using three diagnostic probes:

- **Explanation probe:** Can you explain the key mechanisms without looking anything up? Where do you get vague? Vagueness under self-explanation is evidence of an illusion of knowing.
- **Prediction probe:** Given the mechanisms as you understand them, what would you predict about a specific novel case? Are the predictions specific enough to be wrong? Vague predictions suggest the model is underspecified.
- **Contradiction probe:** What evidence would contradict your current understanding? If you can't name it, your understanding may be unfalsifiable — which means it's not doing real work.

**Before narrowing:** Use `AskUserQuestion` after running the monitoring probes:
- **Question:** "I've run the three monitoring probes. The picture that's emerging is [brief summary of where understanding is solid and where it's weak]. Before I assess control strategies, is there a specific area of the domain where you want to probe more deeply?"
- **Header:** "Monitoring"
- **Options:**
  - **Proceed with the control assessment** — the picture is clear enough
  - **Probe deeper on [area]** — user will name the specific area
  - **Adjust the domain scope** — the domain as framed is too broad or too narrow

**Step 4: Diagnose Metacognitive Control**
What adjustments, if any, are being made when monitoring reveals gaps? Three failure modes:
- **No adjustment:** comprehension gaps are noted and ignored — "I'll figure it out when I need to"
- **Compensating adjustment:** effort increases (reading more, working harder) without changing the approach — which doesn't fix a strategy problem
- **Avoidance:** domains of weakness are systematically avoided, so the gap never surfaces until it matters

Identify which failure mode is present and what the right control adjustment would be.

**Step 5: Calibrate Confidence**
Express confidence as a percentage for the key claims being made in this domain. Test for the common calibration failure modes:
- **Overconfidence:** stated confidence exceeds accuracy (the most common error)
- **Underconfidence:** stated confidence is lower than accuracy (common in experts who have internalised how much they don't know)
- **Confidence without resolution:** high stated confidence on claims that are genuinely uncertain, without acknowledgement of the uncertainty

Kahneman's System 1/System 2 distinction is relevant here: fast intuitive confidence is not the same as calibrated epistemic confidence. A feeling of certainty is evidence of familiarity, not necessarily accuracy.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what domain is being assessed and what the primary metacognitive issue appears to be — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — All three components: knowledge mapping, monitoring probes, control diagnosis, confidence calibration
  - **Confidence calibration only** — Focused assessment of whether stated confidence matches actual comprehension
  - **Knowledge gap mapping** — Focus on identifying what is known vs. thought-to-be-known
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Metacognitive Knowledge Assessment**

| Area | Knowledge Type | Status | Evidence |
|---|---|---|---|
| | Recognition / Explanation / Application / Generation | Solid / Partial / Illusory | |

**Monitoring Results**
- Explanation probe: [what was solid, where it got vague]
- Prediction probe: [how specific and testable the predictions were]
- Contradiction probe: [what evidence would falsify the current understanding]

**Control Diagnosis:** [Which failure mode is present and what the right adjustment is]

**Confidence Calibration**

| Claim | Stated confidence | Assessed calibration | Adjustment |
|---|---|---|---|
| | | | |

**Priority Gaps:** [The two or three most consequential things you don't know that you might think you know]

---

## Notes

Metacognition is the most transferable cognitive skill because it applies to every domain — but it is also the most demanding, because it requires honest appraisal of your own limitations. The output of this skill should feel mildly uncomfortable. If it doesn't, the monitoring step wasn't rigorous enough.

The nearest neighbor is `/s4h-epistemology-epistemic-status` — which examines the warrant for specific claims. Metacognition operates on the thinker (what do you actually understand and how well are you monitoring it?); epistemology-epistemic-status operates on the claims (what is the state of evidence for this belief?). Both are often needed when expertise is in question.

For the confidence calibration specifically, `/s4h-probability-confidence-calibration` provides a quantitative framework for expressing and testing uncertainty.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Metacognitive assessment complete. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-cognition-mental-models` — Audit the specific models driving the gaps identified in this assessment
  - `/s4h-epistemology-epistemic-status` — Examine the evidential warrant for the claims where confidence was hardest to calibrate
  - `/s4h-probability-confidence-calibration` — Apply formal probability calibration to the confidence estimates surfaced here
  - **Done** — Wrap up and synthesise what we have so far
