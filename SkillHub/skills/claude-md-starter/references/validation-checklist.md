# Validation Checklist

Run during Node 6 before writing CLAUDE.md to disk. Resolve every failure before writing. Never write a file that fails a required check.

---

## Required Sections Check

| Section | Required? | Pass Condition |
|---|---|---|
| Project Overview | Always | Non-empty, ≥ 1 sentence, project-specific (not generic) |
| Tech Stack | Always | At least language + framework identified |
| Commands | Always | ≥ 2 runnable commands present |
| Architecture | If project has > 1 directory | ≥ 3 directories listed with one-line descriptions |
| Code Conventions | If lint config found or grill-me provided rules | ≥ 1 non-trivial, actionable rule |
| Testing | If test framework detected | Test run command present |
| What NOT To Do | Always | ≥ 2 entries written as hard imperatives |
| Environment Setup | If .env.example or services found | All required env var names listed |

---

## Content Quality Gates

- [ ] No placeholder text — search the output for `[TODO`, `[add`, `[your`, `[fill`, `[insert`
- [ ] All commands in the Commands section were found in signal files or explicitly confirmed by the user — no invented commands
- [ ] Architecture paths match directories actually found on disk
- [ ] What NOT To Do entries are specific to this project, not generic advice ("don't write bad code")
- [ ] Project Overview is project-specific — not "This is a web application built with modern tools"

---

## Failure Handling

| Failure | Recovery action |
|---|---|
| Commands has < 2 entries | Ask: "What commands do you use to run, build, and test this project?" |
| What NOT To Do has < 2 entries | Ask: "Are there any files, directories, or actions Claude should never touch in this repo?" |
| Project Overview is empty | Ask: "What does this project do in one sentence?" |
| Architecture paths don't exist on disk | Remove the non-existent paths before writing |
| Placeholder text found | Resolve each one before writing — never write `[TODO]` or equivalent to disk |
| Tech Stack section is empty | Ask: "What language and framework does this project use?" |

Recovery questions count toward the 3-question grill-me limit. If the limit was already reached, ask only the single most critical recovery question.

---

## Diff-and-Merge Validation

Applies only when an existing CLAUDE.md with > 200 characters was found in Node 1.

- [ ] Diff summary table was shown to the user before writing
- [ ] User explicitly selected option A, B, or C
- [ ] Chosen merge strategy was applied correctly:
  - **A:** Existing content preserved; only new and enhanced sections added
  - **B:** Entire file replaced with generated version
  - **C:** Each conflicting section reviewed individually; user chose which version to keep
- [ ] No content from the existing file was silently dropped under option A or C

---

## Post-Write Confirmation

After successfully writing the file, output exactly:

```
✓ CLAUDE.md written — [X] sections populated from repo scan, [Y] from your answers.
```

If diff-and-merge was used, also output a one-line summary:

```
Sections added: [list]. Sections unchanged: [list].
```

Do not output anything else after the confirmation line.
