# lsp-impact: Reference Patterns

Supplementary reference for the lsp-impact skill. Contains the canonical
Impact Report format, capability check patterns, position_pattern examples,
and the relationship between lsp-impact and lsp-edit-export.

---

## 1. Impact Report Format

Use this format when producing the output in Step 5 of lsp-impact:

```
## Impact Report: SymbolName

- Kind:         function | method | type | interface | class | ...
- Definition:   path/to/file.go:line:column
- References:   N across M files

### Direct References
- path/to/file1.go  lines: 12, 45
- path/to/file2.go  line: 3

### Callers (find_callers incoming)
<call tree listing, or "not supported by this server">

### Type Hierarchy
Supertypes: <list or "not applicable (function)">
Subtypes:   <list or "not applicable (function)">

### Blast Radius Summary
- Total files affected: M
- Distinct callers: N
- Risk level: low | medium | high
```

**Risk level thresholds:**

| References | Risk level |
|---|---|
| 0 | dead code (verify before deleting) |
| 1–5 files | low |
| 6–20 files | medium |
| > 20 files | high |

---

## 2. Capability Check Pattern

`find_callers` and `type_hierarchy` are optional LSP features. Not all
language servers implement them.

Always call `get_server_capabilities()` before attempting these tools. Check
the `supported_tools` list in the response:

```
mcp__lsp__get_server_capabilities()
→ {
    supported_tools: ["go_to_symbol", "find_references", "find_callers", ...],
    unsupported_tools: ["type_hierarchy", ...]
  }
```

**If `find_callers` is not in `supported_tools`:** skip Step 3 entirely.
In the Impact Report, write:
```
### Callers (find_callers incoming)
not supported by this server
```

**If `type_hierarchy` is not in `supported_tools`:** skip Step 4 entirely.
In the Impact Report, write:
```
### Type Hierarchy
Supertypes: not supported by this server
Subtypes:   not supported by this server
```

Do **not** error or abort when a feature is unsupported — gracefully skip
and document the gap in the report.

---

## 3. position_pattern Examples for find_references

The `@@` marker places the cursor immediately before the first character of
the symbol name. Use these patterns for common language constructs:

**Go — top-level function:**
```
"func @@FunctionName("
```

**Go — type declaration:**
```
"type @@TypeName struct"
```
or for interface:
```
"type @@InterfaceName interface"
```

**Go — method on a receiver:**
```
"func (r *ReceiverType) @@MethodName("
```
or use the shorter form if the receiver prefix is ambiguous:
```
") @@MethodName("
```

**TypeScript — exported function:**
```
"export function @@functionName("
```

**TypeScript — exported class:**
```
"export class @@ClassName"
```

**Python — class definition:**
```
"class @@ClassName:"
```

**Python — function/method:**
```
"def @@function_name("
```

**Rust — public function:**
```
"pub fn @@function_name("
```

**Rust — public struct:**
```
"pub struct @@StructName"
```

**Fallback:** If `position_pattern` is not supported by your MCP client,
use the explicit `line` and `column` fields returned by `go_to_symbol` in
Step 1 instead.

### LineScope: Restricting to a Line Range

When the same token appears multiple times in a file, add `line_scope_start`
and `line_scope_end` to restrict the search:

```
"position_pattern": "func @@FunctionName(",
"line_scope_start": 40,
"line_scope_end": 60
```

Use the line number from `go_to_symbol` (Step 1) as an anchor:
`line_scope_start: symbol_line - 5, line_scope_end: symbol_line + 5`.
Omitting both args preserves full-file search for all existing callers.

---

## 4. Relationship to lsp-edit-export

`lsp-impact` and `lsp-edit-export` are complementary skills designed to be
used together in sequence:

| Skill | Purpose | Modifies files? |
|---|---|---|
| `lsp-impact` | Read-only blast-radius analysis | No |
| `lsp-edit-export` | Safe write workflow with confirmation gate | Yes |

**Recommended order:**

1. Run `lsp-impact` first — understand the full scope of what would change
   (reference count, affected files, callers, type relationships).
2. Decide whether to proceed based on the risk level.
3. Run `lsp-edit-export` to execute the change safely — it discovers callers,
   asks for confirmation, applies the edit, and verifies the build.

Running impact before edit-export prevents surprises: you know exactly how
many files to update before you commit to the change. This is especially
important at medium and high blast radii where missed callers cause build
failures or silent regressions.
