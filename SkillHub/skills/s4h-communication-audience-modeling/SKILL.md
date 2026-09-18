---
name: s4h-communication-audience-modeling
description: "Maps what the audience currently believes, actually cares about, and fears before communicating — because communication fails at the receiver, not the sender. Triggers: 'model the audience', 'audience analysis', 'who am I talking to', 'what do they care about', 'why aren't they getting it'."
---

# Communication Audience Modeling

Communication fails at the receiver. The sender almost always knows what they meant —
the question is what the receiver hears, given what they currently believe, what they
actually care about, and what they are trying to protect. Modeling this before communicating
is the most leverage-bearing preparation step there is.

---

## Your Process

**Step 1: Name the Specific People**
Don't model "the team" or "leadership." Name the individuals or segments who will receive
this message. Different people in the same meeting need different models.

**Framing check:** Confirm the message, the audience, and the goal before continuing. State what you've identified — the specific communication being planned, who it's directed at, and what outcome it needs to achieve — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the message, the audience, and the communication goal]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Current Belief**
What do they already think about this topic? Not what you wish they thought — what they
actually think right now. This is the starting position the message must move from.

**Step 3: Real Goal**
What is their underlying motivation? Stated preferences are often proxies for something
deeper: security, recognition, autonomy, fairness, control. If you're addressing the
stated preference without the underlying motivation, the message won't land.

**Step 4: Fear**
What do they need not to lose? Fear is more motivating than ambition for most people in
most professional contexts. A message that threatens something they're protecting will be
rejected even if the logic is sound.

**Step 5: What Would Change Their Mind — and What Won't**
What evidence, framing, or social proof would move them? And what — however well-reasoned
— will not work on this person? Knowing what won't work is as important as knowing what
will.

**Step 6: Threshold Condition**
What must they hear or feel first before they can receive the actual message? Some people
need to feel heard before they can listen. Others need certainty about scope. Others need
a specific concern addressed before anything else can land.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Fears and concerns only** — What the audience is most worried about, skip beliefs and goals
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Audience segments:**

| Person / Segment | Current belief | Real goal | Fear | What moves them | What won't work | Threshold condition |
|-----------------|---------------|-----------|------|-----------------|-----------------|---------------------|
| | | | | | | |
| | | | | | | |

**Message implications:**
> [What must the message do, in what order, to land for each segment?]
> [Where do segments conflict — and how should that tension be resolved?]

**Highest-risk segment:**
> [The person or group most likely to reject the message — and why]

---

## Notes

The threshold condition in Step 6 is the most commonly skipped and most valuable element.
A message that tries to make its main point before meeting the threshold condition will be
filtered out before it arrives.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Audience modelled. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-communication-objection-mapping` — Map the objections this audience will raise
  - `/s4h-communication-clarity-audit` — Audit whether the message is clear to this specific audience
  - `/s4h-writing-tone-alignment` — Align tone to the audience model
  - **Done** — Wrap up and synthesise what we have so far
