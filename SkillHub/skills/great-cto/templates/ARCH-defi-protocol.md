---
name: ARCH-defi-protocol
description: DeFi protocol ARCH template: subtype + block-ship gate (lending/AMM/bridge/aggregator), security stack (Slither/Echidna/Foundry/Certora), upgradeability matrix, oracle strategy, MEV protection, L2 resilience, custody, bug bounty TVL tier
when_to_use: Writing ARCH for web3 archetype with subtype defi-protocol/bridge-protocol/lending/dex/aggregator
applies_to:
  - web3
---

# ARCH-{slug}.md — DeFi protocol template (web3 archetype)

> **Reader:** the engineer joining post-launch who needs to ship the next protocol upgrade without draining TVL.
> **Source:** `skills/great_cto/templates/ARCH-defi-protocol.md`. Mandatory for `archetype: web3` with subtype `defi-protocol | bridge-protocol | lending | dex | aggregator`.
> Cannot ship to mainnet without `## Upgradeability` + `## Oracle Strategy` + `## Block-ship Gate` (which test must pass with 0 vectors).

## Decision (one sentence)
{What the protocol does in protocol-economics terms, on which chain, with target TVL.}

## Subtype + block-ship gate
| Subtype | Hard block-ship gate | Strong gates (document if any finding) |
|---|---|---|
| Lending protocol | `flash-loan-sim` 0 profitable vectors + `slither-audit` 0 high/crit + `formal-verification` (solvency) + `interest-rate-model` + `l2-resilience` if L2 | `economic-attack-sim`, `liquidation-keeper-decentralization`, `insurance-fund` |
| AMM / DEX | `flash-loan-sim` + `slither-audit` + `formal-verification` (k-invariant) | `economic-attack-sim` (MEV), `gas-optimization` |
| Bridge | `formal-verification` (cross-chain message integrity) + `economic-attack-sim` + `slither-audit` | `l2-resilience` for both sides |
| Aggregator / router | `slither-audit` + `reentrancy-guard` | `economic-attack-sim`, `gas-optimization` |
| Token / vesting / vault (no oracle, no lending) | `slither-audit` + `echidna-fuzz` + `reentrancy-guard` | `formal-verification` for accounting |

## Smart contract security stack
- **Slither** — CI gate: 0 high/critical, SWC-103/104/107/110/113/115/116/124/125 clean. Filter `test|mock`.
- **Foundry fuzz** (`forge test --fuzz-runs 10000`) — invariants on collateral accounting, interest accrual, LTV bounds.
- **Echidna** (`--test-mode assertion --test-limit 50000`) — properties: `totalSupply == sum(balances)`, no negative shares, liquidation-always-profitable-for-keeper.
- **Certora Prover** — formal spec for: solvency invariant (assets ≥ liabilities), interest monotonicity, no-loss-on-liquidation, access-control on critical setters.
- **External audits**: 2 independent firms (Trail of Bits / Spearbit / OpenZeppelin) before mainnet; Code4rena contest pre-launch.

## Upgradeability (decision matrix from web3-pack)
- **Pattern**: {Immutable / UUPS proxy / Transparent / Diamond / Beacon}
- **Why**: {< $1M TVL token → Immutable; $1M+ stateful protocol → UUPS; > 24KB contract → Diamond; many instances → Beacon}
- **Universal discipline**:
  - 48 h timelock on parameter changes, 7 d on logic upgrade or oracle replace, 0 h on `pause()` (separate guardian role, 2-of-3 multisig)
  - Storage gaps (`uint256[50] __gap`) on every implementation
  - Storage layout diff in CI: any reorder/remove/retype blocks merge
  - Upgrade auth path: 4-of-7 Safe multisig → Timelock → Proxy. Signers on hardware wallets, geo-distributed.
  - Maturity off-ramp: documented plan to revoke upgrade authority after N years

## Oracle strategy (if pricing or LTV)
- **Primary**: Chainlink price feeds (heartbeat ≤ 24 h, deviation ≤ 0.5%)
- **Secondary**: Pyth as cross-check; reject if Chainlink ↔ Pyth diverge > 2%
- **TWAP fallback**: Uniswap v3 30-min TWAP for liveness during oracle stale/halt
- **Staleness guards**: revert if `updatedAt < block.timestamp - heartbeat * 1.5`
- **Manipulation resistance**: collateral pricing uses median(Chainlink, Pyth, TWAP); circuit-break on >5% per-block move

## MEV protection
- Liquidations: Dutch auction (no PGA gas wars) OR Flashbots private mempool relay
- Flash-loan attacks: re-read oracle after every external interaction, CEI strict, `nonReentrant` on all entry points
- Sandwich on user actions: share-based deposits/withdrawals (ERC-4626), no slippage on user
- JIT liquidity: liquidation incentive curve flattened (close-factor 50%, bonus 5–8%)

## L2-resilience scenarios (if deploying to L2)
- Sequencer halt > 1 h → oracle TWAP must remain usable; no force-liquidation if oracle stale
- Sequencer censorship → force-inclusion via L1 entrypoint exists
- Reorg up to L1 finality (~13 min on Ethereum) → protocol pauses safely on stale-oracle
- Cross-domain message delays → tested via Foundry fork against the specific L2 stack (OP-stack / Arbitrum Nitro / ZK-stack)

## Custody / admin
- **Protocol admin**: 4-of-7 Safe multisig, signers on Ledger HSMs, geo-distributed, 1 cold backup
- **Timelock**: 48 h on parameter changes, 7 d on upgrade/oracle replace, 0 h on `pause()` (guardian role 2-of-3)
- **Treasury**: separate 5-of-9 Safe; CCSS Level 3 documented in `docs/security/CCSS-classification.md`
- **Key ceremony** transcript signed by witnesses

## Bug bounty (sized to TVL)
| Stage | TVL | Programme |
|---|---|---|
| Pre-launch | n/a | Code4rena / Sherlock contest, $50–250 k pot, 7–14 d |
| Post-launch < $5 M | < $5 M | Immunefi, **critical max $50 k** |
| $5–50 M | $5–50 M | Immunefi, **critical max $250 k** |
| $50–500 M | $50–500 M | Immunefi, **critical max $500 k–1 M** |
| > $500 M | > $500 M | Immunefi, **critical max $1 M–10 M** |

Rules: Immunefi v2.3 severity matrix, payout SLA ≤ 30 d, safe-harbour clause, `SECURITY.md` published.

## Insurance fund / bad debt absorption (if lending or leverage)
- Insurance fund seed: ≥ 0.5% of TVL at launch
- Reserve factor → fund flow on every accrual
- Haircut formula on lender shares if fund < threshold
- Emergency multisig top-up procedure documented
- Fund balance dashboard public

## Out of scope (explicit)
- {e.g. cross-chain — phase 2 with separate bridge audit}
- {e.g. permissioned vaults — needs separate KYC layer}

## Security (cross-link `docs/sec-threats/TM-{slug}.md`)
Critical / High threats and mitigations from threat model.

## Compliance defaults
| Trigger | Add to compliance: |
|---|---|
| Always | `slither-audit`, `echidna-fuzz`, `reentrancy-guard` |
| Lending | `flash-loan-sim`, `interest-rate-model`, `liquidation-keeper-decentralization`, `insurance-fund` |
| L2 deploy | `l2-resilience` |
| Custody / treasury | `key-ceremony`, `ccss` |
| User onboarding | `kyc-aml`, `fatf`, `ofac` |

## Open questions
- {Items to decide before next ARCH revision}
