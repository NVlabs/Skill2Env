---
title: Color and Contrast for TV Displays
impact: MEDIUM
tags: color, contrast, hdr, palette, accessibility, tv-design
---

# Color and Contrast for TV Displays

Color systems that work on phones can wash out or over-glow on TV. Distance, panel technology, ambient light, and HDR all affect how colors appear.

## Quick Reference
- Aim for ≥4.5:1 contrast ratio for normal text, ≥7:1 for core UI
- Avoid pure white (#FFFFFF) on pure black (#000000) for entire screens — causes eye fatigue
- Focus indicators need multi-cue: color + border/outline + mild scale
- Test in both SDR and HDR modes; ship a palette that works in both

## Contrast Ratios

| Context | Minimum Ratio | Notes |
|---------|--------------|-------|
| Normal text | ≥ 4.5:1 | WCAG standard |
| Core UI (menus, buttons, captions) | ≥ 7:1 | Holds up on cheap panels and bright rooms |
| Focus indicators | Multi-cue | Color alone fails for color-deficient users |

## Color Palette with Contrast Ratios

| Purpose | Color | vs Black | vs Dark Gray (#1a1a1a) | Use Case |
|---------|-------|----------|----------------------|----------|
| Primary text | #FFFFFF | 21:1 | 17.8:1 | Body text, headings |
| Secondary text | #E5E5E7 | 18.5:1 | 15.7:1 | Labels, metadata |
| Tertiary text | #A1A1AA | 8.6:1 | 7.3:1 | Timestamps, auxiliary |
| Disabled text | #6B7280 | 4.2:1 | 3.6:1 | Inactive elements (sparingly) |
| Primary accent | #007AFF | 8.2:1 | 7.0:1 | Links, CTAs, selected states |
| Focus border | #00D4FF | 11.3:1 | 9.6:1 | Focus indicators, active |
| Success | #34C759 | 9.8:1 | 8.3:1 | Confirmations, positive |
| Warning | #FF9500 | 7.1:1 | 6.0:1 | Warnings, notices |
| Danger | #FF3B30 | 5.9:1 | 5.0:1 | Errors, destructive actions |

> WCAG 1.4.3 requires **4.5:1** for normal text and **3:1** for large text (≥24px, or ≥18.66px bold). The disabled-text row falls below 4.5:1 by design — inactive/disabled UI components are exempt from the contrast minimum. Don't reuse that ratio for active text.

## Ambient Light Adaptation

| Environment | Background | Primary Text | Secondary Text | Accent | Min Contrast |
|-------------|-----------|-------------|----------------|--------|-------------|
| Bright room | #000000 | #FFFFFF | #E5E5E7 | #007AFF | 7:1 |
| Dim room | #1a1a1a | #E5E5E7 | #B3B3B3 | #5AC8FA | 4.5:1 |
| Dark room | #2a2a2a | #D1D1D6 | #8E8E93 | #64D2FF | 3:1 |

> The dark-room 3:1 minimum applies to **large text and UI components** only (WCAG large-text / non-text contrast). Keep body text at 4.5:1 regardless of ambient profile.

## HDR Considerations

HDR displays show brighter whites and deeper blacks — great for video, but UI can over-glow:
- Keep UI whites around **80-90% luminance** — avoid hard #FFFFFF for long-lived text
- Watch highlights (focus glow, selection chips) against HDR content — cap intensity to prevent blooming
- Test both SDR and HDR modes; ship a palette that doesn't collapse in either

## Display Variations

Consider various TV display technologies:
- **LCD, LED, QLED, OLED** render colors differently
- Design for **Standard picture mode** — many TVs offer Cinema/Game/HDR modes
- Use **sRGB color space** for consistency across TVs and mobile
- Darker colors save power on OLED screens

## Technical Considerations

- **Gradients:** Can display as color bands — use high-color-depth gradients
- **Dithering:** Apply noise to reduce color banding — creates illusion of more colors
- **Color-based information:** Never rely solely on color to convey information — add text labels
- **Test on multiple devices** and color spaces — viewing in real life matters

## Related Skills
- [design-typography.md](./design-typography.md) — Text sizing and readability
- [design-10foot.md](./design-10foot.md) — 10-foot experience principles
- [a11y-implementation.md](./a11y-implementation.md) — Accessible color and contrast
