---
name: c-notes
description: Manage Apple Notes and Apple Reminders from the CLI. Uses memo for Notes and remindctl for Reminders. Supports listing, searching, reading, creating notes, and adding/completing reminders.
tags: [notes, reminders, apple, memo, remindctl]
---

This skill manages Apple Notes via `memo` and Apple Reminders via `remindctl`.

## Apple Notes — `memo`

```bash
memo list                          # List all notes
memo list --folder "Work"          # List notes in a folder
memo search "query"                # Search notes by content or title
memo read "Note Title"             # Read a specific note
memo create "Title" "Body text"    # Create a new note
memo create --folder "Work" "Title" "Body"
memo delete "Note Title"           # Delete a note
memo folders                       # List all folders
```

## Apple Reminders — `remindctl`

```bash
remindctl list                     # List all reminders
remindctl list "List Name"         # List reminders in a specific list
remindctl add "Task" --due "tomorrow 9am"
remindctl add "Task" --list "Work" --due "2026-03-01"
remindctl complete "Task name"     # Mark reminder as complete
remindctl delete "Task name"       # Delete a reminder
remindctl lists                    # Show all reminder lists
```

## Usage Guidelines

- Use `memo search` before creating to avoid duplicates.
- Dates for `remindctl --due` accept natural language ("tomorrow", "next Monday") and ISO format.
- If `memo` or `remindctl` is not found, inform the user and suggest installing the OpenPaw c-notes skill.
- Notes are stored locally in Apple Notes app — no external API needed.

## Notes

- `memo` requires macOS and Apple Notes app.
- `remindctl` requires macOS and Apple Reminders app.
- Both tools operate on the local user account.
