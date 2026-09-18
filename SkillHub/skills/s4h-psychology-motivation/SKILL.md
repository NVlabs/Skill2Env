---
name: s4h-psychology-motivation
description: "Diagnose what's actually driving behavior — the person's own, someone else's, or a group's. Surface motivation vs. root motivation. Triggers: 'what motivates them', 'why are they doing this', 'what does this person actually want', 'how do I get buy-in', 'why won't they engage', 'what's really driving this', 'intrinsic vs extrinsic motivation', 'what need is this serving'."
---

# Psychology: Motivation

Surface explanations for behavior are almost always incomplete. When someone says they want more money, they may actually want to feel competent and respected. When someone resists a change, they may be protecting a sense of autonomy, not opposing the specific idea. When someone keeps doing something self-defeating, an unmet need is usually doing the driving. Getting the motivation right is the prerequisite for any meaningful influence, leadership, design, or change.

---

## Your Process

**Step 1: Observe the Behavior**
Describe the actual behavior, not the interpretation. "Keeps missing deadlines" rather than "doesn't care about quality." "Pushes back on every new initiative" rather than "resistant to change." The behavior is the data; the motivation is the hypothesis.

**Framing check:** Confirm the specific person or group and the behavior being analyzed before continuing. State what you've identified — the actual subject, the behavior observed, and the context — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of who is doing what, in what context]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Name the Surface Motivation**
What's the stated reason, or the most obvious explanation? This is the first layer — what the person says they want, or what seems to be driving them at face value. Surface motivations are real, but they're rarely the full picture. Capture them clearly before going deeper.

**Step 3: Probe for the Root Motivation**
Apply three diagnostic lenses:

**Self-Determination Theory (SDT):** People have three fundamental psychological needs. Behavior is often a strategy for meeting one of these:
- **Autonomy** — the need to feel that one's actions are self-chosen and self-directed. Unmet: behavior feels controlled, micromanaged, or overridden. Strategy: resistance, disengagement, or surface compliance with private resentment.
- **Competence** — the need to feel effective and capable. Unmet: tasks feel too hard, too easy, or outcomes feel disconnected from effort. Strategy: avoidance, perfectionism, or seeking tasks where competence is assured.
- **Relatedness** — the need to feel connected to and valued by others. Unmet: person feels isolated, unseen, or like they're performing for an indifferent audience. Strategy: people-pleasing, conflict avoidance, or withdrawal.

**Maslow as a Diagnostic:** Not a rigid hierarchy, but a useful scan: is a lower-order need currently unmet that's dominating attention? Security threats (job uncertainty, financial stress) crowd out growth. Belonging threats crowd out esteem. If the answer to "what need is unmet?" is at the safety or belonging level, the solution is rarely a performance or incentive change.

**Identity Dimension:** People behave in ways consistent with how they see themselves. "I am the kind of person who..." shapes behavior more powerfully than incentives in many contexts. The question: is the person acting to protect or affirm an identity? Is the proposed change threatening their self-concept? ("Asking me to do X is saying I'm not the kind of person I believe I am.")

**Step 4: Identify What's Actually Needed for Sustained Engagement**
Having diagnosed the root motivation, ask: what does this person or group actually need for sustained, genuine engagement — not compliance, not short-term performance, but real motivation? This is the intervention target.

The gap between surface and root motivation is where most management, persuasion, and design fails. Giving people more of what they say they want (money, promotion, recognition) often doesn't move the needle if the root need (autonomy, competence, belonging) is what's actually unmet.

**Step 5: Identify the Lever**
What's the specific thing that addresses the root motivation? Not "make them feel more autonomous" (too vague) but "give them ownership of the technical architecture decision within defined constraints." Not "improve belonging" but "include them in the stakeholder briefing so their perspective shapes the outcome."

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full diagnostic** — All steps, reasoning shown throughout
  - **Root motivation only** — Skip surface; go straight to what's really driving this
  - **Lever only** — I already have the diagnosis; what's the specific lever?
  - **Refine the behavior** — Clarify what behavior we're analyzing before starting

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

---

## Output Format

### Behavior Observed
[Specific behavior, not interpretation]

### Surface Motivation
[What the person says they want, or the obvious explanation]

### Root Motivation
**SDT lens:** [Which need — autonomy, competence, or relatedness — is most live here, and how]
**Maslow scan:** [Is a lower-order need crowding out everything else? If so, which one]
**Identity dimension:** [Is a self-concept at stake? What is it]

### What's Actually Needed
[What this person/group actually requires for sustained engagement — the real target]

### The Lever
[Specific, concrete action that addresses the root motivation]

---

## Notes

Motivation diagnosis is probabilistic, not certain. You're building a model of someone's inner state from external behavior, which is inherently incomplete. Hold the diagnosis as a working hypothesis, test it through conversation or experiment, and revise it when the behavior doesn't respond as predicted.

Motivation and emotion are related but distinct. Motivation is about what drives behavior toward goals; emotion is about the feeling states shaping experience. When the question is about how someone *feels* rather than what's *driving* them, use psychology-emotional or emotional-motivation-mapping.

Do not conflate motivation with incentives. Incentives work on surface motivation (more pay = more output) in narrow conditions. Root motivation is structural and requires structural responses. Adding incentive on top of an autonomy or belonging deficit often makes things worse (overjustification effect: external reward can crowd out intrinsic motivation that was already present).

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Motivation analysed. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-emotional-motivation-mapping` — Map motivations in their emotional and relational context
  - `/s4h-social-incentive-analysis` — Align incentives with the motivations found
  - `/s4h-communication-audience-modeling` — Model the audience through their motivations
  - **Done** — Wrap up and synthesise what we have so far
