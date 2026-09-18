---
name: lsp-extract-function
description: Extract a selected code block into a named function. Primary path uses the language server's extract-function code action; falls back to manual extraction when no code action is available. Validates captured variables, scope shadowing, and compilation after extraction.
argument-hint: "[file-path] [start-line] [end-line] [new-function-name]"
user-invocable: true
allowed-tools: mcp__lsp__list_symbols mcp__lsp__suggest_fixes mcp__lsp__execute_command mcp__lsp__apply_edit mcp__lsp__get_diagnostics mcp__lsp__open_document mcp__lsp__format_document mcp__lsp__get_server_capabilities
license: MIT
compatibility: Requires the agent-lsp MCP server (github.com/blackwell-systems/agent-lsp)
metadata:
  required-capabilities: codeActionProvider
  optional-capabilities: documentFormattingProvider documentSymbolProvider
---

> Requires the agent-lsp MCP server.

# lsp-extract-function: Extract Code Block into a Named Function

**This skill RESTRUCTURES existing code** — it takes code that already exists
and moves it into a new function. This is distinct from `/lsp-generate`, which
creates NEW code that does not yet exist (stubs, mocks, interface implementations).
Use this skill when the code is already written; use `/lsp-generate` when you
need to generate code from scratch.

**Invocation:** User provides `file_path` (absolute path), `start_line` and
`end_line` (1-indexed range), and `new_function_name` (desired name for the
extracted function).

---

## Prerequisites

If LSP is not yet initialized, call `mcp__lsp__start_lsp` with the workspace
root first. Auto-inference applies when file paths are provided, but an explicit
start is required when switching workspaces.

---

## Step 1 — Get context (document symbols)

Call `mcp__lsp__open_document` to open the file, then call
`mcp__lsp__list_symbols` to understand the containing function and scope:

```
mcp__lsp__open_document({ "file_path": "<file_path>" })
mcp__lsp__list_symbols({ "file_path": "<file_path>" })
```

This establishes:
- Which function contains the selection
- Whether `new_function_name` already exists in the file (name collision check)

**Mandatory name collision check:** If `new_function_name` already exists as a
symbol in the document symbols list, report the conflict and stop immediately:

> Cannot extract: function `new_function_name` already exists in this file.
> Choose a different name and retry.

---

## Step 2 — Check server capabilities

Call `mcp__lsp__get_server_capabilities` to understand what the language server
supports:

```
mcp__lsp__get_server_capabilities({})
```

Check for `codeActionProvider` in the response. Note whether `execute_command`
is listed in `executeCommandProvider.commands`. This determines whether the
primary path (Step 3) is available.

---

## Step 3 — Primary path: LSP code action

Call `mcp__lsp__suggest_fixes` with the selection range:

```
mcp__lsp__suggest_fixes({
  "file_path": "<file_path>",
  "start_line": N,
  "start_column": 1,
  "end_line": M,
  "end_column": 999
})
```

Filter the returned actions for extract-function actions: include any action
whose `kind` contains `"refactor.extract"` OR whose `title` contains both
"Extract" and "function" (case-insensitive).

**If an extract-function action is found:**
- Display the action title to the user
- If the action proposes a different name than `new_function_name`, ask for
  confirmation before proceeding
- Execute via `mcp__lsp__execute_command` if the action has a `command` field:
  ```
  mcp__lsp__execute_command({
    "command": "<action.command.command>",
    "arguments": <action.command.arguments>
  })
  ```
- OR apply directly via `mcp__lsp__apply_edit` if the action has an `edit` field:
  ```
  mcp__lsp__apply_edit({ "workspace_edit": <action.edit> })
  ```
- Skip to Step 5 after applying.

**If no extract-function action is found:** fall through to Step 4 (manual fallback).

---

## Step 4 — Manual fallback

When no code action is available, perform manual extraction:

### a) Analyze the selection

Read the selected lines (`start_line` through `end_line`) and identify:
- **Parameters:** Variables used inside the selection that are declared outside
  (captured from outer scope — must become function parameters)
- **Return values:** Variables declared inside the selection that are used outside
  (must be returned from the extracted function)
- **Early returns:** Return statements inside the selection (the extracted function
  must wrap these)

### b) Construct and confirm the proposed signature

Build the extracted function signature based on the captured variables analysis.
Display the proposed signature to the user before writing:

> Proposed extraction:
> ```
> func new_function_name(param1 Type1, param2 Type2) (ReturnType, error) {
>     // selected lines
> }
> ```
> Proceed with this signature? [y/n]

Wait for user confirmation before applying any edit.

### c) Apply the extraction (order matters)

Apply edits sequentially — do NOT batch edits from different line regions into a
single `apply_edit` call:

1. **First:** Replace the selected lines with a call to the new function:
   ```
   mcp__lsp__apply_edit({
     "workspace_edit": {
       "changes": {
         "<file_path>": [{
           "range": { "start": { "line": start_line-1, "character": 0 },
                      "end":   { "line": end_line,     "character": 0 } },
           "newText": "    result := new_function_name(args...)\n"
         }]
       }
     }
   })
   ```

2. **Second:** Insert the new function definition after the containing function's
   closing brace:
   ```
   mcp__lsp__apply_edit({
     "workspace_edit": {
       "changes": {
         "<file_path>": [{
           "range": { "start": { "line": insert_line, "character": 0 },
                      "end":   { "line": insert_line, "character": 0 } },
           "newText": "\nfunc new_function_name(params) ReturnType {\n    ...\n}\n"
         }]
       }
     }
   })
   ```

Apply call-site replacement first, then insert the new function. This order
preserves line numbers during editing: replacing call site does not shift the
insertion point for the new function definition.

---

## Step 5 — Validate

After extraction via either path:

### 1. Check diagnostics

```
mcp__lsp__get_diagnostics({ "file_path": "<file_path>" })
```

If errors are reported, display them with the table of common causes below.

### 2. Common post-extraction errors

| Error type | Likely cause | Fix |
|------------|--------------|-----|
| Undefined variable | Captured var not passed as parameter | Add parameter |
| Type mismatch | Return type inferred incorrectly | Adjust return type in signature |
| Name shadows outer | New function name matches outer scope | Choose different name |
| Unused variable | Return value not captured at call site | Add variable at call site |

### 3. Format the document

```
mcp__lsp__format_document({ "file_path": "<file_path>" })
```

This cleans up indentation introduced by the extraction.

---

## Output Format

After completing extraction, display:

```
## Extraction Summary
- File:           path/to/file.go
- Extracted:      lines N–M
- New function:   new_function_name
- Path used:      LSP code action / Manual fallback
- Post-extraction errors: 0
```

Follow with the Diagnostic Summary if any errors changed (format in
[references/patterns.md](references/patterns.md)).

---

## Language-Specific Notes

- **Go:** gopls may offer "Extract function" in code actions for selection ranges.
  Check code actions first; gopls support varies by version.
- **TypeScript/JavaScript:** typescript-language-server may offer "Extract to function in global scope"
  or "Extract to inner function" — filter for these titles in Step 3.
- **Python:** pylsp and pyright-langserver typically do NOT offer extract-function
  code actions. Manual fallback (Step 4) is required for Python files.
