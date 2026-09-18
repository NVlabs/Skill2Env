---
name: c-lockin
description: Lock In Mode — orchestrate distraction blocking, environment setup, and session tracking.
tags: [lockin, focus, productivity, deep-work, pomodoro, distraction-blocking]
---

## Behavior

You run lock-in sessions using generated shell scripts — fast, one command.
Be FAST. Say one short line like "Locking you in for 90 min" then run TWO commands max. Don't narrate steps. Only speak again when done ("Locked in until HH:MM") or if something fails.

## Starting a Session

When the user says "lock in", "focus", "deep work", etc:

1. Read `~/.config/openpaw/lockin.json`. If missing → suggest `openpaw lockin setup`
2. Check `~/.config/openpaw/lockin-session.json` — if `endsAt` is in the future, session is already active. Tell the user.
3. If config has `askEachTime` sites or apps, ask the user briefly which to include this session
4. Calculate `endsAt` = now + duration minutes (ISO 8601 format, e.g. `2026-03-03T16:30:00.000Z`)
5. Say ONE short line like "Locking you in for 90 min"
6. Generate scripts + run:

```bash
openpaw lockin gen-scripts --ends "ENDS_AT_ISO8601" --extra-sites "site1,site2" --extra-apps "App1,App2"
```

Omit `--extra-sites` and `--extra-apps` if none were chosen from askEachTime.

Then immediately run:

```bash
bash /tmp/lockin-start.sh
```

7. Say "Locked in until HH:MM"

That's it — TWO bash commands to start a session.

## Ending a Session

When the user says "stop", "end session", "I'm done":

1. Read `~/.config/openpaw/lockin-session.json` to get session data
2. Run:

```bash
bash /tmp/lockin-end.sh
```

3. Read the output for git stats
4. If `obsidianLog` is true in config: `obsidian-cli append daily "## Lock In Session\n- Duration: X min\n- Commits: N\n..."`
5. Give a brief warm summary: duration, commits + messages, lines changed, encouraging note referencing SOUL.md personality

## Reconfigure

```bash
openpaw lockin setup
```

## Guidelines

- Be FAST — one line to start, two commands, one line when done
- Never explain or narrate each step — just do it
- If something fails, mention it briefly and move on
- Only start when the user explicitly asks
- Reference SOUL.md for personality in summaries
