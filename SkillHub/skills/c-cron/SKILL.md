---
name: c-cron
description: Manage cron jobs and macOS launchctl services — schedule recurring tasks, start/stop services using lunchy-go.
tags: [cron, scheduling, launchctl, automation]
---

# Scheduling & Cron

## lunchy-go (launchctl wrapper)

Friendly wrapper around macOS `launchctl`:

```bash
# List all services (pattern match)
lunchy-go ls
lunchy-go ls redis

# Start a service
lunchy-go start com.example.service
lunchy-go start redis    # pattern match

# Stop a service
lunchy-go stop redis

# Restart a service
lunchy-go restart redis

# Show service status
lunchy-go status redis
```

## crontab (built-in)

Standard Unix cron scheduler:

```bash
# List current cron jobs
crontab -l

# Edit cron jobs (opens editor)
crontab -e

# Cron syntax: MIN HOUR DOM MON DOW command
# Every day at 9am:
# 0 9 * * * /path/to/script.sh
# Every 5 minutes:
# */5 * * * * /path/to/script.sh
# Weekdays at 8:30am:
# 30 8 * * 1-5 /path/to/script.sh
```

## Guidelines

- Prefer lunchy-go for macOS services (launchd plists)
- Use crontab for simple recurring commands
- Always use full paths in cron jobs
- Redirect output to log files: `command >> /tmp/cron.log 2>&1`
- Test commands manually before scheduling them
