---
name: web3-pack
description: Smart contract security (Slither/Echidna/Foundry/Certora), upgradeability decision matrix (Immutable/UUPS/Diamond/Beacon), oracle strategy (Chainlink/Pyth/TWAP), MEV protection, custody (HSM/MPC/Shamir), L2 resilience
when_to_use: Building smart contracts, DeFi protocols, custody wallets, bridges, CEX exchanges, trading bots — anything with funds at risk on-chain
applies_to:
  - web3
---

# Web3 Domain Pack

> Extends `web3` archetype with domain-specific depth for smart contracts, DeFi protocols, custody wallets, bridge protocols, CEX exchanges, and trading bots.
> Loaded when `packs: [web3-pack]` is in PROJECT.md or auto-loaded for `web3` archetype.

## QA Extras Reference

### `formal-verification` — Mathematical Proof (defi-protocol, bridge-protocol)
- **What**: Prove contract correctness against formal specification
- **Tool**: Certora Prover, K Framework, or Scribble annotations
- **Threshold**: All specified invariants proven; 0 counter-examples
- **Artifacts**: Formal spec file + verification report in `docs/security/`

### `flash-loan-sim` — Flash Loan Attack (defi-protocol)
- **What**: Simulate flash loan attacks against protocol
- **Tool**: Foundry fork test with flash loan provider
- **Scenarios**: Price manipulation, liquidity drain, governance attack, oracle manipulation
- **Threshold**: 0 profitable attack vectors found
- **Report**: Attack simulation log in `docs/security/`

### `economic-attack-sim` — Economic Attack (bridge-protocol, defi-protocol)
- **What**: Simulate economic attacks (MEV, sandwich, front-running)
- **Tool**: Foundry + Flashbots simulation or custom attack scripts
- **Scenarios**: Sandwich attack on swaps, front-running on mints, back-running on oracle updates
- **Threshold**: 0 profitable MEV vectors or documented mitigation for each

### `kill-switch` — Emergency Stop (trading-bot)
- **What**: Verify kill-switch disables all trading activity within SLA
- **Tool**: Trigger kill-switch during active trading simulation
- **Threshold**: All open orders cancelled within 5s, no new orders placed, position exposure capped
- **Test both**: bot-level kill-switch + exchange-level API kill-switch

### `slither-audit` — Static Analysis (smart-contract)
- **What**: Slither static analysis for known vulnerability patterns
- **Tool**: `slither . --filter-paths "test|mock" 2>&1`
- **Threshold**: 0 high/critical findings, all medium findings documented with justification
- **SWC checklist**: SWC-103 (floating pragma), SWC-104 (unchecked return), SWC-107 (reentrancy), SWC-110 (assert), SWC-113 (DoS), SWC-115 (tx.origin), SWC-116 (timestamp), SWC-124 (lack of ctor), SWC-125 (incorrect inheritance)

### `echidna-fuzz` — Property-Based Fuzzing (smart-contract, defi-protocol)
- **What**: Fuzz contract with Echidna for invariant violations
- **Tool**: `echidna . --test-mode assertion --test-limit 50000`
- **Threshold**: 50,000+ runs, 0 invariant violations
- **Properties**: balance invariants, access control, state machine transitions

### `reentrancy-guard` — Reentrancy Audit (smart-contract)
- **What**: Verify all external calls are protected against reentrancy
- **Tool**: Manual audit + Slither reentrancy detector
- **Checklist**: CEI pattern (Checks-Effects-Interactions), ReentrancyGuard on all public functions with external calls, no callbacks in state-changing functions

### `gas-optimization` — Gas Profiling (smart-contract)
- **What**: Profile gas usage per function, identify optimization opportunities
- **Tool**: `forge test --gas-report`
- **Threshold**: No function >500k gas without documented justification
- **Report**: Gas report in `docs/qa-reports/`

### `key-ceremony` — Key Management (custody-wallet)
- **What**: Audit key generation ceremony transcript
- **Checklist**: Multi-party computation (MPC) or Shamir's Secret Sharing, HSM attestation verified, no single point of compromise, ceremony witnesses documented
- **Artifact**: Key ceremony transcript in `docs/security/` (signed by witnesses)

### `sanctions-screening` — Compliance Screening (custody-wallet, cex-exchange)
- **What**: Verify sanctions screening integration
- **Lists**: OFAC SDN, EU consolidated list, UNSC consolidated list
- **SLA**: Screening data updated ≤24h
- **Test**: Submit known sanctioned addresses → verify blocking

### `kyc-aml` — KYC/AML Integration (cex-exchange)
- **What**: Verify KYC/AML flow completeness
- **Checklist**: Identity verification, proof of address, PEP screening, adverse media check, ongoing monitoring, suspicious activity reporting (SAR)
- **Test**: End-to-end KYC flow with test identities

### `order-matching` — Order Book Correctness (cex-exchange)
- **What**: Prove order matching engine correctness
- **Properties**: FIFO/price-time priority, no order duplication, no phantom fills, atomic execution
- **Tool**: Property-based tests + formal specification of matching rules
- **Threshold**: 0 matching errors across 100k+ simulated orders

### `circuit-breaker` — Market Circuit Breaker (cex-exchange, trading-bot)
- **What**: Verify circuit breaker triggers correctly
- **Scenarios**: Flash crash (>10% drop in 1min), liquidity drain, API overload
- **Threshold**: Circuit breaker triggers within configured parameters, graceful degradation confirmed

### `interest-rate-model` — IR Model Fuzzing (defi-protocol — lending)
- **What**: Fuzz interest-rate kink curve and utilization invariants
- **Tool**: Foundry invariant tests with random borrow/repay/liquidate sequences
- **Properties**: utilization ∈ [0, 1] always; borrow APR monotonically non-decreasing in utilization; supply APR ≤ borrow APR × (1 − reserveFactor); rate-update step-bound respected
- **Threshold**: 100k+ runs, 0 violations; gas-cost of `accrueInterest` < 60k

### `liquidation-keeper-decentralization` — Keeper Decentralization (defi-protocol — lending)
- **What**: Verify liquidation cannot be monopolized by a single keeper
- **Checklist**: Public liquidation interface (no allowlist); incentive curve flat enough to prevent PGA gas wars; Dutch auction or batch settlement preferred; keeper bot reference implementation open-sourced; chain census of unique liquidator EOAs over 30 days ≥ 5
- **Threshold**: top-1 keeper share < 50% of liquidations over 30 days post-launch

### `insurance-fund` — Bad-Debt Socialization (defi-protocol)
- **What**: Define and verify the bad-debt absorption mechanism
- **Checklist**: insurance-fund seed funded; reserve-factor → fund flow on accrual; haircut formula on lender shares if fund < threshold; emergency multisig top-up procedure documented; fund balance dashboard public
- **Threshold**: insurance fund covers ≥ 0.5% of TVL at launch; haircut clearly disclosed in T&Cs

### `l2-resilience` — Layer-2 Specific Risks (any web3 deploying to L2)
- **What**: Verify protocol behavior under L2-specific failure modes
- **Scenarios**: sequencer halt > 1h (oracle TWAP must remain usable; no force-liquidation if oracle stale); sequencer censorship (force-inclusion via L1 entrypoint exists); reorg up to L1 finality (~13 min on Ethereum); cross-domain message delays
- **Tool**: Foundry fork tests against the specific L2 stack (OP-stack, Arbitrum Nitro, ZK-stack)
- **Threshold**: protocol pauses safely on stale-oracle (configurable threshold); no liquidations during sequencer halt window; reorg safety property: actions confirmed by L2 batch posted to L1 cannot be reverted by user-side transaction reordering

## Upgradeability Decision Matrix

The single biggest architecture choice for any new contract. Pick at design time, not at audit time.

| Pattern | When to use | Avoid when | Tooling |
|---------|-------------|------------|---------|
| **Immutable** (no proxy) | Single-purpose contract, well-trodden logic, low TVL, security-critical primitives (e.g. token vesting, lock contract) | Any protocol > $1M TVL needing patch path; novel logic with high bug surface | Foundry, hardhat — no special tooling |
| **UUPS proxy** (OpenZeppelin) | Default for stateful protocols at $1M+ TVL; minimal proxy gas overhead; auth lives in implementation (revocable) | Multiple independent feature surfaces that change at different cadences | OZ upgrades plugin, `forge inspect` storage layout diff |
| **Transparent proxy** | Legacy / OZ v3 era; new projects should prefer UUPS | New projects — TP overhead is wasted gas | OZ upgrades plugin |
| **Diamond (EIP-2535)** | > 24 KB contract size limit hit; many independent feature facets | Anything simpler — facet routing is harder to audit and formally verify, fewer reference deployments | diamond-1-hardhat, louper.dev |
| **Beacon proxy** | Many instances of the same logic (e.g. per-vault clones) all upgraded together | Single-instance protocols | OZ BeaconProxy |

**Universal upgrade discipline (any proxy pattern):**
- 48h timelock on parameter changes, 7d on logic upgrade or oracle replace, 0h on `pause()` (separate guardian role, 2-of-3 multisig)
- Storage gaps (`uint256[50] __gap`) on every implementation
- `@custom:oz-upgrades-unsafe-allow` only with documented justification
- Storage layout diff in CI: any upgrade that reorders, removes, or retypes storage slots blocks merge
- Upgrade auth path: 4-of-7 Safe → Timelock → Proxy. Signers on hardware wallets, geo-distributed.
- Maturity off-ramp: documented plan to revoke upgrade authority after N years (some protocols do this; investors increasingly ask)

### Block-ship gate — which one wins for `defi-protocol`?

The pack has overlapping checks (`flash-loan-sim`, `economic-attack-sim`, `formal-verification`, `slither-audit`, `echidna-fuzz`). Disambiguation:

| Subtype | Hard block-ship gate (must pass) | Strong gates (must document if any finding) |
|---------|----------------------------------|------------------------------------------------|
| Token / vesting / vault (no oracle, no lending) | `slither-audit` + `echidna-fuzz` + `reentrancy-guard` | `formal-verification` for accounting invariant |
| Lending protocol | **`flash-loan-sim`** + `slither-audit` + `formal-verification` (solvency) + `interest-rate-model` + `l2-resilience` if L2 | `economic-attack-sim`, `liquidation-keeper-decentralization`, `insurance-fund` |
| AMM / DEX | `flash-loan-sim` + `slither-audit` + `formal-verification` (k-invariant) | `economic-attack-sim` (MEV), `gas-optimization` |
| Bridge | **`formal-verification`** (cross-chain message integrity) + `economic-attack-sim` + `slither-audit` | `l2-resilience` for both sides |
| Aggregator / router | `slither-audit` + `reentrancy-guard` | `economic-attack-sim`, `gas-optimization` |

The lending block-ship gate is **`flash-loan-sim`** with 0 profitable vectors — explicit and bright-line.

## Bug Bounty Sizing (Immunefi tier mapping)

Pre-mainnet contest, post-mainnet ongoing program. Reward sizing must match TVL or you'll attract no whitehat attention.

| Stage | TVL | Recommended program |
|-------|-----|---------------------|
| Pre-launch | N/A | **Code4rena** or **Sherlock** contest, $50–250k pot, 7–14 days |
| Post-launch, < $5M TVL | < $5M | Immunefi or self-hosted, **critical max $50k** |
| $5–50M TVL | $5–50M | Immunefi, **critical max $250k** (Immunefi requires ≥10% of TVL or $1M cap) |
| $50–500M TVL | $50–500M | Immunefi, **critical max $500k–1M** |
| > $500M TVL | > $500M | Immunefi, **critical max $1M–10M** |

**Rules**: rewards proportional to severity (Immunefi v2.3 severity matrix); pay in stablecoin or protocol token at attacker's choice; safe-harbour clause for whitehats; payout SLA ≤ 30 days from confirmed report; published program scope file (`SECURITY.md`).

## Compliance Extras

### `fatf` — FATF Travel Rule
- Verify travel rule implementation for transfers >$1,000 (or jurisdiction threshold)
- Originator + beneficiary info transmitted with transaction
- Integration with travel rule provider (Notabene, Sygna, TRP)

### `ccss` — CryptoCurrency Security Standard
- Classify each component: Level 1 (basic), Level 2 (standard), Level 3 (advanced)
- Key storage audit per CCSS requirements
- Signing protocol verification
- Document classification in `docs/security/CCSS-classification.md`

### `ofac` — Sanctions Compliance
- Wallet screening against OFAC SDN list
- Transaction monitoring for sanctioned jurisdictions
- Blocking mechanism verified (transactions from/to sanctioned addresses rejected)
- Update SLA: ≤24h after list update published

### `kyc-aml-regs` — KYC/AML Regulatory
- Jurisdiction-specific requirements documented
- Customer Due Diligence (CDD) process verified
- Enhanced Due Diligence (EDD) for high-risk customers
- SAR filing process tested
- Record retention: minimum 5 years
