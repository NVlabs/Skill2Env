# Research Engine

> **Role**: Stage 4 research execution operations manual
>
> **Core Pattern**: A+B parallel (Subagent) + D→E→F→G→C sequential (Main Session)
>
> **Related Modules**:
> - [`data_sources.md`](./data_sources.md) - Required data source catalog
> - [`triangulation.md`](../methodology/triangulation.md) - Triangulation methodology
> - [`hypothesis_driven.md`](../methodology/hypothesis_driven.md) - Hypothesis-driven methodology
> - [`interview.md`](../methodology/interview.md) - Expert interview methodology

---

## Core Principles

1. **Hypothesis-driven**: Every search serves to validate or falsify a specific hypothesis
2. **Data Source Priority**: Must prioritize P0-P2 data sources from `data_sources.md`
3. **Triangulation**: Core data must seek 2-3 independent sources
4. **Evidence Chain Traceability**: Every conclusion must trace back to original sources
5. **Execution Order**: A+B parallel → D → E → F → G → C, executed sequentially
6. **Information Transparency**: Broadcast before each track execution; explain reasons when skipping

---

## Execution Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Main Session (Coordinator)                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Task Decomposition + Track Activation Decisions       │   │
│  └─────────────────────────────────────────────────────┘   │
│                            │                                │
│              ┌─────────────┴─────────────┐                 │
│              ▼                           ▼                  │
│       ┌──────────┐                ┌──────────┐             │
│       │ Track A  │                │ Track B  │  ← Parallel │
│       │ Public   │                │ Data     │  (Subagent) │
│       │ Search   │                │ Sources  │             │
│       └──────────┘                └──────────┘             │
│              │                           │                  │
│              └─────────────┬─────────────┘                 │
│                            ▼                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Track D: Knowledge Base Search (Main Session)        │   │
│  └─────────────────────────────────────────────────────┘   │
│                            ▼                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Track E: Xiaohongshu / Social Media (Main Session)   │   │
│  └─────────────────────────────────────────────────────┘   │
│                            ▼                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Track F: Internal Database (Main Session)            │   │
│  └─────────────────────────────────────────────────────┘   │
│                            ▼                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Track G: User Voice Data (Main Session)              │   │
│  └─────────────────────────────────────────────────────┘   │
│                            ▼                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Track C: Expert Interviews (Main Session, if triggered)│   │
│  └─────────────────────────────────────────────────────┘   │
│                            ▼                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Evidence Integration + Triangulation                  │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Track Definitions

| Track | Name | Execution Mode | Data Sources |
|-------|------|---------------|--------------|
| **A** | Public Data Collection | Subagent parallel | Search engines + web scraping |
| **B** | Directed Source Search | Subagent parallel | Authoritative source websites (iResearch, LeadLeo, etc.) |
| **D** | Knowledge Base Search | Main Session | Internal historical research, notes |
| **E** | Xiaohongshu / Social Media | Main Session | Consumer sentiment, product feedback |
| **F** | Internal Database | Main Session | Business data, user behavior |
| **G** | User Voice Data | Main Session | User experience issues, complaints, satisfaction |
| **C** | Expert Interviews | Main Session | Interview notes (requires user coordination) |

---

## Execution Rules

### Track A+B: Parallel Execution (Subagent)

**Trigger Condition**: Required for all research projects

**Execution Method**:
1. Main Session decomposes tasks and generates distribution list
2. Launch 2 Subagents for parallel execution
3. Wait for results to return; **Main Session consolidates and merges evidence**

⛔ **Parallel Write Protection**: Subagents do not write directly to `evidence_base.md`. Each Subagent returns results to the Main Session, which performs unified writing to avoid concurrent write conflicts.

⚠️ **Fallback When Agent Tool Unavailable**: If the platform does not support Agent/Subagent tools, execute Track A → Track B sequentially in the Main Session. All other processes remain unchanged.

**Progress Broadcast**:
```
━━━ Track A+B Parallel Execution ━━━
📚 Launching Subagent 1: Public Data Collection
📚 Launching Subagent 2: Directed Source Search
⏳ Waiting for results...

✅ Track A complete: Found X pieces of evidence
✅ Track B complete: Found X pieces of evidence
```

### Evidence Incremental Writing Rules (Context Loss Prevention)

After completing each Track (or when Layer 1 completes), **immediately append that round's evidence to `evidence_base.md`**. Do not wait until all Tracks are complete before writing.

**Writing Cadence**:
- Track A+B return → First write to `evidence_base.md` (hypothesis validation framework + initial data)
- Each subsequent Track (D/E/F/G/C) completion → Append corresponding section
- Stage 4 end → Final consolidation (add validation summary, data quality assessment, triangulation table)

**Principle: Better to write to file multiple times than to keep data only in context.** The platform automatically compresses early conversation content; files are the only reliable persistence mechanism.

⛔ **Evidence Chain Integrity**: All data cited in `report.html` must be traceable to `evidence_base.md`. Data expanded during Stage 7 iteration must also be written to `evidence_base.md` first before appearing in the report — no skipping. See SKILL.md "Core Behavioral Rules → Change Cascade Rule" for the full cascade mechanism.

**Empty Result Handling**: When any Track returns 0 valid pieces of evidence → Expand keywords and retry once (synonyms/hypernyms/English equivalents) → If still empty, note in evidence_base.md as "Evidence gap: Track X found no data, reason: [keyword/data source limitation]" → Continue to next Track.

**evidence_base.md Structure Template**:

```markdown
# Evidence Base

> Research topic: [topic]
> Generated: [date]
> Last updated: [date]

## Research Execution Summary

> ⏳ This section is filled by Layer 3 Step 3.4 after all Tracks complete

### Core Findings per Track (1-2 sentences each)
- **Track A**: [Most important finding]
- **Track B**: [Most important finding]
- **Track D/E/F/G**: [Fill per actually activated tracks]

### Cross-Track Key Signals
- 🔴 [Contradiction]: [Track X vs Track Y data conflict — needs interpretation in Stage 5]
- 🟢 [Corroboration]: [Findings confirmed across multiple Tracks]
- ⚠️ [Gap]: [Key data from only a single source, annotate confidence level]

### Hypothesis Validation Status Overview
| Hypothesis | Status | Core Evidence Source |
|-----------|--------|---------------------|
| H1 | ✅ Validated / ❌ Falsified / ⏳ Partial | [Source Track] |

## Research Execution Plan (Layer 1 Output)

> ⏳ This section is filled immediately after Layer 1 completes

### Hypothesis → Search Task Mapping
| Hypothesis | Key Data Point | Search Task | Assigned Track | Keywords |
|-----------|---------------|-------------|---------------|----------|
| H1 | [Data point] | [Search question] | A+B | [Keywords] |

### Track Activation Decisions
| Track | Status | Rationale |
|-------|--------|-----------|
| A+B | ✅/⚠️ | [Rationale] |
| D | ✅/⚠️ | [Rationale] |
| E | ✅/⚠️ | [Rationale] |
| F | ✅/⚠️ | [Rationale] |
| G | ✅/⚠️ | [Rationale] |

## Hypothesis Validation Framework

| Hypothesis | Sub-question | Analysis Lens | Validation Status | Supporting Evidence | Contradicting Evidence |
|-----------|-------------|--------------|-------------------|--------------------|-----------------------|
| H1 | Q1 | [Framework dimension] | ✅ Validated / ❌ Falsified / ⏳ Partial | [Evidence ID] | [Evidence ID] |

## Framework-Evidence Map (Updated per Track)

### [Framework Name]
| Dimension | Related Hypothesis | Evidence ID | Key Finding | Status |
|-----------|-------------------|-------------|-------------|--------|
| [Dim 1] | H1 | — | — | ⏳ |
| [Dim 2] | — | — | — | ➖ N/A: [reason] |

> Initialized in Step 1.0, updated per Track following universal rules, final review in Layer 3 Step 3.2.5

## Track A: Public Data Search

### Search Strategy
- Keywords: [Actual keyword list used]
- Search rounds: [Initial keywords → Adjusted keywords (if any)]
- Data source hits: [Which sources yielded valid data, which came up empty]

### Evidence Related to [Hypothesis/Sub-question]
- **[E-001]** [Data point] | Source: [URL/document] | Confidence Level: A/B/C/D | 📊/💡/📰

### Analysis Notes
- **Expected vs Actual**: [What you expected to find based on hypothesis before searching, whether actual results aligned] (⛔ Required)
- **Unexpected Signals**: [Unanticipated data points/trends/contradictions; write "No unexpected findings" if none] (⛔ Required)
- **Evidence Gaps**: [Data you wanted but couldn't find, may need other Tracks to supplement] (⛔ Required)
- **Cross-Track Correlation**: [Contradictions or corroborations with data from completed Tracks] (Fill when prior Tracks exist)

## Track B: Directed Sources
[Same structure as Track A: Search Strategy → Evidence List → Analysis Notes]

## Track D-G: Specialized Data Sources
[Appended per activated Track, each containing Search Strategy → Evidence List → Analysis Notes]

## Framework Analysis Conclusions

### [Primary Framework] Analysis Conclusions
- **Dimension Coverage**: X/Y dimensions ([N/A dimensions]: [reason])
- **Key Findings**: [3-5 items]
- **Data Support**: [Evidence IDs]
- **Preliminary Assessment**: [Overall assessment from framework perspective]

### Cross-Framework Findings (if any)
- [Cross-cutting insights where multiple framework dimensions point to the same conclusion]

## Data Quality Assessment
| Level | Count | Percentage |
|-------|-------|------------|
| A-level | | |
| B-level | | |
| C-level | | |
| D-level | | |

## Triangulation Table
[Per triangulation.md template]
```

---

### Track D-G: Sequential Execution (Main Session)

**Execution Principle**:
- All tracks are executed by default
- When skipping, must follow the "Skip Interaction Rules" below — silent skipping is prohibited

**Skip Criteria**:

| Track | Skip Condition | Example |
|-------|---------------|---------|
| **D Knowledge Base** | No knowledge base tool / no relevant documents | "Knowledge base search tool not detected, skipping this track" |
| **E Social Media** | Non-consumer topic / no access | "Topic is B2B business, social media data has low value, skipping this track" |
| **F Database** | No database tool / (external research **and** user is not an industry participant) | "This is purely external industry research with no internal business data, skipping this track" |
| **G User Voice** | No access / (non-product topic **and** user is not an industry participant) | "This is purely external industry research with no user feedback data, skipping this track" |

**Skip Interaction Rules**:

| Skip Type | Decision Basis | Handling |
|-----------|---------------|----------|
| **Value Judgment** | AI assesses low data value (e.g., "B2B topic, social media value is low") | **Must use AskUserQuestion to ask the user** — user may have a different perspective |
| **Technical Failure** | API error, no access, tool unavailable | Inform user of reason + proactively offer fallback (e.g., "Social media API unavailable, I can use search engines to indirectly obtain social media content — would you like me to?") |

> **Industry Participant Determination**: If the user indicates in Stage 1 `user_brief.md` that they are an existing enterprise/practitioner in the industry being researched (e.g., "we are a cat food company researching the cat food market"), they are considered an industry participant. In this case, D/F/G should be activated by default for exploration, as internal data may contain market insights (e.g., user profiles, competitor comparisons, sales trends).
>
> **Priority**: Industry participant determination > skip interaction rules. That is: when the user is an industry participant, F/G do not trigger "value judgment skip" and are activated directly (still subject to access constraints).
>
> **When uncertain**: If `user_brief.md` does not clearly indicate whether the user is an industry participant, ask the user during Stage 3 Track planning: "Are you a practitioner or company in this industry? If so, we can leverage your internal data to enhance the research."

**Progress Broadcast**:
```
━━━ Track D: Knowledge Base Search ━━━
📚 Loading tool: Knowledge base search
🔍 Search keywords: [keywords]
✅ Found X relevant documents

━━━ Track E: Social Media (Xiaohongshu) ━━━
📚 Loading capability: public social-media search / optional private adapter
🔍 Search keywords: [keywords]
❓ Value judgment: Topic is B2B SaaS business, social media data value may be low
   → Using AskUserQuestion: "Should we still search social media?"
   → User chooses to skip → ⚠️ Skipping this track (user confirmed)

━━━ Track F: Internal Database ━━━
📚 Loading tool: Database table search → SQL query
⚠️ Skipping this track: Database query tool not detected. Please configure the corresponding MCP tool if needed

━━━ Track G: User Voice Data ━━━
📚 Loading tool: Database query tool
🔍 Query table: {user_feedback_table} (per user configuration)
✅ Found X relevant issue records
```

---

### Track C: Expert Interviews (Stage 3.5 Workflow Activation)

**Trigger Condition**: AI proactively suggests at end of Stage 3; user selects "need interviews."

**Stage 3 Interview Suggestion** (after research_plan.md confirmation):
AI proactively suggests whether interviews are needed based on topic characteristics:
```
"Would you like to arrange expert interviews? My recommendation is {specific suggestion}"
A. Yes, help me prepare interview guides (→ Enter Stage 3.5 to generate guides)
B. No, skip interviews (→ Proceed directly to Stage 4)
```

**Stage 3.5 Execution**:
1. Load `methodology/interview.md`
2. Based on Stage 2 research definition + Stage 3 hypotheses, generate `interview_guides.md`
3. After user confirms the guides, remind:
```
"Interview guides have been generated. After completing the interviews, share the notes or raw records with me and I'll integrate them into the research.
If they're not done during the research process, I'll remind you before Stage 4 concludes."
```

**⛔ Interview Collection Checkpoint** (End of Stage 4):

Interviews are the user's asynchronous action and typically take several days. **After all other tracks in Stage 4 are complete and before generating `evidence_base.md`**, if Stage 3.5 was activated (`interview_guides.md` was generated), the collection check must be executed:

```
Using AskUserQuestion:
"Stage 3.5 generated interview guides. Have the interviews been completed?"

A. Yes, here are the interview notes/raw records
   → User provides file or path → Read → Organize as Track C evidence → Include in evidence_base.md

B. Not yet, continue with existing data for now
   → Note "Interview evidence pending" in evidence_base.md Track C section
   → Remind user: "No problem. Whenever the interviews are done, share the notes with me and I'll supplement the research and report"
```

**Stage 7 Interview Supplement** (User returns across sessions):
When the user returns with interview files, follow this process:
1. Read the interview file provided by the user (notes, raw records, or transcripts are all acceptable)
2. Organize into standard Track C evidence format (Evidence ID: C1-01, etc.)
3. Append to `evidence_base.md` Track C section
4. Incrementally update `insights.md` (does new evidence change/strengthen/overturn existing insights?)
5. Regenerate `report.html`

**Interview File Processing Rules**:
- Supported formats: .md / .txt / .docx (plain text reading)
- User can drag in files or provide file paths — never require users to place files in a specific directory
- Transcripts (from transcription tools): Extract key viewpoints + annotate speakers
- Handwritten notes: Use directly as evidence source

Regardless of user's choice, record the status in the Track C section of `evidence_base.md`.

---

## Error Handling

### No Access / No Data

**Handling Process**:
```
1. Detect no access or no data
   ↓
2. Clearly inform user of the reason
   ↓
3. Remind user how to configure (if applicable)
   ↓
4. Skip this track, continue to next track
```

**Broadcast Template**:
```
⚠️ Track [X] Skip Notification

Reason: [specific reason]
- No access permission
- Topic type mismatch
- Data source temporarily unavailable

Suggestion: [configuration advice]
- Contact administrator for access if needed
- You can manually provide data

Continuing to next track...
```

---

### Subagent Timeout

**Handling**:
1. Wait for other Subagents to complete
2. Use already-obtained data for the timed-out track
3. Note "incomplete data" in evidence base

---

## Time Estimates

| Phase | Track | Estimated Time |
|-------|-------|---------------|
| Parallel | A+B | 20-40 minutes |
| Sequential | D | 5-10 minutes |
| Sequential | E | 10-20 minutes |
| Sequential | F | 10-20 minutes |
| Sequential | G | 5-10 minutes |
| Conditional | C | 30-60 minutes (if triggered) |
| Integration | Triangulation | 15-20 minutes |

**Estimates by Tier** (includes 20-30% retry/adjustment buffer):
- **Tier 1** (Layer 1 only): 45-75 minutes
- **Tier 2** (Layer 1-2): 75-120 minutes
- **Tier 3** (All layers): 120-180 minutes
- With interviews: +30-60 minutes

---

### Track Activation Decision Matrix

**Three-Dimensional Decision**: Topic characteristics × Data source characteristics × User permissions

#### Dimension 1: Topic Characteristics → Data Needs

| Topic Type | Core Data Needs | Required Tracks | Optional Tracks | Additional When User Is Industry Participant |
|-----------|----------------|----------------|----------------|---------------------------------------------|
| Industry Research | Market size, competitive landscape, trends | A + B | D (historical research) | **F** (internal business data corroboration), **G** (user feedback validating market demand) |
| Competitive Analysis | Competitor data, strategies, movements | A + B | C (deep information), D | **F** (internal competitor comparison data), **G** (user feedback on competitors) |
| Consumer Insights | User profiles, needs, feedback | A + B + E | D, G | **F** (user behavior data) |
| Internal Business Analysis | Business data, user behavior | F + A + B | D (historical research), G | — |
| Business Opportunity Discovery | Market gaps, unmet needs | A + B + E | C, D | **F** (existing business data to identify gaps), **G** (unmet user needs) |
| Business Model Analysis | Revenue models, unit economics | A + B | C (competitor info), D | **F** (own unit economics data) |
| Emerging Industry | Industry definition, players, trends | A + B + C | D | — |

#### Dimension 2: Data Source Characteristics → Applicable Scenarios

| Track | Data Source Characteristics | Best For | Not Suitable For |
|-------|---------------------------|----------|-----------------|
| **A Public Search** | Broad, surface-level, timely | Baseline scanning for all topics | Deep data, internal data |
| **B Directed Sources** | Authoritative, structured, in-depth | Topics requiring authoritative data support | Very emerging fields with no authoritative reports |
| **C Expert Interviews** | Deep, non-public, customized | Non-public information, deep insight validation | Topics with sufficient public information |
| **D Knowledge Base** | Internal accumulation, historical research, methodology | Topics with historical knowledge base | Entirely new fields |
| **E Social Media** | Consumer sentiment, product feedback, trends | Consumer products, C-end products, brand sentiment | B2B business, non-consumer domains |
| **F Internal Database** | Business data, user behavior, transactions | Internal analysis, business diagnostics, data validation | External research where user is not an industry participant, no-access scenarios |
| **G User Voice** | UX issues, complaint pain points | Product optimization, UX analysis, consumer insights | Purely external industry research where user is not an industry participant |

#### Dimension 3: User Permissions → Track Availability

| Track | Permission Requirements | Handling When No Permission |
|-------|------------------------|----------------------------|
| A / B | None | — |
| C | Expert resources or budget needed | Skip, use public data only |
| D | Knowledge base search tool | Skip |
| E | Social media data API access | Skip, or user provides manually |
| F | Database query tool | Skip, or user provides data manually |
| G | Database access permission (per user-configured database project) | Skip, or user provides data manually |

---

### Track Activation Flow (Layer 1 Execution)

```
Step 1: Identify topic type
    ↓
Step 2: Query "Topic Characteristics → Data Needs" table to determine required/optional tracks
    ↓
Step 2.5: Check user identity — are they an industry participant? (Determine from user_brief.md)
          → Yes: Add tracks from "Additional When User Is Industry Participant" column to optional list
          → No: Maintain original optional list
    ↓
Step 3: Check user permissions, mark tracks as available/unavailable
    ↓
Step 4: Check data source characteristic applicability, adjust track priority
    ↓
Step 5: Output "Track Activation List"
```

**Track Activation List Template**:

```markdown
## Track Activation List

### Topic Type
[Industry Research / Competitive Analysis / Consumer Insights / ...]

### Activated Tracks
| Track | Status | Reason |
|-------|--------|--------|
| A Public Search | ✅ Activated | Required track |
| B Directed Sources | ✅ Activated | Required track |
| C Expert Interviews | ⏸️ Pending | Requires user confirmation of resources |
| D Knowledge Base | ✅ Activated | Historical research available |
| E Social Media | ❌ Skipped | Non-consumer topic |
| F Internal Database | ❌ Skipped | External research, no database tool |
| G User Voice | ❌ Skipped | Non-product topic |

### Subagent Distribution
- Subagent 1: Track A (X tasks)
- Subagent 2: Track B (X tasks)
```

---

### Track Execution Priority

When resources are limited, execute in the following priority order:

| Priority | Track | Rationale |
|----------|-------|-----------|
| P0 | A Public Search | Foundational, required for all topics |
| P1 | B Directed Sources | High authority, reliable data |
| P2 | D Knowledge Base | Internal perspective, high efficiency |
| P3 | E/F/G Specialized Sources | Incremental value, activated on demand |
| P4 | C Expert Interviews | High cost, requires user coordination |

---

---

## Layer 1: Hypothesis Mapping & Task Decomposition (Main Session, 10-15 minutes)

### Input
- Stage 3 output: research hypothesis list (`research_plan.md`), containing Q→H→Lens mapping
- Stage 2 output: research definition (`research_definition.md`), containing framework combination and dimension coverage
- Research topic type (for selecting data source combinations)

### Actions

**Step 1.0: Initialize Framework-Evidence Map**

From `research_definition.md`'s sub-question→lens assignment and `research_plan.md`'s Q→H→Lens mapping, automatically generate the Framework-Evidence Map. The map is created in `evidence_base.md` and incrementally updated by subsequent Tracks.

```markdown
## Framework-Evidence Map (Updated per Track)

### [Enhanced Framework Name, e.g., PESTEL]
| Dimension | Related Hypothesis | Evidence ID | Key Finding | Status |
|-----------|-------------------|-------------|-------------|--------|
| Political | H2 | — | — | ⏳ |
| Economic | H1 | — | — | ⏳ |
| Social | H2 | — | — | ⏳ |
| Tech | — | — | — | ⏳ |
| Environmental | — | — | — | ➖ N/A: [S2 annotated reason] |
| Legal | H7 | — | — | ⏳ |

### [Enhanced Framework Name, e.g., Five Forces]
| Force | Related Hypothesis | Evidence ID | Key Finding | Status |
|-------|-------------------|-------------|-------------|--------|
| Existing Competition | H3 | — | — | ⏳ |
| ... | ... | — | — | ⏳ |
```

**Initialization Rules**:
- "Related Hypothesis" column: Filled from Q→H→Lens mapping. Dimensions with hypothesis associations = clear research direction
- ➖ N/A: Inherited from Stage 2 research_definition.md's annotated N/A dimensions and reasons
- ⏳: Has hypothesis association but no evidence yet (awaiting Track population)
- Dimensions with no hypothesis association and not N/A: Also marked ⏳; subsequent Tracks may incidentally cover them

---

**Step 1.1: Hypothesis → Data Point Mapping**

For each hypothesis, identify the key data points that need validation:

```markdown
### Hypothesis H1: [Hypothesis description]

Data points requiring validation:
1. [Data point 1]: e.g., "2024 China SaaS market size"
2. [Data point 2]: e.g., "Leading vendor user penetration rate"
3. [Data point 3]: e.g., "Top competitor market share"
```

**Step 1.2: Data Point → Search Task Mapping**

For each data point, design a search task:

```markdown
| Data Point | Search Question | Keyword Combination | Primary Source | Alternative Source |
|-----------|----------------|--------------------|--------------|--------------------|
| Market size | What is the 2024 China SaaS market size? | "SaaS market size 2024 iResearch" | iResearch (P1) | LeadLeo (P1) |
| User penetration | Leading vendor user counts and penetration? | "SaaS users 2024" | Industry reports (P3) | iResearch reports (P1) |
```

**Step 1.3: Task Distribution Decision**

Assign search tasks to corresponding tracks:

```markdown
## Task Distribution List

### Track A (Subagent 1): Public Data Collection
- Task A1: [Search question 1]
- Task A2: [Search question 2]
- ...

### Track B (Subagent 2): Directed Source Search
- Task B1: Access [data source] and search for [keywords]
- Task B2: Access [data source] and search for [keywords]
- ...

### Track C (Main Session): Expert Interviews
- [If triggered, see interview.md]
```

### Output

1. **Search Task List** (distributed to Subagents)
2. **Subagent Prompt** (including task description, output format, time constraints)

### ⛔ Persist to Disk Immediately After Layer 1

After Layer 1 completes, **immediately write the task decomposition to the "Research Execution Plan" section of `evidence_base.md`**:
- Hypothesis → search task mapping table (hypothesis, data points, search tasks, assigned tracks, keywords)
- Track activation decision table (track, status, rationale)

**Why persist immediately**: Layer 1's task decomposition logic is the critical context for Stage 5 to understand "why this evidence was collected." If it only exists in context, it will be compressed and lost by the platform after 60-120 minutes. Once persisted to disk, Stage 5 can recover the complete hypothesis → evidence causal chain when re-reading.

---

## Layer 2: Parallel Execution (Subagent + Main Session, 30-60 minutes)

### ⛔ Universal Rule: Update Framework-Evidence Map After Each Track

After each Track (A/B/D/E/F/G) completes, perform the following write operations:

**A. Framework-Evidence Map Update**:
1. **Allocate**: Assign this Track's evidence to the corresponding framework dimensions per H→Lens mapping; fill in evidence ID and key findings
2. **Status Update**: ⏳→✅ (evidence supported)
3. **Incidental Coverage**: If an evidence item incidentally relates to a framework dimension without a hypothesis, fill it into the map as well (expanding coverage)
4. **Gap Observation**: Note which dimensions remain ⏳, leaving them for subsequent Tracks or Layer 3

> Note: Map update is a lightweight operation (~2-3 minutes per Track). No need to write complete conclusions — just update the table.

### ⛔ Dual-Objective Research: Hypothesis Validation + Chapter Blueprint Fulfillment (Tier 2/3)

Stage 4 research serves two objectives — consider both during every search:

1. **Hypothesis Validation** (directional judgment): Validate/falsify hypotheses — existing mechanism unchanged
2. **Blueprint Material Collection** (depth assurance): Collect specific materials for the chapter blueprints in `research_definition.md`

> **Key Distinction**: Hypothesis validation stops when confidence is sufficient, but the blueprint may not yet be filled. During searches, actively seek the specific materials the blueprint requires (entity profiles, quantitative comparisons, case details, etc.), not just macro-level conclusions sufficient for hypothesis validation.

**B. ⛔ Evidence Source URL Requirement**:

Each evidence item's "Source" column must include a **traceable, specific source** (not vague descriptions like "industry report" or "LinkedIn post"):
- **Web sources** (Track A/B/E/F): Include specific URL. Subagents already visit the original pages during search — recording the URL is not extra work
- **Database/knowledge base sources** (Track D/G): Include query statement or table name/document ID
- **Untraceable sources** (verbal references, pages taken offline): Mark as C-level (untraceable) in verification column

**C. ⛔ Subagent Data Spot-Check** (after each Track return, executed by Main Session):

After a Subagent returns data, Main Session spot-checks 2-3 key data points with independent searches. Priority targets:
- Outliers (e.g., "single-day $7M ARR increase")
- Data supporting high-impact conclusions (e.g., core evidence for A-class insights)
- Single-source data

Data that fails spot-check should be downgraded to C-level in evidence_base.md with reason annotated.

**D. ⛔ Analysis Notes Write** (mandatory, written in the same pass as evidence list):

When each Track's evidence is written to `evidence_base.md`, **immediately following the evidence list**, write analysis notes with all four fields mandatory:

| Field | Content | Why Mandatory |
|-------|---------|--------------|
| **Expected vs Actual** | What you expected to find based on hypothesis before searching, whether actual results aligned | Helps Stage 5 understand the significance of evidence |
| **Unexpected Signals** | Unanticipated data points/trends/contradictions; write "No unexpected findings" if none | Surprises are often the most valuable insight sources |
| **Evidence Gaps** | Data you wanted but couldn't find, may need other Tracks to supplement | Guides subsequent Tracks and Layer 3 supplementary search direction |
| **Cross-Track Correlation** | Contradictions or corroborations with data from completed Tracks | Explicitly captures "process intuition" during sequential execution |

⛔ **Writing must happen immediately, not retroactively**. When a Track completes, analytical reasoning in context is at its fullest. Delayed writing degrades note quality due to context compression.

---

### Track A: Public Data Collection (Subagent 1)

**Tools**: Search engine → Web scraping (using search and scraping tools available in the current environment)

**Execution Flow**:

```
1. Receive task list (from Main Session)
   ↓
2. For each task:
   ├── Search keywords using search engine
   ├── Use web scraping tool to fetch search result page content
   ├── Trace data back to original source (do not settle for second-hand citations)
   └── Record data + source + link
   ↓
3. Output structured evidence (JSON/Markdown)
   ↓
4. Return to Main Session
```

**Keyword Design Formula**:

```
Core keywords = Subject term + Data term + Source term + Time term

English examples:
- "China SaaS market size 2024 IDC Gartner"
- "second-hand electronics market 2024 report"
- "credit scoring industry global landscape"
```

**Multilingual Search Rules**:
- **Tier 2+**: Default bilingual search (Chinese + English). Each set of Chinese keywords generates a corresponding English version
- English searches use the search engine tool, covering international benchmarks, global institution reports, and worldwide trends
- English-source data in search results must cite sources and be cross-validated against Chinese data

**Source Tracing Rules**:

| Information Encountered | Tracing Action |
|------------------------|---------------|
| Media report citing data | Find the original report/official data |
| "According to XX report" | Find the XX report original text |
| "According to public data" | Find the specific source |
| Blog/self-media analysis | Trace data sources; do not cite directly |

**Output Format** (Subagent 1 returns):

```markdown
## Track A Evidence List

### Task A1: [Search question]

| Evidence ID | Data Content | Original Excerpt | Source | Publication Date | Link | Preliminary Validation |
|------------|-------------|-----------------|--------|-----------------|------|----------------------|
| A1-01 | [Refined data] | "[Key original quote]" | [Source] | [Date] | [URL] | [Pending validation] |
| A1-02 | [Refined data] | "[Key original quote]" | [Source] | [Date] | [URL] | [Pending validation] |

### Task A2: ...
```

---

### Track B: Directed Source Search (Subagent 2)

**Required Data Source Combination**: Based on topic type, select corresponding P0-P2 data sources from the "Data Source Combination Strategy by Topic" section of [`data_sources.md`](./data_sources.md).

**Execution Flow**:

```
1. Receive task list + data source list (from Main Session)
   ↓
2. For each data source:
   ├── Access official website/report platform
   ├── Use site search or keyword search
   ├── Download/scrape relevant reports
   └── Extract core data
   ↓
3. Record search results in structured format
   ↓
4. Return to Main Session
```

**Search Record Format**:

```markdown
## Data Source Search Record

| Data Source | Search Keywords | Reports/Data Found | Relevance | Data Availability |
|-----------|----------------|-------------------|-----------|------------------|
| iResearch | "personal credit" | "2024 China Personal Credit Industry Report" | High | Core data available |
| QuestMobile | "credit scoring APP" | Monthly report summary | Medium | Partial data |
```

**Output Format** (Subagent 2 returns):

```markdown
## Track B Evidence List

### Data Source: [Source name]

| Evidence ID | Data Content | Source Report | Publication Date | Link | Preliminary Validation |
|------------|-------------|-------------|-----------------|------|----------------------|
| B1-01 | [Data] | [Report name] | [Date] | [URL] | [Pending validation] |

### Data Source: ...
```

---

### Track C: Expert Interviews (Main Session)

**Trigger Condition**: Stage 3.5 was activated (user selected "need interviews" in Stage 3)

**Process**: Refer to [`interview.md`](../methodology/interview.md) + Track C workflow above

**Main Session Actions**:
1. Stage 3.5 already generated `interview_guides.md`
2. Stage 4 collection checkpoint asks user about interview progress
3. User provides interview notes/raw records → Read file → Organize as Track C evidence
4. Or user chooses to skip → Mark as pending → Can supplement in Stage 7

---

### Track D: Knowledge Base Search (Main Session)

**Tools**: Knowledge base search tool → Knowledge base document detail tool

**Execution Flow**:

```
1. Receive task list (from Main Session)
   ↓
2. For each task:
   ├── Search keywords using knowledge base search tool
   ├── Filter relevant documents (by relevance and date)
   ├── Use document detail tool to get full content
   └── Extract useful information, record source
   ↓
3. Output structured evidence
   ↓
4. Return to Main Session
```

**Search Strategy**:
- Search personal knowledge base first, then team knowledge base
- Keyword combinations: Subject term + Domain term + Time term
- Document type priority: Research reports > Industry notes > Methodology > Meeting notes

**Output Format**:

```markdown
## Track D Evidence List

### Document: [Document title]

| Evidence ID | Data Content | Document Source | Updated | Document Link | Relevance |
|------------|-------------|----------------|---------|--------------|-----------|
| D1-01 | [Data/viewpoint] | [Knowledge base name] | [Date] | [URL] | High |

### Document: ...
```

---

### Track E: Social Media Data Search (Main Session)

**Tools**: Public web search, browser-readable social-media pages, user-provided links/screenshots, or a separately installed private adapter if the user's environment provides one.

> **Public package boundary**: The GitHub package does not bundle provider-specific Xiaohongshu/RedNote collection scripts. Do not assume local adapter scripts exist. If a private adapter is available in the user's environment, use it only as an optional data collection capability and keep evidence grading explicit.

**Collection Modes**:

| Mode | When to Use | Confidence Handling |
|------|-------------|---------------------|
| Public search | Default for GitHub/public installs | Usually C unless original pages are directly accessible and timestamped |
| Browser-readable note/share links | User provides links or pages are publicly accessible | B/C depending on source visibility and timestamp completeness |
| Screenshots or exports from user | Content is login-gated or private | C unless screenshot/export includes author, date, and URL |
| Optional private adapter | User environment explicitly provides one | Grade by adapter reliability, raw sample size, and source traceability |

**Execution Flow**:

```
1. Receive task list (from Main Session)
   ↓
2. For each task:
   ├── Build keyword groups (brand/product/category/competitor/pain-point terms)
   ├── Search public web or use available private adapter
   ├── Preserve source metadata (author, date, link/screenshot, engagement if visible)
   └── Downgrade weak or indirect evidence instead of overstating it
   ↓
3. Value judgment:
   ├── High-engagement posts → In-depth analysis
   ├── KOL/KOC original content → Record viewpoints
   └── Routine content → Brief record or ignore
   ↓
4. Output structured evidence with evidence grade and source traceability
   ↓
5. Return to Main Session
```

**Search / Collection Guide**:

| Scenario | Query or Collection Pattern |
|----------|-----------------------------|
| Topic search | `{topic} Xiaohongshu`, `{topic} RedNote`, `site:xiaohongshu.com {topic}` |
| Brand/product sentiment | `{brand} review Xiaohongshu`, `{product} user feedback RedNote` |
| Competitor comparison | `{brand A} {brand B} comparison Xiaohongshu` |
| Pain-point discovery | `{category} complaint Xiaohongshu`, `{product} pain point RedNote` |
| User-provided evidence | Ask for note links, screenshots, or exports when access is gated and Track E is material |

**Failure Handling Rules**:

Do not declare Track E unavailable after one failed path. Follow this degradation chain:

```
Step 1: Search public web with multiple keyword groups
    ↓ No useful results
Step 2: Try browser-readable share links or original pages if the user provides them
    ↓ Access is gated or links are unavailable
Step 3: Ask the user for screenshots, exports, or permission to use a configured private adapter
    ↓ Still unavailable
Step 4: Record Track E as an evidence gap and continue with other tracks
```

> When evidence is indirect, login-gated, screenshot-based, or sample size is small, mark it as C-level and avoid quantitative claims that imply complete platform coverage.

**Search Volume & Completion Standards**:

> XHS data is rich — maximize information gathered within reasonable time investment. Search volume provides the statistical foundation for quantitative analysis.

| Condition | Minimum Requirement | Notes |
|-----------|-------------------|-------|
| **Keyword groups** | ≥ 3 groups (core terms + competitor terms + scenario terms) | Cover different search angles |
| **Search depth per group** | ≥ 10 pages (~100 posts/group) | Ensure sample size |
| **Total raw search volume** | ≥ 300 posts | Statistical foundation for quantitative analysis |
| **Quantitative analysis** | Computed from **full** raw dataset | NOT only from selected posts |
| **Qualitative selection** | ≥ 15 high-value posts with user quotes written to evidence_base.md evidence pool (**NOT all going into the report** — report citations are selected by Stage 5/6 as needed) | Deep reviews / KOL opinions / high-engagement / typical user feedback |

> When search volume falls short: expand keywords + try different sort orders (popular/latest/general). If still insufficient, record in analysis notes "Evidence Gaps": "Searched X posts, obtained only Y valuable content." Continue to subsequent Tracks.

**Quantitative-Qualitative Analysis Model**:

```
Search 300+ raw posts
    ├── Full dataset → Quantitative analysis (sentiment ratio, pain point TOP5, brand mention frequency, popularity index)
    └── Selected → Qualitative evidence pool (≥15 high-value posts written to evidence_base.md; report cites 3-5 as needed)
```

| Analysis Type | Quantitative Metrics (full dataset) | Qualitative Evidence (selected) |
|--------------|-------------------------------------|-------------------------------|
| **Pain point analysis** | Pain point TOP5 by percentage + engagement-weighted | Typical user quotes (5-8) |
| **Competitor analysis** | Brand mention frequency + positive/negative ratio | Real user reviews (3 positive + 3 negative) |
| **Demand analysis** | "Seeking recommendations" post percentage + demand trends | Typical help-seeking post summaries (3-5) |
| **Popularity analysis** | Keyword popularity index = post count × avg engagement / 1000 | Top viral content analysis (3 posts) |

**Search Combination Suggestions**:

| Purpose | Search Pattern |
|---------|----------------|
| Consumer sentiment scanning | `"brand_name product_name review Xiaohongshu"` |
| Popular content search | `"keyword Xiaohongshu popular discussion"` |
| Latest activity tracking | `"keyword RedNote recent feedback"` |

**Value Judgment Criteria**:

| Type | Characteristics | Handling |
|------|----------------|----------|
| Worth attention | In-depth reviews, industry trends, KOL opinions, high engagement (10K+) | In-depth analysis |
| Routine content | Reposts, ads, low engagement, low relevance | Brief record or ignore |

**Output Format**:

```markdown
## Track E Evidence List

### Keyword: [keyword]

| Evidence ID | Title | Author | Engagement | Post Date | Link | Value Assessment |
|------------|-------|--------|------------|-----------|------|-----------------|
| E1-01 | [Title] | @blogger | ❤️12K⭐8956 | [Date] | [URL] | High |
| E1-02 | [Title] | @blogger | ❤️3456⭐2100 | [Date] | [URL] | Medium |

### Core Insights Extracted
- [Insight 1]
- [Insight 2]
```

**Quantitative Analysis Methodology**:

> Social media data requires not only qualitative analysis but also quantitative measurement, producing comparable and traceable data insights.

| Dimension | Metric | Calculation Method | Value |
|-----------|--------|-------------------|-------|
| **Popularity Analysis** | Keyword popularity index | Post count × Average engagement / 1000 | Assess topic attention level |
| **Sentiment Analysis** | Positive/negative ratio | Positive posts / Total posts | Assess sentiment trend |
| **Pain Point Clustering** | Top 5 pain points | High-frequency terms + engagement-weighted | Identify core needs |
| **Competitor Mentions** | Brand mention frequency | Brand name occurrences in posts | Compare competitor share of voice |
| **Demand Insights** | Unmet needs | "Seeking recommendations" post percentage | Discover opportunities |

**Quantitative Analysis Output Format**:

```markdown
📊 Social Media Sentiment Analysis Report

【Popularity Analysis】
- Search keyword: "[keyword]"
- Post count: X posts
- Average engagement: ❤️ X ⭐ X 💬 X
- Popularity index: X.X (High/Medium/Low)

【Pain Point Clustering TOP5】
1. Pain point 1 (X%): "keyword"
2. Pain point 2 (X%): "keyword"
...

【Competitor Mentions】
| Brand | Mention Count | Positive Ratio |
|-------|--------------|----------------|
| Brand 1 | X | X% |

【Unmet Needs】
- "Seeking recommendations" post percentage: X%
- Core unmet need: [description]
```

---

### Track F: Internal Database (Main Session)

**Tools**: Database table search tool → Table detail tool → SQL query tool

**Execution Flow**:

```
1. Receive task list (from Main Session)
   ↓
2. Table discovery:
   ├── Use database table search tool to find relevant tables (natural language description)
   ├── Or use field search tool to search by field name
   └── Filter to the 3-5 most relevant tables
   ↓
3. Table comprehension:
   ├── Use table detail tool to get table details
   ├── Understand field definitions and data specifications
   └── Confirm data availability
   ↓
4. Data extraction:
   ├── Write SQL query (SELECT only)
   ├── Add partition filters and LIMIT constraints
   └── Execute query using SQL query tool
   ↓
5. Output structured evidence
   ↓
6. Return to Main Session
```

**SQL Writing Standards**:
```sql
-- ✅ Recommended: Explicit fields, partition filter, row limit
SELECT
    user_id,
    SUM(gmv) AS total_gmv,
    COUNT(*) AS order_count
FROM project_name.table_name
WHERE dt = '2024-01-01'
    AND user_type = 'active'
GROUP BY user_id
LIMIT 1000;

-- ❌ Prohibited: SELECT * full scan on large tables
SELECT * FROM huge_table;
```

**Important Notes**:
1. Only execute SELECT statements — INSERT/UPDATE/DELETE/DROP are prohibited
2. Large table queries must include LIMIT
3. Prefer partition fields (e.g., dt) for filtering
4. User privacy data must be anonymized

**Output Format**:

```markdown
## Track F Evidence List

### Table: [table_name]

| Evidence ID | Data Content | SQL Query | Execution Time | Data Scale | Confidence Level |
|------------|-------------|-----------|---------------|-----------|-----------------|
| F1-01 | [Data] | SELECT... | [Time] | [Row count] | B-level |

### Table: ...
```

---

### Track G: User Voice Data (Main Session)

**Tools**: Database query tool

**Core Data Table**: `{user_feedback_table}` (configured per `data_sources.md` user voice section, project: `{project_name_dev}`)

**Execution Flow**:

```
1. Determine analysis dimensions (from Main Session task list)
   ↓
2. Issue distribution scan:
   ├── GROUP BY first-level category to understand issue type distribution
   ├── Locate categories related to the research topic
   └── Drill down by second/third/fourth-level categories to cluster high-frequency issues
   ↓
3. Pain point deep dive:
   ├── Filter target categories, get question_name original text
   ├── Extract [User Question] [Solution] [User Attitude] components
   └── Cross-analyze by product / sub_product dimensions
   ↓
4. Quantitative + qualitative integration:
   ├── Quantitative: Top N issue volume, trend changes
   └── Qualitative: Typical user quotes (3-5)
   ↓
5. Output structured evidence
```

**SQL Writing Standards**:

```sql
-- ✅ Must include partition filter and LIMIT
SELECT first_level_name, COUNT(*) AS cnt
FROM {user_feedback_table}
WHERE dt >= '20260101'
GROUP BY first_level_name
ORDER BY cnt DESC
LIMIT 20;

-- ⚠️ First-level categories may have a localized prefix, match the raw table values accordingly
WHERE first_level_name = '<raw_category_name>'
```

**Quantitative-Qualitative Integration Requirement**:

| Analysis Type | Quantitative Metrics | Qualitative Insights |
|--------------|---------------------|---------------------|
| **Pain point analysis** | Top 5 category issue volume + percentage | Typical user quotes (3-5) |
| **Product experience** | Sub-product issue volume ranking | User attitude analysis (positive/negative/neutral) |
| **Trend analysis** | Monthly/weekly issue volume changes | New issue type identification |

**Output Format**:

```markdown
## Track G Evidence List

### Issue Distribution Overview
| First-level Category | Issue Count | Percentage |
|---------------------|------------|------------|
| Payments | X | X% |
| After-sales | X | X% |

### High-frequency Pain Points TOP5
| Rank | Fourth-level Category | Issue Count | Typical User Quote |
|------|----------------------|------------|-------------------|
| 1 | [Pain point] | X | "[Quote excerpt]" |

### Evidence Detail
| Evidence ID | Data Content | SQL Query | Data Scale | Confidence Level |
|------------|-------------|-----------|-----------|-----------------|
| G1-01 | [Data] | SELECT... | [Row count] | A-level |
```

---

## Layer 3: Evidence Integration & Triangulation (Main Session, 20-30 minutes)

### Step 3.1: Consolidate Evidence from All Tracks

```markdown
## Evidence Base

### Hypothesis H1: [Hypothesis description]

#### Consolidated Evidence
| Evidence ID | Track | Data Content | Source | Confidence Level |
|------------|-------|-------------|--------|-----------------|
| H1-E01 | A | [Data] | [Source] | Pending validation |
| H1-E02 | B | [Data] | [Source] | Pending validation |
| H1-E03 | C | [Data] | [Interview] | Pending validation |
```

### Step 3.2: Execute Triangulation

For each core data point:

1. **Check whether 2-3 independent sources exist**
2. **Compare data consistency**
3. **If inconsistent, analyze reasons** (different definitions? different time periods?)
4. **Assign confidence level** (A/B/C/D)

**Confidence Level Standards**: A/B/C/D grade definitions are in the "Confidence Level Grading" section of [`triangulation.md`](../methodology/triangulation.md).

### Step 3.2.5: Framework-Evidence Map Final Review

After all Tracks complete, perform a final review of the Framework-Evidence Map:

1. **Classify remaining ⏳ dimensions**:
   - **⚠️ Gap exists and relates to core question** (dimension affects core hypothesis validation) → Targeted supplementary search of 2-3 queries, lightweight supplement, do not re-run the entire Track
   - **➖ N/A** (no direct relation to core question) → Annotate reason; mention in one sentence in framework conclusions

2. **Targeted supplementary search execution**: Only for ⚠️ dimensions, execute 2-3 precise searches in the Main Session. Search results are assigned to corresponding framework dimensions, updating map status.

3. **Map final state**: All dimensions should be ✅ (evidence found) or ➖ N/A (with reason). No residual ⏳ should remain.

### Step 3.3: Output Data Validation List

> Use the "Output Format → Data Validation List" template from [`triangulation.md`](../methodology/triangulation.md).

### Step 3.4: Generate Research Execution Summary

Write into the "Research Execution Summary" section at the **top** of `evidence_base.md`:

1. **Core findings per track**: Re-read each Track's analysis notes and distill the most important finding in 1-2 sentences
2. **Cross-track key signals**:
   - 🔴 Contradiction: Points where different Tracks' data conflict (this is a rich mine for Stage 5 insights)
   - 🟢 Corroboration: Findings confirmed across multiple Tracks (high-confidence evidence)
   - ⚠️ Gap: Key data from only a single source (must annotate confidence level)
3. **Hypothesis validation status overview**: ✅/❌/⏳ status for each hypothesis and core evidence source

**Why this step matters**: During sequential execution, the Main Session naturally accumulates a global understanding of the data across Track D→E→F→G — which contradictions, which corroborations, what was unexpected. But by Stage 5, these understandings have been compressed away by context. The Research Execution Summary **explicitly captures this process intuition**, allowing Stage 5 to recover the global picture in 30 seconds when re-reading.

### Step 3.5: Chapter Blueprint Gap Check & Targeted Supplementary Search (Tier 2/3, ⛔ Mandatory Step)

> **Design Intent**: Hypothesis validation answers "is the direction correct?"; blueprint gap check ensures "is the depth sufficient?" This is Stage 4's safety net — even if blueprint materials were missed during Track searches, they are caught here.

**Execution Flow**:

1. **Re-read blueprint**: Read the chapter blueprints for each sub-question from `research_definition.md`
2. **Item-by-item comparison**: For each blueprint material item, check whether `evidence_base.md` contains corresponding specific data
3. **Mark status**:
   - ✅ Fulfilled — evidence_base contains corresponding specific data/entities/cases, **and meets the blueprint item's specification standard** (quantity, dimensions, scope). A single mention does not qualify as a deep profile; two data points do not qualify as a comparison table.
   - ⚠️ Unavailable — searched but data does not exist (with brief reason, e.g., "Company does not publicly disclose pricing")
   - ❌ Gap — not searched or search was insufficient
4. **Targeted supplementary search**: For all ❌ items, execute precise searches (don't re-run Tracks, directly search for specific information), 1-3 searches per item
5. **Update status**: After supplementary search, update ❌ to ✅ or ⚠️ (if still unfound, annotate reason)
6. **Write to research_definition.md**: Update the checkbox status for each blueprint item

**Completion Standard**: All blueprint material items must be ✅ or ⚠️ (with explanation). No remaining ❌ allowed.

> Note: ⚠️-annotated "unavailable" materials will be reflected in the report's blind spot section — users can see "this data was not found because XXX."

---

## Subagent Task Handoff Standards

> ⛔ **Mandatory requirement**: All Subagent prompts **must** follow the template format below.
> Simplified prompts are prohibited (e.g., "You are a business research assistant, please search for XX").
> Every Subagent prompt must include: ≥5 search keywords (including English), explicit output format, ≥2 target data sources.

### Subagent Prompt Template

```markdown
# Research Task: [Track A/B Public Data Collection / Directed Source Search]

## Background
You are assisting with a business analysis research project, currently in the Stage 4 research execution phase.

## Your Task
[Specific task description for Track A/B]

## Search Task List
| Task ID | Search Question | Chinese Keywords | English Keywords | Target Data Sources |
|---------|----------------|-----------------|-----------------|-------------------|
| A1 | [Question] | [Chinese keywords] | [English keywords] | [Data sources] |
| ... | ... | ... | ... | ... |

> ⛔ **Bilingual Search Mandatory (Tier 2+)**: Each task must have both Chinese and English keywords, searched separately. English keywords are not literal translations of Chinese but professional expressions for the topic in English contexts.
> **Tier 1 search language**: Chinese-only search is sufficient (quick scan does not require English counterparts), but English keywords may be added if the topic involves international markets.

## Output Requirements
1. Each task must output structured data (see format below)
2. **Each task must include both Chinese and English search results**
3. Must trace data to original sources (do not settle for second-hand citations)
4. Record source, publication date, and link for each data point
5. Preliminarily assign confidence levels (if multiple sources available)

## Output Format
```markdown
## Track [A/B] Evidence List

### Task [ID]: [Search question]

| Evidence ID | Data Content | Source | Publication Date | Link | Preliminary Validation |
|------------|-------------|--------|-----------------|------|----------------------|
| ... | ... | ... | ... | ... | ... |
```

## Time Constraint
- Estimated completion time: [X] minutes
- Return evidence to Main Session upon completion
```

### Main Session Integration Actions

1. **Receive Subagent output**
2. **Format standardization** (unified evidence IDs, confidence level annotations)
3. **Organize evidence by hypothesis**
4. **Execute triangulation**
5. **Output data validation list**

---

## Progress Broadcast Mechanism

**Broadcast Nodes**:

| Node | Trigger Condition | Broadcast Content |
|------|-------------------|-------------------|
| Layer 1 complete | Task decomposition done | Search task list, Subagent distribution details |
| Track A complete | Subagent 1 returns | Track A evidence summary, core data found |
| Track B complete | Subagent 2 returns | Track B evidence summary, data source coverage |
| Track C complete | Interviews done (if triggered) | Interview core viewpoint summary |
| Layer 3 complete | Evidence integration done | Data validation list, validation coverage rate |

**Broadcast Format**:

```markdown
## Research Progress Update [timestamp]

### Current Phase
[Layer 1/2/3]

### Completed in This Phase
- [Completed item 1]
- [Completed item 2]

### Key Findings Summary
- [Finding 1]
- [Finding 2]

### Next Steps
- [Next action]

### Items Requiring User Confirmation (if any)
- [Item 1]
```

---

## Quality Checklist

### Layer 1: After Task Decomposition

- [ ] Every hypothesis has corresponding search tasks
- [ ] Every task has clear keywords and target data sources
- [ ] Tasks are correctly distributed to Track A/B/C

### Layer 2: After Subagent Returns

- [ ] Track A evidence traces back to original sources
- [ ] Track B covers the required data source combination
- [ ] Evidence format is standardized

### Layer 3: After Evidence Integration

- [ ] Core data points all have 2+ source validation
- [ ] Confidence level annotations are correct
- [ ] Data validation list is complete
- [ ] Evidence is organized by hypothesis

---

## Common Errors & Prevention

### Error 1: Unclear Subagent Task Descriptions

❌ "Go search for market size"
✅ "Search for 2024 China personal credit market size, keywords 'personal credit market size 2024 iResearch', target data source: iResearch official website"

### Error 2: Inconsistent Evidence Formats

❌ Each Subagent outputs in a different format
✅ Use unified output template; Main Session handles standardization

### Error 3: Superficial Triangulation

❌ Using multiple reports from the same institution as "multiple independent sources"
✅ Ensure sources are truly independent (different institutions, different methodologies)

### Error 4: Opaque Progress

❌ User doesn't know what Subagents are doing
✅ Broadcast progress and key findings at every node

---

## Module Interfaces

### Input Interfaces

| Upstream Module | Input Content | Usage |
|----------------|--------------|-------|
| Stage 2 Research Definition | `research_definition.md` (framework combination, dimension coverage, N/A annotations) | Step 1.0 Framework-Evidence Map initialization |
| Stage 3 Hypotheses & Plan | `research_plan.md` (hypothesis list, Q→H→Lens mapping) | Convert to search tasks + Step 1.0 hypothesis association |
| `data_sources.md` | Required data source catalog | Track B directed search targets |
| `triangulation.md` | Confidence level standards | Layer 3 validation execution |

### Output Interfaces

| Downstream Module | Output Content | Usage |
|------------------|---------------|-------|
| Stage 5 Insight Synthesis | Evidence base, confidence level annotations, Framework-Evidence Map, framework analysis conclusions (including cross-framework findings) | Insight synthesis foundation + cross-dimension pattern recognition |
| Stage 6 Report Generation | Data validation list, framework combination and N/A notes | Report appendix + "Research Background & Methods" section |

---

## Appendix

> Each Layer section above contains complete examples and templates. Execute in Layer 1 → 2 → 3 order during actual execution; inputs/outputs are defined in the corresponding sections.

---

## Post-Stage 4: Framework Analysis Conclusions (Mandatory)

> After all Stage 4 Tracks complete, framework analysis conclusions **must** be aggregated from the Framework-Evidence Map.
> Framework analysis conclusions are based on map data accumulated throughout Stage 4, not extracted all at once from raw evidence.

**Execution Requirements**:

For each framework confirmed in Stage 2 (primary + enhanced frameworks), aggregate conclusions from the Framework-Evidence Map and produce at the end of `evidence_base.md`:

```markdown
## Framework Analysis Conclusions

### [Primary Framework Name] Analysis Conclusions
- **Dimension Coverage**: X/Y dimensions ([N/A dimensions]: [reason])
- **Key Findings**: [3-5 key findings based on ✅ dimensions in the map]
- **Data Support**: [Reference corresponding evidence IDs from the map]
- **Preliminary Assessment**: [Overall assessment from the framework perspective]

### [Enhanced Framework 1] Analysis Conclusions
- **Dimension Coverage**: X/Y dimensions ([N/A dimensions]: [reason])
- **Key Findings**: [2-3 key findings]
- **Relationship to Primary Framework**: [How it deepens analysis of a specific step in the primary framework]

### Cross-Framework Findings (if any)
- [Cross-cutting insights where multiple framework dimensions point to the same conclusion]
- [These are typically the most valuable insight sources for Stage 5]
```

**Purpose**: Ensure frameworks are not just "selected" but actually "used" — the map provides the accumulation process; conclusions provide the aggregated output. Explicit N/A dimension annotation demonstrates analytical completeness and honesty.
