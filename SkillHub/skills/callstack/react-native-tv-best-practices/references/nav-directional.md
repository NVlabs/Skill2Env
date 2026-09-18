---
title: Directional Navigation Fundamentals
impact: CRITICAL
tags: navigation, directional, focus-engine, d-pad, spatial-navigation, tv
---

# Directional Navigation Fundamentals

Every TV app starts with a simple question: where does the focus go next? When a viewer presses an arrow on the remote, the app must decide which element becomes active.

## Quick Reference

- TV navigation is fundamentally physical — each button press is deliberate
- Platform focus engines differ: tvOS uses spatial inference, Android TV uses proximity, web-based TVs need JS libraries
- Design layouts that work with the focus engine, not against it
- Align and space elements logically so directional presses resolve to the intended neighbor

## How Focus Engines Work

### tvOS — High Precision

Apple's engine examines layout geometry:

- Searches for focusable views based on spatial proximity in the pressed direction
- Treats related items as "focus islands" (cohesion zones)
- Expects clean grid/alignment patterns
- When layouts are clean: focus slides and decelerates like real physics
- Account for diagonal movement and inertia-based swipes

### Android TV — Developer-Defined

More flexible, leans on developer direction:

- Focus moves to nearest visible item along pressed direction (Cartesian)
- Override with `nextFocusUp`, `nextFocusDown`, `nextFocusLeft`, `nextFocusRight`
- Tolerates less regular layouts
- When no valid target exists, focus can disappear

### Vega OS

Same Cartesian focus management as Android TV — focus moves to "closest" item in D-pad direction.

### Web-Based TVs (Tizen, webOS)

No native focus engine — must use JavaScript spatial navigation:

- `@noriginmedia/norigin-spatial-navigation` is the most popular library
- Keeps a registry of focusable nodes
- Listens for arrow/enter keys
- Decides next target based on geometry and direction

## Preferred Approach: Let the Platform Lead

For most apps, the best focus management is no explicit management at all:

```jsx
<View style={styles.row}>
	{items.map((item) => (
		<Pressable
			key={item.id}
			onPress={() => select(item)}
			onFocus={() => setFocusedItem(item.id)}
		>
			<Image source={item.poster} />
		</Pressable>
	))}
</View>
```

**Key strategies:**

- Align and space elements logically
- Avoid dead zones — gaps cause unpredictable jumps
- Group related UI into containers ("focus islands")
- On tvOS: account for diagonal movement; on Android TV: design for strict up/down/left/right

If focus suddenly behaves strangely, it's usually a sign the layout needs adjusting, not that you need more code.

## React Native TV's Focus Tree

Each platform builds a focus tree — an internal map of all focusable elements. Every `Pressable`, `Touchable`, or `TextInput` becomes a node. React Native TV mirrors this with unified focus APIs.

## Two Navigation Layers

1. **Global navigation** — Moves between main sections (Home, Search, Settings). Typically a drawer.
2. **Local navigation** — Operates within a section (Popular, Recommended tabs). Typically tabs.

## Building Predictable Navigation

- **Consistent movement:** If "right" moves to next card, keep that everywhere
- **Let layout lead:** Clear alignment helps the engine make right decisions
- **Plan focus transitions:** Define where focus starts, how "back" behaves, what regains focus on return
- **Shallow hierarchy:** Too many layers makes users lose their bearings

## Related Skills

- [focus-management.md](./focus-management.md) — TVFocusGuideView, hasTVPreferredFocus, debugging
- [nav-patterns.md](./nav-patterns.md) — Drawer, tabs, modals, back navigation
- [design-layout.md](./design-layout.md) — Layout patterns that support natural focus flow
