---
title: Getting Started with React Native for TV
impact: MEDIUM
tags: setup, react-native-tvos, expo, tvos, android-tv, getting-started
---

# Getting Started with React Native for TV

Use this reference only after stack detection identifies a `react-native-tvos` or Expo TV app. For Amazon Vega/Kepler or web-based TV targets, use the platform toolchain instead; do not require `react-native-tvos`, a tvOS Podfile, or Android TV manifest entries there.

`react-native-tvos` is an independent React Native fork for Apple TV, Android TV, and Fire TV. It tracks React Native core while adding TV focus, remote input, and platform APIs.

## Quick Reference
- Use `react-native-tvos` as a drop-in replacement for `react-native`
- For Expo, use the TV templates or `@react-native-tvos/config-tv` and keep the `react-native-tvos` version aligned with the Expo SDK
- The fork does NOT prevent building regular iOS/Android mobile apps
- TV support adds focus handling, remote input, and TV-optimized components

## Without Expo (React Native CLI)

### New Project
```bash
npx @react-native-community/cli@latest init TVTest \
  --template @react-native-tvos/template-tv
```

### Existing Project
Replace `react-native` in `package.json`:
```json
"react-native": "npm:react-native-tvos@latest"
```

#### Android TV Setup
Add to `AndroidManifest.xml`:
```xml
<intent-filter>
  <category android:name="android.intent.category.LEANBACK_LAUNCHER" />
</intent-filter>

<uses-feature android:name="android.hardware.touchscreen" android:required="false" />
<uses-feature android:name="android.hardware.faketouch" android:required="false" />
<uses-feature android:name="android.software.leanback" android:required="true" />
```

> Add these to TV-specific manifest only. Mobile builds still need touchscreen.

#### Apple TV Setup
- Update `project.pbxproj` to include tvOS platform
- In Podfile: `platform :tvos, min_ios_version_supported`
- Current `react-native-tvos` app Podfiles support either an iOS target or a tvOS target; do not keep both targets in the same Podfile

## With Expo

### New Project
```bash
npx create-expo-app MyTVProject -- -e with-tv
# Or with navigation:
npx create-expo-app MyTVProject -- -e with-router-tv
```

### Existing Expo Project
1. Replace react-native:
   ```json
   "react-native": "npm:react-native-tvos@0.85-stable"
   ```
2. Match the `react-native-tvos` version to the Expo SDK's React Native version. For SDK 56+, Expo upgrades this dependency with SDK upgrades; for SDK 55 and earlier, upgrade it manually and exclude it from `expo install` validation:
   ```json
   "expo": { "install": { "exclude": ["react-native"] } }
   ```
3. Install TV plugin:
   ```bash
   npx expo install @react-native-tvos/config-tv -- --dev
   ```
4. Add to `app.json`:
   ```json
   { "plugins": ["@react-native-tvos/config-tv"] }
   ```
5. Build. The plugin runs when `EXPO_TV=1` is set, or when its `isTV` plugin option is true:
   ```bash
   export EXPO_TV=1
   npx expo prebuild --clean
   ```

## Environment Setup

Same as React Native mobile, plus:
- **Android:** Download TV system image in SDK Manager, create Android TV emulator
- **Apple TV:** Install tvOS SDK via `xcodebuild --downloadAllPlatforms`

## Key API Differences from Core React Native

| Component / API | TV Changes |
|----------------|------------|
| `Platform` | Added `Platform.isTV` (any TV) and `Platform.isTVOS` (Apple TV only). No `isAndroidTV` flag — detect with `Platform.OS === 'android' && Platform.isTV`. Fire TV needs device info (manufacturer), not a `Platform` flag. |
| `Pressable`, `TouchableHighlight`, `TouchableOpacity` | Native `onFocus` & `onBlur` events + remote mapping |
| `TouchableNativeFeedback`, `TouchableWithoutFeedback` | Press events work, but focus/blur events do not; avoid for TV focusable controls |
| `Pressable` | `.focus:` and `.active:` Tailwind pseudo classes |
| `TVEventHandler` / `useTVEventHandler` | Custom remote event handling |
| `TVFocusGuideView` | Focus management between disconnected areas |
| `View` | `nextFocus*` props for directional focus overrides (Cartesian platforms — Android TV, Fire TV, Vega OS — plus tvOS with a caveat; see [focus-management.md](./focus-management.md)) |
| `ScrollView` | TV-only snap/focus props such as `snapToAlignment="item"`, `scrollSnapAlign`, `scrollSnapOffset`, and `scrollAnimationEnabled` |
| `VirtualizedList` | Extended for focus management, including `additionalRenderRegions` for critical always-rendered ranges |
| `BackHandler` | Extended for Apple & Android TV back button |
| `TVTextScrollView` (Apple TV) | Scrolling via swipe gestures from remote |
| `TVEventControl` (Apple TV) | Enable/disable Siri remote features |

## Community Resources
- **Ignite TV** — Boilerplate from Infinite Red for TV apps
- **Amazon Sample Apps** — Multi-platform TV best practices
- **Hoppix** — Demo showing spatial navigation on TV
- **@bamlab/react-tv-space-navigation** — Spatial navigation across platforms

## Related Skills
- [setup-architecture.md](./setup-architecture.md) — Project structure and code sharing
- [setup-cross-platform.md](./setup-cross-platform.md) — Handling platform differences
