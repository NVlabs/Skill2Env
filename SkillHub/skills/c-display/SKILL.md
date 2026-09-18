---
name: c-display
description: Control display brightness and safely move files to trash instead of permanently deleting with rm.
tags: [display, brightness, trash, safety]
---

# Display & Safety

## brightness

```bash
# Get current brightness (0.0 to 1.0)
brightness -l

# Set brightness to 80%
brightness 0.8

# Set brightness to minimum
brightness 0.0

# Set brightness to maximum
brightness 1.0
```

## trash (macos-trash)

Safe alternative to `rm` — moves files to macOS Trash:

```bash
# Move file to trash
trash file.txt

# Move multiple files
trash file1.txt file2.txt dir/

# Move with confirmation prompt
trash --interactive file.txt
```

## Guidelines

- Use `trash` instead of `rm` when the user might want to recover files
- Use `rm` only for temporary/generated files where recovery isn't needed
- Brightness value is 0.0 (off) to 1.0 (max)
- `brightness -l` lists all displays when multiple monitors connected
