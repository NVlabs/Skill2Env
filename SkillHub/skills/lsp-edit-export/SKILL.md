---
name: lsp-edit-export
description: Safe workflow for editing exported symbols or public APIs. Use when changing a function signature, modifying a public type, or altering any symbol used outside its own package — finds all callers first so nothing breaks silently.
argument-hint: "[symbol-name]"
user-invocable: true
allowed-tools: mcp__lsp__go_to_symbol mcp__lsp__open_document mcp__lsp__find_references mcp__lsp__get_diagnostics mcp__lsp__run_build mcp__lsp__replace_symbol_body Edit Write
license: MIT
compatibility: Requires the agent-lsp MCP server (github.com/blackwell-systems/agent-lsp)
metadata:
  required-capabilities: referencesProvider
  optional-capabilities: workspaceSymbolProvider
---

> Requires the agent-lsp MCP server.

# lsp-edit-export

Safe workflow for editing exported symbols. Always discovers all callers before
touching any code, then verifies the change is clean.

## When to Use

Use this skill whenever you intend to change the signature, name, or behavior of
an **exported symbol**: a symbol visible outside its defining package or module.

**Language-specific definitions:**

| Language   | Exported means...                                                      |
|------------|------------------------------------------------------------------------|
| Go         | Identifier starts with an uppercase letter (e.g. `MyFunc`, `MyType`)  |
| TypeScript | Has `export` keyword; or is a public class member (no `private`)       |
| Python     | Not prefixed with `_`; or explicitly listed in `__all__`               |
| Java/C#    | Has `public` or `protected` visibility modifier                        |
| Rust       | Has `pub` keyword                                                      |

If you are unsure whether a symbol is exported, treat it as exported and run
this workflow anyway. The cost is a few extra tool calls; the benefit is never
breaking a hidden caller.

**Do NOT skip this workflow** even when you believe there are zero callers.
The confirmation gate in step 3 exists precisely for that case.

## Workflow

**If LSP is not yet initialized**, call `mcp__lsp__start_lsp` with the
workspace root first. (agent-lsp supports auto-inference from file paths, so
explicit start is only required when switching workspaces or on a cold session.)

### Step 1 — Locate the symbol

Use `go_to_symbol` to find the symbol's definition by name, without needing to
know its file path or line number in advance:

```
mcp__lsp__go_to_symbol({
  "symbol_path": "PackageName.ExportedFunction",
  "workspace_root": "/abs/path/to/repo"   // optional, narrows scope
})
```

`symbol_path` uses dot notation. For a top-level function `Encode` in package
`codec`, use `"codec.Encode"`. For a method `Reset` on type `Buffer`, use
`"Buffer.Reset"`. The last component is the leaf name; any prefix is used to
disambiguate when multiple symbols share the same leaf.

The tool returns a `FormattedLocation` with the definition file and 1-indexed
line/column. Record this position — you will need it in step 2.

### Step 2 — Discover all callers

Call `find_references` using the `position_pattern` field to express the cursor
position as a readable text pattern rather than raw coordinates. The `@@` marker
indicates exactly where the cursor sits (the character immediately after `@@`):

```
mcp__lsp__find_references({
  "file_path": "<definition file from step 1>",
  "position_pattern": "func @@ExportedFunction(",
  "include_declaration": false
})
```

The `@@` must immediately precede the first character of the symbol name.
Examples:

- `"func @@Encode("` — Go function declaration
- `"type @@Buffer struct"` — Go type declaration
- `"export function @@parse("` — TypeScript function
- `"class @@Parser:"` — Python class
- `"pub fn @@process("` — Rust function

If `position_pattern` is unavailable on your MCP client, fall back to the
`line` and `column` fields from the location returned in step 1.

The tool returns a list of reference locations across the codebase.

### Step 3 — Confirmation gate (REQUIRED — never skip)

Before making any change, present the impact summary to the user and ask for
explicit confirmation. This gate is mandatory even when the caller count is zero.

Format the gate as follows:

```
## Impact Check: <SymbolName>

- Definition: <file>:<line>
- Callers found: N reference(s) in M file(s)

Files with callers:
  - <file1>
  - <file2>
  ...

Proceed with the edit? [y/n]
```

If the user answers **n**, stop. Do not make any edits.

If the user answers **y**, proceed to step 4.

**Why this gate exists even for 0 callers:** the LSP index may be incomplete
(e.g. files not yet saved, workspace not fully loaded). Zero callers is a data
point, not a guarantee.

### Step 4 — Make the edit

Apply your intended change using `Edit` or `Write`. When replacing a complete
function or method body, `replace_symbol_body` is an option that resolves the
symbol by name and replaces its full range without position math:

```
mcp__lsp__replace_symbol_body({
  "file_path": "<definition file>",
  "symbol_path": "ExportedFunction",
  "new_body": "<new full definition>"
})
```

For other edits (signature changes, partial modifications), use `Edit` or `Write`.
Follow the standard edit workflow for the language. If renaming, update all call
sites identified in step 2 as well; do not leave broken callers.

Collect diagnostics **before** the edit so you have a baseline for comparison
in step 5:

```
mcp__lsp__get_diagnostics({
  "file_path": "<definition file>"
})
```

Then apply the edit and collect diagnostics again after.

### Step 5 — Check diagnostics

Compare before and after diagnostic snapshots using the format in
[references/patterns.md](references/patterns.md).

If new errors appear, fix them before proceeding. Do not run the build with
known diagnostic errors outstanding.

### Step 6 — Run the build

```
mcp__lsp__run_build({
  "workspace_root": "/abs/path/to/repo"
})
```

A clean build confirms no compilation errors across all affected packages.
If the build fails, diagnose using the error output and diagnostic data from
step 5. Fix and re-run until the build passes.

### Step 7 — Report

Emit the final output block:

```
## Edit Summary
- Symbol: <name> (<kind>)
- Callers found: N in M files
- Diagnostics: net +N/-N
- Build: PASSED / FAILED
```

If build is FAILED, include the first 3–5 error lines and a brief diagnosis.

## Example

```
Goal: rename exported function `ParseConfig` → `LoadConfig` in pkg/config

Step 1 — go_to_symbol: symbol_path="config.ParseConfig"
  → pkg/config/parser.go:42:6

Step 2 — find_references: position_pattern="func @@ParseConfig("
  → 7 references in 4 files

Step 3 — gate:
  ## Impact Check: ParseConfig
  - Definition: pkg/config/parser.go:42
  - Callers found: 7 in 4 files
  Files: cmd/main.go, internal/app.go, internal/loader.go, pkg/config/parser_test.go
  Proceed? [y/n] → y

Step 4 — edit: rename declaration + all 7 call sites

Step 5 — diagnostics: net 0 (no new errors)

Step 6 — build: PASSED

Step 7 — report:
  ## Edit Summary
  - Symbol: LoadConfig (function)
  - Callers found: 7 in 4 files
  - Diagnostics: net 0
  - Build: PASSED
```

## Note on position_pattern

`position_pattern` with `@@` is a agent-lsp extension. If your MCP client
or server does not support it, fall back to explicit `line` and `column`
parameters from the location returned by `go_to_symbol` in step 1.
