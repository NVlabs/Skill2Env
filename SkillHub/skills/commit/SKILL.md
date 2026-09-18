---
name: commit
description: Create a git commit with a good message. Use when the user says "commit", "save changes", "commit this", or asks to create a commit after making code changes.
allowed-tools: Bash, Read, Grep, Glob
---

# Git Commit

Review all staged changes and create a well-crafted commit message.

## Steps

1. Run `git status` to see staged and unstaged changes
2. Run `git diff --cached` to review staged changes in detail
3. If nothing is staged, run `git diff` and suggest what to stage based on the changes
4. Run `git log --oneline -5` to see recent commit message style in the repo
5. Draft a concise commit message following conventional commits format:
   - `feat:` — new feature
   - `fix:` — bug fix
   - `refactor:` — code restructuring without behavior change
   - `docs:` — documentation changes
   - `test:` — adding or updating tests
   - `chore:` — build, tooling, config changes
6. Focus the message on **why** not **what** — the diff shows what changed
7. Keep the first line under 72 characters
8. Add a body paragraph if the change is non-trivial
9. Create the commit

Do NOT push unless explicitly asked. Do NOT use `--no-verify` or skip hooks.

$ARGUMENTS
