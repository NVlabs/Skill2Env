# Securities & Savings Bonds Datasets — U.S. Treasury Fiscal Data

## Treasury Securities Auctions Data

**Endpoint:** `/v1/accounting/od/auctions_query`  
**Frequency:** As Needed  
**Date Range:** November 1979 to present

Historical data on Treasury securities auctions including bills, notes, bonds, TIPS, and FRNs.

**Key fields** (this is a wide table — 100+ columns; field names below are verified against the live API):
| Field | Type | Description |
|-------|------|-------------|
| `record_date` | DATE | Auction date |
| `security_type` | STRING | Bill, Note, Bond, TIPS, FRN |
| `security_term` | STRING | e.g., "13-Week", "2-Year", "10-Year" |
| `cusip` | STRING | CUSIP identifier |
| `offering_amt` | CURRENCY | Amount offered |
| `high_yield` | NUMBER | High accepted yield (notes/bonds/TIPS) |
| `high_discnt_rate` | NUMBER | High discount rate (bills) |
| `high_investment_rate` | NUMBER | High investment rate (bills) |
| `bid_to_cover_ratio` | NUMBER | Bid-to-cover ratio |
| `total_accepted` | NUMBER | Total accepted amount |
| `total_tendered` | NUMBER | Total tendered amount |
| `indirect_bidder_accepted` | NUMBER | Indirect bidder amount accepted |
| `direct_bidder_accepted` | NUMBER | Direct bidder amount accepted |
| `primary_dealer_accepted` | NUMBER | Primary dealer amount accepted |
| `issue_date` | DATE | Issue/settlement date |
| `maturity_date` | DATE | Maturity date |

Notes vs. bills carry the rate in different fields: notes/bonds/TIPS populate `high_yield`, while bills populate `high_discnt_rate` / `high_investment_rate` (and leave `high_yield` as `"null"`). There is no single "accepted bid rate" or "indirect percentage" column — bidder figures are dollar amounts, so compute shares yourself (e.g. `indirect_bidder_accepted / total_accepted`).

```python
# Get recent 10-year Treasury note auctions
resp = requests.get(
    "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/auctions_query",
    params={
        "filter": "security_type:eq:Note,security_term:eq:10-Year",
        "fields": "record_date,security_term,high_yield,bid_to_cover_ratio,indirect_bidder_accepted,total_accepted",
        "sort": "-record_date",
        "page[size]": 10
    }
)
df = pd.DataFrame(resp.json()["data"])

# Get all auctions in 2024
resp = requests.get(
    "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/auctions_query",
    params={
        "filter": "record_date:gte:2024-01-01,record_date:lte:2024-12-31",
        "sort": "-record_date",
        "page[size]": 10000
    }
)
```

## Treasury Securities Upcoming Auctions

**Endpoint:** `/v1/accounting/od/upcoming_auctions`  
**Frequency:** As Needed  
**Date Range:** March 2024 to present

Announced but not yet settled auction schedule.

**Key fields:**
| Field | Type | Description |
|-------|------|-------------|
| `auction_date` | DATE | Scheduled auction date |
| `security_type` | STRING | Security type |
| `security_term` | STRING | Maturity term |
| `offering_amt` | CURRENCY | Announced offering amount |

```python
# Get upcoming auctions
resp = requests.get(
    "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/upcoming_auctions",
    params={"sort": "auction_date"}
)
upcoming = pd.DataFrame(resp.json()["data"])
print(upcoming[["auction_date", "security_type", "security_term", "offering_amt"]])
```

## Record-Setting Treasury Securities Auction Data

**Frequency:** As Needed

Tracks auction records (largest, highest rate, lowest rate, etc.) for each security type and term.

## Treasury Securities Buybacks

**Frequency:** As Needed (2 data tables)  
**Date Range:** March 2000 to present

Data on Treasury's secondary market buyback (repurchase) operations. Active since the program's relaunch in 2024.

---

## I Bonds Interest Rates

**Endpoint:** `/v1/accounting/od/i_bonds_interest_rates`  
**Frequency:** Semi-Annual (May and November)  
**Date Range:** September 1998 to present

Composite interest rates for Series I Savings Bonds, including fixed rate and inflation rate components.

**Key fields** (verified against the live API):
| Field | Type | Description |
|-------|------|-------------|
| `earning_period` | STRING | Earning period (`YYYY-MM`) |
| `earning_period_start` | DATE | Start of earning period |
| `earning_period_end` | DATE | End of earning period |
| `issue_year_month` | STRING | Issue cohort (`YYYY-MM`) |
| `fixed_rate` | PERCENTAGE | Fixed rate component |
| `semi_annual_inflation_rate` | PERCENTAGE | Semi-annual CPI-U inflation rate |
| `combined_rate` | PERCENTAGE | Combined composite rate |

There is no `effective_date` / `announcement_date` field — sort and filter on `earning_period_start` (or `earning_period`) instead.

```python
# Current I Bond rates
resp = requests.get(
    "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/i_bonds_interest_rates",
    params={"sort": "-earning_period_start", "page[size]": 5}
)
df = pd.DataFrame(resp.json()["data"])
latest = df.iloc[0]
print(f"Current I Bond rate: {latest['combined_rate']}%")
print(f"  Fixed rate: {latest['fixed_rate']}%")
print(f"  Inflation component: {latest['semi_annual_inflation_rate']}%")
```

## U.S. Treasury Savings Bonds: Issues, Redemptions & Maturities

**Endpoint:** `/v1/accounting/od/savings_bonds_report`  (3 tables)  
**Frequency:** Monthly  
**Date Range:** September 1998 to present

Monthly statistics on Series EE, Series I, and Series HH savings bonds outstanding, issued, and redeemed.

**Key fields:**
| Field | Type | Description |
|-------|------|-------------|
| `record_date` | DATE | Month end date |
| `series_cd` | STRING | Bond series (EE, I, HH) |
| `issued_amt` | CURRENCY | Amount issued |
| `redeemed_amt` | CURRENCY | Amount redeemed |
| `matured_amt` | CURRENCY | Amount matured |
| `outstanding_amt` | CURRENCY | Total outstanding |

## Savings Bonds Value Files

**Frequency:** Semi-Annual  
**Date Range:** May 1992 to present

Files for calculating current redemption values of savings bonds.

## Accrual Savings Bonds Redemption Tables (Discontinued)

**Endpoint:** `/v2/accounting/od/redemption_tables`  
**Frequency:** Discontinued (last updated 2022)  
**Date Range:** March 1999 – May 2023

Monthly redemption value tables for historical savings bonds.

## Savings Bonds Securities Sold (Discontinued)

**Frequency:** Discontinued  
**Date Range:** October 1998 – June 2022

---

## State and Local Government Series (SLGS) Securities

**Endpoint:** `/v1/accounting/od/slgs_statistics`  
**Frequency:** Daily  
**Date Range:** October 1998 to present

SLGS securities outstanding data — non-marketable special purpose securities sold to state and local governments.

## Monthly State and Local Government Series (SLGS) Securities Program

**Frequency:** Monthly  
**Date Range:** March 2014 to present

Monthly statistics on the SLGS program.

---

## Electronic Securities Transactions

**Frequency:** Monthly (8 data tables)  
**Date Range:** January 2000 to present

Electronic book-entry transactions for Treasury securities in the TRADES (Treasury/Reserve Automated Debt Entry System) system.

---

## Federal Investments Program

### Interest Cost by Fund
**Frequency:** Monthly  
**Date Range:** October 2001 to present

Monthly interest cost by government trust fund for invested federal funds.

### Principal Outstanding
**Frequency:** Monthly (2 tables)  
**Date Range:** October 2017 to present

### Statement of Account
**Frequency:** Monthly (3 tables)  
**Date Range:** November 2011 to present

---

## Federal Borrowings Program

### Distribution and Transaction Data
**Frequency:** Daily (2 tables)  
**Date Range:** September 2000 to present

### Interest on Uninvested Funds
**Frequency:** Quarterly  
**Date Range:** December 2016 to present

### Summary General Ledger Balances Report
**Frequency:** Monthly (2 tables)  
**Date Range:** October 2005 to present
