---
name: wiki-onboarding
description: Generates four audience-tailored onboarding guides in an onboarding/ folder — Contributor, Staff Engineer, Executive, and Product Manager. Use when the user wants onboarding documentation for a codebase.
license: MIT
metadata:
  author: Microsoft
  version: "1.0.0"
---

# Wiki Onboarding Guide Generator

Generate four audience-tailored onboarding documents in an `onboarding/` folder, each giving a different stakeholder exactly the understanding they need.

## Source Repository Resolution (MUST DO FIRST)

Before generating any guides, you MUST determine the source repository context:

1. **Check for git remote**: Run `git remote get-url origin` to detect if a remote exists
2. **Ask the user**: _"Is this a local-only repository, or do you have a source repository URL (e.g., GitHub, Azure DevOps)?"_
   - Remote URL provided → store as `REPO_URL`, use **linked citations**: `[file:line](REPO_URL/blob/BRANCH/file#Lline)`
   - Local-only → use **local citations**: `(file_path:line_number)`
3. **Determine default branch**: Run `git rev-parse --abbrev-ref HEAD`
4. **Do NOT proceed** until source repo context is resolved

## When to Activate

- User asks for onboarding docs or getting-started guides
- User runs `/deep-wiki:onboard` command
- User wants to help new team members understand a codebase

## Output Structure

Generate an `onboarding/` folder with these files:

```
onboarding/
├── index.md                    # Onboarding hub — links to all 4 guides with audience descriptions
├── contributor-guide.md        # For new contributors (assumes Python or JS background)
├── staff-engineer-guide.md     # For staff/principal engineers
├── executive-guide.md          # For VP/director-level engineering leaders
└── product-manager-guide.md    # For product managers and non-engineering stakeholders
```

### `index.md` — Onboarding Hub

A landing page with:
- **One-paragraph project summary**
- **Guide selector table**:

| Guide | Audience | What You'll Learn | Time |
|-------|----------|-------------------|------|
| [Contributor Guide](./contributor-guide.md) | New contributors with Python/JS experience | Setup, first PR, codebase patterns | ~30 min |
| [Staff Engineer Guide](./staff-engineer-guide.md) | Staff/principal engineers | Architecture, design decisions, system boundaries | ~45 min |
| [Executive Guide](./executive-guide.md) | VP/directors of engineering | Capabilities, risks, team topology, investment thesis | ~20 min |
| [Product Manager Guide](./product-manager-guide.md) | Product managers | Features, user journeys, constraints, data model | ~20 min |

## Language Detection

Scan the repository for build files to determine the primary language for code examples:
- `package.json` / `tsconfig.json` → TypeScript/JavaScript
- `*.csproj` / `*.sln` → C# / .NET
- `Cargo.toml` → Rust
- `pyproject.toml` / `setup.py` / `requirements.txt` → Python
- `go.mod` → Go
- `pom.xml` / `build.gradle` → Java

---

## Guide 1: Contributor Guide

**File**: `onboarding/contributor-guide.md`
**Audience**: Engineers joining the project. Assumes proficiency in Python or JavaScript and general software engineering experience.
**Length**: 1000–2500 lines. Progressive — each section builds on the last.

### Required Sections

**Part I: Foundations** (skip if repo uses Python or JS)
1. **{Primary Language} for Python/JS Engineers** — Syntax comparison tables, async model, collections, type system, package management. Concrete code side-by-side, NOT abstract descriptions.
2. **{Primary Framework} Essentials** — Compare to equivalent Python/JS frameworks (e.g., FastAPI, Express). Request pipeline, routing, DI, config.

**Part II: This Codebase**
3. **What This Project Does** — 2-3 sentence elevator pitch
4. **Project Structure** — Annotated directory tree (what lives where and why). Include `graph TB` architecture overview.
5. **Core Concepts** — Domain-specific terminology explained with code examples. Use `erDiagram` for data model.
6. **Request Lifecycle** — `sequenceDiagram` (with `autonumber`) tracing a typical request end-to-end.
7. **Key Patterns** — "If you want to add X, follow this pattern" templates with real code

**Part III: Getting Productive**
8. **Prerequisites & Setup** — Table: Tool, Version, Install Command. Step-by-step with expected output at each step.
9. **Your First Task** — End-to-end walkthrough of adding a simple feature
10. **Development Workflow** — Branch strategy, commit conventions, PR process. Use `flowchart` diagram.
11. **Running Tests** — All tests, single file, single test, coverage commands
12. **Debugging Guide** — Common issues table: Symptom, Cause, Fix
13. **Common Pitfalls** — Mistakes every new contributor makes and how to avoid them

**Appendices**
- **Glossary** (40+ terms)
- **Key File Reference** — Table: Path, Purpose, Why It Matters, Source
- **Quick Reference Card** — Cheat sheet of most-used commands and patterns

### Rules
- All code examples in the detected primary language
- Every command must be copy-pasteable with expected output
- **Minimum 5 Mermaid diagrams** (architecture, ER, sequence, flowchart, state)
- Use Mermaid for workflow diagrams (dark-mode colors) — add `<!-- Sources: ... -->` comment block after each
- Ground all claims in actual code — cite using linked format

---

## Guide 2: Staff Engineer Guide

**File**: `onboarding/staff-engineer-guide.md`
**Audience**: Staff/principal engineers who need the "why" behind every decision. Deep systems experience, may not know this repo's language.
**Length**: 800–1200 lines. Dense, opinionated, architectural.

### Required Sections

1. **Executive Summary** — What the system is in one dense paragraph. What it owns vs delegates.
2. **The Core Architectural Insight** — The SINGLE most important concept. Include pseudocode in a DIFFERENT language from the repo.
3. **System Architecture** — Full Mermaid `graph TB` diagram. Call out the "heart" of the system.
4. **Domain Model** — Mermaid `erDiagram` of core entities. Data invariants table: Entity, Invariant, Enforced By, Source.
5. **Key Abstractions & Interfaces** — `classDiagram` showing load-bearing abstractions.
6. **Request Lifecycle** — `sequenceDiagram` (with `autonumber`) showing typical request from entry to response.
7. **State Transitions** — `stateDiagram-v2` for entities with meaningful lifecycle states.
8. **Decision Log** — Table: Decision, Alternatives Considered, Rationale, Source.
9. **Dependency Rationale** — Table: Dependency, Purpose, What It Replaced, Source.
10. **Data Flow & State** — How data moves through the system. Storage comparison table.
11. **Failure Modes & Error Handling** — `flowchart` for error propagation paths.
12. **Performance Characteristics** — Bottlenecks, scaling limits, hot paths.
13. **Security Model** — Auth, authorization, trust boundaries, data sensitivity.
14. **Testing Strategy** — What's tested, what isn't, testing philosophy.
15. **Known Technical Debt** — Table: Issue, Risk Level, Affected Files, Source.
16. **Where to Go Deep** — Recommended reading order of source files, links to wiki sections.

### Rules
- Use **pseudocode in a different language** to explain concepts
- Use **comparison tables** to map unfamiliar concepts (e.g., `Task<T>` = `Awaitable[T]`)
- Dense prose with tables, NOT shallow bullet lists
- Every claim backed by linked citation
- **Minimum 5 Mermaid diagrams** (architecture, ER, class, sequence, state, flowchart)
- Each diagram followed by `<!-- Sources: ... -->` comment block
- **Use tables aggressively** — decisions, dependencies, debt should ALL be tables with Source columns
- Focus on WHY decisions were made, not just WHAT exists

---

## Guide 3: Executive Guide

**File**: `onboarding/executive-guide.md`
**Audience**: VP/director of engineering. Needs capability overview, risk assessment, and investment context — NOT code-level details.
**Length**: 400–800 lines. Strategic, concise, decision-oriented.

### Required Sections

1. **System Overview** — What it does, who uses it, business value in 2-3 sentences
2. **Capability Map** — Table: Capability, Status (Built/Partial/Planned), Maturity, Dependencies. What the system can and cannot do today.
3. **Architecture at a Glance** — High-level Mermaid `graph LR` diagram. Services, data stores, external integrations — NO internal code details. Focus on deployment units and team boundaries.
4. **Team Topology** — Which team/person owns which components. Table: Component, Owner, Criticality, Bus Factor.
5. **Technology Investment Thesis** — Why these technologies were chosen. Table: Technology, Purpose, Alternatives Considered, Risk Level.
6. **Risk Assessment** — Table: Risk, Likelihood, Impact, Mitigation, Owner. Cover reliability, security, scalability, compliance.
7. **Cost & Scaling Model** — How costs scale with usage. What the bottlenecks are. When the next scaling investment is needed.
8. **Dependency Map** — `graph TB` showing critical external dependencies. Table: Dependency, Type (Service/Library/Platform), Risk if Unavailable.
9. **Key Metrics & Observability** — What's measured, what dashboards exist, alerting coverage. Table: Metric, Current Value, Target, Source.
10. **Roadmap Alignment** — Engineering workstreams mapped to business priorities. What's in progress, what's planned, what's blocked.
11. **Technical Debt Summary** — Top 5 debt items with business impact. Table: Issue, Business Impact, Effort to Fix, Priority.
12. **Recommendations** — 3-5 actionable recommendations for the next quarter, prioritized by impact.

### Rules
- **NO code snippets** — this guide is for engineering leaders, not coders
- **Diagrams at service/team level**, not class/function level
- **Every claim backed by evidence** — cite wiki sections, architecture docs, or source files
- **Minimum 3 Mermaid diagrams** (architecture overview, dependency map, capability/roadmap)
- Tables for every structured finding — this audience reads tables, not prose
- **Business language** — translate technical concepts into impact (reliability, velocity, cost, risk)

---

## Guide 4: Product Manager Guide

**File**: `onboarding/product-manager-guide.md`
**Audience**: Product managers and non-engineering stakeholders. Needs to understand what the system does, what's possible, and where the boundaries are — NOT how it's built.
**Length**: 400–800 lines. User-centric, feature-focused, constraint-aware.

### Required Sections

1. **What This System Does** — 2-3 sentence elevator pitch in user-facing language (no jargon)
2. **User Journey Map** — Mermaid `graph LR` or `journey` diagram showing primary user flows through the system
3. **Feature Capability Map** — Table: Feature, Status (Live/Beta/Planned/Not Possible), User-Facing Behavior, Limitations. Comprehensive map of what's built and what's not.
4. **Data Model (Product View)** — Simplified Mermaid `erDiagram` showing entities users interact with. Explain in business terms (e.g., "A Project has many Documents" not "FK relationship").
5. **Configuration & Feature Flags** — Table: Flag/Config, What It Controls, Default, Who Can Change It. What can be toggled without engineering work.
6. **API Capabilities** — What integrations are possible. Table: Capability, Endpoint/Method, Authentication, Rate Limits. Written for integration partners, not developers.
7. **Performance & SLAs** — Response times, throughput limits, availability targets. Table: Operation, Expected Latency, Throughput Limit, Current SLA.
8. **Known Limitations & Constraints** — Honest list of what the system can't do or does poorly. Table: Limitation, User Impact, Workaround, Planned Fix.
9. **Data & Privacy** — What data is collected, where it's stored, retention policies, compliance status. Table: Data Type, Storage Location, Retention, Compliance.
10. **Glossary** — Domain terms explained in plain language (not engineering jargon)
11. **FAQ** — 10+ common questions a PM would ask, answered concisely

### Rules
- **ZERO engineering jargon** — no "middleware", "dependency injection", "ORM". Use plain language.
- **User-centric framing** — describe everything in terms of what users experience, not how code works
- **Minimum 3 Mermaid diagrams** (user journey, data model, feature map/capability overview)
- Tables for every structured finding — PMs scan tables, not prose
- If a technical concept must be mentioned, explain it in one sentence (e.g., "Feature flags — toggles that let us turn features on/off without deploying code")
- Every claim grounded in evidence — cite wiki sections or source files for verification

---

## Mermaid Diagram Rules (ALL guides)

ALL diagrams must use dark-mode colors:
- Node fills: `#2d333b`, borders: `#6d5dfc`, text: `#e6edf3`
- Subgraph backgrounds: `#161b22`, borders: `#30363d`
- Lines: `#8b949e`
- If using inline `style` directives, use dark fills with `,color:#e6edf3`
- Do NOT use `<br/>` in Mermaid labels (use `<br>` or line breaks)

## Validation

After generating each guide, verify:
- All file paths mentioned actually exist in the repo
- All class/method names are accurate (not hallucinated)
- Mermaid diagrams render (no syntax errors)
- No bare HTML-like tags (generics like `List<T>`) outside code fences — wrap in backticks
- Each guide is appropriate for its audience — no code in Executive/PM guides
