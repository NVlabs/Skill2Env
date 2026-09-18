---
name: jahro-troubleshooting
description: >
  Diagnoses common Jahro issues using decision trees: commands not
  appearing, watcher not updating, console not opening, snapshots
  failing, launch button missing. Use when the user reports something
  not working, missing, broken, or unexpected with Jahro, or when
  generated Jahro code doesn't behave as expected.
---

# Jahro Troubleshooting

Diagnose and fix common Jahro issues. Follow the decision tree for the reported symptom.

## Diagnostic Approach

1. **Identify the symptom** — match to a decision tree below
2. **Walk the tree** — check conditions in priority order
3. **Apply fix** — provide code snippet or configuration change
4. **VERIFY** — "Enter Play Mode, reproduce the original issue"
5. **If still broken** — continue down the tree or escalate

---

## Issue: Commands Not Appearing

The user added `[JahroCommand]` attributes but commands don't show in the console.

### Decision Tree

```
Commands not appearing
├── Is the method static or instance?
│   ├── Instance → Is RegisterObject called?
│   │   ├── No → FIX: Add OnEnable/OnDisable registration
│   │   └── Yes → Is the object active in scene?
│   │       ├── No → Object never enables → RegisterObject never runs
│   │       └── Yes → Continue below
│   └── Static → Continue below
├── Is the correct assembly selected?
│   └── Check Tools → Jahro Settings → Assemblies Selection
│       └── Is the assembly containing this class checked?
│           ├── No → FIX: Select the assembly
│           └── Yes → Continue below
├── Is Jahro enabled?
│   ├── Check Jahro.Enabled at runtime (log it)
│   ├── Check JAHRO_DISABLE in Scripting Define Symbols
│   └── Check Auto-disable + build type
├── Is the method public?
│   └── Private/internal methods → FIX: Make public
├── Are parameter types supported?
│   └── Only: int, float, bool, string, Vector2, Vector3, enum
│       └── Custom class params → FIX: Change to supported type
└── Assembly scanning order issue?
    └── Static commands discovered at startup; if class loaded late,
        try manual RegisterObject or dynamic registration
```

### Fix: Missing RegisterObject

```csharp
// Add to the class with instance [JahroCommand] methods:
void OnEnable()  => Jahro.RegisterObject(this);
void OnDisable() => Jahro.UnregisterObject(this);
```

### Fix: Wrong assembly selected

1. Open **Tools → Jahro Settings → General Settings**
2. Under **Assemblies Selection**, check the assembly containing your class
3. Your main game assembly is typically `Assembly-CSharp`

---

## Issue: Watcher Not Updating

Watcher entries appear but values are frozen or stale.

### Decision Tree

```
Watcher values not updating
├── Is the Watcher tab actually open?
│   └── Values are ONLY read when the Watcher UI is visible
│       └── FIX: Switch to the Watcher tab to see live updates
├── Is RegisterObject called?
│   ├── No → FIX: Add OnEnable/OnDisable registration
│   └── Yes → Continue below
├── Is the watched member a field or property?
│   ├── Field → Updates automatically when value changes
│   └── Property → Check the getter
│       ├── Does the getter reference stale data?
│       ├── Does the getter throw an exception? (silently caught)
│       └── Is it an expensive getter that's being throttled?
├── Was the object destroyed?
│   └── Object destroyed without OnDisable → watcher reads stale reference
│       └── FIX: Ensure UnregisterObject runs (OnDisable handles this)
├── Is it a static watcher?
│   └── Static watchers don't need RegisterObject but do need
│       the assembly selected in Jahro Settings
└── Is Jahro enabled?
    └── Same checks as commands: JAHRO_DISABLE, auto-disable, settings
```

### Fix: Property getter issues

```csharp
// BAD: getter may throw if Rigidbody is destroyed
[JahroWatch("Velocity", "Physics")]
public Vector3 Velocity => GetComponent<Rigidbody>().velocity;

// GOOD: null-safe getter
[JahroWatch("Velocity", "Physics")]
public Vector3 Velocity => TryGetComponent<Rigidbody>(out var rb) ? rb.velocity : Vector3.zero;
```

---

## Issue: Console Not Opening

User presses ~ (or triple-taps) but nothing happens.

### Decision Tree

```
Console not opening
├── Is Jahro enabled?
│   ├── Check Tools → Jahro Settings → Enable Jahro → must be ON
│   ├── Check JAHRO_DISABLE in Player Settings → Scripting Define Symbols
│   │   └── If defined → FIX: Remove it (or it's intentional for this build)
│   └── Check Auto-disable in Release Builds + build type
│       └── If Release build with auto-disable ON → expected behavior
├── Is the launch key correct?
│   └── Check Tools → Jahro Settings → Launch Key
│       └── Default is ~ (Tilde). May have been changed.
├── Is it a mobile build?
│   └── ~ key doesn't work on mobile
│       └── FIX: Triple-tap at top of screen (must be enabled in settings)
│           └── Check Mobile Tap Activation in Jahro Settings
├── Is Play Mode actually running?
│   └── Jahro only works in Play Mode, not Edit Mode
├── Check Unity console for messages:
│   ├── "Jahro Console: Disabled in this build" → Jahro disabled (see above)
│   └── Any Jahro initialization errors → report them
└── Keyboard shortcut conflict?
    └── Another asset or system binding may capture ~ before Jahro
        └── FIX: Change Launch Key to an unused key
```

### Fix: Verify Jahro is running

Add this to any MonoBehaviour's Start method temporarily:

```csharp
void Start()
{
    Debug.Log($"Jahro.Enabled: {Jahro.Enabled}");
    Debug.Log($"Jahro.IsOpen: {Jahro.IsOpen}");
}
```

---

## Issue: Snapshots Failing

Snapshots don't upload, don't stream, or show errors.

### Decision Tree

```
Snapshots failing
├── Is the API key configured?
│   └── Check Tools → Jahro Settings → Account → API Key
│       ├── Empty → FIX: Get key from console.jahro.io → Project → API Keys
│       └── Present → Does it validate? (settings show project info if valid)
├── Is the device online?
│   └── Upload and streaming require network connectivity
│       └── Recording mode works offline; upload when connected
├── What snapshot mode is selected?
│   ├── Recording → Must manually tap Upload after stopping
│   ├── Streaming (All) → Should auto-stream; check network
│   └── Streaming (Except Editor) → Won't stream from Editor
│       └── If testing in Editor → FIX: Use Recording or Streaming (All)
├── Is the session in the right state?
│   ├── Recording → must Stop first → then Upload
│   ├── Recorded → ready to Upload
│   ├── Uploading → wait for completion
│   └── Error shown → check inline error message, tap Retry
├── Check snapshot mode setting:
│   └── Tools → Jahro Settings → Snapshots Settings
└── Web console access:
    └── Can you access console.jahro.io? → verify account and project exist
```

---

## Issue: Launch Button Missing

The floating launch button doesn't appear.

### Decision Tree

```
Launch button missing
├── Is it enabled?
│   └── Check if code calls Jahro.DisableLaunchButton()
│       └── FIX: Call Jahro.EnableLaunchButton()
├── Is it hidden?
│   └── Check if code calls Jahro.HideLaunchButton()
│       └── FIX: Call Jahro.ShowLaunchButton()
├── Is Jahro itself enabled?
│   └── Same checks: JAHRO_DISABLE, auto-disable, settings
├── UI layer conflict?
│   └── Launch button renders in an overlay canvas
│       └── Check if another full-screen UI is rendering on top
└── Was it dragged off-screen?
    └── Position persists across sessions
        └── FIX: Reset Jahro settings or call EnableLaunchButton() to reset
```

---

## Issue: Configuration Conflicts

### JAHRO_DISABLE but expecting Jahro to work

```
User defined JAHRO_DISABLE in Scripting Define Symbols but expects
Jahro to function in Debug builds.

FIX: JAHRO_DISABLE overrides ALL other settings. Remove it from
Player Settings → Scripting Define Symbols if you want Jahro to
function. Use "Auto-disable in Release Builds" instead for
production-only disabling.
```

### Auto-disable ON but testing in Release build

```
User has Auto-disable in Release Builds ON and is testing a Release
build. Jahro correctly disables itself.

FIX: Use a Development Build for testing with Jahro, or temporarily
disable Auto-disable in Jahro Settings.
```

### Commands work in Editor but not on device

```
Commands appear in Editor but not on built devices.

CHECK:
1. Assembly scanning — device builds may use different assemblies
2. JAHRO_DISABLE — may be set for the target platform only
3. Auto-disable — device build may be Release
4. RegisterObject — ensure the MonoBehaviour is active in the device scene
```

---

## Source Code Tracing (Optional)

If the Jahro source code is available in the project (either `jahro-unity-package/` or `Assets/JahroPackage/`), you can optionally read relevant source files to trace issues deeper:

- Registration logic: look for `RegisterObject` implementation
- Assembly scanning: look for attribute discovery code
- Lifecycle: look for `RuntimeInitializeOnLoadMethod` handlers

Only do this if the standard decision tree doesn't resolve the issue. The source is not always present (UPM installations don't include it).

---

## Verify-After-Fix Loop

After every fix suggestion:

> **Verify:** Enter Play Mode and reproduce the original issue. If fixed, confirm the expected behavior. If still broken, report back what you see and we'll continue down the decision tree.

For commands/watchers: check the relevant tab in the console.
For console not opening: press ~ and check Unity console for messages.
For snapshots: try the full capture → upload/stream → check web console flow.
