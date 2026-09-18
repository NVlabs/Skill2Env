---
name: c-obsidian
description: Obsidian vault as persistent memory — daily notes, session logs, knowledge capture, and search across your entire vault.
tags: [obsidian, notes, knowledge-base, memory, daily-notes]
---

# Obsidian — Knowledge Base & Memory

Manage your Obsidian vault as a persistent memory layer. Use it for daily notes, session logs, knowledge capture, and searching your second brain.

## CLI Commands

```bash
# Search before creating (avoid duplicates)
obsidian-cli search "query"
obsidian-cli search --tag "project" --folder "Work"

# Create and edit
obsidian-cli create "Title" --content "Body"
obsidian-cli create "Title" --template "Daily Note"
obsidian-cli append "Note Title" "Additional content"

# Open, list, vault
obsidian-cli open "Note Title"
obsidian-cli list --folder "Projects"
obsidian-cli tags
obsidian-cli vault --list
```

## Daily Notes Integration

When the user starts a session, check for today's daily note:

```bash
obsidian-cli search --folder "Daily Notes" "$(date +%Y-%m-%d)"
```

If none exists, create one:

```bash
obsidian-cli create "$(date +%Y-%m-%d)" --folder "Daily Notes" --content "# $(date +%Y-%m-%d)\n\n## Tasks\n\n## Notes\n\n## Session Log\n"
```

Append a session log entry at the end of each session:

```bash
obsidian-cli append "$(date +%Y-%m-%d)" "### Session $(date +%H:%M)\n- [summary of what was done]\n"
```

## Memory Sync (Auto)

If both c-memory and c-obsidian are installed (check `ls ~/.claude/skills/c-memory/`), keep them in sync automatically:

### Bidirectional Sync
- `~/.claude/memory/` → Obsidian `AI/` folder (on every memory write)
- Obsidian `AI/` → `~/.claude/memory/` (on session start, if Obsidian has newer content)

### Sync Commands
```bash
# Push memory to Obsidian
obsidian-cli create "AI/Memory" --content "$(cat ~/.claude/memory/MEMORY.md)"
obsidian-cli create "AI/People" --content "$(cat ~/.claude/memory/people.md)"

# Pull from Obsidian to check for updates
obsidian-cli search --folder "AI" "Memory"

# Append session log to daily note
obsidian-cli append "$(date +%Y-%m-%d)" "### Claude Session $(date +%H:%M)\n- [summary]"
```

### Rules
- When the user says "remember this", save to both systems
- Obsidian is the long-term archive; `~/.claude/memory/` is the quick-access cache
- MEMORY.md is authoritative for quick facts; Obsidian is richer context

## Guidelines

- Always search before creating to avoid duplicate notes
- Use frontmatter tags: `tags: [project, active]`
- File paths are relative to vault root
- Obsidian app does not need to be running
- Keep daily notes in a consistent folder (default: `Daily Notes/`)
