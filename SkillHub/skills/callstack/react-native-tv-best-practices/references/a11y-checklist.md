---
title: Accessibility Checklist for TV Apps
impact: MEDIUM
tags: accessibility, checklist, screen-reader, captions, focus, tv
---

# Accessibility Checklist for TV Apps

Pre-launch checklist for remote-only navigation, TV screen readers, captions, and focus-visible UI.

## 1. Navigation & Focus Management
- [ ] All interactive elements reachable via D-pad or remote
- [ ] Focus moves logically (left→right, top→bottom)
- [ ] Focus is visible and clearly indicated (highlight or border)
- [ ] No "focus traps" — areas where focus gets stuck or lost
- [ ] Back button behaves consistently and predictably
- [ ] Menus and modals trap focus while active and restore on close

## 2. Screen Reader & VoiceOver Support
- [ ] All interactive elements have clear, descriptive labels ("Play Button", "Episode 2: Stranger Things")
- [ ] Dynamic content changes announced via `accessibilityLiveRegion`
- [ ] Screen reader correctly reads button states (selected, disabled)
- [ ] Non-text elements (icons, images) have appropriate alt text/labels
- [ ] Dialogs ("Are you still watching?") announced and navigable via screen reader

## 3. Visual Design & Contrast
- [ ] Text size large enough for TV viewing (>18px minimum)
- [ ] Text and interactive elements ≥4.5:1 contrast ratio against background
- [ ] Focus indicators are high contrast and visible from distance
- [ ] No overlaid or animated text on busy video backgrounds
- [ ] No flashing or strobing elements (seizure risk)

## 4. Audio & Captions
- [ ] Captions/subtitles available for all video content
- [ ] Captions customizable: size, color, background
- [ ] Audio descriptions available and easy to enable/disable
- [ ] Action feedback ("Added to Watchlist") provided visually AND audibly
- [ ] Autoplay previews can be paused or disabled by user

## 5. Search & Content Discovery
- [ ] On-screen keyboard fully navigable with remote/D-pad
- [ ] Search suggestions readable and selectable via focus
- [ ] Search results announced to screen readers or at least navigable
- [ ] Search input has visible label or hint ("Search for shows or movies")

## 6. Dynamic Content & Live Updates
- [ ] New content in carousels/rows/lists is announced or focusable
- [ ] Lazy-loaded content doesn't reset or lose focus state
- [ ] Infinite scroll has clear separators/headings between content types
- [ ] Row headers ("Recommended", "Trending Now") announced as landmarks

## 7. Interactive Features (Like, Rate, Watchlist)
- [ ] Like/dislike/watchlist buttons focusable and labeled clearly
- [ ] Button states (liked, saved) announced to screen readers
- [ ] Confirmation messages both visual and accessible
- [ ] All icons (heart, star, thumb) have text equivalents

## 8. Testing & Platform-Specific
- [ ] Agent smoke-tested after loading the `agent-device` skill and reading `agent-device help workflow`; verified exposed labels, roles, states, focus, and modal focus behavior
- [ ] Manually tested spoken output on platform screen readers (TalkBack, VoiceOver, VoiceView) before release
- [ ] Reviewed against platform accessibility guidelines (tvOS HIG, Android TV UI)

## 9. Settings & User Control
- [ ] Accessibility settings (captions, audio description, high contrast) easily accessible
- [ ] Autoplay previews and audio can be disabled
- [ ] Users can control text size, color themes, contrast where supported
- [ ] App respects system-wide accessibility settings

## 10. Avoid These Common Mistakes
- [ ] No unlabeled buttons or icons ("button1")
- [ ] No focus on non-interactive elements (static labels)
- [ ] No inaccessible custom components (carousels without keyboard support)
- [ ] No functionality requiring complex remote combos or gestures only

## Testing Tools

| Tool | Type | Notes |
|------|------|-------|
| agent-device | Agent-run | Load the `agent-device` skill and read `agent-device help workflow`, then inspect accessibility tree, focused elements, labels, roles, states, and modal focus behavior |
| TalkBack | Manual | Android TV, Fire TV |
| VoiceOver | Manual | Apple TV |
| React Native Testing Library | Integration | Test accessibility props/labels |
| Accessibility Inspector | Manual | Xcode (tvOS) |

## Related Skills
- [a11y-overview.md](./a11y-overview.md) — Accessibility fundamentals
- [a11y-implementation.md](./a11y-implementation.md) — Implementation details
- [design-color.md](./design-color.md) — Color contrast guidelines
