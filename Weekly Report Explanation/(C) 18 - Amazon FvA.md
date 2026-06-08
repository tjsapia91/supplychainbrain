# Tab 18 — 📈 Amazon FvA

**Purpose:** Forecast vs Actual comparison — surfaces SoStocked FvA (Forecast vs Actual) history per ASIN per period. Used to evaluate forecast accuracy and identify items where SoStocked is consistently off.

---

## Columns

| Column | Source | Calculation |
|---|---|---|
| **PERIOD** | SoStocked FvA file | e.g., "May 2026 (MTD)" — current month-to-date, plus closed prior months |
| **BRAND** | item_master | |
| **PRODUCT** | item_master / FvA file | |
| **SAP UPC** | FvA SKU → item_master | |
| **ASIN** | FvA file | |
| **FORECAST UNITS** | SoStocked FvA | What SoStocked predicted for that period |
| **ACTUAL UNITS** | SoStocked FvA | What actually sold |
| **VARIANCE (UNITS)** | Computed | `Actual − Forecast` |
| **VARIANCE %** | Computed | `(Actual − Forecast) / Forecast × 100` |
| **STATUS** | Computed | Within ±10% = ✅ Accurate · ±10-25% = ⚠️ Off · >25% = ❌ Wildly off |

---

## Why This Matters

FvA tells you which items have RELIABLE SoStocked forecasts and which don't:
- **✅ Accurate items** — trust the PFM forecast for PO sizing
- **⚠️ Off items** — apply more buffer when sizing POs
- **❌ Wildly off items** — DON'T trust PFM; use Adj. Velocity × 150 instead

---

## Where The Data Comes From

`reports/_data/sostocked/<brand>/fva-history/*.xlsx` files. The pipeline reads all FvA history files per brand and pivots by ASIN × period.

Current period (e.g., "May 2026 (MTD)") shows month-to-date data; prior periods show closed months.

---

## Source Files

`reports/_data/sostocked/<brand>/fva-history/*.xlsx`

This data is exported from SoStocked separately from the weekly forecast file (different SoStocked report type).

---

## Reading the Tab

Common views:
- Sort by VARIANCE % desc → biggest over-forecasts (SoStocked predicted more than actual)
- Sort by VARIANCE % asc → biggest under-forecasts (SoStocked predicted less than actual)
- Filter STATUS = ❌ Wildly off → items where the PFM forecast can't be trusted
- Look at recent periods → has SoStocked accuracy improved month-over-month?
