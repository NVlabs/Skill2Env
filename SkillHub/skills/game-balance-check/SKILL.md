---
name: "game-balance-check"
description: >
  Invoke when the user needs to validate game balance, tune economy systems, analyze
  progression curves, evaluate difficulty scaling, or check reward pacing. Includes
  Monte Carlo simulation and statistical validation. Triggers on: "balance", "economy
  tuning", "progression curve", "difficulty scaling", "reward pacing", "Monte Carlo",
  "fairness check". Do NOT invoke for economy/monetization design (use
  game-economy-designer) or code review (use game-code-review). Part of the AlterLab
  GameForge collection.
argument-hint: "[system to analyze]"
effort: medium
context: fork
allowed-tools: Read, Glob, Grep, Write, AskUserQuestion
version: 1.3.0
---

# AlterLab GameForge -- Economy & System Balance Validation

Balance is not about making everything equal -- it is about making everything feel fair while keeping decisions meaningful. A perfectly balanced game where every option is identical is a game with no interesting decisions. Into the Breach achieves near-perfect balance not through symmetry but through information transparency -- every option is viable because every consequence is visible. Slay the Spire achieves it through controlled variance -- any card can be powerful in the right deck, and Jorbs' statistical breakdowns prove the math holds across thousands of runs.

The goal is controlled asymmetry: every choice has a trade-off, every path is viable, and every player feels their preferred playstyle is respected. This workflow provides formal models -- including statistical validation and simulation -- for validating economy, progression, difficulty, and reward systems.

### Purpose & Triggers

**Invoke this workflow when:**
- An in-game economy is producing unintended inflation or deflation
- Players are gravitating toward a single dominant strategy and ignoring all alternatives
- Progression feels too fast (trivializing content), too slow (creating grind walls), or uneven (dead zones followed by spikes)
- Difficulty scaling needs calibration -- either players are breezing through or hitting walls
- Reward pacing needs analysis to sustain engagement through the mid-game and endgame
- A new item, character, ability, or system is being introduced and needs integration with existing balance
- Free-to-play monetization fairness needs auditing -- the gap between paying and non-paying players must be reasonable
- Pre-release balance pass is needed before a playtest or launch

**Do NOT use this workflow when:**
- The game has no systems to balance (pure narrative games, walking simulators with no mechanics)
- You are still in the prototyping phase and systems are not yet defined (use `game-prototype` first)
- The balance problem is actually a design problem -- if the system is fundamentally broken, tuning numbers will not save it

### Critical Rules

1. **Balance is relative, not absolute.** A weapon that deals 100 damage is not overpowered or underpowered in isolation. It is only meaningful relative to enemy health pools, other weapon options, ammunition scarcity, and player skill ceiling.
2. **Dominant strategies kill games.** If one approach is strictly better than all alternatives in all situations, you have a balance failure. Dead Cells handles this by making every weapon viable through situational DPS curves -- a slow broadsword outdamages daggers against single targets but fails against swarms. Every viable strategy must have at least one situation where it is suboptimal.
3. **Perception matters more than math.** A system can be mathematically balanced but FEEL unfair. Player psychology (loss aversion, anchoring, confirmation bias) must be factored into balance analysis. A player who loses a rare item to a 5% failure chance remembers that loss far more vividly than the 95 successes. Balatro understands this -- its pity system and score multiplier transparency make variance feel fair even when the math is brutal.
4. **Never balance in a vacuum.** Every system interacts with every other system. Changing the warrior's damage output affects healer balance, enemy design, level pacing, and economy. Map the dependency graph before touching any number. Factorio's developers famously trace every balance change through the entire production chain before shipping it.
5. **Data over intuition.** When you have telemetry, use it. When you do not, use Monte Carlo simulation to generate synthetic data. "It feels about right" is not a balance methodology.
6. **Reference `docs/game-design-theory.md`** for Flow Theory (challenge-skill balance), SDT (competence feedback loops), and MDA Framework (how balance affects target aesthetics).

### Workflow

**Step 1: System Inventory and Dependency Mapping**

Before you can balance a system, you must understand what the system contains and how it connects to everything else.

Create a complete inventory of:
- **Currencies**: Every resource the player can earn, spend, trade, or lose (gold, XP, stamina, gems, reputation, crafting materials, etc.)
- **Sinks**: Every place currency leaves the economy (shops, upgrades, repairs, consumables, taxes, etc.)
- **Faucets**: Every place currency enters the economy (quest rewards, loot drops, selling, daily bonuses, etc.)
- **Progression tracks**: Every axis of player growth (level, gear score, skill tree, reputation tiers, collection progress, etc.)
- **Difficulty variables**: Every parameter that affects challenge (enemy stats, spawn rates, AI behavior, environmental hazards, time limits, etc.)
- **Reward mechanisms**: Every system that gives the player positive feedback (loot, achievements, unlocks, cosmetics, narrative progress, etc.)

Build a dependency graph showing how these systems connect. When system A changes, which other systems are affected? This graph is your guard rail -- before changing any number, trace the ripple effects through the dependency graph.

**Step 2: Economy Validation**

**Faucet/Sink Analysis**

Map every currency source and sink with flow rates:

```
[Source] --[rate/hour]--> [Currency Pool] --[rate/hour]--> [Sink]

Example:
Quest Rewards  --500g/hr-->  Gold Pool  --300g/hr-->  Equipment Shop
Monster Drops  --200g/hr-->  Gold Pool  --150g/hr-->  Consumables
Daily Login    --100g/day->  Gold Pool  --50g/hr--->  Fast Travel
                                        --100g/hr-->  Crafting
```

Calculate the net flow: Total Faucet Rate minus Total Sink Rate = Net Accumulation Rate. If net accumulation is positive, the economy inflates over time (currency becomes worthless). If negative, the economy deflates (players feel increasingly poor). Neither extreme is good -- target a slight positive accumulation that is periodically reset by major purchases (new gear tier, base upgrade, etc.).

**Earn-Rate Analysis by Player Archetype**

Not all players play the same way. Model at least three player archetypes:

| Archetype | Play Pattern | Earn Rate | Expected Behavior |
|-----------|-------------|-----------|-------------------|
| **Casual** | 30 min/day, focuses on main quests, skips optional content | Lowest | Should progress at a satisfying pace without feeling punished for limited playtime |
| **Average** | 1-2 hrs/day, completes main + some side content, moderate exploration | Median | The "target" player. Balance primarily for this archetype. |
| **Hardcore** | 4+ hrs/day, min-maxes everything, optimizes farm routes | Highest | Should have meaningful things to spend surplus on. Currency should never become meaningless. |

**Time-to-X Analysis**

Calculate how long each archetype takes to reach key milestones:

| Milestone | Casual | Average | Hardcore | Target Range |
|-----------|--------|---------|----------|-------------|
| First major upgrade | ? hrs | ? hrs | ? hrs | 1-2 sessions |
| Midgame gear plateau | ? hrs | ? hrs | ? hrs | 10-15 sessions |
| Endgame entry | ? hrs | ? hrs | ? hrs | 30-50 sessions |
| Max level/gear | ? hrs | ? hrs | ? hrs | 80-150 sessions |

If the casual-to-hardcore ratio exceeds 5:1 for any milestone, the economy may be too grind-dependent and too punishing for casual players.

**Premium Currency Fairness (if applicable)**

If the game has premium (paid) currency alongside earned currency:
- Can a free player access ALL gameplay-relevant content at a reasonable rate? ("Reasonable" means the casual archetype reaches endgame within 6 months of regular play.)
- Are premium purchases time-savers or power advantages? Time-savers are generally accepted by players. Power advantages create pay-to-win perception even if the math says otherwise.
- Is there a conversion path between earned and premium currency? If so, is the exchange rate fair or exploitative?
- Are loot boxes or gacha mechanics involved? If so: Are probability tables disclosed? Is there a pity system (guaranteed reward after N attempts)? Is there duplicate protection?

**Step 3: Progression Curve Analysis**

**Power Curve Mapping**

Plot player power (aggregate combat effectiveness, measured as DPS * survivability) against time or content progression. Categorize the curve shape:

- **Linear**: Power grows at a constant rate. Feels predictable and steady but becomes boring after the midpoint because each increment feels identical. Common failure mode: "I leveled up but I don't feel stronger."
- **Exponential**: Power grows faster and faster. Feels incredible early (every upgrade is huge) but becomes unsustainable -- either the endgame is trivially easy or enemies must scale exponentially to match, creating a numbers treadmill. Common failure mode: "The numbers are meaningless."
- **Logarithmic**: Power grows quickly early and then plateaus. Front-loads satisfaction but creates a feeling of stagnation in the midgame. Common failure mode: "Nothing I do makes me stronger anymore."
- **S-Curve (Sigmoid)**: Fast initial growth, gentle middle, satisfying mastery plateau. This is the target for most games. The early phase teaches and rewards rapidly. The middle phase deepens mastery. The endgame rewards optimization and expression rather than raw power. Common success indicator: "I'm not stronger, but I'm BETTER."

**Dead Zone Detection**

Scan the progression curve for flat sections where the player receives no meaningful power increase for an extended period. Dead zones cause churn -- players quit during the midgame slog more than at any other point. Every dead zone should either be eliminated (add a reward) or justified (narrative beat that intentionally strips power for dramatic effect, with a clear promise of restoration).

**Spike Zone Detection**

Scan for sudden jumps in power. A player who doubles in effectiveness by equipping a single item has just made every previous upgrade feel worthless. Spikes should be rare, earned, and narratively justified (legendary weapon, prestige class, transformation).

**Level-Gating Fairness**

For each level/tier gate in the game:
- Is the XP/resource requirement achievable through normal play within 2-3 sessions?
- Does the content available at the current level remain engaging while the player works toward the next gate?
- Is there a clear feedback loop showing progress toward the next gate (progress bars, checklists, milestone indicators)?
- Does the gate feel like an achievement ("I reached level 10!") or a wall ("I'm stuck at level 9 and there's nothing to do")?

**Step 4: Difficulty Scaling Assessment**

**Challenge-Skill Balance (Flow Theory)**

Reference the Flow Theory framework from `docs/game-design-theory.md`. For each major section of the game, assess:

- Is the challenge level matched to the expected player skill at that point in the game?
- Does the difficulty increase in step with the player's growing mastery?
- Are there intentional difficulty oscillations (hard encounter followed by easy encounter) that create a breathing rhythm?
- Does the game avoid the two failure modes: anxiety (challenge vastly exceeds skill) and boredom (skill vastly exceeds challenge)?

**Difficulty Mode Analysis**

If the game offers difficulty settings, evaluate the quality of the implementation:

| Implementation Quality | Description | Verdict |
|----------------------|-------------|---------|
| **Lazy** | Enemy HP and damage are multiplied. Nothing else changes. | Poor. Higher difficulty just means longer fights, not harder decisions. |
| **Adequate** | Enemy stats scale AND enemy count/placement changes. | Acceptable. More tactical consideration required. |
| **Good** | AI behavior changes. Enemies use more advanced tactics, coordinate, exploit player weaknesses. | Strong. Higher difficulty is a qualitatively different experience. |
| **Excellent** | Game systems change. New mechanics emerge at higher difficulties. The player must master systems that are optional on lower difficulties. | Outstanding. Each difficulty mode feels like a different game. |

**Rubber Banding Assessment**

Does the game adjust difficulty dynamically based on player performance?
- If yes: Is it invisible? (Players should never feel the game is going easy on them -- that destroys the sense of accomplishment.) How sensitive is the system? (Adjusting after a single death is too aggressive. Adjusting after 5 deaths in the same encounter is reasonable.)
- If no: Is the fixed difficulty curve appropriate for the target audience? Are there accessibility options for players who struggle?

**Time-to-Kill (TTK) Analysis**

For combat-focused games, TTK is a core feel parameter:
- **Fast TTK** (< 1 second): Tactical, punishing, high-stakes. Suits realistic shooters, stealth games. Risk: feels unfair if netcode or AI precision is not flawless.
- **Medium TTK** (2-5 seconds): Balanced engagement window. Suits action RPGs, hero shooters. Risk: can feel "spongy" if enemies do not react to damage.
- **Slow TTK** (10+ seconds): Strategic, resource-management focused. Suits boss encounters, MMOs. Risk: feels tedious if the player's actions during the encounter are not varied and interesting.

Is the TTK consistent with genre expectations? Does TTK scale appropriately as player power grows?

**Step 5: Reward Pacing Analysis**

**Reward Schedule Classification**

Identify which reinforcement schedule each reward system uses:

| Schedule Type | Description | Player Behavior | Best For |
|--------------|-------------|-----------------|----------|
| **Fixed Ratio** | Reward every N actions (every 10 kills) | Predictable grind. Players optimize toward the threshold. | Crafting, collection |
| **Variable Ratio** | Reward on average every N actions, but randomized | Compulsive engagement. The "slot machine" schedule. Most engaging but ethically questionable at extremes. | Loot drops, gacha |
| **Fixed Interval** | Reward every N minutes/hours | Clock-watching behavior. Players log in, collect, log out. | Daily rewards, timers |
| **Variable Interval** | Reward on average every N minutes, but randomized | Sustained attention. Players keep playing because "it might happen soon." | World events, rare spawns |

**Loot and Reward Fairness**

If randomized rewards are used:
- Are probability tables clearly communicated to the player (either in-game or in publicly available documentation)?
- Is there a pity system? After N unsuccessful attempts, is a reward guaranteed? The industry standard pity threshold is generally 50-100 attempts for rare items.
- Is there duplicate protection? Receiving the same rare item twice should either be impossible or the duplicate should convert to meaningful value (not a trivial amount of common currency).
- Are "feel-bad" moments minimized? Randomized loss (losing items on death, random stat downgrades) creates stronger negative emotion than randomized gain creates positive emotion. Loss aversion is approximately 2.5x gain satisfaction.

**Milestone Reward Spacing**

Plot all significant rewards on a timeline. Check for gaps longer than 2 play sessions where no meaningful reward occurs. These gaps are churn risk zones. Solutions:
- Add intermediate rewards (achievement unlocks, cosmetics, lore entries)
- Break a large reward into multiple smaller rewards distributed across the gap
- Add progress indicators showing accumulation toward the next big reward

**Endgame Retention**

Does the reward system sustain engagement after the main campaign is complete?
- Are there endgame-exclusive rewards that provide ongoing goals (prestige systems, seasonal content, mastery challenges)?
- Does the endgame reward system shift from power growth to lateral progression (cosmetics, alternative playstyles, collection)?
- Is there social reward (leaderboards, cooperative challenges, player expression) that provides motivation beyond material rewards?

**Step 5B: DDE Framework Lens for Balance Analysis**

When analyzing any game system for balance, apply the Design-Dynamics-Experience (DDE) framework lens alongside the MDA framework. Specifically, ask: "How does this system affect the player Experience layer?" Balance changes that look correct at the Design layer (the numbers) can produce unexpected results at the Dynamics layer (how systems interact) and unintended emotional responses at the Experience layer (what the player actually feels).

For every balance adjustment, trace the impact through all three layers:
- **Design**: What number changed? (e.g., weapon damage reduced by 15%)
- **Dynamics**: How does the system behavior change? (e.g., time-to-kill increases, players must engage enemies for longer, ammo consumption increases)
- **Experience**: How does the player's emotional response change? (e.g., combat feels more deliberate and tactical -- OR -- combat feels tedious and spongy, depending on other variables)

If you can only predict the Design and Dynamics impact but not the Experience impact, you need a playtest, not more math.

**Step 5C: Advanced Simulation and Monitoring**

**ML-Driven Simulation Approaches:**
For complex economies and progression systems, train reinforcement learning (RL) agents to play your game's economy:
- Define the player's "optimal" behavior as the RL agent's reward function
- Let the agent play thousands of iterations to discover exploit paths, degenerate strategies, and equilibrium states that human testing would take months to surface
- RL agents are particularly effective at finding resource duplication exploits, infinite loops in crafting chains, and arbitrage opportunities in multi-currency economies
- This approach requires investment but can detect exploits before players do, saving post-launch emergency patches

**Machinations.io:**
For visualizing and simulating economy flows without writing code, use Machinations.io (machinations.io). It provides a visual node-based editor specifically designed for game economy modeling:
- Build your faucet/sink diagram as a live simulation
- Run thousands of iterations to see how currency pools behave over time
- Test "what if" scenarios (what if drop rates are halved? what if a new sink is added?) without touching game code
- Particularly useful for pre-implementation validation -- test the economy design before building it

**Hard Sink vs. Soft Sink Distinction:**
Not all sinks are equal. Distinguish between:
- **Hard sinks**: Currency is permanently destroyed. Examples: consumable items that are used and gone, repair costs, fast travel fees, crafting materials consumed during crafting. Hard sinks are the primary tool for controlling inflation.
- **Soft sinks**: Currency changes form but is not destroyed. Examples: trading between players (currency moves, net supply unchanged), cosmetic purchases (currency to the system, cosmetic to the player -- the cosmetic has ongoing value). Soft sinks slow velocity but do not reduce supply.

A healthy economy needs both. Hard sinks control inflation. Soft sinks control velocity. If you only have soft sinks, your economy will inflate over time regardless of flow rates.

**Stock/Flow Monitoring Guidelines:**
After launch, monitor these metrics continuously:
- **Currency stock levels** per player segment (new, mid-game, endgame) -- are they growing, stable, or declining?
- **Flow rates** at each faucet and sink -- which are the highest-volume flows? These are your most impactful tuning levers.
- **Velocity** -- how quickly does currency circulate? High velocity means currency moves fast through the economy (healthy in moderation, inflationary at extremes). Low velocity means currency is hoarded (indicates sinks are unattractive or faucets are too generous).
- **Gini coefficient** -- measures wealth inequality across the player population. A high Gini coefficient means a small number of players hold most of the wealth. This is expected (hardcore players accumulate faster) but extreme values indicate the economy is not serving casual players.

**Step 6: Statistical Validation Methods**

Qualitative balance assessment catches the obvious problems. Statistical validation catches the subtle ones -- the economy that inflates 2% per hour until hour 40 when it collapses, the weapon that is balanced on average but has a 3% chance of one-shotting a boss, the matchup that is 50/50 overall but 90/10 at high skill levels.

**6.1 Distribution Analysis**

Every randomized system has an underlying probability distribution. Know which one yours uses and whether it matches your design intent:

```
DISTRIBUTION TYPE GUIDE
-------------------------------------------------
Normal (Gaussian):
  Use for: Damage ranges, stat variation, NPC behavior variance
  Shape: Bell curve -- most results cluster near the mean
  Example: Base damage 100, standard deviation 10 → 95% of hits
  land between 80-120. Players experience consistent damage.
  Watch for: Tails. A normal distribution with high variance
  produces occasional extreme outliers that feel like bugs.

Uniform:
  Use for: Loot table rolls, random map generation, spawn placement
  Shape: Flat -- every outcome equally likely
  Example: Drop table with 10 items, each 10% chance.
  Watch for: Streaks. Uniform random FEELS streaky because humans
  are terrible at recognizing true randomness. 5 of the same drop
  in a row is statistically plausible but psychologically devastating.
  Slay the Spire mitigates this by using weighted shuffle bags
  instead of pure uniform random for card rewards.

Poisson:
  Use for: Rare event timing (boss spawns, critical failures, jackpots)
  Shape: Skewed right -- most intervals are short, occasional long gaps
  Example: Average 1 legendary drop per 10 hours, but actual gaps
  range from 2 hours to 30+ hours.
  Watch for: The long tail. A Poisson process can produce gaps so long
  that players assume the system is broken.

Weighted Random with Pity Timer:
  Use for: Gacha, loot boxes, rare reward systems
  Shape: Weighted random with a guaranteed floor
  Implementation: Track consecutive failures. After N failures,
  force a success. Reset the counter.
  Example: Hades uses pity timers on its boon system -- if you have
  not received a specific god's boon in N rooms, the probability
  weight increases until it appears.
  Industry standard pity thresholds: 50-100 attempts for rare items,
  10-20 for uncommon. Publish these numbers to build player trust.
-------------------------------------------------
```

**6.2 Expected Value Calculations**

For every player decision with multiple outcomes, calculate the Expected Value (EV):

```
EV = Sum of (Probability_i * Value_i) for all outcomes i

EXAMPLE: Upgrade gamble system
  Success (70%): weapon gains +10 damage (value: +10)
  Failure (25%): weapon unchanged (value: 0)
  Catastrophe (5%): weapon loses 5 damage (value: -5)

  EV = (0.70 * 10) + (0.25 * 0) + (0.05 * -5) = 7.0 - 0.25 = 6.75

  The EV is positive, so upgrading is mathematically correct every time.
  But the 5% catastrophe creates fear disproportionate to its probability
  (loss aversion factor ~2.5x). The FELT EV is lower than the actual EV.
```

Use EV calculations to verify that:
- No decision has a strictly dominant strategy (one option with highest EV in ALL contexts)
- Risk-reward tradeoffs are real -- higher-risk options have higher EV to compensate
- The "safe" option is viable but suboptimal, not optimal (otherwise risk is never rewarded)
- Currency conversions and trade systems do not create arbitrage loops (buy low, sell high, infinite money)

Into the Breach achieves this brilliantly -- every move has a calculable EV because all information is visible. The tension comes from the tradeoffs between protecting buildings, killing Vek, and positioning for next turn. No move is mathematically dominant because the EV depends entirely on board state.

**6.3 Win Rate Analysis and Matchup Matrices**

For competitive or asymmetric games, build a matchup matrix:

```
MATCHUP MATRIX (win rates, row vs. column)
-------------------------------------------------
           | Warrior | Mage    | Rogue   | Ranger
-------------------------------------------------
Warrior    | 50%     | 55%     | 40%     | 52%
Mage       | 45%     | 50%     | 58%     | 43%
Rogue      | 60%     | 42%     | 50%     | 55%
Ranger     | 48%     | 57%     | 45%     | 50%
-------------------------------------------------

HEALTH THRESHOLDS:
  45-55% per matchup: Healthy. Rock-paper-scissors dynamic is working.
  40-60%: Acceptable with awareness. One class counters another, but
    the disadvantaged class can still win through superior play.
  Below 40% or above 60%: Imbalanced. The counter is too hard.
    Either nerf the advantage or give the disadvantaged class tools
    to outplay the matchup.
  Any class with ALL matchups above 52%: Overpowered. Nerf directly
    or buff ALL other classes (usually nerf is cleaner).
  Any class with ALL matchups below 48%: Underpowered. Buff directly.
```

For PvE with build diversity (roguelikes, RPGs), replace matchup matrices with build win-rate tracking:

```
BUILD WIN-RATE ANALYSIS
-------------------------------------------------
Track across N simulated or observed runs:
  Build archetype | Win rate | Avg clear time | Pick rate
  [build A]       | [%]      | [minutes]      | [% of runs]
  [build B]       | [%]      | [minutes]      | [% of runs]

Red flags:
- One build with >70% pick rate: it is either overpowered or perceived
  as overpowered. Either way, the meta is stale.
- Any build below 30% win rate: it feels unplayable. Buff it or remove it.
- High win rate + low pick rate: hidden gem. Consider making it more
  discoverable, not nerfing it.
- Low win rate + high pick rate: it is fun but weak. Buff it -- players
  are already drawn to the fantasy; reward them for choosing it.

Slay the Spire's balance: all four characters maintain 40-60% win rates
at high ascension, but through completely different strategic lenses.
The Silent's win rate drops at Ascension 18+ while the Defect's rises --
this is intentional difficulty differentiation, not imbalance.
-------------------------------------------------
```

**6.4 Sensitivity Analysis**

Before shipping a balance change, test how sensitive the system is to that parameter:

```
SENSITIVITY ANALYSIS PROTOCOL
-------------------------------------------------
1. Identify the parameter being changed (e.g., sword damage: 25 → 22)
2. Model the ripple effects at three magnitudes:
   - Conservative change: -5% (23.75)
   - Proposed change: -12% (22.0)
   - Aggressive change: -20% (20.0)
3. For each magnitude, trace through the dependency graph:
   - How does TTK change against each enemy type?
   - How does the economy shift (repair costs, replacement rate)?
   - How does the progression curve bend (time to midgame, time to endgame)?
   - How does the player's PERCEPTION change? (-12% damage may feel like
     -30% if the weapon already felt weak.)
4. If the proposed change produces dramatically different outcomes at
   +/- 2%, the system is brittle at this parameter. Consider a structural
   fix instead of number tuning.

Dead Cells demonstrates good sensitivity management -- weapon DPS curves
are designed so that a 10% nerf moves a weapon from "top tier" to "viable"
rather than from "viable" to "unusable." This is achieved by compressing
the DPS range: the best weapon deals ~40% more DPS than the worst, not
400% more.
-------------------------------------------------
```

**Step 7: Monte Carlo Simulation Guidance**

**When to Simulate**

Use Monte Carlo simulation when:
- Systems have randomized elements that interact (loot + crafting + upgrade chance)
- You need to understand the distribution of possible outcomes, not just the average
- Edge cases could create degenerate player experiences (extremely lucky or unlucky runs)
- Multiple interdependent systems make analytical solutions intractable

**Simulation Setup**

1. Define all random variables (drop rates, damage ranges, proc chances, critical hit probability)
2. Define the player decision model (what choices does the simulated player make? Use at least three archetypes: optimal, average, suboptimal)
3. Run a minimum of 10,000 iterations per scenario. For rare events (< 1% probability), run 100,000+.
4. Record the full distribution of outcomes, not just the mean.

**Interpreting Results**

- **Median vs. Mean**: If they diverge significantly, your distribution is skewed. The median is what a "typical" player experiences. The mean is distorted by outliers.
- **Percentile analysis**: Check the 5th and 95th percentiles. The 5th percentile is the "unlucky" player experience. The 95th is the "lucky" player. If the gap between them is too wide, the system feels random rather than skill-based.
- **Worst-case scenarios**: What happens in the bottom 1%? If the unluckiest 1% of players have a truly miserable experience (200 attempts for a guaranteed drop, zero useful loot in 10 hours of play), you need a safety net.
- **Exploit detection**: Look for strategies that produce outcomes far above the median. If a specific combination of choices produces 10x the median outcome, players will find it and it will become the only viable strategy.

**Step 8: Compile Balance Report**

Synthesize all analysis into the standardized Balance Report format (see Output Format below). Prioritize findings by impact on player experience and effort to fix.

### Output Format

```
## Balance Report: [Game / System Name]
## Version: [Build version analyzed]
## Date: [YYYY-MM-DD]
## Analyst: [Name]

### Executive Summary
[3 sentences: Current balance state, biggest concern, top recommendation]

### Economy Flow Diagram
[Visual representation of all faucets, sinks, and flow rates]
[Net accumulation rate and inflation/deflation assessment]

### Earn-Rate Table
| Currency | Casual Rate | Average Rate | Hardcore Rate | Net Flow |
|----------|------------|-------------|--------------|----------|
| [name]   | [rate]     | [rate]      | [rate]       | [+/-]    |

### Progression Curve Assessment
- Curve Type: [Linear / Exponential / Logarithmic / S-Curve / Mixed]
- Dead Zones Identified: [list with game progression points]
- Spike Zones Identified: [list with game progression points]
- Overall Shape Health: [Healthy / Needs Adjustment / Critical]

### Difficulty Scaling Report
- Flow Channel Adherence: [percentage estimate]
- Difficulty Mode Quality: [Lazy / Adequate / Good / Excellent]
- Rubber Banding Assessment: [Present/Absent, Invisible/Visible]
- TTK Analysis: [Current TTK, Target TTK, Assessment]

### Reward Pacing Analysis
- Primary Schedule Type: [Fixed/Variable Ratio/Interval]
- Longest Reward Gap: [duration and location in game]
- Pity System Status: [Present/Absent, Threshold if present]
- Endgame Retention Mechanisms: [list]

### Identified Imbalances

| ID | System | Issue | Severity | Impact | Recommendation | Expected Effect |
|----|--------|-------|----------|--------|----------------|-----------------|
| B1 | [sys]  | [desc]| Critical | [desc] | [specific fix]  | [what changes]  |
| B2 | [sys]  | [desc]| Major    | [desc] | [specific fix]  | [what changes]  |

### Simulation Results (if applicable)
- Scenarios Simulated: [count]
- Iterations per Scenario: [count]
- Key Findings: [percentile analysis, exploit risks, edge cases]

### Tuning Recommendations (Priority Order)
1. [Recommendation] -- Expected impact: [description]
2. [Recommendation] -- Expected impact: [description]
3. [Recommendation] -- Expected impact: [description]

### Next Steps
- [What to monitor after applying tuning changes]
- [When to re-run the balance analysis]
- [Dependencies on other systems or upcoming features]
```

### Quality Criteria

- **Completeness**: All balance dimensions (economy, progression, difficulty, reward pacing, statistical validation, simulation) are addressed, even if some are brief due to the game's design.
- **Statistical rigor**: EV calculations for key decisions, distribution analysis for randomized systems, and matchup matrices for competitive/asymmetric elements. No balance claim without supporting math.
- **Data grounding**: Every finding is supported by either telemetry data, simulation results, or systematic analysis -- not guesswork or "feel."
- **Actionability**: Every identified imbalance includes a specific tuning recommendation with an expected outcome. "Reduce gold drop rate by 15%" is actionable. "Fix the economy" is not.
- **Dependency awareness**: Recommendations include sensitivity analysis of ripple effects. No change is proposed in isolation.
- **Player archetype coverage**: Analysis covers at least three player archetypes (casual, average, hardcore) and verifies all three have a viable experience.
- **Edge case awareness**: Extreme scenarios (very lucky, very unlucky, degenerate strategies) are identified and addressed through percentile analysis and pity system validation.

### Example Use Cases

1. "Players are accumulating gold faster than they can spend it, and by midgame everything feels trivial. Analyze our economy and recommend sink adjustments."
2. "We have a gacha system for character unlocks and I need to verify the pity system is fair. Here are the probability tables -- run the numbers and tell me if a free player can reasonably collect all characters."
3. "Our difficulty curve feels flat in Acts 2 and 3. Players breeze through after struggling in Act 1. Help me analyze the scaling and propose adjustments."
4. "We're adding a new weapon class to our RPG and need to integrate it without breaking the existing balance. Walk me through the impact analysis."
5. "Our retention data shows a massive drop-off at the 10-hour mark. I suspect it's a reward pacing problem. Help me map the reward schedule and identify the gap."
