---
name: c-timer
description: Timers, alarms, and pomodoro — set countdowns with native notifications.
tags: [timer, alarm, pomodoro, countdown, reminder]
---

# Timer — Countdowns & Pomodoro

Set timers and get notified via native macOS notifications. Uses `terminal-notifier` and background sleep.

## Commands

```bash
# Simple timer (runs in background)
(sleep 300 && terminal-notifier -title "Timer" -message "5 minutes is up!" -sound default) &

# Timer with custom message
(sleep 1800 && terminal-notifier -title "Timer" -message "Break time!" -sound Glass) &

# Pomodoro (25 min work, 5 min break)
(sleep 1500 && terminal-notifier -title "Pomodoro" -message "Time for a break!" -sound Purr) &

# Quick reminder (with say for audio)
(sleep 60 && say "One minute timer done" && terminal-notifier -title "Timer" -message "1 minute" -sound default) &
```

## Time Conversions

| Duration | Seconds |
|----------|---------|
| 1 minute | 60 |
| 5 minutes | 300 |
| 10 minutes | 600 |
| 15 minutes | 900 |
| 25 minutes | 1500 |
| 30 minutes | 1800 |
| 1 hour | 3600 |

## Notification Sounds

Available: `default`, `Basso`, `Blow`, `Bottle`, `Frog`, `Funk`, `Glass`, `Hero`, `Morse`, `Ping`, `Pop`, `Purr`, `Sosumi`, `Submarine`, `Tink`

## Pomodoro Workflow

When the user asks for pomodoro:
1. Start 25-minute work timer
2. Notify when work session ends
3. Start 5-minute break timer
4. Notify when break ends
5. Repeat (ask user after 4 cycles if they want a 15-min long break)

## Guidelines

- Always confirm the timer was set with the exact duration
- Use `&` to run in background so the terminal stays responsive
- Default sound: `default` for timers, `Purr` for pomodoro
- If `terminal-notifier` is not installed, fall back to `say` command
- For "remind me in X minutes", treat as a timer
- Convert natural language: "half hour" = 1800s, "quarter hour" = 900s
