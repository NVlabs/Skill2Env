---
name: claude-md-starter
description: "Generates a fully structured, project-specific CLAUDE.md by scanning the repo for signal files (package.json, Makefile, .github/workflows/, .env.example, etc.), inferring stack, commands, architecture, and conventions, then asking at most 3 targeted questions for what cannot be inferred. Use whenever the user says 'create a CLAUDE.md', 'my CLAUDE.md is blank', 'generate project context', 'initialize CLAUDE.md', 'set up Claude context for this repo', 'fill in my CLAUDE.md', or any variation where someone needs their project context documented for Claude. If a CLAUDE.md already exists with content, runs a diff-and-merge flow before writing."
user-invokable: true
argument-hint: ""
metadata:
  category: utility
  version: 1.0.0
---

# Claude.md Starter — Project Context Generator

Scans the repo, infers the tech stack and conventions, asks at most 3 targeted questions, and writes a populated CLAUDE.md that gives Claude full project context from session one.

## Invocation Triggers

**Explicit:**
- "create a CLAUDE.md"
- "my CLAUDE.md is blank"
- "generate project context"
- "initialize CLAUDE.md"
- "set up Claude context for this repo"
- "fill in my CLAUDE.md"
- "run the claude-md-starter skill"

**Implicit:**
- User pastes a near-empty CLAUDE.md and asks Claude to populate it
- User keeps re-explaining the same project context at the start of sessions

Run immediately when triggered — no upfront questions before scanning.

## Workflow (6 Nodes)

| Node | Role |
|---|---|
| 1 — Detect | Check if CLAUDE.md exists and measure content length |
| 2 — Scan | Read signal files from the project root (see `references/scan-signals.md`) |
| 3 — Infer | Draft all sections that can be derived from scanned signals |
| 4 — Grill-me | Ask at most 3 questions for what cannot be inferred |
| 5 — Generate | Write the full CLAUDE.md using the template in `references/claude-md-template.md` |
| 6 — Validate | Confirm required sections are present and non-placeholder |

## Node 1 — Detect

Check for CLAUDE.md at the project root.

**If not found:** Proceed directly to Node 2.

**If found and has ≤ 200 characters:** Treat as blank — proceed to Node 2.

**If found and has > 200 characters:** Run the diff-and-merge flow before writing:

1. Read the existing file
2. Complete Nodes 2–4 to produce the generated version
3. Compare section by section — for each of the 8 required sections, classify as:
   - **NEW** — exists in generated, absent or empty in existing
   - **ENHANCED** — both versions have content; generated version adds more
   - **SAME** — both versions have equivalent content
   - **CONFLICT** — both versions have different non-empty content

4. Present a diff summary table:

```
Section              | Existing | Generated | Action
---------------------|----------|-----------|-------
Project Overview     | present  | enhanced  | +additions available
Tech Stack           | absent   | new       | will add
Commands             | present  | enhanced  | +2 commands found
Architecture         | absent   | new       | will add
Code Conventions     | present  | same      | no change
Testing              | absent   | new       | will add
What NOT To Do       | absent   | new       | will add
Environment Setup    | absent   | new       | will add
```

5. Offer three options:
   - **A (Recommended)** — Keep existing content + add new and enhanced sections only (safe, additive)
   - **B** — Full replace with generated version
   - **C** — Review each conflicting section individually before writing

6. Write the chosen merge result.

## Node 2 — Scan

Read signal files using the catalog in `references/scan-signals.md`. For each file found, extract the fields it reveals. Missing files are skipped silently.

Run all reads in parallel where possible:

1. `package.json` — framework, scripts, package manager, dependencies
2. `pyproject.toml` / `requirements.txt` / `setup.py` — Python stack
3. `Cargo.toml` / `go.mod` / `pom.xml` / `build.gradle` — language
4. `Makefile` / `justfile` — named commands
5. `.github/workflows/*.yml` — CI/CD steps, deploy targets
6. `Dockerfile` / `docker-compose.yml` — runtime environment, services
7. `.eslintrc.*` / `.prettierrc.*` / `eslint.config.*` — JS/TS code style
8. `ruff.toml` / `.flake8` / `mypy.ini` — Python lint/type config
9. `jest.config.*` / `vitest.config.*` / `pytest.ini` / `conftest.py` — test framework
10. `tsconfig.json` — TypeScript settings
11. `.env.example` / `.env.sample` — required environment variables
12. `README.md` (first 40 lines only) — project description
13. Top-level directory listing — architecture pattern
14. `.gitignore` — build artifacts and generated files

## Node 3 — Infer

Using scanned data, populate as many sections as possible before asking questions:

- **Project Overview** → from README.md first paragraph; fall back to `package.json` `description` field
- **Tech Stack** → from language files + framework dependencies
- **Commands** → from `package.json` scripts, Makefile targets, workflow run steps
- **Architecture** → from top-level directory structure
- **Code Conventions** → from eslint/prettier/ruff config values
- **Testing** → from test config files and test directory location
- **What NOT To Do** → from `.gitignore` build outputs, workflow branch protection, lock files
- **Environment Setup** → from `.env.example` variable names and docker-compose services

## Node 4 — Grill-Me Intake

Ask only for what cannot be inferred. Maximum 3 questions. Skip any question whose answer is already clear from scanned files.

Present all applicable questions together in one message — never ask them across multiple turns:

> **Quick questions to finish your CLAUDE.md** (answer whichever apply):
>
> 1. What does this project do in one sentence? *(skip if README was found)*
> 2. Are there any files, directories, or systems that should never be touched or auto-modified by Claude?
> 3. Any team conventions not captured in your lint config? *(naming patterns, PR size, commit format, review process)*

## Node 5 — Generate

Produce the CLAUDE.md using the exact section structure from `references/claude-md-template.md`.

**Critical rules:**
- Every populated section must have real content — no `[TODO: add your X here]` placeholders
- If a section cannot be filled at all, omit it entirely rather than writing a placeholder
- Commands must be exact and runnable (`npm run dev`, not "run the dev server")
- What NOT To Do must have at least 2 entries
- Write in imperative, direct style ("Run tests with...", "Never edit files in...")
- No heading levels deeper than H2 within sections

## Node 6 — Validate

Before writing, verify against `references/validation-checklist.md`:

- [ ] All populated sections have real content (no placeholders)
- [ ] Commands section has ≥ 2 runnable commands
- [ ] What NOT To Do has ≥ 2 entries
- [ ] No unreplaced placeholder text remains
- [ ] If existing CLAUDE.md had > 200 characters, diff-and-merge flow was completed

If Commands or What NOT To Do would fail: ask one final targeted question before writing.

## Output

Write the file to `CLAUDE.md` at the project root. After writing, print a one-line confirmation:

```
✓ CLAUDE.md written — X sections populated from repo scan, Y from your answers.
```

If in diff-and-merge mode, also print which sections were added vs. left unchanged.

## Anti-Patterns To Reject

- Generating CLAUDE.md without running the scan first
- Asking more than 3 intake questions
- Writing placeholder sections ("add your commands here")
- Overwriting an existing populated CLAUDE.md without running the diff-and-merge flow
- Writing generic boilerplate not specific to the scanned project
- Including commands that weren't found in signal files and weren't confirmed by the user

## References

- `references/scan-signals.md` — full catalog of signal files and what each reveals
- `references/claude-md-template.md` — canonical CLAUDE.md section structure and style rules
- `references/validation-checklist.md` — required fields and quality gates before writing

---

**Version:** 1.0.0
