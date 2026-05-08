# (C) Weekly Analysis SOP — Step by Step

> The Monday-morning recipe to generate the weekly demand plan, weekly report, action plan, and shipment tracking. Top to bottom, end to end. First time = ~90 min. After 2-3 cycles = ~30-45 min.
>
> **Last updated:** May 4, 2026
> **Companion docs:** [[06 Processes & SOPs/(C) Weekly Inputs Sourcing SOP]] (where every file comes from) · [[06 Processes & SOPs/(C) Weekly Analysis Cheat Sheet — 1 Page]]

---

## What you'll have at the end

- 📊 **Weekly Report** — 12-tab Excel showing what's stocked out, what to reorder, what's healthy across all marketplaces
- ✅ **Action Plan** — exact list of POs to place + ShipBob send-ins
- 📦 **Shipment Tracking Report** — every container, truck, and air shipment in transit

---

## Pre-flight checklist

- [ ] Computer on, Python installed (one-time setup)
- [ ] Command Prompt access
- [ ] Logins for **all 3 Amazon brands** (MTB, NFMD, SS)
- [ ] Login for **SoStocked**
- [ ] Logins for **all 4 ShipBob brand accounts** (MTB, NFMD, SS, LUMOS)
- [ ] Logins for **Walmart Seller Center** (NFMD, SS)
- [ ] Login for **Floship**
- [ ] Login for **Valogix**
- [ ] Access to the **In-Transit Log** (SharePoint or whoever maintains it)

If any of those is "no" → fix that first.

---

# 🟦 PART 1 — Download the reports (45 min)

Goal: drop **24 files** into the right folders. **No renaming required** — the scripts auto-classify by columns and brand subfolder.

Don't worry about doing them in order. Tick each off as you go.

> Tip: use 4 Chrome incognito windows so you can be logged into multiple Amazon (and ShipBob) brands simultaneously.

---

## 📥 1 of 8 — SoStocked: 9 files (3 brands × 3 reports)

**Why:** Sales velocity, forecasts, FBA inventory, forecast accuracy across all 3 Amazon brands.

For each of the 3 brands (**MTB → 5118**, **NFMD → 5109**, **SS → 5119**), pull these 3 reports:

| # | Report | Where in SoStocked | Format |
|---|---|---|---|
| A | **Projected Forecast Model** | Forecast section → export | .xlsx |
| B | **Inventory** — pick **"Export Inventory with Breakdown by Warehouses"** | Inventory page → cloud-download icon (top right) | .csv |
| C | **Forecasted vs Actual (FvA)** | Reports section → Forecast Accuracy | .xlsx |

⚠️ **Verify Report B has ~50 columns.** If you see only 12-15 columns, you picked "Export Current View" by mistake. Re-pull with the "Breakdown by Warehouses" option.

**Where to drop:** organize into the brand subfolders — keep the files exactly as SoStocked names them, no renaming:
```
reports\sostocked\MTB\     reports\sostocked\NFMD\     reports\sostocked\SS\
```
(`Downloads\` works as a fallback too, but the brand folders make it visually obvious you grabbed all 3 reports for each brand.)

📚 Detail: [[06 Processes & SOPs/(C) Weekly Inputs Sourcing SOP#1️⃣ SoStocked]]

---

## 📥 2 of 8 — Amazon Seller Central: 6 files (3 brands × 2 reports)

**Why:** AWD inbound (the only ASIN-level supplier-to-warehouse signal we get) + comprehensive FBA inventory state.

For each of the 3 brands, pull these 2 reports:

| # | Report | Path in Seller Central | Format |
|---|---|---|---|
| A | **AWD Inventory Report** | Inventory → AWD → Replenishment / Auto-Replenishment Dashboard → Download | .csv |
| B | **FBA Inventory Report** (full, 97 cols) | Reports → Fulfillment → **FBA Inventory** | .csv |

⚠️ **Don't pull "Manage FBA Inventory" from the Inventory tab** — that's the abbreviated 30-column version. Use Reports → Fulfillment → FBA Inventory for the full file.

**Where to drop:**
```
reports\seller-central\MTB\
reports\seller-central\NFMD\
reports\seller-central\SS\
```

**No renaming.** Each CSV is auto-classified by its column structure.

📚 Detail: [[06 Processes & SOPs/(C) Amazon Seller Central — Reports Pull List]]

---

## 📥 3 of 8 — ShipBob: 4 files (4 brand logins)

**Why:** Independent inventory truth at ShipBob — validates Valogix and feeds Shopify fulfillment readiness.

ShipBob requires a separate login per brand — there's no master account. Sign in to each, export, and sign out.

| Brand | Path |
|---|---|
| MTB | shipbob.com → Inventory → Export → **On Hand Summary** |
| NFMD | (same) |
| SS | (same) |
| **LUMOS** | (same) |

ShipBob emails a download link. **You must be logged into the correct brand when clicking the link** — otherwise it grabs the wrong account's data.

**Where to drop:**
```
reports\shipbob\MTB\     reports\shipbob\NFMD\
reports\shipbob\SS\      reports\shipbob\LUMOS\
```

**No renaming.**

📚 Detail: [[06 Processes & SOPs/(C) ShipBob — Reports Pull List]]

---

## 📥 4 of 8 — Walmart Seller Center: 2 files (NFMD + SS)

**Why:** Direct truth for Walmart inventory. Walmart NFMD isn't in Valogix at all — this is the only way we see it.

For each brand login (NFMD, then SS):

1. Sign into Walmart Seller Center
2. Left menu → **WFS** → **Inventory**
3. Right side → **Download** → **All items** → **Download**
4. File downloads as **`.xlsx`** (Excel format)

**Where to drop:**
```
reports\walmart\NFMD\     reports\walmart\SS\
```

**No renaming.**

📚 Detail: [[06 Processes & SOPs/(C) Walmart Seller Center — Reports Pull List]]

---

## 📥 5 of 8 — Floship: 1 file

**Why:** International fulfillment for MTB only. Validates Valogix `FLO-MTB`.

1. Sign into Floship
2. Inventory → **Product Inventory** → Export

**Where to drop:**
```
reports\floship\
```

**No renaming.**

---

## 📥 6 of 8 — Valogix: 1 file

**Why:** Source of truth for non-Amazon channels — Shopify MTB, SS DTC, NFMD DTC, Walmart-SS, Floship Intl. Plus unit cost (the only place we get it) and 24 months of sales history.

1. Log into **Valogix**
2. Reports → **Item Location History Forecast** → all items, all locations
3. Export → CSV

The file downloads as `schain_itemLocationHistoryForecast_YYYY_MM_DD.csv`. **Don't rename.**

**Where to drop:**
```
reports\valogix\
```

The pipeline auto-archives older Valogix CSVs to `reports\archive\valogix\YYYY-MM-DD\`.

---

## 📥 7 of 8 — In-Transit Log: 1 file (skip if not updated)

**Why:** Master shipment tracker for everything in flight (containers + trucks + air).

1. Get the latest version (SharePoint or whoever maintains it)
2. Rename to `IN_TRANSIT_LOG_YYYY-MM-DD.xlsx`
3. Drop into `reports\in-transit\`

If nobody updated it this week → skip. The script falls back to the most recent file in that folder.

---

## 📥 8 of 8 — Carryover SKU Review (if you have decisions to fold in)

If you filled out last week's `sku-review-*.xlsx` (Active Y/N, Replenish From, Notes):

1. Save it as `sku-review-YYYY-MM-DD.xlsx` for **this week's date**
2. Drop into `outputs\YYYY-MM-DD\` (this week's folder — create it if it doesn't exist)

If today's file isn't there, the action plan auto-falls-back to the most recent one. Carryover-friendly.

---

## ✅ Sanity check before running

Open File Explorer → `MTB-SupplyChain\reports\`. You should see populated brand subfolders for SoStocked / seller-central / shipbob / walmart, plus floship + valogix + in-transit + item-master.

Don't worry if the SoStocked files are still in `Downloads\` — the combiner picks them up there too.

If anything is missing → go back and grab it before continuing.

---

# 🟧 PART 2 — Run the scripts (15 min)

Open Command Prompt (Start → type `cmd` → Enter). Navigate to the repo:

```
cd C:\Users\Tom Sapia\MTB-SupplyChain
```

Then run all 5 scripts in order:

```
python scripts\combine_forecast.py
python scripts\demand_planning.py
python scripts\build_report.py
python scripts\build_action_plan.py
python scripts\build_shipment_tracking.py
```

What each one does:

### Script 1 — `combine_forecast.py` (~10s)
Auto-detects all 9 SoStocked files (in `Downloads\` or `reports\sostocked\[BRAND]\`), combines them into `reports\weekly\Weekly_Forecast_YYYY-MM-DD.xlsx` (8 sheets), auto-archives raw files to `reports\archive\sostocked\YYYY-MM-DD\`.

### Script 2 — `demand_planning.py` (~30s)
Reads the combined forecast + AWD inbound CSV + (optional) carryover sku-review. Outputs:
- `outputs\YYYY-MM-DD\demand-plan-YYYY-MM-DD.xlsx` + `.json` + `.md`
- ~177 items classified by urgency (TRUE STOCKOUT / CRITICAL / HIGH / FBA REPL / HEALTHY / etc.)

### Script 3 — `build_report.py` (~60s) ⭐
The big one. Pulls demand plan + Valogix + Walmart-NFMD direct + item master + cost lookup + ABC + ShipBob inventory and builds the 12-tab Weekly Report.
- `outputs\YYYY-MM-DD\weekly-report-YYYY-MM-DD.xlsx`

### Script 4 — `build_action_plan.py` (~10s)
Reads the priority items + carryover sku-review and produces a 3-tab action plan: ShipBob send-ins / Supplier POs / Inactive & Phase Out.
- `outputs\YYYY-MM-DD\action-plan-YYYY-MM-DD.xlsx`

### Script 5 — `build_shipment_tracking.py` (~30s)
Reads the In-Transit Log + AWD CSV + (optional) FBA Inbound Shipments. Produces a 7-tab shipment dashboard.
- `outputs\YYYY-MM-DD\shipment-tracking-YYYY-MM-DD.xlsx`

---

## ✅ Sanity check after Part 2

In `outputs\YYYY-MM-DD\` you should see:

```
demand-plan-YYYY-MM-DD.xlsx     (5 sheets)
demand-plan-YYYY-MM-DD.json     (data file — don't open)
demand-plan-YYYY-MM-DD.md       (text summary)
weekly-report-YYYY-MM-DD.xlsx   ⭐ THE BIG ONE — 12 tabs
action-plan-YYYY-MM-DD.xlsx     (3 tabs)
shipment-tracking-YYYY-MM-DD.xlsx (7 tabs)
```

If a script errors → see Troubleshooting at the bottom.

---

# 🟩 PART 3 — Read the report (30 min)

Open `weekly-report-YYYY-MM-DD.xlsx`. Walk the tabs in this order:

| Tab | What's there |
|---|---|
| **Amazon US** | FULL UNIVERSE for Amazon US — action items at top (sorted by status urgency → DOS), green divider, then HEALTHY items below. E (Phase-Out) items excluded. New `ON ORDER (SUPPLIER)` column shows open POs from Valogix AMZN-MT + AMZN-SS. |
| **🇨🇦 Amazon CA** | FULL UNIVERSE for Amazon CA — same layout as Amazon US. No SUPPLIER on-order column (Valogix doesn't separate US vs CA POs). |
| **Shopify** | FULL UNIVERSE for Shopify — MTB / SS / NFMD all in one filterable list, action items + healthy split |
| **Walmart** | FULL UNIVERSE for Walmart — SS (Valogix) + NFMD (direct from Seller Center), action + healthy split |
| **Floship Intl** | FULL UNIVERSE for Floship — international SKUs, action + healthy split |
| **🚨 Priority Actions** | Amazon priority detail with full columns |
| **✅ Action Plan** | Three sections: ShipBob Send-ins · Supplier POs · Urgent (no SB stock) |
| **🏷 Bundles & Custom SKUs** | Non-UPC + combo/specials + special-account items |
| **🗑 Phase-Out, Obsolete & BOMs** | Combined visibility tab for everything off the active radar — sectioned by ABC: E (Phase-Out) → F (Other) → I (Ind. Comp.) → S (Sales BOM) → Z (Obsolete) |
| **📈 Forecast Pivot** | Valogix-style row-per-SKU × month grid. Last 12 months ACTUAL (sage heatmap) ‖ next 12 months FORECAST (amber heatmap). TTM / Prior-TTM / YoY % / Forward-12mo summary cols. Frozen identity panes + auto-filter. Covers all channels. |
| **📊 Amazon Sales History** | 12 months of Amazon actuals by ASIN from Sellerboard — TTM Qty · YoY % · Avg/mo · Last-mo profit · ROI % |
| **📈 Amazon FvA** | Forecast vs Actual variance from SoStocked snapshots — color-coded (red ≥±20%, amber ±10–20%, green <±10%) |
| **📊 Sales Anomalies** | Statistical outliers from Valogix History Exception Report — flags bad-data months automatically |

**Removed tabs (April → May 2026 redesign):**
- ❌ Weekly Summary, Key SKUs, Multi-Channel, Dashboard, Inventory Overview — content folded into per-marketplace tabs (Amazon US, Amazon CA, Shopify, Walmart, Floship Intl) which now show the full universe per channel
- ❌ Brand tabs (MTB / SS / NFMD) — per-channel tabs filterable by brand replace these
- ❌ Separate Phase-Out / Obsolete / Sales BOMs tabs — merged into one combined `🗑 Phase-Out, Obsolete & BOMs` tab

**Default open tab:** Amazon US.

**Hover any column header** to see a comment showing exactly where the data comes from (source system + column name + computation logic).

**Volatility columns (live on every per-marketplace tab):**
- `DEMAND VOLATILITY` — bucket: STABLE (CV<30%) · MODERATE (30–60%) · VOLATILE (>60%) · — (insufficient history)
- `VOLATILITY CV %` — raw coefficient of variation
- Source: Sellerboard 12mo for Amazon · Valogix history for non-Amazon

---

# 🟪 PART 4 — Take action (1-3 hours)

This is judgment. The report tells you WHAT — you decide WHO and WHEN.

## Decision rules

| Status | What it means | What to do |
|---|---|---|
| 🔴 **TRUE STOCKOUT** | FBA + AWD + ShipBob all = 0. Genuinely no stock anywhere. | Urgent supplier PO. Air freight if needed. |
| 🚨 **AMAZON STOCKOUT** | FBA = 0 but ShipBob/AWD has stock to bridge. | **ShipBob → FBA send-in TODAY.** No new supplier PO needed yet. |
| 🔴 **CRITICAL** / BELOW ROP | DOS ≤ Lead Time. Will run out before next normal PO arrives. | Today or tomorrow. Place supplier PO. Consider expedite. |
| 🟠 **HIGH** / LOW | DOS ≤ Lead Time + 30. Need to act this week. | Schedule the PO. |
| 🟡 **FBA REPLENISHMENT** | FBA = 0 but ShipBob has plenty (>30 days coverage). | Routine ShipBob → FBA send-in this week. |
| 🟢 **HEALTHY** | DOS > Lead Time + 30. | Skip — no action needed. |
| ⚫ E / Z classification | Phase-out or obsolete. | No new POs. Deplete and stop replenishing. |

## ⚠️ Sanity check before acting on a priority item

If something looks off — flagged TRUE STOCKOUT but you remember stock exists — verify in Seller Central directly:

1. Open the item in Amazon Seller Central → Inventory page
2. Check **`Available in FBA`** and **`Available in AWD (units)`** numbers
3. Compare to the report's `FBA STOCK` and `AWD STOCK` columns (expand the Amazon stock breakdown group on Weekly Summary)
4. They should match exactly — both come from the same Seller Central reports

**If they don't match,** it's a pipeline issue (not a real stockout). Slack/Teams Tommy and re-pull the Seller Central files.

## For each priority item

1. Open **Action Plan** tab — tells you ShipBob send-in vs Supplier PO
2. Note **PO Qty** and **Reorder By** date
3. Email supplier or place PO in your system
4. Mark it done in your daily action plan
5. Update next week's `sku-review-*.xlsx` so Claude knows it's been actioned

---

# 🟫 PART 5 — File the report

1. Weekly Report stays in `outputs\YYYY-MM-DD\` — future runs reference it
2. Email link to leadership if needed
3. Drop a copy into the **SharePoint Master Brain** folder for archival

---

# 🆘 Troubleshooting

| Symptom | Fix |
|---|---|
| `No such file or directory` | A file is missing from `reports\`. Re-check Part 1 by source system. |
| `Permission denied` (Excel) | An Excel file is open. Close it. Re-run. |
| `ModuleNotFoundError` | Run: `pip install pandas openpyxl` |
| Output Excel missing tabs | Re-run `build_report.py`. |
| Numbers look wildly wrong | Confirm all 24 inputs are in the right folders. Re-run from Script 1. |
| Action plan saves to old date folder | This was a bug — fixed May 4. Pull latest scripts. |
| Item count drops dramatically | Likely the wrong SoStocked Inventory export (Current View vs Breakdown by Warehouses). Re-pull Report B. |
| You're stuck > 30 min | Slack/Teams Tommy. Don't burn 2 hours debugging alone. |

---

# 📅 Cadence

Run **every Monday morning** (or first thing Tuesday if you can't on Monday).

Total time: ~3-4 hours your first month, ~1.5 hours when you're seasoned.

---

## Glossary

| Term | Plain English |
|---|---|
| DOS | Days of Supply — days until we run out at current sales pace |
| ROP | Reorder Point — inventory level that triggers a new order |
| FBA | Fulfilled by Amazon — Amazon stores and ships our products |
| AWD | Amazon Warehousing & Distribution — Amazon's holding warehouse before FBA |
| 3PL | Third Party Logistics — external warehouses (ShipBob, Floship) |
| SKU | Stock Keeping Unit — a specific product variant |
| UPC | Universal Product Code — the 12-digit barcode on a product |
| ASIN | Amazon Standard Identification Number — Amazon's unique ID per product |
| ABC | Volume classification (A/B/C/D/E/Z — see [[06 Processes & SOPs/(C) ABC Classification Reference]]) |
| Lead Time | Days between placing a PO and receiving the goods |
| OTIF | On Time In Full — KPI for whether shipments arrive on schedule and complete |

---

*Rewritten: May 4, 2026 · Owner: Supply Chain (Tommy + Augusto)*
