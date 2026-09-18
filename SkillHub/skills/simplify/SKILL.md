---
name: simplify
description: Review code for unnecessary complexity and simplify it. Use when the user wants to clean up code, reduce complexity, remove dead code, or make code more readable.
allowed-tools: Bash, Read, Grep, Glob, Edit, Write
---

# Code Simplification

Review the specified code (or recent changes) for unnecessary complexity and simplify it.

## What to look for

1. **Over-abstraction** — helpers, utilities, or wrapper functions used only once. Inline them.
2. **Unnecessary indirection** — callback chains, event buses, or service layers that just pass data through.
3. **Defensive overkill** — error handling for impossible cases, null checks deep inside trusted internal code.
4. **Dead code** — unused imports, unreachable branches, commented-out blocks, unused variables.
5. **Complex conditionals** — nested if/else that could be early returns, switch statements that could be lookups.
6. **Premature generalization** — config objects for one use case, plugin systems with one plugin, factory patterns for one type.
7. **Redundant comments** — comments that restate the code instead of explaining why.

## Principles

- Three similar lines of code are better than a premature abstraction
- Delete code rather than add it when possible
- If removing something breaks nothing, it shouldn't have been there
- The right amount of complexity is the minimum needed for the current requirements
- Don't design for hypothetical future requirements

## Process

1. Read the target files
2. For each issue found, explain what's overly complex and why it can be simplified
3. Show the simplified version
4. Apply the fix
5. Verify the changes don't break anything (run tests if available)

$ARGUMENTS
