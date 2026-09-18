# Troubleshooting

## Common Issues and Solutions

### Installation Issues

| Issue | Solution |
|-------|----------|
| `emblemai: command not found` | Run: `npm install -g @emblemvault/agentwallet` |
| npm permission errors | Do **not** use `sudo` for global installs — `sudo npm install -g` runs untrusted package install scripts as root, which is a privilege-escalation footgun. Configure a user-owned npm prefix instead: `mkdir -p ~/.npm-global && npm config set prefix ~/.npm-global && export PATH=~/.npm-global/bin:$PATH`. Or use a version manager such as [nvm](https://github.com/nvm-sh/nvm), [fnm](https://github.com/Schniz/fnm), or [volta](https://volta.sh/). See the [npm docs on resolving EACCES errors](https://docs.npmjs.com/resolving-eacces-permissions-errors-when-installing-packages-globally). |
| Node.js version too old | Update Node.js to version 18.0.0 or higher |
| Package download fails | Check network connectivity: `npm config get registry` |

### Authentication Issues

| Issue | Solution |
|-------|----------|
| "Authentication failed" | Check network connectivity to auth service |
| Browser doesn't open for auth | Copy the printed URL and open it manually |
| Session expired | Run `emblemai --profile <name>` again — browser will open for fresh login |
| Authentication timeout | Increase timeout: wait up to 5 minutes for browser auth |
| `Multiple profiles detected. In agent mode you must pass --profile <name>.` | Re-run with `--profile <name>`; agent mode fails closed when multiple profiles exist |
| Agent created a new wallet unexpectedly | Check which profile was selected and whether that profile already had `.env`, `.env.keys`, or `session.json` |
| Restoring auth into a new profile fails | Use `--profile <name> --restore-auth <path>`; restore creates the target profile first |

### Runtime Issues

| Issue | Solution |
|-------|----------|
| **Slow response** | Normal — queries can take up to 2 minutes for complex operations |
| No response after 2+ minutes | Check network connectivity; press Ctrl+C and retry |
| glow not rendering | Install glow: `brew install glow` (optional, falls back to plain text) |
| Plugin not loading | Check that the npm package is installed correctly |
| Memory issues | Ensure sufficient RAM; complex queries may require 1GB+ |
| Terminal display issues | Ensure terminal supports 256 colors; try `export TERM=xterm-256color` |

### Configuration Issues

| Issue | Solution |
|-------|----------|
| Config file permissions | Check permissions: sensitive profile files should be `600`, directories `700` |
| Corrupted session file | Preferred: `/auth` -> Logout, then rerun `emblemai --profile <name>`; fallback: remove `~/.emblemai/profiles/<name>/session.json` locally |
| History not persisting | Check write permissions inside `~/.emblemai/profiles/<name>/history/` |
| Log file not created | Check directory permissions: `mkdir -p ~/.emblemai` |
| Plugins missing after upgrade | Custom plugins are now stored per profile in `plugins.json`, not `~/.emblemai-plugins.json` |
| Old install paths changed | Legacy flat-layout installs are migrated automatically into `profiles/default/` on first run |

### Network Issues

| Issue | Solution |
|-------|----------|
| Cannot connect to EmblemAI API | Check firewall/network settings |
| SSL certificate errors | Update system certificates or use `--hustle-url` with HTTP (not recommended) |
| Proxy issues | Configure npm proxy: `npm config set proxy http://proxy:port` |
| DNS resolution failures | Check DNS settings; try using IP addresses in URLs |

## Performance Optimization

### Response Time Management

**Expected response times:**
- Simple queries (balances, addresses): 5-15 seconds
- Portfolio and activity queries: 15-30 seconds
- NFT collection lookups: 30-60 seconds
- Large history summaries: 60-120 seconds

**If responses are consistently slow:**
1. Check internet connection speed
2. Monitor system resources (CPU, memory)
3. Try during off-peak hours
4. Use simpler queries

## Debugging

### Enable Debug Mode

```bash
# Start with debug mode
emblemai --debug

# Or enable during runtime
/debug on
```

Debug mode shows:
- Tool arguments and parameters
- Intent context and parsing
- Network request details
- Response processing steps

### Logging

```bash
# Enable logging
emblemai --log

# Custom log file location
emblemai --log --log-file /path/to/custom.log
```

Log files contain:
- Timestamped messages
- User queries and AI responses
- Error messages and stack traces
- Performance metrics

### Common Error Messages

| Error Message | Meaning | Solution |
|---------------|---------|----------|
| `ECONNREFUSED` | Cannot connect to API | Check network, verify API URL |
| `ETIMEDOUT` | Connection timeout | Increase timeout, retry later |
| `ENOTFOUND` | DNS resolution failed | Check DNS settings |
| `EACCES` | Permission denied | Check file permissions |
| `ENOSPC` | Disk space full | Free up disk space |
| `EMFILE` | Too many open files | Increase file descriptor limit |

## Recovery Procedures

### Session Recovery

If your session is corrupted or expired:

```bash
# Preferred: use the interactive menu
# /auth -> Logout

# Start fresh
emblemai --profile <name>

# Fallback only if menu is unavailable: clear the local session file using your normal shell workflow, then relaunch `emblemai`
```

### Configuration Reset

To reset local configuration safely, first make a local backup/export using the CLI's own recovery flow or your normal local operator procedure, then relaunch `emblemai`. Keep backup artifacts local and out of shared prompts.

### Backup Recovery

If a profile was created in agent mode and you need to move it to another machine, restore the backup into the same profile name:

```bash
emblemai --profile motoko --restore-auth ~/emblemai-auth-backup.json
```

This recreates the profile if needed and restores the encrypted local credentials.

### Conversation History Reset

```bash
# Clear history
emblemai --reset

# Or manually
rm ~/.emblemai/profiles/<name>/history/*.json
```

## Getting Help

### Community Support

- **GitHub Issues**: [github.com/EmblemCompany/EmblemAi-AgentWallet/issues](https://github.com/EmblemCompany/EmblemAi-AgentWallet/issues)
- **Discord**: [discord.gg/Q93wbfsgBj](https://discord.gg/Q93wbfsgBj)
- **Documentation**: [emblemvault.ai/docs](https://emblemvault.ai/docs) (canonical) · [emblemvault.dev](https://emblemvault.dev) (interactive)

### Diagnostic Information

When reporting issues, include:

```bash
# System information
node --version
npm --version
uname -a

# Package information
npm list -g @emblemvault/agentwallet

# Configuration (sanitized)
ls -la ~/.emblemai/
find ~/.emblemai/profiles -maxdepth 2 -type f | sort
```
