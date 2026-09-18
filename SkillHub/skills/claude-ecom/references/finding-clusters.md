# Finding Clusters for Ecommerce Review


## Purpose and design assumptions

"Finding clusters" are a layer above individual checks: they group multiple related non-pass results (watch/fail) into executive-level themes that are more likely to represent **systemic** problems than isolated metric noise. Many of the biggest ecommerce performance drags show up as *patterns* across merchandising, pricing, and customer behavior rather than as single-metric anomalies.

Retention economics are well-established: improving retention rates can have outsized profit effects, which is why "repeat + churn + LTV" clusters should be treated as board-level issues when multiple sub-signals fire together.

---

## Finding cluster catalog

The check descriptions below use only **implemented checks** (those the Python backend evaluates). The cluster logic is designed so that **multiple** non-pass checks activate a theme, which reduces false alarms and elevates "structural" patterns.

---

### Cluster B -- Promo-Led Growth and Margin Compression

**Member checks (cross-category):**

| Check ID | Brief description (what "non-pass" typically implies) |
|---|---|
| discounted_order_ratio | Promo penetration is high (% of orders with discounts/codes). |
| discount_depth_trend | Discount depth trend is escalating (deeper discounts over time). |
| free_shipping_threshold_effectiveness | Free-shipping threshold is not driving AOV increase effectively. |
| monthly_revenue_trend | Revenue growth appears driven by discounting rather than underlying demand. |
| avg_discount_rate_trend | Average discount rate is rising, eroding margins (subsumes former PR01). |

**Activation rule:** Activate when **>= 2** checks are non-pass, **including at least one** discount intensity check (discounted_order_ratio/discount_depth_trend) **and** at least one revenue or margin signal (monthly_revenue_trend/avg_discount_rate_trend/free_shipping_threshold_effectiveness).

**Root cause hypothesis template:**

> "{n} pricing and margin checks flagged {severity_level}, indicating growth is being purchased through discount depth/frequency and is compressing unit economics. {worst_check} is most critical; validate whether discounting is incremental or cannibalizing full-price demand."

**Recommended approach:** Rebuild pricing/promo governance: segment promos by goal (acquisition vs reactivation vs inventory liquidation), tighten code eligibility, and introduce markdown optimization rather than blanket discounts.

---

### Cluster C -- Assortment and Merchandising Misfit

**Member checks (cross-category):**

| Check ID | Brief description (what "non-pass" typically implies) |
|---|---|
| top20_revenue_concentration | Assortment breadth misfit: too many or too few SKUs for demand (dilution or lack of choice). |
| converting_sku_rate | Converting SKU rate is low: many SKUs are inactive/low-velocity. |
| multi_item_order_rate | Multi-item order rate is low (weak cross-sell / product adjacency). |
| cross_sell_pair_lift | Cross-sell pair lift is weak (no strong product affinities found). |
| lifecycle_stage_distribution | Lifecycle imbalance: too many decline-stage products vs core winners. |
| price_tier_distribution | Price tier distribution is too narrow (limited market reach). |
| category_margin_variance | Category margin variance signals: negative-margin categories drag down profitability. |

**Activation rule:** Activate when **>= 3** checks are non-pass, including at least **two** Product checks and at least **one** of category_margin_variance to ensure this is cross-functional (assortment *and* commercial architecture).

**Root cause hypothesis template:**

> "{n} assortment/merchandising checks flagged {severity_level}, suggesting the catalog is misaligned to demand and value positioning (too much tail, weak launches, or unclear tiers). {worst_check} is most critical; validate whether the issue is breadth (too many SKUs) or depth (missing winners) and whether pricing architecture reinforces or confuses choices."

**Recommended approach:** Do SKU and category rationalization with clear roles (hero/core/seasonal/experimental), improve category-level merchandising (sorting, bundling, cross-sell adjacency), and align internal price ladders to clear "good-better-best" tiers.

---

### Cluster F -- Customer and LTV Engine Weakness

**Member checks (cross-category):**

| Check ID | Brief description (what "non-pass" typically implies) |
|---|---|
| repeat_purchase_rate | Repeat purchase rate is low for the business model/category. |
| champions_loyal_share | Champions + Loyal segment share is low (not enough high-value customers). |
| at_risk_segment_share | At-Risk segment share is high (engaged customers drifting away). |
| lost_segment_share | Lost segment share is high (chronic retention failure). |
| days_to_second_purchase | Days to second purchase is too long (slow second-order conversion). |
| repeat_customer_revenue_share | New vs returning revenue mix is skewed toward new (repeat base not contributing). |
| large_order_dependency | Large order dependency suggests fragile, non-recurring revenue. |

**Activation rule:** Activate when **>= 3** checks are non-pass, including at least one RFM segment check (champions_loyal_share/at_risk_segment_share/lost_segment_share) and at least one value check (repeat_purchase_rate/days_to_second_purchase/repeat_customer_revenue_share).

**Root cause hypothesis template:**

> "{n} customer and value checks flagged {severity_level}, indicating the store is failing to convert first-time buyers into repeat buyers at profitable frequency/velocity. {worst_check} is most critical; diagnose whether the primary break is early repeat (time-to-2nd) or long-run churn, and identify the weakest cohort ({worst_cohort})."

**Recommended approach:** Build a customer "engine" (post-purchase onboarding, replenishment triggers, lifecycle marketing, loyalty economics, and category expansion) and tie it tightly to margin and product strategy.

---

### Cluster G -- Revenue Concentration and Growth Sustainability Risk

**Member checks (cross-category):**

| Check ID | Brief description (what "non-pass" typically implies) |
|---|---|
| order_count_trend | Order count trend declining (demand concentration risk). |
| revenue_concentration_top10 | Revenue concentration: top 10% of customers drive too much revenue. |
| top20_revenue_concentration | Product concentration: top 20% of SKUs overly dominant. |

**Activation rule:** Activate when **>= 2** checks are non-pass, including at least one concentration check (revenue_concentration_top10/top20_revenue_concentration).

**Root cause hypothesis template:**

> "{n} concentration-related checks flagged {severity_level}, suggesting structural fragility: revenue depends on a narrow set of customers/SKUs. {worst_check} is most critical; quantify downside if the top dependency is disrupted and define the diversification path."

**Recommended approach:** Quantify concentration (top-N share) and pursue deliberate diversification (bench products behind hero SKUs, broaden customer base through customer programs).

---

## Standalone checks

These checks are intentionally **not included in cluster activation logic** because they are either single-point-of-failure incidents or highly data-dependent:

| Check ID | Why it is standalone | Brief description |
|---|---|---|
| category_margin_variance | Model-dependent | Category margin variance signal is category-specific; cluster activation would be noise. |
| daily_revenue_volatility | Can be incident-like | Daily revenue volatility may reflect one-off events rather than structural issues. |

---

## Deduplication and overlap rules

1. **Single primary owner.** A check can appear in multiple clusters as **supporting evidence**, but it should have exactly one **Primary Cluster** for activation counting.

2. **Closest actionable root cause.** If two clusters could plausibly own a check, assign ownership based on **closest actionable root cause** (not the symptom). Discount intensity belongs to Cluster B; customer segment drift belongs to Cluster F.

3. **Worst-check selection.** When selecting `{worst_check}` in hypothesis templates, pick the non-pass check with the highest severity (Fail = 2 points, Watch = 1 point; tie-break by estimated $ impact).

---

## Priority ordering when multiple clusters activate simultaneously

1. **B -- Promo-Led Growth and Margin Compression** -- Discount dependency creates a treadmill where revenue requires margin sacrifice.
2. **C -- Assortment and Merchandising Misfit** -- Catalog structure influences both conversion and margin.
3. **F -- Customer and LTV Engine Weakness** -- Customer programs are a compounding engine; failure means growth only through acquisition spend.
4. **G -- Revenue Concentration and Growth Sustainability Risk** -- Concentration is the "second-order" strategic risk.

---

## Practical implementation notes

Implement clusters as deterministic rules over your existing check statuses: each check emits `{pass, watch, fail, n/a}`. Activate a cluster when its rule is met, then generate the executive narrative using the template placeholders (`{n}`, `{worst_check}`, etc.).

To keep clusters robust across seasonality and promo calendars, consider evaluating checks on two windows:

- **Short window** (e.g., trailing 28 days) for incident detection.
- **Long window** (e.g., trailing 90 days) for structural confirmation.

Treat a finding as "structural" only when the cluster activates in both windows or repeatedly across weeks.
