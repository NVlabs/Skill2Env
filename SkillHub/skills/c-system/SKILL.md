---
name: c-system
description: macOS Swiss Army Knife — control volume, wifi, battery, dock, display, trash, firewall, screensaver, shutdown, and more via m-cli.
tags: [macos, system, volume, wifi, battery]
---

# System Control (m-cli)

Swiss Army Knife for macOS. Run `m` followed by a category:

```bash
# Volume
m volume 50          # Set volume to 50%
m volume mute        # Mute
m volume unmute      # Unmute

# WiFi
m wifi status        # Show WiFi status
m wifi scan          # Scan available networks
m wifi connect SSID PASSWORD
m wifi off           # Turn WiFi off
m wifi on            # Turn WiFi on

# Battery
m battery status     # Battery percentage and state
m battery cycle      # Battery cycle count

# Display
m display status     # Display info
m display up         # Increase brightness
m display down       # Decrease brightness

# Dock
m dock addblank      # Add blank space to dock
m dock autohide YES  # Enable auto-hide
m dock magnification YES

# Trash
m trash clean        # Empty trash
m trash status       # Show trash size

# Bluetooth
m bluetooth status
m bluetooth on
m bluetooth off

# Network
m network ls         # List network interfaces
m network location   # Show current location

# Power
m nosleep           # Prevent sleep (until Ctrl+C)
m restart           # Restart Mac
m shutdown          # Shut down Mac
m screensaver       # Start screensaver
m lock              # Lock screen

# Finder
m finder showpath YES    # Show full path in title
m finder showhidden YES  # Show hidden files

# Firewall
m firewall status
m firewall enable
```

## Guidelines

- `m` requires no auth for most commands; some need sudo
- Always confirm before `m restart`, `m shutdown`, or `m trash clean`
- Use `m wifi` instead of raw `networksetup` commands
- Use `m volume` instead of `osascript` for volume control
