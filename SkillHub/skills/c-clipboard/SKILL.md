---
name: c-clipboard
description: System clipboard — copy, paste, transform content between clipboard and files.
tags: [clipboard, copy, paste, pbcopy, pbpaste]
---

# Clipboard — Copy & Paste

Read from and write to the system clipboard. Built into macOS, no install needed.

## Commands

```bash
# Read clipboard contents
pbpaste

# Copy text to clipboard
echo "hello world" | pbcopy

# Copy file contents to clipboard
pbcopy < /path/to/file.txt

# Save clipboard to file
pbpaste > /path/to/output.txt

# Copy command output to clipboard
ls -la | pbcopy
date | pbcopy

# Transform clipboard content
pbpaste | tr '[:lower:]' '[:upper:]' | pbcopy    # uppercase
pbpaste | sort | pbcopy                            # sort lines
pbpaste | wc -w                                    # word count

# Copy with no trailing newline
printf "%s" "exact text" | pbcopy
```

## Linux Equivalents

```bash
# If on Linux, use xclip or xsel
xclip -selection clipboard           # copy (pipe into)
xclip -selection clipboard -o        # paste
```

## Guidelines

- When the user says "copy this" or "put this in my clipboard", use `pbcopy`
- When the user says "what's in my clipboard?" or "paste", use `pbpaste`
- For transformations, pipe `pbpaste` through the transform and back to `pbcopy`
- Always confirm what was copied with a brief summary
- Never display clipboard contents unless asked — they may contain sensitive data
