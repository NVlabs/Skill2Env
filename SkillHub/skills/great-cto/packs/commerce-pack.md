---
name: commerce-pack
description: Payment provider decision tree (Stripe/Adyen/Paddle), subscription billing patterns, idempotency rules, fraud detection, PCI-DSS scope reduction (SAQ-A vs SAQ-D), refund/dispute, EU VAT
when_to_use: Building e-commerce, payments, SaaS billing, marketplace. Read at architecture time + by pci-reviewer subagent
applies_to:
  - commerce
---

# Commerce Pack

> Extends `commerce` archetype with payment provider decision tree, subscription billing patterns, fraud detection, idempotency rules, PCI-DSS scope reduction, and tax/compliance for global commerce.
> Auto-loaded when `archetype: commerce` is detected in PROJECT.md.
> Also loaded explicitly via `packs: [commerce-pack]`.

## Decision tree — payment provider

| Need | Pick |
|------|------|
| Global SaaS, dev-friendly API, broad payment method support | **Stripe** |
| EU/global B2C with deep local payment methods (iDEAL, Bancontact, Sofort) | **Adyen** or **Mollie** |
| US in-store + online retail | **Square** |
| Marketplace with split payments | **Stripe Connect** or **Braintree Marketplace** |
| Crypto payments | **Coinbase Commerce**, **BitPay**, **Triple-A** (regulated) |
| One-time digital downloads | **Paddle** or **LemonSqueezy** (handle merchant-of-record + tax for you) |
| Subscription business that wants tax + global reach handled | **Paddle** (merchant of record) |
| Open-source / indie | **Polar.sh** (handles tax, low fees, GitHub-native) |

**Default for new SaaS** without strong reason: Stripe. Best docs, mature API, largest dev community.

**For EU-heavy SaaS**: consider Paddle as merchant-of-record — they handle EU VAT, sales tax in 100+ jurisdictions, chargeback disputes. Saves an accounting team.

## Subscription billing — provider vs custom

| Need | Use |
|------|-----|
| Simple flat-rate or per-seat tiers | **Stripe Billing** (built-in) |
| Usage-based / metered billing (per API call, per GB) | **Stripe Billing** (Meters), **Lago** (open-source), **Stigg**, **Orb** (purpose-built for usage) |
| Complex pricing (hybrid, ramped, tiered, volume discounts) | **Recurly**, **Chargebee**, **Stigg**, **Lago** |
| Self-hosted, want full control | **Lago** (Rails, self-host or cloud) |
| Indie / open-source merchandise | **LemonSqueezy** (pre-Stripe), **Polar.sh** |

**Anti-pattern**: rolling your own subscription engine. Proration + grandfathering + downgrades + tax + invoice generation + dunning is a 6-engineer team for a year. Buy.

## PCI-DSS scope reduction

If you take card payments, you're in PCI scope. Goal: minimise that scope to the smallest possible footprint.

### SAQ-A — easiest, you want this
- You **never** see/store/process card data
- All payment forms hosted by provider (Stripe Elements, Adyen Drop-in)
- Card data goes browser → provider directly
- You only get a token/customer ID

**This should be your default for any new commerce project.** Stripe Elements / Checkout / Adyen Drop-in all support SAQ-A.

### SAQ-A-EP — slightly harder
- Same as SAQ-A but you redirect to provider page (not embed)
- Useful if you can't run JS on the page (e.g. some content management systems)

### SAQ-D-Merchant — avoid unless you must
- You touch card data at any point
- Required if you build custom card forms, store full PAN, or process via terminal

If you're considering SAQ-D, reconsider the architecture. Almost every requirement that "needs" SAQ-D can be solved by tokenisation.

`security-officer` blocks the security gate if PROJECT.md declares `pci-dss` but commerce-pack detects code that takes raw card numbers (looking for patterns like `cardNumber`, `cvc`, `pan` in form handlers).

## Idempotency — non-negotiable

Networks fail. Webhooks retry. Users double-tap. Without idempotency, you charge twice.

### The pattern

Every state-changing API call accepts an idempotency key from the client:

```
POST /api/checkout
Idempotency-Key: <uuid-or-deterministic-string>
```

Server stores: `(idempotency_key, response_body, response_status, created_at)`.

If same key arrives within retention window (e.g. 24 hours), return stored response without re-executing.

### Implementation

```typescript
// Express middleware sketch
async function idempotent(req, res, next) {
  const key = req.header('Idempotency-Key');
  if (!key) return next();
  const cached = await db.idempotency.find({ key });
  if (cached) {
    res.status(cached.status).json(cached.body);
    return;
  }
  // Capture response, store after
  const origJson = res.json.bind(res);
  res.json = (body) => {
    db.idempotency.insert({ key, body, status: res.statusCode, created_at: now() });
    return origJson(body);
  };
  next();
}
```

Stripe uses 24-hour retention, scoped per API key. This is a reasonable default.

**Anti-pattern**: idempotency on `GET` requests. They should already be safe to retry. Idempotency keys are for `POST` / `PUT` / `PATCH`.

## Webhook handling

Payment providers send webhooks for every interesting event (charge succeeded, subscription cancelled, dispute opened). Handle them right.

### Verify signatures

Every webhook MUST be verified before any DB write:

```typescript
import Stripe from 'stripe';
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

app.post('/webhooks/stripe', express.raw({ type: 'application/json' }), (req, res) => {
  const sig = req.header('stripe-signature')!;
  let event;
  try {
    event = stripe.webhooks.constructEvent(req.body, sig, process.env.STRIPE_WEBHOOK_SECRET!);
  } catch (e) {
    return res.status(400).send('Invalid signature');
  }
  // Now safe to process
  handleEvent(event);
  res.status(200).send();
});
```

**Anti-pattern**: trusting the request body without signature check. Anyone can POST to your webhook endpoint with fake event payloads.

### Idempotent webhook handlers

Same event ID may arrive multiple times. Store processed event IDs:

```typescript
async function handleEvent(event) {
  const exists = await db.processedEvents.find({ id: event.id });
  if (exists) return; // already handled
  await processEvent(event);
  await db.processedEvents.insert({ id: event.id, processed_at: now() });
}
```

### Return 200 fast

Webhook endpoint MUST return 2xx within ~5 seconds. If processing takes longer, queue it and return 200 immediately.

```typescript
async function handleEvent(event) {
  await queue.send('payment-events', event); // < 100ms
  // background worker processes
}
```

## Subscription reactivation flow

Reactivation is the highest-revenue lever in subscription B2C — and the most error-prone because it crosses three systems (auth, payments, billing state).

| Case | Stripe pattern | Edge cases |
|------|----------------|------------|
| **Canceled, payment method still valid** | `subscriptions.create` with existing `pm_xxx`; reuse `customer.id` | Verify card not expired (`pm.card.exp_month/year`); if expired, fall to "PM expired" path |
| **Canceled, payment method expired or removed** | `setup_intent` flow → collect new `pm_xxx` → `subscriptions.create` | Don't surprise-charge old card before consent; require fresh `confirm_setup_intent` |
| **Paused (Stripe pause + resume)** | `subscriptions.update(pause_collection=null, resume_at=now)` | Use only if the user paused mid-cycle; do not use after explicit cancel |

**Hard rules** (add to gate:ship):
- Never silently reactivate. Reactivation is always user-initiated; "win-back" emails / links must hit a confirm-screen, never a one-click reactivate.
- Pro-rate or zero-out the first cycle for users who reactivate within 30 days of cancel — anti-pattern is double-charging dunning + reactivation in one cycle.
- Reactivation flow uses **idempotency keys** namespaced as `reactivate:{user_id}:{epoch_day}`. Two clicks within 1 day → one Stripe charge.
- Webhook handler distinguishes `customer.subscription.created` (new) from `customer.subscription.resumed` (reactivation) — different welcome emails, different revenue attribution.
- Track win-back cohort metrics: % reactivated within 30/60/90 days; median LTV uplift. Surface in `/digest` weekly.

## Stripe ↔ DB reconciliation job

Webhooks are best-effort, not authoritative. Run a reconciliation job that pulls Stripe Events API and replays any `event.id` we haven't recorded.

| Aspect | Target |
|--------|--------|
| **Frequency** | Hourly during business hours, daily full-sync at 02:00 UTC |
| **RPO (max data lag)** | 1 hour for active subscriptions, 25 hours for archived |
| **SLA** | Reconciliation must complete within 15 min; alert pages on-call if > 30 min |
| **Drift tolerance** | 0 tolerance for `subscription.status` mismatch; alert immediately |
| **Storage** | `stripe_events_processed(event_id PK, type, created_at, processed_at)` — 90-day retention |
| **Audit trail** | All Stripe API calls + responses logged in `stripe_audit_log` for 7 years (PCI / financial-audit retention) |

Without this job: a missed webhook silently breaks revenue recognition until a user complains. With it: drift is detected within 1 hour and self-heals.

## Refund / dispute workflow

Define this before launch, not after first complaint.

### Refund

- Customer-initiated: button in customer portal calls `POST /api/refund` → your code calls Stripe API
- Support-initiated: support tool with role-based permission, audit log of who refunded what why
- Auto-refund cases (defined in policy): downtime > X hours → auto-refund pro-rata; failed delivery > Y days → auto-refund full

Log every refund decision: who, why, when, related transaction, amount. PCI auditors will ask.

### Dispute (chargeback)

When a customer disputes a charge with their bank:

1. Stripe sends `charge.dispute.created` webhook
2. Your code:
   - Marks order in `disputed` state
   - Optionally pauses related subscription
   - Notifies fraud team via Slack/email
   - Gathers evidence: order details, IP, fingerprint, shipping address, communication logs
3. Submit evidence within deadline (Stripe gives 7-21 days depending on dispute type)
4. Result via `charge.dispute.closed` webhook

Track dispute rate. If > 1% of transactions, your provider may suspend you.

## Fraud detection

| Tool | When |
|------|------|
| **Stripe Radar** | Default if you're on Stripe — built in, no extra integration |
| **Sift** | Best-in-class for B2C, ML-driven scoring across many signals |
| **Signifyd** | Best for e-commerce, offers chargeback guarantee |
| **Castle** | Account takeover protection, login fraud |
| **Adyen RevenueProtect** | If you're on Adyen, similar to Radar |

For new project: Stripe Radar (free tier) or upgrade to Radar for Fraud Teams ($0.07/transaction). Add Sift only if Radar isn't catching enough.

### Manual review queue

Some transactions are ambiguous — too risky to auto-approve, too valuable to auto-decline. Build a review queue:

- Flag transactions where Radar score > X
- Notify analyst via Slack within 1 hour
- Analyst reviews: customer history, shipping address fit, IP geo, device fingerprint
- Decision logged for fraud model retraining

## Multi-currency

Two strategies:

### Single settlement currency (simpler)
- Customer sees prices in their currency (display-only conversion)
- You always charge in USD/EUR
- Currency conversion happens at customer's bank
- Prices may look weird ($9.99 → €8.47) — fine for B2B SaaS

### Multi-currency settlement (better UX)
- You receive funds in customer's currency (or a few major currencies)
- Need a multi-currency bank account or use Stripe/Wise/Mercury
- Pricing per currency: $9.99 USD, €9.99 EUR, £8.99 GBP — choose round numbers per market

**Stripe**: supports multi-currency settlement, automatic conversion to USD/EUR/GBP for payout.

**Tax complication**: pricing per currency means you need to manage VAT-inclusive vs VAT-exclusive display per market. Use Paddle or Stripe Tax to handle this.

## Tax compliance

| Need | Tool |
|------|------|
| US sales tax (50 states + thousands of districts) | **TaxJar**, **Avalara**, or **Stripe Tax** |
| EU VAT (digital services to EU consumers, MOSS or OSS scheme) | **Stripe Tax**, **Quaderno**, or use Paddle (MoR) |
| Global, you don't want to deal with it | **Paddle** or **LemonSqueezy** as merchant of record |

If you're a SaaS with B2C customers in EU and US, you have a tax obligation. Don't ignore it. Tax authorities catch up.

For new SaaS without tax expertise: Paddle / LemonSqueezy as MoR. They charge a higher transaction fee but handle ALL tax. Switch to direct Stripe + Stripe Tax once you have an accounting team.

## Subscription pricing patterns

### Flat-rate per seat
Simple. $X per user per month. Most B2B SaaS.

### Tiered (Free / Pro / Enterprise)
Common. Differentiator: features, limits, support level. Avoid more than 3-4 tiers.

### Usage-based (per API call, per GB, per workflow execution)
Increasingly common for AI/data products. Requires:
- Accurate metering (no over- or under-counting)
- Real-time customer dashboard showing usage
- Caps to prevent surprise bills
- Pre-paid credits OR post-paid invoicing

Tools: Lago, Stigg, Orb, Stripe Billing Meters.

### Hybrid (base + usage)
Base subscription + overage. Common for cloud services. Hardest to implement.

### Per-event / per-resolution
Used by Intercom Fin AI, Zendesk Answer Bot. Customer pays per outcome.

### Anti-pattern: complex pricing on day 1
Start with flat-rate. Add usage-based after you have data on usage patterns and willingness to pay.

## Compliance defaults for `commerce` archetype

| Trigger | Add to compliance |
|---------|-------------------|
| Always | `owasp-api`, `gdpr` (you process customer data) |
| Card payments | `pci-dss-saq-a` (or `saq-d` if scope is wider) |
| US customers | `ccpa` (California), `coppa` (under 13), per-state laws |
| EU customers | `gdpr`, `eu-vat`, `dma` if marketplace gatekeeper |
| Subscription billing | `consumer-rights-directive` (EU 14-day cancellation) |
| Marketplace with sellers | `kyc`, `aml` for sellers, `1099-K` reporting (US) |
| Healthcare commerce | `hipaa` |
| Financial services (lending, brokerage) | `dora` (EU), `sox` (US public co) |

`security-officer` runs the matching checklist when these are set.

## Anti-patterns specific to `commerce` archetype

| Pattern | Why it fails | Fix |
|---------|-------------|-----|
| Storing card numbers in your DB | PCI-DSS violation, breach risk | Use Stripe customer IDs / payment method IDs only |
| No idempotency on checkout | Double charges on retry | Idempotency-Key header, see above |
| Trusting client-side price | User can edit cart, pay $0.01 for $100 item | Server-side price calculation always |
| Sending emails synchronously in checkout | Email service down → checkout fails | Queue emails (BullMQ, SQS, Resend), respond to user fast |
| No webhook signature verification | Attackers send fake "payment succeeded" events | `stripe.webhooks.constructEvent` always |
| Manually applying coupons via search-and-replace | Edge cases, math errors | Stripe Coupons / Promotion Codes |
| Letting subscription be created before payment confirms | Free trial loophole, refund headaches | Use `payment_intent` confirm flow, only activate sub after `succeeded` |
| Not testing the failed-card path | Renewal fails, churn spikes silently | Dunning flow with retry schedule + customer email |
| Storing full address strings | International edge cases (no street numbers in JP, no postal codes in IE) | Use structured address fields per ISO 19160 |

## QA extras provided by this pack

When `archetype: commerce`, `qa-engineer` automatically runs:

- **E2E checkout flow** (Playwright) for happy path + 3-DS challenge + declined card
- **Idempotency proof**: same checkout request twice → one charge
- **Webhook signature verification** test
- **PCI scan**: grep for raw card patterns in code, ban list of `cardNumber`, `cvc`, `pan` in non-test code
- **Load test** (k6) on checkout if `qa-extras: [load-test]`
- **Reconciliation test**: orders in DB match Stripe Dashboard for the test window

## Recommended `PROJECT.md` for new commerce project

```yaml
primary: e-commerce
archetype: commerce
project_size: medium
stack: [typescript, nextjs, stripe, postgres]
team-size: 3
compliance: [pci-dss-saq-a, gdpr, owasp-api]
performance-sla: p95 < 200ms (checkout < 1s end-to-end)
qa-extras: [idempotency, webhook-sig, load-test]
packs: [commerce-pack]
```
