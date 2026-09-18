---
title: The 10-Foot Experience
impact: HIGH
tags: 10-foot, tv-design, remote, feedback, shared-screen
---

# The 10-Foot Experience

TV UIs are viewed from ~3 m (10 ft) with a D-pad remote, not 30 cm with a touchscreen. This file covers the TV-specific design concerns that follow from that distance and input model. For the concrete numbers, defer to the focused references:

- Text sizing for distance → [design-typography.md](./design-typography.md)
- Safe zones, spacing, grids → [design-layout.md](./design-layout.md)
- Contrast and color on TV panels → [design-color.md](./design-color.md)
- Focus movement and modal focus traps → [focus-management.md](./focus-management.md)
- Directional navigation rules → [nav-directional.md](./nav-directional.md)

## Quick Reference
- Design for legibility at 3 m; verify by testing from a couch with a remote, not at a desk with a keyboard.
- Acknowledge every remote press with a visual cue within ~100 ms.
- Keep focus/transition animations under 200 ms so they never delay the next input.
- Treat the TV as a shared device — don't expose personal data by default.

## Input Latency and Feedback

TV hardware and remotes add ~100–200 ms between a button press and the on-screen response. Mask that latency, don't add to it:

- Show a focus cue (highlight, ~3–5% scale, or border) within ~100 ms of every press.
- Keep focus and transition animations under 200 ms; an animation that outlasts the next press is too long.
- Use motion only to reinforce direction or highlight focus changes — never decorative sequences that block input.

## Shared Screen Considerations

TVs are shared among family, roommates, and guests — design for that:

- Don't display account email, payment details, or other personal data unless the action requires it.
- Make profile switching reachable within 2 D-pad presses from the home screen.
- Show a confirmation step for voice-entered text before submitting it.
- Auto-dismiss subtitles, overlays, and menus on a timer once they've served their purpose.

## Couch Test Checklist

Test each completed screen from the intended viewing position (couch, remote, ~3 m). Each step is pass/fail:

1. Reach the first **Play** action from the home screen in ≤3 D-pad presses.
2. Return to the starting screen using only the **Back** button.
3. After every directional press, focus lands on a visible element (no off-screen or lost focus).
4. Every press produces a visible cue within ~100 ms.
5. Screen remains legible with room lights both on and off.

If a step fails, reduce the number of focusable elements or realign the layout before adding manual `nextFocus*` overrides.

## Related Skills
- [design-layout.md](./design-layout.md) — Layout patterns, safe zones, component design
- [design-typography.md](./design-typography.md) — Text sizing for distance
- [design-color.md](./design-color.md) — Contrast and color for TV displays
- [focus-management.md](./focus-management.md) — Focus engine, traps, restoration
