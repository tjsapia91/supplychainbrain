# Weekly Report — Tab-by-Tab Explanation

**File:** `C:\Users\Tom Sapia\MTB-SupplyChain\outputs\latest\weekly-report-2026-05-27.xlsx`
**Generator:** `scripts/build_report.py`
**Auto-chains:** Velocity Watch + ORDER NOW

This folder documents every tab in the weekly report — what each column means, which source file it pulls from, and any calculations applied.

---

## How to Use This Documentation

**For verifying any specific number → start with [[(C) 00 - Data Source Map]].** That doc maps every column to its exact source file and source column.

**For understanding what a tab is for → use the per-tab docs below.**

1. Open the weekly report.
2. Find the tab you have a question about in the list below.
3. Open the matching markdown file — every visible column is explained.
4. For the **exact source file + column** behind any field, cross-reference with [[(C) 00 - Data Source Map]].

---

## Tab Index

| # | Tab | Doc | Purpose |
|---|---|---|---|
| **00** | **(Master)** | **[[(C) 00 - Data Source Map]]** | **Every column → exact source file + source column name. THE precision reference.** |
| 1 | Amazon US | [[(C) 01 - Amazon US]] | Amazon US channel — items needing PO action, watch list, healthy, inactive |
| 2 | Amazon CA | [[(C) 02 - Amazon CA]] | Amazon Canada — same structure as US but routed via Alliance WH |
| 3 | Amazon UK | [[(C) 03 - Amazon UK]] | International placeholder — SAP POs routed to UK warehouse |
| 4 | Amazon AU | [[(C) 04 - Amazon AU]] | International placeholder — SAP POs routed to AU warehouse |
| 5 | Amazon EU | [[(C) 05 - Amazon EU]] | International placeholder — SAP POs routed to EU warehouse |
| 6 | ShipBob | [[(C) 06 - ShipBob]] | Shopify-fulfilled SKUs via ShipBob 3PL |
| 7 | Walmart | [[(C) 07 - Walmart]] | Walmart Marketplace + Inventory Health |
| 8 | TikTok | [[(C) 08 - TikTok]] | TikTok Shop — SAP inventory (TIKTOKMT/TIKTOKSS) + wholesale-derived velocity |
| 9 | Floship Intl | [[(C) 09 - Floship Intl]] | International fulfillment via Floship |
| 10 | 🚨 Priority Actions | [[(C) 10 - Priority Actions]] | All marketplaces, only items needing PO / urgent action |
| 11 | ✅ Action Plan | [[(C) 11 - Action Plan]] | ShipBob send-ins + Supplier POs broken out for execution |
| 12 | 📋 SAP Open POs | [[(C) 12 - SAP Open POs]] | Every open SAP supplier PO with same-day flags |
| 13 | 📦 Replenishment Triggers | [[(C) 13 - Replenishment Triggers]] | SoStocked reorder-point trigger checks |
| 14 | 🏷 Bundles & Custom SKUs | [[(C) 14 - Bundles & Custom SKUs]] | Non-UPC bundles, combos, special accounts |
| 15 | 🗑 Phase-Out, Obsolete & BOMs | [[(C) 15 - Phase-Out Obsolete BOMs]] | Items being phased out (E/Z), zero-vel obsolete, sales BOMs |
| 16 | 📈 Forecast Pivot | [[(C) 16 - Forecast Pivot]] | 9-month forecast totals — brand × month rollup |
| 17 | 📊 Amazon Sales History | [[(C) 17 - Amazon Sales History]] | Sellerboard 12-month sales history per ASIN |
| 18 | 📈 Amazon FvA | [[(C) 18 - Amazon FvA]] | Sellerboard Forecast vs Actual comparison |
| 19 | 📊 Sales Anomalies | [[(C) 19 - Sales Anomalies]] | Over/under anomalies — current vs trailing 12-mo |

---

## Source Files — The Whole Picture

The weekly report pulls from these sources, all of which auto-classify from Downloads:

| Source | Files | What's in it |
|---|---|---|
| **SoStocked** | `reports/_data/sostocked/{MTB,NFMD,SS}/projected-forecast-model-*.xlsx`, `inventory-warehouse-breakdown-*.csv`, `fva-history/` | 9-month monthly forecast, FvA history, regional inventory |
| **Amazon Seller Central US** | `reports/_data/seller-central/US/{MTB,NFMD,SS}/` | FBA Inventory Report (Available, FC Transfer, Inbound stages) + AWD Inventory Report (Available in AWD, Inbound to AWD) |
| **Amazon Seller Central CA** | `reports/_data/seller-central/CA/{MTB,NFMD,SS}/` | CA FBA Health Report (same fields) — CA has no AWD |
| **Sellerboard Monthly** | `reports/_data/sellerboard/{MTB,NFMD,SS}/*.csv` | 12-month sales history by ASIN — drives seasonality + Sales Anomalies |
| **Sellerboard CA Dashboard** | `reports/_data/sellerboard/{MTB,NFMD,SS}/canada/*.csv` | Per-marketplace CA sales — drives CA quarterly seasonality |
| **ShipBob** | `reports/_data/shipbob/{MTB,NFMD,SS,LUMOS}/*.csv` | On-hand at ShipBob 3PL (used for Shopify fulfillment + Amazon emergency backup) |
| **Valogix** | `reports/_data/valogix/schain_itemLocationHistoryForecast_*.csv` | Per-location forecast + history (Floship, Shopify MTB, SS DTC, Walmart) |
| **Valogix Exceptions** | `reports/_data/valogix-exceptions/*.csv` | Sales anomalies flagged by Valogix |
| **SAP Open POs** | `reports/_data/sap-open-pos/*.xlsx` | Every open supplier PO + due date + destination warehouse |
| **SAP Inventory in Warehouse** | `reports/_data/sap-inventory/*.xlsx` | Per-warehouse on-hand snapshot. Drives Alliance WH (ASG-*) staging stock for Amazon CA + TIKTOKMT/TIKTOKSS on-hand for the TikTok tab |
| **Wholesale Monthly Sales** | `reports/_data/wholesale-sales/*.xlsx` | SAP-derived customer-item-level sales detail. Used by the TikTok tab to derive daily velocity from rows where Customer/Vendor Name ∈ TikTok-HL / -MTB / -SS |
| **Walmart Marketplace** | `reports/_data/walmart/{NFMD,SS}/inventory-*.xlsx` | WM direct inventory exports (NFMD + SS) |
| **Walmart Inventory Health** | `reports/_data/walmart/{NFMD,SS}/inventoryHealth*.csv` | WFS aged-stock + expiration breakdown |
| **Floship** | `reports/_data/floship/*.csv` | International fulfillment inventory |
| **Item Master** | `reports/item-master/item_master.xlsx` | SAP item master — 1,384 items, ABC codes, descriptions, branch assignment |
| **Amazon SKU Mapping** | `reports/item-master/amazon-sku-mapping.xlsx` | SAP UPC ↔ Amazon SKU ↔ ASIN crosswalk per brand |

---

## Reading Conventions

- **Hidden columns** — Some columns exist in the file but are hidden by default (cleaner default view). They reference data the formulas use or that's only relevant on other tabs. Each tab doc notes which columns are hidden.
- **Color coding**:
  - 🔴 Brick (red) — Critical / stockout
  - 🟠 Amber — High urgency / watch
  - 🟢 Sage (green) — Healthy / PO covered
  - ⚪ Slate (gray) — Inactive / phase-out
  - ABC colors: teal=A, indigo=B, plum=C, lavender=D, burnt sienna=E, charcoal=Z
- **Brand tags** — MTB (navy) · SS (sage) · NFMD (slate blue)

---

## Key Definitions

| Term | Meaning |
|---|---|
| **FBA Available** | Sellable at Amazon RIGHT NOW (`afn-fulfillable-quantity`). Already NET of reserved units. |
| **FC Transfer** | Units physically at Amazon but in motion between Fulfillment Centers (`Reserved FC Transfer`). |
| **AWD Stock** | Sellable inventory at Amazon Warehousing & Distribution (`Available in AWD`). Amazon's own bulk-storage tier. Takes 1-2 weeks to replenish FBA from here. |
| **AWD Inbound** | Supplier shipment in transit to AWD (`Inbound to AWD`). Not sellable yet. |
| **FBA Pipeline** | Anything inbound to FBA — supplier→FBA + AWD→FBA. Sums `inbound-shipped` + `inbound-received` + `inbound-working`. |
| **ShipBob Backup** | On-hand at ShipBob 3PL, NET of a 30-day Shopify reserve (so Shopify orders aren't starved when we transfer to Amazon). |
| **Alliance WH** | Canadian staging warehouse (`ASG-MTB / ASG-NF / ASG-SS`). Routes to Amazon CA via 60-day staging→Amazon transfer. |
| **Adj. Velocity** | SoStocked's ~30-day stockout-corrected daily sales rate. The operational velocity used for DOS calc. |
| **Daily Demand (PFM)** | Forward-looking daily rate derived from SoStocked's 9-month forecast — used for supplier-PO sizing only. |
| **DOS** | Days of Supply. (FBA + FC Transfer + AWD) ÷ Adj. Velocity (Tommy 2026-05-29 — physical at Amazon only). |
| **Lead Time** | 60 days (staging → Amazon transit). For new supplier POs, see SUPPLIER LEAD TIME = 140 days (ocean). |
| **ROP** | Reorder Point. Valogix's threshold below which a reorder triggers. |
| **PO Covered** | Status demotion — item would be CRITICAL but a real SAP supplier PO with an ETA closes the gap. |
| **Staging Covered** | Status demotion — item would be CRITICAL but ShipBob backup alone closes the gap (no supplier PO needed). |

---

## Companion Files

| File | Purpose |
|---|---|
| `outputs/latest/weekly-report-*.xlsx` | This report (documented in this folder) |
| `outputs/latest/velocity-watch-*.xlsx` | Top 40 SKUs by all-channels velocity — 2-day cadence |
| `outputs/latest/order-list-*.xlsx` | 🛒 ORDER NOW — "do I have 150 days of stock?" supplier POs + staging transfers |

---

*Tommy 2026-05-29 — first cut. Update this folder when columns are added or formulas change.*
