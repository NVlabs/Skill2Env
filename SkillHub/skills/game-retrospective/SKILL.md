---
name: "game-retrospective"
description: >
  Run a game development post-mortem rooted in the GDC tradition. Triggers on:
  "retrospective", "retro", "post-mortem", "lessons learned", "what went right", "what
  went wrong", "kill list review". Do NOT invoke for design document review (use
  game-design-review) or playtesting (use game-playtest). Part of the AlterLab GameForge
  collection.
argument-hint: "[sprint-N or milestone-name or 'project']"
effort: medium
allowed-tools: Read, Glob, Grep, Write, AskUserQuestion
version: 1.3.0
---

# AlterLab GameForge -- Game Development Post-Mortem

The game industry has the best post-mortem tradition in software. Gamasutra's classic
post-mortem series — Diablo II, Baldur's Gate, Black & White, Thief — taught an entire
generation of developers more than any textbook because they were brutally honest. Five
things that went right. Five things that went wrong. No spin, no corporate sanitizing,
no "learnings and opportunities." Just the truth about what happened when a team tried to
ship a game.

This workflow follows that tradition. Not Scrum retrospectives. Not agile ceremonies. Game
development post-mortems — the format that Supergiant used to iterate Hades from a decent
roguelike into a genre-defining masterpiece, that ConcernedApe used to survive five years
of solo development on Stardew Valley without losing his mind, that the Dwarf Fortress
brothers used to sustain a twenty-year development cycle without burning out or losing
direction.

The difference between a corporate retro and a game post-mortem: a corporate retro asks
"what could we improve?" A game post-mortem asks "did we build the right game, and did we
build it the right way?" One optimizes process. The other interrogates the creative and
technical decisions that determine whether your game ships, and whether it is worth
shipping.

### Purpose & Triggers

Run this workflow when:
- A sprint ends and the next one has not started
- A milestone lands (vertical slice, alpha, beta, gold)
- A project ships or is cancelled
- Development feels stuck and nobody can articulate why
- The game is "fine but not fun" and the team needs to diagnose the gap
- A major pivot or scope cut just happened and the dust has settled
- Before starting a new project, to extract lessons from the last one

Problems this solves:
- Repeating the same design mistakes because nobody documented why a feature failed
- Cutting the wrong features because scope pressure overrides design judgment
- Technical debt accumulating invisibly until it blocks progress
- Teams that playtest but never analyze the patterns in playtest data
- Solo developers who skip reflection and wonder why their third prototype dies the
  same death as the first two
- The "it felt off but we shipped it anyway" regret cycle

### Critical Rules

1. **GDC format, not agile format.** The structure is "What Went Right / What Went Wrong /
   Lessons Learned." Not "went well / didn't go well / action items." The distinction
   matters: GDC format forces you to commit to a judgment. Something either went right or
   it went wrong. Fence-sitting is not allowed.

2. **Game-specific lenses, not generic process questions.** Every retrospective passes
   through six game development lenses (detailed below). "Did we communicate well?" is a
   process question. "Did the core loop deliver the intended experience?" is a game
   development question. This workflow asks the second kind.

3. **The Kill List is mandatory.** Every retrospective includes a review of what was cut.
   The discipline to cut is the discipline to ship. The Kill List forces you to evaluate
   whether your cuts were correct, premature, or too late.

4. **"The One Thing" is mandatory.** After all analysis, distill everything to a single
   sentence. One lesson. The one that changes how you work next time. If you cannot pick
   one, you have not thought hard enough.

5. **Evidence over feelings.** "The combat felt off" is not a finding. "Playtesters
   disengaged during combat encounters longer than 45 seconds, suggesting the damage
   loop is too slow for the encounter scale" is a finding. Back everything with data,
   playtest observations, or specific incidents.

6. **Read the last post-mortem first.** Before starting, review the previous retrospective.
   Did those lessons actually change anything? If the same problems appear twice, the issue
   is not awareness — it is execution. That distinction changes the action plan entirely.

7. **Solo devs do this too.** ConcernedApe developed Stardew Valley alone for five years.
   He has spoken publicly about the burnout, the scope creep, the periods where he almost
   quit. Solo developers have zero external feedback loops. This workflow IS your external
   feedback loop. Write it down. Do not just think about it.

### The Six Game Development Lenses

These lenses replace generic retro questions. Every retrospective — sprint, milestone, or
project — passes through all six. Not every lens will produce findings every time. That is
fine. But you must look through each one.

---

**Lens 1: Core Loop Validation**

Did the core loop deliver the intended experience? Was it fun in isolation before content,
narrative, and progression systems were layered on top?

Celeste's core loop — dash, jump, climb — was fun in a blank room with white rectangles.
Madeline's movement felt good before a single strawberry, B-side, or story beat existed.
If your core loop is not fun in a blank room, content will not save it. This is the most
important lens because everything else is built on top of it.

Questions to answer:
- Strip away all content, progression, and narrative. Is the core verb set satisfying on
  its own? Can you play the loop for 10 minutes in a test room and want to keep going?
- Where in the loop does the player feel agency? Where do they feel constrained? Are those
  the right places?
- What is the loop's rhythm? Is it the rhythm you designed, or did it drift during
  implementation?
- How long is one cycle of the loop? Is that length correct for your genre and session
  target?
- Reference check: Hades' core loop (enter room, fight, choose boon, repeat) was iterated
  for over a year in Early Access. Supergiant shipped the loop first and layered content
  on a proven foundation. Did you do the same, or did you build content on an unproven
  loop?

---

**Lens 2: Pillar Integrity**

Did the design pillars hold through implementation, or did they drift? If they drifted,
was the drift intentional evolution or unconscious erosion?

Pillars are only useful if they survive contact with production. A pillar that reads
beautifully in a GDD but gets quietly abandoned when implementation gets hard was never a
real pillar — it was an aspiration. This lens detects the gap between stated pillars and
shipped reality.

Questions to answer:
- For each pillar: name three specific implementation decisions where the pillar guided the
  choice. If you cannot name three, the pillar was not operational.
- For each pillar: name one moment where the pillar was violated or compromised. What
  caused it? Schedule pressure? Technical limitation? A better idea that superseded the
  pillar?
- Did any new implicit pillars emerge during development? Something the team was
  consistently prioritizing that was never formally named? Name it now.
- Are the pillars still the right pillars, or does the game you actually built suggest
  different ones?
- Reference check: Hollow Knight's pillar of "atmospheric exploration" held through every
  expansion. Team Cherry cut content that did not serve it, even content they loved. Did
  your pillars have that authority, or were they suggestions?

---

**Lens 3: Scope Tier Review**

Did the Must/Should/Could prioritization protect the right features? What moved between
tiers during development, and were those moves correct?

Scope management is not about cutting features. It is about protecting the features that
make your game YOUR game while having the discipline to let go of everything else.

Questions to answer:
- List every feature that was in the "Must" tier at the start of this period. How many
  shipped? How many were downgraded or cut?
- For each downgraded "Must": was the downgrade correct? If you had to make that call
  again with current knowledge, would you?
- What "Should" or "Could" features consumed more resources than planned? Were they worth
  the overrun?
- What is the ratio of planned scope to shipped scope? Is the delta acceptable, or does it
  indicate a systemic estimation problem?
- Reference check: Stardew Valley's scope grew continuously for five years because
  ConcernedApe had no external deadline and no scope authority except himself. The game is
  a masterpiece, but the development nearly destroyed him. Scope discipline is self-care.

---

**Lens 4: Flow State Analysis**

Where did playtesters enter flow? Where did they bounce? Map observed engagement against
the intended experience curve.

Flow — the Csikszentmihalyi state where challenge perfectly matches skill — is not an
accident. It is designed. This lens compares your intended flow curve against what players
actually experienced.

Questions to answer:
- Map the intended experience curve for a play session: where should challenge rise? Where
  should it rest? Where is the peak?
- Overlay playtest data: where did players actually engage deeply (long sessions, repeated
  attempts, audible reactions)? Where did they disengage (put down the controller, check
  their phone, quit)?
- Where are the flow breakers? Inventory management mid-combat? Unskippable dialogue?
  Loading screens at tension peaks? Tutorials that interrupt momentum?
- Is the difficulty curve a curve or a cliff? Where do players hit walls? Are those walls
  intentional gates or unintentional friction?
- Reference check: Dark Souls' flow design is a masterclass in intentional frustration.
  The difficulty is the point — but the game never wastes your death. Every failure teaches
  something. If your players are frustrated AND not learning, your difficulty is not Dark
  Souls difficulty — it is bad difficulty.

---

**Lens 5: Technical Debt Audit**

What shortcuts taken for speed are now blocking progress? Which shortcuts were worth it?
Which should have been paid down earlier?

Every game accumulates technical debt. The question is not "do we have debt?" but "is our
debt in the right places?" Debt in a prototype system that will be rewritten is free. Debt
in a core system that everything depends on is compounding interest.

Questions to answer:
- List the top 5 technical shortcuts currently in the codebase. For each: what would it
  cost to fix? What is the cost of NOT fixing it over the next milestone?
- Which shortcuts enabled you to hit deadlines that mattered? Those were good debt. Name
  them and acknowledge the tradeoff.
- Which shortcuts are now blocking new features or causing bugs? Those are bad debt that
  should have been paid sooner. Why were they not?
- Is there a pattern in where debt accumulates? If it is always in the same system, that
  system needs an architectural rethink, not a patch.
- What is the "bus factor" for your most critical technical debt? If the one person who
  understands the hacky save system leaves, how much damage does that cause?
- Reference check: Dwarf Fortress has been in development for over twenty years. The Adams
  brothers make deliberate, documented technical decisions about what to hack and what to
  build properly — because they know they will be maintaining this codebase for decades.
  Your timeline is shorter, but the principle holds: know what you owe and why.

---

**Lens 6: Ludonarrative Check**

Where did mechanics and narrative reinforce each other? Where did they contradict? Did the
game say one thing with its story and another with its systems?

Ludonarrative dissonance — the term Clint Hocking coined reviewing BioShock — is when the
story tells you to care about characters while the gameplay tells you to loot their
corpses. It is the gap between what the narrative says the game is about and what the
mechanics actually reward.

Questions to answer:
- Identify three moments where mechanics and narrative aligned perfectly. What made them
  work? Can you create more moments like these?
- Identify any moments where mechanics and narrative contradicted. The story says "time is
  running out" but the gameplay lets you farm sidequests for hours. The narrative says
  "violence has consequences" but the combat system rewards kill combos.
- Do the progression systems reinforce the narrative arc? Does the player grow in ways that
  match their character's journey?
- What do the game's mechanics say about the game's themes, independent of any dialogue
  or cutscenes? Is that message intentional?
- Reference check: Disco Elysium is the gold standard. Every skill IS a narrative voice.
  Every stat check IS a story moment. The mechanics do not support the narrative — they ARE
  the narrative. Outer Wilds achieves the same unity: every "story" moment is actually a
  physics puzzle. You do not need to reach that level, but you need to know where your
  mechanics and narrative are pulling in different directions.

---

### The Kill List

This section is mandatory for every retrospective scope. It is a dedicated review of every
feature, system, or content piece that was cut during this period.

Team Cherry cut multiple biomes from Hollow Knight that were partially built — geometry
laid out, enemies designed, some art complete. The discipline to cut half-built work is
harder than cutting ideas, because you can see the sunk cost. The Kill List forces you to
confront your cuts honestly.

```
KILL LIST: [Sprint/Milestone/Project Name]
Date: [date]

+------------------------------------------------------------------+
| Feature Cut       | Stage When Cut  | Reason      | Correct Call?|
+-------------------+-----------------+-------------+--------------+
| [Feature name]    | [Idea/Design/   | [Why it was | [Yes/No +    |
|                   |  In-Progress/   |  cut]       |  reasoning]  |
|                   |  Nearly-Done]   |             |              |
+-------------------+-----------------+-------------+--------------+
| [Feature name]    | [stage]         | [reason]    | [assessment] |
+-------------------+-----------------+-------------+--------------+

CUTS THAT WERE CORRECT:
- [Feature]: Right call because [specific reason it was the right cut].

CUTS THAT WERE TOO LATE:
- [Feature]: Should have been cut at [earlier stage] instead of [when it was
  actually cut]. Cost of delay: [wasted effort in hours/days/sprints].

CUTS THAT WERE PREMATURE:
- [Feature]: In hindsight, this should have survived. Evidence: [why you now
  believe it was worth keeping].

FEATURES THAT SHOULD HAVE BEEN CUT BUT SURVIVED:
- [Feature]: This shipped but should not have. It [diluted the experience /
  consumed resources better spent elsewhere / violated a pillar]. Why it
  survived: [inertia / sunk cost fallacy / stakeholder attachment].

THE EARLIER CUT:
If you could go back to the start of this period, what would you cut on day
one that you did not cut until [later]?
- [Feature]: Cut immediately because [reason].

THE FIERCER PROTECTION:
What would you protect more fiercely against scope pressure?
- [Feature]: Protect because [reason it was more important than recognized].
```

### "The One Thing"

After completing all six lenses and the Kill List, distill everything to a single sentence.
This is the hardest part. It is also the most valuable.

The single most important thing we learned is: ____________________

Rules for "The One Thing":
- It must be specific. "Communicate better" is not an insight. "Playtest the core loop in
  isolation before building content on top of it" is an insight.
- It must be actionable. It should change a specific behavior or decision in the next
  sprint, milestone, or project.
- It must be honest. The comfortable lesson and the true lesson are rarely the same.
- It should be the thing that, if you had known it at the start, would have changed the
  most about how this period went.

Examples of good "One Things":
- "We should have cut the crafting system in week two — it served no pillar and consumed
  30% of our implementation time."
- "The core loop was not fun until we added hit-stop and screen-shake, which means we were
  evaluating an incomplete loop for two months and making design decisions based on wrong
  data."
- "Our milestone estimates were 40% under actual because we scoped features but not
  integration time, and integration was where every bug lived."
- "The narrative branching added complexity that QA could not cover, and we shipped three
  progression-breaking bugs because of paths we never tested."

Examples of bad "One Things":
- "We need to plan better." (Vague. Plan what? How?)
- "Communication is important." (Obviously. What specific communication failure, between
  whom, caused what damage?)
- "We should have had more time." (Not actionable. You will never have more time.)

### Output Templates

Three formats scaled to scope. All follow GDC post-mortem structure, not agile retro
structure.

---

**FORMAT 1: Sprint Post-Mortem (15 minutes)**

```
SPRINT POST-MORTEM: [Sprint Name/Number]
Date: [date]
Sprint goal: [the single-sentence sprint goal]
Goal met: [Yes / No / Partially -- one sentence on why]

PREVIOUS POST-MORTEM REVIEW:
- [Action from last time] | [Done/Not Done] | [If not: why?]

--- SIX LENSES (hit only those with findings this sprint) ---

Core Loop:     [Finding or "No change this sprint"]
Pillars:       [Finding or "Held / Drifted -- specify"]
Scope:         [What moved between tiers and why]
Flow:          [Playtest observation or "No new data"]
Tech Debt:     [New debt taken on / Old debt paid down]
Ludonarrative: [Alignment finding or "N/A this sprint"]

--- WHAT WENT RIGHT (max 3) ---
1. [Specific positive] -- Why: [root cause of success]
2.
3.

--- WHAT WENT WRONG (max 3) ---
1. [Specific problem] -- Root cause: [system failure, not person]
2.
3.

--- KILL LIST ---
[Features cut this sprint, evaluated per Kill List format above]

--- THE ONE THING ---
The single most important thing we learned is:
[one sentence]

--- ACTIONS ---
| Action          | Owner   | Deadline | How We Will Know It Worked |
|-----------------|---------|----------|----------------------------|
| [specific act]  | [name]  | [date]   | [measurable outcome]       |
| [max 3 actions] |         |          |                            |
```

---

**FORMAT 2: Milestone Post-Mortem (45 minutes)**

```
MILESTONE POST-MORTEM: [Milestone Name]
Date range: [start] to [end]
Sprints covered: [N]

HEADLINE: [One sentence — the story of this milestone]

--- GOALS VS. REALITY ---
| Goal                | Target              | Actual              | Verdict   |
|---------------------|---------------------|---------------------|-----------|
| [milestone goal]    | [what success was]  | [what happened]     | [Met/Miss]|

--- SIX LENSES (full analysis) ---

CORE LOOP VALIDATION:
[Detailed findings. Is the loop proven? Where is it weak?]

PILLAR INTEGRITY:
[Per-pillar assessment. Which held? Which drifted? Why?]

SCOPE TIER REVIEW:
| Feature         | Starting Tier | Ending Tier | Move Justified? |
|-----------------|---------------|-------------|-----------------|
| [feature]       | Must          | Cut         | [Yes/No + why]  |

FLOW STATE ANALYSIS:
[Map intended experience curve vs. observed player behavior.
 Identify flow breakers and flow peaks.]

TECHNICAL DEBT AUDIT:
| Debt Item       | Cost to Fix | Cost of Ignoring | Priority    |
|-----------------|-------------|------------------|-------------|
| [shortcut]      | [effort]    | [consequence]    | [Fix/Defer] |

LUDONARRATIVE CHECK:
[Where do mechanics and story align? Where do they fight?]

--- WHAT WENT RIGHT (5 items, GDC format) ---
1. [Title]: [2-3 sentences. What went right and WHY it went right.
   Be specific enough that another team could replicate the success.]
2.
3.
4.
5.

--- WHAT WENT WRONG (5 items, GDC format) ---
1. [Title]: [2-3 sentences. What went wrong and WHY it went wrong.
   Trace to a system or decision, not a person.]
2.
3.
4.
5.

--- KILL LIST ---
[Full Kill List format from above]

--- THE ONE THING ---
The single most important thing we learned is:
[one sentence]

--- ACTIONS ---
| Priority | Action              | Owner  | Deadline | Success Metric  |
|----------|---------------------|--------|----------|-----------------|
| P1       | [urgent]            | [name] | [date]   | [measurable]    |
| P2       | [important]         | [name] | [date]   | [measurable]    |
| P3       | [improvement]       | [name] | [date]   | [measurable]    |

PROCESS CHANGES (effective immediately):
- [Change]: [Rationale]

CARRY FORWARD:
- [Systemic issue requiring ongoing attention across next milestone]
```

---

**FORMAT 3: Project Post-Mortem (90 minutes)**

*The full GDC-style post-mortem. This is a historical document. Write it honestly enough
that it would be worth publishing. Reference `@templates/post-mortem.md` for the complete
template.*

```
PROJECT POST-MORTEM: [Project Name]
Duration: [start] to [end] ([total months])
Team size: [headcount or "solo"]
Final scope: [features shipped] / [features originally planned] ([percentage])

ELEVATOR PITCH (as designed):
[What was this game supposed to be?]

ELEVATOR PITCH (as shipped):
[What did this game actually become?]
[If these two pitches are different, that delta IS the post-mortem.]

--- PROJECT TIMELINE ---
| Phase          | Planned     | Actual      | Delta       | Key Event     |
|----------------|-------------|-------------|-------------|---------------|
| Concept        | [dates]     | [dates]     | [+/- weeks] | [what happened]|
| Pre-production | [dates]     | [dates]     | [+/- weeks] |               |
| Production     | [dates]     | [dates]     | [+/- weeks] |               |
| Alpha          | [dates]     | [dates]     | [+/- weeks] |               |
| Beta           | [dates]     | [dates]     | [+/- weeks] |               |
| Polish         | [dates]     | [dates]     | [+/- weeks] |               |
| Launch         | [dates]     | [dates]     | [+/- weeks] |               |
Total delta: [how far from original schedule]

--- SIX LENSES (definitive assessment) ---

CORE LOOP VALIDATION:
[Final verdict on the core loop. Was it proven before production began?
 What would you change about when and how you validated it?]

PILLAR INTEGRITY:
[For each pillar: did it survive from GDD to gold master? Where did it
 bend? Where did it break? Grade each pillar A through F.]

SCOPE TIER REVIEW:
[Full audit. Original scope vs. shipped scope. Every feature that moved
 between tiers, with justification assessment.]

FLOW STATE ANALYSIS:
[Aggregate playtest data across the full project. Where does the shipped
 game achieve flow? Where does it lose players?]

TECHNICAL DEBT AUDIT:
[What debt shipped? What debt was paid down during polish? What debt
 will haunt a sequel or DLC?]

LUDONARRATIVE CHECK:
[Final assessment of mechanics-narrative alignment in the shipped product.]

--- WHAT WENT RIGHT (5 items, GDC format) ---
1. [Title]
   [Full paragraph. What went right, why, what conditions enabled it,
    and what other teams can learn from this success.]
2.
3.
4.
5.

--- WHAT WENT WRONG (5 items, GDC format) ---
1. [Title]
   [Full paragraph. What went wrong, the root cause, the impact, when
    the team recognized it, and what should have been done differently.]
2.
3.
4.
5.

--- COMPLETE KILL LIST ---
[Every feature cut across the entire project, evaluated with full
 hindsight. This is the most valuable section for future projects.]

--- THE ONE THING ---
The single most important thing we learned is:
[one sentence]

[Then: 2-3 sentences expanding on why this is THE lesson, and how it
 will specifically change your approach on the next project.]

--- KEY LEARNINGS (5-7 maximum) ---
| Lesson                        | Evidence                   | Applies To     |
|-------------------------------|----------------------------|----------------|
| [transferable principle]      | [specific project example] | [future scope] |

Each lesson must be backed by specific evidence from this project. "Planning
matters" is not a lesson. "Our estimates were 40% under actual because we did
not account for integration time between the dialogue system and the save
system, which added 6 weeks" is a lesson.

--- PUBLISH ASSESSMENT ---
Audience:      [internal only / team blog / GDC talk / public post-mortem]
Redactions:    [anything not for public consumption]
Value to others: [what would another team learn from reading this?]
```

### Facilitation Guide

**For Solo Developers:**

You are both participant and facilitator. You have no one to challenge your assumptions,
which makes this exercise more important, not less.

Use these prompts — and write the answers down. ConcernedApe journaled during Stardew
Valley development. It was part of how he survived.

```
SOLO DEV POST-MORTEM PROMPTS
1. What did I spend the most time on? Was it the RIGHT thing to spend
   time on, or was it the comfortable thing?
2. What task took 3x longer than expected? Why was my estimate wrong?
   (Not "it was harder than I thought" — WHY was it harder?)
3. What am I avoiding? What part of the project do I open last? That
   avoidance is data.
4. Run the six lenses solo. Even two-sentence answers per lens are
   valuable.
5. Fill out the Kill List. What did I cut? Was each cut right?
6. Am I still excited about this project? Scale of 1-10. Track this
   number over time. A downward trend that hits 3 means you need to
   change something fundamental — scope, direction, or schedule — not
   just push through.
7. The One Thing. Force yourself to pick one.
```

**For Teams (2+ people):**

The facilitator's job is to protect honesty. People will self-censor in group settings.
The facilitator prevents that.

```
FACILITATION PROTOCOL
Before:
  [ ] Review previous post-mortem and its actions
  [ ] Collect playtest data, velocity metrics, bug counts
  [ ] Send the six lenses to the team 24 hours in advance so they
      arrive with findings, not blank stares
  [ ] Book the room. Set a timer. Enforce the timebox.

During:
  [ ] Start with previous action review. Accountability first.
  [ ] Run each lens in order. 5-7 minutes per lens for sprints,
      10-15 for milestones.
  [ ] The Kill List gets its own dedicated block. Do not skip it.
  [ ] One person talks at a time. No defending, no explaining away.
  [ ] When someone says "it's fine" about something that clearly is
      not fine, the facilitator pushes: "What would you change about
      it if you could?"
  [ ] Capture The One Thing individually first (everyone writes it
      down silently), then share. Consensus is not required — divergent
      "One Things" are informative.

After:
  [ ] Distribute the document within 1 hour
  [ ] Actions go into the sprint backlog immediately, not "later"
  [ ] File the post-mortem in the project archive
  [ ] Schedule mid-sprint check on actions
```

### Anti-Patterns

These kill retrospectives faster than skipping them:

- **The Gamasutra Sanitized Version:** Everything is phrased as a positive. "We had the
  opportunity to learn about scope management" means "we cut half the game and it was
  painful." Stop sanitizing. The honest version is the useful version.

- **The Blame Post-Mortem:** "John broke the build three times." That is not analysis. "Our
  CI pipeline had no pre-merge validation, so broken builds reached main. The system failed,
  not John." Redirect every blame to a system question.

- **The Action Graveyard:** You generated 12 action items last retro. How many were
  completed? If the answer is fewer than half, generate fewer actions this time and
  actually do them. Three completed actions beat twelve abandoned ones.

- **The Missing Kill List:** "We did not cut anything." You either cut features or you
  overscoped. Both are worth examining. If you truly cut nothing, examine whether your
  scope was too conservative — were you building a game that was safe instead of ambitious?

- **The Comfortable One Thing:** "We learned a lot." That is not a lesson. Push harder. The
  real One Thing is usually the one that is slightly uncomfortable to say out loud.

- **The Skipped Post-Mortem:** "We are too busy." This is the clearest signal that you need
  one. Fifteen minutes for a sprint post-mortem. If you cannot find fifteen minutes, your
  sprint has deeper problems than this retro will fix.

### Cross-References

- `@docs/collaboration-protocol.md` -- Communication norms for post-mortem discussions
- `@docs/coordination-rules.md` -- Escalation paths for systemic issues found in retros
- `@docs/game-design-theory.md` -- Flow Theory, MDA Framework, SDT for lens analysis
- `@templates/post-mortem.md` -- Extended project post-mortem template
- Workflow handoffs: follows any sprint or milestone, feeds into `game-sprint-plan` for
  the next cycle and `game-scope-check` if scope issues surface

Part of the AlterLab GameForge -- Indie Game Development Skills suite.
