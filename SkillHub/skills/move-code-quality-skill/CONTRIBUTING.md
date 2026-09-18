# Contributing to Move Code Quality Checker

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Code of Conduct

This project adheres to a Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected behavior** vs actual behavior
- **Code samples** demonstrating the issue
- **Environment details** (OS, Claude Code version, Move version)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear use case** - Why is this enhancement useful?
- **Detailed description** of the proposed functionality
- **Examples** of how it would work
- **Alternative approaches** you've considered

### Pull Requests

1. **Fork** the repository
2. **Create a branch** from `main` with a descriptive name:
   - `feature/add-new-check`
   - `fix/parsing-error`
   - `docs/improve-readme`
3. **Make your changes** following our coding standards
4. **Test your changes** thoroughly
5. **Commit** with clear, descriptive messages (see below)
6. **Push** to your fork
7. **Open a Pull Request** with a clear description

## Commit Message Guidelines

We follow conventional commit format for clear git history:

```
<type>: <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

### Examples

```
feat: add parameter ordering validation

Implements check for proper Move function parameter ordering:
objects first, capabilities second, primitives, Clock, and
TxContext last. Includes examples from Move Book.

Closes #42
```

```
fix: handle edge case in module name parsing

Module names with underscores were incorrectly flagged.
Updated regex pattern to properly match valid identifiers.
```

```
docs: add examples for common issues

Added before/after code samples for the top 5 most
common issues found in Move codebases.
```

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/move-code-quality-skill.git
   cd move-code-quality-skill
   ```

2. Link to Claude Code skills directory:
   ```bash
   ln -s $(pwd) ~/.claude/skills/move-code-quality
   ```

3. Test your changes with Claude Code

## Skill Structure

```
move-code-quality-skill/
├── SKILL.md              # Main skill definition
├── checklist/            # Detailed checklist rules
│   ├── organization.md
│   ├── manifest.md
│   ├── functions.md
│   └── ...
├── examples/             # Example Move code
│   ├── bad/
│   └── good/
└── tests/               # Test cases
```

## Adding New Checks

When adding a new code quality check:

1. **Reference the Move Book** - Include the source URL
2. **Provide examples** - Both bad and good patterns
3. **Explain the why** - Not just what's wrong, but why it matters
4. **Test thoroughly** - Include test cases
5. **Update documentation** - Add to README and SKILL.md

## Style Guidelines

### Markdown

- Use ATX-style headers (`#` not `===`)
- One sentence per line in paragraphs
- Code blocks must specify language
- Use relative links for internal references

### Code Examples

- Keep examples minimal and focused
- Include comments explaining the issue
- Show both incorrect and correct versions
- Use realistic Move code patterns

## Testing

Before submitting a PR:

1. Test the skill with various Move packages
2. Verify all checklist items are working
3. Ensure examples are accurate
4. Check that documentation is up to date

## Questions?

Feel free to open an issue for:
- Questions about contributing
- Clarification on guidelines
- Discussion of potential changes

## Recognition

Contributors will be acknowledged in:
- README.md contributors section
- Release notes
- GitHub contributors page

Thank you for contributing to better Move code quality!
