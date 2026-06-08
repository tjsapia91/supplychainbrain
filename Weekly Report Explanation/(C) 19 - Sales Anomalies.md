# Tab 19 — 📊 Sales Anomalies

**Purpose:** Flags items where current sales velocity deviates significantly from the trailing 12-month baseline — either an unexpected demand surge or a sudden drop.

Two underlying sources:
1. **Amazon** — internal anomaly detection using Sellerboard's 12-month history
2. **Valogix** — Valogix's own exception report (`schain_itemLocationHistoryException_*.csv`)

---

## Columns

| Column | Source | Calculation |
|---|---|---|
| **TYPE** | Computed | "OVER" (current > baseline) or "UNDER" (current < baseline) |
| **CHANNEL** | Various | Amazon / Shopify / Walmart / Floship |
| **BRAND** | item_master | |
| **PRODUCT** | item_master | |
| **SAP UPC** | item lookup | |
| **ASIN** | (Amazon items only) | |
| **CURRENT VELOCITY** | Amazon: SoStocked Adj. Velocity / Valogix: Forecast 30d/30 | |
| **TRAILING 12M AVG** | Sellerboard 12-mo / 365 (Amazon) or Valogix history (Valogix) | Daily-rate baseline |
| **DEVIATION %** | Computed | `(Current − Baseline) / Baseline × 100` |
| **CONFIDENCE** | Computed | Higher when more months of data + tighter variance |
| **POSSIBLE CAUSE** | Notes | Anomaly type — promo / stockout / new launch / seasonality / etc. |

---

## Detection Logic

### Amazon side (Sellerboard-driven)

For each Amazon ASIN with ≥6 months of Sellerboard history:
1. Compute trailing 12-month daily average (excluding stockout months where qty < 25% of mean)
2. Compare to current Adj. Velocity
3. Flag if |deviation| > 50% AND current > 1.0/day (skip low-velocity noise)

### Valogix side

Read `reports/_data/valogix-exceptions/schain_itemLocationHistoryException_*.csv` — Valogix's pre-computed exception report. Each row is an item × location where Valogix's model detected an anomaly.

---

## Why This Matters

Sales anomalies indicate:
- **OVER** — demand surge that the forecast may not capture. Risk: stockout if not addressed.
- **UNDER** — demand drop. Risk: overstock / cash tied up.

Either way, the forecast and PO plans need review for those items.

---

## Source Files

| Data | File |
|---|---|
| Amazon anomalies | Computed from `reports/_data/sellerboard/<brand>/*.csv` + current SoStocked velocity |
| Valogix anomalies | `reports/_data/valogix-exceptions/schain_itemLocationHistoryException_*.csv` |

---

## Reading the Tab

Common views:
- Filter TYPE = OVER + sort DEVIATION % desc → biggest surges
- Filter TYPE = UNDER + sort DEVIATION % asc → biggest drops
- Filter CHANNEL = Amazon → Amazon-only anomalies

For OVER anomalies, immediate action: revisit PO qty, consider air freight / staging transfer.
For UNDER anomalies, action: investigate cause (listing issue? competitor? seasonality?) before reordering.

---

## Common Causes

| Pattern | Likely cause |
|---|---|
| Spike OVER right after Buy Box win / promo / advertising push | Genuine demand shift — adjust forecast |
| Sudden UNDER with no listing change | Competitor undercut / listing suppressed / out-of-stock at higher tier (oversold) |
| Smooth seasonal pattern flagged as anomaly | Seasonality model missed the trend — review seasonality factors |
| OVER for new-launch items | Expected — new SKUs have no baseline, anything is a spike |
