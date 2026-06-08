# Tab 7 — Walmart

**Purpose:** Walmart Marketplace + WFS (Walmart Fulfillment Services) inventory for NFMD + SS brands.

Two underlying data paths feed this tab:
1. **Valogix** (`WM-NFMD` + `WM-SS` locations) — used for forecast + history + ROP
2. **Walmart Seller Center direct exports** — authoritative for on-hand, aged stock, expiration, sell-through

Walmart direct exports OVERRIDE Valogix on-hand. Valogix forecast/history is preserved.

---

## Identity Columns

Same as Amazon US ([[(C) 01 - Amazon US]]): STATUS, BRAND, ABC, PRODUCT, SAP UPC, AMAZON SKU, ASIN.

(For Walmart, "AMAZON SKU" is the Walmart SKU when available — pipeline reuses the column).

---

## Stock Columns

| Column | Source | Calculation |
|---|---|---|
| **ON HAND** | Walmart `inventory*.xlsx` "Total on hand" — **authoritative override** | Direct from Walmart Seller Center export |
| **AVAILABLE** | Computed | `On Hand − Committed` |
| **COMMITTED** | Walmart inventory file or Valogix | Allocated / reserved |
| **ON ORDER (INBOUND)** | Walmart "Inbound units" (NFMD direct) or Valogix "On Order Total" (SS via Valogix) | |

---

## Velocity + DOS

| Column | Source | Calculation |
|---|---|---|
| **DAILY SALES (THIS ROW)** | Walmart "Daily units sold" (NFMD direct) or Valogix 30-day forecast (SS) | NFMD uses direct Walmart data; SS uses Valogix |
| **DOS** | Walmart "Forecasted days of supply" (NFMD direct) or `Available / daily_vel` (SS) | Walmart provides this directly for NFMD |
| **REORDER POINT** | Valogix per-location ROP | |

---

## Walmart-Specific Columns (visible only on Walmart tab)

| Column | Source | Calculation |
|---|---|---|
| **AGED 180+ DAYS** | `inventoryHealth*.csv` | Sum of ATS 181-270 + 271-365 + 366-450 + 450+ buckets — units that have sat 180+ days. **Candidates for markdown / promo.** |
| **EXPIRING 90D** | `inventoryHealth*.csv` | Sum of "Going to expire in 31 to 60 days" + "Going to expire in 61 to 90 days" — critical for beauty SKUs with shelf life |
| **SELL THRU %** | `inventoryHealth*.csv` | Walmart's 30-day sell-through rate. Higher = healthier. <100% = inventory accumulating faster than selling. |

---

## Forecast

| Column | Source |
|---|---|
| **12MO FORECAST** | Valogix "Forecast Total (Next 12 Months)" — NFMD direct estimates: `monthly_rate × 12` from Walmart's 3-month forecast window |
| **Monthly forecast cols** | Valogix monthly breakdown |

---

## Source Files

| Data | File |
|---|---|
| Walmart direct inventory (NFMD) | `reports/_data/walmart/NFMD/inventory*.xlsx` |
| Walmart direct inventory (SS) | `reports/_data/walmart/SS/inventory*.xlsx` |
| Walmart Inventory Health (aged + expiration) | `reports/_data/walmart/<brand>/inventoryHealth*.csv` |
| Valogix forecast (fallback / forecast preservation) | `reports/_data/valogix/schain_itemLocationHistoryForecast_*.csv` (filtered to WM-NFMD, WM-SS locations) |

---

## NFMD vs SS Differences

| Field | NFMD | SS |
|---|---|---|
| On-hand source | Walmart direct (overrides Valogix) | Walmart direct (overrides Valogix) |
| Velocity source | Walmart "Daily units sold" (more accurate — actual orders) | Valogix 30d forecast / 30 |
| DOS source | Walmart "Forecasted days of supply" | `Available / daily_vel` |
| Forecast source | Valogix 12mo estimate from Walmart 3-month window | Valogix 12mo direct |

---

## Status Logic

Same as ShipBob — Valogix status with Net Inventory Position for ROP check.

---

## Common Walmart Issues

1. **WFS aged stock** — 33+ items currently aged 180+ days. Each week the Inventory Health export should be re-pulled to track these.
2. **Expiration risk** — beauty SKUs with 90-day expiration flagged in EXPIRING 90D column. Watch for liquidation opportunities.
3. **SS Valogix-driven** — until SS Walmart data is wired directly, SS rows use Valogix forecast which may be more conservative than actual sales velocity.
