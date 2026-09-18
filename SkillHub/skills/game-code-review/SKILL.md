---
name: "game-code-review"
description: >
  Invoke when the user wants a game-specific code review, architecture check, or
  technical analysis of game code. Covers frame independence, hot path performance,
  state machine integrity, and resource lifecycle. Triggers on: "code review", "review
  my code", "check architecture", "game code quality". Do NOT invoke for design
  document review (use game-design-review) or general sprint planning (use
  game-sprint-plan). Part of the AlterLab GameForge collection.
argument-hint: "[file or directory to review]"
effort: high
context: fork
allowed-tools: Read, Glob, Grep, Write, Edit, AskUserQuestion
version: 1.3.0
---

# AlterLab GameForge -- Game Code Review Workflow

Game code has failure modes that web code does not. A web app that allocates memory in a request handler costs you some latency. A game that allocates memory in an update loop costs you frame drops that players feel in their hands. A web app with a state management bug shows stale data. A game with a state management bug lets the player walk through walls or fire invisible bullets. Celeste's codebase is legendary precisely because Maddy Thorson and Noel Berry treated frame-perfect input handling as a first-class engineering concern -- and the result is the tightest platformer ever shipped.

This workflow reviews game code through two lenses simultaneously: standard software quality (naming, structure, testing, documentation) and game-specific correctness (frame independence, hot path performance, state machine integrity, resource lifecycle). Both lenses matter. Factorio maintains a million-entity simulation at 60fps because Wube Software treats architecture as a gameplay feature. Ignoring either lens produces code that is either well-structured but broken at runtime, or high-performing but unmaintainable.

### Purpose & Triggers

Use this workflow when:
- A developer asks "review my game code" or "check my architecture"
- Before merging a significant feature branch
- When debugging a performance issue and suspecting structural causes
- When a new developer joins and needs to understand code quality standards
- After prototyping, when deciding which code to promote to production
- When transitioning from prototype to production-quality codebase

Problems this solves:
- Frame rate drops caused by per-frame allocations nobody noticed
- Physics that behave differently at 30fps vs 60fps vs 144fps
- State machines that enter impossible states under edge conditions
- Leaked resources on scene transitions causing gradual memory growth
- Hardcoded gameplay values that require recompilation to tune
- Circular dependencies that make systems impossible to test in isolation
- Raw input handling scattered through gameplay code instead of abstracted

### Critical Rules

1. **Game-specific checks first.** Standard code quality matters, but game-specific issues
   cause harder-to-diagnose failures. A naming convention violation is annoying. A frame-rate-
   dependent physics calculation is a shipped bug on every hardware configuration except
   the developer's machine.

2. **Context-aware severity.** A `new` allocation in a menu screen handler is fine. The same
   allocation in a per-frame particle update is a critical GC pressure point. Always consider
   where code runs before rating severity.

3. **Measure, do not guess.** Do not flag hypothetical performance issues without evidence.
   If something looks expensive, note it as "potential concern -- profile before optimizing."
   Premature optimization is real. So is premature optimization anxiety.

4. **Engine idioms matter.** Each engine has conventions. Godot signals are not Unity events are not Unreal delegates. Review code against the conventions of its engine, not against abstract ideals. Noita's pixel physics system works because Nolla Games wrote to the engine's strengths rather than fighting its architecture. Reference the appropriate engine specialist skill for engine-specific standards.

5. **Gameplay values in data, not code.** Any numeric value that a designer might want to tweak (damage, speed, cooldown, spawn rate, drop chance) must live in a config file or data table, not as a constant in source code. This is non-negotiable -- it is a fundamental game architecture requirement documented in `docs/collaboration-protocol.md`.

6. **Test the untestable.** Game systems are notoriously hard to unit test. Push for testable architecture anyway. If a system cannot be tested because it is tightly coupled to the engine, that coupling is a design smell worth flagging. Factorio's developers maintain comprehensive automated tests for their simulation layer by keeping game logic separate from rendering -- that separation is why they ship with confidence.

### Workflow

**Step 1: Architecture Overview**

Before reading individual files, understand the shape of the codebase.

- Map the major systems (rendering, physics, gameplay, AI, UI, audio, input, networking)
- Identify the dependency graph between systems
- Check for a clear architectural pattern (ECS, component-based, scene tree, MVC variant)
- Note the presence or absence of abstraction layers between gameplay and engine

```
ARCHITECTURE MAP TEMPLATE
-------------------------------------------------
System            | Location          | Dependencies       | Abstracted?
-------------------------------------------------
Game Loop / Core  | [path]            | [all systems]      | Y/N
Player Controller | [path]            | Input, Physics     | Y/N
Enemy AI          | [path]            | Pathfinding, State | Y/N
UI System         | [path]            | Game State         | Y/N
Audio Manager     | [path]            | Events             | Y/N
Save System       | [path]            | Serialization      | Y/N
-------------------------------------------------
```

**Step 2: Game-Specific Code Checks**

These are the checks that distinguish a game code review from a generic code review.
Each check targets a failure mode specific to real-time interactive software.

**Check 2.1 -- Delta Time Usage**

All time-dependent calculations must use delta time (the time elapsed since the last
frame). Without delta time, game behavior changes with frame rate.

```
DELTA TIME AUDIT
-------------------------------------------------
FIND: Any += or -= in update/process/tick functions without * delta
FLAG: position += speed (WRONG: frame-rate dependent)
FIX:  position += speed * delta_time (CORRECT: frame-rate independent)

Also check:
- Timers that count frames instead of elapsed time
- Animation speed tied to frame rate
- Cooldowns that expire faster on faster machines
- Velocity calculations that assume fixed frame rate

Severity: CRITICAL when found in gameplay-affecting code
          MINOR when found in cosmetic-only code (particle trails, etc.)
-------------------------------------------------
```

**Check 2.2 -- Hot Path Allocations**

Code that runs every frame must not allocate heap memory. The garbage collector will
eventually reclaim it, but GC pauses cause visible frame drops.

```
HOT PATH ALLOCATION AUDIT
-------------------------------------------------
FIND: new, Array(), Object.create(), .push() growing arrays, string
      concatenation, closures capturing variables, lambda creation --
      in any function called per-frame

FLAG: Allocations in update(), _process(), _physics_process(), Tick(),
      FixedUpdate(), any function called from the main loop

FIX:  Object pooling, pre-allocated arrays, cached references,
      struct-based data (for engines that support it)

Also check:
- Dictionary/Map creation inside loops
- Temporary vector/matrix objects in physics calculations
- String formatting for debug output left in production code
- LINQ queries or functional chain calls in hot paths (C# / Unity)

Severity: CRITICAL in physics or rendering code
          MAJOR in gameplay update code
          MINOR in low-frequency systems (menu transitions, save games)
-------------------------------------------------
```

**Check 2.3 -- State Management**

Game objects typically have complex state (idle, running, jumping, attacking, stunned,
dying, dead). Mismanaged state is the number one source of visual glitches and logical
bugs in games.

```
STATE MANAGEMENT AUDIT
-------------------------------------------------
FIND: Boolean flags controlling behavior (is_jumping, is_attacking, can_move)
FLAG: "Boolean soup" -- multiple booleans that create implicit state combinations,
      some of which are invalid (is_jumping AND is_dead should be impossible)

PREFER: Explicit state machines with defined transitions
  - Enum-based states with switch/match statements
  - State pattern with enter/exit/update per state
  - Hierarchical state machines for complex characters

Also check:
- Can the object enter an invalid state combination?
- Are state transitions guarded (can only go from A to B, not A to D)?
- Is state entry/exit cleanup handled (stop animation on state exit)?
- Are states visualizable for debugging (can you see current state in editor)?

Severity: CRITICAL when state bugs cause gameplay-breaking behavior
          MAJOR when state bugs cause visual glitches
          MINOR when state management works but is hard to extend
-------------------------------------------------
```

**Check 2.4 -- Frame-Rate Independence**

Physics must run at a fixed timestep. Rendering can run at variable rates. Mixing these
causes behavior that changes on different hardware.

```
FRAME-RATE INDEPENDENCE AUDIT
-------------------------------------------------
FIND: Physics calculations in variable-rate update functions
FLAG: Movement, collision, force application in Update() instead of
      FixedUpdate() (Unity) or _process() instead of _physics_process() (Godot)

Also check:
- Is the fixed timestep actually fixed, or is it accidentally variable?
- Are interpolation/extrapolation used for smooth rendering between physics steps?
- Do input-driven actions respect the physics timestep boundary?
- Are animation events synchronized with physics or rendering?

Severity: CRITICAL -- frame-rate dependent physics is always a shipped bug
-------------------------------------------------
```

**Check 2.5 -- Resource Cleanup**

Scene transitions, level loads, and respawns are memory leak hotspots. Every resource
acquired must be released.

```
RESOURCE CLEANUP AUDIT
-------------------------------------------------
CHECK: Scene/level transition code
- Are all dynamic objects properly freed/destroyed?
- Are event listeners/signals disconnected?
- Are audio sources stopped and released?
- Are particle systems stopped before their parent is destroyed?
- Are async operations cancelled or properly awaited?
- Are pooled objects returned to pools?

CHECK: Object lifecycle
- Do spawned objects have a corresponding despawn path?
- Are references cleared when objects are destroyed?
- Are weak references used where appropriate?

Severity: MAJOR -- resource leaks cause gradual performance degradation
          CRITICAL -- if leaks cause crashes during extended play sessions
-------------------------------------------------
```

**Check 2.6 -- Dependency Direction**

Systems should depend on abstractions, not on concrete implementations. Circular
dependencies make systems untestable and modification-fragile.

```
DEPENDENCY DIRECTION AUDIT
-------------------------------------------------
CHECK: Do high-level systems (gameplay) depend on low-level systems (rendering)?
       This is fine. The reverse is a red flag.
CHECK: Do peer systems reference each other directly?
       Use events, signals, or a mediator pattern instead.
CHECK: Can you instantiate a system in a test without bringing up the entire game?
       If not, coupling is too tight.

FLAG: Circular dependencies (A depends on B depends on A)
FLAG: God objects that everything references (GameManager with 50 public fields)
FLAG: Direct references to singletons scattered throughout gameplay code

Severity: MAJOR -- architectural coupling compounds over time
-------------------------------------------------
```

**Check 2.7 -- Data-Driven Values**

Gameplay numbers must live in data files, not source code.

```
DATA-DRIVEN AUDIT
-------------------------------------------------
FIND: Hardcoded numeric literals in gameplay code
FLAG: speed = 5.0, damage = 10, cooldown = 0.5, spawnRate = 3
FIX:  Load from JSON, XML, CSV, or engine-native resource files

Why this matters:
- Designers cannot tune values without programmer intervention
- A/B testing requires code changes instead of config changes
- Balancing requires recompilation instead of data edits
- Platform-specific tuning (mobile vs. desktop) becomes a code branch

Exception: Mathematical constants (PI, gravity constant) and engine
configuration (target FPS, physics substeps) can be hardcoded with
a comment explaining why.

Severity: MAJOR for player-facing values (damage, speed, etc.)
          MINOR for internal system values (pool sizes, buffer lengths)
-------------------------------------------------
```

**Check 2.8 -- Input Handling**

Input should flow through an abstraction layer, not be read directly in gameplay code.

```
INPUT HANDLING AUDIT
-------------------------------------------------
FLAG: Direct keyboard/mouse/gamepad checks in gameplay code
      (Input.GetKey, Input.is_action_pressed without action mapping)
FLAG: Hardcoded key bindings (KeyCode.Space, KEY_W)
FLAG: Mouse/touch handling that assumes a specific screen resolution

PREFER:
- Input action maps that players can remap
- Input abstraction that translates raw input to game actions
- Context-sensitive input (same button does different things based on state)
- Input buffering for action games (queue inputs during animations)

Severity: MAJOR for shipping products (accessibility and user experience)
          MINOR for prototypes (acceptable to defer)
-------------------------------------------------
```

**Check 2.9 -- Concurrency Safety**

If the game uses threading (audio, networking, asset loading), shared state must be
protected.

```
CONCURRENCY AUDIT
-------------------------------------------------
CHECK: Is game state accessed from multiple threads?
CHECK: Are async operations properly synchronized?
CHECK: Is there a clear thread ownership model (which thread owns which data)?
FLAG:  Shared mutable state without locks or atomic operations
FLAG:  Race conditions in network code (state update vs. render)
FLAG:  Callback chains that assume execution order

Severity: CRITICAL when concurrency bugs cause crashes or data corruption
          MAJOR when they cause visual glitches or desync
-------------------------------------------------
```

**Check 2.10 -- AI-Generated Code Anti-Patterns**

As AI-assisted code generation becomes standard practice, game codebases increasingly contain AI-generated code that introduces a specific category of bugs. These anti-patterns are distinct from human-authored bugs because they often look plausible but are subtly wrong.

```
AI CODE ANTI-PATTERN AUDIT
-------------------------------------------------
CHECK 2.10.1 -- Hallucinated APIs:
  Verify that EVERY API call, method, property, and enum value referenced in
  the code actually exists in the current engine version. AI models frequently
  generate calls to APIs that existed in older versions, exist only in a
  different engine, or never existed at all.

  FLAG: Any API call that does not appear in the engine's official documentation
        for the project's engine version.
  FLAG: Method signatures that do not match the current API (wrong parameter
        count, wrong parameter types, wrong return type).
  FLAG: Enum values that do not exist in the current engine version.

  Severity: CRITICAL -- hallucinated APIs cause compile errors at best,
            silent runtime failures at worst.

CHECK 2.10.2 -- Engine-Specific Pattern Violations:
  AI models often generate code that follows generic programming patterns
  rather than engine-specific idioms. Check against `@docs/coding-standards.md`
  engine version table.

  FLAG: Using generic design patterns where the engine provides a built-in
        solution (e.g., hand-rolling an observer pattern in Godot when signals
        exist, implementing a custom coroutine system in Unity when UniTask or
        native coroutines are available).
  FLAG: Anti-patterns for the specific engine (e.g., using GetComponent() in
        Update() in Unity, using get_node() with long paths in Godot hot loops).
  FLAG: Version-specific API usage -- code written for engine version X running
        on engine version Y.

  Severity: MAJOR -- pattern violations cause maintenance burden and potential
            performance issues.

CHECK 2.10.3 -- License Compliance:
  AI-generated code can reproduce copyrighted patterns, licensed algorithms,
  or proprietary API wrappers from its training data.

  FLAG: Code blocks that appear to be direct reproductions of copyrighted
        source code (exact variable names, exact comment text, identical
        structure to known open-source implementations).
  FLAG: Algorithm implementations that match patented methods without license.
  FLAG: Middleware or SDK wrapper code that bypasses licensing requirements.

  Severity: MAJOR -- license violations create legal liability.

CHECK 2.10.4 -- Attribution:
  Document AI-assisted code sections per the project's AI usage policy.

  FLAG: Significant code blocks generated by AI without attribution comments
        indicating AI assistance.
  FLAG: Missing documentation of which AI tool was used, when, and what prompt
        produced the code.

  Follow the project's AI content policy (reference `@templates/ai-content-policy.md`
  if available). At minimum, add a comment indicating AI-assisted generation for
  any function or class substantially produced by AI tools.

  Severity: MINOR -- attribution is a process issue, not a runtime issue, but
            is important for audit trails and legal compliance.
-------------------------------------------------
```

**Check 2.11 -- Magic Numbers**

Every numeric constant should have a name and ideally a comment explaining the design
rationale behind the chosen value.

```
MAGIC NUMBER AUDIT
-------------------------------------------------
FLAG: Unnamed numeric literals in any context
BAD:  if velocity.y > 4.5:    # what is 4.5? why 4.5?
GOOD: if velocity.y > TERMINAL_VELOCITY:
      # TERMINAL_VELOCITY = 4.5 -- chosen to match the visual free-fall
      # animation length (0.6s at 60fps). Tuned via playtest session #3.

The comment matters as much as the name. "SPEED = 5" tells you the name.
"SPEED = 5 -- matched to feel responsive on 1920x1080 at 60fps, may need
 scaling for other resolutions" tells you the reasoning.

Severity: MINOR individually, but accumulated magic numbers become MAJOR
          (a codebase full of unexplained numbers is a codebase nobody can tune)
-------------------------------------------------
```

**Step 3: Standard Code Quality Checks**

After game-specific checks, review standard software quality.

- **Naming conventions**: Are they consistent? Do they follow engine conventions?
- **Code organization**: Is there a logical file/directory structure?
- **Error handling**: Are failure cases handled, or will they crash silently?
- **Documentation**: Are public APIs commented? Are complex algorithms explained?
- **Test coverage**: Are gameplay systems tested? What is the testing strategy?
- **Code duplication**: Is there significant copy-paste code that should be extracted?
- **Dead code**: Are there unused functions, classes, or commented-out blocks?

### Output Format

```markdown
# Game Code Review Report
**Project:** [name]
**Engine:** [detected engine]
**Reviewer:** GameForge Code Review
**Date:** [date]
**Files Reviewed:** [count]

## Summary
[2-3 sentences: overall code health, top concern, biggest strength]

## Game-Specific Findings

### Critical
- **[GS-CRIT-01]** [Title] -- [file:line]
  [Description of the issue, why it matters for gameplay, and fix suggestion]

### Major
- **[GS-MAJ-01]** [Title] -- [file:line]
  [Description and fix suggestion]

### Minor
- **[GS-MIN-01]** [Title] -- [file:line]
  [Description and fix suggestion]

## Standard Quality Findings
[Same severity structure for non-game-specific issues]

## Architecture Assessment
[Dependency map, coupling analysis, pattern evaluation]

## Positive Highlights
[What the code does well -- always acknowledge good work]

## Recommended Actions
1. [Highest priority fix with estimated effort]
2. [Second priority]
3. [Third priority]
```

### Quality Criteria

A successful game code review meets all of these:
- Every finding includes a specific file and line reference
- Game-specific checks are prioritized over style concerns
- Severity ratings reflect actual gameplay impact, not theoretical purity
- The review distinguishes between prototype code (where shortcuts are acceptable)
  and production code (where they are not)
- Performance concerns are flagged as "profile first" rather than assumed
- Engine-specific conventions are applied (not language-generic advice)
- The architecture assessment identifies the most dangerous coupling points
- Positive patterns are highlighted to reinforce good practices
- Recommendations are prioritized by effort-to-impact ratio

## MCP Integration

The code review workflow connects to MCP servers for version control integration and engine-specific live code analysis -- enabling reviews that operate on real PR diffs and can verify code against engine documentation in real time.

### Connected MCP Servers

| MCP Server | Code Review Use | How It Helps |
|---|---|---|
| **GitHub** (connected) | PR integration, diff analysis | Pull PR diffs for targeted review, read changed files in context, post review comments with line-specific references, check CI status and test results before reviewing, verify branch protection rules are met |
| **Context7** (connected) | Engine documentation verification | When reviewing code for hallucinated APIs (Check 2.10.1), query Context7 for the engine's current documentation to verify that every API call, method, and enum actually exists in the project's engine version |
| Engine MCPs (install per project) | Live code analysis | Connect the appropriate engine MCP to verify code behavior in the running editor: |
| - [Coding-Solo/godot-mcp](https://github.com/Coding-Solo/godot-mcp) (2,616 stars) | Godot code verification | Run GDScript in the editor to verify delta time behavior, test signal connections, validate scene tree structure |
| - [CoplayDev/unity-mcp](https://github.com/CoplayDev/unity-mcp) (7,540 stars) | Unity code verification | Inspect Unity editor state, verify component references, check asset dependencies |
| - [chongdashu/unreal-mcp](https://github.com/chongdashu/unreal-mcp) (1,637 stars) | Unreal code verification | Control Unreal Editor to test Blueprint connections, verify C++ compilation, inspect actor hierarchies |

### Example Workflows

**PR-Based Code Review:**
1. Use GitHub MCP to fetch the PR diff and list of changed files
2. Read each changed file using the Filesystem tools
3. Run all 11 game-specific checks (delta time, hot path allocations, state management, etc.) against the changed code
4. Use Context7 to verify any unfamiliar API calls against the engine's current documentation
5. Post review findings as GitHub PR comments with inline code references and severity ratings

**Engine-Assisted Live Review:**
1. Connect the appropriate engine MCP for the project (Godot, Unity, or Unreal)
2. For performance-suspect code, use the engine MCP to run the code in the editor and observe frame timing
3. For state management issues, use the engine MCP to inspect the object's runtime state during gameplay
4. Include engine-verified findings in the review report alongside static analysis results

### Example Use Cases

1. **"Review my player controller code."**
   Focus on delta time usage, state management, input handling, and frame-rate
   independence. These are the four highest-impact checks for a player controller.

2. **"We're getting frame drops in combat. Can you find the cause?"**
   Focus on hot path allocations, object pooling, and resource cleanup in combat
   systems. Profile suggestions should accompany every finding.

3. **"We're about to promote our prototype to production. What needs to change?"**
   Full review with emphasis on data-driven values, dependency direction, and
   resource cleanup. Prototype shortcuts that were acceptable for testing become
   technical debt in production.

4. **"A new developer is joining. Help me clean up the code first."**
   Focus on naming conventions, documentation, magic numbers, and architecture
   assessment. The goal is making the codebase navigable for someone new.

5. **"Our game behaves differently on my teammate's computer."**
   Frame-rate independence and delta time are the prime suspects. Also check for
   hardcoded screen resolutions, platform-specific assumptions, and timing-dependent
   logic.
