---
title: Focus Management
impact: CRITICAL
tags: focus, tvfocusguideview, hastvpreferredfocus, d-pad, focus-traps, tv
---

# Focus Management

Focus is the core interaction model on TV. Every D-pad press sends focus from one element to another. When focus behaves as expected, users glide through the interface. When it doesn't, they get stuck or overshoot.

## Quick Reference
- **Let the platform focus engine handle it** — design layouts that are naturally focus-friendly before adding manual focus logic
- Use `TVFocusGuideView` for complex layouts that don't naturally connect
- Use `hasTVPreferredFocus` to set initial focus on screen load
- Use focus traps for modals and overlays
- Imperative focus (`requestTVFocus()`) should be a last resort

## Platform Focus Engines

### tvOS — Inferred Focus Engine
Apple's focus engine examines element positions and spatial proximity:
- Searches for focusable views in the direction of input
- Treats clusters as "focus islands"
- Expects clean grid/alignment patterns — misaligned elements cause unexpected jumps
- Supports diagonal movement and inertia-based swipes

### Android TV — Explicit Directional Model
- Focus moves to nearest visible item along pressed direction (Cartesian)
- Supports `nextFocusUp`, `nextFocusDown`, `nextFocusLeft`, `nextFocusRight` props
- More tolerant of irregular layouts
- When no valid target exists, focus can disappear entirely

### Vega OS
Works like Android TV using Cartesian focus management strategy.

## TVFocusGuideView

Groups focusable elements so the system can remember last focused child or redirect focus intelligently.

```jsx
const refSidebar = useRef(null);
const refGrid = useRef(null);
const [destinations, setDestinations] = useState([]);

// destinations takes resolved components (ref.current), not the ref objects.
// Build it AFTER mount: ref.current is null on first render and mutating a
// ref triggers no re-render, so a new array must be set into state.
useEffect(() => {
  setDestinations([refSidebar.current, refGrid.current].filter(Boolean));
}, []);

<TVFocusGuideView destinations={destinations}>
  <View style={{ flexDirection: 'row' }}>
    <Sidebar ref={refSidebar} />
    <ContentGrid ref={refGrid} />
  </View>
</TVFocusGuideView>
```

> If `Sidebar`/`ContentGrid` are custom function components, they must accept the ref: on **Vega OS (RN 0.72 / React 18)** wrap them in `forwardRef`; on **react-native-tvos with React 19 (RN 0.78+)** `ref` can be a plain prop. Built-in components like `TouchableOpacity` accept refs on both.

### Props
- **`destinations`** — Array of `Component`s (pass `ref.current`, not the ref) to register as focus targets. The guide updates only when this prop *changes*; if refs are null on first render, set them into state once mounted so a new array is passed
- **`trapFocusUp/Down/Left/Right`** — Prevents focus from escaping in specified directions
- **`autoFocus`** — Redirects focus to first focusable child; remembers last focused child on revisit

## hasTVPreferredFocus

Tells the focus engine where to start on screen load:

```jsx
<Pressable hasTVPreferredFocus onPress={startPlayback}>
  <Text>Start Watching</Text>
</Pressable>
```

**Rules:**
- Avoid setting multiple `hasTVPreferredFocus` in the same view
- Delay focus until data-dependent UI has rendered
- Available on: `View`, `Pressable`, `TouchableHighlight`, `TouchableOpacity`, `TextInput`, `Button`, `TVFocusGuideView`

## Focus Traps for Modals/Overlays

When modals open, focus must stay inside them:

```jsx
<TVFocusGuideView trapFocusUp trapFocusDown trapFocusLeft trapFocusRight>
  <View>
    <Pressable hasTVPreferredFocus onPress={onConfirm}>
      <Text>Confirm</Text>
    </Pressable>
  </View>
</TVFocusGuideView>
```

For web-based platforms (Tizen, webOS), use `@noriginmedia/norigin-spatial-navigation` to replicate similar behavior.

## Imperative Focus — Last Resort

```jsx
useEffect(() => {
  if (lastFocusedRef.current?.requestTVFocus) {
    lastFocusedRef.current.requestTVFocus();
  } else if (lastFocusedRef.current?.focus) {
    lastFocusedRef.current.focus();
  }
}, [isActiveScreen]);
```

**When imperative focus is needed:**
- Restoring focus when returning to a screen
- Scrolling a list where next target isn't yet mounted

**Prefer focusing a stable container** (e.g., a `TVFocusGuideView`) rather than a granular element.

## nextFocus* Props

`nextFocusUp`, `nextFocusDown`, `nextFocusLeft`, `nextFocusRight` set on `View` are honored natively by the **directional (Cartesian) focus engines** — Android TV, Fire TV, and Vega OS — and also by **tvOS** in current `react-native-tvos`. The tvOS caveat: if there is no focusable view in the specified direction, the override is ignored and the engine falls back to inferred (spatial) focus.

**Default rule:** prefer natural focus order and `TVFocusGuideView` for complex or shared layouts. Reach for `nextFocus*` only as a targeted override when that tvOS caveat is acceptable — not as the primary navigation strategy.

## Debugging Focus Issues

### Visualize Focus Movement
- **tvOS:** Simulator → Debug > Toggle Focus Rectangle
- **Android TV:** `adb logcat` and log focus changes
- **In-component:** Add red borders on focus for visual debugging

```jsx
<Pressable
  testID="playButton"
  style={({ focused }) => ({
    borderWidth: focused ? 2 : 0,
    borderColor: focused ? 'red' : 'transparent',
  })}
>
  <Text>Play</Text>
</Pressable>
```

### Add Logs
```jsx
<Pressable
  onFocus={() => console.log('Focused: playButton')}
  onBlur={() => console.log('Blurred: playButton')}
>
```

### Use React DevTools
- Inspect which components are actually focusable
- Identify invisible/off-screen elements receiving focus
- Profile re-renders after D-pad key presses

## Common Gotchas

| Issue | Solution |
|-------|----------|
| No focusable element on screen | Render a temporary focusable placeholder during loading |
| Focus lost after re-render | Keep `key` values stable; restore focus after new item renders |
| Focus on hidden content | Unmount hidden elements or disable focus explicitly |
| Gaps between elements | Use `TVFocusGuideView` to bridge them |
| Wrong initial focus | Only one `hasTVPreferredFocus` per view; wait for UI to render |

## Related Skills
- [focus-performance.md](./focus-performance.md) — Performance impact of focus changes
- [nav-directional.md](./nav-directional.md) — Directional navigation fundamentals
- [nav-patterns.md](./nav-patterns.md) — Navigation patterns and focus restoration
