---
name: "game-brainstorm"
description: >
  Invoke when the user wants to brainstorm game ideas, explore concepts, run structured
  ideation, or develop a new game concept from scratch. Triggers on: "game idea",
  "brainstorm", "concept", "ideation", "what if", "game concept", "pitch". Do NOT invoke
  for reviewing existing designs (use game-design-review) or market analysis (use
  game-market-research). Part of the AlterLab GameForge collection.
argument-hint: "[genre or theme, or 'open' for freeform]"
effort: medium
context: fork
allowed-tools: Read, Glob, Grep, Write, AskUserQuestion
version: 1.3.0
---

# AlterLab GameForge -- Structured Ideation Workflow

Most game ideas die not from lack of creativity but from lack of structure. A notebook of "what if" scribbles never becomes a shipped game without deliberate shaping. This workflow takes raw creative energy through seven phases of increasingly focused refinement, transforming vague excitement into a concrete, market-validated, scope-aware game concept a team can execute.

This is not a template you fill out in silence. It is an interactive process -- every phase involves direct questions to you, the designer. Your answers steer the direction. Early phases have no wrong answers. By the end, every answer defends itself against market reality, player psychology, and honest scope assessment.

The seven phases alternate between divergent thinking (expand possibilities) and convergent thinking (narrow to decisions). Skipping phases causes predictable failures: skip Discovery and you build something you do not care about. Skip Market Validation and you build something nobody will buy -- Baba Is You succeeded because Arvi Teikari validated that puzzle fans were starving for constraint-based innovation, not because he got lucky. Skip Core Loop Design and you have a concept that sounds cool but plays like nothing. Skip Scope and you announce a game you cannot finish.

### Purpose & Triggers

Use this workflow when:
- A developer says "I want to make a game but don't know what kind"
- Someone has a vague concept ("something with time travel") but no structure around it
- A team needs to explore multiple directions before committing
- The user finished `game-start` and was routed here for concept development
- Anyone is stuck in idea-paralysis, cycling through concepts without committing
- A developer wants to pivot an existing concept and needs fresh ideation

Problems this kills:
- The "infinite possibility" paralysis of starting from zero
- Ideas that sound exciting but have no playable core
- Concepts that ignore market reality -- building a game nobody asked for in a genre nobody buys
- Games designed for nobody in particular (no target player type)
- Scope blindness -- designing a 5-year project on a 5-month timeline
- Derivative designs that accidentally clone existing games without knowing it

### Critical Rules

1. **Interactive, not generative.** Do NOT generate a game concept for the user. Guide them
   through discovering their own. Ask questions. Present frameworks. Let them fill in the
   substance. Your job is structure and provocation, not authorship.

2. **Emotions before features.** Phase 1 starts with feelings, not mechanics. "What
   experience do you want the player to have?" comes before "What buttons do they press?"
   Features are servants of experience, never the other way around.

3. **Constraints are creative fuel.** A solo dev with 3 months and a free engine is not
   limited -- they are focused. ConcernedApe built Stardew Valley alone. Toby Fox made
   Undertale with almost nothing. The best games in history were born from severe constraints.

4. **The 30-second loop is sacred.** If the core 30-second gameplay loop is not intrinsically
   fun without any progression, unlocks, story, or rewards layered on top, the concept is
   structurally flawed. Vampire Survivors proves this -- the 30-second loop of dodging and
   auto-attacking is hypnotic before a single upgrade enters the picture.

5. **No precious ideas.** Every concept generated in Phase 2 must survive scrutiny in
   Phases 3-7. If it cannot, discard it without sentimentality. Kill concepts in brainstorms,
   not after six months of development.

6. **Market awareness is not selling out.** Passion projects still need players. Outer Wilds
   was deeply personal AND found its audience because Mobius understood the "curious explorer"
   market existed. Validate that real humans want what you are building.

7. **Honest scope from the start.** If the concept requires 20 unique enemy types and the
   team has one artist working part-time, say so. Scope honesty is kindness to your future self.

8. **Reference the theory.** All frameworks referenced here (MDA, SDT, Bartle, Flow) are
   defined in `docs/game-design-theory.md`. Do not reinvent the definitions. Point there.

### Workflow

---

**PHASE 1: Creative Discovery**

*Goal: Explore the emotional and experiential space before touching mechanics.*

This phase is entirely about excavating what genuinely excites the designer. Not what seems
marketable. Not what is trending on Steam. What makes them lean forward in their chair.

**Exercise 1.1 -- The Excitement Inventory**

Ask these questions and listen carefully to what lights up:

```
DISCOVERY QUESTIONS (ask all, discuss responses)
-------------------------------------------------
1. What is the last game that made you lose track of time? Why?
2. What is a moment in any game that you still think about years later?
3. What emotion do you most want your player to feel?
   (wonder, tension, triumph, melancholy, mischief, mastery, connection, dread)
4. What non-game experience would you love to translate into gameplay?
   (a sport, a job, a relationship dynamic, a natural phenomenon)
5. If you could only keep ONE system from your favorite game,
   which system and why?
6. What is a game that almost got it right but fumbled? What would you fix?
```

Do not rush through these. Each answer contains seeds. Identify recurring themes across
the answers. Those themes are the emotional foundation of the concept.

**Exercise 1.2 -- Reference Mining**

Go beyond games. The most original games draw from unexpected sources.

```
REFERENCE MAPPING
-------------------------------------------------
Category       | Title              | What it contributed
-------------------------------------------------
Games          | [user fills in]    | [specific mechanic or feeling]
Films          | [user fills in]    | [visual style, pacing, theme]
Books          | [user fills in]    | [world logic, character arc]
Music          | [user fills in]    | [mood, rhythm, atmosphere]
Real life      | [user fills in]    | [system, interaction, sensation]
-------------------------------------------------
```

Look for unexpected connections between references. A game that combines the pacing of a
particular film with the system logic of a real-world job is already more interesting than
"like Dark Souls but with guns."

**Exercise 1.3 -- Constraint Mapping**

Constraints define the creative space. Map them honestly.

```
CONSTRAINT INVENTORY
-------------------------------------------------
Dimension       | Reality
-------------------------------------------------
Team size       | [1 person / 2-5 / 6-15 / 15+]
Timeline        | [jam / 1-3 months / 3-12 months / 12+ months]
Budget          | [zero / small / moderate / funded]
Platform        | [PC / console / mobile / web / VR / multi]
Engine          | [chosen or undecided]
Art capacity    | [programmer art / asset store / dedicated artist / art team]
Audio capacity  | [stock / freelance / dedicated / full audio team]
Tech skill      | [beginner / intermediate / advanced / expert]
Genre comfort   | [genres the team has shipped or prototyped before]
-------------------------------------------------
```

**Exercise 1.4 -- Anti-Inspiration**

Equally valuable: what you do NOT want to make.

```
ANTI-INSPIRATION (ask the user)
-------------------------------------------------
- What genre are you tired of?
- What game mechanic do you find tedious even when well-executed?
- What trend in current games makes you roll your eyes?
- What type of player experience do you want to avoid creating?
- What game do people keep suggesting you should clone, and why do you resist?
-------------------------------------------------
```

Anti-inspiration sharpens the concept by exclusion. Knowing what you refuse to build is as
clarifying as knowing what you want to build.

---

**PHASE 2: Concept Generation**

*Goal: Produce 3-5 distinct game concepts using structured divergent techniques.*

Do not settle on the first idea. Generate multiple candidates using three different methods,
then evaluate them against each other. Each method approaches ideation from a fundamentally
different angle, which is deliberate -- it prevents tunnel vision.

**Technique 2.1 -- Verb-First Design**

The core verb IS the game. Strip away theme, art, story, progression. What does the player
DO moment-to-moment?

```
VERB-FIRST GENERATION
-------------------------------------------------
Step 1: Choose a core verb
  build, explore, survive, negotiate, compose, rescue, deceive, cultivate,
  investigate, perform, dismantle, connect, translate, terraform, orchestrate

Step 2: Add a constraint world
  "What if the player could [VERB] in a world where [CONSTRAINT]?"

  Example constraints:
  - gravity reverses every 30 seconds
  - every action has a permanent consequence
  - you can only perceive one sense at a time
  - resources are emotions, not materials
  - the world is a single continuous loop
  - you share a body with an AI that has different goals

Step 3: Test immediacy
  "Is the verb itself fun to execute, regardless of WHY you are doing it?"
  If yes: strong candidate. If no: the verb needs a more interesting expression.
-------------------------------------------------
```

Generate 2-3 verb-first concepts. Write each as a single sentence.

**Technique 2.2 -- Mashup Method**

Combine two systems, genres, or themes that have no business being together. The collision
of unrelated ideas creates novelty.

```
MASHUP GENERATION
-------------------------------------------------
Step 1: Pick System A (a gameplay system from any genre)
  tower defense, dating sim, courtroom drama, factory management,
  rhythm game, deck building, flight simulator, cooking show

Step 2: Pick System B (a completely unrelated system or theme)
  underwater archaeology, corporate espionage, ant colony behavior,
  musical composition, geological survey, political negotiation

Step 3: Force the connection
  "What if [System A] mechanics existed in a [System B] context?"
  "What if the core tension of [System B] was expressed through [System A] gameplay?"

  Example: "Tetris meets courtroom drama"
  --> Physical evidence blocks fall; you must arrange them to build a legal argument
      before time runs out. Misplaced evidence weakens your case. The jury reacts
      in real time.

Step 4: Evaluate surprise
  "Does this combination produce an experience that neither source could alone?"
  If yes: strong candidate. If no: the mashup is cosmetic, not structural.
-------------------------------------------------
```

Generate 2-3 mashups. The weirder the combination, the more likely it surfaces something
genuinely novel. But weirdness alone is not enough -- the mashup must create emergent
gameplay, not just a novelty skin.

**Technique 2.3 -- MDA-Backward Design**

Most designers start with mechanics and hope aesthetics emerge. This technique reverses
the process: choose the target player experience first, then derive mechanics that
deliver it. Reference `docs/game-design-theory.md` for the full MDA Framework breakdown.

```
MDA-BACKWARD GENERATION
-------------------------------------------------
Step 1: Choose 2-3 target aesthetics from the MDA taxonomy
  Sensation, Fantasy, Narrative, Challenge, Fellowship,
  Discovery, Expression, Submission (zen/comfort)

Step 2: For each aesthetic, identify what dynamics deliver it
  Discovery --> exploration of unknown spaces, revealed information, "aha" moments
  Challenge --> escalating difficulty, mastery curves, meaningful failure
  Expression --> customization depth, creative tools, shareable output

Step 3: For each dynamic, design mechanics that produce it
  "Aha" moments --> fog of war, hidden connections, environmental storytelling
  Escalating difficulty --> adaptive enemy scaling, resource scarcity curves
  Creative tools --> modular building system, color palette, user-authored levels

Step 4: Assemble into a coherent system
  "A game where the player [mechanic cluster] to experience [aesthetic pair]"
-------------------------------------------------
```

Generate 1-2 MDA-backward concepts. These tend to produce the most psychologically
grounded designs because they start from the player's emotional needs.

**Concept Comparison**

After generating 3-5 concepts across the three techniques, compare them:

```
CONCEPT COMPARISON MATRIX
-------------------------------------------------
Concept  | Excitement | Feasibility | Uniqueness | Team Fit | Total
-------------------------------------------------
[A]      | /5         | /5          | /5         | /5       | /20
[B]      | /5         | /5          | /5         | /5       | /20
[C]      | /5         | /5          | /5         | /5       | /20
-------------------------------------------------
```

Select the top concept to carry forward. Do not average scores -- a concept that scores
5/5 on Excitement and 2/5 on Feasibility is worth discussing differently than one that
scores 3/5 across the board. Discuss tradeoffs explicitly.

---

**PHASE 3: Market Validation**

*Goal: Verify that real players exist for this concept and the market can sustain it.*

Passion without market awareness is how talented developers spend two years building a game that sells 47 copies. Vampire Survivors succeeded because poncle identified the underserved "casual bullet hell" niche -- players who wanted the dopamine of screen-filling chaos without the execution barrier of traditional shmups. Balatro found the "poker roguelike" gap nobody knew existed. Outer Wilds created an entirely new market for "knowledge-as-progression." None of these were accidents. Each creator understood the landscape before building.

**Exercise 3.1 -- Market Sizing**

Estimate the addressable market for your concept using comparable titles:

```
MARKET SIZING
-------------------------------------------------
Step 1: Identify 3-5 comparable games (same genre, similar scope, similar audience)
  Comparable       | Est. Revenue (SteamSpy/VGInsights) | Peak Players
  [game 1]         | [$X]                                | [N]
  [game 2]         | [$X]                                | [N]
  [game 3]         | [$X]                                | [N]

Step 2: Assess genre health
  Is the genre growing, stable, or declining?
  (Check Steam tag trends, itch.io tag volume, genre-specific subreddit growth)

  Growing genres (2024-2025 signal): roguelikes, cozy sims, extraction shooters
  Oversaturated: battle royales, zombie survival, generic pixel platformers
  Underserved (opportunity): asymmetric co-op, deduction games, tactile
  physics puzzlers, single-player narrative FPS

Step 3: Calculate realistic floor and ceiling
  Floor: Worst-performing comparable * 0.5 (assume you are less known)
  Ceiling: Best-performing comparable * 0.3 (unless you have a marketing edge)
  Realistic estimate: Median of comparables * 0.7

  If the realistic estimate does not cover development costs, the concept
  needs either a smaller scope or a more commercial angle. Do not ignore this.
-------------------------------------------------
```

**Exercise 3.2 -- Competitive Analysis**

Your game is not launching into a vacuum. Map the competitive landscape:

```
COMPETITIVE ANALYSIS
-------------------------------------------------
Direct competitors (same genre + similar hook):
  [Game]  | Strength         | Weakness         | Your differentiation
  [game1] | [what it nails]  | [where it fails] | [how you exploit that gap]
  [game2] | [what it nails]  | [where it fails] | [how you exploit that gap]

Indirect competitors (different genre, same player motivation):
  [Game]  | Why players might choose it over yours
  [game1] | [reason]
  [game2] | [reason]

The gap: What does your concept offer that NO existing game provides?
  [Specific answer -- "more accessible X" or "Y mechanic in Z context"]

If you cannot articulate the gap in one sentence, your concept is not
differentiated enough. Return to Phase 2 and sharpen the hook.
-------------------------------------------------
```

Obra Dinn did not just make a deduction game -- it identified that the deduction genre had been abandoned by studios while player appetite for it was growing through tabletop games. That gap was the market thesis.

**Exercise 3.3 -- Concept Validation Gates**

Run your top concept through three binary gates:

```
VALIDATION GATES
-------------------------------------------------
Gate 1: The Wishlist Test
  "If you saw this game's Steam page right now, would you wishlist it?"
  Ask 5 people who are NOT on your team and NOT your friends.
  If fewer than 3 say yes, the concept is not commercially compelling
  enough in its current form.

Gate 2: The Elevator Test
  Describe the concept in two sentences to someone unfamiliar with games.
  Do their eyes light up, or do they politely nod?
  Light up = hook works. Polite nod = hook is too niche or too generic.

Gate 3: The Comparison Test
  "What is this game competing against for the player's $15 and 20 hours?"
  If the answer includes a free-to-play juggernaut or an established franchise
  with a sequel coming, reassess your positioning. Compete where the giants
  are not looking.
-------------------------------------------------
```

Do not proceed past this phase if the concept fails two or more gates. Return to Phase 2 and generate new concepts, or sharpen the existing one until it passes. Ideas are cheap. Development time is not.

---

**PHASE 4: Core Loop Design**

*Goal: Design the heartbeat of the game across four timescales.*

The core loop is not a feature list. It is a cycle of player actions and game responses
that repeats throughout the experience. A game with a weak core loop cannot be saved by
content, story, or polish. A game with a strong core loop can survive with almost nothing
else.

Design the loop at four timescales. Each timescale must form a complete cycle:
**action --> feedback --> reward --> decision --> next action.**

**Timescale 1: The 30-Second Loop (Micro)**

This is the atomic unit of gameplay. What happens in any given 30-second window?

```
30-SECOND LOOP TEMPLATE
-------------------------------------------------
Action:    What the player physically does (input)
Feedback:  What the game immediately communicates back (visual, audio, haptic)
Reward:    What the player gains (progress, resource, information, satisfaction)
Decision:  What choice this creates for the next action
Repeat:    How the cycle feeds back into itself
-------------------------------------------------

CRITICAL TEST: Remove all progression, unlocks, story, and meta-rewards.
Is this 30-second loop still fun on its own?

If YES --> proceed. You have a core loop.
If NO  --> the concept needs mechanical redesign before proceeding.
           No amount of content wrapping fixes a boring core loop.
```

**Timescale 2: The 5-Minute Loop (Session Segment)**

A meaningful sub-goal that gives shape to a play window.

```
5-MINUTE LOOP TEMPLATE
-------------------------------------------------
Objective:  What is the player trying to accomplish in this window?
Escalation: How does tension or complexity build across these minutes?
Resolution: What marks the end of this segment (boss, puzzle, wave, trade)?
Carry-over: What persists into the next 5-minute segment?
-------------------------------------------------
```

**Timescale 3: The Session Loop (30-60 Minutes)**

What does a full play session feel like from sit-down to put-down?

```
SESSION LOOP TEMPLATE
-------------------------------------------------
Session goal:    What draws the player to start a session?
Session arc:     How does difficulty/intensity curve across the session?
Session reward:  What meaningful progress was made by session end?
Session hook:    What makes the player want to come back for another session?
Quit trigger:    What is the natural stopping point? (Never trap players.)
-------------------------------------------------
```

**Timescale 4: The Progression Loop (Full Game)**

The macro arc across the entire experience.

```
PROGRESSION LOOP TEMPLATE
-------------------------------------------------
Beginning:  What does the player start with? What is their initial capability?
Middle:     How does capability, complexity, or narrative evolve?
Mastery:    When does the player feel like they truly understand the systems?
Endgame:    What does the late game look like? (Avoid content drought.)
Completion: What marks the end? Is there post-completion content?
-------------------------------------------------
```

**Loop Visualization**

Draw each loop as a cycle, not a list. A loop that does not visually cycle back on itself
is a linear sequence, not a gameplay loop.

```
        +--> [ACTION] --+
        |               |
        |               v
   [DECISION]      [FEEDBACK]
        |               |
        |               v
        +-- [REWARD] <--+
```

---

**PHASE 5: Pillars and Boundaries**

*Goal: Define what the game IS and what it IS NOT.*

Pillars are the load-bearing promises of your design. Every mechanic, feature, and piece
of content must trace back to at least one pillar. If a feature does not serve a pillar,
it is either an orphan that should be cut or evidence that you are missing a pillar.

Reference `docs/game-design-theory.md` for the full pillar methodology and use
`@templates/game-pillars.md` to document the pillars formally.

**Exercise 5.1 -- Define 3-5 Pillars**

Each pillar must be:
- **Falsifiable**: You can clearly say whether a feature supports it or violates it
- **Distinct**: No two pillars should overlap significantly
- **Memorable**: One phrase each, not a paragraph
- **Actionable**: The pillar directly guides design decisions

```
PILLAR TEMPLATE
-------------------------------------------------
Pillar          | "Every moment is a meaningful choice"
Supports        | Branching dialogue, build diversity, multiple solutions
Violates        | Linear corridors, optimal builds, single correct answers
Design test     | "Does this feature give the player a real decision?"
-------------------------------------------------
```

Bad pillar examples (too vague to be useful):
- "Fun gameplay" -- everything claims this, it guides nothing
- "Beautiful art" -- an aspiration, not a design constraint
- "Immersive world" -- what does immersive specifically mean for YOUR game?

Good pillar examples:
- "The world reacts to everything" -- falsifiable, testable, guides design
- "Failure teaches, never punishes" -- directly shapes difficulty tuning
- "Every resource has two uses" -- creates tension in every spending decision

**Exercise 5.2 -- Define Anti-Pillars**

What this game explicitly refuses to be:

```
ANTI-PILLAR TEMPLATE
-------------------------------------------------
Anti-Pillar     | "No grinding"
Meaning         | Player power comes from skill and knowledge, never from
                | repeating content for incremental stat increases
Implication     | No XP bars, no level-gated content, no repetitive farming
-------------------------------------------------
```

Anti-pillars prevent scope creep by giving you permission to say no. When someone suggests
a feature, check it against anti-pillars first. Rejection is faster than evaluation.

**Exercise 5.3 -- The Bar Test**

Can you describe this game compellingly in two sentences to a stranger at a bar who does
not play games? If not, the concept is either too complex or too derivative to explain
quickly.

```
BAR TEST TEMPLATE
-------------------------------------------------
"It's a game where you [core verb] [in what context].
 The twist is [what makes it unique]."

Rules:
- No jargon ("roguelike deckbuilder" means nothing to a non-gamer)
- No comparisons ("it's like X meets Y" is a crutch)
- Must provoke a follow-up question ("how does that work?")
-------------------------------------------------
```

If the bar test produces a flat response, the concept needs a sharper hook.

---

**PHASE 6: Player Type Validation**

*Goal: Verify that the concept serves identifiable player motivations.*

A game designed for everyone appeals to no one. Identify your primary audience by their
psychological motivations, not their demographics.

**Exercise 6.1 -- Bartle Type Mapping**

Map the concept against the four Bartle types (reference `docs/game-design-theory.md`):

```
BARTLE MAPPING
-------------------------------------------------
Type        | How your game serves them     | Priority
-------------------------------------------------
Achievers   | [specific systems]            | [Primary/Secondary/Not served]
Explorers   | [specific systems]            | [Primary/Secondary/Not served]
Socializers | [specific systems]            | [Primary/Secondary/Not served]
Killers     | [specific systems]            | [Primary/Secondary/Not served]
-------------------------------------------------
```

**Exercise 6.2 -- Self-Determination Theory Check**

Does the concept satisfy the three basic psychological needs?

```
SDT VALIDATION
-------------------------------------------------
Need         | How your game delivers it          | Strength
-------------------------------------------------
Autonomy     | [player agency, meaningful choice] | [Strong/Moderate/Weak]
Competence   | [skill expression, mastery curve]  | [Strong/Moderate/Weak]
Relatedness  | [connection, shared experience]    | [Strong/Moderate/Weak]
-------------------------------------------------
```

A concept does not need to be strong in all three, but it needs to be strong in at least
one and should not actively undermine any of them.

**Exercise 6.3 -- Explicit Exclusions**

Who are you NOT designing for? Name them and accept the tradeoff.

```
EXCLUSION ACKNOWLEDGMENT
-------------------------------------------------
"This game is NOT for players who want [specific experience], because
 our pillars explicitly prioritize [alternative experience] instead."
-------------------------------------------------
```

This is not about gatekeeping. It is about focus. A game that tries to serve competitive
PvP players AND relaxing sandbox players will satisfy neither.

---

**PHASE 7: Scope and Feasibility**

*Goal: Ground the concept in reality. What can actually be built?*

This is where enthusiasm meets arithmetic. The concept from Phases 1-5 must survive
contact with the team's actual capacity, timeline, and technical skill level.

**Exercise 7.1 -- Vertical Slice Definition**

The vertical slice is the minimum playable proof of concept that demonstrates the core
loop works. It is not a demo. It is not a polished product. It is evidence that the
fundamental gameplay is worth building more of.

```
VERTICAL SLICE SCOPE
-------------------------------------------------
Must include:
- The complete 30-second loop, playable
- Enough content to demonstrate the 5-minute loop once
- Placeholder art and audio (programmer art is fine)
- One complete player decision cycle
- Basic game feel (responsive controls, clear feedback)

Must NOT include:
- Full progression system
- Multiple levels/areas
- Polished UI
- Story/narrative beyond setup context
- Monetization features
- Multiplayer (unless the core loop requires it)
-------------------------------------------------
```

**Exercise 7.2 -- Feature Tiering**

Categorize every identified feature into four tiers using the MoSCoW method:

```
FEATURE TIERS
-------------------------------------------------
MUST-HAVE (pillar features -- the game does not exist without these)
- [feature] --> supports [pillar]
- [feature] --> supports [pillar]

SHOULD-HAVE (enhancers -- significantly better with these, but playable without)
- [feature] --> enhances [pillar]

COULD-HAVE (polish -- nice if time permits, cut without guilt)
- [feature]

WON'T-HAVE (explicitly deferred -- do not build these in v1, no matter what)
- [feature] --> why it's deferred
-------------------------------------------------
```

The Won't-Have list is as important as the Must-Have list. It gives the team permission to
say "we already decided not to do that" when scope creep shows up wearing a clever disguise.

**Exercise 7.3 -- Timeline Estimation**

Rough timeline based on team capacity:

```
TIMELINE ESTIMATE
-------------------------------------------------
Phase             | Duration      | Milestone
-------------------------------------------------
Concept document  | 1 week        | Concept doc complete, reviewed
Vertical slice    | 4-8 weeks     | Core loop playable, pillar tested
Alpha             | [team-dependent] | All Must-Have features functional
Beta              | [team-dependent] | Feature-complete, bug fixing begins
Release           | [team-dependent] | Polished, tested, store-ready
-------------------------------------------------

Apply reality checks:
- Solo dev: multiply estimates by 1.5 (context switching overhead)
- First game: multiply estimates by 2.0 (learning curve)
- Unfamiliar engine: add 2-4 weeks of ramp-up time
- Part-time team: convert to calendar time using actual available hours
```

**Exercise 7.4 -- Risk Identification**

Name the top 5 risks and how you will handle each:

```
RISK REGISTER
-------------------------------------------------
Risk              | Probability | Impact | Mitigation
-------------------------------------------------
[technical risk]  | H/M/L       | H/M/L  | [specific plan]
[content risk]    | H/M/L       | H/M/L  | [specific plan]
[scope risk]      | H/M/L       | H/M/L  | [specific plan]
[team risk]       | H/M/L       | H/M/L  | [specific plan]
[market risk]     | H/M/L       | H/M/L  | [specific plan]
-------------------------------------------------
```

### Output Format

The workflow produces a **Game Concept Document** structured as follows.
Reference `templates/game-concept.md` for the full template.

```markdown
# Game Concept Document

## Identity
- **Working Title:** [name]
- **Genre:** [genre or genre-blend]
- **Platform:** [target platforms]
- **Team Size:** [number and roles]
- **Target Duration:** [expected play time]

## The Pitch
**Elevator Pitch (2 sentences):**
[The bar test sentences]

**Core Fantasy:**
[The central experience the player is buying into]

**Unique Hook:**
[What makes this different from everything else in the genre]

## Emotional Foundation
[Themes and feelings from Phase 1, with references]

## Market Validation
[Market sizing, competitive analysis, and validation gate results from Phase 3]

## Core Loop
[All four timescales from Phase 4, with cycle diagrams]

## Design Pillars
[3-5 pillars with support/violate examples from Phase 5]

## Anti-Pillars
[What the game refuses to be]

## Target Aesthetics (MDA)
[Primary and secondary aesthetics from Phase 2/6]

## Player Type Alignment
[Bartle mapping and SDT validation from Phase 6]

## Feature Tiers
[MoSCoW breakdown from Phase 7]

## Vertical Slice Plan
[Scope and definition from Phase 7]

## Risk Register
[Top 5 risks with mitigation plans]

## Next Steps
[Recommended immediate actions and workflow sequence]
```

### Quality Criteria

A successful brainstorm session meets all of these:
- The user drove the creative decisions, not the assistant
- At least 3 distinct concepts were generated before selecting one
- The 30-second loop passes the "fun without progression" test
- Market validation is complete -- comparable games identified, gap articulated, validation gates passed
- Pillars are falsifiable and genuinely guide design decisions
- The scope estimate is honest, with explicit Won't-Have items
- The concept can be explained in 2 sentences (bar test passes)
- The vertical slice is achievable within the stated constraints
- Risks are named honestly, not dismissed with optimism
- The concept document is complete enough to hand to a developer who was not
  in the brainstorm session and have them understand what to build
- All framework references (MDA, SDT, Bartle, Flow) are used correctly per
  the definitions in `docs/game-design-theory.md`

### Example Use Cases

1. **"I want to make a game but I have no idea what kind."**
   Start at Phase 1, Exercise 1.1. The Excitement Inventory will surface themes and
   emotions that point toward genres and mechanics organically.

2. **"I have an idea for a puzzle game with gravity mechanics."**
   Skip to Phase 2 to generate variations on the concept, then proceed through
   Phases 3-7 to stress-test, validate, and scope the strongest variant.

3. **"My team wants to brainstorm our next project together."**
   Run the full 6-phase process, using the Constraint Mapping to ground the session
   in the team's actual capacity and the Concept Comparison Matrix to facilitate
   group decision-making without opinion-shouting.

4. **"I keep starting projects and abandoning them. Help me commit."**
   Emphasize Phase 5 (Pillars create commitment through clarity) and Phase 7 (Scope
   honesty prevents the overwhelm that triggers abandonment). The vertical slice
   definition gives a finishable first milestone.

5. **"I love Hades and Slay the Spire. I want to make something in that space."**
   Use Phase 1 Reference Mining to unpack WHY those specific games resonate, then
   Phase 2 Mashup Method to find a unique angle that does not accidentally create
   a clone. The anti-inspiration exercise prevents derivative design.
