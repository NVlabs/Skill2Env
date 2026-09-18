---
name: web-design-guidelines
description: Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", or "check my site against best practices".
---

# Web Interface Guidelines

Review files for compliance with Web Interface Guidelines.

## How It Works

1. Fetch the latest guidelines from the source URL below
2. Read the specified files (or prompt user for files/pattern)
3. Check against all rules in the fetched guidelines
4. Output findings in the terse `file:line` format

## Guidelines Source

Fetch fresh guidelines before each review:

```
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

Use WebFetch to retrieve the latest rules. The fetched content contains all the rules and output format instructions.

## Usage

When a user provides a file or pattern argument:
1. Fetch guidelines from the source URL above
2. Read the specified files
3. Apply all rules from the fetched guidelines
4. Output findings using the format specified in the guidelines

If no files specified, ask the user which files to review.

## Remediating Findings

After identifying issues, use `ui-ux-pro-max` to get deeper remediation guidance per category:

```bash
# Accessibility findings
python3 ui-ux-pro-max/scripts/search.py "accessibility contrast aria keyboard" --domain ux

# Form UX findings
python3 ui-ux-pro-max/scripts/search.py "forms validation error feedback" --domain ux

# Animation / motion findings
python3 ui-ux-pro-max/scripts/search.py "animation reduced-motion timing" --domain ux

# Navigation findings
python3 ui-ux-pro-max/scripts/search.py "navigation breadcrumb back behavior" --domain ux

# Performance / layout findings
python3 ui-ux-pro-max/scripts/search.py "layout shift lazy loading performance" --domain ux
```

Map findings from the audit to the closest domain keyword above. The `ui-ux-pro-max` Quick Reference (sections 1–9) covers every category the guidelines checker surfaces.

## Related Skills

- **ui-ux-pro-max**: Deeper UX guidance and remediation rules for every finding category
- **frontend-design**: Design direction and planning before code is written
- **ui-styling**: Component implementation — shadcn/ui and Tailwind — where fixes require component-level changes