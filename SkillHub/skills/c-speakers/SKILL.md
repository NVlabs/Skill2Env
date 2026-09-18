---
name: c-speakers
description: Control Sonos speakers using the `sonos` CLI (sonoscli). Play, pause, adjust volume, manage groups, and play favorites across rooms and speaker zones.
tags: [sonos, speakers, audio, smart-home, music, sonoscli]
---

## What This Skill Does

Enables Claude to control Sonos speakers — playback, volume, grouping, and favorites — via the `sonos` CLI.

## Available CLI Tool: `sonos`

### Common Commands

```bash
# List all Sonos rooms/players
sonos rooms

# Play and pause
sonos play --room "Living Room"
sonos pause --room "Living Room"

# Skip tracks
sonos next --room "Living Room"
sonos previous --room "Living Room"

# Set volume (0-100)
sonos volume 50 --room "Living Room"

# Adjust volume relative
sonos volume +10 --room "Kitchen"
sonos volume -5 --room "Kitchen"

# Play a favorite (from Sonos app favorites)
sonos favorite "Morning Jazz" --room "Bedroom"

# List favorites
sonos favorites

# Group rooms together
sonos group "Kitchen" --with "Living Room"

# Ungroup a room
sonos ungroup "Kitchen"

# Show now playing info
sonos status --room "Living Room"
```

## Usage Guidelines

- Always specify `--room` to target the correct speaker
- Use `sonos rooms` to discover available rooms if unsure of names
- Grouping joins a room into the specified room's group

## Notes

- Requires `sonos` CLI (sonoscli) installed and Sonos system on local network
- Favorites must be pre-configured in the Sonos app
