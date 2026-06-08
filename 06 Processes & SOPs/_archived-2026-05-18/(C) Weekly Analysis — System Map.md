# (C) Weekly Analysis — System Map

> **The architecture doc.** Single-page overview of how the weekly analysis pipeline works end-to-end — what data goes in, what scripts process it, what tabs come out, and how every column traces back to a source. Use this when you need to understand the WHY behind a number on the report.
>
> **Companion docs:**
> - [[06 Processes & SOPs/(C) Weekly Analysis SOP — Step by Step]] — operational SOP (run the scripts)
> - [[06 Processes & SOPs/(C) Weekly Inputs Sourcing SOP]] — where to pull each file from
> - [[06 Processes & SOPs/(C) Weekly Analysis Cheat Sheet — 1 Page]] — printable quick reference

---

## 🗺 One-page data flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            INPUT SOURCES (11)                                    │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  📊 SoStocked            📦 Seller Central        📦 ShipBob (4 brand logins)    │
│  (3 brands × 3 reports)  (3 brands × 2 reports)   On Hand Summary                │
│  • Forecast Model        • AWD Inventory          • MTB / NFMD / SS / LUMOS      │
│  • Inventory             • FBA Inventory                                          │
│  • FvA                                                                            │
│                                                                                  │
│  🌐 Valogix              🛒 Walmart Seller Ctr.   🚢 Floship                     │
│  Item-Location-History-  (NFMD + SS only)         Product Inventory               │
│  Forecast CSV            WFS Inventory .xlsx      (international, MTB only)      │
│  • 24mo history actuals                                                          │
│  • 18mo forward forecast                                                          │
│  • UPC cost                                                                       │
│                                                                                  │
│  ⚠️ Valogix Exceptions    📈 Sellerboard          📋 SAP Open POs                │
│  History Exception Rpt   Sales by product/month   Open Purchase Order Report     │
│  (statistical outliers)  (3 brands · 28mo back)   (full export, 5000+ rows)      │
│                                                                                  │
│  🏷 SAP Item Master       🚚 In-Transit Log        🆕 AWD-to-FBA Shipments       │
│  ABC + Description       Sea/Truck/Air shipments  (parked — accumulating only)   │
│  (as-needed refresh)     (manual update)                                          │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          PIPELINE SCRIPTS (3 steps)                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  STEP 1: combine_forecast.py                                                     │
│    Combines 9 SoStocked CSVs → Weekly_Forecast_YYYY-MM-DD.xlsx (8 sheets)        │
│                                                                                  │
│  STEP 2: demand_planning.py                                                      │
│    Reads Weekly_Forecast + AWD inbound + SKU review                              │
│    → demand-plan-YYYY-MM-DD.json (Amazon priority tiers, DOS, status)            │
│                                                                                  │
│  STEP 3: build_report.py    ◄── pre-flight auto-archives stale prior-week files  │
│    Reads ALL inputs above + demand-plan JSON                                     │
│    → weekly-report-YYYY-MM-DD.xlsx (14 tabs)                                     │
│    → Auto-published to SharePoint via outputs/latest/ junction                   │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        WEEKLY REPORT (14 tabs)                                   │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  Per-marketplace full universe (default tab = Amazon US):                        │
│  1. Amazon US     2. 🇨🇦 Amazon CA   3. Shopify   4. Walmart   5. Floship Intl   │
│                                                                                  │
│  Action layer:                                                                   │
│  6. 🚨 Priority Actions   7. ✅ Action Plan   8. 📋 SAP Open POs                 │
│                                                                                  │
│  Routing layer:                                                                  │
│  9. 🏷 Bundles & Custom SKUs   10. 🗑 Phase-Out, Obsolete & BOMs                  │
│                                                                                  │
│  Insight layer:                                                                  │
│  11. 📈 Forecast Pivot   12. 📊 Amazon Sales History   13. 📈 Amazon FvA         │
│  14. 📊 Sales Anomalies                                                          │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📥 The 11 input sources

| # | Source | What it brings | Files | Folder | Loader function |
|---|---|---|---:|---|---|
| 1 | **SoStocked** | Amazon forecasts · velocity · FBA stock · FvA accuracy | 9 | `reports/sostocked/<BRAND>/` | `combine_forecast.py` |
| 2 | **Amazon Seller Central** | Authoritative FBA + AWD stock + inbound pipeline (overrides SoStocked) | 6 | `reports/seller-central/<BRAND>/` | `load_fba_inbound()` + `load_awd_inbound()` |
| 3 | **ShipBob** | Total On Hand for emergency-stock + Shopify on-hand | 4 | `reports/shipbob/<BRAND>/` | `load_shipbob()` |
| 4 | **Walmart Seller Center** | NFMD direct inventory + forecast (Valogix doesn't carry NFMD on Walmart) | 2 | `reports/walmart/<BRAND>/` | `load_walmart_nfmd()` |
| 5 | **Floship** | International FLO-MTB inventory validation | 1 | `reports/floship/` | (cross-checked against Valogix FLO-MTB row) |
| 6 | **Valogix** | 24mo history · 18mo forward forecast · cost · multi-channel inventory · supplier on-order | 1 | `reports/valogix/` | `load_valogix()` + `load_amazon_supplier_on_order()` |
| 7 | **Valogix Exceptions** | Statistical outliers in actuals (bad-data months) | 1 | `reports/valogix-exceptions/` | `load_valogix_exceptions()` |
| 8 | **Sellerboard** | 28mo Amazon sales actuals (TTM Qty · YoY · volatility) | 3 | `reports/sellerboard/<BRAND>/` | `load_sellerboard_history()` |
| 9 | **SAP Open POs** | Open PO ETAs · same-day flag · supplier-on-order via warehouse | 1 | `reports/sap-open-pos/` | `load_sap_open_pos()` |
| 10 | **SAP Item Master** | ABC classifications · canonical product descriptions | 1 | `reports/item-master/` | `load_item_master()` |
| 11 | **In-Transit Log** | Container/truck/air shipment tracking (manual) | 1 | `reports/in-transit/` | (separate `build_shipment_tracking.py` script) |

**Total: 28 files per weekly run.**

---

## ⚙️ The 3 pipeline scripts

### STEP 1 — `scripts/combine_forecast.py`

**Reads:** 9 SoStocked CSVs (3 brands × 3 reports — Projected Forecast Model, Inventory, FvA)

**Produces:** `reports/weekly/Weekly_Forecast_YYYY-MM-DD.xlsx` — 8 sheets:
1. Forecast SS · 2. Forecast MTB · 3. Forecast NFMD
4. Red Flags (variance >30%) · 5. Inv. MTB · 6. Inv. SS · 7. Inv. NFMD
8. Forecast Accuracy (FvA aggregated)

**Auto-archives:** the 6 raw source files → `reports/archive/sostocked/YYYY-MM-DD/`

---

### STEP 2 — `scripts/demand_planning.py`

**Reads:**
- `Weekly_Forecast_*.xlsx` (output of step 1)
- AWD inbound CSV (`reports/seller-central/<BRAND>/awd-*.csv`)
- SKU review (carryover from prior week — `outputs/<prev-date>/sku-review-*.xlsx`)

**Produces:** `outputs/YYYY-MM-DD/demand-plan-YYYY-MM-DD.json` + `.md`

**Logic:**
- Computes Days of Supply (DOS) per ASIN: `(FBA + AWD + AWD Inbound) ÷ Adj. Velocity`
- Classifies each ASIN into urgency tier (CRITICAL / HIGH / WATCH / FBA REPLENISHMENT / HEALTHY / INACTIVE / LOW VEL STOCKOUT / TRUE STOCKOUT / AMAZON STOCKOUT)
- Sizes Order Qty: `daily_vel × (Lead Time + 60d buffer) − total_stock`
- Drops inactive + phase-out items from action lists

---

### STEP 3 — `scripts/build_report.py`

**Pre-flight (auto-archive stale prior-week files):**

Scans every input folder. If multiple files exist, moves all but the newest to `reports/archive/<source>/YYYY-MM-DD/`. Prevents stale data from contaminating fresh runs.

Covers: Seller Central (per brand × report type), ShipBob, Walmart, Floship, Sellerboard, Valogix Exceptions, SAP Open POs, AWD-to-FBA shipments (parked).

Valogix archive happens inside `load_valogix()` itself.

**Reads:** demand-plan JSON + ALL 11 input sources

**Produces:** `outputs/YYYY-MM-DD/weekly-report-YYYY-MM-DD.xlsx` (14 tabs)

**Publishes:** copies to `outputs/latest/weekly-report-YYYY-MM-DD.xlsx` (SharePoint junction)

---

## 📊 The 14 output tabs — what flows into each

| # | Tab | Inputs that feed it |
|---|---|---|
| 1 | **Amazon US** | demand-plan JSON (Amazon section, market=US) + SAP Item Master (ABC, desc) + Seller Central (FBA/AWD stock) + ShipBob (emergency) + Valogix (supplier on-order from AMZN-MT/SS) + Sellerboard (volatility) + SAP Open POs (PO ETA) |
| 2 | **🇨🇦 Amazon CA** | demand-plan JSON (market=CA) + same enrichment as Amazon US, minus SUPPLIER on-order (CA not split in Valogix) |
| 3 | **Shopify** | Valogix (SBGA-MT / SBGA-SS / SBGA-SS-NFMD rows) + ShipBob (overrides Shopify on_hand) + Sellerboard volatility |
| 4 | **Walmart** | Valogix (WM-SS row) + direct Walmart Seller Center pull (WM-NFMD) + ShipBob emergency |
| 5 | **Floship Intl** | Valogix (FLO-MTB row) + Floship export cross-check |
| 6 | **🚨 Priority Actions** | Amazon priority items from demand-plan, full columns view |
| 7 | **✅ Action Plan** | Amazon items needing replenishment, split into ShipBob send-ins vs Supplier POs |
| 8 | **📋 SAP Open POs** | SAP Open Purchase Order Report (filtered: not closed, posted ≥2026-01-01, 12-digit UPC, qty>0) |
| 9 | **🏷 Bundles & Custom SKUs** | Non-UPC SKUs (bundle/combo codes) + S-class items + special-account UPCs |
| 10 | **🗑 Phase-Out, Obsolete & BOMs** | E + Z + F + I + S classified items from SAP Item Master |
| 11 | **📈 Forecast Pivot** | Valogix (24mo actuals + 18mo forecast) + Sellerboard (Amazon actuals) |
| 12 | **📊 Amazon Sales History** | Sellerboard 12mo per-ASIN actuals + YoY + ROI |
| 13 | **📈 Amazon FvA** | Archived SoStocked FvA snapshots → forecast vs actual variance |
| 14 | **📊 Sales Anomalies** | Valogix History Exception Report (statistical outliers) |

---

## 🧮 Key business logic

### DOS (Days of Supply)

```
Amazon side:
  DOS = (FBA Available + FC Transfer + AWD Available + AWD Inbound) ÷ Adj. Velocity

Non-Amazon (Shopify/Walmart/Floship):
  DOS = Available ÷ Valogix 30-day velocity (last fully closed month)
  Where Available = On Hand − Committed

Walmart NFMD (direct from Walmart Seller Center):
  DOS = "Forecasted days of supply" field straight from Walmart
```

**Velocity sources** (all 30-day basis):
- Amazon: SoStocked `Adj. Velocity` (~30d stockout-corrected)
- Shopify/Walmart-SS/Floship: Valogix last-closed-month actuals ÷ 30
- Walmart NFMD direct: Walmart's `Daily units sold`

### Lead Time Floor (150 days)

Per-item lead times from SoStocked are usually under-stated. For URGENCY classification, the system uses `max(per-item lead_time, 150)` to reflect real door-to-door time:

```
Production (30-60d) + Ocean freight (30-45d) + Customs + Receiving (15-30d) = ~150d typical
```

### Status Classification (Amazon)

| Status | Trigger |
|---|---|
| 🚨 AMAZON STOCKOUT | FBA=0 but AWD or ShipBob has stock |
| 🔴 TRUE STOCKOUT | Nothing anywhere (PO needed) |
| 🔴 CRITICAL | DOS ≤ Lead Time floor (150d) |
| 🟠 HIGH | DOS ≤ Lead Time + 30d |
| 🟡 WATCH | DOS ≤ 60d |
| 🟡 FBA REPLENISHMENT | FBA=0 but DOS > 30d (routine send-in) |
| 🟢 HEALTHY | DOS > Lead Time + 30d |
| ⚫ INACTIVE | Velocity < 0.1/day |
| 🔵 LOW VEL STOCKOUT | Stocked out but velocity < 0.1/day |

### Status Classification (non-Amazon — Valogix)

| Status | Trigger |
|---|---|
| 🔴 STOCKOUT | On Hand = 0 |
| 🔴 BELOW ROP | (On Hand + On Order − Committed) < Reorder Point |
| 🟡 LOW | DOS < Lead Time, or DOS < 30d |
| 🟢 HEALTHY | Otherwise |
| ⚪ NO DEMAND | Both Forecast 12mo and Rolling 12mo are 0 |

### ABC Classification

| Code | Meaning | Where shown |
|---|---|---|
| **A** | High Volume | Main views (per-marketplace tabs) |
| **B** | Medium Volume | Main views |
| **C** | Low Volume | Main views |
| **D** | Phase-In (new) | Main views |
| **E** | Phase-Out | Bottom section of per-marketplace tabs + 🗑 Phase-Out tab |
| **F** | Other | 🗑 Phase-Out tab only |
| **I** | Ind. Component | 🗑 Phase-Out tab only |
| **S** | Sales BOM (combo packs) | 🗑 Phase-Out tab only + 🏷 Bundles tab |
| **Z** | Obsolete | 🗑 Phase-Out tab only |

Source: SAP Item Master CSV (`Item No.` UPC match) · manual overrides in `ABC_OVERRIDE` dict in `build_report.py` for mid-cycle changes.

### Demand Volatility (Phase 3)

Coefficient of variation (CV) of last 12 months of actuals:

| Bucket | CV % | Interpretation |
|---|---|---|
| 🟢 STABLE | <30% | Predictable demand — normal buffer enough |
| 🟡 MODERATE | 30-60% | Some swing — slight buffer cushion |
| 🔴 VOLATILE | >60% | Erratic — extra buffer or safety stock |
| — | <4mo data | INSUFFICIENT history |

Source: Sellerboard 12mo for Amazon · Valogix history for non-Amazon

### PO ETA

- Source: SAP Open Purchase Order Report
- Per item × channel: earliest `Original Due Date` among open POs
- ⚠️ flag = `Original Due Date == Posting Date` (SAP data quality issue — due date wasn't filled in)
- ETA = warehouse arrival date (NOT port date), based on the receiving warehouse code on the PO
- Warehouse → channel: `AMZN-MT/SS → Amazon US` · `SBGA-MT/SS → Shopify` · `FLO-MTB / AMZ-MT* / AMZ-NF* → Floship Intl`

---

## 🔑 Authoritative source rules

Multiple inputs can carry overlapping data (e.g., SoStocked also has FBA stock). Pipeline trusts:

| Field | Authoritative source | Why |
|---|---|---|
| **FBA Stock** | Seller Central FBA Inventory Report | Direct from Amazon — immune to SoStocked column-name changes |
| **AWD Stock + AWD Inbound** | Seller Central AWD Inventory Report | Direct from Amazon AWD system |
| **Adj. Velocity (Amazon)** | SoStocked `Adj. Velocity` | SoStocked's stockout-corrected velocity is the best signal |
| **Shopify On Hand** | ShipBob On Hand Summary | Shopify orders ship from ShipBob — that's the operational truth |
| **30-day velocity (non-Amazon)** | Valogix last-closed-month actuals | Apples-to-apples with Amazon's 30d basis |
| **Walmart NFMD inventory + forecast** | Walmart Seller Center direct | NFMD not in Valogix |
| **ABC code** | SAP Item Master | + manual `ABC_OVERRIDE` for mid-cycle changes |
| **Cost per UPC** | Valogix `Inventory Cost` | Only place we have cost data |
| **Product description (canonical)** | SAP Item Master `Item Description` | Overrides marketplace-specific titles |
| **PO ETA** | SAP Open POs `Original Due Date` | Planning-side commit date |

---

## 🗂 File system layout

```
C:\Users\Tom Sapia\MTB-SupplyChain\
├── reports\
│   ├── sostocked\<BRAND>\           ← 9 weekly files (auto-archive after combine)
│   ├── seller-central\<BRAND>\      ← AWD + FBA Inventory CSVs
│   │   └── awd-to-fba-shipments\    ← parked — accumulating only
│   ├── shipbob\<BRAND>\             ← On Hand Summary
│   │   └── _new-format\<BRAND>\     ← parked — accumulating only
│   ├── walmart\<BRAND>\             ← WFS Inventory .xlsx
│   ├── floship\                     ← Product Inventory export
│   ├── valogix\                     ← Item-Location-History-Forecast CSV
│   ├── valogix-exceptions\          ← History Exception Report CSV
│   ├── sellerboard\<BRAND>\         ← Sales by product/month .xlsx
│   ├── sap-open-pos\                ← SAP Open Purchase Order Report .xlsx
│   ├── item-master\                 ← item_master.xlsx (as-needed)
│   ├── in-transit\                  ← IN_TRANSIT_LOG_YYYY-MM-DD.xlsx (manual)
│   ├── weekly\                      ← (auto-generated) Weekly_Forecast_*.xlsx
│   └── archive\                     ← (auto-rotated) every stale file lives here forever
│       ├── sostocked\YYYY-MM-DD\
│       ├── seller-central\<BRAND>\YYYY-MM-DD\
│       └── ...
├── outputs\
│   ├── YYYY-MM-DD\
│   │   ├── sku-review-*.xlsx        ← carryover from prior week (you fill in)
│   │   ├── demand-plan-*.{xlsx,json,md}
│   │   ├── weekly-report-*.xlsx     ← THE deliverable
│   │   └── action-plan-*.xlsx
│   └── latest\                      ← junction → SharePoint synced folder
│       └── weekly-report-*.xlsx     ← auto-published copy
└── scripts\
    ├── combine_forecast.py
    ├── demand_planning.py
    ├── build_report.py              ← primary builder, 14 tabs
    ├── build_action_plan.py
    ├── build_shipment_tracking.py
    └── one_off_*.py                 ← ad-hoc reports (E-items, Valogix variance, etc.)
```

---

## 🔁 Standard weekly cadence

1. **Monday morning** — pull all 11 source files into their folders (see [[06 Processes & SOPs/(C) Weekly Inputs Sourcing SOP]])
2. **Run the 3 scripts** in order:
   ```bash
   cd C:\Users\Tom Sapia\MTB-SupplyChain
   python scripts\combine_forecast.py
   python scripts\demand_planning.py
   python scripts\build_report.py
   ```
3. **Open** `outputs\latest\weekly-report-YYYY-MM-DD.xlsx` (or pulls from SharePoint)
4. **Default view = Amazon US** with priority items at the top
5. **Work the action list** — top of the Priority Actions tab
6. **Fill out next week's sku-review** for items you've actioned

---

## ❓ Common questions answered

### "Why is my item not showing on Amazon US?"

Check ABC classification:
- If **E (Phase-Out)** → it's in the bottom "PHASE-OUT" section of Amazon US AND on the 🗑 Phase-Out tab
- If **F, I, S, Z** → routed to 🗑 Phase-Out & BOMs tab (not on per-marketplace tabs)
- If **INACTIVE** (velocity < 0.1/day) → bottom "INACTIVE" section of Amazon US

If completely missing, likely a UPC normalization issue — check `ABC_OVERRIDE` and the SAP item master for that UPC.

### "Why does the FBA stock number differ from what I see in Seller Central?"

The report mirrors Seller Central exactly:
- `FBA AVAILABLE` (sellable now) = SC `Available`
- `+ FC TRANSFER` (in motion between FCs) = SC `FC Transfer`
- `= FBA Stock` = SC "On-hand" panel total

If these don't match, it's a pipeline bug — file an issue.

### "What does the ⚠️ next to PO ETA mean?"

Original Due Date = Posting Date on that SAP PO row. Someone created the PO but didn't enter the actual expected delivery date in SAP. Fix it in SAP so the column shows a real arrival date.

### "Why are my 'On Order (Pipeline)' and 'On Order (Supplier)' numbers different?"

- **AMZN PIPE** = already in motion to Amazon (FBA pipeline + AWD inbound from Seller Central)
- **SUPPLIER** = open POs to supplier from Valogix AMZN-MT + AMZN-SS warehouses (not yet shipped)
- Total expected inbound = AMZN PIPE + SUPPLIER

### "Why is my Walmart NFMD data different from Valogix?"

Walmart NFMD is **not in Valogix**. The pipeline pulls it directly from Walmart Seller Center (`reports/walmart/NFMD/inventory*.xlsx`). All other Walmart-SS data still comes through Valogix.

---

## 🚨 Troubleshooting

| Error | Likely cause | Fix |
|---|---|---|
| `KeyError: 'Adj. Velocity'` | SoStocked changed a column name again | Check the column header in the inventory CSV, update `demand_planning.py` |
| `PermissionError: [Errno 13] ... weekly-report-*.xlsx` | The file is open in Excel | Close it and re-run |
| `Forecast Total (Next 12 Months) not found` | Wrong Valogix export type | Re-pull from Valogix Reports → Item Location History Forecast (NOT the simplified inventory export) |
| Inventory Overview tab missing | (Expected) — replaced by full-universe per-marketplace tabs in May 2026 | None needed |
| Items with high velocity flagged INACTIVE | Seller Central reclassification overrode SoStocked status | Check the recompute log line for that ASIN |
| `🚨` flag count jumped | More POs in SAP have `Original Due Date == Posting Date` than usual | Check who's entering POs, fix workflow |

---

## 📚 Related references

- [[06 Processes & SOPs/(C) Weekly Analysis SOP — Step by Step]] — operational run-book
- [[06 Processes & SOPs/(C) Weekly Inputs Sourcing SOP]] — pull-list for the 11 sources
- [[06 Processes & SOPs/(C) Weekly Analysis Cheat Sheet — 1 Page]] — print-and-stick
- [[06 Processes & SOPs/(C) Valogix CSV Format Reference]] — Valogix CSV column structure
- [[06 Processes & SOPs/(C) ABC Classification Reference]] — full ABC code definitions
- [[06 Processes & SOPs/(C) Daily Morning Routine — SCM]] — daily routine that uses this report
- [[07 AI Tools & Builds/(C) Forecast Accuracy & Buffer Sizing — Build Plan]] — parked enhancement
- [[07 AI Tools & Builds/(C) AWD-to-FBA Shipment Pipeline — Parked]] — parked enhancement
- [[07 AI Tools & Builds/(C) ShipBob New Format Migration — Parked]] — parked enhancement

---

*Created May 11, 2026 · Owner: Tommy · Update this when the pipeline architecture changes*
