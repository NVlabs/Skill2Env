---
title: Layout Patterns and Common Components
impact: HIGH
tags: layout, cards, swimlanes, safe-zones, overscan, responsive, tv-design
---

# Layout Patterns and Common Components

## Quick Reference
- Use safe zones (5-10% margin) to prevent overscan clipping
- Leave enough spacing for focus indicators to scale or glow without overlapping adjacent cards
- Keep row-to-row and card-to-card focus movement visually predictable
- Test layouts in SDR/HDR and common TV display modes because overscan and color processing vary

## Cards and Content Tiles

- Focus feedback: 3-5% scale increase, glow/drop shadow for depth
- Leave spacing so focus indicators never overlap adjacent cards
- Avoid cramming too much info; dense cards are harder to scan from TV distance

## Rows / Swimlanes

- Left/right within a row, up/down between rows
- Auto-scroll when focus reaches row edge
- Keep row headers readable and announced as landmarks where appropriate
- Keep fewer, more distinct categories rather than many nearly identical rows

## TV Scroll Alignment

On `react-native-tvos`, `ScrollView` has TV-only props for focus-driven snapping:

- Use `snapToAlignment="item"` when each child needs its own snap alignment through `scrollSnapAlign`.
- Use `scrollSnapOffset` when different rows/items need different landing offsets.
- Use `scrollAnimationEnabled={false}` when animated focus scrolling adds input latency or causes overshoot.

Do not combine TV snapping modes with paging assumptions without testing D-pad focus movement; two scroll-positioning systems can fight each other.

## Buttons

- Focused buttons: contrast, outlines, or subtle scaling
- Group related actions ("Play" + "More Info") with consistent spacing
- Short verb labels: "Play", "Retry", "Cancel"

## Overlays

Video controls, pause menus:
- Fade in quickly, fade out after inactivity
- Predictable focus order (left to right)
- Dim content beneath but don't hide completely

## Safe Zones

Many TVs apply overscan — outer 5-10% may get cropped:
- Keep all essential elements (text, logos, buttons) inside 5-10% margin
- Backgrounds and hero images can extend to the edge
- Use gridlines or bounding boxes during development to visualize safe boundaries

## Responsive TV Design

TVs range from 32" to 85" and don't all render pixels identically:
- **Use relative units** (viewport height/width, percentages) not fixed pixels
- **Center critical content** — peripheral areas less reliable
- **Test multiple display modes:** Standard, Cinema, Game, HDR
- Design around 16:9 base grid, ensure it adapts to 21:9 without breaking

## Spacing

- Consistent vertical rhythm between rows (1.5x card height for padding)
- Invisible baselines for text/components keep focus transitions smooth
- TV design prioritizes clarity over space efficiency

## Related Skills
- [design-10foot.md](./design-10foot.md) — 10-foot experience principles
- [design-typography.md](./design-typography.md) — Text sizing and readability
- [perf-lists.md](./perf-lists.md) — List virtualization for performance
