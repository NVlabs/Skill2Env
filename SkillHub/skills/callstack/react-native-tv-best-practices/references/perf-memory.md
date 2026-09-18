---
title: Memory Management on TV
impact: HIGH
tags: memory, ram, image-optimization, garbage-collection, tv-performance
---

# Memory Management on TV

On TVs, you're sharing RAM with the OS, video decoder, DRM, audio buffers, and even the live TV tuner. Your UI runs in the leftovers.

## Quick Reference
- Many devices have 1-1.5 GB total — your app might only get 300-500 MB
- 4K video streams eat 100-200 MB just for decoded frames
- Poster/backdrop caches are the biggest UI-side memory lever
- Smart TVs aggressively reclaim memory from your app

## Symptoms of Memory Pressure

- Sudden GC spikes (frame drops during scrolling)
- Images unloading from cache and re-downloading mid-session
- Crashes or forced restarts (Tizen and webOS are notorious)

## Image Memory Optimization

**Bad:**
```jsx
<Image source={{ uri: posterUrl }} />
```
Without cache control, changing `posterUrl` holds multiple decoded bitmaps until GC runs.

**Better:**
```jsx
<Image
  source={{ uri: posterUrl, cache: 'force-cache' }}
  resizeMode="cover"
/>
```
Or use `react-native-fast-image` for cache control.

## List Item Memory

Even with virtualization, if row components keep large objects in state (full metadata blobs), you're holding memory hostage.

**Better:** Store only IDs in list item state, fetch full details on demand.

## TV-Specific Checks

1. **Match asset size to display size** — A decoded 4K backdrop for a small thumbnail wastes the same memory as a visible full-screen asset.

2. **Measure with video mounted** — UI memory that looks fine without playback can fail once decoded frames and DRM buffers exist.

3. **Keep cache pressure visible** — Watch for poster eviction/re-download loops during fast row navigation.

4. **Avoid large list item state** — Keep IDs in rows; fetch full metadata on demand.

5. **Use native profiling tools:**
   - Android TV/Fire TV: Android Studio Profiler → Memory tab
   - Apple TV: Xcode Instruments → Allocations + Leaks
   - Tizen/webOS: Emulator memory usage overlays

## Platform Quirks

- **Low-end Fire TV:** ~0.5-1 GB RAM total. Every extra library adds startup time.
- **Tizen/webOS:** Aggressive OS memory reclaim — your app can be killed without warning.
- **Apple TV 4K:** More generous RAM (4 GB) but don't assume you can skip optimization.

## Related Skills
- [perf-overview.md](./perf-overview.md) — Overall performance strategy
- [perf-lists.md](./perf-lists.md) — Virtualized lists reduce memory
- [perf-network.md](./perf-network.md) — Caching and payload optimization
