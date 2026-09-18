# DexPaprika CLI Reference

Free DEX data from the terminal. 35 chains, 220+ DEXes, 32M+ tokens, 34M+ pools. No API key needed.

- GitHub: https://github.com/coinpaprika/dexpaprika-cli
- Install: `curl -sSL https://raw.githubusercontent.com/coinpaprika/dexpaprika-cli/main/install.sh | sh`
- Quick start: `dexpaprika-cli onboard`

**For agent use:** Always append `--output json --raw` for machine-readable JSON output.

---

## All commands

| Command | Description | Example |
|---------|-------------|---------|
| `stats` | Global stats (networks, DEXes, pools, tokens) | `dexpaprika-cli stats` |
| `networks` | List all supported networks/chains | `dexpaprika-cli networks` |
| `dexes` | List DEXes on a network | `dexpaprika-cli dexes ethereum` |
| `pools` | List top pools on a network | `dexpaprika-cli pools ethereum --limit 10` |
| `pool-filter` | Filter pools by volume, liquidity, txns, creation date | `dexpaprika-cli pool-filter ethereum --volume-24h-min 100000` |
| `pool` | Get detailed info about a specific pool | `dexpaprika-cli pool ethereum 0x88e6...` |
| `dex-pools` | List pools on a specific DEX | `dexpaprika-cli dex-pools ethereum uniswap_v3` |
| `transactions` | Get recent transactions for a pool | `dexpaprika-cli transactions ethereum 0x88e6...` |
| `pool-ohlcv` | Get OHLCV data for a pool | `dexpaprika-cli pool-ohlcv ethereum 0x88e6... --start 2025-01-27` |
| `token` | Get detailed info about a token | `dexpaprika-cli token ethereum 0xc02a...` |
| `token-pools` | Get pools containing a token | `dexpaprika-cli token-pools ethereum 0xc02a...` |
| `filter-tokens` | Filter tokens by volume, liquidity, FDV, txns, creation date | `dexpaprika-cli filter-tokens ethereum --volume-24h-min 100000` |
| `top-tokens` | Discover top tokens by volume (derived from pools) | `dexpaprika-cli top-tokens ethereum` |
| `prices` | Get batch prices for multiple tokens | `dexpaprika-cli prices ethereum --tokens 0xc02a...,0xa0b8...` |
| `search` | Search tokens, pools, DEXes across all networks | `dexpaprika-cli search USDC` |
| `stream` | Stream real-time token prices via SSE | `dexpaprika-cli stream ethereum 0xc02a...` |
| `stream-reserves` | Stream real-time pool/token reserves via SSE | `dexpaprika-cli stream-reserves ethereum 0x88e6... --method pool_reserves` |
| `status` | Check DexPaprika API health status | `dexpaprika-cli status` |
| `check-update` | Check for CLI updates | `dexpaprika-cli check-update` |
| `attribution` | Get attribution snippets for DexPaprika | `dexpaprika-cli attribution` |
| `shell` | Interactive shell mode (REPL) | `dexpaprika-cli shell` |
| `onboard` | Welcome message and quick start guide | `dexpaprika-cli onboard` |

---

## Search-backed commands and sort fields

`pools`, `pool-filter`, `top-tokens`, and `filter-tokens` call the API's `/search` endpoints (`/networks/{network}/pools/search`, `/networks/{network}/tokens/search`) under the hood. The command names and flags did not change, and the CLI maps legacy sort-field values to the canonical names the search endpoints require:

| Legacy value | Canonical value sent to the API |
|--------------|--------------------------------|
| `volume_usd`, `volume_24h` | `volume_usd_24h` |
| `volume_7d` | `volume_usd_7d` |
| `volume_30d` | `volume_usd_30d` |
| `transactions`, `txns` | `txns_24h` |
| `last_price_change_usd_24h`, `price_change` | `price_change_percentage_24h` |
| `liquidity` | `liquidity_usd` |
| `fdv` | `fdv_usd` |

Canonical values pass through unchanged. Unknown values fall back to `volume_usd_24h`. Note: token search rejects `price_usd` ordering, so `top-tokens --order-by price_usd` falls back to volume. The search endpoints are cursor-paginated, so `--page` has no effect on these four commands; use `--limit` and the CLI's next-cursor hint.

```bash
# Sort flags: pools/top-tokens use --order-by/--sort, pool-filter/filter-tokens use --sort-by/--sort-dir
dexpaprika-cli pools ethereum --order-by volume_usd_24h --sort desc
dexpaprika-cli top-tokens solana --order-by price_change_percentage_24h --sort asc
dexpaprika-cli pool-filter ethereum --volume-24h-min 500000 --sort-by liquidity_usd --sort-dir desc
dexpaprika-cli filter-tokens solana --fdv-min 1000000 --sort-by liquidity_usd
```

---

## Global flags

| Flag | Description |
|------|-------------|
| `-o, --output json` | Output as JSON (default: table) |
| `--raw` | Raw JSON without _meta wrapper (for scripts/piping) |
| `-h, --help` | Command help |
| `-V, --version` | Print version |

---

## Streaming commands

```bash
# Single token prices
dexpaprika-cli stream ethereum 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2

# Multiple tokens: --tokens takes a PATH to a JSON file (max 25 entries),
# e.g. [{"chain": "ethereum", "address": "0xc02a..."}, {"chain": "solana", "address": "JUPy..."}]
dexpaprika-cli stream --tokens watchlist.json

# Limit number of events
dexpaprika-cli stream ethereum 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2 --limit 10

# Reserves: one pool (fires pool_reserves events)
dexpaprika-cli stream-reserves ethereum 0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640 --method pool_reserves

# Reserves: one token across all its pools (fires token_reserves events)
dexpaprika-cli stream-reserves ethereum 0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48 --method token_reserves --limit 10

# Reserves: multiple subscriptions from a JSON file (max 25, methods can be mixed),
# e.g. [{"chain": "ethereum", "address": "0x88e6...", "method": "pool_reserves", "request_id": 1}]
dexpaprika-cli stream-reserves --subscriptions reserves.json
```

`stream-reserves` accepts `--request-id <0..4294967295>` on single-target streams; the server echoes it back on each data event. In the subscriptions file, `request_id` is per entry and defaults to the array index when omitted.

---

## Common token addresses

| Token | Chain | Address |
|-------|-------|---------|
| WETH | ethereum | `0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2` |
| USDC | ethereum | `0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48` |
| SOL | solana | `So11111111111111111111111111111111111111112` |
| USDC | solana | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` |
