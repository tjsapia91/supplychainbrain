# Tab 17 — 📊 Amazon Sales History

**Purpose:** 12-month rolling sales history per Amazon ASIN, sourced from Sellerboard's "Sales by Product/Month" report. Drives seasonality factors and provides the source data for trend analysis.

---

## Columns

| Column | Source | Calculation |
|---|---|---|
| **BRAND** | item_master / Sellerboard file folder | |
| **PRODUCT** | item_master / Sellerboard | |
| **SAP UPC** | Sellerboard ASIN → item_master lookup | |
| **ASIN** | Sellerboard | Direct |
| **AMAZON SKU** | Sellerboard | Direct |
| **Month columns** (last 12 months) | Sellerboard "Sales by Product/Month" | Units sold per month |
| **12MO TOTAL** | Computed | `SUM(month columns)` |
| **TRAILING AVG** | Computed | `SUM(12mo) / 12` — used as seasonality baseline |
| **RECENT 3MO AVG** | Computed | `SUM(last 3 months) / 3` — used to detect recent demand shifts |
| **MOM CHANGE %** | Computed | `(Recent 3mo − Prior 3mo) / Prior 3mo × 100` |

---

## Why This Matters

The data on this tab drives THREE downstream calculations:
1. **Seasonality factors** — per-month multipliers for `forecast_seasonality_*` columns (used as fallback when SoStocked PFM is missing)
2. **Demand swing classification** — coefficient of variation buckets (STABLE / MODERATE / VOLATILE)
3. **Sales anomaly detection** — current month vs trailing 12-mo baseline (see [[(C) 19 - Sales Anomalies]])

---

## Sellerboard Cadence Warning

This data is a **MONTHLY** pull, not weekly. The pipeline auto-detects file age and emits a warning if the last Sellerboard Monthly file is more than 35 days old:

```
⚠ Sellerboard Monthly is N days old — pull the 3 Monthly reports (monthly cadence)
```

When you see that warning, pull fresh exports from:
- Sellerboard MTB account → Sales by Product → Monthly → Export
- Same for SS + NFMD

Drop into Downloads — classifier auto-routes to `reports/_data/sellerboard/<brand>/`.

---

## Stockout Outlier Protection

When building seasonality factors, the pipeline excludes months where qty < 25% of the 12-mo mean (these are likely stockout months that would falsely depress the seasonality factor). This prevents past stockouts from baking into the forecast.

---

## Source Files

`reports/_data/sellerboard/<brand>/*.csv` — files named like `Sales-by-Product-Monthly-<date>.csv`

Brand assignment from folder structure (`MTB/`, `NFMD/`, `SS/`).

---

## Reading the Tab

Sortable / filterable. Common views:
- Sort by 12MO TOTAL descending → top sellers
- Sort by MOM CHANGE % descending → fastest-growing items
- Filter by BRAND → per-brand sales view
- Look at month-over-month columns to spot seasonal patterns
