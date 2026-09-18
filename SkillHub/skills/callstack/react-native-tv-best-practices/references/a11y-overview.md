---
title: Accessibility on TV Overview
impact: MEDIUM
tags: accessibility, a11y, screen-readers, focus, d-pad, talkback, voiceover
---

# Accessibility on TV — Overview

What's different about accessibility on TV versus mobile/web — the deltas you can't infer from general React Native a11y knowledge. For prop usage and patterns see [a11y-implementation.md](./a11y-implementation.md); for the audit list see [a11y-checklist.md](./a11y-checklist.md). WCAG/POUR and the legal baseline (ADA, Section 508, EN 301 549) apply to TV exactly as to mobile/web — treat a11y as a requirement, not a nice-to-have.

## Quick Reference
- TV accessibility differs from mobile/web on three axes: D-pad navigation, focus-driven UI, and viewing distance
- Focus management *is* the primary a11y surface on TV — there is no touch fallback
- Screen readers: TalkBack (Android TV), VoiceOver (Apple TV), VoiceView (Fire TV)
- Behavior is NOT consistent across platforms — test on each device, not just one

## Why TV Accessibility Is Unique

| Feature | TV | Mobile | Web |
|---------|-----|--------|-----|
| Input | Remote / voice | Touch + assistive tech | Keyboard, mouse, screen readers |
| Focus Management | Essential (D-pad) | Implicit with touch | Tab focus |
| Screen Reader | Limited/inconsistent | VoiceOver, TalkBack | JAWS, NVDA, VoiceOver |
| Text Scaling | Limited; fixed layout | Dynamic type | CSS zoom |
| Contrast | Critical (viewing distance) | Important | Important |
| Gestures | Not applicable | Swipe, pinch | Keyboard, mouse |

## Platform Screen Readers

| Platform | Tool | Activation |
|----------|------|------------|
| Fire TV | VoiceView | Accessibility settings |
| Apple TV | VoiceOver | Menu + Siri Remote, or Settings |
| Android TV | TalkBack | Accessibility shortcut or dev settings |

### Platform Differences

- **Fire TV (VoiceView):** Similar to TalkBack but not all props honored on older models. Extra verbose by default.
- **Apple TV (VoiceOver):** Focus can jump non-linearly. `accessibilityHint` read immediately after label. Role mapping consistent with iOS.
- **Android TV (TalkBack):** Linear D-pad navigation. `accessibilityHint` sometimes skipped unless `accessible={true}` is explicit.

These are the core React Native accessibility props (`accessible`, `accessibilityLabel`, `accessibilityRole`, `accessibilityState`, `accessibilityLiveRegion`, `accessibilityViewIsModal`) you'll use on TV, but support varies by platform — see [a11y-implementation.md](./a11y-implementation.md) for TV-specific usage and the platform quirks above for where they diverge.

## Related Skills
- [a11y-implementation.md](./a11y-implementation.md) — Detailed implementation guide
- [a11y-checklist.md](./a11y-checklist.md) — Pre-launch checklist
- [design-color.md](./design-color.md) — Contrast requirements
