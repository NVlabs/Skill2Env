# Move Code Quality Checker - Claude Code Skill

A Claude Code skill that analyzes Move language packages against the official [Move Book Code Quality Checklist](https://move-book.com/guides/code-quality-checklist/), helping you write better, more maintainable Move code.

## Overview

This skill extends Claude Code with deep knowledge of Move language best practices, providing:

- **Automated code quality analysis** against 10+ categories of best practices
- **Specific, actionable recommendations** with examples from the Move Book
- **Move 2024 Edition compliance checking**
- **Package manifest validation**
- **Function signature and structure analysis**
- **Testing best practices review**

## What It Checks

The skill analyzes your Move code across multiple dimensions:

1. **Code Organization** - Formatting consistency
2. **Package Manifest** - Edition requirements, dependencies, named addresses
3. **Imports & Modules** - Modern syntax, naming conventions
4. **Structs** - Capability patterns, event naming, dynamic fields
5. **Functions** - Visibility modifiers, composability, parameter ordering
6. **Function Bodies** - Method chaining, string operations, collections
7. **Option & Loop Macros** - Modern idiomatic patterns
8. **Testing** - Attribute usage, assertions, cleanup patterns
9. **Documentation** - Comment quality and completeness

## Installation

### From Claude Code

```bash
# Clone to your Claude skills directory
git clone https://github.com/1NickPappas/move-code-quality-skill ~/.claude/skills/move-code-quality
```

### Manual Installation

1. Create the skills directory if it doesn't exist:
   ```bash
   mkdir -p ~/.claude/skills
   ```

2. Clone or copy this skill to the skills directory:
   ```bash
   cd ~/.claude/skills
   git clone https://github.com/1NickPappas/move-code-quality-skill
   ```

3. Claude Code will automatically load the skill when working with Move code

## Usage

The skill activates automatically when you're working with Move code. You can also explicitly invoke it:

```
Analyze this Move package for code quality issues
```

```
Review this module against the Move code quality checklist
```

```
Check if this code follows Move 2024 best practices
```

## Examples

The skill provides specific feedback based on the Move Book examples:

- **Before**: `use my_package::{Self};`
- **After**: `use my_package;`
- **Reason**: Avoid redundant Self imports

- **Before**: `public entry fun transfer(...)`
- **After**: `public fun transfer(...)`
- **Reason**: Public functions are more composable for PTBs

## Requirements

- Claude Code CLI
- Move 2024 Edition projects
- Basic familiarity with Move language

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Resources

- [Move Book Code Quality Checklist](https://move-book.com/guides/code-quality-checklist/)
- [Move Language Documentation](https://move-language.github.io/move/)
- [Claude Code Skills Documentation](https://docs.claude.com/claude-code)

## Acknowledgments

This skill is based on the comprehensive code quality guidelines from [The Move Book](https://move-book.com/) by the Move community.
