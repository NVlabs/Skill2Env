---
name: s4h-design-user-needs
description: "Distinguishes real needs from stated wants — uses jobs-to-be-done and latent need mapping to find what actually matters. Triggers: 'what do users actually need', 'jobs to be done', 'understand the user', 'find the real need', 'stated want versus actual need', 'user research', 'what problem are we solving'."
---

# Design: User Needs

The most common design failure is building the wrong thing well. People don't articulate needs — they articulate solutions. "I want a faster horse," "I need a bigger inbox," "give me more options." These are requests framed as solutions to problems the user hasn't quite stated. A designer who takes them at face value will build a faster horse, a bigger inbox, more options — and miss the underlying need entirely.

Clayton Christensen's jobs-to-be-done framework makes the shift explicit: people don't buy products, they hire them to do a job. Understanding the job — not the product request — is the designer's actual brief. Don Norman extended this with the distinction between stated needs (what people say), observed needs (what people do), and latent needs (what people don't yet know they need but would recognise immediately if you showed them). All three matter. Only one of them is given to you directly.

This skill works through all three levels, using structured inquiry to separate the real need from the stated proxy and surface the design target that actually matters.

---

## Your Process

**Step 1: State the Request**
Write down exactly what was asked for, in the words it was stated. Preserve the phrasing — the precise language reveals how the person is framing the problem.

**Framing check:** Confirm the request and the context in which it arose before continuing. State what you've identified — the stated request and the situation it comes from — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the request and its context]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Decompose the Job**
Apply jobs-to-be-done decomposition. For the stated request, identify:

- **Functional job:** What are they trying to accomplish? What outcome do they need to reach?
- **Emotional job:** How do they want to feel while doing it? How do they want to feel when it's done?
- **Social job:** How do they want to be perceived by others in this context?

All three jobs are real design requirements. Ignoring emotional and social jobs produces functional things people don't use.

**Step 3: Trace the Context**
Map the situation in which this job arises. When does it occur? What triggers it? What has the person tried before? What is the current workaround, and what does that workaround reveal about what they've accepted as good enough? The workaround is a latent needs signal — it shows what people will tolerate, which implies what they'd choose if offered something better.

**Step 4: Separate Stated Want from Real Need**
For each element of the stated request, ask: is this a solution (a specific form) or a need (an outcome)? Solutions can usually be restated as needs. "I want a dashboard" → "I need to see the status of multiple things at once without searching." "I want notifications turned off" → "I need to control when I give attention to requests from others."

Restate every solution-framed element as a need-framed one.

**Step 5: Surface Latent Needs**
Latent needs are not stated because people haven't conceptualised them as possible. They emerge from:
- Asking what frustrates people about the current best option (not about any specific solution)
- Asking what they wish they didn't have to do
- Observing where people add their own workarounds and shortcuts
- Asking "what would make this ten times better?" — people rarely ask for the obvious; they imagine what hasn't been built yet

List candidate latent needs. Mark confidence level for each.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is the design context and what job category is most important here — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Jobs focus** — Decompose the functional/emotional/social jobs in depth, skip latent needs
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Stated request:**
> [Exact wording]

**Jobs-to-be-done:**

| Job type | Description |
|---|---|
| Functional | [What they're trying to accomplish] |
| Emotional | [How they want to feel] |
| Social | [How they want to be perceived] |

**Current workaround and what it reveals:**
[Describe the workaround. What it implies about accepted tolerances and unmet needs.]

**Stated want → Real need:**

| Stated as (solution) | Restated as (need) |
|---|---|
| [Solution framing] | [Need framing] |

**Latent needs:**
- [Need] — *confidence: high/medium/speculative*

**Design target:**
> [The core need, stated precisely. One to two sentences. This is what design should solve against.]

---

## Notes

The most common mistake here is conflating the emotional job with sentiment — "they want to feel happy." The emotional job is more specific: they want to feel in control, competent, not embarrassed, trusted, efficient. These are designable. Vague emotional goals aren't.

This skill pairs naturally with `/s4h-design-constraints` — once the real need is stated, the next question is what constraints define the solution space. It also precedes `/s4h-design-iteration`, which structures the testing loop once a design direction exists. For broader audience analysis — who is this for, and how do different groups differ — see `/s4h-communication-audience-modeling`.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Needs mapped. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-design-constraints` — Map the constraints that define what solutions are actually possible
  - `/s4h-design-iteration` — Structure the cycle of prototyping and testing against these needs
  - `/s4h-creativity-brainstorm` — Generate solution directions now that the real need is clear
  - **Done** — Wrap up and synthesise what we have so far
