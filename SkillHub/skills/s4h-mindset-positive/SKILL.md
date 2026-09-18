---
name: s4h-mindset-positive
description: "Applies positive psychology as a rigorous practice — not pop-psychology positivity. Use when you want to build flourishing, diagnose what dimension of wellbeing is underdeveloped, understand what makes life feel meaningful or hollow, or identify why you're not thriving despite the absence of obvious problems. Triggers: 'positive psychology', 'flourishing', 'I want to thrive', 'I'm not happy but I don't know why', 'what makes life meaningful', 'I have everything I need but still feel flat', 'wellbeing', 'PERMA'."
---

# Mindset — Positive Psychology

Positive psychology is the scientific study of what makes life worth living — not the absence of disorder, but the presence of flourishing. Martin Seligman's PERMA model identifies five distinct dimensions of wellbeing that are each independently necessary: Positive emotion, Engagement, Relationships, Meaning, and Accomplishment. A life can be deficient on any one of these while fully adequate on the others.

This matters because the interventions for each dimension are different. If your deficit is meaning, more positive emotion won't fix it. If your deficit is engagement, more accomplishment won't fill the gap. Rigorous positive psychology starts with diagnosis.

---

## Your Process

**Step 1: PERMA Audit**
Evaluate each dimension honestly on a 1–10 scale and provide the evidence for that rating.

**Framing check:** Confirm the specific wellbeing situation before continuing. State what you've identified — the person's situation, the dimension(s) they've flagged (if any), and what kind of output they're seeking — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the situation and what they want to understand or improve]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

*Positive Emotion (P):*
The frequency and quality of positive emotional experiences — not just happiness, but the full range: joy, gratitude, serenity, interest, hope, pride, awe, love. Barbara Fredrickson's broaden-and-build theory shows that positive emotions do something distinctive: they broaden momentary thought-action repertoires and build lasting personal resources (psychological, physical, social, intellectual). They are not just pleasant — they compound. A low score here means not that the person is depressed but that the soil isn't being cultivated.

*Engagement (E):*
Flow experiences — complete absorption in challenging activity where action and awareness merge. Time distorts. Self-consciousness drops. This is not the same as enjoyment (you can be engaged in something difficult and exhausting). The key predictor: challenge/skill balance. Engagement is low when activities are either too easy (boredom) or too hard (anxiety). It requires activities matched to the growing edge of one's capabilities.

*Relationships (R):*
Not quantity of social contact but quality of connection — feeling genuinely known, caring about others' wellbeing, having people you would call at 2am. Seligman and others have found this to be among the most robust predictors of wellbeing. Loneliness is not the same as being alone; connection is not the same as being surrounded.

*Meaning (M):*
Belonging to and serving something you believe is bigger than yourself. Religion, political movements, family, profession, causes — the specific vehicle matters far less than the sense that one's existence is in service of something beyond it. Viktor Frankl, whose work prefigured Seligman's, wrote from inside the Nazi camps: *"He who has a why to live can bear almost any how."*

*Accomplishment (A):*
Pursuing achievement for its own sake — not because it produces positive emotion (often it doesn't, in the moment) but because the pursuit of mastery and completion is itself a component of a full life. Distinct from Engagement: you can accomplish without being engaged (dull but necessary work you finish), and be engaged without accomplishing (flow in an activity that produces nothing).

**Step 2: Identify the Deficit**
**Before narrowing:** Show all five PERMA ratings to the user first. Use `AskUserQuestion`:
- **Question:** "I've rated all five dimensions. Before I identify the primary deficit, are there any you'd flag as especially important, or any where the score doesn't feel accurate?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the ratings look right
  - **Flag one** — user will name a specific dimension to prioritise
  - **Adjust a rating** — user will correct a score that doesn't feel right

Which dimension(s) scored lowest? Are there dimensions at adequate levels that are masking genuine deficits in others?

*Common patterns:*
- High A, low P — accomplishment without savoring; the hedonic treadmill in full operation
- High R, low M — rich relationships but sense of purposelessness
- High P, low E — pleasure without absorption; entertainment rather than engagement
- High M, low A — rich sense of purpose with no execution; frustration
- Low R across a high life — the loneliness that hides behind a busy exterior

**Step 3: Distinguish Genuine Positive Psychology from Toxic Positivity**
Toxic positivity suppresses negative emotion and insists on positive framing in ways that invalidate real experience, prevent processing, and ultimately worsen wellbeing. Genuine positive psychology does not ask you to feel good about bad things. It builds resources and conditions that make flourishing possible — and it treats negative emotions as carrying information, not as failures.

Test: is the intervention asking the person to *suppress or reframe* a negative emotion, or to *build capacity* in an underdeveloped dimension? The former is toxic positivity. The latter is the practice.

**Step 4: Apply the Right Intervention**
For each underdeveloped dimension, apply a targeted evidence-based intervention:

*Low Positive Emotion:*
- Savoring practices: deliberate attention to positive experiences as they occur, or after (three good things; gratitude journaling focused on specifics rather than generalities)
- Fredrickson's positivity ratio is a rough guide: sustained flourishing is associated with a ratio of positive to negative emotional experiences around 3:1 — but this is a diagnostic, not a prescription
- Cultivate awe specifically: it is among the most potent positive emotions and is chronically under-generated in modern life

*Low Engagement:*
- Challenge/skill audit: identify activities where skill has outpaced challenge (boredom) vs. challenge has outpaced skill (anxiety) → route to mindset-flow for detailed redesign
- Job crafting: reframe existing work tasks to increase engagement, emphasize strengths, add complexity
- Identify signature strengths (via VIA Character Strengths) and design activities that deploy them

*Low Relationships:*
- Active-constructive responding: respond to others' good news actively and constructively (not passive, not destructive)
- Deepen existing relationships rather than broadening shallow ones — quality is the lever
- Identify where genuine knowing is absent (you are known as a role, not as a person) and create the conditions for it

*Low Meaning:*
- Purpose articulation: what would still matter if all external validation were removed?
- Craft a personal mission that connects daily work to larger contributions — not a performance, a genuine answer
- Post-traumatic growth practices: meaning is often forged in difficulty, not despite it

*Low Accomplishment:*
- Goal decomposition: large ambitions that produce no completion experiences vs. structured milestones that generate ongoing closure
- Mastery tracking: explicit records of progress make growth visible where it would otherwise be invisible
- Distinguish outcome goals (depend on external factors) from process goals (within your control) — the latter build accomplishment sustainably

**Step 5: Design a Concrete Practice**
For the highest-deficit dimension, specify a concrete daily or weekly practice. Not "spend more time with friends" but: a specific behavior, at a specific frequency, measurable enough to know if it's happening.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool:

- **Question:** "What's the wellbeing situation you want to work through?"
- **Header:** "Positive Psychology"
- **Options:**
  - **Full PERMA audit** — Rate all five dimensions, find the deficit, get a targeted intervention
  - **I know which dimension is low** — Skip the audit and go straight to intervention for [P/E/R/M/A]
  - **Something feels missing but I can't name it** — Run the diagnostic without scores, from conversation
  - **Toxic positivity check** — Examine whether an approach I'm using is genuine vs. suppressive

---

## Output Format

### PERMA Audit
| Dimension | Score | Evidence |
|---|---|---|
| Positive emotion | /10 | [What's present/absent] |
| Engagement | /10 | [What's present/absent] |
| Relationships | /10 | [What's present/absent] |
| Meaning | /10 | [What's present/absent] |
| Accomplishment | /10 | [What's present/absent] |

### Diagnosis
**Primary deficit:** [Dimension(s) most underdeveloped]
**Pattern:** [The specific wellbeing pattern this represents — e.g., "accomplishment without savoring", "high purpose, absent engagement"]
**What the numbers say vs. what they hide:** [Where the audit may be misleading]

### Genuine vs. Toxic
**Assessment:** [Is the person's current coping approach building capacity or suppressing legitimate experience?]

### Targeted Intervention
**For [primary deficit dimension]:**
[Full description of the specific intervention — evidence base, how to execute, what to expect]

### Concrete Practice
**What to do:** [Specific behavior]
**Frequency:** [How often]
**Measure of success:** [How you'll know it's happening and working]

---

## Notes

Positive psychology is not the same as positive thinking. It does not claim that good things happen to people who think positively, or that negative emotions should be avoided. The research tradition it draws on is empirical: these are interventions that have been tested, with effect sizes, replicated across populations.

Nearest neighbors: mindset-stoic (for equanimity under adversity, rather than building flourishing), mindset-growth (for development orientation rather than wellbeing dimensions), emotional (for working with specific feeling states rather than long-run flourishing structure). Use positive psychology when the question is "what makes life worth living" or "why am I not thriving." Use Stoic when the question is "how do I find peace with what I cannot change."

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Positive reframe applied. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-emotional-motivation-mapping` — Map the motivations behind the positive reframe
  - `/s4h-decision-premortem-analysis` — Stress-test the optimistic assumptions
  - `/s4h-probability-confidence-calibration` — Calibrate the positivity against base rates
  - **Done** — Wrap up and synthesise what we have so far
