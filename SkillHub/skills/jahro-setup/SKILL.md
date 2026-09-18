---
name: jahro-setup
description: >
  Detects Jahro in Unity projects and guides installation, API key
  configuration, and feature overview. Use when the user mentions Jahro
  setup, installation, getting started, debug console, or asks what
  Jahro can do. Also triggers when no Jahro references are found in a
  Unity project and the user asks about debugging.
---

# Jahro Setup & Orientation

Help users install, configure, and get oriented with the Jahro debugging platform for Unity.

## Detection

Before giving advice, determine Jahro's status in the project:

**Check 1 — Package Manager:**
Read `Packages/manifest.json` and search for `io.jahro.console` in the dependencies.

**Check 2 — Code references:**
Search C# files for `using JahroConsole` or `[JahroCommand` or `[JahroWatch`.

**Check 3 — Source folder:**
Check if `jahro-unity-package/` or `Assets/JahroPackage/` exists (indicates source-included installation).

| Result | Action |
|:-------|:-------|
| Package found in manifest | Jahro is installed — check API key config |
| Code references but no package | Jahro may be installed via source — verify |
| Nothing found | Guide installation |

## Installation

### Via Unity Package Manager (recommended)

1. Open Unity → **Window → Package Manager**
2. Click **+** → **Add package from Git URL**
3. Paste: `https://github.com/jahro-console/unity-package.git`
4. Click **Install**

Requirements: Unity 2021.3.0f1 or later. No additional dependencies.

## API Key Configuration

After installation, the user needs an API key to enable snapshot sync and team features.

1. Create account at **console.jahro.io/auth/signup** (free)
2. In web console → navigate to **Project → API Keys** → copy key
3. In Unity → **Tools → Jahro Settings** → **Account** tab → paste API key
4. Settings auto-validate and display project/team info

The API key connects the Unity project to the Jahro web console for snapshot uploads and team collaboration. Jahro works for local debugging (logs, commands, watcher) even without an API key, but snapshots won't upload.

## Opening the Console

| Platform | Action |
|:---------|:-------|
| Desktop (Editor/Standalone) | Press **~** (tilde) key in Play Mode |
| Mobile (Android/iOS) | **Triple-tap** at top of screen |
| Programmatic | Call `Jahro.ShowConsoleView()` |
| Alternative | Tap the floating **Launch Button** |

The launch key is configurable in **Tools → Jahro Settings → General Settings → Launch Key**.

Keyboard shortcuts for tabs: **Alt+1** (Text Mode), **Alt+2** (Visual Mode), **Alt+3** (Watcher), **Alt+4** (Snapshots).

## Feature Overview

Guide users to the right feature based on what they need:

### What to adopt first

Recommend features in this order based on effort-to-value ratio:

**1. Logs (zero effort)** — Jahro automatically intercepts all `Debug.Log`, `Debug.LogWarning`, and `Debug.LogError` calls. Just open the console to see them filtered and searchable in-game. Especially valuable on mobile where you'd otherwise need ADB logcat or Xcode.

**2. Commands (low effort)** — Add `[JahroCommand]` attributes to existing methods to make them callable from the console. Ideal for cheats, debug actions, and testing without rebuilding. Works in both Text Mode (CLI with autocomplete) and Visual Mode (touch-friendly buttons).

Read `references/api-reference.md` for the `[JahroCommand]` attribute constructor and parameter types.

**3. Watcher (low effort)** — Add `[JahroWatch]` attributes to fields and properties for real-time monitoring. Replaces Debug.Log polling patterns. Values only update when the Watcher tab is open, so negligible performance cost.

Read `references/api-reference.md` for the `[JahroWatch]` attribute constructor and supported types.

**4. Snapshots (needs API key)** — Capture logs + screenshots + device metadata and share via URL. Three modes: Recording (local until upload), Streaming All (real-time), Streaming Except Editor (hybrid). Essential for QA teams on mobile.

### Quick answers

**"How do I open the console?"**
Press `~` on desktop, triple-tap on mobile, or call `Jahro.ShowConsoleView()`.

**"How do I change the hotkey?"**
Tools → Jahro Settings → General Settings → Launch Key.

**"Does Jahro work on mobile?"**
Yes — Android and iOS. Triple-tap to open. Supports Standalone (PC/Mac) and Mobile. WebGL, Consoles, and VR are on the roadmap.

**"What's the performance impact?"**
Minimal. Watcher only reads values when the UI is visible. When disabled via `JAHRO_DISABLE` or auto-disable, Jahro exits at initialization with near-zero overhead.

**"How do I disable Jahro in production?"**
Enable "Auto-disable in Release Builds" in Jahro Settings, or add `JAHRO_DISABLE` to Scripting Define Symbols. See the jahro-production skill for detailed guidance.

**"Do I need to change my existing Debug.Log calls?"**
No. Jahro intercepts Unity's logging system automatically. Your existing `Debug.Log`, `Debug.LogWarning`, and `Debug.LogError` calls all appear in the Jahro console.

## Assembly Configuration

Jahro scans selected assemblies for `[JahroCommand]` and `[JahroWatch]` attributes.

Configure in **Tools → Jahro Settings → General Settings → Assemblies Selection**.

Recommended: select your main game assembly plus Jahro assemblies (for Samples). The system supports up to 31 user assemblies and automatically filters Unity system assemblies.

If commands or watchers aren't appearing, check that the correct assemblies are selected.

## Settings Persistence

Settings are saved to `Assets/Jahro/Resources/jahro-settings.asset`. Include this file in version control so all team members share the same configuration.

## Contextual Awareness

When working with Unity code:

- If you see `using JahroConsole` or `[JahroCommand]` or `[JahroWatch]` in existing code → Jahro is installed. Offer improvements or suggest additional features (watcher if only commands exist, commands if only watcher exists).
- If you see `OnGUI()` with debug buttons → suggest migrating to Jahro commands.
- If you see `Debug.Log` in `Update()` for monitoring values → suggest using `[JahroWatch]` instead.
- If no Jahro references exist → offer setup guidance.

## Next Steps

After setup, guide the user to the appropriate specialized skill:

| User wants to... | Suggest |
|:-----------------|:--------|
| Add debug commands to their code | jahro-commands skill |
| Monitor variables in real-time | jahro-watcher skill |
| Share debugging sessions with team | jahro-snapshots skill |
| Prepare for production release | jahro-production skill |
| Diagnose why something isn't working | jahro-troubleshooting skill |
| Migrate from a custom debug system | jahro-migration skill |

For full API details, read `references/api-reference.md`.
For common code patterns, read `references/common-patterns.md`.
