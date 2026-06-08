# Tab 16 — 📈 Forecast Pivot

**Purpose:** 9-month forecast totals pivoted by brand × month — answers "how many units will we sell across each brand by month?"

This is the high-level look at where forecasted demand sits.

---

## Layout

A pivot-style table:

| BRAND | MAY 26 | JUN 26 | JUL 26 | AUG 26 | SEP 26 | OCT 26 | NOV 26 | DEC 26 | JAN 27 | 9MO TOTAL |
|---|---|---|---|---|---|---|---|---|---|---|
| MTB | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| SS | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| NFMD | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| **TOTAL** | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

The 9 monthly columns are the same rolling 9-month window used elsewhere in the report.

---

## Calculation

Each cell = `SUM(forecast_m<i> for all items with that brand)`

Source: each item's `forecast_m1..m9` field, which is sourced from the SoStocked PFM "Forecasted Sales Monthly" tab (per `(ASIN, marketplace)` lookup), with fallbacks to seasonality or flat-rate.

The brand assignment comes from `item_master.xlsx` (Branch column).

---

## Companion Views

- Per-item forecasts → Amazon US / Amazon CA / ShipBob / Walmart / Floship tabs (rolling 9 columns + 9MO total)
- Source file → `reports/_data/sostocked/<brand>/projected-forecast-model-*.xlsx` ("Forecasted Sales Monthly" tab)

---

## Common Operations

| Task | What to look at |
|---|---|
| "How much demand does each brand have in Q4?" | Sum OCT/NOV/DEC columns by brand |
| "Which brand has the seasonal spike?" | Compare month-over-month changes within each brand row |
| "Total expected sales across the company over 9 months?" | TOTAL row, 9MO TOTAL column |
