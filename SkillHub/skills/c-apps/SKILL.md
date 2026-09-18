---
name: c-apps
description: Install, update, and search Mac App Store apps from the command line using mas.
tags: [apps, appstore, macos, install]
---

# Mac App Store (mas)

```bash
# Search for apps
mas search Xcode
mas search "Bear Notes"

# Install by app ID
mas install 497799835    # Xcode

# List installed apps
mas list

# Check for outdated apps
mas outdated

# Upgrade all outdated apps
mas upgrade

# Upgrade specific app
mas upgrade 497799835

# Show app info
mas info 497799835

# Open app page in App Store
mas open 497799835
```

## Guidelines

- User must be signed into the Mac App Store
- On macOS 15+, install/upgrade requires admin password
- Use `mas search` to find app IDs before installing
- `mas upgrade` updates all apps — confirm with user first
- Free and paid apps both work (paid requires prior purchase)
