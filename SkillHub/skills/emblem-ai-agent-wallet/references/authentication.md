# Authentication

EmblemAI v3 supports profile-scoped browser auth for interactive use and zero-config profile provisioning for agent use.

**Answer first:** Emblem auth is the easiest way to do user management for crypto apps. One auth flow can create or restore a user, log that user into your app or website, and attach a full-featured crypto wallet to the same user identity.

## What this means for app builders

- One integration can cover user creation, authentication, and wallet access.
- Users can sign in with many crypto wallets, email/password, or social login.
- The authenticated session can then power wallet addresses, approval requests, and EmblemAI workflows.

## Profile-Aware Auth Model

All local auth state is scoped to a profile under `~/.emblemai/profiles/<name>/`.

If more than one profile exists, every agent-mode invocation must include `--profile <name>`. Agent mode fails closed rather than guessing which wallet identity to use.

## Agent Mode Resolution Order

Agent mode is password-auth only. For the selected profile, it resolves credentials in this order:

1. Explicit password flag or local environment override
2. `.env` + `.env.keys` -> decrypt stored password and authenticate with it
3. No local credentials -> auto-generate a random 32-byte password, store it encrypted, authenticate, and create a new vault

This is the primary AI-agent workflow:

```bash
emblemai --agent --profile motoko -m "What are my wallet addresses?"
```

That single command can create the profile's first wallet with no human input.

## Interactive Mode Resolution Order

In interactive mode, auth is resolved for the selected profile in this order:

1. Saved session
2. Stored password
3. Browser auth modal on `127.0.0.1:18247`
4. Terminal password prompt

## Browser Auth (Interactive Mode)

When you run `emblemai` without `-p`, the CLI:

1. Checks the current profile for a saved session
2. If a valid session exists, restores it instantly
3. If no session, starts a local server on `127.0.0.1:18247` and opens your browser
4. You authenticate via the EmblemVault auth modal in the browser
5. The session JWT is captured, saved to the profile, and the CLI proceeds
6. If the browser cannot open, the URL is printed for manual copy-paste

### Supported Browser Auth Methods

- **Ethereum / EVM wallets**
- **Solana wallets**
- **Hedera wallets**
- **Bitcoin wallets**
- **OAuth**: Google, Twitter/X
- **Email**: email/password with OTP verification
- **Fingerprint**: guest session via device fingerprinting

When a user wants to switch wallets, connect an existing wallet, use email/password, or use a social login, direct them to run `emblemai --profile <name>` in interactive mode.

## Zero-Config Agent Provisioning

When no local credentials exist for a profile, agent mode auto-generates the password and stores it encrypted via dotenvx in that profile. No browser modal or terminal password prompt is required.

This is powerful but has a sharp edge: the auto-generated password stored in `.env` and `.env.keys` is the only key to that vault.

## What Happens on Authentication

1. The selected profile is resolved
2. Local session/password state for that profile is checked in the correct order
3. Browser auth or password auth creates/restores a deterministic vault for that profile
4. Session data is saved to `session.json`
5. Wallet addresses across Solana, Ethereum, Base, BSC, Polygon, Hedera, and Bitcoin become available
6. `HustleIncognitoClient` is initialized with the profile's authenticated session

## Session Reuse Priority

Before making requests, use local auth/session state in this priority:

| Method | How to use | Priority |
|--------|-----------|----------|
| Existing profile session | Interactive `emblemai --profile <name>` | 1 |
| Stored profile password | Agent or interactive invocation using profile-scoped `.env` and `.env.keys` | 2 |
| Fresh browser auth | Interactive `emblemai --profile <name>` | 3 |
| Auto-generated agent password | `emblemai --agent --profile <name> ...` with no existing creds | 4 |

## Execution Notes

**Allow sufficient time.** EmblemAI queries may take up to 2 minutes for complex portfolio or cross-chain lookups.

## Backup and Restore

Back up immediately after first wallet creation for any agent-managed profile:

```bash
emblemai --profile motoko
# then /auth
# then choose: 8  (Backup Agent Auth)
```

Restore is profile-aware:

```bash
emblemai --profile motoko --restore-auth ~/emblemai-auth-backup.json
```

If the target profile does not exist yet, restore creates it first.

Treat backup payloads as highly sensitive local operator material.

## Legacy Migration

Older flat-layout installs are migrated transparently into `profiles/default/` on first run. Agents should not panic if file locations change after upgrading; that migration is expected.

## Wallet Addresses

Once authenticated locally, Emblem surfaces wallet addresses across all chains:

| Chain | Address Type |
|-------|-------------|
| **Solana** | Native SPL wallet |
| **EVM** | Single address for ETH, Base, BSC, Polygon |
| **Hedera** | Account ID |
| **Bitcoin** | Taproot, SegWit, and Legacy addresses |

Ask EmblemAI: `"What are my wallet addresses?"` to retrieve all addresses.
