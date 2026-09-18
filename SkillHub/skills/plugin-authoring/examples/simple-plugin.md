# Example: Simple Plugin

This example shows a minimal but complete Claude Code plugin.

## Directory Structure

```
my-greeting-plugin/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   └── greet.md
└── README.md
```

## plugin.json

```json
{
  "name": "my-greeting-plugin",
  "version": "1.0.0",
  "description": "A simple greeting plugin",
  "author": {
    "name": "Your Name"
  },
  "license": "MIT",
  "keywords": ["greeting", "example"]
}
```

**Note**: No `commands` field needed since we're using the standard `commands/` directory.

## commands/greet.md

```markdown
---
description: Greet the user with a personalized message
argument-hint: [name]
---

# Greet Command

Provide a warm, friendly greeting to the user.

## Instructions

1. If the user provided a name via `$ARGUMENTS`, greet them personally
2. If no name provided, use a generic friendly greeting
3. Add a fun emoji to make it welcoming

## Examples

**Input**: `/my-greeting-plugin:greet Alice`
**Output**: "Hello, Alice! 👋 Great to see you!"

**Input**: `/my-greeting-plugin:greet`
**Output**: "Hello there! 👋 How can I help you today?"
```

## README.md

```markdown
# My Greeting Plugin

A simple example plugin that demonstrates Claude Code plugin basics.

## Installation

From a marketplace:
```bash
/plugin install my-greeting-plugin@marketplace-name
```

## Usage

```bash
/my-greeting-plugin:greet [name]
```

## Examples

- `/my-greeting-plugin:greet World` - Greet with a name
- `/my-greeting-plugin:greet` - Generic greeting
```

## Adding to a Marketplace

In your marketplace's `.claude-plugin/marketplace.json`:

```json
{
  "plugins": [
    {
      "name": "my-greeting-plugin",
      "description": "A simple greeting plugin",
      "version": "1.0.0",
      "author": {
        "name": "Your Name"
      },
      "source": "./plugins/my-greeting-plugin",
      "category": "examples",
      "tags": ["greeting", "example"]
    }
  ]
}
```

## Testing Locally

1. Create the plugin structure
2. Create a dev marketplace:
   ```bash
   mkdir -p dev-marketplace/.claude-plugin
   ```
3. Create `dev-marketplace/.claude-plugin/marketplace.json` (see above)
4. Add marketplace:
   ```bash
   /plugin marketplace add ./dev-marketplace
   ```
5. Install plugin:
   ```bash
   /plugin install my-greeting-plugin@dev-marketplace
   ```
6. Test command:
   ```bash
   /my-greeting-plugin:greet World
   ```

## Key Takeaways

- **Minimal structure**: Only `.claude-plugin/plugin.json` and `commands/` are required
- **Frontmatter**: Commands need `description` (and optionally `argument-hint`)
- **Namespacing**: Commands are called with `/plugin-name:command-name`
- **Arguments**: Access via `$ARGUMENTS` or `$1`, `$2`, etc.
- **Standard paths**: No need to specify component fields in `plugin.json` when using standard directories
