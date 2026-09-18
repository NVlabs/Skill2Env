---
name: c-location
description: Search Apple Maps, find nearby places, and get directions using the `goplaces` CLI. Supports keyword searches, category filters (restaurants, coffee, gas), and turn-by-turn directions by driving, walking, or transit.
tags: [maps, location, apple-maps, directions, places, search]
---

## What This Skill Does

Queries Apple Maps via the `goplaces` CLI to search for places, find businesses nearby, and get directions between locations.

## CLI Tool: `goplaces`

### Common Commands

```bash
# Search for a place by name or keyword
goplaces search "coffee shops near downtown Austin"

# Find nearby places by category
goplaces nearby "pizza"
goplaces nearby "gas station"

# Get directions between two locations
goplaces directions "Austin TX" "San Antonio TX"
goplaces directions --mode walking "Zilker Park" "South Congress Ave"

# Get details about a specific place
goplaces details "Barton Springs Pool, Austin"
```

### Transport Modes

- `--mode driving` (default)
- `--mode walking`
- `--mode transit`

## Usage Guidelines

1. Use natural language for location queries — `goplaces` handles geocoding automatically.
2. For "nearby" searches, the current device location is used unless a starting point is specified.
3. When providing directions, confirm origin and destination with the user if ambiguous.
4. Present results as a numbered list when multiple places are returned.

## Notes

- Requires macOS with location services enabled for proximity searches.
- Results are sourced from Apple Maps — coverage quality varies by region.
