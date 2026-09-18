---
name: s4h-psychology-heuristics
description: "Assess the fast-thinking pattern at work — when it's reliable, when it misleads, and whether to trust or override it. Triggers: 'should I trust my gut', 'is my intuition right here', 'fast thinking', 'heuristic', 'when does instinct work', 'System 1 vs System 2', 'pattern recognition', 'am I just pattern matching', 'is this a gut check or analysis question'."
---

# Psychology: Heuristics

Fast thinking is not sloppy thinking — it's compressed expertise. Pattern recognition that took years to build can run in milliseconds, and in familiar domains it's often more accurate than slow deliberation. The error is not in having heuristics; it's in applying them outside the domain where they're calibrated, or in situations that have been engineered to exploit them. The question is never "did I use a heuristic?" (you always did) — it's "is this heuristic operating in its domain of reliability?"

---

## Your Process

**Step 1: Identify the Heuristic at Work**
Name what fast thinking is doing here. Common heuristics:

**Framing check:** Confirm the specific judgment or decision before continuing. State what you've identified — the actual situation where fast thinking is being used and what is at stake — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific situation and the heuristic potentially at work]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

- **Representativeness** — Judging probability by how much something resembles the prototype of a category. "This startup's pitch sounds like every successful startup I've seen." Fast and often right within familiar patterns; fails when base rates matter (most startups fail regardless of how compelling the pitch sounds).
- **Availability** — Judging frequency or likelihood by how easily examples come to mind. Recent, vivid, or emotionally charged examples feel more probable. Fails when the most available examples are systematically unrepresentative (media coverage, personal experience).
- **Affect heuristic** — If you feel good about something, you perceive it as lower risk and higher benefit; if you feel bad, higher risk and lower benefit. Fast integration of complex information; fails when the feeling is a response to something unrelated to the actual decision.
- **Recognition heuristic** — Preferring the recognized option when one option is recognized and another isn't. "I've heard of this company, so it must be better." Adaptive when recognition correlates with quality; fails when recognition is driven by marketing rather than merit.
- **Fluency heuristic** — Judging things that are easier to process as more true, more valuable, or more trustworthy. Clear writing, simple numbers, and familiar ideas benefit from this; it penalizes novelty and complexity that is genuine.
- **Social consensus** — Using what others are doing as a guide to what's correct. Adaptive in stable environments with accumulated collective wisdom; fails in novel situations, bubbles, or when the crowd is itself reacting to a cascade.
- **Expert intuition** — Pattern recognition built through deliberate practice in a domain with regular feedback. Reliable in high-validity environments (chess, firefighting, intensive care); unreliable in low-validity environments where feedback is delayed, noisy, or absent (financial forecasting, hiring decisions).

**Step 2: Classify the Domain**
Is the heuristic being applied in its domain of reliability? The key dimensions:
- **Familiarity:** How similar is this to situations the person has actually experienced? Heuristics calibrate to past experience; novel situations break calibration.
- **Feedback regularity:** Has the fast-thinker received consistent, timely feedback when this heuristic was right or wrong? Experts in surgery get fast feedback; managers making hiring decisions often don't.
- **Engineered exploitation:** Has the situation been designed to trigger the heuristic for someone else's benefit? Pricing anchors, scarcity signals, social proof manufactured through fake reviews — these exploit availability and social consensus.
- **Emotional activation:** Is a strong emotion active that could contaminate the affect heuristic? Fear, desire, or resentment can load all subsequent judgments.

**Step 3: Assess Systematic Distortion Risk**
Is there a predictable direction in which this heuristic, in this context, is likely to mislead?
- If yes: name the direction and the magnitude. "Availability is likely producing overestimation of failure probability by roughly 2x given recent high-profile failures in adjacent space."
- If no: the heuristic is probably operating within its domain.

**Step 4: Decide Whether to Trust, Override, or Supplement**

**Trust the fast thinking when:**
- The domain is familiar and feedback has been regular
- There is no emotional activation from an irrelevant source
- The situation has not been engineered to exploit the heuristic
- Stakes are moderate and the cost of analysis exceeds the cost of being wrong

**Override and apply System 2 analysis when:**
- The situation is novel — outside prior experience
- There is a predictable direction of distortion
- Stakes are high and the error is asymmetric (being wrong in one direction is much worse)
- The situation shows classic signs of exploitation (artificial scarcity, social proof manipulation, anchors set by counterparty)

**Supplement (use both) when:**
- Strong intuition but high stakes: use System 2 to check the fast read, not replace it
- Weak or absent intuition: slow analysis is the only option
- Multiple experts are available and their intuitions diverge: the disagreement is informative data

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full assessment** — All steps, reasoning shown throughout
  - **Recommendation only** — Skip the diagnosis; just tell me whether to trust or override
  - **Identify the heuristic** — I just want to know what fast-thinking pattern is at work
  - **Refine the situation** — Clarify what's being decided before starting

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

---

## Output Format

### Situation
[Restate the decision or judgment being made in one sentence]

### Heuristic Identified
**[Heuristic name]** — [How it's operating in this specific situation]

### Domain Assessment
- **Familiarity:** [High / Medium / Low] — [Why]
- **Feedback regularity:** [High / Medium / Low] — [Why]
- **Exploitation risk:** [Present / Not present] — [Why]
- **Emotional contamination:** [Present / Not present] — [Why]

### Distortion Risk
**Direction:** [Which way does this heuristic likely err in this context?]
**Magnitude:** [Rough sense of how far off it might be]

### Recommendation
**[Trust / Override / Supplement]** — [One paragraph explaining why, and what to do]

---

## Notes

The goal is calibration, not skepticism. Dismissing all heuristics produces analysis paralysis; the research on expert intuition shows that in high-validity domains, fast thinking from genuine experts outperforms deliberate analysis. Klein's research on naturalistic decision-making, and the disagreement between him and Kahneman, is instructive: they are both right about different domains.

Use psychology-cognitive-biases when the question is about systematic distortions in a group's beliefs or decisions (biases operate at the population level and compound over time). Use psychology-heuristics when the question is about a specific instance of fast thinking and whether to rely on it. They overlap but have different entry points: biases are about distorted conclusions; heuristics are about the reasoning shortcuts that get you there.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Heuristics mapped. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-decision-criteria-weighting` — Weight criteria using the right heuristics
  - `/s4h-logic-check` — Validate where heuristics may mislead the reasoning
  - `/s4h-probability-confidence-calibration` — Calibrate confidence adjusting for heuristic errors
  - **Done** — Wrap up and synthesise what we have so far
