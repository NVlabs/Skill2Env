# Datasets Reference

## Overview

The HFM API provides data from four source datasets. Each dataset has a short key used in API calls.

| Key | Full Name | Source | Update Frequency |
|-----|-----------|--------|-----------------|
| `fpf` | SEC Form PF | U.S. Securities and Exchange Commission | Quarterly |
| `tff` | CFTC Traders in Financial Futures | Commodity Futures Trading Commission | Monthly |
| `scoos` | Senior Credit Officer Opinion Survey on Dealer Financing Terms | Federal Reserve Board | Quarterly |
| `ficc` | FICC Sponsored Repo Service Volumes | DTCC Fixed Income Clearing Corp | Daily |

> The `/series/dataset` index reports `long_name: "FormPF"` for all four datasets — an upstream
> labeling quirk, not a real description. Treat the table above as authoritative and verify a
> given series' cadence via its `schedule/observation_frequency` metadata.

---

## SEC Form PF (`fpf`)

The largest and most comprehensive dataset in the HFM. Covers aggregated statistics from Qualifying Hedge Fund filings.

**Who files:** SEC-registered investment advisers with ≥$150M in private fund AUM. Large Hedge Fund Advisers (≥$1.5B in hedge fund AUM) file quarterly; others file annually.

**What is a Qualifying Hedge Fund:** Any hedge fund with net assets ≥$500M advised by a Large Hedge Fund Adviser.

**Data aggregation:** OFR aggregates, rounds, and masks data to avoid disclosure of individual filer information. Winsorization is applied to remove extreme outliers.

**Strategies tracked** (exact scope tokens — verified against `/metadata/mnemonics?dataset=fpf`):
- All Qualifying Hedge Funds (`ALLQHF`)
- Equity (`STRATEGY_EQUITY`)
- Credit (`STRATEGY_CREDIT`)
- Macro (`STRATEGY_MACRO`)
- Relative value (`STRATEGY_RV`)
- Multi-strategy (`STRATEGY_MULTI`)
- Event-driven (`STRATEGY_EVENT`)
- Fund of funds (`STRATEGY_FOF`)
- Other (`STRATEGY_OTHER`)
- Managed futures (`STRATEGY_FUTURES`)

**Mnemonic naming convention:**
```
FPF-{SCOPE}_{METRIC}_{AGGREGATION_TYPE}
```

| Scope | Meaning |
|-------|---------|
| `ALLQHF` | All Qualifying Hedge Funds |
| `STRATEGY_EQUITY` | Equity strategy funds |
| `STRATEGY_CREDIT` | Credit strategy funds |
| `STRATEGY_MACRO` | Macro strategy funds |
| `STRATEGY_RV` / `_FUTURES` / `_MULTI` / `_EVENT` / `_FOF` / `_OTHER` | Other strategies (see list above) |

Leverage, cash-ratio, count and similar per-fund statistics for `ALLQHF` carry a gross-asset
**cohort** segment between scope and metric: `GAVN10` (10 largest funds), `GAVN11TO50`, `GAVN51`
(rest) — e.g. `FPF-ALLQHF_GAVN10_LEVERAGERATIO_AVERAGE`. Dollar totals (`GAV`/`NAV`/`GNE` `_SUM`)
and counterparty series (`PARTY{n}_SUM`) have no cohort segment.

| Metric | Meaning |
|--------|---------|
| `NAV` | Net assets value |
| `GAV` | Gross assets value |
| `GNE` | Gross notional exposure |
| `LEVERAGERATIO` | Leverage ratio (gross assets / net assets) |
| `CASHRATIO` | Unencumbered cash ratio |
| `COUNT` | Number of qualifying funds |
| `PARTY{n}` | n-th largest counterparty's lending |
| `CDSDOWN250BPS` / `CDSUP250BPS` | Stress test: CDS spreads −/+250 bps net impact on NAV |

> Verify metric availability for a scope before requesting — not every metric/cohort/stat
> combination exists, and the API returns `Invalid mnemonic` (plain text) for any that don't.

| Aggregation type | Meaning |
|-----------------|---------|
| `SUM` | Sum (total dollar value) |
| `AVERAGE` | Equal-weighted average across funds (used for `ALLQHF` cohort ratios) |
| `GAVWMEAN` | Gross asset-weighted average (strategy-level ratios) |
| `NAVWMEAN` | Net asset-weighted average (strategy-level ratios) |
| `P5` / `P50` / `P95` | 5th percentile / median / 95th percentile fund |
| `PCTCHANGE` | Percent change |

**Key series examples:**

```
FPF-ALLQHF_NAV_SUM                            All funds: total net assets
FPF-ALLQHF_GAV_SUM                            All funds: total gross assets
FPF-ALLQHF_GNE_SUM                            All funds: gross notional exposure
FPF-ALLQHF_COUNT                              All funds: number of qualifying funds
FPF-ALLQHF_GAVN10_LEVERAGERATIO_AVERAGE       10 largest funds: leverage (equal-weighted)
FPF-ALLQHF_GAVN11TO50_LEVERAGERATIO_AVERAGE   Funds ranked 11–50 by GAV: leverage
FPF-ALLQHF_GAVN51_LEVERAGERATIO_AVERAGE       Remaining funds: leverage
FPF-ALLQHF_CDSUP250BPS_P5                     Stress test: CDS +250bps (5th pct)
FPF-ALLQHF_CDSUP250BPS_P50                    Stress test: CDS +250bps (median)
FPF-ALLQHF_PARTY1_SUM                         Largest counterparty: total lending
FPF-STRATEGY_EQUITY_LEVERAGERATIO_GAVWMEAN    Equity funds: leverage (GAV-weighted)
FPF-STRATEGY_CREDIT_LEVERAGERATIO_GAVWMEAN    Credit funds: leverage (GAV-weighted)
```

**Data note:** Historical data starts Q1 2013 (2013-03-31). Masked values appear as `null`.

---

## CFTC Traders in Financial Futures (`tff`)

Select statistics from the CFTC Commitments of Traders (COT) report covering financial futures.

**What is tracked:** Net positioning of leveraged funds (hedge funds and commodity trading advisors) in financial futures markets, including equity index futures, interest rate futures, currency futures, and other financial instruments.

**Update frequency:** Monthly (derived from weekly CFTC COT releases)

**Key use cases:**
- Monitoring hedge fund positioning in futures markets
- Analyzing speculative vs. commercial positioning
- Tracking changes in financial futures open interest

---

## FRB SCOOS (`scoos`)

Senior Credit Officer Opinion Survey on Dealer Financing Terms conducted by the Federal Reserve Board.

**What it measures:** Survey responses from senior credit officers at major U.S. banks on terms and conditions of their securities financing and over-the-counter derivatives transactions. Covers topics including:
- Availability and terms of credit
- Collateral requirements and haircuts
- Maximum maturity of repos
- Changes in financing terms for hedge funds

**Update frequency:** Quarterly

**Key use cases:**
- Monitoring credit tightening/easing for hedge funds
- Tracking changes in dealer financing conditions
- Understanding repo market conditions from the dealer perspective

---

## FICC Sponsored Repo (`ficc`)

Statistics from the DTCC Fixed Income Clearing Corporation (FICC) Sponsored Repo Service public data.

**What it measures:** Volumes of sponsored repo and reverse repo transactions cleared through FICC's sponsored member program.

| Mnemonic | Description |
|----------|-------------|
| `FICC-SPONSORED_REPO_VOL` | Sponsored repo: repo volume (U.S. dollars) |
| `FICC-SPONSORED_REVREPO_VOL` | Sponsored repo: reverse repo volume (U.S. dollars) |

**Update frequency:** Daily (business-day observations)

**Key use cases:**
- Monitoring growth of the sponsored repo market
- Tracking volumes of centrally cleared repo activity
- Analyzing changes in repo market structure
