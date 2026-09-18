---
name: c-linear
description: Manage Linear issues and projects using the `linear` CLI. List and filter issues, create new issues, update status, start work on a branch, and create linked pull requests directly from the terminal.
tags: [linear, issues, project-management, tasks, sprint, prs]
---

## What This Skill Does

Uses the `linear` CLI to manage Linear issues — list, create, update, and transition issues, as well as start work and create linked PRs.

## CLI Tool: `linear`

### List & View Issues

```bash
linear issue list                          # List your assigned issues
linear issue list --team ENG               # Filter by team
linear issue list --state "In Progress"    # Filter by state
linear issue view ENG-123                  # View issue details
```

### Create Issues

```bash
linear issue create \
  --title "Fix login redirect bug" \
  --description "Users are redirected to /home instead of /dashboard" \
  --team ENG \
  --priority 2 \
  --label bug
```

### Update & Transition Issues

```bash
linear issue update ENG-123 --state "In Progress"
linear issue update ENG-123 --assignee me
linear issue update ENG-123 --priority 1
```

### Start Work

```bash
# Creates a git branch linked to the issue
linear issue start ENG-123
```

### Create a PR

```bash
# Creates a PR linked to the Linear issue
linear pr create ENG-123
```

## Usage Guidelines

1. Use `linear issue list` before creating issues to avoid duplicates.
2. When starting work, `linear issue start` handles branch creation and status update in one command.
3. Use issue identifiers (e.g., `ENG-123`) consistently — they are case-insensitive.

## Notes

- Requires `linear auth` to be completed before use.
- Priority levels: 1 = Urgent, 2 = High, 3 = Medium, 4 = Low
