# Google Sheets Skill

An AI agent skill for reading Google Sheets spreadsheets - get content, fetch specific ranges, search, and view metadata. Works with Claude Code, Gemini CLI, Cursor, OpenAI Codex, Goose, and other AI clients supporting the [Agent Skills Standard](https://agentskills.io).

## Features

- **Read Spreadsheets** - Get all content as text, CSV, or JSON
- **Get Ranges** - Fetch specific cell ranges (A1 notation)
- **Search** - Find spreadsheets by name
- **Metadata** - View sheet names, dimensions, and properties

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
# Get spreadsheet content as plain text (default)
python scripts/sheets.py get-text SPREADSHEET_ID

# Get spreadsheet content as CSV
python scripts/sheets.py get-text SPREADSHEET_ID --format csv

# Get spreadsheet content as JSON
python scripts/sheets.py get-text SPREADSHEET_ID --format json

# Get values from a specific range (A1 notation)
python scripts/sheets.py get-range SPREADSHEET_ID "Sheet1!A1:D10"
python scripts/sheets.py get-range SPREADSHEET_ID "A1:C5"

# Find spreadsheets by search query
python scripts/sheets.py find "budget 2024"
python scripts/sheets.py find "sales report" --limit 5

# Get spreadsheet metadata (sheets, dimensions, etc.)
python scripts/sheets.py get-metadata SPREADSHEET_ID
```

## Command Reference

| Command | Description | Arguments |
|---------|-------------|-----------|
| `get-text <id>` | Get all content | spreadsheet ID, `--format` |
| `get-range <id> <range>` | Get specific cells | spreadsheet ID, A1 range |
| `find <query>` | Search spreadsheets | search query, `--limit` |
| `get-metadata <id>` | Get sheet info | spreadsheet ID |

## Output Formats

### Text (default)
```
Spreadsheet Title: Sales Data
Sheet Name: Q1
Name | Revenue | Units
Product A | 10000 | 50
```

### CSV
```
Name,Revenue,Units
Product A,10000,50
```

### JSON
```json
{"Q1": [["Name", "Revenue", "Units"], ["Product A", "10000", "50"]]}
```

## A1 Notation Examples

- `Sheet1!A1:B10` - Range A1 to B10 on Sheet1
- `Sheet1!A:A` - All of column A
- `Sheet1!1:1` - All of row 1
- `A1:C5` - Range on first sheet

## Token Management

Tokens stored securely using the system keyring:
- **macOS**: Keychain
- **Windows**: Windows Credential Locker
- **Linux**: Secret Service API (GNOME Keyring, KDE Wallet)

Service name: `google-sheets-skill-oauth`

## Troubleshooting

### "Failed to get access token"
Run `python scripts/auth.py login` to authenticate.

### "Spreadsheet not found"
Check the spreadsheet ID and your access permissions.

### "Invalid range"
Verify the A1 notation format and that the sheet name exists.

## License

Apache 2.0
