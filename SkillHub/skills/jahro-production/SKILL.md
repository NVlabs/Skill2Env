---
name: jahro-production
description: >
  Configures Jahro lifecycle controls for safe production deployment
  including JAHRO_DISABLE, auto-disable, and build validation. Use
  when the user mentions production builds, release builds, disabling
  Jahro, shipping, CI/CD, lifecycle controls, or production safety.
---

# Jahro Production Readiness

Help users configure Jahro for safe production deployment so debugging tools never leak into release builds.

## Three-Tier Disable Mechanism

Jahro evaluates these conditions at startup in priority order:

```
1. JAHRO_DISABLE defined?           → Disabled (highest priority)
2. Auto-disable ON + Release build? → Disabled
3. Enable Jahro switch              → Uses switch value (lowest priority)
```

### Tier 1: JAHRO_DISABLE Preprocessor Define

**What:** Compile-time disable. When defined, Jahro exits at initialization regardless of all other settings.

**How to set:**
1. Open **Edit → Project Settings → Player**
2. Under **Other Settings → Scripting Define Symbols**
3. Add `JAHRO_DISABLE` (semicolon-separated if other defines exist: `MY_DEFINE;JAHRO_DISABLE`)

**When to use:** CI/CD pipelines, absolute control, platform-specific disabling (set per-platform defines).

**Validation:** Build logs show "Jahro Console: Disabled in this build".

### Tier 2: Auto-disable in Release Builds

**What:** Runtime check. Jahro checks `Debug.isDebugBuild` at startup. If `false` (Release build) and this setting is ON, Jahro disables itself.

**How to set:**
1. Open **Tools → Jahro Settings → General Settings**
2. Enable **Auto-disable in Release Builds**

**When to use:** Recommended default for most projects. Development and Debug builds keep Jahro active; Release builds automatically disable it.

**Validation:** Same build log message when triggered.

### Tier 3: Manual Enable/Disable

**What:** The master toggle in Jahro Settings.

**How to set:** Tools → Jahro Settings → General Settings → **Enable Jahro**

**When to use:** Temporarily disable during development (e.g., testing without Jahro interference).

### Recommendation

For most projects:
1. Enable **Auto-disable in Release Builds** (Tier 2) — this is sufficient
2. Add **JAHRO_DISABLE** (Tier 1) in CI/CD for extra safety
3. Leave the manual toggle ON for development

## Lifecycle

### Initialization (BeforeSplashScreen)

Jahro initializes via `[RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSplashScreen)]`:

1. Loads settings from `Assets/Jahro/Resources/jahro-settings.asset`
2. Evaluates the three-tier disable logic
3. If disabled: logs "Jahro Console: Disabled in this build" and **exits early** — minimal overhead
4. If enabled: sets up logging infrastructure, then continues to runtime boot

The `BeforeSplashScreen` timing ensures Jahro is ready before any game code runs, so it captures logs from the very start.

### Runtime Boot

After initialization (if enabled):
- Initializes console storage and UI view
- Verifies API key, starts session
- Injects UI manager (window, tabs, launch button)
- Binds hotkeys and mobile activation

### Shutdown

Triggered on app quit, assembly reload, or explicit `Jahro.Release()`:
- Saves console state (window size, position, favorites)
- Disposes logger, destroys UI
- Ends Jahro session

## CI/CD Guidance

### Setting JAHRO_DISABLE per build configuration

In your build script or CI/CD pipeline:

```csharp
// In a custom build script
PlayerSettings.SetScriptingDefineSymbolsForGroup(
    BuildTargetGroup.Android,
    "JAHRO_DISABLE;OTHER_DEFINES");
```

Or via command line:

```bash
unity -batchmode -executeMethod Build.PerformReleaseBuild \
  -define "JAHRO_DISABLE"
```

### Build log validation

After a Release build, verify Jahro is properly disabled:

```
// Expected in build log output:
Jahro Console: Disabled in this build
```

If this message is absent and Jahro was expected to be disabled, check:
- `JAHRO_DISABLE` is in the correct platform's Scripting Define Symbols
- Auto-disable is ON and the build is actually a Release build (not Development)

## Runtime Validation Code

Add this to verify Jahro's state in a build:

```csharp
void Start()
{
    #if JAHRO_DISABLE
    Debug.Log("JAHRO_DISABLE is defined — Jahro stripped at compile time");
    #else
    Debug.Log($"Jahro.Enabled: {Jahro.Enabled}");
    if (Jahro.Enabled)
        Debug.LogWarning("Jahro is ENABLED in this build — is this intentional?");
    #endif
}
```

## Production Readiness Checklist

Use this checklist before shipping:

- [ ] **Auto-disable in Release Builds** is ON in Tools → Jahro Settings
- [ ] (Optional) **JAHRO_DISABLE** added to Scripting Define Symbols for release platform
- [ ] Build configuration is **Release** (not Development Build)
- [ ] Build log contains "Jahro Console: Disabled in this build"
- [ ] Test the Release build: pressing ~ or triple-tap does NOT open console
- [ ] `Jahro.Enabled` returns `false` at runtime in the Release build
- [ ] `jahro-settings.asset` is committed to version control with correct settings
- [ ] API key is NOT exposed in public builds (Jahro handles this — when disabled, no network calls are made)

## Role-Based Access (Team Projects)

For teams using the Jahro web console:

| Role | Permissions |
|:-----|:------------|
| **Owner** | Billing, subscription, team settings, role assignment, ownership transfer |
| **Admin** | Manage members (except Owner), configure integrations, access all content |
| **Member** | Create/view/edit snapshots, interact with assigned content |

Configure roles at **console.jahro.io** → Team Settings.

## Contextual Awareness

| Pattern | Suggestion |
|:--------|:-----------|
| User mentions "release build" or "shipping" | Guide through production checklist |
| User mentions CI/CD or build pipeline | Show JAHRO_DISABLE in build scripts |
| User has JAHRO_DISABLE but expects Jahro to work | Explain priority: define overrides everything |
| User asks about performance in production | Reassure: disabled Jahro exits early with near-zero overhead |

## Verification

> **Verify:** Make a Release build (not Development Build). Run it. Confirm:
> 1. Build log shows "Jahro Console: Disabled in this build"
> 2. Console does NOT open on ~ or triple-tap
> 3. `Jahro.Enabled` returns `false`
>
> Then make a Development Build and confirm Jahro works normally.
