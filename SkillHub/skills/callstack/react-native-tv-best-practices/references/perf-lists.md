---
title: "Lists and Grids: Virtualization Is Mandatory"
impact: CRITICAL
tags: lists, grids, virtualization, flashlist, flatlist, tv
---

# Lists and Grids: Virtualization Is Mandatory

TV UIs are grids of lists inside lists. Home screens have 10-15 rows with 10-20 items each. Without virtualization, your app will be unusable on TV hardware.

## Quick Reference
- **Always virtualize large feeds** — Use FlatList/VirtualizedList, FlashList, or RecyclerListView instead of mounting every poster
- Keep poster rows lightweight; heavy shadows/gradients compound across dozens of focused cards
- Preload only the next likely row/screen; aggressive poster prefetch can trigger TV memory kills
- On `react-native-tvos`, use `additionalRenderRegions` for critical ranges that must stay mounted during focus navigation
- Render hero row outside the virtualized list

## Why It's Worse on TV

- **Lower RAM:** Fewer off-screen items can stay in memory
- **No GPU tile caching:** On older Tizen/webOS, scrolling back = re-render from scratch
- **Focus-driven navigation:** Users whip through rows faster than mobile swipes
- **Large assets:** Movie posters, 4K stills are heavier than mobile thumbnails

## Bad: Non-Virtualized Grid
```jsx
<ScrollView>
  {rows.map((row) => (
    <Row key={row.id} data={row.items} />
  ))}
</ScrollView>
```
Every item in every row exists in memory all the time.

## Better: Virtualized with FlashList
```jsx
<FlashList
  data={movies}
  renderItem={renderPoster}
/>
```
Only a "window" of items exists in memory at any time.

## React Native TV VirtualizedList

`react-native-tvos` wraps `VirtualizedList` contents with TV focus helpers and adds `additionalRenderRegions`:

```jsx
<FlatList
  data={rows}
  renderItem={renderRow}
  additionalRenderRegions={[{ first: 0, last: 1 }]}
/>
```

Use `additionalRenderRegions` sparingly for critical ranges that must not blank out during D-pad navigation, such as the current row plus an adjacent row. These regions are still a memory tradeoff.

## TV-Specific Checks

1. **Virtualize nested rows** — TV home screens often have many horizontal rows inside a vertical feed. Avoid keeping every poster mounted.

2. **Preload conservatively** — Prefetch images for the next likely screen or row, then verify memory while video is mounted.

3. **Keep focus work local** — Moving focus across one row should not re-render unrelated rows.

4. **Measure fast remote repeats** — Users can hold a direction and traverse rows faster than mobile swipe assumptions.

5. **Defer rich metadata** — Load ratings, trailer previews, and entitlement badges after the row is visible or focused.

6. **Hero row outside list** — Render the hero row outside the virtualized list to avoid recalculating its layout during row scroll.

## Platform Quirks

- **Tizen:** Prefetching too aggressively triggers out-of-memory reloads. Keep cache conservative.
- **webOS:** Scrolling performance drops if images aren't decoded yet — preload 1-2 screens ahead.
- **Apple TV:** Generally smoothest rendering, but older models still choke on giant grids.

## Related Skills
- [perf-overview.md](./perf-overview.md) — Overall performance strategy
- [perf-memory.md](./perf-memory.md) — Image and memory optimization
- [design-layout.md](./design-layout.md) — Row/card layout patterns
