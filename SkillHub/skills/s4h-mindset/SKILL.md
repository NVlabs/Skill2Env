---
name: s4h-mindset
description: "Entry point for the mindset toolkit. Routes to the right mindset skill based on your situation. Use when you say 'mindset', 'change my perspective', 'I keep thinking about this the wrong way', 'help me deal with what I can't control', 'I want to flourish more', 'I keep treating failure personally', 'I'm stuck in a negative thought loop', 'I can't focus', 'I want to get into flow', or any request for a philosophical or psychological orientation shift."
---

# Mindset

Applies deep philosophy-grade thinking orientations to life, work, and challenge. Diagnoses what kind of mindset work is needed and routes to the right tool — whether that's learning to distinguish what's in your control, building genuine flourishing, shifting how you relate to failure, restructuring a thought distortion, or designing conditions for optimal experience.

## Which tool fits

| You need to... | Tool |
|---|---|
| Deal with what you can't control; stop worrying about outcomes; find equanimity | mindset-stoic |
| Build more flourishing and wellbeing; understand what's missing in your life | mindset-positive |
| Stop treating failure like it means something about you; develop in areas you find hard | mindset-growth |
| Get out of a negative thought loop; generate more accurate interpretations | mindset-reframe |
| Get into deep focus and flow; design conditions for optimal experience | mindset-flow |

## Routing Decision

**Framing check:** Confirm the specific situation before diagnosing. State what you've identified — the actual mindset challenge and its emotional or behavioural context — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific mindset challenge and context]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

- **"I keep worrying about outcomes / things I can't control"** → mindset-stoic (the dichotomy of control is the entry point)
- **"I'm not thriving / I want more wellbeing / something feels missing"** → mindset-positive (PERMA diagnosis)
- **"I keep treating failure like it means something about me"** / **"I hate not being good at things yet"** → mindset-growth (fixed-mindset trigger identification)
- **"I'm stuck in a negative thought loop"** / **"I keep interpreting this the worst way"** / **"I can't stop catastrophizing"** → mindset-reframe (cognitive distortion mapping)
- **"I can't focus"** / **"I want to get into deep work"** / **"I used to experience flow and don't anymore"** → mindset-flow (flow channel diagnosis)
- **Unclear** → mindset-reframe (starts with the thought, which surfaces which deeper orientation is needed)

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

## Stoic

*The full Stoic toolkit: identify what's in your control, apply the right practice, reframe from first principles.*

The Stoic tradition — Marcus Aurelius, Epictetus, Seneca — offers the most developed framework for distinguishing what is "up to us" (judgments, desires, actions) from what is not (body, reputation, outcomes, others). The skill encodes four core practices: negative visualization, amor fati, memento mori, and the view from above. Process: identify the situation → isolate what is and isn't in your control → apply the relevant practice → articulate the Stoic reframe.

---

## Positive Psychology

*Diagnose which dimension of flourishing is underdeveloped and apply the right evidence-based intervention.*

Based on Seligman's PERMA model (Positive emotion, Engagement, Relationships, Meaning, Accomplishment) and the broaden-and-build theory of positive emotions. Distinguishes genuine flourishing from toxic positivity. Process: PERMA audit → diagnosis → targeted intervention for the underdeveloped dimension.

---

## Growth Mindset

*Identify the fixed-mindset trigger, surface the hidden belief, and design the learning response.*

Based on Carol Dweck's research — the actual mechanics, not the pop version. Fixed mindset treats abilities as fixed traits; growth mindset treats them as developable capacities. Process: identify the fixed-mindset trigger (challenge, failure, comparison) → surface the hidden fixed-mindset belief → reframe through the growth lens → design a concrete learning response.

---

## Reframe

*Map the cognitive distortion and generate a more accurate interpretation.*

Based on CBT cognitive restructuring. The cognitive triangle: thoughts → feelings → behaviors. Core process: identify the automatic thought → examine evidence for and against → name the cognitive distortion → generate an alternative interpretation equally consistent with the facts but more useful. Not about forced positivity — about accuracy.

---

## Flow

*Diagnose why flow isn't occurring and redesign the conditions for optimal experience.*

Based on Csikszentmihalyi's flow framework. Flow requires: clear goals, immediate feedback, and challenge/skill balance. Process: identify the target activity → audit what's blocking flow (wrong challenge/skill ratio? absent feedback? unclear goals? interruptions?) → redesign the conditions → enter the flow channel.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Mindset work complete. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-identity-values-clarification` — Connect the mindset shift to your underlying values
  - `/s4h-emotional-motivation-mapping` — Map the motivations connected to the mindset patterns
  - `/s4h-decision-premortem-analysis` — Stress-test decisions with the new mindset applied
  - **Done** — Wrap up and synthesise what we have so far
