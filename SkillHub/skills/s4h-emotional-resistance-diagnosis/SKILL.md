---
name: s4h-emotional-resistance-diagnosis
description: "Diagnoses why people are resisting — finding what's underneath the pushback. Resistance is information, not obstruction; it always has a source. TRIGGERS: 'why are they resisting', 'diagnose the pushback', 'they won't get on board', 'people aren't buying in', 'resistance diagnosis'."
---

# Emotional Resistance Diagnosis

Resistance is not a problem to overcome — it is a signal to decode. People resist for
different reasons, and applying the wrong response to the wrong type makes it worse.
Presenting more data to someone who is emotionally resistant does nothing. Acknowledging
feelings with someone who has an intellectual objection is patronising. This skill
identifies the source before prescribing the response.

---

## Your Process

**Step 1: Describe the Resistance**
Who is resisting, what are they saying explicitly, and how are they behaving?
Get behaviorally specific — passive non-compliance, vocal objection, questions
designed to slow things down, and political manoeuvring are different signals
pointing to different sources.

**Framing check:** Confirm the specific resistance situation before continuing. State who is resisting, what they appear to be resisting, and in what context, in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of who is resisting, what they're resisting, and in what context]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Classify Each Instance**
Assign each type of resistance to one or more of these categories:
- **Intellectual** — they disagree with the reasoning, evidence, or conclusion.
  They think you're wrong.
- **Emotional** — they feel something important to them is at risk. They may not
  be able to articulate what, but something feels threatening.
- **Political** — a competing interest is served by the current state. Changing
  things costs them something real.
- **Practical** — they don't believe the plan can actually work. They've seen
  similar things tried and fail.

**Step 3: Source of Each Type**
Dig to the specific source. Intellectual: which claim do they reject, and why?
Emotional: what are they afraid of losing — status, security, relationships,
credit? Political: whose interests benefit from the status quo, and how do they
intersect with this person? Practical: what specifically do they believe will
fail, and what informs that belief?

**Step 4: What Are They Legitimately Protecting?**
Most resistance protects something real — a working system, a relationship, a
principle, an investment of time and reputation. Name it explicitly. Even if their
expression of resistance is unhelpful, the thing they're protecting may be
legitimate. Dismissing this hardens resistance into permanent opposition.

**Step 5: What Would Reduce Each Type?**
Each type has a different lever. Intellectual resistance needs evidence, logic,
or acknowledgment that their counter-argument was considered. Emotional needs
acknowledgment of the risk they feel and credible reassurance. Political needs
negotiation or incentive realignment. Practical needs proof of concept or a staged
rollout that limits downside.

**Step 6: Engagement vs Clarity**
Some resistance requires genuine engagement — changing the plan, negotiating
trade-offs, addressing real concerns with merit. Some requires clarity — the plan
isn't actually what they think it is, and better communication resolves it.
Distinguish these before acting.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Resistance source only** — What's actually causing the resistance, skip the implications
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Resistance Diagnosis**

| Resistance | Type | Source | What They're Legitimately Protecting | What Reduces It | Engage or Clarify? |
|---|---|---|---|---|---|
| [description] | [type] | [root cause] | [legitimate interest] | [lever] | [engage/clarify] |

**Engagement Priority**
Which resistance requires the most substantive response first, and why. Name the
one thing that, if addressed well, would most shift the overall dynamic.

---

## Notes

The worst response to resistance is to push harder. The best is to correctly
classify it first — then respond to the actual type. Treating emotional resistance
as intellectual (presenting more data) is a common and costly mistake. Treating
political resistance as emotional (offering reassurance) is equally ineffective.
Classification is the work.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Resistance diagnosed. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-emotional-trust-audit` — Assess whether trust issues are fuelling the resistance
  - `/s4h-communication-objection-mapping` — Map objections rooted in the resistance
  - `/s4h-strategy-alliance` — Build alliances to reduce or bypass the resistance
  - **Done** — Wrap up and synthesise what we have so far
