# EmblemAI Agent Wallet

Review wallet state across 7 blockchains with [EmblemAI](https://emblemvault.ai).

This is the easiest way to give your agent a wallet with profile-scoped local auth, zero-config agent provisioning, and review-first operator workflows. The same Emblem auth system can also log users into apps with wallets, email/password, or social sign-in, while giving each user a wallet-aware account.

## Install

```bash
npm install -g @emblemvault/agentwallet
```

## Usage

```bash
# Interactive mode (browser auth)
emblemai --profile motoko

# Agent mode (zero-config, single-shot)
emblemai --agent --profile motoko -m "What are my wallet addresses?"
```

If more than one profile exists in `~/.emblemai`, every agent-mode invocation must include `--profile <name>`. Agent mode never guesses which wallet identity to use.

## Supported Chains

Solana, Ethereum, Base, BSC, Polygon, Hedera, Bitcoin

## Docs

See [SKILL.md](SKILL.md) for the full reference -- authentication, commands, agent mode, troubleshooting, and wallet-focused review guidance.

If you want to integrate EmblemAI into your own React app, see [../emblem-ai-react/SKILL.md](../emblem-ai-react/SKILL.md).

## Links

- [emblemvault.ai/docs](https://emblemvault.ai/docs) — canonical docs
- [emblemvault.dev](https://emblemvault.dev) — interactive docs
- [npm: @emblemvault/agentwallet](https://www.npmjs.com/package/@emblemvault/agentwallet)
- [GitHub: EmblemCompany](https://github.com/EmblemCompany)
