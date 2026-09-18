---
title: Handling Cross-Platform Inconsistencies
impact: HIGH
tags: cross-platform, platform-detection, platform-select, spatial-navigation, tv
---

# Handling Cross-Platform Inconsistencies

When building for both mobile and TV, small platform differences add up. Centralize platform-specific logic and leverage libraries with built-in platform support.

## Quick Reference
- Use `Platform.isTV` for conditional TV logic
- Use platform-specific file extensions for drastically different UI
- Abstract platform-specific styles with `Platform.select()`
- Many libraries (react-navigation, react-native-gesture-handler) handle platform quirks internally

## Platform Detection

```jsx
import { Platform } from 'react-native';
if (Platform.isTV) {
  // TV-specific logic
}
```

Centralize platform checks in utility functions rather than scattering them throughout components.

## Platform-Specific Files

```
MyComponent.tvos.js
MyComponent.ios.js
MyComponent.android.js
```

React Native automatically selects the correct file for the running platform.

## Platform-Specific Styles

`Platform.select` keys match `Platform.OS`, not the marketing name — there are no `tvOS`/`fireTV` keys. The value differs per fork: `ios` on Apple TV and `android` on Android TV / Fire TV (`react-native-tvos`), but `kepler` on Vega (`react-native-kepler`). Branch on `Platform.OS` and gate TV-only logic with `Platform.isTV` (which is `true` on all three):

```jsx
const styles = StyleSheet.create({
  container: {
    ...Platform.select({
      ios: { shadowColor: '#000', shadowOpacity: 0.2 }, // tvOS uses shadow*
      android: { elevation: 4 },                        // Android TV / Fire TV
      // Vega (Platform.OS === 'kepler') matches neither — add a `kepler` key if needed
    }),
    ...(Platform.isTV ? { padding: 24 } : {}),
  },
});
```

> Note: `react-native-tvos` can't tell Fire TV apart from Android TV via `Platform` — both report `android`. Use device manufacturer info for that distinction.

## Third-Party Libraries

Check if a library already addresses your cross-platform needs before building custom solutions:
- **react-navigation** — Handles navigation patterns across platforms
- **react-native-gesture-handler** — Platform-aware gesture handling
- **@bamlab/react-tv-space-navigation** — Spatial navigation across TV platforms
- **@noriginmedia/norigin-spatial-navigation** — For web-based TV platforms

## nextFocus* for Cross-Platform

`nextFocusUp`, `nextFocusDown`, etc. on `View` are honored by the **Cartesian focus engines** (Android TV, Fire TV, Vega OS) and by **tvOS** — with a tvOS caveat: the override is ignored when no focusable view exists in that direction. For shared codebases, prefer `TVFocusGuideView` and inferred focus as the default, and use `nextFocus*` only as a targeted override where that caveat is acceptable. See [focus-management.md](./focus-management.md) for the full rule.

## react-native-tvos Compatibility

The `react-native-tvos` fork does not prevent mobile builds. It extends core with TV-specific features while maintaining API compatibility. Mobile app logic stays intact.

## Related Skills
- [setup-getting-started.md](./setup-getting-started.md) — Project setup
- [setup-architecture.md](./setup-architecture.md) — Code sharing strategies
- [focus-management.md](./focus-management.md) — Cross-platform focus handling
