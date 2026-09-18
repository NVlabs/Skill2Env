---
name: s4h-psychology-behavior-change
description: "Diagnose what's maintaining an entrenched behavior and design the right intervention to shift it. Covers habits, routines, and behavioral defaults. Triggers: 'how do I change this behavior', 'why does this habit persist', 'how do I make this stick', 'behavior change', 'breaking a habit', 'building a habit', 'why can't I stop doing X', 'how do I get people to consistently do Y', 'implementation intentions', 'habit loop'."
---

# Psychology: Behavior Change

Behavior is not driven primarily by intention. A person can fully intend to exercise, stop checking their phone, or give direct feedback — and consistently fail to do so. The intention-behavior gap is real and large. It exists because behavior is maintained by systems: habit loops, environmental cues, identity commitments, friction levels, and social norms. Changing behavior requires diagnosing which of these systems is doing the work, then intervening at the right level. Motivational exhortation without system change produces guilt, not results.

---

## Your Process

**Step 1: Specify the Behavior**
Be precise. Not "be healthier" but "go for a 30-minute walk after work on weekdays." Not "be a better communicator" but "give direct negative feedback in the weekly 1:1 rather than softening it into ambiguity." Vague behavior targets produce vague interventions.

Also specify: are you trying to **stop** a behavior, **start** a behavior, or **modify** (frequency, intensity, consistency) a behavior? These have different intervention profiles.

**Framing check:** Confirm the specific behavior before continuing. State what you've identified — the exact behavior and whether the goal is to start, stop, or modify it — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific behavior and direction]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Diagnose What's Maintaining the Current Behavior**
Most behavioral persistence has a cause. Identify which mechanism is doing the work:

**Habit loop (Cue → Routine → Reward):**
Is the behavior automatic — triggered by a cue without deliberate decision? If yes, the habit loop is the primary mechanism. The cue activates the routine; the routine delivers a reward (often neurological, often faster than the negative consequence). To change it: identify the cue, design a competing routine that delivers the same (or better) reward, and repeat until the new loop is automatic.

**Motivation deficit:**
Is the behavior driven by lack of sufficient want? Is the person (or group) aware the behavior needs to change but not sufficiently moved to change it? Distinguish between *not knowing what to do* (capability gap) and *not wanting to enough* (motivation gap). Motivation-based approaches: connect the behavior to deep values, identity, or meaningful outcomes. Surface vs. root distinction from psychology-motivation applies here.

**Capability gap:**
Does the person not know how, lack a skill, or lack confidence in their ability to execute? Motivation is present; the behavior fails because execution is broken. Intervention: skill building, scaffolding, or breaking the behavior into smaller executable steps (tiny habits).

**Friction:**
Is the behavior failing because it's just hard enough to be skipped when willpower is low? The environment is doing the behavioral work. To start a behavior: reduce friction to near zero (lay out the gym clothes the night before). To stop a behavior: add friction (delete the app, log out, require a second device).

**Identity conflict:**
Does the behavior conflict with how the person sees themselves? "I'm not the kind of person who gives harsh feedback." "I'm not an exerciser." Identity-based change addresses this directly: the goal is not to do the behavior but to become the person who does it. Each small action is a vote for that identity. Particularly powerful for long-term sustained change (Atomic Habits framework).

**Social norm:**
Is the current behavior maintained by what the surrounding group does? Social norms exert constant, mostly invisible pressure. If the environment normalizes the behavior you're trying to eliminate, individual change is fighting an uphill battle. Intervention: change who the person is around during the relevant context, or change the group norm.

**Step 3: Select the Right Intervention Type**

| Maintaining mechanism | Right intervention |
|----------------------|-------------------|
| Habit loop | Cue identification → competing routine → reward alignment |
| Motivation deficit | Connect to identity, values, or meaningful outcomes |
| Capability gap | Skill training, scaffolding, or micro-habit decomposition |
| Friction | Environment design — reduce friction to start, add friction to stop |
| Identity conflict | Identity reframing — small votes for the new identity |
| Social norm | Change context or norm; social commitments and accountability |

Multiple mechanisms often co-occur. **Before narrowing:** Show the complete set of mechanisms identified to the user first. Use `AskUserQuestion`:
- **Question:** "I've identified [N] maintaining mechanisms. Before I select the primary one to address, are there any you'd flag as especially important, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific mechanism to prioritise
  - **Add a missing one** — user will describe it

Then prioritize: which one, if addressed, would unblock the rest?

**Step 4: Design the Implementation**

**Implementation intentions** — The most robust single intervention for intention-behavior gaps. Format: "When [situation X] occurs, I will do [behavior Y]." This pre-loads the response so it executes automatically. Not "I'll exercise more" but "When I close my laptop at 5:30pm, I will immediately put on my running shoes." The specificity does the work.

**Habit stacking** — Attach the new behavior to an existing anchor behavior. "After I pour my morning coffee, I will review the three priorities for the day." The existing behavior provides the cue.

**Environment design** — Change the context so the behavior is the path of least resistance. Default settings, proximity, and visibility all shape behavior without requiring willpower.

**Tiny habits** — Start with a version of the behavior so small it feels trivially easy. The goal is to establish the pattern and the identity, not to produce results immediately. Two minutes of reading is not the destination; it's the anchor for the habit.

**Identity-based framing** — Reframe the intervention from outcome to identity. Not "I want to lose weight" but "I'm becoming someone who takes care of their body." Each successful action is evidence for the identity; each failure is noise, not signal.

**Step 5: Address Relapse**
All behavior change involves setbacks. Design the relapse response in advance: what happens the first time the new behavior fails? The "never miss twice" rule (James Clear): one miss is an accident; two is the start of a new habit. Pre-commit to the recovery response.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full diagnosis + intervention design** — All steps, full output with specific implementation plan
  - **Diagnosis only** — Just identify what's maintaining the behavior; I'll design the intervention
  - **Intervention design** — I already know the maintaining mechanism; design the implementation
  - **Refine the behavior** — Clarify what behavior we're targeting before starting

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

---

## Output Format

### Target Behavior
**[Specific behavior to start/stop/modify]**
**Direction:** [Start / Stop / Modify — and what the target state looks like]

### Maintenance Diagnosis
**Primary mechanism:** [Habit loop / Motivation deficit / Capability gap / Friction / Identity conflict / Social norm]
**How it's operating:** [Specific explanation for this situation]
**Secondary mechanisms:** [Any co-occurring factors]

### Intervention Design
**Primary intervention:** [Type and rationale]
**Implementation intention:** "When [X], I will [Y]."
**Environment change:** [What to add, remove, or restructure in the context]
**Identity framing:** [How to frame this as identity, if applicable]
**Relapse plan:** [What happens when the behavior lapses — specifically]

### First Week
[The concrete, specific actions for the first seven days — not "work toward the behavior" but exactly what to do, when, and in what context]

---

## Notes

Willpower is not the primary lever. Willpower is a finite resource that depletes over the day, degrades under stress, and is an unreliable foundation for sustained behavior change. Environment design, habit loops, and identity reframing are more reliable because they don't require willpower to maintain.

Use psychology-persuasion when the primary obstacle is that someone doesn't believe the behavior change is worth making — belief and attitude need to shift before behavior targeting makes sense. Use psychology-motivation when you need to diagnose why a person isn't motivated to change before designing the intervention. Behavior change often requires motivation diagnosis as a precursor: it's hard to design the right implementation if you don't know what need the current behavior is serving.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Behaviour change approach mapped. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-social-incentive-analysis` — Align incentives with the behaviour change strategy
  - `/s4h-communication-audience-modeling` — Model the audience through the behaviour change lens
  - `/s4h-ethics-consent-review` — Check consent and ethical bounds of the approach
  - **Done** — Wrap up and synthesise what we have so far
