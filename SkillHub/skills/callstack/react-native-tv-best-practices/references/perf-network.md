---
title: Network Performance on TV
impact: HIGH
tags: network, prefetching, caching, optimistic-ui, payloads, tv
---

# Network Performance on TV

On TV, there's no "loading spinner safety net." People expect content to instantly fill the screen. If nothing happens after a remote press, they'll assume the app froze — and press again (duplicate requests).

## Quick Reference
- Show something within 200ms of navigation — even a blurred poster or placeholder
- Prefetch the next likely screen while current one is stable
- Never block navigation/focus on network responses
- Debounce input during network stalls to prevent duplicate requests

## Why It's Worse on TV

- **Wi-Fi is often bad:** TVs in far corners, running on 2.4 GHz with packet loss/jitter
- **Platform timeouts:** Tizen aggressively kills "stuck" requests
- **Large payloads:** Home screen = multiple JSON payloads + dozens of poster images
- **No background fetch:** TVs don't run your app in background between sessions

## Problem: Blocking Navigation

**Bad:**
```jsx
const onRowFocus = async (rowId) => {
  const details = await fetchRowDetails(rowId); // Blocks focus
  setDetails(details);
};
```
User presses down, nothing highlights until network returns.

**Better (optimistic UI):**
```jsx
const onRowFocus = (rowId) => {
  highlightRow(rowId); // Instant visual feedback
  fetchRowDetails(rowId).then(setDetails);
};
```

## TV-Specific Checks

1. **Prefetch where it matters** — Preload the next likely screen or row, then verify memory on low-end devices.

2. **Use placeholders instead of blocking** — Focus movement should remain instant even when row metadata is stale or still loading.

3. **Prioritize visible content** — Load the hero/current row first; defer secondary rows and rich metadata.

4. **Handle retries gracefully** — Remote presses during stalls should not spam duplicate requests.

5. **Keep caches memory-aware** — Cached posters plus JSON plus video buffers can create GC stutter on Fire TV and smart TVs.

## Platform Quirks

- **Tizen:** Requests >5 seconds can be killed without warning. Set shorter timeouts + retry logic.
- **webOS:** Some models cache aggressively in firmware — add version param to URLs.
- **Fire TV:** Prefetching too aggressively on slow Wi-Fi spikes memory (cached images + JSON) → GC stutter.
- **Apple TV:** Fast on wired Ethernet but test on Wi-Fi too.

> Optimize first paint time, not just throughput. Show something within 200ms of navigation.

## Related Skills
- [perf-overview.md](./perf-overview.md) — Overall performance strategy
- [perf-memory.md](./perf-memory.md) — Memory impact of caching
- [perf-lists.md](./perf-lists.md) — Virtualized list rendering
