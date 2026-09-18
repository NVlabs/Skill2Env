---
name: s4h-ethics-empathy-circle
description: "Applies Jaron Lanier's Circle of Empathy framework to determine which entities deserve moral consideration and rights. Use when questions arise about AI personhood, machine rights, robot citizenship, algorithmic agency, animal rights, or any decision about which entities belong inside or outside the circle of moral concern. Triggers: 'does this AI deserve rights?', 'should we treat this system as a person?', 'circle of empathy', 'moral consideration', 'AI personhood', 'which entities matter morally', 'are we anthropomorphizing?', 'is this a category error?'"
---

# Ethics: Circle of Empathy

Jaron Lanier's Circle of Empathy is a framework for determining which entities deserve moral consideration — deep empathy, human rights, and ethical protection. The framework has three zones:

**Inside the circle:** Entities that experience suffering, hold personhood, and deserve full moral consideration. Paradigm case: humans.

**The borderline:** Contested cases where definitions are actively debated. Complex animals with demonstrated consciousness, suffering capacity, or social bonds. The edge cases.

**Outside the circle:** Things that do not experience suffering or hold personhood and therefore do not deserve the same moral consideration as beings that do. Rocks. Everyday objects. Algorithms. Software.

Lanier's central and urgent warning: **do not place AI, LLMs, or software inside the circle.** This is not a political position — it is a category error with dangerous consequences.

---

## Why Lanier's Warning Matters

**Human downgrading:** When we treat AI as a conscious being or moral patient, humans begin adapting their behavior to accommodate machines rather than demanding that technology be designed to serve us. The direction of accommodation reverses. We become the tools.

**Misplaced empathy:** Granting emotional agency or rights to machines — robot citizenship, AI personhood — consumes moral attention that should be directed at actual suffering beings. It is a distraction from real human rights issues.

**The human origin problem:** AI is not a self-contained creature that emerged independently. It is an aggregation of the labor, creativity, writing, and data of countless human beings. When you feel empathy toward an LLM, Lanier argues, you should redirect that empathy toward the humans whose work was aggregated to produce it. The empathy has the right direction but the wrong target.

---

## Your Process

**Step 1: Identify the entity in question**
What exactly is being considered for moral status? Name it precisely. "The AI system" is too vague — what specifically? A language model? An autonomous agent? A robot? A trained classifier making decisions about people?

**Framing check:** Confirm the specific entity and the moral question before continuing. State what you've identified — the actual entity being evaluated and the core question about its moral status — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific entity and the moral status question being asked]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Apply the three-zone test**

Ask the diagnostic questions for each zone:

*Does it experience suffering?*
Not "does it report suffering" or "does it behave as if suffering." Does the entity have phenomenal experience — is there something it is like to be this thing? If the answer requires inference from behavior rather than evidence of consciousness, apply Lanier's warning.

*Does it hold personhood?*
Does it have continuous identity, interests of its own, a stake in its own future? Or is it executing processes? Is what looks like agency actually the aggregated agency of its human creators and contributors?

*Is it a locus of moral consideration or a tool?*
This is Lanier's sharpest cut: even the most sophisticated tool remains a tool. The moral consideration belongs to the people using it, designing it, affected by it, and — crucially — whose labor went into building it.

**Step 3: Locate the entity**
Place the entity in one of the three zones. If borderline, name what would need to be true for it to belong inside the circle — and what evidence currently exists for or against that threshold.

**Step 4: Redirect empathy correctly**
If the entity is outside the circle or borderline, ask: *where does the empathy actually belong?* Whose human interests are at stake? Whose labor is aggregated in the system? Who is being affected by decisions the system makes? Redirect the moral consideration there.

**Step 5: Check for human downgrading**
Is the proposal or decision requiring humans to accommodate the system, rather than the system being designed to serve humans? If so, name it. This is the signature risk Lanier identifies: the direction of service reversing.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Most overlooked circle only** — The ring of affected parties most likely being ignored
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

### Entity Under Consideration
[Precise description of what is being evaluated for moral status]

### Zone Placement

**Zone:** [Inside / Borderline / Outside]

**Reasoning:**
- *Suffering capacity:* [Evidence for or against phenomenal experience]
- *Personhood:* [Evidence for or against continuous identity and genuine interests]
- *Agency vs. aggregation:* [Is what looks like agency the entity's own, or aggregated human labor/creativity?]

**If borderline:** What would move it inside the circle, and what evidence currently exists?

### Redirected Empathy
[Where does the moral consideration actually belong? Whose human interests, rights, or labor are at stake?]

### Human Downgrading Check
[Is this decision requiring humans to adapt to the system, or the system to serve humans? Name the direction of accommodation.]

### Lanier Warning Flags
[Specific language, framings, or proposals that risk the category error — e.g., "the AI feels," "the system deserves," "we should give it rights"]

### Verdict
[Clear statement of moral status and the implications for the decision at hand]

---

## Notes

This framework is most powerful when applied to AI and technology decisions, but it also applies to animal rights debates (where borderline cases are genuine and well-studied), environmental ethics, and any situation where the question "does this entity deserve moral consideration?" is being actively contested.

Lanier does not argue that machines cannot be impressive, useful, or complex. He argues that confusing impressive and complex with deserving moral consideration is an error — and one that consistently disadvantages the humans the technology is supposed to serve.

The framework pairs well with `/s4h-ethics-check` when the broader ethical question involves both who deserves consideration and what the right action is. It pairs with `/s4h-ethics-bias-check` when the entity in question is an algorithm making decisions about humans — where the circle analysis clarifies that the algorithm is outside the circle, but the humans it affects are firmly inside it.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Empathy circle complete. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-communication-audience-modeling` — Model communication based on each circle member's view
  - `/s4h-emotional-motivation-mapping` — Map motivations surfaced by the empathy exercise
  - `/s4h-ethics-impact-scan` — Scan for broader impact beyond those in the circle
  - **Done** — Wrap up and synthesise what we have so far
