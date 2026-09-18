# Release Files

This directory contains pre-packaged release files for easy installation of the PICT Test Designer skill.

## Minimal Installation Package

**File:** `pict-test-designer-minimal.zip` (9.3 KB)

This ZIP contains only the essential files needed for the skill to function:

- `SKILL.md` - Core skill definition
- `LICENSE` - MIT License
- `references/pict_syntax.md` - PICT syntax reference
- `references/examples.md` - Common patterns and examples
- `README-INSTALL.txt` - Installation instructions

### Quick Installation

**For personal use (all projects):**
```bash
# Download the ZIP
wget https://github.com/omkamal/pypict-claude-skill/raw/main/releases/pict-test-designer-minimal.zip

# Extract and install
unzip pict-test-designer-minimal.zip
mv pict-test-designer-minimal ~/.claude/skills/pict-test-designer

# Restart Claude Code
```

**For project-specific use:**
```bash
# Download the ZIP
wget https://github.com/omkamal/pypict-claude-skill/raw/main/releases/pict-test-designer-minimal.zip

# Extract and install
unzip pict-test-designer-minimal.zip
mv pict-test-designer-minimal .claude/skills/pict-test-designer

# Restart Claude Code
```

**Windows:**
```powershell
# Download manually or use:
Invoke-WebRequest -Uri "https://github.com/omkamal/pypict-claude-skill/raw/main/releases/pict-test-designer-minimal.zip" -OutFile "pict-test-designer-minimal.zip"

# Extract to:
# Personal: %USERPROFILE%\.claude\skills\pict-test-designer\
# Project:  .claude\skills\pict-test-designer\
```

## What's Not Included

The minimal package excludes:
- Full examples (ATM test plan)
- Helper scripts (pict_helper.py)
- Extended documentation (README.md, QUICKSTART.md, etc.)

For the complete package with examples and documentation, clone the full repository:
```bash
git clone https://github.com/omkamal/pypict-claude-skill.git ~/.claude/skills/pict-test-designer
```

## Verification

After installation, restart Claude Code and verify by asking:
```
Do you have access to the pict-test-designer skill?
```

Or start using it immediately:
```
Design test cases for a login function with username, password, and remember me checkbox.
```

## Version Information

- **Current Version:** 1.0.0
- **Last Updated:** October 19, 2025
- **Size:** 9.3 KB (compressed)
- **Files:** 5 files

## Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/omkamal/pypict-claude-skill/issues
- Full Documentation: https://github.com/omkamal/pypict-claude-skill
