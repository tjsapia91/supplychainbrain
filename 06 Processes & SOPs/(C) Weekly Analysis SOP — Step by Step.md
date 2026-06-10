# (C) Weekly Analysis SOP — Step by Step

> The Monday-morning recipe to generate the weekly supply chain report end-to-end. Top to bottom, first time = ~60 min. After 2-3 cycles = ~25-30 min (mostly download time).
>
> **Last updated:** June 8, 2026
> **Companion docs:**
> - [[06 Processes & SOPs/(C) Weekly Analysis Cheat Sheet — 1 Page]] (quick reference)
> - [[06 Processes & SOPs/(C) Weekly Inputs Sourcing SOP]] (where every file comes from, in detail)
> - `Weekly Report Explanation/` folder (tab-by-tab reference)

---

## What you'll have at the end

- 📊 **`weekly-report-YYYY-MM-DD.xlsx`** — 19-tab Excel — the operator's dashboard
- 🎯 **✅ THIS WEEK tab** (5 sections) — what to do this Monday
- 🏭 **PO Priority tab** — vendor-by-vendor manufacturing priority list to send suppliers
- 📦 **In Transit tab** — what's en route + real ETAs from the In-Transit Log
- 📋 **SAP Open POs tab** — every open PO + same-day-error flags
- Supporting reports auto-generated alongside: `demand-plan.json/md`, `velocity-watch.xlsx`, `order-list.xlsx`

---

## Pre-flight checklist (one-time)

- [ ] Computer on, Python installed (`pandas openpyxl` in env)
- [ ] Command Prompt access
- [ ] Logins for **all 3 Amazon brands** (MTB · NFMD · SS) — US **and** CA
- [ ] Login for **SoStocked**
- [ ] Logins for **all 4 ShipBob brand accounts** (MTB · NFMD · SS · LUMOS)
- [ ] Logins for **Walmart Seller Center** (NFMD · SS)
- [ ] Login for **Floship**
- [ ] Login for **Valogix**
- [ ] Login for **Sellerboard**
- [ ] SharePoint access for the **In-Transit Log**
- [ ] SAP access for the **Open Purchase Order Report**

If any of those is "no" → fix that first.

---

# 🟦 PART 1 — Download the reports (~30 min)

**Drop everything into `C:\Users\Tom Sapia\Downloads\`.** No folder navigation needed. `sort_downloads.py` (runs first as a pre-flight) classifies every recognized file and routes it.

Don't worry about the order — tick each off as you go. Use 4 Chrome incognito windows to be logged into multiple brand accounts simultaneously.

---

## 📥 1 of 11 — SoStocked: 9 files (3 brands × 3 reports)

**Why:** Sales velocity, monthly forecasts, FBA inventory, forecast accuracy.

For each of the 3 brands (**MTB → 5118** · **NFMD → 5109** · **SS → 5119**), pull these 3:

| # | Report | Where in SoStocked | Format |
|---|---|---|---|
| A | **Projected Forecast Model** | Forecast section → export | `.xlsx` |
| B | **Inventory** — pick **"Export Inventory with Breakdown by Warehouses"** | Inventory page → cloud-download icon (top right) | `.csv` |
| C | **Forecasted vs Actual (FvA)** — current month | Reports → Forecast Accuracy | `.xlsx` |

⚠ **Verify Report B has ~50 columns.** If you see only 12-15 cols you picked "Export Current View" — re-pull with the Breakdown by Warehouses option.

📚 Detail: [[06 Processes & SOPs/(C) Weekly Inputs Sourcing SOP#1️⃣ SoStocked]]

---

## 📥 2 of 11 — Amazon Seller Central US: 6 files (3 brands × 2 reports)

**Why:** Authoritative FBA inventory + AWD inbound (the only ASIN-level supplier→AWD signal).

For each brand:

| # | Report | Path in Seller Central | Format |
|---|---|---|---|
| A | **AWD Inventory Report** | Inventory → AWD → Replenishment Dashboard → Download | `.csv` |
| B | **FBA Inventory Report** (full, 97 cols) | Reports → Fulfillment → **FBA Inventory** | `.csv` |

⚠ **Don't pull "Manage FBA Inventory" from the Inventory tab** — that's the 30-col abbreviated version.

---

## 📥 3 of 11 — Amazon Seller Central CA: 3 files (3 brands × 1 report)

**Why:** Canada FBA state. MTB has no AWD program in CA so we pull FBA only.

For each brand, from the **CA marketplace** in Seller Central:

| Report | Path | Format |
|---|---|---|
| **FBA Inventory Report** (Canada) | Reports → Fulfillment → FBA Inventory (with `amazon.ca` market selected) | `.csv` |

---

## 📥 4 of 11 — ShipBob: 4 files (4 brand logins, NEW format)

**Why:** Independent inventory truth at ShipBob — primary fulfillment for Shopify + manual Amazon send-ins.

ShipBob requires separate login per brand — there's no master account. For each:

| Brand | Path |
|---|---|
| MTB · NFMD · SS · LUMOS | Inventory → Inventory Status → **Export → Export All Data** |

⚠ **NEW FORMAT REQUIRED.** If `build_report.py` logs `→ ShipBob (LEGACY)` you're still pulling the old On Hand Summary. The new format includes columns: Sellable / Committed / Exception / Backordered / Incoming / Internal Transfer / Lot Number / Fulfillment Center.

---

## 📥 5 of 11 — Walmart: 4 files (2 brands × 2 reports)

**Why:** Walmart Marketplace inventory + Inventory Health (aged-out, expiring, sell-through).

For NFMD and SS each:

| Report | Path |
|---|---|
| **Marketplace Inventory** (bulk export) | Seller Center → Reports → Marketplace Bulk Inventory |
| **Inventory Health** | Seller Center → Reports → Inventory Health |

---

## 📥 6 of 11 — Floship: 1 file

**Why:** International inventory for Spa Sciences direct.

| Report | Path |
|---|---|
| **Product Inventory export** | Floship → Inventory → Product Inventory → Export |

---

## 📥 7 of 11 — Valogix: 2 files

**Why:** Multi-channel forecast model + history exception (statistical outlier flags).

| Report | Format |
|---|---|
| **Item-Location-History-Forecast** | `schain_itemLocationHistoryForecast_*.csv` |
| **History Exception Report** | `schain_itemLocationHistoryException_*.csv` |

---

## 📥 8 of 11 — SAP: 1 file

**Why:** Every open purchase order — the system-of-record for what's been ordered from suppliers.

| Report | Format |
|---|---|
| **Open Purchase Order Report** (full export) | `Open POs.xlsx` |

⚠ **Same-day SAP errors are endemic.** When `posting_date == due_date == ship_by_date`, the buyer entered the PO with no realistic ETA. The pipeline auto-flags these in the SUPPLY RISK section of THIS WEEK.

---

## 📥 9 of 11 — In-Transit Log: 1 file

**Why:** Real ETAs for what's actually shipped (overrides SAP's same-day-error noise). Distinguishes Amazon-bound vs ShipBob-bound containers.

Pull from SharePoint:
- Open the master `IN TRANSIT LOG.xlsx`
- File → Download → Excel
- Rename to `IN_TRANSIT_LOG_YYYY-MM-DD.xlsx` (matches the auto-classify regex)
- Drop in Downloads (sort_downloads will route to `reports/in-transit/`)

The WATER tab is the primary source. Pipeline filters by cell fill color:
- 🟩 **Green** = arrived (ignored)
- 🟠 **Orange** = Amazon-bound (active)
- ⬜ **White** = ShipBob-bound (active)

---

## 📥 10 of 11 — Sellerboard: 6 files (3 monthly + 3 CA dashboard)

**Why:** Amazon US sales velocity (Monthly) + Amazon CA marketplace-filtered velocity (CA Dashboard).

### Monthly — `Sales by Product/Month` (3 files, **monthly cadence**)

For each brand (MTB · NFMD · SS):
- Sellerboard → Sales by Product/Month
- Max date range
- Marketplace ignored (combined US + CA — pipeline handles split)

### CA Dashboard — `Dashboard Products` (3 files, weekly cadence)

For each brand:
- Sellerboard → Dashboard Products
- **Set marketplace filter = `amazon.ca`** (REQUIRED — without it, CA velocity is 30-50× inflated)
- Last 90 days

---

## 📥 11 of 11 — Optional / on-change-only files

These don't need to be pulled weekly:

| File | When to pull |
|---|---|
| SAP `SAPABCCLASSIFICATION.xlsx` → `reports\item-master\item_master.xlsx` | Only when ABC codes change in SAP |
| `amazon-sku-mapping.xlsx` | Only when new Amazon SKUs launch (Tommy maintains internally) |
| 15 FvA backfill files (5 months × 3 brands) | One-time backfill (Apr 2026) — drop in `reports\sostocked\[BRAND]\fva-history\` |

---

# 🟦 PART 2 — Run the pipeline (~5 min)

Open Command Prompt → `cd C:\Users\Tom Sapia\MTB-SupplyChain` → run:

```
python scripts\demand_planning.py
python scripts\build_report.py
```

**That's it.** `build_report.py` auto-chains the rest of the pipeline:

1. **`sort_downloads.py`** runs as a pre-flight — auto-classifies every recognized file in Downloads and routes it to the right `reports\` subfolder. Unrecognized files (screenshots, personal docs) are left in place.
2. **Loads** all classified inputs into memory: SoStocked PFM, FBA, AWD, ShipBob, Walmart, Floship, Valogix, Sellerboard, SAP POs, In-Transit Log
3. **Computes** per-SKU urgency, stockout dates, Days of Supply, PO sizing, transfer recommendations
4. **Runs `run_deep_plan()`** — the 7-stage multi-echelon workflow for all A+B+C+D items (returns SUPPLY RISK rows)
5. **Builds** the 19-tab `weekly-report-YYYY-MM-DD.xlsx` with the ✅ THIS WEEK tab as the cover sheet
6. **Auto-generates** sister files: `velocity-watch.xlsx`, `order-list.xlsx`, `demand-plan.json/md`

**Expected console output:** look for the `✅ Saved: …weekly-report-2026-MM-DD.xlsx` line + the `📤 Published: …outputs/latest/…` line. If you see `❓ UNSORTED` warnings, fix those manually before relying on the report.

---

# 🟦 PART 3 — Open the report (the 30-minute review)

Open `outputs\latest\weekly-report-*.xlsx`. The active tab on open is **✅ THIS WEEK**.

## 🎯 Read THIS WEEK top-to-bottom (10 min)

5 sections, each with a clear action:

### 1. 🛒 ORDER (Supplier POs to place this week)
- Items where THIS WEEK ORDER engine says "place a new PO with the supplier now"
- For each: `ORDER  X,XXX units` + stockout date + supplier name
- Action: send the PO via SAP / supplier portal

### 2. ⏱ EXPEDITE (Open POs arriving AFTER stockout)
- Items where the existing PO is late vs the projected stockout (gap > 0 days)
- For each: `EXPEDITE  (Xd late)` + PO arrival date
- Action: **call the supplier this week.** Negotiate partial air-freight or rush ocean booking.

### 3. 🚛 TRANSFER (ShipBob → Amazon send-ins)
- FBA is running thin BUT ShipBob has stock — file a send-in
- Context shows: `SB net: X (Y raw − Z Shopify reserve) · FBA: Nd`
- Action: create the send-in in Amazon Seller Central → AWD inbound

### 4. ⚠ SUPPLY RISK (POs with unverified ETAs landing < 90d)
- Open POs in SAP with same-day date errors (posting = due = ship-by)
- Means SAP's claimed ETA can't be trusted — supplier may or may not actually have the units shipped
- Action: `CONFIRM  PO #XXXX  (qty → AMZN-SS or SBGA-SS)`. Call supplier and get real ETA + container/B/L number.

### 5. ⏳ WATCH (PO covered — verify ETA next week)
- Items where there IS a PO in flight that *should* cover the stockout
- Low-action — just verify the PO didn't slip when you re-run next week

---

## 🏭 Open the PO Priority tab (10 min)

After scanning THIS WEEK, switch to **🏭 PO Priority**. This is what you send to each supplier.

**Layout:** grouped by vendor (Ningbo Dream Big · Ningbo Ocean · Ningbo Rivers · Vastwing · etc.). Within each vendor section:

| Rank | Status | PO# | UPC | Item | Brand | Units (still at supplier) | Stockout Date | Days | Reason |
|---|---|---|---|---|---|---:|---|---:|---|

**Status ranking (days-first, June 5 update):**
- 🔴 **OVERDUE** (< 0d) — already stocked out
- 🔴 **CRITICAL** (≤ 30d)
- 🟠 **HIGH** (31-90d)
- 🟡 **MEDIUM** (91-180d)
- 🟢 **HEALTHY** (> 180d) — these are open POs but not urgent
- ⚪ **NO DATA** — verify before ordering

**Key fields:**
- **Units (still at supplier)** = SAP open qty − In-Transit Log qty. Only the unshipped portion shows here.
- **Stockout Date** = total supply pipeline stockout (current stock + inbound). Drives the rank.
- **Reason** = days-driven explanation: *"CRITICAL: 28d to stockout — manufacture immediately"* etc.

**Action:** Copy each vendor's CRITICAL + HIGH rows into an email → send to supplier with subject *"Manufacturing Priority — Week of YYYY-MM-DD"*. The supplier sees their POs ranked by urgency.

---

## 📦 Open the In Transit tab (5 min)

**33 active line items typical** — 21 Amazon-bound + 12 SB-bound. Shows what's ALREADY SHIPPED:
- PO #, vendor, UPC, item, qty shipped, qty received, sailed date, ETA at port, warehouse delivery date
- Destinations: AMZ (Amazon-bound — orange in source log) vs SB (ShipBob-bound — white)

**Cross-reference here before assuming a PO is overdue.** Example: SAP says PO 3092 is open with 4,320 unreceived units. The In-Transit Log confirms it arrived May 13. The SAP record just wasn't closed out.

---

## 📋 SAP Open POs tab (5 min — skim only)

Every open PO from SAP. Use as a reference / audit trail. Same-day-error rows are flagged with ⚠. The SUPPLY RISK section above is the curated subset.

---

## Other tabs (reference only)

| Tab | Use it when |
|---|---|
| **Amazon US** | Per-marketplace deep dive — stockout dates, PO ETAs, DOS, daily sales |
| **Amazon CA** | Same as US but Canada-specific. CA has no AWD program for MTB. |
| **Amazon UK / AU / EU** | International — limited data, PO-only synthesis |
| **ShipBob** | SB inventory by FC, with Shopify reserve math visible |
| **Walmart** | Walmart Marketplace inventory + Inventory Health (aged stock) |
| **TikTok** | TikTok Shop — SAP inventory + wholesale-receipt velocity |
| **Floship Intl** | International fulfillment state |
| **🏷 Bundles & Custom SKUs** | Non-UPC custom codes (BODYBRBLK etc.), bundles, special accounts |
| **🗑 Phase-Out, Obsolete & BOMs** | E/F/I/S/Z items — write-off exposure visibility |
| **📈 Forecast Pivot** | Per-item × per-month forecast matrix (for forecast tuning) |
| **📊 Amazon Sales History** | Sellerboard monthly view per ASIN |
| **📈 Amazon FvA** | Sellerboard Forecast vs Actual variance |
| **📊 Sales Anomalies** | Statistical outliers from Valogix exception report |
| **🔄 SAP↔SB Rebalance** | Weekly variance scan vs SAP inventory at SB warehouses — see monthly cadence below |
| **🌏 SAP↔Floship Rebalance** | Weekly variance scan vs SAP inventory at FLO-MTB — SS/NFMD have no SAP counterpart (FLO-only list) |

---

# 🟦 PART 4 — Make decisions

By now you have a clean view. Two pro-discipline rules:

1. **Trust the system.** If THIS WEEK / PO Priority say it's fine, it's fine. Don't second-guess by reviewing every SKU.
2. **Supplier calls > dashboard hours.** The bottleneck most weeks is a phone conversation, not a spreadsheet. EXPEDITE + SUPPLY RISK rows are calls to make this week.

### Monthly + quarterly cadences (added beyond the weekly flow)

| Cadence | What runs | Owner | Time |
|---|---|---|---|
| **Weekly** (every Monday) | Full weekly report. Skim 🔄 SAP↔SB Rebalance tab — only act if variances are flagged ⚠ | Tommy | included in weekly run |
| **Monthly** (1st Monday of month) | **Formal SAP↔3PL reconciliation:** run `python scripts/build_sap_rebalance.py` standalone for the combined cleanup file (ShipBob + Floship in one workbook, 9 tabs). Investigate every flagged variance (>50u or >5%). Update SAP to match physical, OR work with the 3PL to investigate missing units. Aligns with financial monthly close. | Tommy + SAP admin | ~3 hrs |
| **Quarterly** | Physical cycle count at one or two SB FCs (rotate quarterly) to validate ShipBob's own numbers. | Tommy + ShipBob ops | ~half day |
| **Annually** | Full physical inventory + write-down accounting | Finance + ops | full day |

The 🔄 SAP↔SB Rebalance tab in weekly-report.xlsx is the early-warning system between formal monthly passes. Threshold: variance flagged ⚠ when |Δ| > 50 units OR > 5% of SAP qty.

### Time budget (for a clean week)

| Activity | Time |
|---|---|
| Monday AM — pipeline run + report open | 30 min |
| Monday AM — scan THIS WEEK + write down decisions | 30 min |
| Monday/Tuesday — execute PO placements + send-ins | 1-2 hrs |
| Tue-Wed — supplier calls (EXPEDITE + SUPPLY RISK list) | 2-3 hrs |
| Friday — week-over-week check | 15 min |
| **Total** | **~5 hrs/week** for the analysis-and-decide loop |

Anything more = miscalibrated. If a future analyst joins the team, deeper triage gets delegated to them.

---

# 🟦 PART 5 — Send to suppliers

For each vendor in 🏭 PO Priority:
1. Take their CRITICAL + HIGH section
2. Paste into an email (subject: *"Manufacturing Priority — Week of YYYY-MM-DD"*)
3. Send to their contact (vendor list in `02 Vendors & Suppliers/`)

Template:

> Hi [Name],
>
> Below is our manufacturing priority for this week. Please confirm by [DAY] which POs you can ship by their landing dates.
>
> [Paste the table — PO# · Units · Item · Stockout Date · Days]
>
> If any cannot be shipped on schedule, we need to know NOW so we can evaluate air freight or expedited ocean.
>
> Thanks,
> Tommy

---

# 🟦 Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `PermissionError: weekly-report-*.xlsx` | Excel has the file open | Close Excel, rerun |
| `❓ UNSORTED` in sort log | Classifier doesn't recognize the file pattern | Move manually OR add rule to `scripts/sort_downloads.py` |
| Numbers don't match Seller Central dashboard | CSV is cached older than the dashboard | Re-download FBA Inventory Report |
| `⚠️ Sellerboard Monthly is N days old` | Time to refresh (monthly cadence) | Pull the 3 monthly Sellerboards |
| `⚠️ Sellerboard CA Dashboard is N days old` | Weekly cadence; needs refresh | Pull 3 CA Dashboards with `amazon.ca` filter |
| Velocity inflated 30-50× on CA items | Sellerboard Monthly applied to CA rows OR CA Dashboard pulled without filter | Re-pull CA Dashboard with `marketplace=amazon.ca` |
| `→ ShipBob (LEGACY)` log line | Old On Hand Summary format | Re-export from Inventory Status → Export All Data |
| In-Transit Log dates look stale | You pulled an old SharePoint copy | Pull latest from SharePoint and re-drop in Downloads |
| PO Priority shows NO DATA on items the ORDER section flagged | `supplier_rows` lookup gap | Verify build_report ran to completion; check console for errors |
| Numbers on Amazon US tab differ from THIS WEEK | THIS WEEK uses build_order_list math; Amazon tab uses raw per-channel | Both are right, different views (THIS WEEK = "needs PO this week" perspective) |

---

## When something deeper breaks

If a tab is empty or numbers look wildly off:
1. Re-run `build_report.py` once more — sometimes a transient file lock resolves itself
2. Check the console output for the line `→ ShipBob: N SKUs across X brand files…` — verify all 4 brand files loaded
3. Check Valogix line: `→ Valogix: schain_itemLocationHistoryForecast_*.csv` — confirms latest CSV loaded
4. Check SAP Open POs line: `📋 SAP Open POs — N POs · ⚠️ X same-day flags`
5. Check In-Transit line: `📦 In Transit — N active (X → Amazon · Y → ShipBob)`

If any of those lines say "0" or "skipped" — go back to Part 1 and verify the corresponding input file is in Downloads.

---

## Related docs

- [[06 Processes & SOPs/(C) Weekly Analysis Cheat Sheet — 1 Page]] — the 1-page reference
- [[06 Processes & SOPs/(C) Weekly Inputs Sourcing SOP]] — where every file comes from (detailed)
- [[06 Processes & SOPs/(C) ABC Classification Reference]] — A/B/C/D/E/Z code meanings
- [[06 Processes & SOPs/(C) ShipBob Inventory Protection — Channel Reserve Logic]] — Shopify reserve math
- [[10 System/(C) Master SupplyChainBrain — Architecture]] — three-layer architecture
- `Weekly Report Explanation/` folder — tab-by-tab field reference (20 files, one per tab)

---

*Updated: 2026-06-08 · Refresh after THIS WEEK 5-section + PO Priority + In Transit tab additions (June 5)*
