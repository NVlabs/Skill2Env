# review.json Schema

This is the data contract between Python and Claude. Every field below is
guaranteed to exist in the output. Claude reads this structure; Claude does
NOT invent data that isn't here.

```jsonc
{
  "version": "0.1.0",

  // --- Metadata ---
  "metadata": {
    "generated_at": "2026-03-05T18:00:00Z",
    "data_start": "2025-01-01",
    "data_end": "2025-12-31",
    "total_orders": 5784,
    "total_customers": 2765,
    "total_revenue": 1383651,
    "currency": "USD",
    "revenue_definition": "Net sales after discounts, before tax and shipping"
  },

  // --- Data quality warnings (empty array = no issues) ---
  "data_quality": [
    // Example entries (only present when issues detected):
    // { "type": "partial_period", "period": "2026-02", "days_with_data": 3,
    //   "message": "Latest month (2026-02) has only 3 days of data. MoM comparisons use prior complete months." }
    // { "type": "short_data_span", "days": 45, "message": "Data spans only 45 days..." }
    // { "type": "limited_data_span", "days": 200, "message": "Data spans 200 days (<1 year)..." }
  ],

  // --- Data coverage: which periods are available ---
  "data_coverage": {
    "30d": true,       // true if >=45 days of data exist
    "90d": true,       // true if >=120 days of data exist
    "365d": true       // true if >=400 days of data exist
  },

  // --- Period metrics (one block per available period) ---
  "periods": {
    "30d": {
      "summary": {
        "revenue": 98000,
        "revenue_change": -0.003,       // vs prior 30d
        "orders": 412,
        "orders_change": -0.03,
        "aov": 238,
        "aov_change": -0.001,
        "customers": 287,
        "customers_change": -0.05
      },
      "kpi_tree": {
        "new_customer_revenue": 38000,
        "new_customer_revenue_share": 0.388,
        "new_customers": 95,
        "new_customers_change": -0.08,
        "new_customer_aov": 400,
        "returning_customer_revenue": 60000,
        "returning_customer_revenue_share": 0.612,
        "returning_customers": 192,
        "returning_customers_change": -0.03,
        "returning_customer_aov": 312
      },
      "drivers": {
        "aov_effect": 1200,            // revenue change attributable to AOV
        "volume_effect": -1500,         // revenue change attributable to order count
        "mix_effect": 0                 // revenue change attributable to new/returning mix shift
      }
    },
    "90d": { /* same structure */ },
    "365d": {
      /* same structure as 30d (summary, kpi_tree, drivers) plus: */
      "repeat_purchase_rate": 0.38,   // only in 365d block
      "monthly_trend": [
        { "month": "2025-01", "revenue": 95000, "orders": 420, "aov": 226, "customers": 310, "new_customers": 180, "returning_customers": 130, "days_with_data": 31 },
        // ... only months with actual data (no zero-fill for future months)
        { "month": "2025-12", "revenue": 12000, "orders": 45, "aov": 267, "customers": 38, "new_customers": 10, "returning_customers": 28, "days_with_data": 3, "partial": true }
      ]
    }
  },

  // --- Health checks (powers 🟢/🟡/🔴 markers) ---
  "health": {
    "checks": [
      {
        "id": "monthly_revenue_trend",   // internal only, never expose
        "category": "revenue",
        "severity": "high",
        "result": "watch",              // pass | watch | fail
        "message": "MoM revenue growth: -3.8%",
        "value": -0.038,
        "threshold": 0.0
      }
      // ... more checks
    ],
    "top_issues": [
      // Pre-sorted by severity * impact. Max 10.
      {
        "id": "multi_item_order_rate",
        "category": "product",
        "severity": "high",
        "result": "fail",
        "message": "Multi-item order rate: 0.0%",
        "estimated_annual_impact": 77573
      }
      // ...
    ]
  },

  // --- Pre-computed action candidates ---
  "action_candidates": [
    {
      "action": "Introduce product bundles to increase multi-item orders",
      "source_check": "multi_item_order_rate",  // internal reference
      "severity": "high",
      "estimated_annual_impact": 77573,
      "timeline": "this_month"
    }
    // ... max 10 candidates, sorted by impact
  ]
}
```

## Schema Rules

- `periods` only contains keys for periods where `data_coverage` is `true`
- All `_change` fields are proportional change vs prior period (e.g., 0.08 = +8%)
- `health.checks` contains every check result; `health.top_issues` is a
  filtered/sorted subset (fail and watch only, max 10, sorted by severity × impact)
- `action_candidates` are suggestions from Python; Claude refines, merges, and
  rewrites them in business language for the report
- `monthly_trend` contains only months with actual order data (no zero-fill for future months)
- `monthly_trend` entries with `"partial": true` have less than half the month's days with data
- When `data_quality` is non-empty, mention relevant warnings in Data Notes
