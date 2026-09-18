---
title: Accessibility Implementation in React Native TV
impact: HIGH
tags: accessibility, screen-reader, focus, voiceover, talkback, tv
---

# Accessibility Implementation in React Native TV

## Quick Reference
- For agent-run checks, load the `agent-device` skill first, then read `agent-device help workflow`
- Use `agent-device` accessibility-tree evidence to inspect exposed labels, roles, states, focus, and modal behavior
- Use manual screen-reader testing only for spoken-output timing, audio behavior, and platform quirks that automation cannot prove
- Do not put `accessible={true}` high in a modal/body tree; it collapses focusable children into one item
- Prefer `TVFocusGuideView` for shared focus paths; use `nextFocus*` only as a targeted override
- Await `AccessibilityInfo.isScreenReaderEnabled()` before muting autoplay or changing announcements
- Pair visual-only remote feedback with an accessibility announcement when state changes

## Agent-Run Accessibility Smoke

Before planning or running device automation, load the `agent-device` skill and follow its setup/help flow. Do not duplicate command recipes here; use the installed `agent-device` help for current command shapes and platform limits.

An AI agent should not claim it heard VoiceOver, TalkBack, or VoiceView. Instead, use `agent-device` to inspect what the app exposes to platform accessibility. Check the accessibility-tree evidence for:

- Interactive controls expose useful labels, roles, enabled/disabled state, and selected/checked state
- The currently focused element is the expected remote target after each D-pad press
- Modal opening moves focus inside the modal and hides or de-prioritizes background controls
- Closing a modal restores focus to the invoking control or another predictable target
- Dynamic state changes expose updated labels/state or a live-region/announcement path

Escalate to manual screen-reader testing for the parts `agent-device` cannot verify: exact spoken order, announcement timing, audio-description behavior, caption rendering, and platform-specific verbosity.

## Accessible Modals

```jsx
<Modal
  visible={isVisible}
  accessibilityViewIsModal={true}
  onRequestClose={handleClose}
>
  <View>
    {/* Don't wrap the body in `accessible` — it collapses children into one
        element and hides the buttons from focus. Label a header node instead. */}
    <Text accessibilityRole="header">Continue watching?</Text>
    <Text>Are you still watching?</Text>
    <Button title="Yes" onPress={handleContinue} />
    <Button title="No" onPress={handleExit} />
  </View>
</Modal>
```

- Set initial focus inside modal
- Trap focus within modal
- Announce dialog opening

## Autoplay Content

- Include remote-focusable playback controls
- `AccessibilityInfo.isScreenReaderEnabled()` returns a **Promise** — `await` it (or subscribe to the `screenReaderChanged` event) before deciding whether to mute; a bare synchronous `if` is always truthy:
  ```jsx
  const srOn = await AccessibilityInfo.isScreenReaderEnabled();
  if (srOn) muteAutoplay();
  ```
- Apple TV: respect system audio focus, integrate with `AVAudioSession`

## Cross-Platform Focus

Prefer `TVFocusGuideView` over `nextFocus*` for shared layouts. `destinations` takes an array of resolved components (`ref.current`), not the ref objects and not string IDs. Don't build it inline — `ref.current` is `null` on the first render and mutating a ref triggers no re-render, so the guide would register nothing. Hoist the resolved components into state once the children have mounted:
```jsx
const playRef = useRef(null);
const infoRef = useRef(null);
const [destinations, setDestinations] = useState([]);

// Children assign their refs after this component first renders; push the
// resolved nodes into state so a NEW array is passed and the guide updates.
useEffect(() => {
  setDestinations([playRef.current, infoRef.current].filter(Boolean));
}, []);

<TVFocusGuideView destinations={destinations}>
  <TouchableOpacity ref={playRef} accessibilityRole="button" accessibilityLabel="Play" />
  <TouchableOpacity ref={infoRef} accessibilityRole="button" accessibilityLabel="Info" />
</TVFocusGuideView>
```
See [focus-management.md](./focus-management.md) for when `nextFocus*` overrides are acceptable.

## Related Skills
- [a11y-overview.md](./a11y-overview.md) — Accessibility fundamentals for TV
- [a11y-checklist.md](./a11y-checklist.md) — Pre-launch checklist
- [focus-management.md](./focus-management.md) — Focus APIs
