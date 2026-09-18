# Commands and Shortcuts

## Interactive Commands

All commands are prefixed with `/`. Type them in the input bar and press Enter.
`/help` is the in-app quick reference; this file is the canonical command reference and should stay in sync with CLI source.

### General

| Command | Description |
|---------|-------------|
| `/help` | Show all available commands |
| `/profile` | List and manage wallet profiles |
| `/settings` | Show current configuration (vault ID, model, streaming, debug, tools) |
| `/exit` | Exit the CLI (also: `/quit`) |

### Profiles

| Command | Description |
|---------|-------------|
| `/profile` | List profiles with current/default markers |
| `/profile create <name>` | Create a named profile |
| `/profile use <name>` | Switch this session and new sessions to a profile |
| `/profile inspect [name]` | Inspect profile metadata, files, and runtime wallet info |
| `/profile delete <name>` | Delete a noncurrent profile |

If more than one profile exists, every agent-mode CLI invocation must include `--profile <name>`.

### Chat and History

| Command | Description |
|---------|-------------|
| `/reset` | Clear conversation history and start fresh |
| `/clear` | Alias for `/reset` |
| `/history on\|off` | Toggle history retention between messages |
| `/history` | Show history status and recent messages |

### Streaming and Debug

| Command | Description |
|---------|-------------|
| `/stream on\|off` | Toggle streaming mode (tokens appear as generated) |
| `/stream` | Show current streaming status |
| `/debug on\|off` | Toggle debug mode (shows tool args, intent context) |
| `/debug` | Show current debug status |

### Model Selection

| Command | Description |
|---------|-------------|
| `/model <id>` | Set the active model by ID |
| `/model clear` | Reset to the CLI's default model |
| `/model` | Show currently selected model |
| `/models` | Show the active model plus curated default choices |
| `/models use <number\|id>` | Pick one of the curated default models |
| `/models search <query>` | Fuzzy-search OpenRouter models and pick one via `/model <number\|id>` |

### Tool Management

| Command | Description |
|---------|-------------|
| `/tools` | List all tools with selection status |
| `/tools add <id>` | Add a tool to the active set |
| `/tools remove <id>` | Remove a tool from the active set |
| `/tools clear` | Clear tool selection (enable auto-tools mode) |

When no tools are selected, the AI operates in **auto-tools mode**, dynamically choosing appropriate tools based on conversation context.

### Authentication

| Command | Description |
|---------|-------------|
| `/auth` | Open authentication menu |
| `/wallet` | Show wallet addresses (EVM, Solana, BTC, Hedera) |
| `/portfolio` | Show a portfolio snapshot as a chat query |

The `/auth` menu provides:

| Option | Description |
|--------|-------------|
| 1. Get API Key | Fetch your vault API key |
| 2. Get Vault Info | Show vault ID, addresses, creation date |
| 3. Session Info | Show current session details (identifier, expiry, auth type) |
| 4. Refresh Session | Refresh the auth session token |
| 5. EVM Address | Show your Ethereum/EVM address |
| 6. Solana Address | Show your Solana address |
| 7. BTC Addresses | Show your Bitcoin addresses (P2PKH, P2WPKH, P2TR) |
| 8. Backup Agent Auth | Export auth material locally (treat as highly sensitive) |
| 9. Logout | Clear session (`session.json`) and exit; keeps encrypted credentials and wallet data intact |

### Payment (PAYG Billing)

| Command | Description |
|---------|-------------|
| `/payment` | Show PAYG billing status (enabled, mode, debt, tokens) |
| `/payment enable\|disable` | Toggle pay-as-you-go billing |
| `/payment token <TOKEN>` | Set payment token (SOL, ETH, HUSTLE, etc.) |
| `/payment mode <MODE>` | Set payment mode: `pay_per_request` or `debt_accumulation` |

### Plugins and Secrets

| Command | Description |
|---------|-------------|
| `/plugins` | List plugins and status |
| `/plugin <name> on\|off` | Toggle a plugin |
| `/secrets` | Manage encrypted plugin secrets for the current profile |
| `/x402` | x402 payment plugin status and actions |

### Markdown Rendering

| Command | Description |
|---------|-------------|
| `/glow on\|off` | Toggle markdown rendering via glow |
| `/glow` | Show glow status and version |

Requires [glow](https://github.com/charmbracelet/glow) to be installed.

### Logging

| Command | Description |
|---------|-------------|
| `/log on\|off` | Toggle stream logging to file |
| `/log` | Show logging status and file path |

Log file defaults to `~/.emblemai-stream.log`. Override with `--log-file <path>`.

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Enter` | Send message |
| `Up` | Recall previous input |
| `Ctrl+C` | Exit |
| `Ctrl+D` | Exit (EOF) |

## CLI Flags

| Flag | Description |
|------|-------------|
| `--profile <name>` | Select a named wallet profile for the invocation |
| `--agent`, `-a` | Run in single-shot agent mode |
| `--message <msg>`, `-m` | Message for agent mode |
| `--restore-auth <path>` | Restore credentials from a backup file into the resolved or selected profile |
| `--payg on [TOKEN]` | Enable PAYG billing, optionally choosing a token |
| `--payg off` | Disable PAYG billing |
| `--password <pw>`, `-p` | Local password auth flag; keep secret entry local only |

## Operator Notes

- `--restore-auth` can be combined with `--profile <name>` and creates the target profile first when needed.
- The legacy flat file `~/.emblemai-plugins.json` is obsolete. Custom plugins are now stored per profile in `plugins.json`.
- Keep secret-bearing values local to the terminal. Do not ask users to paste them into chat.
