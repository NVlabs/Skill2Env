---
name: s4h-play-worst-case-reversal
description: "Deliberately designs the worst possible version — then reverses each failure mode into a design principle. Removes the pressure of being right and unlocks creative honesty that polite brainstorming suppresses. TRIGGERS: 'worst possible idea', 'how would you make this terrible', 'reverse brainstorm', 'design the failure', 'how would you deliberately fail'."
---

# Play: Worst-Case Reversal

Direct brainstorming produces cautious, socially acceptable ideas. Designing the
worst possible version removes the social cost of being wrong and unlocks the honest
list of everything that actually fails — which, when reversed, becomes the most direct
path to the design requirements that matter. The technique works because the
worst-possible list is easy: everyone knows how to fail. The reversals do the serious
work.

---

## Your Process

**Step 1: State the Design Challenge**
What are you designing, building, or solving? Be specific about the intended outcome
— what would success look like if it worked?

**Framing check:** Confirm the specific design challenge before continuing. State what you've identified — the actual thing being designed and what success looks like — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the design challenge and its intended outcome]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different challenge than read; incorporate the correction before proceeding

**Step 2: Design the Worst Version**
Ask: how would you make this as bad as possible? What would guarantee failure,
alienate users, destroy trust, waste resources, or produce the exact opposite of the
intended outcome? Generate without filter or politeness. Aim for 8-12 specific ways
to make it terrible.

Rules for this step:
- No self-censorship. The worse the better.
- Be specific, not vague. "Make users wait 10 minutes" not "be slow." "Never
  acknowledge errors" not "have bad error handling."
- Include the uncomfortable ones — the ones that reveal real tensions, ignored
  trade-offs, or problems the current design is quietly making. These are the most
  valuable entries.
- If it feels too harsh to say, say it. Those are usually the ones that generate
  the most useful reversals.

**Step 3: Reverse Each Failure Mode**
For each terrible idea, state the affirmative inverse as a design principle. The
reversal should be specific and actionable, not generic. "Make users re-enter the
same information three times" → "Eliminate all redundant data entry; information
provided once should propagate automatically." "Never tell users what went wrong"
→ "Every failure state names what happened and what to do next."

**Step 4: Collect as Design Requirements**
The reversed principles are design requirements. State them as a clean list,
affirmatively, in present tense. These are things the design must do.

**Step 5: Audit Against the Existing Design**
Which requirements were already present and strong? Which were present but weak or
inconsistent? Which were missing entirely? The missing ones — requirements that never
appeared in the direct design process — are the primary output.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Reversal list only** — The failure modes and their direct inverses, skip elaboration
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Challenge:** [what you're designing and what success looks like]

**Worst-Possible List + Reversals**

| Terrible Idea | Reversed Design Principle |
|---|---|
| [specific failure mode — concrete and unfiltered] | [affirmative design requirement] |

**Design Requirements Derived:** [clean numbered list of all reversed principles]

**Audit Against Existing Design**
- Already present and strong: [list]
- Present but weak or inconsistent: [list — these need tightening]
- Missing entirely: [list — these are the highest priority findings]

---

## Notes

The uncomfortable entries in the worst-possible list are the most valuable — they
surface real tensions that politeness has kept invisible. If every item on your list
feels obvious and safe, you haven't gone far enough. Push into the territory where
naming it feels a little risky.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Worst cases reversed. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-decision-premortem-analysis` — Formalise the worst case as a structured premortem
  - `/s4h-constraint-workaround-mapping` — Address the worst cases with concrete workarounds
  - `/s4h-creativity-alternatives` — Generate alternatives that avoid the worst cases
  - **Done** — Wrap up and synthesise what we have so far
