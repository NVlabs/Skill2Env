---
name: "game-prototype"
description: >
  Invoke when the user wants to rapidly prototype a mechanic, test a proof of concept,
  run hypothesis-driven development, or validate a game idea before full production.
  Triggers on: "prototype", "proof of concept", "test this mechanic", "validate idea",
  "rapid prototype", "bake-off". Do NOT invoke for starting a full project (use
  game-start) or brainstorming concepts (use game-brainstorm). Part of the AlterLab
  GameForge collection.
argument-hint: "[mechanic to prototype]"
effort: medium
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, AskUserQuestion
version: 1.3.0
---

# AlterLab GameForge -- Hypothesis-Driven Prototyping

Prototypes are experiments, not demos. Every prototype exists to answer one question: "Is this worth building?" The moment you start polishing a prototype, you have stopped prototyping and started building -- and you may be building the wrong thing. Undertale's original demo was rough, ugly, and proved exactly one thing: the bullet-hell-meets-RPG mechanic was worth a full game. Hollow Knight started as a game jam prototype that validated tight combat in an atmospheric 2D world. Celeste began as a PICO-8 prototype that proved a single idea: precise air-dash platforming feels incredible at 8x8 pixel resolution. This workflow enforces that same discipline: define a hypothesis, build the minimum viable test, observe real players, make a binary kill-or-promote decision based on evidence.

### Purpose & Triggers

**Invoke this workflow when:**
- A team member proposes a new mechanic and the response should be "prove it" rather than "ship it"
- The design document contains an assumption that has never been tested with real players
- Two competing mechanic designs need a head-to-head bake-off to determine which one feels better
- A feature sounds good on paper but the team has no visceral sense of whether it will be fun
- Pre-production needs to validate core loops before committing engineering resources
- A pivot is being considered and the new direction needs rapid feasibility confirmation

**Do NOT use this workflow when:**
- The mechanic is well-understood and already validated in similar games (just build it properly)
- You need a vertical slice for stakeholder presentation (that is a demo, not a prototype)
- The question is about content, not mechanics (content questions need playtesting, not prototyping)

### Critical Rules

1. **One hypothesis per prototype.** If you are testing two things, you have two prototypes. Combining hypotheses contaminates your results -- when it fails, you will not know which part failed.
2. **Time-box or die.** Every prototype gets a strict time limit: 1-3 days maximum. If the hypothesis cannot be tested in that window, the scope is too large. Decompose it further.
3. **Prototype code is biohazard.** It does not graduate to production. Ever. When a hypothesis is validated, the real implementation starts from scratch with proper architecture. Letting prototype code leak into production is how technical debt is born. Celeste's PICO-8 prototype shared zero code with the final game -- it proved the feel, then the real build started clean.
4. **Ugly is correct.** Colored rectangles for characters. Placeholder sounds. Programmer art. Comic Sans labels. If anyone comments on the visual quality of a prototype, they have misunderstood its purpose. The Hollow Knight game jam prototype used simple silhouettes -- the atmosphere came later, the feel came first.
5. **Observe behavior, not opinions.** Players will tell you what they think you want to hear. Watch what they DO. A player who says "yeah it was fine" but leaned forward and played for 20 minutes straight is giving you different data than their words suggest.
6. **Kill without sentiment.** If the evidence says the hypothesis is false, the prototype dies. It does not matter how clever the idea was, how much you personally like it, or how much time you spent building it. Supergiant kills prototypes constantly -- their GDC talks reveal dozens of dead mechanics that never made it past the test phase because the team trusts evidence over attachment.
7. **Always reference `docs/game-design-theory.md`** for shared theoretical frameworks (MDA, Flow Theory, SDT) when formulating hypotheses about player experience.

### Workflow

**Step 1: Define the Hypothesis**

Write the hypothesis in this exact format: "We believe that [mechanic/system] will produce [player behavior/emotion] when [specific condition]."

Then define falsification criteria -- what evidence would DISPROVE the hypothesis? This is the most important part. If you cannot define what failure looks like, your hypothesis is unfalsifiable and therefore untestable.

Examples of strong hypotheses:
- "We believe that a grappling hook with momentum preservation will make traversal feel exhilarating when the player chains three or more swings without touching the ground."
- "We believe that asymmetric co-op roles (one player builds, one player defends) will produce emergent communication when the builder can see threats the defender cannot."
- "We believe that a stamina system with visible recovery will create tactical tension when the player faces two enemies and cannot defeat both without resting."

Examples of weak hypotheses (and why):
- "The combat will be fun" -- unfalsifiable. What is fun? Under what conditions? For whom?
- "Players will like the art style" -- this is a content question, not a mechanic question. You do not need a prototype for this.
- "The game will be better with multiplayer" -- too broad. Which specific multiplayer interaction? What does "better" mean measurably?

Map the hypothesis to the MDA framework from `docs/game-design-theory.md`: which aesthetic are you targeting (Sensation, Fantasy, Narrative, Challenge, Fellowship, Discovery, Expression, Submission)? This grounds the hypothesis in established theory and helps you define what success looks like.

**Step 2: Scope Ruthlessly**

Ask: "What is the absolute minimum implementation that tests this hypothesis?" Then cut it in half.

You do not need:
- A menu system. Start the prototype in the test scenario directly.
- Multiple levels. One room, one encounter, one situation.
- Save/load functionality. Nobody is playing this for more than 10 minutes.
- Audio. Unless audio IS the hypothesis (e.g., testing rhythm-based mechanics).
- Any UI beyond what the player needs to understand the core interaction.
- Animations. Lerp between states. Snap to positions. Teleport if you must.
- Edge case handling. If a player finds a bug in a prototype, congratulations -- they are exploring. Note it and move on.

You DO need:
- The core input-to-feedback loop working at full speed. If the hypothesis is about how a mechanic FEELS, input latency and response timing must be representative.
- Enough game state to test the hypothesis. If you are testing resource management tension, you need at least a minimal economy that creates scarcity.
- A way to reset quickly. Testers will play multiple rounds. A 30-second restart cycle kills your testing velocity.

Create a scope checklist with exactly three columns:
| Must Have (tests hypothesis) | Nice to Have (improves test clarity) | Out of Scope (save for production) |

If the "Must Have" column has more than 5 items, you have not scoped ruthlessly enough. Go back and decompose.

**Step 3: Build Dirty**

This is the only time in your career when bad code is the correct code.

- Hardcode everything. Magic numbers everywhere. No config files. No data-driven anything.
- One script file if you can manage it. No architecture. No separation of concerns. No design patterns.
- Copy-paste instead of abstracting. You are writing code that will be deleted in 72 hours.
- Use the fastest path to playable, even if that means ignoring every best practice you know.
- If your engine has a visual scripting system (Blueprints, Bolt, VisualScript), use it -- faster iteration for throwaway logic.
- Commit nothing to the main repository. Prototype code lives in a throwaway branch or a separate folder that will be deleted after the decision.

The build phase should consume no more than 60% of your time budget. If you are spending 2 of your 3 days building, you have 0.5 days for testing and 0.5 days for analysis. That is not enough. Target a 40/30/30 split: 40% build, 30% test, 30% analyze.

**Step 4: Structured Evaluation**

Do NOT test alone. Your own assessment of your own prototype is the least valuable data you can collect.

Minimum viable test: 3-5 people who are NOT on the development team play the prototype while you observe silently.

Observation protocol:
- **Silent observation only.** Do not explain, help, hint, or react. If the player is confused, note what confused them and why. If they are stuck, note where and let them struggle for at least 60 seconds before offering any guidance (and note that you had to intervene -- that is a finding).
- **Record everything.** Screen recording at minimum. Face camera if available. Verbal think-aloud protocol if the player is comfortable with it.
- **Track time-stamped events:** moments of visible frustration, moments of visible delight, moments of confusion, moments where the player pauses to think (strategic engagement), moments where the player disengages (checks phone, looks away).
- **Post-session questions** (keep to 3-5 questions max):
  1. "What were you trying to do?" (tests comprehension of the core mechanic)
  2. "Was there a moment that felt really good?" (identifies delight peaks)
  3. "Was there a moment that felt frustrating?" (identifies friction points)
  4. "Would you play this again?" (blunt retention signal -- their body language while answering matters more than the words)

Apply the Flow Theory lens from `docs/game-design-theory.md`: did the player appear to enter a flow state? Was the challenge-skill balance in the right zone? Did they experience anxiety (challenge too high) or boredom (challenge too low)?

**Step 5: Kill or Promote Decision**

This is a binary decision. There is no "maybe" and there is no "let's iterate on the prototype." Either the hypothesis was validated or it was not.

**KILL criteria (any one is sufficient):**
- Fewer than 2 out of 5 testers exhibited the target behavior/emotion
- The core interaction does not produce the intended feeling even when it works correctly
- The mechanic requires extensive explanation to be understood (indicates it will not onboard naturally)
- The "fun" came from a secondary interaction, not the one you were testing (the hypothesis was wrong about what would be engaging)
- Players found a degenerate strategy that makes the intended interaction unnecessary

**PROMOTE criteria (all must be met):**
- At least 3 out of 5 testers exhibited the target behavior/emotion without prompting
- The core interaction produces the intended feeling reliably, not just occasionally
- At least one tester said something equivalent to "can I play again?" unprompted
- No degenerate strategy was discovered that trivializes the core challenge
- The mechanic aligns with at least one design pillar (check against the project's vision document)

When you KILL a prototype:
- Document what you learned. The failed experiment has value -- it eliminated a possibility.
- Share the findings with the team. Failed prototypes prevent future teams from testing the same dead-end.
- Delete the prototype code. Not archive -- delete. Its purpose is served.

When you PROMOTE a prototype:
- Write a design brief for the production implementation. Specify what the prototype proved and what still needs design work.
- The production implementation starts from zero. No prototype code carries forward.
- Identify the open questions the prototype did NOT answer (there will always be some) and plan playtests to address them.

### Output Format

```
## Prototype Report: [Prototype Name]
## Date: [YYYY-MM-DD]
## Time Budget: [X days allocated, Y days used]

### Hypothesis
[Full hypothesis statement in the required format]

### Falsification Criteria
[What evidence would disprove this hypothesis]

### MDA Alignment
- Target Aesthetic: [which MDA aesthetic this tests]
- Relevant Design Pillar(s): [which project pillars this serves]

### What Was Built
[2-3 sentence description of the prototype]
[Screenshots or video links]

### Scope Decisions
| Must Have | Nice to Have | Out of Scope |
|-----------|-------------|--------------|
| [items]   | [items]     | [items]      |

### Observation Notes
| Tester | Key Observations | Delight Moments | Friction Points | Flow State? |
|--------|-----------------|-----------------|-----------------|-------------|
| P1     | [notes]         | [moments]       | [points]        | [Y/N/Partial] |
| P2     | [notes]         | [moments]       | [points]        | [Y/N/Partial] |
| ...    |                 |                 |                 |             |

### Evidence Assessment
**For the hypothesis:**
- [Observation supporting the hypothesis]
- [Observation supporting the hypothesis]

**Against the hypothesis:**
- [Observation contradicting the hypothesis]
- [Observation contradicting the hypothesis]

### Decision: [KILL / PROMOTE]
**Reasoning:** [2-3 sentences explaining the decision based on evidence]

### Lessons Learned
- [Insight 1 -- applicable beyond this prototype]
- [Insight 2]
- [Insight 3]

### Next Steps
- If KILL: [What alternative approaches might work, or what to test next]
- If PROMOTE: [Design brief summary for production implementation, open questions remaining]
```

### Quality Criteria

- **Hypothesis clarity**: Could a stranger read the hypothesis and understand exactly what is being tested? If it requires context or jargon, it is not clear enough.
- **Scope discipline**: Was the prototype built in less than 60% of the time budget, leaving sufficient time for testing and analysis?
- **Evidence quality**: Are the observations behavioral (what players DID) rather than attitudinal (what players SAID)? Behavioral evidence is worth five times attitudinal evidence.
- **Decision integrity**: Does the kill/promote decision follow logically from the evidence? Could you defend it to a skeptic using only the observation data?
- **Learning extraction**: Does the report contain at least one insight that applies beyond this specific prototype? Every experiment should teach you something about your game, your players, or game design itself.
- **Anti-pattern avoidance**: The report should explicitly note if any anti-patterns were triggered during the process (scope creep, polish temptation, prototype-to-production leak).

### Hypothesis-to-MDA Mapping Reference

Use this quick-reference to ensure your hypothesis targets a specific player aesthetic from the MDA framework (`docs/game-design-theory.md`). Hypotheses that do not map to a named aesthetic are usually either too vague or testing a technical question rather than a design question.

| MDA Aesthetic | Prototype Tests For | Example Hypothesis Signal |
|---------------|--------------------|-----------------------------|
| **Sensation** | Moment-to-moment feel — juice, game feel, feedback responsiveness | Player leans forward, comments on how something "feels" unprompted |
| **Fantasy** | Role embodiment — does the player feel like the character? | Player uses "I" language: "I felt powerful when I did that" |
| **Narrative** | Story comprehension and investment | Player asks what happens next; player makes decisions based on story logic |
| **Challenge** | Difficulty calibration, fair failure | Player retries immediately without frustration; says "I almost had it" |
| **Fellowship** | Social interaction quality in multiplayer | Players communicate spontaneously; laughter and negotiation |
| **Discovery** | Exploration motivation and reward | Player moves away from the critical path voluntarily |
| **Expression** | Player creativity and personalization | Player makes choices that reflect identity, not just optimization |
| **Submission** | Idle engagement, low-stakes repetition | Player enters a quiet, rhythmic state; relaxed body language |

If your hypothesis maps to multiple aesthetics, you have combined questions. Split the hypothesis.

### Anti-Patterns to Watch For

**"Let me just clean up the prototype a bit."**
No. You are not cleaning it up. You are emotionally investing in throwaway code. Stop. If the hypothesis is validated, you will build it properly from scratch. If it is not validated, you just wasted time polishing something destined for the trash.

**"The prototype works, let's just ship it."**
No. Prototype architecture does not scale. Prototype code has no error handling, no edge cases, no accessibility, no localization hooks, no save system, no telemetry. Shipping a prototype is how you create a game that technically runs but collapses the moment you try to add content or fix bugs.

**"Let me add one more feature to the prototype."**
No. You are scope creeping. The hypothesis was defined in Step 1. If testing that hypothesis requires features you did not anticipate, either your hypothesis was poorly scoped or you are testing a different question than the one you started with. Go back to Step 1.

**"We need more data -- let's test with 20 people."**
No, not at the prototype stage. 3-5 testers is sufficient for a binary signal. If 5 people play it and the results are ambiguous, the answer is probably "kill" -- a strong mechanic is obvious even to a small sample.

**"It didn't work but I think with more time..."**
The sunk cost fallacy is the most expensive bias in game development. If 3 days could not validate the hypothesis, more time will not help. Either the hypothesis is wrong, or the scope is too large. Reformulate and try again with a tighter focus.

### Prototype Fidelity Levels

Not every prototype needs to be digital. Choose the fidelity level that answers the hypothesis fastest:

| Level | Method | Best For | Time Cost | Realism |
|-------|--------|----------|-----------|---------|
| **Paper** | Index cards, dice, tokens on a table | Turn-based mechanics, economy systems, card game loops, board-like structures | Hours | Low — but fast to iterate |
| **Tabletop Digital** | Spreadsheet simulation or dice-roller scripts | Balance testing, probability distributions, progression math | 1-2 hours | Medium for numbers, zero for feel |
| **Digital Throwaway** | One scene, hardcoded values, programmer art | Real-time feel, input-to-feedback loops, spatial mechanics | 1-3 days | High for feel, low for content |
| **Polish Prototype** | Cleaned-up throwaway with placeholder art | Stakeholder review, investor demo, team morale validation | 1 week | High |

**Decision rule:** Start at the lowest fidelity level that can test your hypothesis. A stamina-system economy can be validated with a spreadsheet in 30 minutes. A grappling-hook feel requires a digital prototype. Jumping to digital when paper would work wastes 80% of the time budget.

### Competitive Bake-Off Protocol

When two competing designs exist, test both simultaneously rather than sequentially. Sequential testing introduces temporal variables (tester mood, team familiarity with the space, external events). Simultaneous testing isolates the design variable.

**Setup:**
1. Build both implementations to the minimum scope required to test the hypothesis.
2. Divide testers into two groups (minimum 3 per group, so minimum 6 testers total).
3. Each group plays only one version -- no tester plays both during the same session.
4. Use identical observation protocols and debrief questions for both groups.
5. The researchers do NOT know which version a tester is playing during the debrief (blind evaluation where possible).

**Analysis:**
- Compare behavioral data first (flow state duration, hesitation counts, emotional peaks). Verbal data is secondary.
- If one version produces clearly stronger behavioral signals, it wins regardless of which design the team prefers.
- If results are inconclusive (both versions score similarly), the hypothesis was not differentiated enough. Refine both designs and test again.
- Document what each version proved, even the losing one -- the loser often teaches more than the winner.

**Anti-pattern alert:** Do not let the team vote on which version is better after watching testers. Team preference is contaminated by authorship bias. Let the behavioral data decide.

### Solo Developer Adaptation

Solo developers face a structural problem: you cannot observe yourself playing your own prototype objectively. Your workarounds:

1. **Time-shifted testing.** Build the prototype, then wait 48 hours before playing it yourself. Your memory will have faded enough that you approach it more like a new player. This is not ideal but better than testing immediately after building.
2. **Record yourself.** Play with a screen recorder running. Watch the recording the next day with the clinical eye of an observer. Treat the recording as if it were a different person playing. You will see things you did not notice while playing.
3. **Minimum 3 external testers, no exceptions.** Solo dev status is not an excuse for skipping external testing. Even 3 testers from your family, friends, or local indie dev community generate better signal than self-testing. Your game must eventually be played by people who are not you.
4. **Online testing platforms.** For remote testing, use OBS + Discord screen share, or platforms like itch.io private access links. Remote testers sacrifice face-camera data but provide authentic cold-start behavior.
5. **Apply the 30% solo buffer.** Prototype time budgets for solo developers should use 30% overhead (not 20%) because you carry every discipline cost: design, build, test facilitation, and analysis. A "3-day prototype" for a solo dev is effectively 2.1 productive days of focused work.

### Pre-Build Checklist

Before writing a single line of prototype code, verify these conditions are met. If any are missing, stop and resolve them first:

- [ ] **Hypothesis is written** in the required format: "We believe that [mechanic] will produce [behavior/emotion] when [condition]."
- [ ] **Falsification criteria are defined**: you can name at least two observable signals that would prove the hypothesis false.
- [ ] **MDA aesthetic is identified**: you know which of the eight aesthetics this test targets.
- [ ] **Time box is set**: you have a fixed end date, not "whenever it feels done."
- [ ] **Scope checklist is complete**: Must Have / Nice to Have / Out of Scope columns are populated with specific items.
- [ ] **Testers are scheduled**: you have names and times for at least 3 external players before you begin building.
- [ ] **Recording setup is tested**: your screen capture software works on a test recording before the prototype exists.
- [ ] **Prototype branch is created**: you are not building on main. This is the physical enforcement of "prototype code does not graduate."

This checklist exists because the build phase is the most seductive part of prototyping. The pull to start building before the hypothesis is clear is powerful and almost always leads to scope creep and ambiguous results. Spending 20 minutes on this checklist saves 2 days of wasted work.

### Example Use Cases

1. "I want to test whether a rewind mechanic feels satisfying in a platformer. Set up a prototype hypothesis and scope for me."
2. "We have two competing designs for our combat system -- turn-based with action elements versus real-time with pause. Help me design a bake-off prototype for both."
3. "Our GDD assumes players will enjoy a base-building loop between dungeon runs, but nobody on the team has tested this assumption. Walk me through prototyping it."
4. "I built a prototype for our grappling hook mechanic and tested it with 4 people. Here are my notes -- help me analyze the results and make a kill/promote decision."
5. "We validated our core combat loop last sprint. Now I need to prototype the progression meta-layer. Help me define the hypothesis and scope."
6. "I'm a solo developer. I built a prototype last week and just got 3 testers to try it. Two of them seemed bored and one seemed confused. Help me interpret whether this is a kill or a conditional promote."
7. "We need to validate two competing economy designs -- a fixed-cost crafting system vs. a variable-cost bidding system. Walk me through designing a paper prototype bake-off."
