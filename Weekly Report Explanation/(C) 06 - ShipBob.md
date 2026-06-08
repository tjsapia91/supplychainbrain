# Tab 6 — ShipBob

**Purpose:** All SKUs fulfilled via ShipBob 3PL — primarily Shopify orders (MTB / SS / NFMD / LUMOS brand stores).

Note: This tab uses **Valogix data** as the primary source (Valogix tracks ShipBob locations: `SBGA-MT`, `SBGA-SS`, `SBGA-SS-NFMD`). ShipBob's own CSV is used as an authoritative override for on-hand.

---

## Identity Columns

Same as Amazon US ([[(C) 01 - Amazon US]]): STATUS, BRAND, ABC, PRODUCT, SAP UPC, AMAZON SKU, ASIN.

---

## Stock Columns

| Column | Source | Calculation |
|---|---|---|
| **ON HAND** | `reports/_data/shipbob/<brand>/*.csv` | "Total On Hand" from ShipBob inventory export. **Authoritative** — overrides Valogix on-hand. |
| **AVAILABLE** | Computed | `On Hand − Committed` — sellable through Shopify |
| **COMMITTED** | Valogix | Allocated to orders / reserved |
| **ON ORDER (INBOUND)** | Valogix "On Order Total" | Open POs routed to ShipBob (from SAP, mapped through Valogix locations) |

---

## Velocity + DOS

| Column | Source | Calculation |
|---|---|---|
| **DAILY SALES (THIS ROW)** | Valogix "Forecast 30d / 30" | Shopify channel daily velocity |
| **DOS** | Computed | `Available ÷ daily_vel` — does NOT include any other channel |
| **REORDER POINT (ROP)** | Valogix | Direct from Valogix per-location ROP |

---

## Forecast

| Column | Source |
|---|---|
| **12MO FORECAST** | Valogix "Forecast Total (Next 12 Months)" |
| **MONTHLY FORECAST cols** | Valogix monthly forecast breakdown (12 months) |

---

## Open PO + Recommendations

| Column | Source | Calculation |
|---|---|---|
| **OPEN PO** | Valogix On Order — broken out per location | |
| **PO ETA** | SAP Open POs — earliest due date for SBGA-* warehouses | |
| **SUPPLIER PO SUGGEST** | Computed | When ROP triggered: suggested order qty = `12mo_forecast / 12 × (lead_time + buffer)` − on-hand − on-order |

---

## Source Files

| Data | File |
|---|---|
| ShipBob on-hand (authoritative) | `reports/_data/shipbob/<brand>/inventory-export-*.csv` |
| Velocity + forecast + ROP + on-order | `reports/_data/valogix/schain_itemLocationHistoryForecast_*.csv` (filtered to SBGA-* locations) |
| Open SAP POs (warehouse routing) | `reports/_data/sap-open-pos/*.xlsx` |

---

## ShipBob Brand → Group ID Mapping

| Brand | ShipBob Group ID | Valogix Location |
|---|---|---|
| MTB | 385579 | SBGA-MT |
| NFMD | 385954 | SBGA-SS-NFMD |
| SS | 385953 | SBGA-SS |
| LUMOS | 396348 | (separate Shopify store) |

---

## Status Logic

Standard Valogix status calc:
```
status = "STOCKOUT"    if Available <= 0
       = "BELOW ROP"   if Available <= ROP
       = "LOW"         if DOS < 60
       = "HEALTHY"     otherwise
```

Status uses **Net Inventory Position** for ROP comparison: `On Hand + On Order − Committed`. Items with large on-order quantities won't be flagged BELOW ROP if the inbound covers the gap.
