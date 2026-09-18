---
name: jahro-watcher
description: >
  Analyzes C# fields and properties and generates [JahroWatch] attributes
  with groups and performance-safe patterns. Use when the user wants to
  monitor variables at runtime, add watchers, track game state, replace
  Debug.Log polling, or mentions JahroWatch, real-time inspection, or
  variable monitoring.
---

# Jahro Watcher

Help users monitor game variables in real-time using Jahro's `[JahroWatch]` attribute system.

## Workflow

1. **Analyze** the user's code — identify fields/properties worth monitoring
2. **Generate** correct `[JahroWatch]` attributes
3. **Add registration** if needed (instance members require `RegisterObject`)
4. **VERIFY** — "Enter Play Mode, open the Watcher tab, confirm values update"

## Analyzing Code for Watcher Candidates

When the user shares a class, identify members worth monitoring:

**Good candidates:**
- Game state fields: health, score, level, currency, inventory counts
- Physics values: velocity, position, rotation (especially via properties wrapping Rigidbody)
- Performance metrics: FPS, memory, draw calls
- Enum state fields: game state, player state, AI state
- Key counters: enemy count, player count, item count

**Skip these:**
- Constants and readonly compile-time values
- Private implementation details that change every frame with no debugging value
- References to other objects (Transform, GameObject) — watch their properties instead
- Collections and dictionaries (arrays are supported, but dictionaries are not)

**Suggest replacing Debug.Log polling:**
If the user has `Debug.Log($"Health: {health}")` in `Update()`, recommend `[JahroWatch]` instead — it eliminates log spam and provides a clean real-time dashboard.

## Attribute Syntax

```csharp
[JahroWatch("Display Name", "GroupName", "Description for detail modal")]
```

Constructor: `[JahroWatch(string name, string group, string description)]`

All parameters are optional. Defaults: name = member name (leading `_` stripped), group = "Default", description = "".

### Complete example

```csharp
using JahroConsole;
using UnityEngine;

public class PlayerController : MonoBehaviour
{
    [JahroWatch("Health", "Player", "Current hit points")]
    public float health = 100f;

    [JahroWatch("Stamina", "Player", "Current stamina")]
    public float stamina = 50f;

    [JahroWatch("Position", "Player", "World position")]
    public Vector3 Position => transform.position;

    [JahroWatch("Velocity", "Player", "Movement velocity")]
    public Vector3 Velocity => GetComponent<Rigidbody>().velocity;

    [JahroWatch("Is Grounded", "Player", "Touching ground")]
    public bool isGrounded;

    void OnEnable()  => Jahro.RegisterObject(this);
    void OnDisable() => Jahro.UnregisterObject(this);
}
```

## Registration

### Instance members — require RegisterObject

```csharp
void OnEnable()  => Jahro.RegisterObject(this);
void OnDisable() => Jahro.UnregisterObject(this);
```

This same call also registers `[JahroCommand]` attributes on the class. If the class already has `RegisterObject` for commands, do not add a second call — one call handles both.

Read `references/common-patterns.md` for the canonical lifecycle pattern.

### Static members — no registration needed

Static fields and properties with `[JahroWatch]` are discovered via assembly scanning:

```csharp
public static class GameStats
{
    [JahroWatch("Total Score", "Game")]
    public static int Score;

    [JahroWatch("Session Time", "Game")]
    public static float SessionTime => Time.realtimeSinceStartup;
}
```

### Adding watchers to a class that already has commands

If the class already has `[JahroCommand]` attributes and `RegisterObject`, just add `[JahroWatch]` attributes — no registration changes:

```csharp
public class GameManager : MonoBehaviour
{
    // Existing command
    [JahroCommand("reset-game", "Game", "Reset game")]
    public void ResetGame() { /* ... */ }

    // New watchers — just add attributes
    [JahroWatch("Player Count", "Game")]
    public int playerCount;

    [JahroWatch("Game Time", "Game")]
    public float gameTime;

    // Already present — no changes needed
    void OnEnable()  => Jahro.RegisterObject(this);
    void OnDisable() => Jahro.UnregisterObject(this);
}
```

## Supported Types

| Type | List View Display | Detail Modal |
|:-----|:-----------------|:-------------|
| `int`, `float`, `double`, `bool` | Value as-is | Same |
| `string` | Truncated | Full text |
| `Vector2` | Compact coords | Coords + magnitude |
| `Vector3` | Compact coords | Coords + magnitude |
| `Quaternion` | Raw values | Raw + Euler angles |
| `Transform` | Position | Position, rotation, scale, child count |
| `Rigidbody` | Summary | Mass, kinematic, gravity, velocity, angular velocity |
| `Collider` | Summary | Trigger status, material, bounds |
| `AudioSource` | Summary | Clip, volume, loop, pitch, mute |
| `Camera` | Summary | FOV, clip planes, aspect ratio |
| Arrays (any `T[]`) | `TypeName[length]` | Full contents |

For custom types not in this table, the watcher calls `.ToString()`. If you need rich display, consider watching individual primitive properties instead.

Read `references/api-reference.md` for the full type display details.

## Performance

Watchers are designed to be safe for development and testing:

- **Values are only read when the Watcher UI tab is visible.** No continuous polling when the console is closed or on another tab.
- **No overhead when disabled.** If Jahro is disabled via `JAHRO_DISABLE` or auto-disable, watchers are never evaluated.
- **Be mindful of expensive property getters.** A property like `public int Count => expensiveList.Where(...).Count()` runs its getter every frame the Watcher is open. Cache expensive computations.

### Performance-safe property pattern

```csharp
private float _cachedFps;
private float _lastFpsUpdate;

void Update()
{
    if (Time.time - _lastFpsUpdate > 0.25f)
    {
        _cachedFps = 1f / Time.unscaledDeltaTime;
        _lastFpsUpdate = Time.time;
    }
}

[JahroWatch("FPS", "Performance")]
public float FPS => _cachedFps;
```

## Group Organization

### By system (recommended default)

```
"Player"      — Health, Stamina, Position, Velocity
"Physics"     — Is Grounded, Angular Velocity, Collision Count
"Performance" — FPS, Memory, Draw Calls
"Game"        — Game State, Level Progress, Player Count
"AI"          — AI State, Target, Path Length
```

### By priority

```
"Critical"    — Health, Frame Time (always need these)
"Gameplay"    — Enemy Count, Spawn Timer
"Diagnostics" — GC Allocs, Memory
```

### Watcher UI behavior

- **Favorites** group always appears at top (user stars individual watchers)
- Custom groups are alphabetically sorted
- Groups are collapsible to reduce clutter
- Tapping a watcher opens a detail modal with description and full type info

## Contextual Awareness

| Pattern in code | Suggestion |
|:---------------|:-----------|
| `Debug.Log` in `Update()` logging variable values | Replace with `[JahroWatch]` — cleaner, no log spam |
| `[JahroWatch]` already present | Suggest additional watchers, better groups, performance tips |
| `[JahroCommand]` but no watchers | Suggest adding watchers for key state the commands modify |
| Rigidbody or physics-heavy code | Suggest velocity, angular velocity, isGrounded watchers |
| Game manager with state fields | Suggest watching game state enum, counts, timers |

## Verification

After generating watchers, always include:

> **Verify:** Enter Play Mode → press ~ → switch to the **Watcher** tab. Confirm your watched values appear in the correct groups and update in real-time as the game runs. Tap a watcher to see its detail modal.

If watchers appear but don't update, or don't appear at all, suggest the jahro-troubleshooting skill — common causes: missing RegisterObject, Watcher tab not open, object destroyed without unregistering.
