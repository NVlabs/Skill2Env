---
name: jahro-migration
description: >
  Analyzes existing debug systems (IMGUI menus, custom loggers, cheat
  frameworks, performance HUDs) and generates incremental migration
  plans to Jahro equivalents. Use when the user wants to replace a
  custom debug UI, migrate from an existing console or cheat system,
  switch to Jahro, or has OnGUI debug code they want to modernize.
---

# Jahro Migration

Help users migrate from custom debug tools to Jahro. Analyze existing code, classify what to replace/keep/adapt, and generate migrated code incrementally.

## Migration Decision Guide

When the user shares their existing debug code, classify each component:

| What are you migrating? | Jahro Replacement | Action |
|:------------------------|:-----------------|:-------|
| IMGUI debug buttons (`OnGUI` + `GUI.Button`) | `[JahroCommand]` + Visual Mode | Replace — Visual Mode provides a better button UI |
| Canvas-based debug UI | `[JahroCommand]` + Visual Mode | Replace — eliminates UI maintenance |
| Custom command parser (string → command) | `[JahroCommand]` + Text Mode | Replace — Jahro handles parsing and type conversion |
| Cheat code system (dictionary/registry) | `[JahroCommand]` with groups | Replace — typed parameters, auto-discovery |
| Custom Debug.Log wrapper | Remove or keep | Jahro intercepts `Debug.Log` automatically — wrapper often unnecessary |
| Performance HUD (FPS, memory overlay) | `[JahroWatch]` groups | Replace — Watcher provides organized monitoring |
| File-based logger | Keep | Jahro doesn't write to files — keep if file logging is needed |
| Custom Inspector/Editor tools | Evaluate | May complement Jahro — keep if Editor-only tools |
| Analytics-based logging | Keep | Different purpose — Jahro is for debugging, not analytics |

## Migration Workflow

1. **User shares existing debug code** — ask to see the files or point to the classes
2. **Classify each component** using the decision guide above
3. **Generate a migration plan**: what to replace, what to keep, what to adapt, effort estimate
4. **Generate migrated code** — file by file, side by side with original
5. **Support incremental migration** — old and new can coexist
6. **VERIFY at each step** — "Enter Play Mode, confirm migrated commands appear in Jahro"

## Pattern: IMGUI Debug Menu → Jahro Commands

### Before (IMGUI)

```csharp
public class DebugMenu : MonoBehaviour
{
    private bool showMenu;

    void OnGUI()
    {
        if (GUI.Button(new Rect(10, 10, 100, 30), "Toggle"))
            showMenu = !showMenu;
        if (!showMenu) return;

        if (GUI.Button(new Rect(10, 50, 150, 30), "God Mode"))
            Player.GodMode = true;
        if (GUI.Button(new Rect(10, 90, 150, 30), "Add 1000 Gold"))
            Player.Gold += 1000;
        if (GUI.Button(new Rect(10, 130, 150, 30), "Skip Level"))
            LevelManager.SkipToNext();

        GUI.Label(new Rect(10, 170, 200, 30), $"FPS: {1f/Time.deltaTime:F0}");
        GUI.Label(new Rect(10, 200, 200, 30), $"Health: {Player.Health}");
    }
}
```

### After (Jahro)

```csharp
using JahroConsole;
using UnityEngine;

public class DebugCommands : MonoBehaviour
{
    [JahroCommand("god-mode", "Cheats", "Enable god mode")]
    public static void GodMode() => Player.GodMode = true;

    [JahroCommand("add-gold", "Cheats", "Add 1000 gold")]
    public static void AddGold() => Player.Gold += 1000;

    [JahroCommand("skip-level", "Game", "Skip to next level")]
    public static void SkipLevel() => LevelManager.SkipToNext();

    [JahroWatch("FPS", "Performance")]
    public static string FPS => (1f / Time.unscaledDeltaTime).ToString("F0");

    [JahroWatch("Health", "Player")]
    public static int Health => Player.Health;
}
```

**What changed:**
- `GUI.Button` actions → `[JahroCommand]` static methods
- `GUI.Label` monitors → `[JahroWatch]` static properties
- `OnGUI` class can be deleted after migration
- Visual Mode replaces the custom button UI — no IMGUI maintenance
- No `RegisterObject` needed since everything is static

### Parameterized version

If the original had user input (e.g., text field for gold amount):

```csharp
[JahroCommand("add-gold", "Cheats", "Add gold to player")]
public static void AddGold(int amount) => Player.Gold += amount;
```

Visual Mode auto-generates an input field; Text Mode accepts `add-gold 500`.

## Pattern: Custom Logger → Jahro (Usually Remove)

### Before

```csharp
public static class GameLogger
{
    public static void Log(string category, string message)
        => Debug.Log($"[{category}] {message}");
    public static void LogWarning(string category, string message)
        => Debug.LogWarning($"[{category}] {message}");
    public static void LogError(string category, string message)
        => Debug.LogError($"[{category}] {message}");
}
```

### After

**No migration needed.** Jahro automatically intercepts all `Debug.Log`, `Debug.LogWarning`, and `Debug.LogError` calls. The logs appear in Jahro's console with filtering and search.

**Decision:**
- If the wrapper only formats messages → **remove it** (Jahro shows full messages)
- If the wrapper adds categorization you rely on → **keep it** (Jahro still captures the output)
- If the wrapper writes to files → **keep it** (Jahro doesn't do file logging)

There is no `Jahro.Log()` API — Jahro works by intercepting Unity's logging system.

## Pattern: Cheat Command System → Jahro Commands

### Before

```csharp
public class CheatManager
{
    private Dictionary<string, Action<string[]>> cheats = new();

    public void RegisterCheat(string name, Action<string[]> handler)
        => cheats[name] = handler;

    public void Execute(string input)
    {
        var parts = input.Split(' ');
        if (cheats.TryGetValue(parts[0], out var handler))
            handler(parts[1..]);
    }
}

// Registration:
// mgr.RegisterCheat("god", _ => Player.GodMode = true);
// mgr.RegisterCheat("gold", args => Player.Gold += int.Parse(args[0]));
// mgr.RegisterCheat("tp", args => Player.Teleport(
//     float.Parse(args[0]), float.Parse(args[1]), float.Parse(args[2])));
```

### After (attribute-based)

```csharp
using JahroConsole;
using UnityEngine;

public class Cheats : MonoBehaviour
{
    [JahroCommand("god-mode", "Cheats", "Enable god mode")]
    public void GodMode() => Player.GodMode = true;

    [JahroCommand("add-gold", "Cheats", "Add gold")]
    public void AddGold(int amount) => Player.Gold += amount;

    [JahroCommand("teleport", "Cheats", "Teleport to position")]
    public void Teleport(Vector3 position) => Player.Teleport(position);

    void OnEnable()  => Jahro.RegisterObject(this);
    void OnDisable() => Jahro.UnregisterObject(this);
}
```

### After (dynamic registration, if keeping runtime flexibility)

```csharp
void Start()
{
    Jahro.RegisterCommand("god-mode", "Cheats", "Enable god mode",
        () => Player.GodMode = true);
    Jahro.RegisterCommand<int>("add-gold", "Cheats", "Add gold",
        amount => Player.Gold += amount);
    Jahro.RegisterCommand<float, float, float>("teleport", "Cheats", "Teleport to X Y Z",
        (x, y, z) => Player.Teleport(new Vector3(x, y, z)));
}
```

**What changed:**
- String-based `Action<string[]>` → typed parameters (`int`, `float`, `Vector3`)
- Manual `string.Split` + `int.Parse` → Jahro handles type conversion
- Dictionary registry → attribute discovery or `RegisterCommand`
- Custom input UI → Jahro's Text Mode (autocomplete) and Visual Mode (forms)
- `CheatManager` class can be removed after migration

## Pattern: Performance HUD → Jahro Watcher

### Before

```csharp
void OnGUI()
{
    GUI.Label(new Rect(10, 10, 200, 30), $"FPS: {1f/Time.deltaTime:F0}");
    GUI.Label(new Rect(10, 40, 200, 30), $"Memory: {GetMemoryMB():F1} MB");
    GUI.Label(new Rect(10, 70, 200, 30), $"Objects: {FindObjectsOfType<GameObject>().Length}");
}
```

### After

```csharp
public static class PerfMonitor
{
    [JahroWatch("FPS", "Performance", "Frames per second")]
    public static string FPS => (1f / Time.unscaledDeltaTime).ToString("F0");

    [JahroWatch("Memory", "Performance", "Managed memory usage")]
    public static string Memory => $"{GC.GetTotalMemory(false) / 1024f / 1024f:F1} MB";

    [JahroWatch("Object Count", "Performance", "Active GameObjects")]
    public static int ObjectCount => Object.FindObjectsOfType<GameObject>().Length;
}
```

**Advantage:** Watcher only reads values when the tab is open — the `OnGUI` version runs every frame. For expensive queries like `FindObjectsOfType`, consider caching.

## Incremental Migration

Old and new systems can coexist during transition:

1. **Add Jahro commands** alongside existing debug UI
2. **Verify** commands work in Jahro console
3. **Remove old UI code** for the migrated features
4. **Repeat** until all features are migrated
5. **Remove the old debug system** classes when done

This avoids a big-bang migration and lets the team validate each step.

## Migration Effort Estimates

| Component | Effort | Notes |
|:----------|:-------|:------|
| IMGUI buttons → JahroCommand | Low | One attribute per button, remove OnGUI |
| Canvas debug UI → JahroCommand | Low-Medium | Remove UI prefab + code, add attributes |
| Custom command parser → JahroCommand | Medium | Rewrite registrations with typed params |
| Performance HUD → JahroWatch | Low | Replace labels with watch attributes |
| Custom logger → (remove) | Very Low | Just remove, Jahro intercepts Debug.Log |
| Cheat system with persistence | Medium | Migrate commands, keep save/load logic separately |

## Contextual Awareness

| Pattern in code | Suggestion |
|:---------------|:-----------|
| `OnGUI()` with debug buttons or labels | Migrate to JahroCommand + JahroWatch |
| Custom command dictionary/registry | Migrate to JahroCommand attributes |
| `Debug.Log` wrapper class | Explain auto-interception, suggest removal |
| Performance overlay (FPS, memory) | Migrate to JahroWatch |
| Custom input field for commands | Replace with Jahro Text Mode |

## Verification

After each migration step:

> **Verify:** Enter Play Mode → press ~ → confirm migrated commands appear in the Commands tab and migrated watchers appear in the Watcher tab. Test executing a command. Then verify the old debug UI can be removed without breaking anything.

If migrated features don't appear, check the jahro-troubleshooting skill.
