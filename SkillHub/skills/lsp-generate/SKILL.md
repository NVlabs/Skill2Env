---
name: lsp-generate
description: Trigger language server code generation — implement interface stubs, generate test skeletons, add missing methods, generate mock types. Uses suggest_fixes to surface generator options and execute_command to run them.
argument-hint: "[file-path:line:col] [generation-intent]"
user-invocable: true
allowed-tools: mcp__lsp__suggest_fixes mcp__lsp__execute_command mcp__lsp__apply_edit mcp__lsp__format_document mcp__lsp__get_diagnostics mcp__lsp__open_document mcp__lsp__get_server_capabilities mcp__lsp__go_to_symbol
license: MIT
compatibility: Requires the agent-lsp MCP server (github.com/blackwell-systems/agent-lsp)
metadata:
  required-capabilities: codeActionProvider
  optional-capabilities: workspaceSymbolProvider documentFormattingProvider
---

> Requires the agent-lsp MCP server.

# lsp-generate

**lsp-generate creates NEW code that does not yet exist in the file** — stubs,
mocks, implementations of interfaces, test functions. It is distinct from
`lsp-extract-function`, which restructures code that already exists. Use
`lsp-generate` when you want the language server to write something new; use
`lsp-extract-function` when you want to reorganize existing code.

## Input

- **`file_path`**: absolute path to the target file
- **`line`, `column`** (or **`position_pattern`**): position in the file where
  generation is triggered (e.g., the line with the unimplemented interface,
  the missing method error, the type declaration)
- **`intent`**: description of what to generate (e.g., "implement io.Reader",
  "generate test skeleton", "add missing methods", "generate mock for Handler")

## Prerequisites

LSP must be running for the target workspace. If not yet initialized, call
`mcp__lsp__start_lsp` with the workspace root before proceeding.

Auto-init note: agent-lsp supports workspace auto-inference from file paths.
Explicit `start_lsp` is only needed when switching workspace roots.

---

## Workflow

### Step 1 — Open document and locate position

Call `mcp__lsp__open_document` for the target file:

```
mcp__lsp__open_document(file_path: "/abs/path/to/file.go", language_id: "go")
```

If using `position_pattern`, use the @@ marker convention from
`references/patterns.md` to identify the exact cursor position. For example:

```
"position_pattern": "var _ io.Reade@@r = (*MyType)(nil)"
```

### Step 2 — Get code actions at target position

```
mcp__lsp__suggest_fixes({
  "file_path": "...",
  "start_line": N,
  "start_column": C,
  "end_line": N,
  "end_column": C
})
```

Filter for generator actions:
- Kind `"quickfix"` with titles matching the intent (e.g., "Implement
  interface", "Generate", "Add stub", "Create test")
- Kind `"source"` for source-level generation

If no matching action is found, report "No generator action available at this
position for the given intent" and proceed to the Fallback section below.

### Step 3 — Select and confirm action

Display available generator actions to the user. If multiple actions match the
intent, list all of them and ask which to apply. Confirm the selected action
before executing — do NOT auto-select when multiple candidates exist.

### Step 4 — Execute generator

Execute one generator at a time. Do NOT batch multiple `execute_command` calls.

- If the action has a `command` field: run via `mcp__lsp__execute_command`
- If the action has an `edit` field: apply via `mcp__lsp__apply_edit`
- If the action has both: apply the edit first, then run the command

### Step 5 — Format and verify

```
mcp__lsp__format_document({ "file_path": "..." })
mcp__lsp__get_diagnostics({ "file_path": "..." })
```

Report remaining diagnostics. Stub methods typically leave TODO comments or
`panic("not implemented")` bodies — this is expected behavior from the language
server. Surface any unexpected errors.

---

## Per-Language Generator Patterns

| Language | Generator | Trigger location | Code action kind |
|----------|-----------|-----------------|-----------------|
| Go (gopls) | Implement interface | Line with `var _ MyInterface = (*MyType)(nil)` or type declaration | `quickfix` — "Implement interface" |
| Go (gopls) | Generate test file | Any .go file without _test.go counterpart | `source` — "Generate unit tests" |
| Go (gopls) | Add missing method | Line with `undefined: method` error | `quickfix` |
| TypeScript (typescript-language-server) | Implement interface | Class declaration | `quickfix` — "Implement interface members" |
| TypeScript (typescript-language-server) | Add missing method | Method call with no definition | `quickfix` — "Add missing function declaration" |
| Python (pyright) | Add import | Name not defined | `quickfix` — "Add import" |
| Rust (rust-analyzer) | Implement trait | `impl Trait for Type {}` | `quickfix` — "Add missing impl members" |

---

## Fallback When No Code Action Is Available

If `suggest_fixes` returns no generator actions, the language server at this
workspace may not support server-side generation for this intent. Explain this
to the user and suggest a manual approach specific to the intent:

- **Interface implementation:** Look up the interface definition first using
  `mcp__lsp__go_to_symbol` to discover all required methods, then implement
  them manually.
- **Test skeleton:** Check `mcp__lsp__get_server_capabilities` to confirm
  whether the server advertises code action support; if not, generate the test
  skeleton manually using standard testing package conventions.
- **Missing methods:** Use `mcp__lsp__get_diagnostics` to enumerate the missing
  symbols by name, then implement them one at a time.

---

## Constraints

- Do NOT batch `execute_command` calls — run one generator at a time
- Do NOT skip user confirmation when multiple generator actions are available
