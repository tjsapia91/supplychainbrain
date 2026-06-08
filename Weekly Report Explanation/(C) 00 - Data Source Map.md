# Data Source Map — Field by Field

**The precision reference.** Every column displayed in the weekly report, mapped to its exact source file + source column name.

When you see a number in the report and want to verify it, use this doc to locate:
1. **Which file** the data came from (exact path + filename pattern)
2. **Which column** within that file was read
3. **Any transformation** applied before display

---

## Quick Source File Reference

| # | Source | Where to download | Folder after auto-classifier |
|---|---|---|---|
| 1 | **SoStocked Weekly Forecast** (combined) | Built by `combine_forecast.py` from per-brand SoStocked Inventory Forecasting exports | `reports/_data/weekly/Weekly_Forecast_YYYY-MM-DD.xlsx` |
| 2 | **SoStocked Projected Forecast Model** | SoStocked → per-brand → Projected Forecast Model → download | `reports/_data/sostocked/{MTB,NFMD,SS}/projected-forecast-model-*-{5118,5109,5119}.xlsx` |
| 3 | **SoStocked Inventory Warehouse Breakdown** | SoStocked → per-brand → Inventory Warehouse Breakdown → CSV | `reports/_data/sostocked/{MTB,NFMD,SS}/inventory-warehouse-breakdown-*.csv` |
| 4 | **SoStocked FvA History** | SoStocked → per-brand → FvA Reports | `reports/_data/sostocked/{MTB,NFMD,SS}/fva-history/*.xlsx` |
| 5 | **Amazon FBA Inventory Report** (US) | Seller Central → Reports → Fulfillment → FBA Inventory | `reports/_data/seller-central/US/{MTB,NFMD,SS}/*.csv` |
| 6 | **Amazon AWD Inventory Report** (US) | Seller Central → AWD → Inventory → Export | `reports/_data/seller-central/US/{MTB,NFMD,SS}/awd-*.csv` |
| 7 | **Amazon CA FBA Health Report** | SC Canada → FBA Health → Export | `reports/_data/seller-central/CA/{MTB,NFMD,SS}/*.csv` |
| 8 | **Sellerboard Sales by Product/Month** | Sellerboard → Sales by Product → Monthly → Export | `reports/_data/sellerboard/{MTB,NFMD,SS}/*.csv` |
| 9 | **Sellerboard CA Dashboard Products** | Sellerboard → Dashboard Products → `amazon.ca` filter | `reports/_data/sellerboard/{MTB,NFMD,SS}/canada/*.csv` |
| 10 | **ShipBob Inventory Status** | ShipBob → Inventory Status → Export All | `reports/_data/shipbob/{MTB,NFMD,SS,LUMOS}/inventory-export-blob_*.csv` |
| 11 | **Valogix Item-Location-History-Forecast** | Valogix → export | `reports/_data/valogix/schain_itemLocationHistoryForecast_*.csv` |
| 12 | **Valogix Exceptions** | Valogix → Exceptions Report | `reports/_data/valogix-exceptions/schain_itemLocationHistoryException_*.csv` |
| 13 | **Walmart Marketplace** (NFMD direct) | Walmart Seller Center → Inventory → Export | `reports/_data/walmart/NFMD/inventory*.xlsx` |
| 14 | **Walmart Marketplace** (SS direct) | Walmart Seller Center → Inventory → Export | `reports/_data/walmart/SS/inventory*.xlsx` |
| 15 | **Walmart Inventory Health** | WM Seller Center → Inventory Health Dashboard → Export | `reports/_data/walmart/{NFMD,SS}/inventoryHealth*.csv` |
| 16 | **Floship Product Inventory** | Floship → Inventory → Export | `reports/_data/floship/Product_Inventory_*.csv` or `*.xlsx` |
| 17 | **SAP Open Purchase Order Report** | SAP → maintained xlsx | `reports/_data/sap-open-pos/SAP Open Purchase Order Report*.xlsx` |
| 18 | **SAP Inventory in Warehouse Report** | SAP → Inventory in Warehouse | `reports/_data/sap-inventory/SAPInventoryinwarehouse.xlsx` |
| 19 | **SAP Item Master** | SAP export | `reports/item-master/item_master.xlsx` |
| 20 | **Amazon SKU Mapping** | Manual | `reports/item-master/amazon-sku-mapping.xlsx` |

---

## 🆔 Identity Fields

| Pipeline Field | Display Header | Source File # | Source Column / Sheet |
|---|---|---|---|
| `brand` | BRAND | #19 SAP Item Master | "Branch" column (Michael Todd Beauty → MTB, Spa Sciences → SS, NasalFresh MD → NFMD). Falls back to product-name heuristic if no match. |
| `abc` | ABC CLASS | #19 SAP Item Master | "ABC Classification" column. Manual overrides in `ABC_OVERRIDE` dict in `build_report.py` for 9 UPCs. |
| `product` | PRODUCT | #19 SAP Item Master | "Item Description" column. Falls back to SoStocked or Amazon listing name if not in master. |
| `sku` | SAP UPC | #1 Weekly Forecast (sheet: `Inv. MTB` / `Inv. SS` / `Inv. NFMD`) | "SKU" column — 12-digit UPC after stripping suffixes like `-AMZ`, `-M`, `AMZ-stickerless` |
| `amazon_sku` | AMAZON SKU | #1 Weekly Forecast (Inv. sheets) + #20 Amazon SKU Mapping | "SKU" raw — includes Amazon listing suffixes |
| `asin` | ASIN | #1 Weekly Forecast (Inv. sheets) | "ASIN" / "Child ASIN" / "Parent ASIN" — first non-empty wins |

---

## 💨 Velocity Fields — THE BIG ONE

This is the field most people want to verify. Different channels use different velocity sources:

| Pipeline Field | Display Header | Channel | Source File # | Source Column | Calculation |
|---|---|---|---|---|---|
| `daily_vel` | DAILY SALES (AMAZON US) | Amazon US | #1 Weekly Forecast (Inv. sheets) | **"Adj. Velocity"** (column) | Direct read — already in units/day. **Falls back to "30 Day Velocity" if Adj. Vel = 0.** |
| `daily_vel` | DAILY SALES (AMAZON CA) | Amazon CA | #1 Weekly Forecast (Inv. sheets) | **"Adj. Velocity"** (column, filtered to CA marketplace row) | Direct read |
| `daily_vel` | DAILY SALES (THIS ROW) | ShipBob | #11 Valogix | Recent month column (last 1 month from history) | Last-month qty ÷ 30 |
| `daily_vel` | DAILY SALES (THIS ROW) | Floship Intl | #11 Valogix | Recent month column | Last-month qty ÷ 30 |
| `daily_vel` | DAILY SALES (THIS ROW) | Walmart NFMD | #13 Walmart NFMD direct | **"Daily units sold"** column | Direct read |
| `daily_vel` | DAILY SALES (THIS ROW) | Walmart SS | #11 Valogix (WM-SS location) | Recent month column | Last-month qty ÷ 30 |
| `amzn_us_vel` | DAILY SALES (AMAZON US) | (Cross-channel reference) | #1 Weekly Forecast (Inv. sheets, US row) | "Adj. Velocity" | US-marketplace velocity for that UPC, surfaced on every tab |
| `all_channels_vel` | DAILY SALES (ALL CHANNELS) | All | Computed | Sum of all channels' daily_vel per UPC | Sum across Amazon US + CA + Shopify + Walmart + Floship |
| `daily_vel_sellerboard_90d` | (reference field, not displayed) | Amazon | #8 Sellerboard Monthly | Sum of last 90 days qty | 90-day Sellerboard total ÷ 90 — used for audit only, does NOT drive DOS or status |

**Where these were before (HISTORICAL):**
- Until 2026-05-28, Amazon US daily_vel was OVERRIDDEN by Sellerboard 90-day. Tommy's audit revealed that under-stated current velocity for many items. **Now: Amazon US/CA both use SoStocked Adj. Velocity as primary.**

---

## 📦 Amazon Stock Fields

### Amazon US

| Pipeline Field | Display Header | Source File # | Source Column |
|---|---|---|---|
| `fba_stock` | READY TO SELL (FBA) | #5 Amazon FBA Inventory Report | **"available"** (or legacy `afn-fulfillable-quantity`) — already net of reserved |
| `fc_transfer` | MOVING BTW FBA FCs | #5 Amazon FBA Inventory Report | **"Reserved FC Transfer"** |
| `awd_stock` | AT AMZN AWD | #6 Amazon AWD Inventory Report | **"Available in AWD (units)"** |
| `awd_inbound` / `inbound_to_awd` | INBOUND TO AWD | #6 Amazon AWD Inventory Report | **"Inbound to AWD (units)"** |
| `fba_pipeline` | INBOUND TO FBA | #5 Amazon FBA Inventory Report | Sum of **"inbound-shipped"** + **"inbound-received"** + **"inbound-working"** |
| `on_hand` | TOTAL AT AMZN | Computed | = `awd_stock + fc_transfer + fba_stock` |
| `on_order` | TOTAL INBOUND TO AMZN | Computed | = `inbound_to_awd + fba_pipeline` |
| `amzn_grand_total` | GRAND TOTAL AT AMZN | Excel formula | = TOTAL AT AMZN + TOTAL INBOUND TO AMZN |

### Amazon CA

| Pipeline Field | Display Header | Source File # | Source Column |
|---|---|---|---|
| `fba_stock` | READY TO SELL (FBA) | #7 Amazon CA FBA Health | **"available"** column |
| `fc_transfer` | MOVING BTW FBA FCs | #7 Amazon CA FBA Health | **"Reserved FC Transfer"** |
| `awd_stock` | AT AMZN AWD | N/A (CA has no AWD) | Always 0 |
| `fba_pipeline` | INBOUND TO FBA | #7 Amazon CA FBA Health | Sum of inbound-shipped/received/working |
| `alliance_wh_ca` | ALLIANCE WH (CA INBOUND) | #18 SAP Inventory in Warehouse | Section "Whse: ASG-MTB" / "ASG-NF" / "ASG-SS" → sum of "In Stock" + "Ordered" per item |

### ShipBob (US emergency backup AND Shopify fulfillment)

| Pipeline Field | Display Header | Source File # | Source Column |
|---|---|---|---|
| `shipbob_emergency` (Amazon tabs) | SHIPBOB BACKUP | #10 ShipBob Inventory Status | "Total On Hand" — NET of a 30-day Shopify reserve (Shopify daily_vel × 30) so Shopify isn't starved |
| `on_hand` (ShipBob tab) | ON HAND | #10 ShipBob Inventory Status | "Total On Hand" — direct read, no Shopify reserve subtraction |

---

## 📅 Forecast Fields

### 9-Month Rolling Forecast Slots (forecast_m1 through forecast_m9)

| Pipeline Field | Display Header | Source File # | Source Column / Tab |
|---|---|---|---|
| `forecast_m1..m9` (current month → 8 months out) | "MAY 26", "JUN 26", … (labels roll forward each run) | #2 SoStocked Projected Forecast Model | Tab: **"Forecasted Sales Monthly"** · Column: "Month 1" through "Month 13" · Row filter: ASIN = item ASIN AND Marketplace = "US" (or "CA") — see normalization below |
| `forecast_total` | 9MO PLANNING | Computed | `= SUM(forecast_m1..m9)` |

**Marketplace normalization in PFM** — SoStocked uses several labels for the US-side market:
- `"US"` → US
- `"US+MX"` → US (most US ASINs)
- `"NAm"` → US (some legacy listings)
- `"CA"` → CA
- `"MX"` → dropped

### Audit / Comparison Fields

| Pipeline Field | Display Header | Source File # | Source / Calculation |
|---|---|---|---|
| `forecast_pfm_total` | PFM 9MO (SOSTOCKED) | #2 Projected Forecast Model | Same as forecast_m1..m9 sum — direct from "Forecasted Sales Monthly" tab |
| `forecast_seasonality_total` | ACTUALS 9MO (SEASONALITY) | #8 Sellerboard Monthly | Computed: `trailing_12mo_daily_avg × per_month_seasonality_factor × days_in_month` for next 9 months |
| `forecast_delta_pct` | FORECAST DELTA % | Computed | `\|PFM_total − Seasonality_total\| ÷ MAX(PFM, Seasonality) × 100` |
| `forecast_vel` | FORECAST VEL/DAY | #1 Weekly Forecast (Forecast sheets) | Near-term weekly forecast averaged, then ÷ 7 → units/day |
| `forecast_12mo` | 12MO FORECAST | #11 Valogix (Valogix channels only) | "Forecast Total (Next 12 Months)" column |

### CA Seasonality (Used as fallback when PFM CA missing)

| Source File # | Source | Used for |
|---|---|---|
| #9 Sellerboard CA Dashboard | Per-marketplace CA sales — quarterly seasonality factors | Anchors CA forecast shape when SoStocked CA PFM is unconfigured for an ASIN |

---

## 🚢 SAP Open PO Fields

| Pipeline Field | Display Header | Source File # | Source Column |
|---|---|---|---|
| `amzn_supplier_on_order` | OPEN PO (SUPPLIER) | #17 SAP Open POs | Sum of open units across PO lines where destination warehouse maps to Amazon US (`AMZN-MT` / `AMZN-SS`) via `SAP_WH_TO_CHANNEL` dict |
| `po_eta` | PO ARRIVES ON | #17 SAP Open POs | "Statistics Date" / "Due Date" column — earliest open PO date for this item × channel |
| `po_all_list` | (used in tooltips / Action Plan) | #17 SAP Open POs | List of all open POs for this item × channel |

The SAP_WH_TO_CHANNEL routing dict in `build_report.py`:
```
AMZN-MT, AMZN-SS         → Amazon US
AMZ-MT-CA, AMZ-SS-CA     → Amazon CA
AMZ-MT-UK, AMZ-SS-UK     → Amazon UK
AMZ-MT-AU, AMZ-SS-AU     → Amazon AU
AMZ-MT-EU, AMZ-SS-EU     → Amazon EU
AMZ-MT-TT, AMZ-SS-TT     → TikTok
ASG-MTB, ASG-NF, ASG-SS  → Alliance WH (CA staging)
SBGA-MT, SBGA-SS         → ShipBob
SBGA-SS-NFMD             → ShipBob (NFMD)
```

---

## 📊 Days of Supply (DOS) Fields

All computed in `build_report.py` — no external source.

| Pipeline Field | Display Header | Calculation |
|---|---|---|
| `dos` | DAYS OF STOCK LEFT | `(FBA + FC Transfer + AWD) ÷ daily_vel` — physical at Amazon only (Tommy 2026-05-29) |
| `dos_fba_only` | FBA ONLY DOS | `FBA ÷ daily_vel` |
| `dos_fba_awd` | FBA+AWD DOS | `(FBA + AWD) ÷ daily_vel` |
| `dos_with_po` | DAYS OF STOCK (W/ INCOMING PO) | `(FBA + FC + AWD + AWD inbound + FBA pipeline + Open SAP PO + ShipBob backup) ÷ MAX(forecast_vel, daily_vel)` |

---

## 📅 Stockout Date Fields

All Excel formulas — recompute live if you edit stock or velocity.

| Pipeline Field | Display Header | Calculation |
|---|---|---|
| `stockout_date` | STOCKOUT DATE (AT CURRENT PACE) | `TODAY() + dos days` |
| `stockout_date_forecast` | STOCKOUT DATE (IF FORECAST HITS) | Walks the rolling monthly forecast (m1..m9) cumulatively until stock runs out. Uses hidden `h_cum_*` helper cells. |
| `stockout_delta_days` | Δ DAYS (FCST − CURRENT) | `stockout_date_forecast − stockout_date` |
| `stockout_date_with_po` | STOCKOUT DATE (W/ INCOMING PO) (US) / (W/ ALLIANCE) (CA) | `TODAY() + dos_with_po days` |

---

## 📊 Sales History / Seasonality Fields

| Pipeline Field | Display Header | Source File # | Source Column |
|---|---|---|---|
| `vol_bucket` | DEMAND SWING | #8 Sellerboard Monthly | Computed from 12 months of history — Coefficient of Variation bucket (STABLE / MODERATE / VOLATILE / INSUFFICIENT) |
| `vol_cv` | SWING % | #8 Sellerboard Monthly | `stdev / mean × 100` over the 12-month history |
| Sales history months on Amazon Sales History tab | "May 26", "Apr 26", … | #8 Sellerboard Monthly | Direct per-month qty columns (last 12 months) |

---

## 🕒 Lead Time Fields

| Pipeline Field | Display Header | Source | Calculation |
|---|---|---|---|
| `lead_time` | LEAD TIME | Constant 60 (Amazon tabs) | Staging → Amazon transit time |
| `lead_time` | LEAD TIME | #11 Valogix "Lead Time" (Valogix channels) | Direct read |
| `supplier_lead_time` | SUPPLIER LEAD TIME | Constant 140 (Amazon tabs only) | Supplier → staging ocean PO lead time. Drives urgency floor. |
| `effective_lead_time` | (internal — drives urgency classification) | Computed | `MAX(per-item lead from SoStocked, 140)`. Items in `LEAD_TIME_OVERRIDE` (BioMist, AIVA, MicroSmooth, Hair Identifier Spray) get 60 instead — those are ShipBob-replenished, not supplier-fed. |

---

## 💰 Cost / Value Fields

| Pipeline Field | Display Header | Source File # | Source Column |
|---|---|---|---|
| `cost_unit` | COST/UNIT (hidden in current views) | #11 Valogix | "Inventory Cost" column (only present for 244 UPCs as of latest run) |
| `on_hand_value` | ON HAND $ | Computed | `on_hand × cost_unit` |

---

## 📋 Status Classification

`status` field — computed in `recompute_amazon_status_with_inbound()` (Amazon items) or `load_valogix()` (other channels).

For Amazon items, drives off:
- `fba_stock`, `fc_transfer`, `awd_stock`, `awd_inbound`, `fba_pipeline` (all SC-sourced)
- `shipbob_emergency` (ShipBob-sourced)
- `daily_vel` (SoStocked Adj. Velocity)

Thresholds:
```
CRITICAL_DOS_THRESHOLD = 100
HIGH_DOS_THRESHOLD     = 130
INACTIVE_THRESHOLD     = 0.1 (velocity)
```

Status post-classification demotions:
- **→ PO COVERED** when `po_eta` exists from SAP AND open PO covers the gap
- **→ HEALTHY** when ShipBob US staging closes the gap (no supplier PO needed)

---

## 🚨 Anomaly Fields

| Pipeline Field | Display Header | Source File # | Source |
|---|---|---|---|
| Sales anomalies (Amazon) | (Sales Anomalies tab rows) | #8 Sellerboard Monthly | Computed — current Adj. Velocity vs trailing 12-mo daily baseline (excluding stockout months <25% of mean) |
| Sales anomalies (Valogix) | (Sales Anomalies tab rows) | #12 Valogix Exceptions | Direct read — Valogix flags these in its exception report |

---

## How Auto-Classifier Routes Files

When you drop a file in `Downloads/`, `scripts/sort_downloads.py` runs as a pre-flight to `build_report.py` and routes recognized files to their `_data/` folders:

| Pattern | Routes to | Brand detection |
|---|---|---|
| `projected-forecast-model-*-5118.xlsx` | `_data/sostocked/MTB/` | Group ID suffix (5118=MTB, 5109=NFMD, 5119=SS) |
| `projected-forecast-model-*-5109.xlsx` | `_data/sostocked/NFMD/` | Same |
| `projected-forecast-model-*-5119.xlsx` | `_data/sostocked/SS/` | Same |
| `inventory-warehouse-breakdown-*.csv` | `_data/sostocked/<brand>/` | Group ID + content sniff |
| `awd-*.csv` (with "Inbound to AWD" column) | `_data/seller-central/US/<brand>/awd-*.csv` | Merchant ID from filename |
| FBA Inventory CSVs (with `afn-*` or `inbound-shipped` cols) | `_data/seller-central/US/<brand>/` | Merchant ID |
| CA FBA Health (with `recommended-action` col) | `_data/seller-central/CA/<brand>/` | Merchant ID |
| `inventory-export-blob_<group-id>_*.csv` | `_data/shipbob/<brand>/` | Group ID (385579=MTB, 385953=SS, 385954=NFMD, 396348=LUMOS) |
| `schain_itemLocationHistoryForecast_*.csv` | `_data/valogix/` | — |
| `schain_itemLocationHistoryException_*.csv` | `_data/valogix-exceptions/` | — |
| `inventoryHealth*.csv` | `_data/walmart/<brand>/` | Content sniff (brand name in rows) |
| Walmart inventory `.xlsx` | `_data/walmart/<brand>/` | Content sniff |
| Sellerboard Monthly CSVs | `_data/sellerboard/<brand>/` | Brand keyword detection |
| Sellerboard CA Dashboard (with `amazon.ca` filter) | `_data/sellerboard/<brand>/canada/` | Content + filename |
| SAP Open PO `.xlsx` | `_data/sap-open-pos/` | Content sniff |
| SAP Inventory in Warehouse `.xlsx` | `_data/sap-inventory/` | Content sniff |

Anything the classifier doesn't recognize is **left in place** in Downloads, flagged with `❓ UNSORTED` in the log.

---

## When To Refresh Each Source

| Cadence | Files |
|---|---|
| **Weekly** | All FBA Inventory, AWD Inventory, CA FBA Health, ShipBob, Floship, Walmart Marketplace + Inventory Health, Valogix, SAP Open POs, Sellerboard CA Dashboard, SoStocked Projected Forecast Model + Inventory Warehouse Breakdown |
| **Monthly** | Sellerboard Sales by Product/Month (3 brand files) |
| **As-changed** | SAP Item Master (when ABC codes change in SAP), Amazon SKU Mapping (when new ASINs launch), SAP Inventory in Warehouse |

---

## How to Verify Any Number

1. **Find the column** in the tab — note the display header
2. **Open this doc** — search for the pipeline field name (e.g., `daily_vel`, `awd_stock`)
3. **Note the source file # + column name**
4. **Open the source file** (from the Quick Source File Reference at top)
5. **Find the row** for that ASIN / SKU
6. **Compare the source column value** to what's shown in the report

If they don't match, that's a bug — check the run log for transformation warnings, or ping a tech-savvy human to investigate.

---

*Tommy 2026-05-29 — master reference. Update when columns or sources change.*
