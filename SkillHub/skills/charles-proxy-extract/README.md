# Charles Proxy Session Extractor

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)
![No Dependencies](https://img.shields.io/badge/dependencies-none-green.svg)

A Claude Code skill that extracts and analyzes HTTP/HTTPS request and response data from Charles Proxy session files (`.chlsj` format).

When debugging API integrations or analyzing network traffic, simply mention a `.chlsj` file and Claude will automatically use this skill to parse and present the data.

**Zero dependencies** - uses Python standard library only.

## Features

- **Pattern-based filtering** - extract requests by URL pattern
- **Method filtering** - filter by HTTP method (GET, POST, PUT, PATCH, DELETE)
- **Request body inspection** - view request bodies for POST/PUT/PATCH operations
- **JSON export** - save filtered responses for further analysis
- **Summary mode** - get quick traffic overview without full response bodies
- **Pretty-printed output** - formatted JSON by default for readability

## How It Works

1. Export a session from Charles Proxy in `.chlsj` (JSON) format
2. Reference the file when chatting with Claude Code
3. Claude automatically detects the file type and uses this skill
4. Get filtered, formatted request/response data instantly

## Prerequisites

- Python 3.x (no external dependencies required)
- Charles Proxy session files exported in `.chlsj` format

## Installation

### For Claude Code Users

Clone this repository into your skills directory:

```bash
# User-level (available in all projects)
git clone https://github.com/yourusername/charles-proxy-extract ~/.claude/skills/charles-proxy-extract

# Project-level (available in specific project)
git clone https://github.com/yourusername/charles-proxy-extract .claude/skills/charles-proxy-extract
```

That's it! No additional dependencies to install.

### Standalone Usage

If you want to use the script without Claude Code, just ensure Python 3.x is installed:

```bash
which python3
```

## Using with Claude Code

Once installed, Claude will automatically suggest this skill when you mention Charles Proxy files. Try phrases like:

- "Extract the /api/users responses from session.chlsj"
- "Show me POST requests to /logs in this Charles session"
- "Analyze the network traffic in debug-session.chlsj"
- "Export all /items responses to a JSON file"
- "Summarize what's in this Charles session file"
- "Show the first /api/auth request"

Claude will use this skill to parse the file and present the results in a clear, formatted way.

## Standalone Usage

You can also use the script directly from the command line:

```bash
python3 ./extract_responses.py <file.chlsj> <path_pattern> [options]
```

### Arguments

- `file` - Charles session file (`.chlsj` format)
- `pattern` - String pattern to match in URL paths (case-sensitive)

### Options

| Option | Description |
|--------|-------------|
| `-m, --method METHOD` | Filter by HTTP method (GET, POST, PUT, PATCH, DELETE) |
| `-f, --first-only` | Show only the first matching request |
| `-s, --summary-only` | Show summary stats without response bodies |
| `-o, --output FILE` | Save all responses to a JSON file |
| `--no-pretty` | Disable pretty-printing of JSON responses |
| `-h, --help` | Show help message |

**Note:** When filtering by POST, PUT, or PATCH methods, request bodies are automatically displayed along with responses.

### Workflow Examples

```bash
# Explore available endpoints
python3 ./extract_responses.py session.chlsj "/" --summary-only

# Inspect specific endpoint
python3 ./extract_responses.py session.chlsj "/logs" --method POST

# Quick peek at first result
python3 ./extract_responses.py session.chlsj "/api/users" --first-only

# Save all responses for analysis
python3 ./extract_responses.py session.chlsj "/items" -o items-response.json

# Filter POST requests with bodies
python3 ./extract_responses.py session.chlsj "/submit" --method POST
```

## Example Output

### Summary Mode

```
Found 145 total requests in session
Pattern '/api/logs' matched 12 requests

Matched paths:
  /api/logs/submit (8 requests)
  /api/logs/query (4 requests)

Methods: POST: 8, GET: 4
Status codes: 200: 11, 404: 1
```

### Full Mode

```
Request 1/12: POST /api/logs/submit
Status: 200 OK
Timestamp: 2025-12-28T10:15:23Z

Request Body:
{
  "level": "error",
  "message": "Connection timeout"
}

Response:
{
  "id": "log_123",
  "status": "recorded"
}
```

### Export Mode

Creates a JSON file with structure:

```json
{
  "pattern": "/api/logs",
  "total_requests": 12,
  "extracted_at": "2025-12-28T10:15:23Z",
  "requests": [
    {
      "method": "POST",
      "path": "/api/logs/submit",
      "status": 200,
      "timestamp": "2025-12-28T10:15:23Z",
      "request_body": {...},
      "response": {...}
    }
  ]
}
```

## Tips

### Pattern Matching

Patterns use simple substring matching (case-sensitive):

- `/history` matches `/history/5fd95c39.../2025-12-04`
- `/items` matches both `/items/...` and `/items-by-day/...`
- `/` matches all requests (useful for summary mode)

### Best Practices

1. **Start with summary mode** - Use `--summary-only` to understand what's in the session
2. **Narrow down gradually** - Start broad, then filter by method or pattern
3. **Use first-only for inspection** - Add `--first-only` when you just need a sample
4. **Export for analysis** - Use `-o` to save data for programmatic analysis

## Troubleshooting

**"File not found"**
- Verify the `.chlsj` file path is correct
- Use absolute paths or ensure you're in the right directory

**"Invalid JSON"**
- Ensure the file is a valid Charles Proxy session export
- Re-export the session from Charles Proxy in `.chlsj` format

**No matching requests**
- Pattern matching is case-sensitive - check capitalization
- Try broader pattern (e.g., `/` matches everything)
- Use `--summary-only` to see all available paths

**Python not found**
- Ensure Python 3.x is installed and available in PATH
- Try using `python` instead of `python3` or vice versa

## Integration Use Cases

This skill is particularly useful for:

- **Extracting sample data** - Generate test fixtures from real API traffic
- **Debugging integrations** - Identify discrepancies between expected and actual API behavior
- **Documenting APIs** - Extract real-world examples for API documentation
- **Model updates** - Find new fields or enum values not yet in your models
- **Regression testing** - Compare API responses before and after changes
- **Performance analysis** - Identify slow endpoints or large payloads

## Related Tools

- [**Charles Proxy**](https://www.charlesproxy.com/) - HTTP debugging proxy for macOS, Windows, and Linux
- [**Claude Code**](https://claude.com/claude-code) - AI-powered coding assistant

## License

MIT License - see [LICENSE.md](LICENSE.md) for details.

## Contributing

Contributions are welcome! Feel free to:

- Open issues for bugs or feature requests
- Submit pull requests for improvements
- Share your use cases and feedback
