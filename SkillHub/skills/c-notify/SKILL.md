---
name: c-notify
description: Send native macOS notification center alerts from the command line using terminal-notifier.
tags: [notifications, alerts, macos]
---

# Notifications (terminal-notifier)

```bash
# Simple notification
terminal-notifier -title "OpenPaw" -message "Task complete!"

# With subtitle and sound
terminal-notifier -title "Build" -subtitle "Project X" -message "Done!" -sound default

# Open URL when clicked
terminal-notifier -title "PR Merged" -message "Click to view" -open "https://github.com/..."

# Activate app when clicked
terminal-notifier -title "Music" -message "Now playing" -activate "com.spotify.client"

# Group notifications (replaces previous in same group)
terminal-notifier -title "Progress" -message "50%" -group "build"
terminal-notifier -title "Progress" -message "100%" -group "build"

# Remove a notification group
terminal-notifier -remove "build"

# Custom app icon
terminal-notifier -title "Alert" -message "Hello" -appIcon /path/to/icon.png
```

## Guidelines

- Use notifications to alert the user when long tasks complete
- Group related notifications so they don't spam
- Add `-sound default` for important alerts
- Use `-open URL` to make notifications actionable
- Keep messages short — notifications truncate long text
