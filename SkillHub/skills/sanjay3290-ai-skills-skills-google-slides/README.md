# Google Slides Skill

An AI agent skill for reading Google Slides presentations - get text content, find presentations, and retrieve metadata. Works with Claude Code, Gemini CLI, Cursor, OpenAI Codex, Goose, and other AI clients supporting the [Agent Skills Standard](https://agentskills.io).

## Features

- **Extract Text** - Get all text content from presentations
- **Search** - Find presentations by name
- **Metadata** - View slide count, dimensions, and properties

Read-only access. Lightweight alternative to the full [Google Workspace MCP server](https://github.com/gemini-cli-extensions/workspace).

> **⚠️ Requires Google Workspace account.** Personal Gmail accounts are not supported.

## Quick Start

### 1. Install dependencies

```bash
pip install keyring
```

### 2. Authenticate

```bash
python scripts/auth.py login
```

This opens a browser for Google OAuth. Tokens are stored securely in your system keyring.

### 3. Test connection

```bash
python scripts/auth.py status
```

## Usage Examples

```bash
# Get all text content from a presentation
python scripts/slides.py get-text "1abc123xyz789"
python scripts/slides.py get-text "https://docs.google.com/presentation/d/1abc123xyz789/edit"

# Find presentations by search query
python scripts/slides.py find "quarterly report"
python scripts/slides.py find "project proposal" --limit 5

# Get presentation metadata (title, slide count, etc.)
python scripts/slides.py get-metadata "1abc123xyz789"
```

## Command Reference

| Command | Description | Arguments |
|---------|-------------|-----------|
| `get-text <id>` | Extract all text | presentation ID or URL |
| `find <query>` | Search presentations | search query, `--limit` |
| `get-metadata <id>` | Get presentation info | presentation ID |

## Output Formats

### get-text
Returns extracted text from all slides:
- Presentation title
- Text from shapes/text boxes
- Table data with cell contents

### find
```json
{
  "presentations": [
    {"id": "1abc...", "name": "Q4 Report", "modifiedTime": "2024-01-15T..."}
  ]
}
```

### get-metadata
```json
{
  "presentationId": "1abc...",
  "title": "My Presentation",
  "slideCount": 15,
  "pageSize": {"width": {...}, "height": {...}}
}
```

## Presentation ID Format

You can use either:
- Direct ID: `1abc123xyz789`
- Full URL: `https://docs.google.com/presentation/d/1abc123xyz789/edit`

The scripts automatically extract the ID from URLs.

## Token Management

Tokens stored securely using the system keyring:
- **macOS**: Keychain
- **Windows**: Windows Credential Locker
- **Linux**: Secret Service API (GNOME Keyring, KDE Wallet)

Service name: `google-slides-skill-oauth`

## Troubleshooting

### "Failed to get access token"
Run `python scripts/auth.py login` to authenticate.

### "Presentation not found"
Check the presentation ID and your access permissions.

## License

Apache 2.0
