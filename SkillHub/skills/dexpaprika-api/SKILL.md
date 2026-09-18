---
name: dexpaprika-api
description: Access the DexPaprika API, CLI, and streaming service to query DEX data including networks, pools, tokens, and trading activity. Use this skill when making HTTP requests to api.dexpaprika.com or streaming.dexpaprika.com, or when using dexpaprika-cli for blockchain DEX information.
version: 2.0.0
---

# DexPaprika API Skill

> **Freshness check (run once per session, before relying on this skill):** this file is `version: 2.0.0`. Fetch the latest copy's header:
>
> ```bash
> curl -s -r 0-400 https://raw.githubusercontent.com/coinpaprika/skills/main/dexpaprika-api/SKILL.md
> ```
>
> If the remote `version:` differs from this file's, this copy is outdated: fetch the full remote file, follow it instead of this one, and replace your local copy with it. DexPaprika removes endpoints (they return HTTP 410) and reshapes responses; a stale skill points you at dead endpoints.

Free DEX data API covering 35 blockchains, 220+ DEXes, 34M+ liquidity pools, and 32M+ tokens. Built by the CoinPaprika team (operating since 2018). No API key, no registration. Free public tier: 10,000 requests/day. Enterprise tier (api-pro.dexpaprika.com): unlimited requests with API key.

- Documentation: https://docs.dexpaprika.com
- AI Agents showcase: https://agents.dexpaprika.com
- Agent skill files: https://dexpaprika.com/agents/skill.md (REST) and https://dexpaprika.com/agents/streaming/skill.md (SSE)
- GitHub: https://github.com/coinpaprika
- Support: support@coinpaprika.com

> **Field naming note:** URL paths use `network` and `token_address`, but JSON responses return `chain` and `id` for the same values.

---

## Integration options

### Option 1: CLI (recommended for agents)

Install and query in seconds. Best for agents that can run shell commands.

```bash
curl -sSL https://raw.githubusercontent.com/coinpaprika/dexpaprika-cli/main/install.sh | sh
```

Always use `--output json --raw` for machine-readable output. Run `dexpaprika-cli onboard` for an interactive quick-start guide.

Common commands:

```bash
# Search for a token
dexpaprika-cli search USDC --output json --raw

# Get token price
dexpaprika-cli token ethereum 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2 --output json --raw

# Top pools on a network
dexpaprika-cli pools ethereum --limit 10 --output json --raw

# Historical OHLCV for a pool
dexpaprika-cli pool-ohlcv ethereum 0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640 --start 2025-01-27 --output json --raw

# Top tokens on a network (ranked, with multi-timeframe metrics)
dexpaprika-cli top-tokens ethereum --limit 20 --output json --raw
dexpaprika-cli top-tokens solana --order-by price_change_percentage_24h --sort asc --output json --raw

# Filter tokens by volume, FDV, liquidity, txns
dexpaprika-cli filter-tokens ethereum --volume-24h-min 100000 --output json --raw
dexpaprika-cli filter-tokens solana --fdv-min 1000000 --liquidity-usd-min 50000 --output json --raw

# Filter pools by volume, liquidity, txns, creation date
dexpaprika-cli pool-filter ethereum --volume-24h-min 500000 --liquidity-usd-min 50000 --output json --raw

# Batch token prices
dexpaprika-cli prices ethereum --tokens 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2,0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48 --output json --raw

# Stream real-time prices (~1s updates)
dexpaprika-cli stream ethereum 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2

# Stream real-time pool reserves (block-level deltas)
dexpaprika-cli stream-reserves ethereum 0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640 --method pool_reserves

# API health check
dexpaprika-cli status
```

The `pools`, `pool-filter`, `top-tokens`, and `filter-tokens` commands call the `/search` endpoints under the hood. They accept both the canonical sort-field names (`volume_usd_24h`, `txns_24h`, `price_change_percentage_24h`, `fdv_usd`) and the legacy aliases (`volume_usd`, `volume_24h`, `txns`, `price_change`, `fdv`), which the CLI maps to canonical before sending.

For the full CLI command reference, read `references/cli-reference.md`.

### Option 2: REST API

Base URL: `https://api.dexpaprika.com`

No authentication required. All responses are JSON.

```bash
curl -s "https://api.dexpaprika.com/networks/ethereum/tokens/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2" | jq
```

#### Endpoint table

| Need | Endpoint |
|------|----------|
| List all networks | `GET /networks` (returns volume_usd_24h, txns_24h, pools_count per network) |
| DEXes on a network | `GET /networks/{network}/dexes` (returns volume_usd_24h, txns_24h, pools_count per DEX) |
| Top pools on network | `GET /networks/{network}/pools/search` (order_by=volume_usd_24h; rows under `results`, cursor pagination) |
| Filter pools | `GET /networks/{network}/pools/search` (volume_usd_24h/7d/30d, liquidity_usd, txns_24h, creation date filters) |
| Pool details | `GET /networks/{network}/pools/{pool_address}` |
| Pool OHLCV (charts) | `GET /networks/{network}/pools/{pool_address}/ohlcv` |
| Pool transactions | `GET /networks/{network}/pools/{pool_address}/transactions` |
| Token price + data | `GET /networks/{network}/tokens/{token_address}` |
| Pools containing token | `GET /networks/{network}/tokens/{token_address}/pools` |
| Filter tokens | `GET /networks/{network}/tokens/search` (volume_usd_24h, liquidity_usd, fdv_usd, txns_24h, creation date filters) |
| Top tokens on network | `GET /networks/{network}/tokens/search` (order_by=volume_usd_24h/liquidity_usd/txns_24h/fdv_usd/price_change_percentage_24h; rows under `results`, cursor pagination) |
| Filter pools across all networks | `GET /pools/search` (same filters and order_by as the per-network variant) |
| Filter tokens across all networks | `GET /tokens/search` (same filters and order_by as the per-network variant) |
| Batch token prices | `GET /networks/{network}/multi/prices?tokens={addr1},{addr2}` |
| Pools for a DEX | `GET /networks/{network}/dexes/{dex}/pools` |
| Search tokens/pools/DEXes | `GET /search?query={term}` |
| Platform statistics | `GET /stats` |

**Removed endpoints (HTTP 410):** `/networks/{network}/pools`, `/pools`, `/networks/{network}/pools/filter`, `/networks/{network}/tokens/filter`, and `/networks/{network}/tokens/top` are gone. They return HTTP 410 with a pointer to the `/search` replacement. Do not call them.

For the full OpenAPI 3.1 specification with all schemas, parameters, and response types, read `references/openapi.yml`.

### Option 3: MCP Server (for AI IDEs)

Hosted MCP server for Claude Desktop, Cursor, Windsurf, and any MCP client.

Add to `claude_desktop_config.json` or equivalent:

```json
{
  "mcpServers": {
    "dexpaprika": {
      "url": "https://mcp.dexpaprika.com/sse"
    }
  }
}
```

No API key needed. Provides tools for querying networks, pools, tokens, OHLCV, transactions, and search.

Documentation: https://docs.dexpaprika.com/ai-integration/hosted-mcp-server

### Option 4: Streaming API (real-time prices + pool reserves)

Base URL: `https://streaming.dexpaprika.com`

Two SSE feeds share one transport:
- `/sse/prices`: live token price updates (~1 s cadence per asset).
- `/sse/reserves`: block-level pool reserve updates with USD-denominated deltas.

**Limits:** 25 subscriptions per POST connection. 10 concurrent SSE streams per IP. A `ping` event lands every 15 s.

Single token price (GET):
```bash
curl --http1.1 -N "https://streaming.dexpaprika.com/sse/prices?method=token_price&chain=ethereum&address=0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
```

Multiple token prices (POST, up to 25):
```bash
curl --http1.1 -N -X POST "https://streaming.dexpaprika.com/sse/prices" \
  -H "Accept: text/event-stream" -H "Content-Type: application/json" \
  -d '[{"chain":"ethereum","address":"0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2","method":"token_price"}]'
```

Pool reserves (GET):
```bash
curl --http1.1 -N "https://streaming.dexpaprika.com/sse/reserves?method=pool_reserves&chain=ethereum&address=0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640"
```

`token_price` event fields: `address`, `chain`, `price` (USD as string), `timestamp`, `timestamp_price` (both unix seconds). The legacy `t_p` method emits a compact `{a, c, p, t, t_p}` shape on the deprecated `/stream` path only and should not be used in new code.

The reserves feed now emits **method-named events**: the old single `reserve_update` event is gone. Match on the two event names instead:

- `pool_reserves` event (one pool, nested tokens): `chain`, `pool_id`, `block`/`previous_block` (strings; `previous_block` can be omitted), `tokens[]` (each `token_id`, `reserve`/`delta` as strings, `price_usd`/`reserve_usd`/`delta_usd` as numbers), `total_reserve_usd`, `total_delta_usd`, `timestamp`, `block_timestamp` (both unix seconds).
- `token_reserves` event (one token across all its pools, flat): `chain`, `token_id`, `reserve`/`delta` (strings), `block` (string), `price_usd`, `reserve_usd`, `delta_usd`, `updated_at`, `timestamp` (both unix seconds).

Raw integer fields (`reserve`, `delta`, `block`, `previous_block`) exceed `Number.MAX_SAFE_INTEGER`, parse with `BigInt`. A consumer tailing reserves must stop matching `reserve_update` and handle these two event names plus their new timestamp fields.

`request_id` correlation (optional): pass `request_id` as a `uint32` (0..4294967295) on GET via the query string, or per-asset in the POST body (it defaults to the asset's array index). The server echoes it back as a `request_id:` SSE line on data events only. `ping`, `warning`, and `error` events carry no `request_id`.

```bash
# GET with request_id; the value comes back on each pool_reserves event
curl --http1.1 -N "https://streaming.dexpaprika.com/sse/reserves?method=pool_reserves&chain=ethereum&address=0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640&request_id=12345"
```

**Important:** Streaming requires HTTP/1.1. Add `--http1.1` with curl. One invalid asset cancels the entire stream with HTTP 400. SSE parsers must buffer one message between blank-line boundaries before dispatching: both `event:`/`data:` orderings are valid and the server uses either, and a `request_id:` line can appear alongside `event:`/`data:`.

For the full streaming reference (events, errors, parser patterns), read `references/streaming-api.md`.

### Option 5: SDKs

| Language | Repository |
|----------|------------|
| Go | https://github.com/coinpaprika/dexpaprika-sdk-go |
| Python | https://github.com/coinpaprika/dexpaprika-sdk-python |
| TypeScript | https://github.com/coinpaprika/dexpaprika-sdk-ts |
| PHP | https://github.com/coinpaprika/dexpaprika-sdk-php |
| Rust | https://github.com/coinpaprika/dexpaprika-sdk-rust |

---

## Common workflows

### Get a token price

CLI:
```bash
dexpaprika-cli token ethereum 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2 --output json --raw
```

curl:
```bash
curl -s "https://api.dexpaprika.com/networks/ethereum/tokens/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2" | jq '.summary.price_usd'
```

Python:
```python
import requests
r = requests.get("https://api.dexpaprika.com/networks/ethereum/tokens/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2")
token = r.json()
print(f"{token['symbol']}: ${token['summary']['price_usd']}")
```

### Search for a token

```bash
curl -s "https://api.dexpaprika.com/search?query=PEPE" | jq '.tokens[:5]'
```

Note: Search uses fuzzy name+symbol matching. "UNI" returns "Uniswap", "United Stables", etc. Filter by exact `symbol` match client-side.

### Get historical OHLCV for a pool

```bash
curl -s "https://api.dexpaprika.com/networks/ethereum/pools/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640/ohlcv?start=2025-01-01&interval=1h&limit=24" | jq
```

OHLCV params: `start` (required), `end`, `interval` (`1m`|`5m`|`10m`|`15m`|`30m`|`1h`|`6h`|`12h`|`24h`), `limit` (max 366), `inversed` (boolean, inverts price ratio for USD-denominated prices from stablecoin-paired pools).

### Batch prices for multiple tokens

```bash
curl -s "https://api.dexpaprika.com/networks/ethereum/multi/prices?tokens=0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2,0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48" | jq
```

Returns an **ARRAY** (not a keyed object). Max 10 tokens per request.

### Stream real-time prices (Python)

```python
import requests, json

assets = [
    {"chain": "ethereum", "address": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2", "method": "token_price"},
    {"chain": "solana",   "address": "So11111111111111111111111111111111111111112",  "method": "token_price"}
]

r = requests.post("https://streaming.dexpaprika.com/sse/prices",
    headers={"Accept": "text/event-stream", "Content-Type": "application/json"},
    json=assets, stream=True)

# Buffer one SSE message at a time, then dispatch. Both `event:`/`data:`
# line orderings are valid SSE and the server has emitted either, so a
# line-by-line parser that assumes one order will silently mis-dispatch.
msg_lines = []
for line in r.iter_lines(decode_unicode=True):
    if line:
        msg_lines.append(line); continue
    event_type, data_str = "message", None
    for ml in msg_lines:
        if ml.startswith("event:"):
            event_type = ml.split(":", 1)[1].strip()
        elif ml.startswith("data:"):
            data_str = ml[5:].lstrip()
    msg_lines = []
    if event_type == "token_price" and data_str:
        d = json.loads(data_str)
        print(f"{d['chain']} {d['address']}: ${d['price']}")
```

---

## Common token addresses

Do not guess addresses. Use `search` to find tokens, or use these known addresses:

| Token | Chain | Address |
|-------|-------|---------|
| WETH | ethereum | `0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2` |
| USDC | ethereum | `0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48` |
| USDC | polygon | `0x2791bca1f2de4661ed88a30c99a7a9449aa84174` |
| USDC | solana | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` |
| SOL | solana | `So11111111111111111111111111111111111111112` |

## Common network IDs

Always lowercase: `ethereum`, `solana`, `bsc`, `polygon`, `arbitrum`, `base`, `avalanche`, `optimism`, `sui`, `ton`, `tron`.

Full list: `GET /networks` or `dexpaprika-cli networks`.

## Pagination

Two pagination models coexist:

- **Page-based** (`/networks/{network}/dexes`, `/networks/{network}/dexes/{dex}/pools`, `/networks/{network}/tokens/{token_address}/pools`): `?page=1&limit=10&order_by=volume_usd&sort=desc`. Pages are 1-indexed (first page is `page=1`). Max 1000 pages. `order_by` values on these endpoints: `volume_usd`, `price_usd`, `transactions`, `last_price_change_usd_24h`, `created_at`.
- **Cursor-based** (the four `/search` endpoints): pass `limit` plus the `cursor` value from the previous response. Rows arrive under `results`, alongside `has_next_page` and `next_cursor`. `order_by` values are canonical: `volume_usd_24h`, `volume_usd_7d`, `volume_usd_30d`, `liquidity_usd`, `txns_24h`, `created_at`, `price_change_percentage_24h`, plus `price_usd` (pools only) and `fdv_usd` (tokens only). The legacy names (`volume_usd`, `transactions`, `last_price_change_usd_24h`) return HTTP 400 on `/search` endpoints.

## Timestamps

All timestamps support Unix, RFC3339, or `yyyy-mm-dd` format. OHLCV data limited to 366 data points per request.

## Rate limits and errors

- Free tier: 10,000 requests/day. Enterprise (api-pro.dexpaprika.com): unlimited with API key.
- HTTP errors: `200` OK | `400` bad params | `404` not found | `429` rate limited | `500` server error
- **On 429 rate limit:** Wait a few seconds/minutes, then retry. Blocks are temporary. If persistent, contact support@coinpaprika.com.
- Check API health: `dexpaprika-cli status` or `GET https://api.dexpaprika.com/stats`
- Full docs: https://docs.dexpaprika.com
