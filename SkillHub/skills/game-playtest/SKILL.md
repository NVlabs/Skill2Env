---
name: "game-playtest"
description: >
  Invoke when the user wants to plan, execute, or analyze a structured playtest session
  with behavioral observation. Covers protocol design, observer guides, and data
  synthesis. Triggers on: "playtest", "player feedback", "usability test", "observation
  session", "playtest analysis". Do NOT invoke for QA bug testing (use game-qa-lead) or
  balance tuning (use game-balance-check). Part of the AlterLab GameForge collection.
argument-hint: "[feature or build to test]"
effort: medium
context: fork
allowed-tools: Read, Glob, Grep, Write, AskUserQuestion
version: 1.3.0
---

# AlterLab GameForge -- Structured Playtest Analysis

Playtesting is not asking players if they had fun. It is the disciplined observation of player behavior to identify where the design succeeds and where it fails. The player's mouth lies -- their hands do not. Nintendo has known this for decades: Miyamoto famously watches players silently, trusting their confusion over their compliments. Larian ran thousands of community playtests during BG3's Early Access, and every major system change traced back to behavioral data, not forum polls. This workflow provides a rigorous behavioral observation framework that transforms raw playtest sessions into actionable design insights.

### Purpose & Triggers

**Invoke this workflow when:**
- A build is ready for external eyes and you need structured feedback, not just reactions
- Specific design questions need answering: "Do players understand the crafting system?" not "Is the game good?"
- Onboarding flow needs validation -- can new players learn the core mechanic without a tutorial?
- Difficulty curve assessment -- are players in the flow channel or oscillating between boredom and frustration?
- A new feature has been integrated and its impact on the overall experience is unknown
- Pre-release polish pass needs data on which rough edges matter most to players
- Competitive analysis requires side-by-side comparison with a reference game

**Do NOT use this workflow when:**
- You need to test a raw mechanic in isolation (use `game-prototype` instead)
- The build is so broken that testers will spend most of their time hitting bugs (fix critical bugs first, then playtest)
- You want marketing quotes or positive testimonials (that is PR, not playtesting)

### Critical Rules

1. **Define questions before inviting testers.** Every playtest answers specific questions. "Is it fun?" is not a question -- it is a prayer. "Can players complete the first dungeon without dying more than twice?" is a question. Celeste's playtests asked "can players learn the dash mechanic within the first three screens?" -- specific, observable, actionable.
2. **The facilitator does not play.** You observe. You take notes. You do not help, explain, suggest, or react. Your poker face is a scientific instrument.
3. **Minimum 5 testers per session.** Fewer than 5 and you are collecting anecdotes, not data. Individual player quirks dominate small samples. At 5+ testers, patterns emerge.
4. **Never test with the development team.** They know too much. Their muscle memory, mental models, and context make them incapable of experiencing the game as a new player. Nintendo's internal playtesting teams are deliberately kept away from development discussions so they approach each session cold. Your developers are blind to every onboarding problem they have already internalized.
5. **Behavioral data outranks verbal data.** If a player says "the controls feel fine" but you observed them pressing the wrong button 11 times in a 10-minute session, the behavioral data wins. Always. Larian tracked BG3 playtester behavior at the input level -- they knew which dialogue options players hovered over before choosing, and that hesitation data informed their rewrite of Act 1.
6. **Separate observation from interpretation.** During the session, record what happened. After the session, interpret what it means. Mixing the two in real-time creates confirmation bias.
7. **Reference `docs/game-design-theory.md`** for Flow Theory and MDA Framework when analyzing player engagement and emotional responses.

### Workflow

**Step 1: Pre-Playtest Preparation**

Define the test objectives. Write 3-5 specific questions this playtest will answer. Each question should be:
- Observable (you can determine the answer by watching, not just asking)
- Actionable (the answer directly informs a design decision)
- Scoped (answerable within a single play session)

Good test questions:
- "Do players discover the dodge-roll mechanic organically within the first two encounters?"
- "At what point in the progression curve do players stop voluntarily exploring and start rushing to objectives?"
- "Does the resource scarcity in Act 2 create tension or frustration?"

Prepare the observation sheet. For each test question, define:
- What specific player behaviors indicate success (positive signals)
- What specific player behaviors indicate failure (negative signals)
- Where in the game session to watch most closely (critical observation windows)

Create the per-player tracking form:
```
Player ID: ___
Session Date: ___
Session Duration: ___
Test Build Version: ___

Timestamped Observations:
[MM:SS] [Observation] [Category: Action/Hesitation/Confusion/Emotion/Verbal]

Post-Session Survey Responses:
Q1: ___
Q2: ___
Q3: ___
```

Set up recording infrastructure:
- Screen capture with audio (mandatory -- you will miss things in real-time that the recording catches)
- Face camera if available (facial micro-expressions reveal engagement, confusion, and frustration that players will never verbalize)
- Input logging if your engine supports it (heatmaps of where players click, where they die, where they spend time)
- Ensure recordings are timestamped and synchronized so you can cross-reference player expression with game events

Prepare the test environment:
- Use a consistent hardware setup across all testers (different frame rates and input devices contaminate results)
- Remove development overlays, debug menus, and console access
- Disable any developer shortcuts or god-mode toggles
- Have a clean save state ready so every tester starts from the same point
- Test the recording setup with a dry run before the first tester arrives

Brief your facilitators (if you have helpers):
- Their only job is to observe and record. Not to help. Not to explain. Not to react.
- If a tester asks "What do I do?" the correct response is: "What do you think you should do?"
- If a tester is completely stuck for more than 90 seconds on a non-critical path, they may offer a single neutral hint ("Have you tried interacting with the glowing object?"). Log this as a critical finding.
- Facilitators should not sit directly next to the player. Peripheral awareness of being watched changes behavior. Sit behind and to the side.

**Step 2: During the Playtest -- Silent Observation Protocol**

This is where discipline matters most. You are a scientist. Your personal feelings about the game are irrelevant during this phase.

**Real-time observation categories:**

*Actions* -- What is the player doing?
- Record moment-to-moment decisions. Not just "player fought the boss" but "player circled the boss for 15 seconds before attacking, suggesting they were looking for a weak point or building courage."
- Track navigation patterns. Do players go where you intended? Where do they go instead? Unintended exploration paths reveal what the environment is actually communicating versus what you think it communicates.
- Note input patterns. Button mashing (panic or boredom), deliberate presses (strategic engagement), repeated failed inputs (control confusion).

*Hesitations* -- Where does the player pause?
- A pause before a door means the player is anticipating what is behind it (good -- you created tension).
- A pause at a menu means the player does not understand the options (bad -- your UI is unclear).
- A pause in combat means the player is either strategizing (good) or overwhelmed (bad). Their facial expression and subsequent action disambiguate.

*Confusions* -- Where does the player misunderstand?
- Track "expectation mismatches" -- moments where the player clearly expected one outcome and got another. These are the highest-value findings in any playtest.
- Note instances where the player uses a mechanic incorrectly but thinks they are using it correctly. This reveals that your feedback systems are not communicating state clearly.
- Watch for players reading the same tooltip or sign multiple times -- it means the information was unclear or they do not trust their own understanding.

*Emotions* -- What is the player feeling?
- **Delight indicators**: leaning forward, widening eyes, spontaneous laughter, "cool" or "whoa" vocalizations, showing the screen to someone nearby
- **Frustration indicators**: sighing, leaning back, crossing arms, clicking more aggressively, muttering, eye-rolling
- **Engagement indicators**: losing track of time, ignoring phone notifications, asking "can I keep playing?" at the end
- **Disengagement indicators**: checking phone, looking around the room, playing with reduced attention, asking "how much longer?"
- **Flow state indicators**: quiet focus, rhythmic input patterns, surprise when told time is up, difficulty recalling specific moments (they were "in it"). Hades playtests reportedly showed players losing 30+ minutes without checking the clock -- the gold standard for flow state confirmation

Map emotional responses to specific game moments. This creates an emotional heatmap of the play session -- where are the peaks and valleys? Compare this to your intended emotional arc from the design document.

**Verbal observations** (think-aloud protocol, if used):
- Record the player's real-time narration without filtering or correcting.
- Flag moments where what the player says contradicts what they are doing -- these are gold. "This is easy" followed by dying three times reveals a gap between perceived and actual skill.

**Step 3: Post-Session Debrief**

Keep it short. 5-7 minutes maximum. The player's attention is most valuable while the experience is fresh, but fatigue sets in quickly after a play session.

Core debrief questions (ask in this order):
1. "What was the game about?" -- tests whether the core fantasy and theme communicated clearly
2. "What were you trying to do most of the time?" -- reveals whether the player understood the primary objective and core loop
3. "Was there a moment that stood out as particularly good?" -- identifies delight peaks from the player's perspective (cross-reference with your observations)
4. "Was there a moment that felt confusing or frustrating?" -- identifies friction from the player's perspective
5. "If you could change one thing, what would it be?" -- reveals the player's top-of-mind pain point

Optional deep-dive questions (only if time permits and the answer informs a test question):
- "Did you feel like you understood what your options were at any given time?" -- tests decision clarity
- "Did the difficulty feel about right, too easy, or too hard?" -- subjective difficulty assessment (triangulate with behavioral data)
- "Was there anything you wanted to do that the game didn't let you?" -- reveals affordance gaps

Do NOT ask:
- "Did you like it?" -- useless. Social pressure ensures a positive answer.
- "Would you buy it?" -- irrelevant at this stage and puts the player in an evaluative mindset that suppresses honest feedback.
- Leading questions: "Did you notice how the lighting changed in the cave?" -- you are feeding them the observation you want.

**Step 4: Post-Playtest Analysis**

Wait at least 2 hours after the last session before analyzing. Immediate analysis is contaminated by recency bias -- the last tester's experience dominates your thinking.

**Cross-player pattern identification:**
- Compile observations into a matrix: rows are game moments/features, columns are players
- Highlight moments where 3+ players exhibited the same behavior -- these are systemic findings, not individual quirks
- Identify divergence points: moments where players split into distinct behavior groups (this reveals a design fork that may need to be resolved or embraced)

**Finding classification:**
Categorize every finding by severity:

| Severity | Definition | Action Required |
|----------|-----------|----------------|
| **Critical** | Breaks the core experience. Player cannot progress, or the intended emotion is inverted (frustration instead of triumph). | Must fix before next playtest. |
| **Major** | Degrades the experience significantly. Player can proceed but the quality of the experience is noticeably diminished. | Should fix in current milestone. |
| **Minor** | Could be better. Player notices but is not significantly impacted. | Fix when convenient, or batch into a polish pass. |
| **Observation** | Interesting behavioral note that does not indicate a problem but may inform future design decisions. | Log for reference. No action required. |

**Recommendation generation:**
For each Critical and Major finding, generate a specific, actionable recommendation:
- What to change (be concrete -- "reduce enemy count in room 3 from 5 to 3" not "make it easier")
- Why it will help (connect the recommendation to the observed behavior)
- Expected impact (what should change in the next playtest if this fix works)
- Potential side effects (will this fix create new problems elsewhere?)

**Longitudinal comparison:**
If prior playtest data exists, compare results across iterations:
- Which findings from the previous playtest were addressed, and did the fixes work?
- Which problems persisted despite attempted fixes (these may be structural, not surface-level)?
- Is the overall trajectory improving? Are you fixing more than you are breaking?

**Step 5: Report Generation and Distribution**

Compile the analysis into the standardized Playtest Report format (see Output Format below). Distribute to the full team with a 2-sentence executive summary at the top -- the lead designer and producer need the headline without reading 10 pages.

### Output Format

```
## Playtest Report: [Build Name / Version]
## Date: [YYYY-MM-DD]
## Facilitator: [Name]
## Testers: [Count] ([demographic notes if relevant])
## Session Duration: [Average across testers]

### Executive Summary
[2 sentences: What was the most important finding? What is the recommended priority action?]

### Test Objectives
1. [Question 1] -- [Answered / Partially Answered / Unanswered]
2. [Question 2] -- [Answered / Partially Answered / Unanswered]
3. [Question 3] -- [Answered / Partially Answered / Unanswered]

### Findings Matrix

| ID | Finding | Severity | Players Affected | Game Moment | Recommendation |
|----|---------|----------|-----------------|-------------|----------------|
| F1 | [desc]  | Critical | 4/5             | [moment]    | [action]       |
| F2 | [desc]  | Major    | 3/5             | [moment]    | [action]       |
| F3 | [desc]  | Minor    | 2/5             | [moment]    | [action]       |

### Emotional Response Map
[Timeline showing emotional peaks and valleys across the session, with game moments annotated]

Opening -> [emotion] -> [event] -> [emotion] -> [event] -> [emotion] -> Close

### Onboarding Assessment
- Core mechanic understood without explanation: [X/5 players]
- Time to first successful use of primary mechanic: [average time]
- Tutorial/hint engagement: [how many players read vs. skipped]
- First death/failure cause: [most common reason]

### Flow Analysis (per docs/game-design-theory.md)
- Estimated flow channel adherence: [percentage of session time in flow]
- Anxiety spikes (challenge > skill): [moments]
- Boredom dips (skill > challenge): [moments]
- Flow entry points: [moments where players appeared to enter flow state]

### Player Behavior Patterns
- **Navigation**: [Where did players go? Where did they NOT go? Where did they get lost?]
- **Combat/Core Loop**: [How did players engage with the primary mechanic?]
- **Exploration**: [What did players investigate voluntarily?]
- **Resource Management**: [How did players handle scarcity/abundance?]

### Comparison to Previous Playtest
| Previous Finding | Status | Notes |
|-----------------|--------|-------|
| [Finding from last time] | Fixed / Improved / Unchanged / Regressed | [details] |

### Prioritized Action Items
1. [Highest priority action] -- addresses findings [F1, F3]
2. [Second priority action] -- addresses finding [F2]
3. [Third priority action] -- addresses finding [F4]

### Raw Observation Notes
[Attached or linked per-player observation sheets]

### Recording Index
| Player | Recording File | Key Timestamps |
|--------|---------------|----------------|
| P1     | [filename]    | [MM:SS notable moments] |
| P2     | [filename]    | [MM:SS notable moments] |
```

### Quality Criteria

- **Question specificity**: Every test objective is observable, actionable, and scoped. No vague "is it fun?" questions survived the planning phase.
- **Observation rigor**: At least 80% of findings are grounded in behavioral data (what players DID), not verbal data (what players SAID). Verbal data is supporting evidence, not primary evidence.
- **Pattern validity**: Findings classified as systemic (Major or Critical) are supported by observations from at least 3 out of 5 testers. Single-player observations are classified as Minor or Observation.
- **Recommendation concreteness**: Every Critical and Major finding has a specific, implementable recommendation -- not "make it better" but "reduce the number of enemies in room 3 from 5 to 3 and add a health pickup before the encounter."
- **Longitudinal tracking**: The report includes comparison to at least one prior playtest (if one exists), tracking whether previous findings were addressed and whether fixes were effective.
- **Emotional mapping**: The report includes an emotional response map showing where delight and frustration occurred in the session timeline, cross-referenced with specific game events.
- **Facilitator neutrality**: The report documents any instances where the facilitator intervened (explained, helped, hinted) and flags those moments as potentially contaminated data.

### AI Playtesting Agents

Human playtesting remains the gold standard for evaluating player experience, but AI playtesting agents can supplement human sessions by providing coverage, regression testing, and overnight stress testing that would be impractical to do with human testers.

**nunu.ai Pattern:**
Define test goals in plain English (e.g., "complete the tutorial without dying," "find and defeat the boss in level 3," "attempt to sequence-break past the locked door"). AI bots execute overnight, producing session recordings and behavioral logs. Use this for:
- Regression testing after balance changes (did this patch break the tutorial completion rate?)
- Coverage testing (can any path through the level design lead to a softlock?)
- Stress testing (what happens when 100 agents play simultaneously in a multiplayer environment?)

**modl.ai Pattern:**
Autonomous test bots that explore your game without specific goals, mapping reachable states and identifying areas where the bot gets stuck. Use this for:
- Pathfinding validation (are there navigation mesh holes?)
- State machine integrity (can the bot reach an unrecoverable state?)
- Content coverage (what percentage of the level geometry is actually reachable?)

**What AI Testing Cannot Replace:**
- Emotional response measurement (delight, frustration, engagement)
- Aesthetic evaluation (does this FEEL good?)
- Social dynamics in multiplayer (AI cannot replicate human social behavior)
- First-impression testing (AI has no expectations to violate)

Use AI testing for coverage and regression. Use human testing for experience and emotion. Never substitute one for the other.

### Structured Session Planning Template

Before any playtest session, complete this planning template to ensure focus and reproducibility:

```
SESSION PLAN
Date: [YYYY-MM-DD]
Build Version: [version string]
Session Type: [First Impression / Targeted Feature / Regression / Full Playthrough]
Duration: [planned session length per tester]
Tester Count: [number of testers scheduled]

Test Questions (max 5):
1. [Specific, observable, actionable question]
2. [Specific, observable, actionable question]
3. [Specific, observable, actionable question]

Focus Areas:
- [Game section or feature under scrutiny]
- [Specific interaction or flow to observe]

Recording Setup:
- Screen capture: [tool and settings]
- Face camera: [available / not available]
- Input logging: [enabled / not available]

Facilitator Notes:
- [Any special instructions for this session]
- [Known issues to ignore during testing]
```

### Four-Question Playtest Focus

When time is limited or you need a rapid signal from testers, reduce the debrief to these four questions. They are ordered to surface the highest-value insights with minimal tester fatigue:

1. **"What confused you?"** -- Identifies onboarding failures, unclear mechanics, and communication gaps. Confusion is the most actionable finding because it points directly to specific moments that need redesign.
2. **"When were you bored?"** -- Identifies pacing dead zones, reward gaps, and content that fails to engage. Boredom is harder to detect through observation alone because bored players often continue playing out of politeness.
3. **"When did you want to stop?"** -- Identifies frustration peaks, fatigue walls, and the natural session length for your game. The difference between "I wanted to stop at the boss" and "I wanted to stop during the inventory management" reveals which systems are friction sources.
4. **"What would you show a friend?"** -- Identifies delight peaks and the game's natural marketing hook. Whatever the tester would show a friend is the moment your trailer should lead with and your store page should emphasize.

These four questions replace the longer debrief when session time is constrained. They are not a substitute for full behavioral observation during the session itself.

### Remote Playtesting Setup

Most indie developers cannot run in-person sessions consistently. Remote playtesting is the realistic default and has specific requirements:

**Recording infrastructure:**
- Ask testers to install OBS or use the built-in recording in their OS (Xbox Game Bar on Windows, QuickTime on macOS). Provide written setup instructions in advance -- do not spend the session troubleshooting recording software.
- Request front-facing webcam footage if the tester consents. Most do. Even a low-quality webcam captures the emotional responses that drive the highest-value findings.
- Use Discord, Zoom, or Google Meet for audio. Keep your own mic muted during observation. Hearing yourself breathing changes tester behavior.
- Use a private itch.io link, Steam early access key, or direct download for build distribution. Never email executables -- they get flagged by security software and contaminate first impressions.

**Session control:**
- Block 90 minutes: 10 minutes setup, 60 minutes play, 20 minutes debrief. Testers who run long naturally truncate debrief quality.
- Use a shared document or form to capture the debrief so you are not transcribing in real-time. Google Forms works well for standardized questions; a shared Google Doc works well for open-ended responses.
- For asynchronous remote testing, provide a structured observation prompt: "After you finish, write down: one moment that surprised you, one moment you felt confused, and one moment where you felt especially engaged. Do not overthink it -- raw reactions are more valuable than considered ones."

**What remote testing cannot capture:**
- Genuine facial micro-expressions without webcam (which some testers decline)
- Physical environment context (distractions, hardware quality, sound environment)
- True cold-start behavior if testers have seen screenshots or trailers

Remote testing works well for mid-development playtests where the goal is identifying specific friction points. For first-impression testing of core onboarding, in-person sessions with a facilitator present are preferable when feasible.

### Finding Evidence Thresholds

Avoid the trap of calling a finding "Critical" because one tester had a strong reaction. Apply these evidence thresholds before classifying:

| Severity | Minimum Evidence Standard |
|----------|--------------------------|
| **Critical** | 4 or more of 5 testers exhibited the behavior, OR 1 tester experienced a complete session-ending failure (crash, softlock, cannot proceed) |
| **Major** | 3 or more of 5 testers showed the behavior, with behavioral confirmation (not just verbal report) |
| **Minor** | 2 of 5 testers noted it verbally, OR 1 tester showed behavioral evidence |
| **Observation** | Any smaller signal worth logging for future reference |

When evidence is ambiguous (e.g., 2 testers showed a behavior and 3 did not), note the split explicitly in the report. A 2/5 signal is not a finding to act on immediately -- it is a finding to watch in the next playtest. If it appears again in the next session, it escalates to Major.

### Example Use Cases

1. "We just finished our first playable build. Help me plan a structured playtest session -- what questions should I be asking and how do I set up observation?"
2. "I ran a playtest last week and took notes on 6 players. Here are my raw observations -- help me analyze the data and generate a prioritized findings report."
3. "Players keep dying in the same spot in level 3. I think it's a difficulty spike but I'm not sure. Help me design a targeted playtest to diagnose the problem."
4. "We changed our control scheme based on last month's playtest feedback. Help me design a follow-up test to see if the changes actually fixed the issues we identified."
5. "Our game has a 20-minute onboarding sequence and I suspect we're losing players before they reach the core loop. Help me set up a first-time user experience playtest with specific metrics to track."
6. "I'm a solo developer and can't run in-person sessions. Help me set up a remote playtest for my action RPG using Discord and OBS."
7. "I have 6 playtest reports from three separate sessions over the past 2 months. Help me identify which findings have been persistent across sessions vs. which ones were one-time observations."
