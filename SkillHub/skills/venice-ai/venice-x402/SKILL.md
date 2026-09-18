---
name: venice-x402
description: Manage Venice x402 wallet credits. Covers POST /x402/top-up (payment discovery + signed USDC settlement), GET /x402/balance/{walletAddress}, GET /x402/transactions/{walletAddress}, USDC on Base (chain 8453), minimum $5 top-up, transaction types TOP_UP/CHARGE/REFUND, and the x402 v2 PAYMENT-REQUIRED response shape returned by all inference endpoints.
---

# Venice x402 (wallet credits)

x402 is Venice's **wallet-based payment** flow. Pay per request with USDC on Base, no account required. Three admin endpoints plus the protocol-level `402` response returned by every inference endpoint.

| Endpoint | Auth | Purpose |
|---|---|---|
| `POST /x402/top-up` | None (discovery) / `X-402-Payment` (settlement) | Discover payment requirements, then settle a signed USDC transfer. |
| `GET /x402/balance/{walletAddress}` | SIWE (`X-Sign-In-With-X`) | Current USD balance for a wallet. |
| `GET /x402/transactions/{walletAddress}` | SIWE | Paginated ledger: `TOP_UP`, `CHARGE`, `REFUND`. |

For the SIWE header format itself, see [`venice-auth`](../venice-auth/SKILL.md).

## Pay with a wallet: end-to-end

### 1. Call an inference endpoint with no balance → `402`

Any inference endpoint (e.g. `POST /chat/completions`) returns a `402` with structured `topUpInstructions` and `siwxChallenge` when the wallet balance is too low. The `PAYMENT-REQUIRED` response header carries the **x402 v2 `paymentRequired` object** (base64-encoded JSON containing `x402Version`, `error`, `resource`, `accepts[]`, and optional `extensions`) — it is **not** the same payload as the 402 body, which is a richer balance/top-up document.

```json
{
  "error": "Payment required",
  "code": "PAYMENT_REQUIRED",
  "message": "Insufficient x402 balance",
  "suggestedTopUpUsd": 10,
  "minimumTopUpUsd": 5,
  "supportedTokens": ["USDC"],
  "supportedChains": ["base"],
  "topUpInstructions": {
    "step1": "POST /api/v1/x402/top-up with no payment header to get payment requirements",
    "step2": "Sign a USDC transfer authorization using the x402 SDK (createPaymentHeader)",
    "step3": "POST /api/v1/x402/top-up with the signed X-402-Payment header",
    "receiverWallet": "<RECEIVER_WALLET_ADDRESS>",
    "tokenAddress": "<USDC_TOKEN_ADDRESS>",
    "tokenDecimals": 6,
    "network": "eip155:8453",
    "minimumAmountUsd": 5
  },
  "siwxChallenge": {
    "info": { "domain": "api.venice.ai", "statement": "Sign in to Venice AI", ... },
    "supportedChains": ["eip155:8453"]
  }
}
```

### 2. Discover payment requirements — `POST /x402/top-up` (no header)

```bash
curl -X POST https://api.venice.ai/api/v1/x402/top-up
```

Response `402`:

```json
{
  "x402Version": 2,
  "accepts": [{
    "protocol": "x402",
    "version": 2,
    "network": "eip155:8453",
    "asset": "<USDC_TOKEN_ADDRESS>",
    "amount": "5000000",          // base units; USDC = 6 decimals → 5 USDC
    "payTo": "<RECEIVER_WALLET_ADDRESS>"
  }]
}
```

### 3. Sign a USDC transfer → `POST /x402/top-up` with `X-402-Payment`

The **x402 SDK** does the EIP-712 USDC `transferWithAuthorization` signing for you:

```bash
npm install x402
```

```ts
import { createPaymentHeader } from 'x402'
import { Wallet } from 'ethers'

const wallet = new Wallet(process.env.WALLET_KEY!)
// 1. Discover
const discover = await fetch(`${base}/x402/top-up`, { method: 'POST' })
const { accepts: [req] } = await discover.json()

// 2. Sign payment for $10 (write your own amount in base units)
const amount = '10000000' // $10
const header = await createPaymentHeader({ ...req, amount }, wallet)

// 3. Settle
const settle = await fetch(`${base}/x402/top-up`, {
  method: 'POST',
  headers: { 'X-402-Payment': header },
})
const { data } = await settle.json()
console.log(data.newBalance, data.amountCredited, data.paymentId)
```

`200` response:

```json
{
  "success": true,
  "data": {
    "walletAddress": "0x...",
    "amountCredited": 10,
    "newBalance": 22.5,
    "paymentId": "payment_01HZ..."
  }
}
```

### 4. Call inference again — credits are now debited from the wallet

The `venice-x402-client` SDK wraps steps 1–4: it catches `402`, auto-tops-up to a configured amount, and retries.

## `GET /x402/balance/{walletAddress}`

```bash
curl "https://api.venice.ai/api/v1/x402/balance/0xYOUR_WALLET" \
  -H "X-Sign-In-With-X: <base64 siwe>"
```

```json
{
  "success": true,
  "data": {
    "walletAddress": "0x...",
    "balanceUsd": 12.5,
    "canConsume": true,
    "minimumTopUpUsd": 5,
    "suggestedTopUpUsd": 10,
    "diemBalanceUsd": 5.25    // optional — present if the wallet is linked to a Venice account with DIEM
  }
}
```

The SIWE signer **must match** the path wallet — `403` otherwise.

## `GET /x402/transactions/{walletAddress}`

```bash
curl "https://api.venice.ai/api/v1/x402/transactions/0xYOUR_WALLET?limit=50&offset=0" \
  -H "X-Sign-In-With-X: <base64 siwe>"
```

```json
{
  "success": true,
  "data": {
    "walletAddress": "0x...",
    "currentBalance": 12.35,
    "transactions": [
      {
        "id": "ledger_01H...",
        "amount": -0.15,
        "balanceAfter": 12.35,
        "type": "CHARGE",
        "createdAt": "2026-04-03T12:34:56.000Z",
        "requestId": "chatcmpl-...",
        "modelId": "zai-org-glm-5-1"
      },
      {
        "id": "ledger_01H...",
        "amount": 10,
        "balanceAfter": 12.5,
        "type": "TOP_UP",
        "createdAt": "2026-04-03T12:00:00.000Z",
        "requestId": null,
        "modelId": null
      }
    ],
    "pagination": { "limit": 50, "offset": 0, "hasMore": false }
  }
}
```

### Transaction types

| `type` | Sign of `amount` | Meaning |
|---|---|---|
| `TOP_UP` | positive | `/x402/top-up` settlement. |
| `CHARGE` | negative | Inference debit. `requestId` / `modelId` link back to the call. |
| `REFUND` | positive | Failed request refund or manual adjustment. |

## Query parameters

### `/x402/transactions/{walletAddress}`

| Param | Notes |
|---|---|
| `limit` | 1–100. Default 50. |
| `offset` | Number of entries to skip. Default 0. |

Use `offset + limit` and `pagination.hasMore` for paging.

## Constants

- **Chain** — Base mainnet, chain ID `8453` (`eip155:8453`).
- **Token** — USDC (6 decimals). Native USDC on Base; not USDbC.
- **Minimum top-up** — `$5` by default. A small number of allow-listed wallets (e.g. internal test wallets) may have a lower per-wallet override — always use the `minimumTopUpUsd` returned in `topUpInstructions` / `/x402/balance` rather than hardcoding `5`.
- **x402 SDK** — `npm install x402` for raw payment header signing, or `venice-x402-client` for the managed Venice flow.
- **Receiver wallet + token contract** are returned in `topUpInstructions`; don't hardcode them.

## Errors

| Code | Meaning |
|---|---|
| `400` | Below minimum top-up, invalid wallet format, or other validation. |
| `401` | `X-Sign-In-With-X` header is **present** but invalid (bad signature, expired, nonce reuse, unsupported chain) — returned as `X402_SIGN_IN_*` error codes. |
| `402` | Expected **discovery** response on `/x402/top-up` (no payment header), on `/x402/balance` and `/x402/transactions` when the SIWE header is **absent**, and on any inference endpoint when the wallet balance is insufficient. Settlement errors use `INVALID_PAYMENT` / `INVALID_PAYMENT_FORMAT` / `INSUFFICIENT_FUNDS` / `EXPIRED_PAYMENT` codes. |
| `403` | SIWE wallet ≠ path wallet. |
| `429` | Too many top-ups/balance checks. |
| `500` | Settlement failure; retry with a fresh nonce. |

## Gotchas

- Use the **x402 SDK** (`npm install x402`) for signing. Hand-rolling the EIP-712 `transferWithAuthorization` is risky — nonce reuse ⇒ `INVALID_PAYMENT`.
- The SIWE signer wallet must match the `walletAddress` path param on `balance` / `transactions`. Separate wallets can't inspect each other.
- `/x402/top-up` is unauthenticated on the **discovery** call — auth is implicit via the signed `X-402-Payment` header on settlement.
- `balanceUsd` on `/x402/balance` is the **USDC** credit balance only. `diemBalanceUsd`, when present, is a **separate** linked-account number — sum them yourself if you need a combined figure.
- `PAYMENT-REQUIRED` (uppercase, hyphens) is the **header** with base64-encoded x402 `paymentRequired` object; don't confuse it with the body field `code: "PAYMENT_REQUIRED"` (which only appears on insufficient-balance bodies, not on auth-style 402s).
- On `/x402/balance` and `/x402/transactions`, **missing** the SIWE header returns `402` (not 401). Only a present-but-invalid header returns `401` with a `X402_SIGN_IN_*` code.
- The x402 v2 `accepts[].amount` is in **base units** (e.g. `"5000000"` = 5 USDC). Don't multiply by decimals again.
- `DIEM`, `BUNDLED_CREDITS`, and Bearer-account `USD` are independent from wallet credits. For account balance, use [`venice-billing`](../venice-billing/SKILL.md).
