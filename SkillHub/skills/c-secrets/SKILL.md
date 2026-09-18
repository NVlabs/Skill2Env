---
name: c-secrets
description: Look up and manage secrets using 1Password CLI (`op`) or Bitwarden CLI (`bw`). Retrieve passwords, generate new passwords, and copy credentials to clipboard. CRITICAL: Never display passwords in plain text — always copy to clipboard.
tags: [passwords, secrets, 1password, bitwarden, credentials, security]
---

## What This Skill Does

Retrieves credentials and generates passwords using `op` (1Password CLI) or `bw` (Bitwarden CLI). All passwords are copied to clipboard — never printed to the terminal.

## CRITICAL RULE

**NEVER display passwords, tokens, or secret values in plain text output.** Always use clipboard copy commands. This applies to every secret retrieval, no exceptions.

## CLI Tools

### 1Password (`op`)

```bash
# Copy a password to clipboard (PREFERRED — never print)
op item get "GitHub" --fields password | pbcopy

# Look up an item
op item get "GitHub"

# List all items
op item list

# Generate a password (copy to clipboard)
op generate-password --length 20 --symbols | pbcopy

# Get a specific field
op item get "AWS" --fields "Access Key ID"
```

### Bitwarden (`bw`)

```bash
# Unlock vault first (session token required)
export BW_SESSION=$(bw unlock --raw)

# Copy password to clipboard (PREFERRED)
bw get password "GitHub" | pbcopy

# Look up an item
bw get item "GitHub"

# Generate a password (copy to clipboard)
bw generate --length 20 --special | pbcopy
```

## Usage Guidelines

1. **Always pipe passwords to `pbcopy`** — confirm "Copied to clipboard" to the user instead of showing the value.
2. If the user asks to "show" or "display" a password, redirect: copy it to clipboard and inform them.
3. For lookups, show non-sensitive fields (username, URL, notes) but never the password itself.
4. If vault is locked, prompt the user to unlock it manually before proceeding.

## Notes

- `op` requires 1Password app installed and CLI signed in: `op signin`
- `bw` requires Bitwarden CLI installed and vault unlocked each session
