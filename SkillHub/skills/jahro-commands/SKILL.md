---
name: jahro-commands
description: >
  Analyzes C# classes and generates [JahroCommand] attributes with correct
  syntax, RegisterObject patterns, and group organization. Use when the
  user wants to add runtime commands, cheats, or debug actions to Unity
  classes, or mentions JahroCommand, console commands, runtime cheats,
  or debug actions.
---

# Jahro Commands

Help users add runtime-callable debug commands to Unity code using Jahro's `[JahroCommand]` attribute system.

## Workflow

1. **Analyze** the user's code — identify methods that are good command candidates
2. **Generate** correct `[JahroCommand]` attributes with proper syntax
3. **Add registration** if needed (instance methods require `RegisterObject`)
4. **VERIFY** — "Enter Play Mode, press ~, check the Commands tab"

## Analyzing Code for Command Candidates

When the user shares a class, identify methods worth exposing as commands:

**Good candidates:**
- Public methods that change game state (damage, heal, spawn, teleport, reset)
- Methods used for testing and tuning (set difficulty, add currency, skip level)
- Diagnostic methods (print stats, dump state, force GC)
- Methods with simple parameter types (int, float, bool, string, Vector2, Vector3, enum)

**Skip these:**
- Unity lifecycle methods (Update, Start, Awake, OnEnable, OnDisable, OnDestroy)
- Private implementation details the developer wouldn't want to call manually
- Methods with complex parameter types (custom classes, interfaces, delegates)
- Property getters/setters (use `[JahroWatch]` for monitoring instead)

## Attribute Syntax

```csharp
[JahroCommand("command-name", "GroupName", "Short description of what it does")]
```

Constructor: `[JahroCommand(string name, string group, string description)]`

All parameters are optional. Defaults: name = method name, group = "Default", description = "".

### Naming conventions

- **Command name**: kebab-case (`"spawn-enemy"`, `"add-gold"`, `"set-difficulty"`)
- **Group name**: PascalCase or Title Case (`"Cheats"`, `"Spawning"`, `"Game"`)
- **Description**: Imperative, concise (`"Spawn enemy at position"`, `"Add gold to player"`)

### Complete example

```csharp
using JahroConsole;
using UnityEngine;

public class PlayerController : MonoBehaviour
{
    public float health = 100f;

    [JahroCommand("heal", "Player", "Restore health by amount")]
    public void Heal(float amount) { health = Mathf.Min(health + amount, 100f); }

    [JahroCommand("teleport", "Player", "Teleport to position")]
    public void Teleport(Vector3 position) { transform.position = position; }

    [JahroCommand("reset-pos", "Player", "Reset to origin")]
    public void ResetPosition() { transform.position = Vector3.zero; }

    void OnEnable()  => Jahro.RegisterObject(this);
    void OnDisable() => Jahro.UnregisterObject(this);
}
```

## Registration Pattern

### Instance methods — require RegisterObject

Any non-static method with `[JahroCommand]` needs the owning object registered so Jahro can invoke it:

```csharp
void OnEnable()  => Jahro.RegisterObject(this);
void OnDisable() => Jahro.UnregisterObject(this);
```

This same call also registers `[JahroWatch]` attributes on the class. If the class already has RegisterObject (e.g., for watchers), do not add a second call.

Read `references/common-patterns.md` for the full lifecycle pattern and anti-patterns.

### Static methods — no registration needed

Static methods are discovered via assembly scanning:

```csharp
public class DebugCommands
{
    [JahroCommand("restart-level", "Game", "Restart current level")]
    public static void RestartLevel()
    {
        UnityEngine.SceneManagement.SceneManager.LoadScene(0);
    }
}
```

### Decision guide

| Method type | Needs RegisterObject? | Why |
|:------------|:---------------------|:----|
| `public void Foo()` (instance) | Yes | Jahro needs the object reference to call it |
| `public static void Foo()` | No | Called on the class, discovered via assembly scan |
| `public void Foo()` on a class that already has RegisterObject | No extra work | Already registered |

## Supported Parameter Types

Commands accept these parameter types:

| Type | Text Mode input | Visual Mode input |
|:-----|:---------------|:-----------------|
| `int` | `42` | Number field |
| `float` | `3.14` | Decimal field |
| `bool` | `true` / `false` | Toggle switch |
| `string` | `hello world` | Text field |
| `Vector2` | `1.5 2.0` | X/Y fields |
| `Vector3` | `10 2.5 -7` | X/Y/Z fields |
| `enum` (any) | `Hard` (name) | Dropdown selector |

Maximum 3 parameters per command. For full type details, read `references/api-reference.md`.

## Command Overloads

Same command name with different parameter signatures:

```csharp
[JahroCommand("spawn-enemy", "Spawning", "Spawn one enemy at position")]
public void SpawnEnemy(Vector3 position) { /* ... */ }

[JahroCommand("spawn-enemy", "Spawning", "Spawn N enemies")]
public void SpawnEnemy(int count) { /* ... */ }
```

Text Mode resolves the correct overload by parameter count and type conversion.

## Return Values

Commands that return `string` display the result in the console log:

```csharp
[JahroCommand("get-pos", "Debug", "Print player position")]
public static string GetPlayerPosition()
{
    return $"Position: {Player.Instance.transform.position}";
}
```

## Dynamic Command Registration

For commands created at runtime instead of compile time. Use when wrapping external APIs, creating commands from data, or in non-MonoBehaviour systems.

```csharp
// No parameters
Jahro.RegisterCommand("clear-cache", "Maintenance", "Clear local cache",
    () => PlayerPrefs.DeleteAll());

// One typed parameter
Jahro.RegisterCommand<int>("add-gold", "Cheats", "Add gold",
    amount => Player.Gold += amount);

// Two parameters
Jahro.RegisterCommand<int, float>("set-stats", "Tuning", "Set health and speed",
    (health, speed) => { Player.Health = health; Player.Speed = speed; });
```

**Parameter order for dynamic registration:** `(name, description, groupName, callback)`.
This differs from the attribute order `(name, group, description)`.

Register command on existing object method:

```csharp
var mgr = FindObjectOfType<GameManager>();
Jahro.RegisterCommand("restart", "Game", "Restart level",
    mgr, nameof(GameManager.RestartLevel));
```

Cleanup:

```csharp
Jahro.UnregisterCommand("clear-cache");
Jahro.UnregisterCommand("restart", "Game");
```

Read `references/api-reference.md` for all `RegisterCommand` overloads (0-3 generic parameters).

## Command Organization

### Group naming strategy

Organize commands by functional area:

```
"Player"    — heal, teleport, reset, set-speed
"Spawning"  — spawn-enemy, spawn-wave, clear-enemies
"Cheats"    — god-mode, add-gold, unlock-all
"Game"      — restart-level, set-difficulty, skip-level
"Debug"     — dump-state, gc-collect, toggle-fps
```

### Visual Mode vs Text Mode

Commands work in both modes automatically. Consider the target audience:

- **Text Mode** — fast for developers who know command names. Autocomplete helps. Vector3 entered as `10 2.5 -7`.
- **Visual Mode** — browsable groups with descriptions, form-based parameter input. Touch-friendly on mobile. Enum parameters render as dropdown selectors.

When designing commands for QA (non-developers), prefer:
- Simple parameter types (bool, enum, int) over Vector3
- Descriptive names and descriptions
- Logical groups that match QA workflows

### Favorites and Recent

Users can star frequently-used commands for quick access. The last 10 executed commands always appear in the Recent section. Command names and groups help discoverability — be descriptive.

## Contextual Awareness

When you see these patterns in user code, proactively suggest:

| Pattern in code | Suggestion |
|:---------------|:-----------|
| `[JahroCommand]` already present | Offer improvements (better groups, descriptions, missing commands) |
| `OnGUI()` with `GUI.Button` debug commands | Migrate to `[JahroCommand]` — Visual Mode replaces the button UI |
| Public methods that modify game state | Suggest exposing as commands |
| Custom command parser (string → command) | Migrate to Jahro's typed command system |

## Verification

After generating commands, always include:

> **Verify:** Enter Play Mode → press ~ → switch to the Commands tab (or Visual Mode). Confirm your commands appear in the correct groups. Try executing one to confirm it works.

If commands don't appear, suggest the jahro-troubleshooting skill — common causes: missing RegisterObject, wrong assembly selected, JAHRO_DISABLE active.
