---
name: s4h-psychology-persuasion
description: "Identify the right influence approach and construct it for the context. What actually changes minds and drives action. Triggers: 'how do I persuade', 'how do I change their mind', 'what would convince them', 'how do I get buy-in', 'how do I influence', 'influence strategy', 'how do I pitch this', 'what makes a persuasive case', 'how do I get them to say yes'."
---

# Psychology: Persuasion

Persuasion fails most often not because the argument is wrong, but because the wrong approach was chosen for the audience and context. A perfectly valid argument presented to someone processing peripherally (low engagement, low stakes in their view) will be ignored. A reciprocity move used with someone who values direct confrontation will backfire. The right influence approach depends on where the audience is, what they need to feel before they can update, and what constraints exist on the relationship. The first question is not "what's my argument?" — it's "who is this person, and what will actually move them?"

---

## Your Process

**Step 1: Define What You're Trying to Change**
Be precise. Are you trying to change:
- A **belief** (they think X is false; you want them to think it's true)
- An **attitude** (they're indifferent to or opposed to X; you want them to value it)
- A **decision** (they're leaning toward A; you want them to choose B)
- A **behavior** (they currently do/don't do X; you want them to do/not do X)

The answer shapes everything else. Belief change requires evidence and trust. Attitude change often requires social proof and identity alignment. Behavior change may be achievable without attitude change through friction design and environment.

**Framing check:** Confirm the specific persuasion situation before continuing. State what you've identified — the change target type, the audience, and the goal — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the change target, who you're trying to persuade, and what you want them to believe, decide, or do]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Profile the Audience**
Assess:
- **Motivation to process:** Are they engaged and motivated to think carefully about this? Or will they process peripherally?
- **Capability:** Do they have the background to evaluate the argument on its merits?
- **Prior position:** Are they opposed, neutral, or already leaning your way?
- **Relationship:** Are you a trusted insider, a neutral outsider, or a known advocate with a stake?
- **What they value:** What does success look like in their world? What fears dominate?

**Step 3: Select the Influence Approach**

**Elaboration Likelihood Model (ELM):**
- **Central route** — When the audience is motivated and capable of processing, a well-constructed argument is the primary lever. Substance matters; logic matters; evidence matters. Don't shortcut to peripheral cues when you can win on the merits.
- **Peripheral route** — When the audience is processing shallowly (low stakes for them, high cognitive load, or low motivation), peripheral cues drive judgment: the credibility of the source, the confidence with which it's presented, the number of arguments (not their quality), social proof. This is not manipulation if applied ethically; it's meeting people where they are.

**Cialdini's Six Principles:**
Deploy these as targeted interventions, not as tricks. Each addresses a real psychological need:
- **Reciprocity** — People repay what they've received. Give something of genuine value before asking. Works in relationships with ongoing exchange; feels manipulative when the gift is obviously instrumental.
- **Commitment and consistency** — People follow through on what they've publicly committed to. Get a small commitment aligned with the larger ask. Works best in cultures that value consistency; weaker where flexibility is valued over reliability.
- **Social proof** — People look to others' behavior when uncertain. Show who else has made this choice, especially peers the audience identifies with. Most powerful when uncertainty is high and the reference group is credible.
- **Authority** — People defer to credible experts. Establish relevant expertise (yours or via endorsement) early. Works when expertise is genuine and recognized; backfires when it's asserted without evidence.
- **Liking** — People are more persuaded by people they like. Similarity, genuine interest, and warmth create liking. Not about being ingratiating — about creating real rapport.
- **Scarcity** — People value what is rare or diminishing. Genuine scarcity (this offer actually expires; this opportunity is genuinely limited) is legitimate. Manufactured scarcity is manipulation.

**Inoculation Theory:**
If the audience will encounter counter-arguments from other sources, pre-emptively acknowledge and refute them (the "weakened dose" approach). This inoculates against persuasion from opposing sources more effectively than waiting for the attack. Particularly useful when: you're presenting to people who will face opposition from other stakeholders; when opposing views are well-known; when you want to harden a position, not just build it.

**Step 4: Identify Ethical Constraints**
Before constructing the approach, check:
- Are you exploiting a bias rather than appealing to a genuine need? (Manufactured scarcity, false social proof)
- Would the audience object if they could see the full influence strategy you're using?
- Is the thing you're persuading them toward actually in their interest?

Ethical persuasion works with the audience's judgment, not against it. Manipulation bypasses judgment. The test: would you be comfortable if the person understood the full approach you're using? If not, redesign.

**Step 5: Construct the Approach**
Build the specific message or sequence. For a central-route argument: premises, evidence, conclusion, pre-emptive objection handling. For a peripheral-route approach: identify the cue, establish it, sequence it before the ask. For Cialdini principles: identify the specific implementation for this context and this relationship.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis + constructed approach** — Audience profile, influence selection, ethical check, and built-out message
  - **Influence selection only** — Tell me which approach fits this situation and why
  - **Construct the message** — I've already identified the approach; help me build it out
  - **Refine the situation** — Clarify the audience or the goal before starting

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

---

## Output Format

### Change Target
**[Belief / Attitude / Decision / Behavior]** — [Specific statement of what you're trying to change]

### Audience Profile
- **Motivation to process:** [High / Low / Unknown]
- **Prior position:** [Opposed / Neutral / Leaning your way]
- **Relationship:** [Trusted insider / Neutral / Known advocate]
- **What they value:** [Key values and concerns]

### Recommended Approach
**Primary lever:** [ELM route or Cialdini principle(s)]
**Why it fits:** [One paragraph connecting the approach to this audience and target]
**Inoculation:** [Whether to pre-emptively address counter-arguments, and which ones]

### Ethical Assessment
**[Clear / Concerns]** — [If concerns: what they are and how to address them]

### Constructed Approach
[The actual message, sequence, or script — specific enough to use]

---

## Notes

Persuasion and manipulation share tools but differ in ethics. The distinction is: persuasion respects the audience's autonomy and judgment; manipulation bypasses it. Using social proof to show someone that their respected peers have made a choice is persuasion. Manufacturing fake social proof is manipulation. Using scarcity when there is genuine scarcity is persuasion. Inventing false urgency is manipulation. The line is real, and it matters.

Use psychology-behavior-change when the goal is to shift entrenched behavior that doesn't primarily require changing a mind (habits, routines, and defaults are better targeted with environment design than argument). Use psychology-motivation when you need to understand what someone actually wants before constructing your influence approach — motivation diagnosis often precedes persuasion design.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Persuasion approach mapped. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-communication-objection-mapping` — Map objections the persuasion must address
  - `/s4h-ethics-consent-review` — Check the ethical bounds of the persuasion approach
  - `/s4h-writing-argument` — Build the persuasive argument from the findings
  - **Done** — Wrap up and synthesise what we have so far
