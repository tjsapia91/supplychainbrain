# Tab 1 — Amazon US

**Purpose:** Every active Amazon US listing, segmented by status (Priority Action → Watch → Healthy → Inactive → Phase-Out), with A SKUs grouped within each section.

Same column structure as Amazon CA — the data within columns differs (US-specific stock + velocity).

---

## 🆔 Identity (Cols A–G)

| Col | Header | Source | Calculation |
|---|---|---|---|
| A | **STATUS** | Computed | `recompute_amazon_status_with_inbound()` — see Status logic below |
| B | MARKETPLACE | *Hidden* | Hard-coded "Amazon US" |
| C | **BRAND** | `item_master.xlsx` (Branch column) | Direct lookup by SAP UPC; falls back to name heuristic |
| D | **ABC CLASS** | `item_master.xlsx` (ABC Classification) | Direct read; `ABC_OVERRIDE` dict can hard-set 9 specific UPCs |
| E | **PRODUCT** | `item_master.xlsx` (Item Description) | Falls back to SoStocked / Amazon listing title if not in master |
| F | **SAP UPC** | SoStocked PFM → SKU column | 12-digit UPC after stripping suffixes like `-AMZ` |
| F2 | **AMAZON SKU** | SoStocked PFM → SKU column (raw) | Original Amazon SKU with suffix variants |
| G | **ASIN** | SoStocked PFM → ASIN column | Direct read |

---

## 📅 Stockout Dates (Cols H–J)

| Col | Header | Source | Calculation |
|---|---|---|---|
| H | **STOCKOUT DATE (AT CURRENT PACE)** | Excel formula | `TODAY() + DOS days` where DOS = (FBA + FC + AWD) / daily_vel |
| I | **STOCKOUT DATE (IF FORECAST HITS)** | Excel walk-forward formula | Walks the monthly forecast cumulatively until total stock runs out. References hidden `h_cum_*` cells. |
| J | **Δ DAYS (FCST − CURRENT)** | Excel formula | `(Stockout If Forecast) − (Stockout At Current)`. Positive = forecast lasts longer; flags forecast/reality disagreement. |

---

## 🚢 Open PO + Recommendations (Cols K–P)

| Col | Header | Source | Calculation |
|---|---|---|---|
| K | **OPEN PO (SUPPLIER)** | `reports/_data/sap-open-pos/*.xlsx` | Sum of open SAP PO units routed to `AMZN-MT` / `AMZN-SS` for this UPC |
| L | **PO ARRIVES ON** | SAP Open POs | Earliest open SAP PO due date for this item × channel |
| M | **STOCKOUT DATE (W/ INCOMING PO)** | Computed | `TODAY() + dos_with_po days` where dos_with_po = (Total at Amzn + AWD inbound + FBA pipeline + Open Supplier PO + ShipBob backup) / MAX(forecast_vel, daily_vel) |
| N | **SB→AMZN SUGGEST** | Computed | For items in `LEAD_TIME_OVERRIDE` (BioMist, AIVA, MicroSmooth, Hair Identifier Spray): `MAX(0, daily_vel × 90 − TOTAL AT AMZN)` — keep ~90d coverage from ShipBob |
| O | **SUPPLIER PO SUGGEST** | *Blank on Amazon tabs* | Shopify-only column |
| P | **AMZ PO QTY (SUPPLIER)** | `demand_planning.py` | `MAX(0, daily_velocity × (lead_time + 60d buffer) − total_stock)` — legacy PO sizing. The new `🛒 ORDER NOW` file is the better source. |

---

## 📦 Amazon Stock — components → totals (Cols Q–Z)

| Col | Header | Source | Calculation |
|---|---|---|---|
| Q | **AT AMZN AWD** | AWD Inventory Report (`awd-*.csv`) | "Available in AWD (units)" column |
| R | **MOVING BTW FBA FCs** | FBA Inventory Report | "Reserved FC Transfer" field |
| S | **READY TO SELL (FBA)** | FBA Inventory Report | "Available" / "afn-fulfillable-quantity" — already net of reserved |
| T | **TOTAL AT AMZN** | Excel formula | `= Q + R + S` |
| U | **INBOUND TO AWD** | AWD Inventory Report | "Inbound to AWD (units)" — supplier → AWD in transit |
| V | **INBOUND TO FBA** | FBA Inventory Report | Sum of `inbound-shipped` + `inbound-received` + `inbound-working` |
| W | **TOTAL INBOUND TO AMZN** | Excel formula | `= U + V` |
| X | **GRAND TOTAL AT AMZN** | Excel formula | `= T + W` |
| Y | ALLIANCE WH (CA INBOUND) | *Hidden on US tab* | CA-only — SAP Inventory in Warehouse (ASG-*) |
| Z | **SHIPBOB BACKUP** | `reports/_data/shipbob/<brand>/*.csv` | ShipBob "Total On Hand", net of 30-day Shopify reserve |

---

## 📊 Days of Supply — 4 progressive views (Cols AA–AD)

| Col | Header | Calculation |
|---|---|---|
| AA | **FBA ONLY DOS** | `FBA ÷ daily_vel` — operational view. <14d = 🔴, <30d = 🟠 |
| AB | **FBA+AWD DOS** | `(FBA + AWD) ÷ daily_vel` |
| AC | **DAYS OF STOCK LEFT** | **(FBA + FC Transfer + AWD) ÷ daily_vel — physical at Amazon only** (Tommy 2026-05-29) |
| AD | **DAYS OF STOCK (W/ INCOMING PO)** | `(All Amazon + inbound + supplier PO + ShipBob backup) / MAX(forecast_vel, daily_vel)` — full procurement view |

---

## 💨 Velocity (Cols AE–AG)

| Col | Header | Source | Calculation |
|---|---|---|---|
| AE | **DAILY SALES (AMAZON US)** | SoStocked "Adj. Velocity" | ~30-day stockout-adjusted daily rate, US marketplace |
| AF | DAILY SALES (THIS ROW) | *Hidden* | Same as Amazon US on this tab |
| AG | DAILY SALES (ALL CHANNELS) | *Hidden* | Sum across every channel — used internally |

---

## ✏️ Scratch Pad — *User-Fillable* (Cols AH–AL)

| Col | Header | Calculation |
|---|---|---|
| AH | **SB TRANSFER QTY** | User types qty to send from ShipBob |
| AI | **NEW STOCKOUT (AFTER SB)** | `Stockout Date + (SB Transfer Qty ÷ daily_vel)` |
| AJ | **COVER THROUGH** | User types target date |
| AK | **DAYS TO COVER** | `Cover Through − New Stockout` |
| AL | **UNITS NEEDED FROM PO** | `Days To Cover × daily_vel` |

---

## 📈 Demand Swing (Cols AM–AN)

| Col | Header | Source | Calculation |
|---|---|---|---|
| AM | **DEMAND SWING** | Sellerboard 12-mo history | CV bucket: STABLE / MODERATE / VOLATILE / INSUFFICIENT |
| AN | **SWING %** | Sellerboard | `stdev / mean × 100` — coefficient of variation |

---

## 📅 Rolling 9-Month Forecast (Cols AO–AW + 9MO total)

| Col | Header | Source | Calculation |
|---|---|---|---|
| AO–AW | MAY 26 → JAN 27 | SoStocked PFM ("Forecasted Sales Monthly" tab) | Per-marketplace lookup by `(ASIN, "US")` |
| AX | **9MO PLANNING** | Excel formula | `= SUM(AO:AW)` |

---

## 🔍 Audit Columns (collapsed by default)

| Col | Header | Calculation |
|---|---|---|
| **PFM 9MO (SOSTOCKED)** | SoStocked PFM "Forecasted Sales Monthly" — same data, 9-mo sum |
| **ACTUALS 9MO (SEASONALITY)** | `(trailing 12mo daily avg) × seasonality_factor × days_in_month` for 9 months |
| **FORECAST DELTA %** | `\|PFM − Seasonality\| ÷ MAX(PFM, Seasonality) × 100` — flags >25% divergence |

---

## 🕒 Lead Time + Notes

| Col | Header | Source | Calculation |
|---|---|---|---|
| **LEAD TIME** | Constant | 60 (staging → Amazon transit) |
| **SUPPLIER LEAD TIME** | Constant | 140 (supplier → staging ocean PO) — drives urgency floor |
| **NOTES** | User input | Free-text; overwritten each pipeline run unless you re-paste |

---

## Hidden Columns

| Column | Reason |
|---|---|
| MARKETPLACE | Always "Amazon US" on this tab |
| DAILY SALES (THIS ROW) | Same as DAILY SALES (AMAZON US) |
| DAILY SALES (ALL CHANNELS) | Cross-channel sum, misleading on a single-channel tab |
| ALLIANCE WH (CA INBOUND) | CA-only |
| APR…DEC (legacy abbr forecasts) | Replaced by rolling MAY 26 / JUN 26 / … columns |
| `h_cum_apr…h_cum_dec`, `h_sm` | Helper cells for forecast-stockout walk-forward formula |
| Walmart-only enrichment cols | Walmart-tab-only |

---

## Status Classification

```
status = "TRUE STOCKOUT"     if (FBA + FC + AWD + AWD inbound + ShipBob) == 0
       = "LOW VEL STOCKOUT"  if velocity < 0.1/day AND nothing anywhere
       = "INACTIVE"          if velocity < 0.1/day AND stock exists
       = "AMAZON STOCKOUT"   if FBA+FC == 0 AND (AWD + ShipBob > 0) AND net_pos/vel ≤ 30
       = "FBA REPLENISHMENT" if FBA+FC == 0 AND (AWD + ShipBob > 0) AND net_pos/vel > 30
       = "CRITICAL"          if net_pos / vel ≤ 100 days
       = "HIGH"              if net_pos / vel ≤ 130 days
       = "HEALTHY"           otherwise

where net_pos = FBA + FC + AWD + AWD inbound + FBA pipeline
```

Two post-classification demotions:
- **→ PO COVERED** if a real SAP supplier PO ETA exists AND the PO closes the gap
- **→ HEALTHY** if staging (ShipBob US) alone closes the gap without a supplier PO

---

## Source Files

- **FBA**: `reports/_data/seller-central/US/<brand>/*.csv` (FBA Inventory Report)
- **AWD**: `reports/_data/seller-central/US/<brand>/awd-*.csv`
- **Velocity**: SoStocked PFM → `demand-plan-*.json` (Adj. Velocity field)
- **9-month forecast**: `reports/_data/sostocked/<brand>/projected-forecast-model-*.xlsx` → "Forecasted Sales Monthly" tab
- **ShipBob**: `reports/_data/shipbob/<brand>/*.csv`
- **SAP POs**: `reports/_data/sap-open-pos/*.xlsx`
- **Sellerboard (seasonality + Demand Swing)**: `reports/_data/sellerboard/<brand>/*.csv`
- **Brand, ABC, Product**: `reports/item-master/item_master.xlsx`
