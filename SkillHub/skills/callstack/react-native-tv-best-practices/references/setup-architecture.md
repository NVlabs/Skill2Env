---
title: Codebase Architecture and Sharing
impact: MEDIUM
tags: architecture, code-sharing, monorepo, platform-extensions, cross-platform, tv
---

# Codebase Architecture and Sharing

The choice of structure depends on your project's scope and whether your app is part of a larger multi-platform product.

## Quick Reference
- Monorepo is the most common structure for TV apps (platforms require bundled applications)
- Reuse business logic, state, hooks, and API layers before reusing screen UI
- Expect TV screen UI, focus behavior, and platform packaging to need dedicated implementations
- Use TV-specific Metro extensions (`.ios.tv.*`, `.android.tv.*`, `.tv.*`) only when the project has enabled them in Metro

## Multi-Platform TV Shape

```
my-tv-app/
├── ios/              # iOS native files
├── tvos/             # tvOS native files
├── android/          # Android, Android TV, Fire TV native
├── vega/             # Vega OS native files
├── web/              # web, webOS, Tizen native files
├── src/              # Application code (shared)
│   ├── index.web.tsx # Web entry point
│   └── index.js      # Native entry point
├── rsbuild.config.ts # Web bundler config
├── metro.config.ts   # Native bundler config
└── package.json
```

Use this shape as a detection aid, not a required layout. The important review question is whether TV-native folders and packaging files match the stack detected in [SKILL.md](../SKILL.md).

## Platform Detection

```jsx
import { Platform } from 'react-native';
if (Platform.isTV) {
  // TV-specific logic
}
```

## Platform-Specific Components

For UI that differs by focus model or TV layout, use file extensions:
```
MyComponent.ios.tv.tsx
MyComponent.android.tv.tsx
MyComponent.tv.tsx
MyComponent.ios.tsx
MyComponent.android.tsx
```

`react-native-tvos` documents this resolution order for projects that opt into TV extensions in Metro: platform-specific TV file, generic TV file, then normal platform file. This Metro configuration is not enabled by default because it can affect bundling performance.

## Platform-Specific Styles

`Platform.select` keys match `Platform.OS`, not the marketing name — there are no `tvOS`/`fireTV` keys. `Platform.OS` is `ios` on Apple TV and `android` on Android TV / Fire TV (`react-native-tvos`), but `kepler` on Vega (see [Vega OS](#vega-os) below). Gate TV-only logic with `Platform.isTV`:

```jsx
import { StyleSheet, Platform } from 'react-native';
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

## Android TV Setup

Minimal changes — same APK runs on TV:
- Add `android.software.leanback` support in manifest
- Add `LEANBACK_LAUNCHER` intent filter

## tvOS Setup

Needs a separate `tvos/` folder (copy of `ios/` with modifications) due to CocoaPods setup. Initialize from template and move the generated `ios/` folder.

## Web-Based TVs (webOS, Tizen)

Put web-native code in `web/` folder. Use Rsbuild (or your preferred bundler) for web builds with server host `0.0.0.0` for TV device discovery.

## Vega OS

Standalone setup using React Native 0.72 (React 18). Follow official Vega OS docs. Code sharing may be limited by React 18/19 API differences.

## Related Skills
- [setup-getting-started.md](./setup-getting-started.md) — Project creation and dependencies
- [setup-cross-platform.md](./setup-cross-platform.md) — Handling platform inconsistencies
- [release-cicd.md](./release-cicd.md) — CI/CD for multi-platform TV apps
