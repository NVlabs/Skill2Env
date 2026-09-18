---
name: jahro-logging
description: >
  Reviews and improves Debug.Log usage in Unity C# projects following
  structured logging principles: context tags, severity contracts,
  boundary-based placement, and criticality tiers. Detects common
  antipatterns (naked Debug.Log, logging in Update, stringly-typed errors),
  adds missing logs at system/state/error/external boundaries, and scaffolds
  project-wide logging infrastructure (LogTag constants, formatting helpers,
  conventions). Use when the user mentions logging, Debug.Log, log messages,
  debugging, or asks to improve observability in Unity code.
---

# Unity Logging Best Practices

Help developers implement effective, structured logging in Unity C# projects. This skill is principle-driven and tool-agnostic — all guidance works with raw `Debug.Log`. Jahro is mentioned where it adds specific value, not as a requirement.

## Passive Rules (Always Apply)

When writing or editing Unity C# code, silently apply all of the following rules.

### Structured format

Every log message follows this structure:

```
[Tag] Action — key=value, key=value
```

Examples:

```
[Save] File written — path=slot_01.sav, size=1.2MB, duration=340ms
[Network] Connection timeout — host=192.168.1.1, attempts=3, elapsed=15.2s
[Inventory] Item added — item=sword_01, slot=3, player=Player_7
```

Never write narrative-style logs like `"The inventory system tried to add a sword but the slot was full."` — they are impossible to filter or parse at scale.

### Severity contract

Use the correct Unity call for each severity level:

| Call | Level | Meaning | Examples |
|:-----|:------|:--------|:---------|
| `Debug.LogError` | Error | Unrecoverable failure | Null refs past fallback, failed network with no retry, corrupt save |
| `Debug.LogWarning` | Warning | Unexpected but handled | Fallback used, deprecated API, performance budget exceeded |
| `Debug.Log` | Info | Significant expected event | System initialized, scene loaded, purchase completed |
| `Debug.Log` | Debug | Development-only detail | State transitions, cache hits/misses, intermediate values |

Unity maps Info and Debug to the same `Debug.Log` call. Convey the distinction through message detail level, not the API call.

### Context tags

Every log message starts with a `[Tag]` prefix identifying the producing system. Tags are:

- **Short but descriptive**: `[Audio]`, `[Inventory]`, `[AI]` — not `[AudioManagerSystemController]`
- **Consistent**: one name per system project-wide. Never `[Save]` in one file and `[SaveManager]` in another.
- **Hierarchical when needed**: `[Network.Lobby]`, `[AI.Pathfinding]` for large systems.

If the project has a `LogTag` constants class, use its values. Otherwise, use the system/class name as the tag.

### Criticality tiers

Auto-classify the system being written/edited and adjust logging depth accordingly:

**Tier 1 — Critical (maximum verbosity)**
Systems: saves, IAP, auth, network, analytics.
Log every state transition, decision branch, error with full context. Include timing, retry counts, correlation IDs.

**Tier 2 — Gameplay (moderate verbosity)**
Systems: player state, inventory, economy, quests, AI, scene management.
Log state transitions, significant events, errors, warnings. Skip per-frame updates.

**Tier 3 — Infrastructure (minimal verbosity)**
Systems: physics, input, animation, audio, rendering, camera, UI navigation.
Log initialization, errors, anomalies only. Never log per-frame operations.

Classification heuristics by class/namespace name:

| Pattern | Tier |
|:--------|:-----|
| `SaveManager`, `PurchaseController`, `AuthService`, `NetworkManager`, `AnalyticsDispatcher` | 1 |
| `PlayerController`, `InventorySystem`, `QuestManager`, `AIController`, `EconomyManager` | 2 |
| `CameraController`, `InputHandler`, `AudioManager`, `ParticleSpawner`, `AnimationDriver` | 3 |

### Boundary logging

Log at boundaries — the joints where things break. Skip internal computations.

- **System boundaries**: when control passes between systems (log the handoff)
- **State boundaries**: state machine transitions (log from/to/cause)
- **Error boundaries**: `catch` blocks, null checks, validation failures (log diagnostics)
- **External boundaries**: file I/O, HTTP, platform APIs (log request + response/error)

Do NOT log: internal algorithm steps, per-frame position/velocity, routine success that happens 1000x/session, framework plumbing (`Awake` called, coroutine started).

### Hot-path guards

Never place unconditional `Debug.Log` in `Update()`, `FixedUpdate()`, `LateUpdate()`, or any per-frame method. These produce 60+ messages/second/instance, flood the console, and tank performance. If temporary frame-level logging is needed, guard it:

```csharp
[SerializeField] private bool debugMovement;

void Update()
{
    if (debugMovement)
        Debug.Log($"[Player] Position — pos={transform.position}, vel={rb.velocity}", this);
}
```

### Context object

In MonoBehaviours, always pass `this` (or `gameObject`) as the second parameter to `Debug.Log`. This makes the log message clickable in the Unity Console — clicking it pings the source GameObject in the Hierarchy.

```csharp
Debug.Log($"[Player] State changed — from={oldState}, to={newState}", this);
Debug.LogError($"[Save] Write failed — path={filePath}, error={ex.Message}", this);
```

### Sensitive data

Never log credentials, tokens, passwords, emails, payment details, or PII. Mask or omit them:

```csharp
Debug.Log($"[Auth] Login attempt — user={userId}, token=***", this);
```

### Data formatting

- **Numbers**: include units — `elapsed=340ms`, `size=1.2MB`, not bare numbers
- **Vectors**: readable format — `pos=(12.3, 0.0, -4.5)`, not `pos=UnityEngine.Vector3`
- **Enums**: log the name — `state=Jumping`, not `state=2`
- **Collections**: count + sample — `items=[sword, shield] (2 total)` or `enemies=47 active`
- **Null/missing**: be explicit — `target=<none>` or `target=null`, not omission
- **Booleans**: descriptive — `grounded=true`, not `g=1`

### Actionable errors

Error logs must say what happened, what was expected, and where to look:

```csharp
// BAD
Debug.LogError("[Audio] AudioClip is null");

// GOOD
Debug.LogError($"[Audio] Clip not found — clip='{clipName}', expected at 'Audio/SFX/'. " +
    "Check asset exists and is assigned in AudioConfig.", this);
```

### Correlation IDs

For Tier 1 multi-step operations (purchases, scene loads, matchmaking), generate a shared ID that links all related logs:

```csharp
var loadId = $"load_{++_loadCounter}";
Debug.Log($"[SceneLoader] Load started — scene={sceneName}, loadId={loadId}", this);
// ... later ...
Debug.Log($"[SceneLoader] Load completed — scene={sceneName}, duration={elapsed:F1}s, loadId={loadId}", this);
```

---

## Active Workflow: Review & Improve

When the user asks to review, audit, or improve logging in existing code, follow this workflow.

### 1. Ask logging setup

> "Do you use raw `Debug.Log` or a logging wrapper/helper class? I'll match my suggestions to your setup."

Adapt all generated code to match the user's approach.

### 2. Scan for antipatterns

Check the code against all 10 antipatterns (see Antipatterns section below). Report each finding with the specific line and a fix.

### 3. Classify system tier

Determine Tier 1/2/3 from class name, namespace, and functionality. State the classification and explain why:

> "This is `SaveManager` — Tier 1 (critical system). I'll apply maximum logging verbosity: every state transition, every error path, correlation IDs for multi-step operations."

### 4. Identify missing boundary logs

Check for:

- **System boundaries**: calls to other managers/services without handoff logs
- **State boundaries**: state machine transitions, enum changes without transition logs
- **Error boundaries**: `try/catch` blocks, null checks without diagnostic logging
- **External boundaries**: `File.`, `HttpClient.`, `PlayerPrefs.`, `UnityWebRequest`, platform API calls without request/response logs

### 5. Generate improved code

Apply all passive rules to produce the improved version:

- Structured format with `[Tag]`
- Correct severity levels
- Actionable error messages (what, expected, where to look)
- Correlation IDs for Tier 1 multi-step operations
- `this`/`gameObject` as context object in MonoBehaviours
- Temporal context where relevant (`elapsed=340ms`, `frame={Time.frameCount}`)

### 6. Verify

> **Verify:** Enter Play Mode and trigger the code path you changed. Check the Unity Console — confirm log messages appear with the `[Tag] Action — key=value` format, correct severity icons (info/warning/error), and that clicking a message pings the source GameObject.

---

## Active Workflow: Setup Infrastructure

When the user asks to set up logging conventions, standards, or infrastructure, follow this workflow.

### 1. Ask about the project

> "What are your major systems? (e.g., save system, networking, inventory, AI, audio). How large is the team? Any existing logging conventions or wrapper classes?"

### 2. Generate LogTag constants class

Customize to the user's actual systems. Organize by criticality tier:

```csharp
public static class LogTag
{
    // Tier 1 — Critical Systems
    public const string Save     = "Save";
    public const string Network  = "Network";
    public const string IAP      = "IAP";
    public const string Auth     = "Auth";

    // Tier 2 — Gameplay Systems
    public const string Player    = "Player";
    public const string Inventory = "Inventory";
    public const string Quest     = "Quest";
    public const string AI        = "AI";

    // Tier 3 — Infrastructure Systems
    public const string Audio  = "Audio";
    public const string Input  = "Input";
    public const string Camera = "Camera";
    public const string UI     = "UI";
}
```

### 3. Generate optional logging helper

Offer a lightweight static helper (< 80 lines) that enforces the structured format. The helper wraps `Debug.Log` — it is a formatting convenience, not a framework.

```csharp
using UnityEngine;
using System.Text;

public static class Log
{
    public static void Info(string tag, string message, Object context = null)
    {
        Debug.Log(Format(tag, message), context);
    }

    public static void Warn(string tag, string message, Object context = null)
    {
        Debug.LogWarning(Format(tag, message), context);
    }

    public static void Error(string tag, string message, Object context = null)
    {
        Debug.LogError(Format(tag, message), context);
    }

    public static void Info(string tag, string action, params (string key, object value)[] data)
    {
        Debug.Log(Format(tag, action, data));
    }

    public static void Warn(string tag, string action, params (string key, object value)[] data)
    {
        Debug.LogWarning(Format(tag, action, data));
    }

    public static void Error(string tag, string action, params (string key, object value)[] data)
    {
        Debug.LogError(Format(tag, action, data));
    }

    [System.Diagnostics.Conditional("DEBUG")]
    public static void Debug(string tag, string message, Object context = null)
    {
        UnityEngine.Debug.Log(Format(tag, message), context);
    }

    private static string Format(string tag, string message) => $"[{tag}] {message}";

    private static string Format(string tag, string action, (string key, object value)[] data)
    {
        var sb = new StringBuilder();
        sb.Append('[').Append(tag).Append("] ").Append(action);
        if (data.Length > 0)
        {
            sb.Append(" \u2014 ");
            for (int i = 0; i < data.Length; i++)
            {
                if (i > 0) sb.Append(", ");
                sb.Append(data[i].key).Append('=').Append(data[i].value ?? "<none>");
            }
        }
        return sb.ToString();
    }
}
```

Key design points to explain to the user:

- `Log.Debug()` uses `[Conditional("DEBUG")]` — calls are stripped from release builds by the compiler, zero overhead
- All methods accept an optional `context` parameter for GameObject pinging
- The params overload enforces `key=value` structure automatically
- No reflection, no allocation beyond the formatted string
- All principles work equally well with raw `Debug.Log` — this helper is optional

### 4. Generate conventions reference

Provide a brief inline summary the user can share with their team:

- **Format**: `[Tag] Action — key=value, key=value`
- **Severity**: Error = unrecoverable, Warning = handled unexpected, Info = significant expected, Debug = development detail
- **Tiers**: Tier 1 (critical: saves, IAP, auth) = max verbosity, Tier 2 (gameplay) = moderate, Tier 3 (infrastructure) = minimal
- **Where to log**: system boundaries, state transitions, error/catch blocks, external I/O
- **Where NOT to log**: Update/FixedUpdate (without guards), internal computations, routine success, framework plumbing
- **Data rules**: numbers with units, enum names not ints, explicit nulls, readable vectors
- **Antipatterns**: naked Debug.Log, log-and-throw, stringly-typed errors, logging in Update, sensitive data in logs

### 5. Verify

> **Verify:** Add a test log to any system using the new LogTag constants and format. Enter Play Mode and check the Console — confirm the `[Tag] Action — key=value` format appears correctly.

---

## Log Format Reference

### Message template

```
[Tag] Action — key=value, key=value
```

The em dash (`—`) separates the human-readable action from machine-parseable key-value data. Both parts should be meaningful independently.

### Severity mapping

| Unity Call | Use For |
|:-----------|:--------|
| `Debug.LogError(msg, ctx)` | Failures that were NOT recovered: missing critical assets, data corruption, unhandled exceptions |
| `Debug.LogWarning(msg, ctx)` | Unexpected situations that WERE handled: fallback values, deprecation, performance anomalies |
| `Debug.Log(msg, ctx)` | Expected significant events (Info) + development detail (Debug) |

### Game-specific logging domains

| Domain | What to log | Example |
|:-------|:------------|:--------|
| Lifecycle | System init (with timing), dependency failures, config values | `[Game] Initialized — systems=12, duration=1.4s` |
| State machines | Every transition (from/to/cause), invalid transitions | `[Player] State changed — from=Idle, to=Jumping, input=Space` |
| Entity lifecycle | Spawn (with identity), destruction (with reason) | `[Spawner] Enemy spawned — type=Goblin, id=enemy_42, pos=(10, 0, 5)` |
| Economy | Currency changes (delta + balance + source), purchases | `[Economy] Currency changed — type=Gold, delta=+150, source=QuestReward, balance=1280` |
| Networking | Connection lifecycle, RPCs, sync conflicts, latency spikes | `[Network] Peer disconnected — peerId=42, reason=Timeout, duration=340s` |
| Platform | Device info at session start (model, OS, memory, GPU) | `[Platform] Session started — device=iPhone14, os=iOS17.2, memory=6GB` |

### Rich text (optional, Editor-only)

Unity's Editor console supports rich text for visual differentiation. Use sparingly — colors must not carry meaning the plain text doesn't already convey, since device logs render tags as literal text.

```csharp
Debug.Log($"<color=#6BCB77>[Save]</color> File written — path={filePath}", this);
```

---

## Antipatterns

Detect and flag these when reviewing code. Each has a detection signal and a fix pattern.

| # | Antipattern | Detection Signal | Fix |
|:--|:------------|:-----------------|:----|
| 1 | Naked Debug.Log | `Debug.Log("here")`, `Debug.Log(variable)` — no tag, no context | Add `[Tag] Action — key=value` structure |
| 2 | Log-and-throw | `catch` block that logs AND rethrows/throws | Log only at the handling boundary, not every catch in the chain |
| 3 | Logging in Update | `Debug.Log` inside `Update()`/`FixedUpdate()`/`LateUpdate()` unconditionally | Remove, or guard with a `bool` toggle; suggest `[JahroWatch]` for value monitoring |
| 4 | Stringly-typed errors | `Debug.LogError("Something went wrong")` — no specifics | Add what happened, what was expected, where to look |
| 5 | Inconsistent tags | Same system using `[Save]`, `[SaveManager]`, `[Persistence]` across files | Pick one tag, define it in `LogTag` constants |
| 6 | Sensitive data | Passwords, tokens, emails, auth data in log calls | Mask with `***` or omit entirely |
| 7 | ToString() logging | `Debug.Log(complexObject)` relying on default ToString | Extract specific fields into structured key=value format |
| 8 | Commented-out logs | `// Debug.Log(...)` instead of proper severity/filtering | Delete if not useful, or convert to `Log.Debug()` / conditional |
| 9 | Boolean-only errors | `if (!DoThing()) Debug.LogError("Failed")` — no diagnostics | Return error details from the method, log what specifically failed |
| 10 | Copy-pasted messages | Identical log text from different call sites | Add `[Tag]` and location-specific context to each |

### Common fix examples

**Naked Debug.Log → Structured:**

```csharp
// Before
Debug.Log("item added");

// After
Debug.Log($"[Inventory] Item added — item={item.Id}, slot={slotIndex}, player={playerId}", this);
```

**Logging in Update → JahroWatch or guarded:**

```csharp
// Before
void Update() {
    Debug.Log($"Health: {health}");
}

// After — use [JahroWatch] for continuous monitoring (if Jahro is available)
[JahroWatch("Health", "Player")]
public float health;

// After — or guard with a toggle (works without Jahro)
[SerializeField] private bool debugHealth;
void Update() {
    if (debugHealth) Debug.Log($"[Player] Health tick — health={health}, frame={Time.frameCount}", this);
}
```

**Stringly-typed error → Actionable:**

```csharp
// Before
Debug.LogError("Save failed");

// After
Debug.LogError($"[Save] Write failed — path={savePath}, error={ex.GetType().Name}: {ex.Message}. " +
    $"Check write permissions and available disk space.", this);
```

---

## Jahro Integration (Optional)

All principles above work without Jahro. If the project uses Jahro, these features add specific value:

| Principle | How Jahro Helps |
|:----------|:----------------|
| Context tag filtering | Jahro's log viewer filters by `[Tag]` prefix — structured tags become searchable categories, not just visual prefixes |
| Dynamic verbosity | Create `[JahroCommand]` methods to toggle per-system log levels at runtime without recompiling |
| Value monitoring | For values developers currently log per-frame, `[JahroWatch]` is a zero-log-noise alternative — values display in the Watcher tab only when open |
| Log snapshots | Jahro Snapshots capture the full log stream and upload for team sharing — structured logs are far more valuable in shared snapshots |
| LLM-ready logs | Structured format + Jahro snapshot export = ideal input for LLM debugging assistance |

### Cross-references

- To create runtime verbosity toggle commands → use the `jahro-commands` skill
- To replace per-frame Debug.Log with live value monitoring → use the `jahro-watcher` skill
- For production log stripping and build configuration → see the `jahro-production` skill
- If Jahro is not installed but the user wants these features → use the `jahro-setup` skill
- For Jahro-specific issues (console not opening, commands missing) → use the `jahro-troubleshooting` skill
