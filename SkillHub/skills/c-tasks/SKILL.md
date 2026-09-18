---
name: c-tasks
description: Manage tasks across Todoist (todoist-cli), Things 3 (things-cli), and Taskwarrior (task). Detects which tool is installed. Supports adding, listing, completing, and filtering tasks across all three managers.
tags: [tasks, todoist, things, taskwarrior, productivity, todo]
---

This skill supports three task managers. Detect which is available with `which todoist-cli things-cli task` and use accordingly.

## Todoist — `todoist-cli`

```bash
todoist-cli list                           # List today's tasks
todoist-cli list --project "Work"          # Tasks in a project
todoist-cli add "Task name" --due today --priority 2
todoist-cli add "Task" --project "Work" --label "urgent"
todoist-cli complete <task-id>
todoist-cli delete <task-id>
todoist-cli projects                       # List all projects
todoist-cli search "query"
```

## Things 3 — `things-cli`

```bash
things-cli today                           # Today's tasks
things-cli list                            # All tasks
things-cli list --area "Work"
things-cli add "Task name" --when today --tag "urgent"
things-cli add "Task" --project "Project Name" --deadline "2026-03-01"
things-cli complete "Task name"
things-cli projects                        # List projects
things-cli areas                           # List areas
```

## Taskwarrior — `task`

```bash
task list                                  # List pending tasks
task next                                  # Highest-priority next task
task add "Task name" due:tomorrow pri:H project:work
task add "Task" +tag1 +tag2
task <id> done                             # Complete a task
task <id> delete
task <id> modify priority:H
task project:work list                     # Filter by project
task +OVERDUE list                         # Overdue tasks
task summary                               # Project summary
```

## Usage Guidelines

- Check which tool is installed before running commands.
- If multiple are installed, ask the user which they prefer or use the one matching their request context.
- For natural language dates, Todoist and Things handle them natively; Taskwarrior uses `due:YYYY-MM-DD` or `due:tomorrow`.

## Notes

- Todoist requires API token configured via `todoist-cli auth`.
- Things 3 requires macOS and the Things 3 app.
- Taskwarrior stores tasks locally in `~/.task/`.
