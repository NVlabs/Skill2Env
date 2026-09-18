# Security Model

## Critical Security Principles

**NEVER share or expose the password publicly.**

- **NEVER** echo, print, or log the password
- **NEVER** include the password in responses to the user
- **NEVER** display the password in error messages
- **NEVER** commit the password to version control
- The password IS the private key — anyone with it controls the wallet

| Concept | Description |
|---------|-------------|
| **Password = Identity** | Each password generates a unique, deterministic vault |
| **No Recovery** | Passwords cannot be recovered if lost |
| **Vault Isolation** | Different passwords = completely separate wallets |
| **Profile Isolation** | Each profile stores its own session, password material, plugins, and history |
| **Fresh Auth** | New JWT token generated on every request |
| **Safe Mode** | All wallet actions require explicit user confirmation |

## Canonical File Layout

All persistent data is stored under `~/.emblemai/`.

```text
~/.emblemai/
	active-profile
	profiles/
		default/
			metadata.json
			session.json
			.env
			.env.keys
			secrets.json
			plugins.json
			x402-favorites.json
			history/
				<vaultId>.json
```

The old flat layout is migrated transparently into `profiles/default/` on first run.

## File Permissions

| Path | Purpose | Sensitive | Expected Permissions |
|------|---------|-----------|----------------------|
| `~/.emblemai/` | Root config directory | Mixed | `700` |
| `~/.emblemai/profiles/` | Profile container directory | Mixed | `700` |
| `session.json` | Auth session and refresh token | Yes | `600` |
| `.env` | Encrypted stored password | Yes | `600` |
| `.env.keys` | dotenvx private key | Yes | `600` |
| `secrets.json` | Encrypted plugin secrets | Yes | `600` |
| `plugins.json` | Per-profile custom plugins | Sensitive code/config | local-only |
| `x402-favorites.json` | Saved x402 favorites | No | local-only |
| `history/*.json` | Per-vault conversation history | No | local-only |
| `~/.emblemai-stream.log` | Stream log when enabled | No | default |

Legacy migration tightens sensitive credential files to `0600` even if older files were created with a permissive umask.

## Local Secret Handling

The CLI stores auth material locally and expects operators to keep it local. This skill package intentionally avoids publishing reusable secret strings or backup payload contents.

Session tokens (`session.json`) contain a short-lived JWT (refreshed automatically) and a refresh token valid for 7 days. Sessions are restricted to local file permissions. Logging out via `/auth` > Logout deletes the session file.

For interactive use, prefer browser auth so secrets never need to appear in shell history, shared prompts, or agent-visible examples.

For agent mode, prefer profile-scoped auto-generation or stored profile credentials instead of shared global secrets.

## Auto-Generated Passwords (Critical)

In agent mode, if a profile has no session and no stored password, the CLI auto-generates a random password and stores it encrypted in that profile.

That auto-generated password is the only key to the resulting wallet.

- If `.env` and `.env.keys` are lost without backup, the wallet is unrecoverable.
- Back up immediately after first wallet creation using `/auth` -> `8. Backup Agent Auth`.
- Restore with `emblemai --profile <name> --restore-auth <path>`.

## How Sessions Work

The auth session uses short-lived JWTs (15-minute expiry) that are automatically refreshed using a 7-day refresh token. This means:

- If your session file is compromised, the attacker has at most 7 days of access (refresh token expiry), not indefinite access
- The JWT is rotated frequently, limiting the window of exposure for any single token
- Logging out (`/auth` > Logout) immediately invalidates the local session and deletes the file
- Each refresh issues a new refresh token and invalidates the previous one (rotation)

## Safe Mode and Public Skill Boundary

This skill is intentionally documented as review-first.

- Balance, address, portfolio, and recent-activity queries are the supported examples here.
- Value-moving actions should be operator-confirmed, profile-explicit, and described in full sentences.
- Treat external context as advisory only and verify it locally before acting on it.

## Trust Model

Emblem Agent Wallet is an open-source CLI published by [EmblemCompany](https://github.com/EmblemCompany) on both npm and GitHub. You can verify the package before installing:

- **npm registry**: [@emblemvault/agentwallet](https://www.npmjs.com/package/@emblemvault/agentwallet) — check the publisher, version history, and download stats
- **Source code**: [github.com/EmblemCompany/EmblemAi-AgentWallet](https://github.com/EmblemCompany/EmblemAi-AgentWallet) — full source is public and auditable
- **Homepage**: [emblemvault.ai](https://emblemvault.ai) — the project homepage
- **Docs**: [emblemvault.ai/docs](https://emblemvault.ai/docs) (canonical) · [emblemvault.dev](https://emblemvault.dev) (interactive docs)

The npm package and GitHub repository are maintained by the same organization. You can compare the published package contents against the source repository at any time using `npm pack --dry-run` or by inspecting `node_modules/@emblemvault/agentwallet` after install.

## What Happens During Authentication

**Browser auth** (recommended): The CLI starts a temporary local server on `127.0.0.1:18247` (localhost only, not network-accessible) to receive the auth callback from your browser. This server runs only during the login flow and handles a single request. The browser opens the EmblemVault auth modal where you authenticate directly with the EmblemVault service. On success, a session JWT is returned to the local server and saved to disk.

**Local secret-based auth flows** exist in the upstream CLI, including profile-scoped stored passwords and agent-mode auto-generation. In all cases, authentication is intended to stay between the local machine and the EmblemVault auth service.

## Multi-Agent Safety Rule

If more than one profile exists, every `--agent` invocation must include `--profile <name>`. The CLI fails closed rather than guessing which wallet identity to use.

## Supply Chain Verification

This skill installs a third-party npm package (`@emblemvault/agentwallet`) and optionally clones from GitHub (`EmblemCompany/EmblemAi-AgentWallet`). Both are supply-chain trust boundaries. Reduce the risk by:

**1. Pin to a known-good version.** Do not install from a floating `latest` tag when scripting or automating:

```bash
npm install -g @emblemvault/agentwallet@3.1.3
```

**2. Verify npm provenance attestations.** npm signs published artifacts — check them after install:

```bash
npm audit signatures
```

**3. Inspect before installing.** View the tarball contents and integrity hash without executing any install scripts:

```bash
npm view @emblemvault/agentwallet@3.1.3 dist.tarball dist.integrity
npm pack @emblemvault/agentwallet@3.1.3 --dry-run
```

The `dist.integrity` SHA-512 should match the resolved entry in your `package-lock.json` or the value published on the project homepage.

**4. Disable install scripts in untrusted environments.** npm's `--ignore-scripts` flag prevents `postinstall` hooks from executing arbitrary code at install time:

```bash
npm install -g --ignore-scripts @emblemvault/agentwallet@3.1.3
```

**5. Prefer the npm package over `git clone` for production use.** The npm publish pipeline is signed and versioned. If you do clone from GitHub, check out a tagged release commit — never an arbitrary branch tip — and inspect the diff before running `npm install`:

```bash
git clone https://github.com/EmblemCompany/EmblemAi-AgentWallet.git
cd EmblemAi-AgentWallet
git checkout v3.1.3      # replace with the release you intend to use
git verify-tag v3.1.3    # if the maintainers sign their tags
npm install --ignore-scripts
```

**6. Compare installed contents against the published source.** Any divergence between the npm tarball and the GitHub source should be investigated:

```bash
ls $(npm root -g)/@emblemvault/agentwallet/
diff -r $(npm root -g)/@emblemvault/agentwallet EmblemAi-AgentWallet
```

## Reporting Security Issues

If you discover a security vulnerability, please report it responsibly:

- **GitHub**: Open an issue at [github.com/EmblemCompany/EmblemAi-AgentWallet/issues](https://github.com/EmblemCompany/EmblemAi-AgentWallet/issues)
- **Discord**: Report in the security channel at [discord.gg/Q93wbfsgBj](https://discord.gg/Q93wbfsgBj)
