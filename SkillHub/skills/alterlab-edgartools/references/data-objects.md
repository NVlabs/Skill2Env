# edgartools — Data Objects Reference

Every SEC filing can be parsed into a structured Python object:

```python
obj = filing.obj()  # returns TenK, EightK, ThirteenF, Form4, etc.
```

## Supported Forms

### Annual & Quarterly Reports (10-K / 10-Q) → TenK / TenQ

```python
tenk = filing.obj()  # or tenq for 10-Q

# Financial statements
tenk.income_statement    # formatted income statement
tenk.balance_sheet       # balance sheet
tenk.financials          # Financials object with all statements

# Document sections
tenk.risk_factors        # full risk factors text
tenk.business            # business description
tenk.mda                 # management discussion & analysis

# Usage via Financials
if tenk.financials:
    income = tenk.financials.income_statement
    balance = tenk.financials.balance_sheet
    cashflow = tenk.financials.cash_flow_statement
```

**Note:** Always check `tenk.financials` before accessing — not all filings have XBRL data.

---

### Current Events (8-K) → EightK

```python
eightk = filing.obj()

eightk.items           # list of reported event codes (e.g. ["2.02", "9.01"])
eightk.press_releases  # attached press releases

print(f"Items: {eightk.items}")
```

Common 8-K item codes:
- `1.01` — Entry into material agreement
- `2.02` — Results of operations (earnings)
- `5.02` — Director/officer changes
- `8.01` — Other events

---

### Insider Trades (Form 4) → Form4 (Ownership)

```python
form4 = filing.obj()

form4.reporting_owner  # insider name
form4.transactions     # buy/sell details with prices, shares, dates

# Get HTML table
html = form4.to_html()
```

Also covers:
- Form 3 — Initial ownership statement
- Form 5 — Annual changes in beneficial ownership

---

### Beneficial Ownership (SC 13D / SC 13G) → Schedule13D / Schedule13G

```python
schedule = filing.obj()

schedule.total_shares                          # aggregate beneficial ownership
schedule.items.item4_purpose_of_transaction    # activist intent (13D only)
schedule.items.item5_interest_in_securities    # ownership percentage
```

- **SC 13D**: Activist investors (5%+ with intent to influence)
- **SC 13G**: Passive holders (5%+)

---

### Institutional Portfolios (13F-HR) → ThirteenF

```python
thirteenf = filing.obj()

thirteenf.infotable    # full holdings DataFrame
thirteenf.total_value  # portfolio market value

# Analyze holdings
holdings_df = thirteenf.infotable
print(holdings_df.head())
print(f"Total AUM: ${thirteenf.total_value/1e9:.1f}B")
```

---

### Proxy & Governance (DEF 14A) → ProxyStatement

```python
proxy = filing.obj()

proxy.executive_compensation  # pay tables (5-year DataFrame)
proxy.proposals               # shareholder vote items
proxy.peo_name                # "Mr. Cook" (principal exec officer)
proxy.peo_total_comp          # CEO total compensation
```

---

### Private Offerings (Form D) → FormD

```python
formd = filing.obj()

formd.offering    # offering details and amounts
formd.recipients  # related persons
```

---

### Crowdfunding Offerings (Form C) → FormC

```python
formc = filing.obj()

formc.offering_information       # target amount, deadline, securities
formc.annual_report_disclosure   # issuer financials (C-AR)
```

---

### Insider Sale Notices (Form 144) → Form144

```python
form144 = filing.obj()

form144.proposed_sale_amount  # shares to be sold
form144.securities            # security details
```

---

### Fund Voting Records (N-PX) → NPX

```python
npx = filing.obj()

npx.votes  # vote records by proposal
```

---

### ABS Distribution Reports (Form 10-D) → TenD (CMBS only)

```python
ten_d = filing.obj()

ten_d.loans           # loan-level DataFrame
ten_d.properties      # property-level DataFrame
ten_d.asset_data.summary()  # pool statistics
```

---

### Municipal Advisors (MA-I) → MunicipalAdvisorForm

```python
mai = filing.obj()
mai.advisor_name  # advisor details
```

---

### Foreign Private Issuers (20-F) → TwentyF

```python
twentyf = filing.obj()
twentyf.financials  # financial data for foreign issuers
```

---

## Complete Form → Class Mapping

| Form | Class | Key Attributes |
|------|-------|----------------|
| 10-K | TenK | `financials`, `income_statement`, `risk_factors`, `business` |
| 10-Q | TenQ | `financials`, `income_statement`, `balance_sheet` |
| 8-K | EightK | `items`, `press_releases` |
| 20-F | TwentyF | `financials` |
| 3 | Form3 | initial ownership |
| 4 | Form4 | `reporting_owner`, `transactions` |
| 5 | Form5 | annual ownership changes |
| DEF 14A | ProxyStatement | `executive_compensation`, `proposals`, `peo_name` |
| 13F-HR | ThirteenF | `infotable`, `total_value` |
| SC 13D | Schedule13D | `total_shares`, `items` |
| SC 13G | Schedule13G | `total_shares` |
| NPORT-P | FundReport | fund portfolio |
| 144 | Form144 | `proposed_sale_amount`, `securities` |
| N-PX | NPX | `votes` |
| Form D | FormD | `offering`, `recipients` |
| Form C | FormC | `offering_information` |
| 10-D | TenD | `loans`, `properties`, `asset_data` |
| MA-I | MunicipalAdvisorForm | `advisor_name` |

---

## How It Works

```python
from edgar import Company

apple = Company("AAPL")
filing = apple.latest("10-K")   # or apple.get_filings(form="10-K").latest()
tenk = filing.obj()          # returns TenK with all sections and financials
```

If a form type is not supported, `filing.obj()` returns `None` (or the filing's raw XBRL object when XBRL is present) — it does not raise. Always guard with `if obj is None`.

## Pattern for Unknown Form Types

```python
obj = filing.obj()
if obj is None:
    # Fallback to raw content
    text = filing.text()
    html = filing.html()
    xbrl = filing.xbrl()
```
