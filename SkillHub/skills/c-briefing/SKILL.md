---
name: c-briefing
description: Daily briefing — morning summary of email, calendar, tasks, weather. Can run on a schedule via launchd/cron.
tags: [briefing, daily, morning, summary, schedule]
---

# Daily Briefing

Compile a morning summary from your installed skills. Checks what's available and builds the briefing accordingly.

## What to Include

Check which skills are installed and pull from each:

| If installed | Include in briefing |
|---|---|
| c-email | Unread email count + top 5 subjects |
| c-calendar | Today's events + tomorrow preview |
| c-tasks | Due today + overdue items |
| c-notes | Recently modified notes |
| c-github | Open PRs, review requests, CI failures |
| c-slack | Unread DM count + mentions |
| c-tracking | Package delivery updates |

## Briefing Format

```
Good morning, {name}! Here's your briefing for {date}:

📧 Email: 12 unread — 3 flagged
  → "Q4 Budget Review" from Sarah
  → "Deploy approval needed" from CI Bot
  → "Lunch tomorrow?" from Mike

📅 Calendar:
  → 9:00 AM  Team standup (30 min)
  → 11:00 AM  1:1 with Alex (45 min)
  → 2:00 PM  Sprint review (1 hr)

✅ Tasks: 3 due today, 1 overdue
  → [overdue] Fix login bug
  → Write API docs
  → Review PR #234

🔔 Other:
  → 2 GitHub PRs need review
  → Package arriving today (Amazon)
```

## Scheduled Briefing

To run automatically each morning, set up a launchd job (macOS) or cron job:

```bash
# Create a briefing script
cat > ~/.claude/briefing.sh << 'SCRIPT'
#!/bin/bash
claude --print "Run my daily briefing using the c-briefing skill. Be concise." \
  | terminal-notifier -title "Morning Briefing" -message "Ready" 2>/dev/null
SCRIPT
chmod +x ~/.claude/briefing.sh

# Schedule with cron (every weekday at 8:00 AM)
(crontab -l 2>/dev/null; echo "0 8 * * 1-5 ~/.claude/briefing.sh") | crontab -

# Or use lunchy-go for launchd (macOS)
lunchy-go install ~/.claude/briefing.plist
```

## Manual Briefing

Just ask Claude: "Give me my daily briefing" or "What's on my plate today?"

## Guidelines

- Read the user's name from SOUL.md or MEMORY.md
- Only include sections for skills that are actually installed
- Keep it concise — no section should exceed 5 items
- Flag urgent items at the top
- Include the date and day of week
