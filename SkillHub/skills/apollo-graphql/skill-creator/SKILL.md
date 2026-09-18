---
name: skill-creator
description: >
  Guide for creating effective skills for Apollo GraphQL and GraphQL development. Use this skill when:
  (1) users want to create a new skill,
  (2) users want to update an existing skill,
  (3) users ask about skill structure or best practices,
  (4) users need help writing SKILL.md files.
license: MIT
compatibility: Works with Claude Code and similar AI coding assistants that support Agent Skills.
metadata:
  author: apollographql
  version: "1.1.0"
allowed-tools: Read Write Edit Glob Grep
---

# Skill Creator Guide

This guide helps you create effective skills for Apollo GraphQL and GraphQL development following the [Agent Skills specification](https://agentskills.io/specification).

## What is a Skill?

A skill is a directory containing instructions that extend an AI agent's capabilities with specialized knowledge, workflows, or tool integrations. Skills activate automatically when agents detect relevant tasks.

## Directory Structure

A skill requires at minimum a `SKILL.md` file:

```
skill-name/
├── SKILL.md              # Required - main instructions
├── references/           # Optional - detailed documentation
│   ├── topic-a.md
│   └── topic-b.md
├── scripts/              # Optional - executable helpers
│   └── validate.sh
├── templates/            # Optional - config/code templates
│   └── config.yaml
└── assets/               # Optional - static resources (images, schemas, data files)
```

## SKILL.md Format

### Frontmatter (Required)

```yaml
---
name: skill-name
description: >
  A clear description of what this skill does and when to use it.
  Include trigger conditions: (1) first condition, (2) second condition.
license: MIT
compatibility: Works with Claude Code and similar AI coding assistants.
metadata:
  author: your-org
  version: "1.0.0"
allowed-tools: Read Write Edit Glob Grep
---
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Lowercase, hyphens only. Must match directory name. Max 64 chars. |
| `description` | Yes | What the skill does and when to use it. Max 1024 chars. |
| `license` | No | License name (e.g., MIT, Apache-2.0). |
| `compatibility` | No | Environment requirements. Max 500 chars. |
| `metadata` | No | Key-value pairs for author, version, etc. |
| `allowed-tools` | No | Space-delimited list of pre-approved tools. Do not include `Bash(curl:*)`. |

### Name Rules

- Use lowercase letters, numbers, and hyphens only
- Do not start or end with a hyphen
- Do not use consecutive hyphens (`--`)
- Must match the parent directory name

Good: `apollo-client`, `graphql-schema`, `rover`
Bad: `Apollo-Client`, `-apollo`, `apollo--client`

### Description Best Practices

Write descriptions that help agents identify when to activate the skill:

```yaml
# Good - specific triggers and use cases
description: >
  Guide for designing GraphQL schemas following industry best practices. Use this skill when:
  (1) designing a new GraphQL schema or API,
  (2) reviewing existing schema for improvements,
  (3) deciding on type structures or nullability,
  (4) implementing pagination or error patterns.

# Bad - vague and unhelpful
description: Helps with GraphQL stuff.
```

## Body Content

The markdown body contains instructions the agent follows. Structure it for clarity:

### Recommended Sections

1. **Overview** - Brief explanation of the skill's purpose
2. **Process** - Step-by-step workflow (use checkboxes for multi-step processes)
3. **Quick Reference** - Common patterns and syntax
4. **Security** - Risks, mitigations, and validation (if the skill touches anything security-sensitive)
5. **Reference Files** - Links to detailed documentation
6. **Key Rules** - Important guidelines organized by topic
7. **Ground Rules** - Critical do's and don'ts

### Example Structure

```markdown
# Skill Title

Brief overview of what this skill helps with.

## Process

Follow this process when working on [task]:

- [ ] Step 1: Research and understand requirements
- [ ] Step 2: Implement the solution
- [ ] Step 3: Validate the result

## Quick Reference

### Common Pattern

\`\`\`graphql
type Example {
  id: ID!
  name: String
}
\`\`\`

## Security

> **Risk: [brief description of what can go wrong].**
> [What the user MUST do to prevent it.]

- ALWAYS [secure default behavior]
- NEVER [dangerous configuration] in production

## Reference Files

- [Topic A](references/topic-a.md) - Detailed guide for topic A
- [Topic B](references/topic-b.md) - Detailed guide for topic B

## Key Rules

### Category One

- Rule about this category
- Another rule

### Category Two

- Rule about this category

## Ground Rules

- ALWAYS do this important thing
- NEVER do this problematic thing
- PREFER this approach over that approach
```

## Security-Sensitive Content

When a skill generates configuration, code, or guidance that could cause security issues if misused, the skill MUST make those risks explicit and visible to the LLM. An LLM cannot infer security implications from context alone — it needs clearly labeled signals.

### When does a skill need security guidance?

If any of these apply, the skill is security-sensitive:

- Generates config that controls access to data (caching, auth, CORS, permissions)
- Handles secrets, credentials, or tokens
- Produces code that runs with elevated privileges
- Controls what data is shared, public, or exposed to users
- Configures network bindings, endpoints, or external access

### How to surface security in a skill

1. **Dedicated Security section** in SKILL.md or a reference file, labeled `## Security`. Not "Private data" or "Customization" — use the word "Security" so the LLM recognizes the category.

2. **Explicit warnings at the point of risk** — place security guidance next to the config or code that creates the risk, not in a separate file the LLM may not load:

   ```markdown
   ### Response caching scope

   > **Security: data leakage risk.** All cached data is PUBLIC by default.
   > User-specific fields MUST use `scope: PRIVATE` with a `private_id`
   > configured, or they will be shared across all users.
   ```

3. **Validation checklist items** — every security-sensitive feature must have corresponding checks in the validation checklist. Group them under a `## Security` heading.

4. **Ground rules** — add ALWAYS/NEVER rules for security-critical behavior. These are the strongest signal to the LLM.

5. **Require the data model** — if correct security configuration depends on understanding the user's data model (e.g., which fields are user-specific), the skill must instruct the LLM to ask the user before generating config. Do not let the LLM guess.

### Anti-patterns

- Describing a security-sensitive default (like "public by default") without labeling it as a security concern
- Placing security guidance only in reference files that load on demand — the SKILL.md itself must contain the key warnings
- Using soft language ("you may want to consider") for hard security requirements — use "MUST" and "NEVER"
- Assuming the LLM understands which fields in a schema are private — require explicit user input

## Progressive Disclosure

Structure skills to minimize context usage:

1. **Metadata** (~100 tokens): `name` and `description` load at startup for all skills
2. **Instructions** (< 5000 tokens): Full `SKILL.md` loads when skill activates
3. **References** (as needed): Files in `references/` load only when required

Keep `SKILL.md` under 500 lines. Move detailed documentation to reference files.

## Reference Files

Use `references/` for detailed documentation:

```
references/
├── setup.md          # Installation and configuration
├── patterns.md       # Common patterns and examples
├── troubleshooting.md # Error solutions
└── api.md            # API reference
```

Reference files should be:

- Focused on a single topic
- Self-contained (readable without other files)
- Under 300 lines each

Link to references from `SKILL.md`:

```markdown
## Reference Files

- [Setup](references/setup.md) - Installation and configuration
- [Patterns](references/patterns.md) - Common patterns and examples
```

## Scripts

Use `scripts/` for executable helpers agents can run:

```
scripts/
├── validate.sh       # Validation commands
├── setup.py          # Setup automation
└── check-version.sh  # Version checking
```

Scripts should be self-contained, include error handling, and have a usage comment at the top. Pre-approve them in `allowed-tools` (e.g., `Bash(./scripts/validate.sh:*)`).

## Templates

Use `templates/` for config files, boilerplate, or starter code:

```
templates/
├── config.yaml       # Default configuration
├── config-v2.yaml    # Version-specific variant
└── example-app/      # Starter project
```

Templates are copied or adapted by the agent — not executed directly.

## Writing Style

Follow the Apollo Voice for all skill content:

### Tone

- Approachable and helpful
- Opinionated and authoritative (prescribe the "happy path")
- Direct and action-oriented

### Language

- Use American English
- Keep language simple; avoid idioms
- Use present tense and active voice
- Use imperative verbs for instructions

### Formatting

- Use sentence casing for headings
- Use code font for symbols, commands, file paths, and URLs
- Use bold for UI elements users click
- Use hyphens (-) for unordered lists

### Avoid

- "Simply", "just", "easy" (can be condescending)
- Vague phrases like "click here"
- Semicolons (use periods instead)
- "We" unless clearly referring to Apollo

## Reference Files

For Apollo GraphQL-specific guidance:

- [Apollo Skills](references/apollo-skills.md) - Patterns and examples for Apollo GraphQL skills

## Versioning

Use semantic versioning (`"X.Y.Z"`) for the `version` field in metadata:

```yaml
metadata:
  author: apollographql
  version: "1.0.0"
```

- **Major (X)**: Breaking changes that alter how the skill behaves or activates (e.g., renamed triggers, removed sections, changed ground rules)
- **Minor (Y)**: New content or capabilities that are backward-compatible (e.g., added reference files, new sections, expanded examples)
- **Patch (Z)**: Small fixes that don't change behavior (e.g., typo corrections, wording tweaks, formatting fixes)

Start new skills at `"1.0.0"`.

## Checklist for New Skills

Before publishing a skill, verify:

- [ ] `name` matches directory name and follows naming rules
- [ ] `description` clearly states what the skill does and when to use it
- [ ] `SKILL.md` is under 500 lines
- [ ] Reference files are focused and under 300 lines each
- [ ] Instructions are clear and actionable
- [ ] Code examples are correct and tested
- [ ] Ground rules use ALWAYS/NEVER/PREFER format
- [ ] Content follows Apollo Voice guidelines

## Ground Rules

- ALWAYS include trigger conditions in the description (use numbered list)
- ALWAYS use checkboxes for multi-step processes
- ALWAYS link to reference files for detailed documentation
- NEVER exceed 500 lines in SKILL.md
- NEVER use vague descriptions that don't help agents identify when to activate
- PREFER specific examples over abstract explanations
- PREFER opinionated guidance over listing multiple options
- USE `allowed-tools` to pre-approve tools the skill needs
- NEVER include `Bash(curl:*)` in `allowed-tools` as it grants unrestricted network access and enables `curl | sh` remote code execution patterns
- ALWAYS include a `## Security` section when the skill generates config or code that controls access, caching, auth, secrets, or data exposure
- NEVER bury security-critical guidance only in reference files — the key warnings must appear in SKILL.md where the LLM will always see them
- ALWAYS instruct the LLM to ask the user about their data model before generating security-sensitive config (e.g., which fields are user-specific, which data is public)
- USE explicit blockquote warnings (`> **Security: ...**`) next to config or code that creates security risks
- ALWAYS add validation checklist items for every security-sensitive feature, grouped under a `## Security` heading
