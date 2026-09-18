# DexPaprika Streaming API Reference

Two SSE feeds share one transport. No API key required.

| Feed | Endpoint | Cadence | Use for |
|---|---|---|---|
| Token prices | `/sse/prices` | ~1s per asset | tickers, portfolios, alerts |
| Pool reserves | `/sse/reserves` | block-level | liquidity dashboards, MEV, real-time TVL |

Base URL: `https://streaming.dexpaprika.com`

---

## Quotas and limits

- **Subscriptions per POST connection:** 25. Larger arrays are rejected with HTTP 400 before any events flow.
  - `POST /sse/prices` rejects with `{"message":"too many assets, max 25 allowed"}`.
  - `POST /sse/reserves` rejects with `{"message":"too many subscriptions"}`.
- **Concurrent SSE streams per IP:** 10. The 11th connection returns `429 {"message":"ip stream limit exceeded"}`.
- **Ping interval:** 15 seconds. A `ping` event keeps idle connections open.

---

## Event types

Either feed can emit any of these:

| Event | Where | Payload shape |
|---|---|---|
| `token_price` | prices feed | `{address, chain, price, timestamp, timestamp_price, token_price}` |
| `pool_reserves` | reserves feed | `{chain, pool_id, block, previous_block, tokens[], total_reserve_usd, total_delta_usd, timestamp, block_timestamp}` |
| `token_reserves` | reserves feed | `{chain, token_id, reserve, delta, block, price_usd, reserve_usd, delta_usd, updated_at, timestamp}` |
| `ping` | both | `{"time": <unix>}` |
| `warning` | both | `{"message": "..."}` (non-fatal notice, e.g. deprecation) |
| `error` | both | `{"message": "..."}` (stream-terminating error) |

The legacy `t_p` event and compact `{a, c, p, t, t_p}` shape exist on the deprecated `/stream` path only.

**Reserves events were restructured.** The old single `reserve_update` event no longer exists. The server now emits one event named after the subscription method:

- `pool_reserves`: fired for a `method=pool_reserves` subscription. Carries a nested `tokens[]` array (one entry per token in the pool, each with `token_id`, `reserve`, `delta`, `price_usd`, `reserve_usd`, `delta_usd`) plus pool-level `block`, `previous_block`, `total_reserve_usd`, `total_delta_usd`, and the new `timestamp` and `block_timestamp` fields.
- `token_reserves`: fired for a `method=token_reserves` subscription. Flat, single-token shape: `token_id`, `reserve`, `delta`, `block`, `price_usd`, `reserve_usd`, `delta_usd`, and the new `updated_at` and `timestamp` fields. No nested array.

A consumer that previously matched `reserve_update` must be updated to match `pool_reserves` and `token_reserves` and to read the new timestamp fields.

### `request_id` correlation

An optional `request_id` lets you correlate events back to the subscription that produced them. It is a `uint32` (range 0..4294967295).

- **GET:** pass `request_id` as a query parameter.
- **POST:** set `request_id` per asset in the body. If omitted, it defaults to that asset's index in the request array.

The server echoes the value back as a dedicated `request_id:` SSE line on **data events only** (`token_price`, `pool_reserves`, `token_reserves`). It is **not** attached to `ping`, `warning`, or `error` events, so a parser must tolerate its absence. On GET, omitting the parameter still produces `request_id: 0` lines on data events, so a parser must also tolerate its presence when it never asked for one.

### Wire-format gotchas

- `block`, `previous_block`, `reserve`, `delta` arrive as **JSON strings**, not numbers. They routinely exceed `Number.MAX_SAFE_INTEGER`. Parse with `BigInt` for arithmetic, or `Number()` for display-only. The USD fields (`price_usd`, `reserve_usd`, `delta_usd`, `total_reserve_usd`, `total_delta_usd`) and the timestamp fields (`timestamp`, `block_timestamp`, `updated_at`) are regular JSON numbers.
- `previous_block` appears on `pool_reserves` events only (`token_reserves` has no such field) and is marked `omitempty` server-side, so parse it defensively rather than assuming it is always present.
- Both orderings of `event:` and `data:` lines within one SSE message are valid per the spec, and the server has used both during the rollout. A `request_id:` line may also appear in the same message. Parsers must buffer one message at a time (split on blank line) and dispatch on the parsed event type, not on field order.

---

## Token prices, single token (GET)

```
GET /sse/prices?method=token_price&chain={network}&address={token_address}
```

| Parameter | Required | Description |
|---|---|---|
| method | yes | `token_price` (current). `t_p` is deprecated. |
| chain | yes | Network ID (`ethereum`, `solana`, `bsc`, etc.) |
| address | yes | Token contract address |
| limit | no | Max number of messages before the server closes the connection |

Example:

```bash
curl --http1.1 -N "https://streaming.dexpaprika.com/sse/prices?method=token_price&chain=ethereum&address=0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
```

---

## Token prices, multiple tokens (POST)

```
POST /sse/prices
Accept: text/event-stream
Content-Type: application/json

[
  {"chain": "ethereum", "address": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2", "method": "token_price"},
  {"chain": "solana",   "address": "So11111111111111111111111111111111111111112",  "method": "token_price"}
]
```

Max 25 entries per request body. One invalid asset cancels the entire stream; validate addresses with REST `GET /search?query=...` first.

---

## Pool reserves, single pool or single token (GET)

```
GET /sse/reserves?method=pool_reserves&chain={network}&address={pool_address}
GET /sse/reserves?method=token_reserves&chain={network}&address={token_address}
```

- `method=pool_reserves`: subscribe to one specific pool. Events fire when that pool's reserves change.
- `method=token_reserves`: subscribe to one token across every pool it sits in (high event volume on major assets like USDC).

---

## Pool reserves, multiple entries (POST)

```
POST /sse/reserves
Accept: text/event-stream
Content-Type: application/json

[
  {"chain": "ethereum", "address": "0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640", "method": "pool_reserves"},
  {"chain": "ethereum", "address": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", "method": "token_reserves"}
]
```

Entries can mix `pool_reserves` and `token_reserves`. Max 25 per request body.

---

## Example wire output

Token price event:
```
event: token_price
data: {"address":"0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2","chain":"ethereum","price":"2145.78","timestamp":1779110450,"timestamp_price":1779110449,"token_price":1779110449}
```

Pool reserves event (block 25,445,005 on a Uniswap V3 USDC/WETH pool, `request_id=12345`):
```
event: pool_reserves
request_id: 12345
data: {"chain":"ethereum","pool_id":"0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640","block":"25445005","previous_block":"25445004","tokens":[{"token_id":"0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48","reserve":"20267554175020","delta":"312181314","price_usd":1.0000086018651697,"reserve_usd":20267728.51378833,"delta_usd":312.1839993415715},{"token_id":"0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2","reserve":"38185564889605351116310","delta":"-187888867058651209","price_usd":1661.0500503604078,"reserve_usd":63428134.48291959,"delta_usd":-312.0928120899326}],"total_reserve_usd":83695862.99670792,"total_delta_usd":0.09118725163892805,"timestamp":1782997443,"block_timestamp":1782997439}
```

That event captures one swap: ~$312.18 of USDC came in, ~$312.09 of WETH went out, `total_delta_usd` is the residual (fee + rounding). No on-chain log decoding required. `timestamp` is when the server emitted the event; `block_timestamp` is the block's own time.

Token reserves event (USDC across all its pools, `request_id=777`):
```
event: token_reserves
request_id: 777
data: {"chain":"ethereum","token_id":"0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48","reserve":"190167972986869","delta":"3225671508","block":"25445017","price_usd":0.9999378879562559,"reserve_usd":190156161.26541212,"delta_usd":3225.471154950191,"updated_at":1782997583,"timestamp":1782997585}
```

This is the flat single-token shape: no nested `tokens[]` array, and the aggregate `reserve`/`delta` is for that one token across every pool it sits in.

---

## Python parser (correct event-by-blank-line buffering)

```python
import json, requests

url = "https://streaming.dexpaprika.com/sse/prices"
params = {"method": "token_price", "chain": "ethereum",
          "address": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"}

with requests.get(url, params=params, stream=True) as r:
    r.raise_for_status()
    msg_lines = []
    for line in r.iter_lines(decode_unicode=True):
        if line:
            msg_lines.append(line); continue

        # Blank line: dispatch the buffered message.
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
        elif event_type == "warning" and data_str:
            print("[warning]", json.loads(data_str)["message"])
```

For reserves, match the two method-named events instead. For `event_type == "pool_reserves"` read `d['pool_id']`, `d['block']`, `d['total_delta_usd']`, `d['block_timestamp']`, and iterate `d['tokens']` (use `int(d['tokens'][0]['reserve'])` for raw-amount arithmetic, not `float`). For `event_type == "token_reserves"` the payload is flat: read `d['token_id']`, `d['reserve']`, `d['delta']`, `d['updated_at']`. To correlate, capture the `request_id:` line during buffering (it sits alongside `event:`/`data:` and is absent on `ping`/`warning`/`error`).

---

## JavaScript parser (fetch + for-await)

```javascript
const url = 'https://streaming.dexpaprika.com/sse/prices';
const body = JSON.stringify([
  { chain: 'ethereum', address: '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', method: 'token_price' },
]);

const r = await fetch(url, {
  method: 'POST',
  headers: { Accept: 'text/event-stream', 'Content-Type': 'application/json' },
  body,
});

const decoder = new TextDecoder();
let buffer = '';

for await (const chunk of r.body) {
  buffer += decoder.decode(chunk, { stream: true });
  const messages = buffer.split('\n\n');
  buffer = messages.pop() ?? '';

  for (const msg of messages) {
    const lines = msg.split('\n');
    const eventLine = lines.find(l => l.startsWith('event:'));
    const dataLine  = lines.find(l => l.startsWith('data:'));
    if (!dataLine) continue;

    const eventType = eventLine ? eventLine.slice(6).trim() : 'message';
    if (eventType !== 'token_price') continue;   // skip ping/warning/error

    const d = JSON.parse(dataLine.slice(5).trim());
    console.log(`${d.chain} ${d.address}: $${parseFloat(d.price).toFixed(4)}`);
  }
}
```

`EventSource` does not support POST, so multi-asset subscriptions on the browser require this `fetch` + ReadableStream pattern. Single-asset GET subscriptions work with `EventSource` directly.

For reserves, match `pool_reserves` (nested `d.tokens[]`, use `BigInt(d.tokens[0].reserve)`) or `token_reserves` (flat, use `BigInt(d.reserve)`).

---

## HTTP/1.1 requirement

SSE streaming requires HTTP/1.1. HTTP/2 (curl's default for HTTPS) may not behave correctly with persistent text streams.

- curl: add `--http1.1`.
- Python `requests`: works by default.
- Node.js `fetch`: works by default.

---

## Error codes

| Code | Cause | Body |
|---|---|---|
| 200 | Connected, streaming | (SSE event stream) |
| 400 | Bad params, unsupported chain, asset not found, or one invalid asset in a batch | `{"message": "..."}` |
| 400 | Too many entries in POST body (26+) | `{"message":"too many assets, max 25 allowed"}` (`/sse/prices`) or `{"message":"too many subscriptions"}` (`/sse/reserves`) |
| 429 | IP stream limit exceeded | `{"message":"ip stream limit exceeded"}` |

In-stream errors arrive as `event: error` SSE messages. They terminate the stream.

---

## Deprecated paths

`/stream` and `/reserves/stream` are predecessors. `/stream` still works but emits a one-shot `warning` event on connect telling clients to migrate to `/sse/prices`. `/reserves/stream` was retired and now returns 404. New code must use `/sse/prices` and `/sse/reserves`.

---

## Best practices

- Reconnect with exponential backoff on disconnect. Don't tight-loop.
- Use POST for multi-asset subscriptions: one connection instead of many.
- Parse `price` as a string for decimal precision. Don't `parseFloat` and re-serialize.
- Filter on the `event:` line. Treat unknown events as no-ops so future server-side additions don't break the handler.
- Use `BigInt` for `reserve`, `delta`, `block`, `previous_block` when you need arithmetic.
- On the reserves feed, match `pool_reserves` and `token_reserves`, not the retired `reserve_update`. Pass a `request_id` if you fan out subscriptions and need to route events back; read it from the `request_id:` line on data events.
- Open parallel connections if you need more than 25 subscriptions, up to the 10/IP cap.
- Validate all asset addresses via REST `/search` before streaming. One bad address kills the entire stream.

---

## CLI streaming

The CLI talks to `/sse/prices` and `/sse/reserves` directly (not the deprecated `/stream` path).

```bash
# Single token prices
dexpaprika-cli stream ethereum 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2

# Multiple tokens: --tokens takes a PATH to a JSON file (max 25 entries),
# e.g. [{"chain": "ethereum", "address": "0xc02a..."}, {"chain": "solana", "address": "JUPy..."}]
dexpaprika-cli stream --tokens watchlist.json

# Cap event count for smoke-tests
dexpaprika-cli stream ethereum 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2 --limit 10

# Reserves: one pool (fires pool_reserves events)
dexpaprika-cli stream-reserves ethereum 0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640 --method pool_reserves

# Reserves: one token across all its pools (fires token_reserves events), with request_id correlation
dexpaprika-cli stream-reserves ethereum 0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48 --method token_reserves --request-id 777 --limit 10

# Reserves: multiple subscriptions from a JSON file (max 25, methods can be mixed),
# e.g. [{"chain": "ethereum", "address": "0x88e6...", "method": "pool_reserves", "request_id": 1}]
dexpaprika-cli stream-reserves --subscriptions reserves.json
```
