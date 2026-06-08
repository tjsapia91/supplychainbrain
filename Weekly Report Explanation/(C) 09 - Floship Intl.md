# Tab 9 — Floship Intl

**Purpose:** International fulfillment via Floship (Hong Kong-based 3PL) — international orders that bypass Amazon/Walmart/Shopify-US fulfillment.

---

## Identity Columns

Same as Amazon US ([[(C) 01 - Amazon US]]): STATUS, BRAND, ABC, PRODUCT, SAP UPC, AMAZON SKU, ASIN.

---

## Stock Columns

| Column | Source | Calculation |
|---|---|---|
| **ON HAND** | `reports/_data/floship/*.csv` — Floship "Product Inventory" export | Direct read |
| **AVAILABLE** | Computed | `On Hand − Committed` |
| **COMMITTED** | Floship | Reserved |
| **ON ORDER (INBOUND)** | Valogix "On Order Total" for FLOSHIP location | |

---

## Velocity + DOS

| Column | Source | Calculation |
|---|---|---|
| **DAILY SALES (THIS ROW)** | Valogix "Forecast 30d / 30" for FLOSHIP location | |
| **DOS** | Computed | `Available / daily_vel` — Floship-only |
| **REORDER POINT** | Valogix per-location ROP | |

---

## Forecast

| Column | Source |
|---|---|
| **12MO FORECAST** | Valogix "Forecast Total (Next 12 Months)" |
| **Monthly forecast cols** | Valogix monthly breakdown |

---

## Source Files

| Data | File |
|---|---|
| Floship on-hand | `reports/_data/floship/Product_Inventory_*.csv` |
| Forecast + history + ROP + on-order | `reports/_data/valogix/schain_itemLocationHistoryForecast_*.csv` (filtered to FLOSHIP location) |

---

## Status Logic

Same as ShipBob — Valogix status with Net Inventory Position for ROP check.
