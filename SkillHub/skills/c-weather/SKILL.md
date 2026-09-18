---
name: c-weather
description: Weather forecasts and conditions — current, hourly, multi-day. No API key needed.
tags: [weather, forecast, temperature, assistant]
---

# Weather — Forecasts & Conditions

Get weather information using `curl` and wttr.in. No API key required, no tool to install.

## Commands

```bash
# Current weather (auto-detects location)
curl -s "wttr.in?format=3"

# Detailed current conditions
curl -s "wttr.in?format=%l:+%c+%t+%h+%w+%p"

# Full forecast (today + 2 days)
curl -s "wttr.in"

# Specific city
curl -s "wttr.in/London"
curl -s "wttr.in/New+York"
curl -s "wttr.in/Tokyo"

# Compact one-line
curl -s "wttr.in/Paris?format=%l:+%c+%t+(feels+like+%f)+%h+humidity+%w+wind"

# Today only
curl -s "wttr.in/Berlin?1"

# JSON output for parsing
curl -s "wttr.in/London?format=j1"

# Moon phase
curl -s "wttr.in/Moon"
```

## Format Codes

| Code | Meaning |
|------|---------|
| `%c` | Weather icon |
| `%t` | Temperature |
| `%f` | Feels like |
| `%h` | Humidity |
| `%w` | Wind |
| `%p` | Precipitation |
| `%l` | Location |
| `%S` | Sunrise |
| `%s` | Sunset |

## Guidelines

- Default to the user's location (check memory/SOUL.md for city)
- Use compact format (`format=3`) for quick checks
- Use full output for detailed forecasts
- If the user asks about weather, always provide temperature and conditions
- Mention "feels like" temperature when it differs significantly
