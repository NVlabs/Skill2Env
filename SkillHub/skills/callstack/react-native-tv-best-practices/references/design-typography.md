---
title: Typography for TV Displays
impact: HIGH
tags: typography, fonts, text-size, readability, contrast, tv-design
---

# Typography for TV Displays

Typography that works on phones fails on TV. Distance, panel tech, ambient light, and OS rendering push designs toward bigger type, clearer spacing, and higher contrast.

## Quick Reference
- Start TV body text around 24px and validate from viewing distance
- Avoid ultra-light/ultra-thin weights — they shimmer on LCDs, bloom on OLEDs

## Minimum Font Sizes

Use these as starting points, then validate on the target TV size and distance:

| Text Style | TV Starting Point | Use Case |
|-----------|-------------------|----------|
| Body | 24px | Descriptions, paragraphs |
| Caption | 20px | Metadata, labels, tags |
| Button | 22px | Interactive elements, CTAs |
| Heading | 32px | Section titles, categories |
| Title | 48px | Page titles, hero text |
| Display | 64px | Large promotional text |

```jsx
const tvTypography = StyleSheet.create({
  body:    { fontSize: 24, lineHeight: 32, fontWeight: '400' },
  button:  { fontSize: 22, lineHeight: 28, fontWeight: '600' },
  caption: { fontSize: 20, lineHeight: 26, fontWeight: '400' },
  heading: { fontSize: 32, lineHeight: 40, fontWeight: '600' },
  title:   { fontSize: 48, lineHeight: 56, fontWeight: '700' },
});
```

## Line Spacing and Letter Spacing

| Context | Line Height | Letter Spacing | Best For |
|---------|-------------|----------------|----------|
| Content (paragraphs) | 1.4x | 0.4px | Long-form reading |
| Navigation (menus) | 1.2x | 0.5px | Menu items, scanning |
| Display (large text) | 1.15x | -0.4px to -0.8px | Hero text, titles |

Negative tracking for large titles: huge sizes amplify default spacing; tightening avoids airy gaps.

## Text Rendering on TV

TVs expose edge cases with subpixel rendering:
- **Text over images:** Add subtle text shadow to separate from backgrounds
  ```jsx
  const readableOnImage = {
    color: '#FFF',
    textShadowColor: 'rgba(0,0,0,0.35)',
    textShadowOffset: { width: 0, height: 1 },
    textShadowRadius: 2,
  };
  ```
- **Subtitles/over-video:** Combine shadow + stroke at low opacity (not heavy blur)
- **Safe zone:** Keep text inside safe zone — overscan clips labels at edges
- **Tile titles:** `numberOfLines={2}` + `ellipsizeMode="tail"` — avoid wrapping issues
- **Long localized titles:** Gentle marquee only on focus, never by default

## Related Skills
- [design-10foot.md](./design-10foot.md) — 10-foot experience design principles
- [design-color.md](./design-color.md) — Color and contrast guidelines
- [design-layout.md](./design-layout.md) — Layout and spacing patterns
