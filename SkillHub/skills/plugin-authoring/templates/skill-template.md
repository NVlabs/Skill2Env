---
name: skill-name
description: What the Skill does and WHEN to use it (third person). Be specific about triggers. Cannot contain XML tags.
# model: claude-sonnet-4-6  # Optional: Specify model to use (defaults to conversation's model)
# allowed-tools: Read, Grep, Glob  # Optional: Tools listed don't require permission when Skill is active
---

<!--
SKILL.md Frontmatter Reference:
- name: (required) lowercase letters, numbers, hyphens only. Max 64 chars. Must match directory name.
        Cannot contain reserved words 'anthropic' or 'claude'. Cannot contain XML tags.
- description: (required) Max 1024 chars. Cannot contain XML tags.
- model: (optional) e.g., claude-sonnet-4-6. Defaults to conversation's model.
- allowed-tools: (optional) Comma-separated. Tools listed auto-approved when Skill active.

Best Practice: Keep SKILL.md under 500 lines for optimal performance.
-->

# Skill Name

[Brief introduction to what this Skill provides]

## Purpose

[Explain the Skill's role and capabilities]

## When to Activate

[Describe specific contexts or patterns that should trigger this Skill]

Examples:
- When the user mentions [specific topic]
- When files matching [pattern] are present
- When working with [technology/framework]

## Capabilities

[What this Skill can help with]

1. [Capability 1]
2. [Capability 2]
3. [Capability 3]

## Quick Links

[Link to sibling files for progressive disclosure]

- [Reference 1](./reference1.md)
- [Reference 2](./reference2.md)

## Workflow

[Step-by-step approach this Skill follows]

1. [Analyze/Read relevant files]
2. [Propose actions]
3. [Execute via commands or provide guidance]

## Notes

[Any constraints, best practices, or important information]
