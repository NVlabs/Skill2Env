# Health Checks Reference

Only checks that the Python backend actively evaluates are listed here.
Three categories: Revenue, Customer, Product.

---

## Revenue Checks (12 implemented)

### monthly_revenue_trend -- Monthly Revenue Trend
- **Severity:** High (3.0x)
- **Thresholds:** PASS: 3 consecutive months MoM growth > 0% | WATCH: latest MoM between -5% and 0% | FAIL: MoM decline > 5% or 3+ consecutive decline months
- **Interpretation:** Measures revenue momentum. Declining MoM signals weakening demand, loss of market share, or seasonal patterns not being leveraged.

### aov_trend -- AOV Trend
- **Severity:** High (3.0x)
- **Thresholds:** PASS: AOV decline < 5%/month | WATCH: 5-10% | FAIL: > 10%
- **Interpretation:** Falling AOV may indicate product mix shifts toward lower-priced items, deeper discounting, or loss of premium customers.

### order_count_trend -- Order Count Trend
- **Severity:** High (3.0x)
- **Thresholds:** PASS: MoM order count > -5% | WATCH: -10% to -5% | FAIL: < -10%
- **Interpretation:** Directly measures demand volume. Combine with AOV trend to determine whether revenue changes are volume-driven or value-driven.

### repeat_customer_revenue_share -- Repeat Customer Revenue Share
- **Severity:** Critical (5.0x)
- **Thresholds:** PASS: repeat revenue > 30% | WATCH: 20-30% | FAIL: < 20%
- **Interpretation:** Low repeat share signals unsustainable acquisition dependency. Healthy ecommerce stores derive 30-45% of revenue from returning customers; top consumable brands reach 60%+.

### revenue_concentration_top10 -- Revenue Concentration (Top 10% Customers)
- **Severity:** Medium (1.5x)
- **Thresholds:** PASS: top 10% customers < 60% of revenue | WATCH: 60-80% | FAIL: > 80%
- **Interpretation:** Extreme customer concentration creates fragility -- losing a few key accounts would materially impact revenue.

### avg_discount_rate_trend -- Average Discount Rate Trend
- **Severity:** High (3.0x)
- **Thresholds:** PASS: avg rate < 15% and no upward trend > 2pt/month | WATCH: 15-25% or 1-2pt/month trend | FAIL: > 25% or > 2pt/month trend
- **Interpretation:** Rising discount rates erode margins and train customers to wait for sales, creating a dangerous dependency cycle. This check subsumes the former PR01 (average discount rate) -- both the level and trend are evaluated here.

### daily_revenue_volatility -- Daily Revenue Volatility (CV)
- **Severity:** Medium (1.5x)
- **Thresholds:** PASS: coefficient of variation < 0.5 | WATCH: 0.5-0.8 | FAIL: > 0.8
- **Interpretation:** High daily volatility makes forecasting unreliable and often indicates over-reliance on promotional spikes rather than steady organic demand.

### large_order_dependency -- Large Order Dependency
- **Severity:** Medium (1.5x)
- **Thresholds:** PASS: largest single order < 5% of period revenue | WATCH: 5-10% | FAIL: > 10%
- **Interpretation:** Large individual orders distort trend metrics and create revenue fragility if those customers don't repeat.

### discounted_order_ratio -- Discounted Order Ratio
- **Severity:** High (3.0x)
- **Thresholds:** PASS: < 40% of orders discounted | WATCH: 40-60% | FAIL: > 60%
- **Interpretation:** High ratios condition customers to expect discounts and undermine full-price conversion. Indicates structural over-reliance on promotions.

### discount_depth_trend -- Discount Depth Trend
- **Severity:** Critical (5.0x)
- **Thresholds:** PASS: monthly avg increase < 1pt | WATCH: 1-2pt/month | FAIL: > 2pt/month
- **Interpretation:** Escalating discount depth signals a dangerous cycle where each promotion must go deeper to maintain conversion, steadily eroding margins and brand value.

### category_margin_variance -- Category Margin Variance
- **Severity:** Medium (1.5x)
- **Thresholds:** PASS: no category with negative gross margin | WATCH: 1 category at break-even | FAIL: any category with negative margin
- **Interpretation:** Negative-margin categories drag down blended profitability. May indicate mispricing, excessive COGS, or promotional over-investment in specific categories.

### free_shipping_threshold_effectiveness -- Free-Shipping Threshold Effectiveness
- **Severity:** High (3.0x)
- **Thresholds:** PASS: > 10% AOV bump for orders near threshold | WATCH: 5-10% | FAIL: < 5%
- **Interpretation:** An effective threshold drives meaningful AOV increases. Weak signal suggests the threshold is set too high (unreachable) or poorly communicated. Optimal threshold is typically 1.2x median AOV.

---

## Customer Checks (5 implemented)

### repeat_purchase_rate -- Repeat Purchase Rate
- **Severity:** Critical (5.0x)
- **Thresholds:** PASS: > 25% of first-time buyers make a second purchase | WATCH: 15-25% | FAIL: < 15%
- **Interpretation:** The single most important retention metric. Repeat purchase conversion is the foundation of all customer lifetime value -- customers who buy a second time have a 45% chance of buying a third.

### champions_loyal_share -- Champions + Loyal Segment Share
- **Severity:** Medium (1.5x)
- **Thresholds:** PASS: > 20% of customers in Champions or Loyal RFM segments | WATCH: 10-20% | FAIL: < 10%
- **Interpretation:** Measures the proportion of high-value engaged customers. Low share indicates retention programs are not cultivating loyalty effectively.

### at_risk_segment_share -- At-Risk Segment Share
- **Severity:** High (3.0x)
- **Thresholds:** PASS: < 25% of customers in At-Risk segment | WATCH: 25-35% | FAIL: > 35%
- **Interpretation:** A large at-risk segment means previously engaged customers are drifting away. Reactivation campaigns are urgent before they become lost.

### lost_segment_share -- Lost Segment Share
- **Severity:** Medium (1.5x)
- **Thresholds:** PASS: < 30% of customers in Lost segment | WATCH: 30-45% | FAIL: > 45%
- **Interpretation:** High lost-customer share is a lagging indicator of chronic retention failure. These customers are unlikely to return without significant win-back investment.

### days_to_second_purchase -- Days to Second Purchase
- **Severity:** High (3.0x)
- **Thresholds:** PASS: median < 60 days | WATCH: 60-90 days | FAIL: > 90 days
- **Interpretation:** Longer gaps to second purchase correlate with lower F2 rates. Post-purchase engagement (email, recommendations) should aim to shorten this window.

---

## Product Checks (6 implemented)

### top20_revenue_concentration -- Top-20% Revenue Concentration
- **Severity:** Medium (1.5x)
- **Thresholds:** PASS: 60-80% of revenue from top 20% products | WATCH: 80-90% or < 50% | FAIL: > 90% or < 40%
- **Interpretation:** A healthy Pareto distribution supports focused inventory and marketing. Extreme concentration means the catalog is too narrow; extreme diffusion means no clear winners.

### converting_sku_rate -- Converting SKU Rate
- **Severity:** High (3.0x)
- **Thresholds:** PASS: > 70% of active SKUs have at least 1 sale | WATCH: 50-70% | FAIL: < 50%
- **Interpretation:** Low converting rate signals catalog bloat -- dead SKUs increase carrying costs, dilute marketing, and degrade customer browsing experience.

### multi_item_order_rate -- Multi-Item Order Rate
- **Severity:** Medium (1.5x)
- **Thresholds:** PASS: > 25% of orders contain 2+ items | WATCH: 15-25% | FAIL: < 15%
- **Interpretation:** Low multi-item rate suggests missed cross-sell opportunities. Improving product adjacency and recommendation logic can lift AOV.

### cross_sell_pair_lift -- Cross-Sell Pair Lift
- **Severity:** Medium (1.5x)
- **Thresholds:** PASS: 3+ product pairs with lift > 2.0 | WATCH: 1-2 pairs | FAIL: no pairs > 1.5
- **Interpretation:** Strong cross-sell pairs indicate actionable affinities for bundling and recommendation strategies that can increase basket size.

### lifecycle_stage_distribution -- Lifecycle Stage Distribution
- **Severity:** Medium (1.5x)
- **Thresholds:** PASS: decline-stage products < 30% of catalog | WATCH: 30-50% | FAIL: > 50%
- **Interpretation:** An aging catalog dominated by declining products signals lack of product innovation and future revenue risk.

### price_tier_distribution -- Price Tier Distribution
- **Severity:** Medium (1.5x)
- **Thresholds:** PASS: products span 3+ distinct price tiers | WATCH: 2 tiers | FAIL: single tier
- **Interpretation:** Multiple price tiers broaden market reach and enable upselling from entry to premium. A single tier limits customer segmentation.

---

## RFM Segment Definitions

Used by champions_loyal_share, at_risk_segment_share, lost_segment_share checks:

| Segment | R Score | F Score | Description |
|---------|---------|---------|-------------|
| Champions | 4-5 | 4-5 | Recent, frequent, high-spend |
| Loyal | 3-4 | 3-4 | Regular purchasers |
| New Customers | 4-5 | 1-2 | Recent first-time buyers |
| Potential | 3 | 2-3 | Could become loyal with engagement |
| At Risk | 1-2 | 3-5 | Were frequent, now inactive |
| Lost | 1-2 | 1-2 | Long inactive, low frequency |

---

## Check → KPI Tree Mapping

Each health check maps to one or more KPI tree nodes. The node's marker
(🟢/🟡/🔴) is determined by the **worst** result among its mapped checks:

- 🟢 = all mapped checks pass
- 🟡 = any mapped check is watch (and none fail)
- 🔴 = any mapped check is fail

### Revenue (root node)

| Check | What it signals |
|-------|----------------|
| monthly_revenue_trend | Overall revenue momentum |
| aov_trend | AOV trend health |
| order_count_trend | Order volume trend |
| daily_revenue_volatility | Revenue stability / predictability |
| large_order_dependency | Large-order dependency risk |
| category_margin_variance | Category margin health |

### New Customer Revenue (branch)

| Check | What it signals |
|-------|----------------|
| repeat_customer_revenue_share | New vs returning revenue balance (inverse: low repeat = high new dependency) |
| revenue_concentration_top10 | Customer concentration risk |

### Existing Customer Revenue (branch)

| Check | What it signals |
|-------|----------------|
| repeat_purchase_rate | Repeat purchase rate -- foundation of repeat revenue |
| champions_loyal_share | High-value customer segment strength |
| at_risk_segment_share | At-risk customer erosion |
| lost_segment_share | Lost customer accumulation |
| days_to_second_purchase | Speed of second purchase |
| repeat_customer_revenue_share | Repeat customer revenue share |

### Discount / Pricing (cross-cutting, affects root)

| Check | What it signals |
|-------|----------------|
| avg_discount_rate_trend | Discount rate level and trend |
| discounted_order_ratio | Breadth of discounting |
| discount_depth_trend | Discount depth escalation |
| free_shipping_threshold_effectiveness | Free-shipping threshold effectiveness |

### Product Mix (cross-cutting, affects AOV branches)

| Check | What it signals |
|-------|----------------|
| top20_revenue_concentration | SKU revenue concentration |
| converting_sku_rate | Catalog utilization |
| multi_item_order_rate | Cross-sell / basket composition |
| cross_sell_pair_lift | Product affinity strength |
| lifecycle_stage_distribution | Product lifecycle balance |
| price_tier_distribution | Price tier coverage |
