# Jobs-to-be-Done (JTBD) | Demand-Side Insight Framework

> **Core Value**: Understand demand from the perspective of "what job does the user hire the product to do," uncovering unmet opportunities
>
> **Creator**: Clayton Christensen (Harvard, 2003) + Anthony Ulwick (ODI, 2005) + Bob Moesta (Switch Interview)
>
> **One-liner**: Users don't buy products — they hire products to get a job done in their lives

---

> **Case Boundary**: Company/industry cases in this file are illustrative examples for framework structure and reasoning, not current factual claims by Alpha Insights. Before reusing any numbers, shares, dates, or conclusions in a live study, re-check sources and record them in the Evidence Claim Ledger.

## Overview

JTBD understands demand from the perspective of "what job does the user want to get done" rather than "who is the user." It is one of the most penetrating analytical lenses in demand insight and product innovation.

**Core Design Principles**:
- **Job Perspective**: Users don't buy products — they "hire" products to get a job done. Understanding the job is more valuable than understanding user demographics
- **Demand Stability**: The job itself is stable over time (e.g., "getting energy and killing time during the morning commute"), but the solutions for the job change with technology
- **Non-Demographic**: Segment markets based on "what users want to accomplish" rather than "who users are" — the same job may span different user groups

**Best Use Cases**:
- New product definition and demand insight (Stage 2-3)
- Discovering unmet user needs and market opportunities
- Understanding the deep reasons why users buy/don't buy
- Product differentiation positioning and value proposition design
- Assessing existing products' competitive advantages and weak points

**Output Value**:
- Structured Job Statements and job hierarchy
- Quantified Outcome Statements list with opportunity scores
- User switching behavior analysis (Forces of Progress)
- Opportunity Landscape of unmet needs

---

## Framework Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                   JTBD Three Schools of Thought                  │
│                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐  │
│  │ Christensen       │  │ Ulwick ODI        │  │ Moesta       │  │
│  │ School            │  │ School            │  │ School       │  │
│  │ Qualitative       │  │ Quantitative      │  │ Behavioral   │  │
│  │ insight           │  │ methodology       │  │ analysis     │  │
│  │ "Why was the      │  │ "Opportunity      │  │ "Forces of   │  │
│  │  milkshake hired?"│  │  scoring algorithm"│  │  Progress"   │  │
│  └──────────────────┘  └──────────────────┘  └──────────────┘  │
│           │                     │                    │           │
│           ▼                     ▼                    ▼           │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Complete JTBD Analysis Process                │   │
│  │                                                          │   │
│  │  Identify Job → Map Job Steps → Define Outcomes →        │   │
│  │  → Score Opportunities → Analyze Switching Behavior →    │   │
│  │  → Identify Innovation Directions                        │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Core Concepts Explained

### 1. Job Statement

**Standard Formula**:

```
When [situation/trigger], I want to [job/motivation], so that [desired outcome/goal]
```

**A good Job Statement must satisfy**:
- **Solution-agnostic**: Does not include any product or technology names
- **Stable**: Even if technology changes, the job itself doesn't change
- **Observable**: Can be directly observed in users' lives/work

| Quality | Example |
|---------|---------|
| ❌ Bad | "Users want to use WeChat Pay" |
| ❌ Bad | "Users want to download a budgeting app" |
| ✅ Good | "When I receive my salary, I want to clearly understand my monthly income and expenses, so that I can ensure I save enough for mortgage and living costs" |
| ✅ Good | "When commuting alone in the morning, I want to get energy and kill boredom, so that I start work feeling energized" |

### 2. Job Hierarchy

| Level | Definition | Case (Breakfast Milkshake) | Analysis Focus |
|-------|-----------|---------------------------|----------------|
| **Functional job** | The core practical thing to be done | Get breakfast energy + kill commute time | Product feature design |
| **Related jobs** | Peripheral needs accompanying the main job | One-hand operation (while driving), don't stain clothes | Experience optimization |
| **Emotional jobs** | Desired emotional/social state | Feel like I made a healthy choice, no guilt from eating fast food | Brand positioning |
| **Consumption chain jobs** | Full lifecycle: purchase → use → maintain → dispose | Quick purchase (don't want to queue), easy cup cleanup | Service design |

### 3. Outcome Statements — Ulwick ODI Methodology

**Outcome Statements are the quantitative core of JTBD**. Each outcome statement follows a strict four-element structure:

```
[Direction] + [Metric] + [Object of Control] + [Context Qualifier]
```

| Element | Description | Example |
|---------|-----------|---------|
| **Direction** | Minimize/Maximize/Increase/Decrease | Minimize |
| **Metric** | Measurable dimension (time/likelihood/quantity) | the time spent |
| **Object of Control** | What is being measured | finding a suitable financial product |
| **Context Qualifier** | Qualifying condition (optional) | without understanding financial expertise |

**Complete Examples**:
- "Minimize / the time needed to / confirm the transfer recipient's identity is correct"
- "Minimize / the likelihood of / transferring to the wrong account"
- "Maximize / the clarity of / understanding where each expense goes"

**Typical count**: A core job usually has 50-150 outcome statements.

### 4. Jobs Map — 8 Universal Steps

Ulwick proposed that any job can be decomposed into 8 universal execution steps (Universal Job Map). Outcome statements can be mined at each step:

| Step | Name | Meaning | Example (Managing Personal Finances) |
|------|------|---------|--------------------------------------|
| 1 | **Define** | Clarify what needs to be done | Set this month's budget target |
| 2 | **Locate** | Find needed inputs/resources | Find all income and expense sources |
| 3 | **Prepare** | Set up the execution environment | Organize bills, set up accounting categories |
| 4 | **Confirm** | Verify readiness | Verify all income/expenses are recorded |
| 5 | **Execute** | Perform the core task | Allocate budget, make spending decisions |
| 6 | **Monitor** | Track execution | Track actual spending vs. budget |
| 7 | **Modify** | Adjust and correct | Adjust subsequent budget after overspending |
| 8 | **Conclude** | Complete and wrap up | Month-end summary, evaluate savings goal achievement |

**Usage**:
1. For the core job, identify user outcome statements step by step
2. List 5-20 outcome statements under each step
3. Pay special attention to steps 1-2 (Define/Locate) and 6-7 (Monitor/Modify) — these steps are typically most overlooked by products

### 5. Opportunity Scoring Algorithm

Ulwick's quantitative core: For each outcome statement, obtain two scores (1-10) through surveys:

- **Importance**: How important is this outcome for completing the job?
- **Satisfaction**: How well does the current solution perform on this outcome?

```
Opportunity Score = Importance + MAX(Importance - Satisfaction, 0)
```

| Score Range | Meaning | Strategy Recommendation |
|------------|---------|------------------------|
| **>12** | 🔴 Severely underserved — high-value innovation opportunity | Prioritize solving; could support an entirely new product |
| **10-12** | 🟡 Underserved — attractive improvement opportunity | Focus on optimization; key to competitive differentiation |
| **6-10** | ⚪ Adequately served — current solutions basically sufficient | Maintain or fine-tune |
| **<6** | 🟢 Overserved — performance surplus | Room for simplification/price reduction (disruptive innovation entry point) |

**Core Insight**: High importance + Low satisfaction = Best innovation opportunity. Low importance + High satisfaction = Performance surplus zone (vulnerable to low-end disruption).

### 6. Forces of Progress Model — Bob Moesta

Analyzes four forces acting on users when switching from an old solution to a new one:

```
                    Push Toward New Solution
                        ↑
    ┌─────────────────────────────────────┐
    │  Push                  Pull          │
    │  Dissatisfaction       Attraction of │
    │  with current          new solution  │
    │  "Current solution     "New solution │
    │   is too slow"          is faster"   │
    └─────────────────────────────────────┘
    ┌─────────────────────────────────────┐
    │  Anxiety               Habit         │
    │  Uncertainty about     Dependence on │
    │  new solution          current state │
    │  "Is the new solution  "Used to the  │
    │   reliable?"            old one"     │
    └─────────────────────────────────────┘
                        ↓
                    Stay with Old Solution
```

**Switching Formula**: Push + Pull > Anxiety + Habit → User switches

**Analysis Method**: Through Switch Interviews, trace the complete process of a user's most recent "hiring/firing" of a product:
1. **First thought**: When did you first think about changing? (Push)
2. **Passive observation**: Did you then notice alternatives? (Passive discovery of Pull)
3. **Active search**: What triggered an active search? (Reinforcement of Push)
4. **Decision moment**: Why did you ultimately choose this one? (Decisive factor of Pull)
5. **Post-purchase**: Are you satisfied after using it? Any regrets? (Verification of Anxiety)

---

## Execution Steps

### Step 1: Identify the Core Job (Define the Job)

**Input**: User interviews, customer service records, behavioral data, competitive analysis

**Actions**:
1. Identify 1-3 core jobs through user research
2. Write job statements using the standard formula
3. Distinguish functional jobs, emotional jobs, and related jobs
4. Verify whether jobs meet the "solution-agnostic" and "long-term stable" criteria

**Data Source Recommendations**:

| Data Type | Source | Applicable Stage |
|-----------|--------|-----------------|
| Job identification | User depth interviews (Switch Interview), diary studies, contextual observation | Qualitative exploration |
| Pain point validation | Customer service records, App reviews, Xiaohongshu sentiment | Large-scale validation |
| Behavioral data | User behavior data, clickstream analysis | Behavioral validation |
| Competitive comparison | Competitor review analysis, user switching interviews | Differentiation insights |

### Step 2: Map the Job Steps

**Actions**:
1. Decompose the core job using the 8-step Universal Job Map
2. Under each step, list user outcome statements
3. Mark current solution performance and pain points at each step

**Output Template**:

```markdown
### Job Map: [Core Job Name]

| Step | User Behavior | Outcome Statements (TOP 3) | Current Pain Points |
|------|-------------|---------------------------|-------------------|
| Define | [behavior] | 1. [outcome] 2. [outcome] 3. [outcome] | [pain point] |
| Locate | [behavior] | 1. [outcome] 2. [outcome] 3. [outcome] | [pain point] |
| ... | ... | ... | ... |
```

### Step 3: Score Opportunities

**Actions**:
1. For key outcome statements (typically 30-50), assess importance and satisfaction
2. Calculate opportunity scores
3. Draw the opportunity map

**Data Collection Methods** (by feasibility):
- **Surveys** (ideal): Distribute quantitative surveys to target users
- **Expert assessment** (viable alternative): Analyst judgment based on user research data
- **Indirect inference** (minimum requirement): Infer from customer complaint frequency, competitor reviews, search trends

**Opportunity Map Visualization**:

```
Importance 10 ┌────────────────────────────┐
              │  Overserved    │  🔴 Best    │
              │  (Simplify     │  Innovation  │
              │   opportunity) │  Opportunity │
         5    ├──────────────┼─────────────┤
              │  Not important │  Low         │
              │  (Ignore)      │  Priority    │
              │                │  Improvement │
         0    └────────────────────────────┘
              10  Satisfaction  5            0
```

### Step 4: Analyze Switching Behavior (Forces Analysis)

**Actions**:
1. Identify Push: Users' specific dissatisfaction with the current solution
2. Identify Pull: Attractive elements of the new/ideal solution
3. Assess Anxiety: Users' concerns about the new solution
4. Assess Habit: Factors keeping users with the old solution
5. Design strategy: Strengthen Push + Pull, reduce Anxiety + Habit

### Step 5: Output Innovation Directions and Recommendations

**Actions**:
1. Synthesize opportunity scores and Forces of Progress analysis
2. Identify TOP 3-5 unmet needs (opportunity score >10)
3. Propose actionable solution directions for each unmet need
4. Assess feasibility and market potential for each direction

---

## Output Format

```markdown
## JTBD Analysis: [Product/Industry Name]

### Core Job Definition
| Job Type | Job Statement | Context |
|----------|-------------|---------|
| Functional job | When [context], I want to [motivation], so that [outcome] | [usage scenario] |
| Emotional job | [statement] | [scenario] |
| Related job | [statement] | [scenario] |

### Job Map
| Step | User Behavior | Key Outcome Statements | Current Satisfaction |
|------|-------------|----------------------|---------------------|
| Define | [behavior] | [outcome] | High/Medium/Low |
| Locate | [behavior] | [outcome] | High/Medium/Low |
| Prepare | [behavior] | [outcome] | High/Medium/Low |
| Confirm | [behavior] | [outcome] | High/Medium/Low |
| Execute | [behavior] | [outcome] | High/Medium/Low |
| Monitor | [behavior] | [outcome] | High/Medium/Low |
| Modify | [behavior] | [outcome] | High/Medium/Low |
| Conclude | [behavior] | [outcome] | High/Medium/Low |

### Opportunity Score TOP 10
| Rank | Outcome Statement | Importance | Satisfaction | Opp. Score | Opp. Level |
|------|------------------|-----------|-------------|-----------|-----------|
| 1 | [outcome] | [X] | [X] | [X] | 🔴 Severely underserved |
| 2 | [outcome] | [X] | [X] | [X] | 🟡 Underserved |
| ... | ... | ... | ... | ... | ... |

### Forces of Progress Analysis
| Force | Specific Manifestation | Strength |
|-------|----------------------|----------|
| Push | [dissatisfaction with current state] | Strong/Medium/Weak |
| Pull | [new solution attractiveness] | Strong/Medium/Weak |
| Anxiety | [concerns about new solution] | Strong/Medium/Weak |
| Habit | [dependence on current state] | Strong/Medium/Weak |

### Innovation Direction Recommendations
| Priority | Unmet Need | Solution Direction | Feasibility | Expected Impact |
|----------|-----------|-------------------|------------|----------------|
| P0 | [need] | [direction] | High/Med/Low | High/Med/Low |
| P1 | [need] | [direction] | High/Med/Low | High/Med/Low |
```

---

## Classic Cases

### Case 1: Christensen's Breakfast Milkshake

**Background**: McDonald's discovered 40% of milkshakes were purchased before 9 AM

**Traditional analysis** (by user demographics): Improve flavors, add varieties → minimal effect

**JTBD Analysis**:
- **Core job**: When commuting alone in the morning, I want something to kill boredom and get energy, so that I last until lunch
- **Why the milkshake is "hired"**: Thick consistency (can drink for 20 minutes), one-hand operable, doesn't stain clothes, filling
- **"Competitors" are not other milkshake brands**: They are bananas, donuts, bagels (different solutions for the same job)

**Takeaway**: Competition is not within the category but among all solutions for the same job.

### Case 2: Alipay — From Payment Tool to Life Services Platform

**Core job evolution**:
- Initial job: When shopping online, I want to complete payment safely and conveniently, so I don't worry about being scammed
- Mid-stage job: When I need to manage personal finances, I want one place to handle all financial needs
- Current job: When encountering various tasks in daily life, I want to quickly find and complete them

**Outcome Statement analysis**:
- "Minimize / worry about / whether the payee is trustworthy" → Escrow transactions
- "Minimize / the complexity of / managing multiple bank cards" → Quick payment
- "Minimize / the time spent / going to different platforms for different services" → Mini programs

### Case 3: Pinduoduo — Disruptive Innovation Through the Job Lens

**Traditional e-commerce core job**: Find the desired product → compare prices → place order

**The different job Pinduoduo discovered**:
- When bored with nothing to do, I want to browse and see what deals are available, so I discover unexpected bargains
- When wanting to save money on daily necessities, I want to spend less for adequate items, so I save on household expenses

**Opportunity Score insights**:
- "Minimize / the price of / same-quality products" → Importance 9 / Satisfaction 4 → Opportunity score 14 🔴
- "Maximize / the entertainment value of / shopping" → Importance 7 / Satisfaction 3 → Opportunity score 11 🟡

---

## Common Mistakes

| Mistake | Manifestation | Correct Approach |
|---------|--------------|-----------------|
| Job includes solution | "Users want to use an App for bookkeeping" | Remove solution: "Users want to track their income and expenses" |
| Job too broad | "Users want to live a better life" | Focus on observable context and behavior |
| Only qualitative, no quantitative | Listed jobs but no opportunity scores | Must quantify importance and satisfaction |
| Ignoring emotional jobs | Only analyzing functional needs | Emotional jobs are often the key to differentiation |
| Equating user needs with feature requests | "Users want more filter options" | Return to the job level: "Users want to quickly find options that meet their criteria" |
| Looking for competitors within the category | Milkshake's competitor is other milkshake brands | All alternative solutions for the same job are competitors |
| Ignoring consumption chain jobs | Only analyzing the usage stage | Purchase, learning, maintenance, and disposal stages also have unmet needs |

---

## Integration with Other Frameworks

| Partner Framework | Relationship | Synergy |
|-------------------|-------------|---------|
| Competitive Positioning Map | JTBD defines evaluation dimensions → positioning map visualizes them | Use JTBD outcome statements as positioning map axes |
| Blue Ocean Strategy | JTBD opportunity scores → Blue Ocean's "Eliminate-Reduce-Raise-Create" | "Eliminate/Reduce" overserved outcomes; "Raise/Create" underserved outcomes |
| BMC Business Model Canvas | JTBD outputs jobs and needs → BMC's value proposition and customer segments | JTBD jobs directly fill BMC's customer jobs module |
| Disruption Theory | JTBD's "overserved zone" = disruptive innovation entry point | Opportunity scores <6 are low-end disruption opportunities |
| Five Forces | JTBD defines substitutes scope (cross-category competition) | Five Forces substitute analysis redefined using JTBD |
| Flywheel | JTBD drives the flywheel's initial value proposition | The flywheel's first push comes from solving the user's core job |

---

## China Market Specifics

| Dimension | China Characteristics | Case |
|-----------|----------------------|------|
| **Job identification** | Pay attention to unique lower-tier market jobs (e.g., "save money + social" combo jobs), silver generation digitization jobs, Gen Z emotional jobs | Pinduoduo solves the "save money + social bragging" combo job; Tangdou Square Dancing solves the silver generation's social job |
| **Data sources** | Xiaohongshu, user behavior data, customer service data can validate jobs and pain points at scale | Xiaohongshu posts mine real user pain points; app analytics data verifies feature usage rates |
| **Competitor definition** | The "super app" phenomenon blurs competitive boundaries — the same job may be "competed for" by different platforms | The "transfer money" job: WeChat vs Alipay vs bank apps — cross-category competition |
| **Emotional jobs** | Face-saving consumption, social currency, national brand identity and other China-specific emotional jobs need special attention | Moutai ice cream's "social currency" job; Florasis's "national brand identity" job |
| **Cultural differences** | Relationship-oriented purchase decisions (high weight on friends/family recommendations), herd mentality influencing the Forces of Progress | WeChat viral marketing leveraging social networks; Xiaohongshu seeding and the herd mentality |
