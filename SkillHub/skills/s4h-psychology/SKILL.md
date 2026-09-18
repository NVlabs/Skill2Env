---
name: s4h-psychology
description: "Entry point for the psychology toolkit. Routes to the right psychology skill based on your situation. Use when you say 'psychology', 'what's driving this behavior', 'why is this person doing X', 'what biases are at play', 'how do I change a habit', 'how do I persuade', 'should I trust my gut', 'what motivates them', or want cognitive/behavioral analysis without knowing which specific tool fits."
---

# Psychology

Applies cognitive and behavioral frameworks to understand why people think, feel, and act as they do — and how to influence and change that. Diagnoses what kind of psychological work is needed and routes to the right tool.

## Which tool fits

| You need to... | Tool |
|---|---|
| Identify which cognitive biases are distorting thinking in a specific situation | psychology-cognitive-biases |
| Diagnose what's actually driving someone's behavior (surface vs. root) | psychology-motivation |
| Assess whether to trust or override fast intuitive thinking | psychology-heuristics |
| Change someone's mind or drive action through influence | psychology-persuasion |
| Shift entrenched behavior or break/build a habit | psychology-behavior-change |

## Routing Decision

**Framing check:** Confirm the specific situation before routing. State what you've identified — the person or group whose psychology is in question, the behavior or decision at issue, and the outcome the user is trying to understand or influence — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific situation, person/group, and goal]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

- **"Why is [person/group] doing this?" / "What's driving this behavior?"** → psychology-motivation (surface vs. root motivation, what need is actually being served)
- **"What biases might be at play?" / "Are we thinking clearly about this?"** → psychology-cognitive-biases (diagnostic scan for active cognitive distortions)
- **"Is my gut right here?" / "Should I trust my instinct?" / "When does fast thinking work?"** → psychology-heuristics (assess the heuristic in use, decide whether to override)
- **"How do I change someone's mind?" / "What would convince them?" / "How do I get buy-in?"** → psychology-persuasion (select influence approach, construct the case)
- **"How do I change this behavior?" / "Why does this habit persist?" / "How do I make X stick?"** → psychology-behavior-change (diagnose what's maintaining the behavior, design the intervention)
- **Unclear** → psychology-motivation (most behavior questions are ultimately about what need is being served)

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

## Cognitive Biases

*Diagnostic scan: which cognitive biases are actively distorting thinking in this specific situation.*

Not a laundry list — a targeted diagnostic. Identify the decision, belief, or behavior in question. Scan for which bias categories are most live given the specific context. Diagnose how the distortion is operating. Recommend the counter-move for each active bias.

Key categories: confirmation bias (seeking confirming evidence), availability heuristic (overweighting vivid or recent examples), anchoring (over-relying on first information), sunk cost (weighting past investment in future decisions), in-group bias (favoring similarity), optimism bias (underestimating risks to self), planning fallacy (underestimating time/cost/complexity).

**Output:** Active biases table with distortion mechanism and counter-move for each.

---

## Motivation

*Diagnose what's actually driving behavior — surface motivation vs. root motivation.*

Observe the behavior. Name the surface motivation (what they say they want, or what the obvious explanation is). Then probe deeper: which fundamental need is this serving? Apply Self-Determination Theory (autonomy, competence, relatedness), Maslow as a diagnostic (is a lower-level need unmet?), and the identity dimension ("I am the kind of person who..."). Identify what's actually needed for sustained engagement.

**Output:** Surface motivation, root motivation, underlying need, and the lever that addresses the real driver.

---

## Heuristics

*Assess the fast-thinking pattern at work — when to trust it, when to override it.*

Identify which heuristic is operating (representativeness, availability, affect, recognition). Classify whether it's in its domain of reliability. Assess whether there's a systematic distortion present. Produce a recommendation: trust the fast thinking, override it with deliberate analysis, or gather more information before deciding.

Kahneman System 1 / System 2 framework: System 1 is fast, automatic, pattern-matching. It's adaptive within its domain of experience; it fails when applied outside that domain or when the situation has been engineered to exploit it.

**Output:** Heuristic identified, domain assessment, distortion risk, and trust/override recommendation.

---

## Persuasion

*Select and construct the right influence approach for the context.*

Identify what you're trying to change (belief, attitude, behavior, decision). Select the most appropriate influence approach: Cialdini's six principles (reciprocity, commitment/consistency, social proof, authority, liking, scarcity), elaboration likelihood model (central route for motivated/capable audiences; peripheral cues for low-engagement), or inoculation (pre-emptive counter-persuasion for hardening positions). Identify ethical constraints. Construct the approach.

**Output:** Influence analysis, recommended approach, ethical assessment, and constructed message or approach.

---

## Behavior Change

*Diagnose what's maintaining a behavior and design the right intervention.*

Identify the behavior to change. Classify what's maintaining it: habit loop (cue → routine → reward), motivation deficit, capability gap, friction, or identity conflict. Select the right intervention: habit redesign, implementation intentions, friction reduction, motivation amplification, or identity reframing. Design the concrete implementation.

**Output:** Maintenance diagnosis, intervention type, and specific implementation design.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Psychology analysis complete. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-communication-audience-modeling` — Apply the psychological insights to communication strategy
  - `/s4h-social-incentive-analysis` — Connect psychological analysis to social incentives
  - `/s4h-emotional-motivation-mapping` — Deepen with emotional motivation analysis
  - **Done** — Wrap up and synthesise what we have so far
