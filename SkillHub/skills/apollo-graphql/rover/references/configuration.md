# Rover Configuration

Installation, authentication, and environment configuration for Apollo Rover CLI.

## Installation

### macOS and Linux

```bash
# Install latest version
curl -sSL https://rover.apollo.dev/nix/latest | sh

# Install specific version
curl -sSL https://rover.apollo.dev/nix/v0.26.0 | sh

# Add to PATH (if not automatic)
export PATH="$HOME/.rover/bin:$PATH"
```

### npm (Cross-platform)

```bash
# Global install
npm install -g @apollo/rover

# Project-local install
npm install --save-dev @apollo/rover
npx rover --version
```

### Windows PowerShell

```powershell
# Install latest
iwr 'https://rover.apollo.dev/win/latest' | iex

# Install specific version
iwr 'https://rover.apollo.dev/win/v0.26.0' | iex
```

### Verify Installation

```bash
rover --version
rover --help
```

## Authentication

### Interactive Authentication

```bash
# Opens browser for authentication
rover config auth
```

**Process:**
1. Browser opens to GraphOS Studio
2. Log in or create account
3. Authorize Rover
4. Token saved to config file

### API Key Authentication

```bash
# Set via environment variable (recommended for CI/CD)
export APOLLO_KEY=your-api-key

# Or configure directly
rover config auth --api-key your-api-key
```

### Verify Authentication

```bash
# Check current authentication
rover config whoami
```

**Output:**
```
Authenticated as: user@example.com
Organization: My Org
API Key Type: User
```

## Environment Variables

### Core Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `APOLLO_KEY` | API key for GraphOS | `user:gh.xxx:yyy` |
| `APOLLO_GRAPH_REF` | Default graph reference | `my-graph@production` |

### Using Environment Variables

```bash
# Set in shell
export APOLLO_KEY=your-api-key
export APOLLO_GRAPH_REF=my-graph@production

# Use in commands
rover subgraph fetch $APOLLO_GRAPH_REF --name products

# Or commands auto-detect APOLLO_GRAPH_REF
rover subgraph fetch --name products
```

### CI/CD Environment

```yaml
# GitHub Actions
env:
  APOLLO_KEY: ${{ secrets.APOLLO_KEY }}
  APOLLO_GRAPH_REF: my-graph@production

steps:
  - run: rover subgraph check $APOLLO_GRAPH_REF --name products --schema ./schema.graphql
```

```yaml
# CircleCI
environment:
  APOLLO_KEY: ${APOLLO_KEY}
  APOLLO_GRAPH_REF: my-graph@production
```

## Configuration File

Rover stores configuration in `~/.rover/config.toml`.

### Location

```bash
# View config path
rover config list

# macOS/Linux: ~/.rover/config.toml
# Windows: %USERPROFILE%\.rover\config.toml
```

### Structure

```toml
[profiles.default]
api_key = "user:gh.xxx:yyy"

[profiles.staging]
api_key = "user:gh.xxx:zzz"
```

## Profiles

Use profiles for different environments or accounts.

### Create Profile

```bash
# Create/update profile
rover config auth --profile staging
```

### Use Profile

```bash
# Specify profile for command
rover subgraph fetch my-graph@staging --name products --profile staging
```

### List Profiles

```bash
rover config list
```

## Output Formats

### Plain Text (Default)

```bash
rover subgraph fetch my-graph@production --name products
```

Output: Raw SDL schema

### JSON

```bash
rover subgraph fetch my-graph@production --name products --format json
```

Output:
```json
{
  "data": {
    "sdl": "type Product { ... }",
    "name": "products"
  },
  "error": null
}
```

### Using with jq

```bash
# Extract just the SDL
rover subgraph fetch my-graph@production --name products --format json | jq -r '.data.sdl'

# Check for errors
rover subgraph check my-graph@production --name products --schema ./schema.graphql --format json | jq '.error'
```

## Logging

### Log Levels

```bash
# Increase verbosity
rover --log debug subgraph fetch my-graph@production --name products

# Available levels: error, warn, info, debug, trace
```

### Environment Variable

```bash
export APOLLO_TELEMETRY_DISABLED=1  # Disable telemetry
export ROVER_LOG=debug              # Set log level
```

## Telemetry

Rover collects anonymous usage data by default.

### Disable Telemetry

```bash
export APOLLO_TELEMETRY_DISABLED=1
```

### What's Collected

- Command names (not arguments or schemas)
- Rover version
- OS type
- Anonymous usage patterns

## Proxy Configuration

### HTTP Proxy

```bash
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
```

### No Proxy

```bash
export NO_PROXY=localhost,127.0.0.1,.internal.example.com
```

## SSL/TLS Configuration

### Custom CA Certificate

```bash
# Set CA bundle
export SSL_CERT_FILE=/path/to/ca-bundle.crt

# Or for curl-based operations
export CURL_CA_BUNDLE=/path/to/ca-bundle.crt
```

### Disable SSL Verification (Not Recommended)

```bash
# For development only
export ROVER_SKIP_SSL_VALIDATION=1
```

## Updating Rover

### Check for Updates

```bash
rover update check
```

### Update to Latest

```bash
# npm
npm update -g @apollo/rover

# curl (reinstall)
curl -sSL https://rover.apollo.dev/nix/latest | sh
```

## Uninstalling

### npm

```bash
npm uninstall -g @apollo/rover
```

### Manual Installation

```bash
# Remove binary
rm -rf ~/.rover

# Remove from PATH (in .bashrc/.zshrc)
# Remove: export PATH="$HOME/.rover/bin:$PATH"
```

## Troubleshooting

### Authentication Issues

```bash
# Clear and re-authenticate
rm ~/.rover/config.toml
rover config auth
```

### Network Issues

```bash
# Test connectivity
curl -I https://api.apollographql.com

# Check DNS
nslookup api.apollographql.com
```

### Permission Issues

```bash
# Fix permissions (macOS/Linux)
chmod +x ~/.rover/bin/rover
```

### Version Conflicts

```bash
# Check installed location
which rover

# Ensure correct version
rover --version
```
