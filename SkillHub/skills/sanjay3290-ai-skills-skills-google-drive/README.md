# Google Drive Skill

An AI agent skill for interacting with Google Drive - search files, find folders, list contents, and download files. Works with Claude Code, Gemini CLI, Cursor, OpenAI Codex, Goose, and other AI clients supporting the [Agent Skills Standard](https://agentskills.io).

## Features

- **Search** - Full-text search across files
- **Find Folders** - Locate folders by name
- **List Contents** - Browse folder contents
- **Download** - Download files locally

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
# Search for files (full-text search)
python scripts/drive.py search "quarterly report"

# Search by title only
python scripts/drive.py search "title:budget"

# Search using Google Drive URL
python scripts/drive.py search "https://drive.google.com/drive/folders/1ABC123..."

# Search files shared with you
python scripts/drive.py search --shared-with-me

# Search with pagination
python scripts/drive.py search "report" --limit 5 --page-token "..."

# Find a folder by exact name
python scripts/drive.py find-folder "Project Documents"

# List files in root Drive
python scripts/drive.py list

# List files in a specific folder
python scripts/drive.py list 1ABC123xyz --limit 20

# Download a file
python scripts/drive.py download 1ABC123xyz ./downloads/report.pdf
```

## Command Reference

| Command | Description | Arguments |
|---------|-------------|-----------|
| `search [query]` | Search files | query, `--shared-with-me`, `--limit` |
| `find-folder <name>` | Find folder by name | folder name |
| `list [folder_id]` | List folder contents | optional folder ID, `--limit` |
| `download <id> <path>` | Download file | file ID, local path |

## Search Query Formats

| Format | Example | Description |
|--------|---------|-------------|
| Full-text | `"quarterly report"` | Searches file contents and names |
| Title | `"title:budget"` | Searches file names only |
| URL | `https://drive.google.com/...` | Extracts and uses file/folder ID |
| Folder ID | `1ABC123...` | Lists folder contents |
| Native query | `mimeType='application/pdf'` | Drive query syntax |

## Download Limitations

- Regular files (PDFs, images, etc.) download directly
- Google Docs/Sheets/Slides cannot be downloaded via this tool
- For Google Workspace files, use export or dedicated tools

## Token Management

Tokens stored securely using the system keyring:
- **macOS**: Keychain
- **Windows**: Windows Credential Locker
- **Linux**: Secret Service API (GNOME Keyring, KDE Wallet)

Service name: `google-drive-skill-oauth`

## Troubleshooting

### "Failed to get access token"
Run `python scripts/auth.py login` to authenticate.

### "File not found"
Check the file ID and your access permissions.

### "Cannot download Google Workspace file"
Use the dedicated skill (google-docs, google-sheets, google-slides) for Google Workspace files.

## License

Apache 2.0
