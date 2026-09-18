---
title: Performance Overview for TV
impact: HIGH
tags: performance, device-tiers, kpis, startup, hardware, tv
---

# Performance Overview for TV

TV hardware is significantly weaker than modern phones. A 65" TV is often closer to a budget Android phone in CPU/GPU terms — while also decoding 4K video.

## Quick Reference
- Set performance budgets from the weakest supported TV device
- Keep one low-end streaming stick or TV in the regular test matrix
- Measure input latency, FPS during focus movement, memory, startup, and time to playback
- Treat video playback as part of the performance budget; UI work competes with decode and buffers

## Why Performance Is Unforgiving on TV

- **CPU/GPU budgets are lower** — every unnecessary render competes with video decoding
- **Memory: 1-2 GB** — shared between OS, video buffer, and your app
- **Users notice everything** — 300ms input delay = "the app froze"; 45 FPS = visible stutter
- **TV chipsets are designed for video playback**, not high-performance UI rendering

## Device Tiers — Progressive Enhancement

### Low-End (Fire TV Stick Gen 1)
Keep it lean. Drop fancy gradients, heavy shadows, long transitions. Stick to snappy focus highlights, lightweight lists, instant feedback. Responsiveness beats visual flair.

### Mid-Range (Samsung Smart TV mid-tier)
Layer in some polish. Quick scale/fade here and there. Still performance-first.

### High-End (Apple TV 4K, Nvidia Shield)
Add visual polish: parallax banners, chained animations, cinematic transitions.

**Implementation:**
- Detect hardware class at runtime (device model, RAM, OS version)
- Maintain feature flags for performance tiers (basic, standard, enhanced)
- Shared baseline layout + conditional animations/effects per tier
- Test on real devices at each tier

## KPIs to Track

| Metric | Low-End Target | Mid-End | High-End |
|--------|---------------|---------|----------|
| Cold start time | <5s | <4s | <4s |
| Time to playback | <10s | <7s | <7s |
| Time to first meaningful paint | <3s | <2s | <1.5s |
| FPS during navigation | 60 | 60 | 60 |

## TV-Specific Performance Checks

1. **Remote input latency** — Measure the delay from D-pad press to visible focus movement. Keyboard input and simulator clicks hide this class of regression.
2. **Playback startup** — Track manifest request, DRM license request, first decoded frame, and controls-ready time separately.
3. **Memory with video active** — Measure carousels and overlays while a video surface is mounted; image caches and video buffers share the same low memory budget.
4. **Focus navigation FPS** — Measure row-to-row and card-to-card movement, not only inertial scrolling.
5. **Device tier fallback** — Disable heavy shadows, gradients, parallax, and long transitions on low-end devices before reducing content density.

## Automating Performance Measurements

Manual testing doesn't scale across TV platforms:

```jsx
import { PerformanceObserver, performance } from 'react-native-performance';
performance.mark('app_start');
AppRegistry.registerComponent(appName, () => {
  performance.mark('app_registered');
  return App;
});
```

- Collect timestamps via automated tests on real devices
- Push metrics to Grafana/Datadog for trend tracking
- Fail CI if metrics regress beyond thresholds

## Related Skills
- [perf-animations.md](./perf-animations.md) — Animation performance
- [perf-lists.md](./perf-lists.md) — List virtualization
- [perf-network.md](./perf-network.md) — Network optimization
- [perf-memory.md](./perf-memory.md) — Memory management
- [focus-performance.md](./focus-performance.md) — Focus-related performance
