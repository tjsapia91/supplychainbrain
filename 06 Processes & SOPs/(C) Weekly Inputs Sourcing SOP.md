# (C) Weekly Inputs Sourcing SOP — Where Every Report Comes From

> Canonical reference cataloging every input the weekly pipeline consumes. Tells you which dashboard, which menu, which export, where it lands, and how the script finds it.
>
> **Last updated:** May 6, 2026 (added SAP Open POs · Sellerboard Sales-by-Month · Valogix History Exception Report)
> **Companion docs:** [[06 Processes & SOPs/(C) Weekly Analysis SOP — Step by Step]] · [[06 Processes & SOPs/(C) Weekly Analysis Cheat Sheet — 1 Page]]

---

## 📋 At a glance — 11 source systems, 28 weekly files (+2 occasional)

| # | Source | What | Files | Frequency | Drop into |
|---|---|---|---|---|---|
| 1 | **SoStocked** | 3 reports × 3 brands (Forecast + Inventory + FvA) | **9** | Weekly | `Downloads\` (auto-detected & moved) |
| 2 | **Amazon Seller Central** | 2 reports × 3 brands (AWD + FBA Inventory) | **6** | Weekly | `reports\seller-central\[BRAND]\` |
| 3 | **ShipBob** | On Hand Summary × 4 brand logins (MTB/NFMD/SS/LUMOS) | **4** | Weekly | `reports\shipbob\[BRAND]\` |
| 4 | **Walmart Seller Center** | WFS Inventory × 2 brands (NFMD + SS) | **2** | Weekly | `reports\walmart\[BRAND]\` |
| 5 | **Floship** | Product Inventory export | **1** | Weekly | `reports\floship\` |
| 6 | **Valogix** | Item Location History Forecast | **1** | Weekly | `reports\valogix\` |
| 7 | **Sellerboard** | Sales by product/month × 3 brands (MTB/NFMD/SS) | **3** | Weekly | `reports\sellerboard\[BRAND]\` |
| 8 | **Valogix Exceptions** | History Exception Report (statistical outliers) | **1** | Weekly | `reports\valogix-exceptions\` |
| 9 | **SAP Open POs** | Open Purchase Order report (full export) | **1** | Weekly | `reports\sap-open-pos\` |
| 10 | **In-Transit Log** | Master shipment tracker (manual) | **1** | When updated | `reports\in-transit\` |
| 11 | **SAP Item Master** | ABC Classification / Item Master export | **1** | **As needed** — only when SAP classifications change | `reports\item-master\` |
| ⊕ | **Internal** | SKU Review (carryover from prior week) | 1 | Weekly (folded forward) | `outputs\YYYY-MM-DD\` |

**Two zero-rename principles to keep in mind:**

1. **Brand subfolders** — every per-brand source has a brand subfolder (`MTB/`, `NFMD/`, `SS/`, `LUMOS/`). Drop the file in the right brand folder; **don't rename**.
2. **Column-based auto-classification** — the scripts auto-detect each report by its column headers. The original filename can be `inventory (3).xlsx` for all we care.

After every successful run, raw files are auto-archived to `reports\archive\<source>\YYYY-MM-DD\`.

---

## 🔑 Data sourcing rules — which system is authoritative for which field

This is the canonical answer to "where does each number on the report come from?" Multiple sources can contain overlapping data (e.g., SoStocked also reports FBA stock); **the table below shows which one the pipeline trusts.**

### Amazon-side fields

| Field | Authoritative source | File | Column(s) |
|---|---|---|---|
| **FBA Stock** (Amazon's "On-hand") | **Amazon Seller Central** | FBA Inventory Report + AWD Inventory Report | `available` (FBA Inv.) **plus** `FC Transfer (units)` (AWD Inv.) — **matches SC's "On-hand" panel exactly** |
| **AWD Stock** (sellable AWD units) | **Amazon Seller Central** | AWD Inventory Report | `Available in AWD (units)` |
| **Inbound to AWD** (supplier in transit) | **Amazon Seller Central** | AWD Inventory Report | `Inbound to AWD (units)` |
| **Outbound to FBA** (AWD → FBA in transit) | **Amazon Seller Central** | AWD Inventory Report | `Outbound to FBA (units)` |
| **FBA Inbound Pipeline** (working / shipped / received) | **Amazon Seller Central** | FBA Inventory Report (97-col) | `inbound-working` / `inbound-shipped` / `inbound-received` |
| **Velocity (Adj.)** | **SoStocked** | Inventory export | `Adj. Velocity` |
| **Forecast Velocity** | **SoStocked** | Projected Forecast Model | (computed from weekly forecast cols) |
| **Lead Time** | SoStocked | Inventory export | `Default Lead Time` (fallback 60d) |
| **ShipBob (Emergency)** | **ShipBob** | On Hand Summary export | `Total On Hand` |

**FBA Stock formula clarification:**
Seller Central's "FBA Inventory Details" panel shows On-hand = Available + FC Transfer. The report mirrors this:
- `Available` (sellable right now)
- `+ FC Transfer` (units physically at Amazon FCs being moved between facilities — they count as on-hand because Amazon owns them and they'll be sellable shortly)
- `= FBA Stock` shown on every tab

The report does NOT count: Reserved (allocated to customer orders + FC processing), Unfulfillable (damaged/defective), or Inbound (supplier → FBA in transit — those live in PIPELINE).

**Verification you can do:**
For any priority item, open Seller Central → that item's FBA Inventory Details panel. The "On-hand" total should equal **FBA AVAILABLE + FC TRANSFER** in the report. If they don't match, it's a pipeline bug.

### Stock columns explained

The report breaks Amazon stock into separate columns so you can verify against SC and so the system can classify honestly:

| Column | What it is | Sellable today? | SC equivalent |
|---|---|---|---|
| **FBA AVAILABLE** | Sellable on FBA right now | ✅ Yes | `Available` |
| **FC TRANSFER** | At Amazon, in motion between FCs | ⏳ In days | `FC Transfer` |
| **AWD STOCK** | Sellable AWD inventory | ✅ Yes (via AWD-FBA path) | `Available in AWD (units)` |
| **FBA PIPELINE** | Inbound + outbound to FBA | ⏳ In weeks | `inbound-shipped + inbound-received + outbound-to-FBA` |
| **INBOUND → AWD** | Supplier → AWD in transit | ⏳ Weeks-months | `Inbound to AWD (units)` |
| **SHIPBOB (EMERG)** | Pullable from ShipBob → FBA | ⏳ In days (with send-in) | (separate ShipBob system) |

**For DOS calculation,** the system counts: FBA Available + FC Transfer + AWD + Inbound + FBA Pipeline. FC Transfer counts because units are physically at Amazon and will be sellable shortly.

**For status classification:** TRUE STOCKOUT means literally everything = 0 (need supplier PO). AMAZON STOCKOUT means FBA Available + FC Transfer = 0 but AWD/ShipBob has stock (need send-in).

### Lead time floor: 150 days

The system applies a **150-day floor** to per-item lead times when classifying urgency. SoStocked's per-item `lead_time` is often understated (e.g., 60 days when reality is 150+). The 150-day floor reflects realistic supplier-to-receiving time:

- Production: 30-60 days
- Ocean freight: 30-45 days
- Customs + AWD/FBA receiving: 15-30 days
- **Total: ~150 days door-to-door** (often more with delays)

So an item showing `Lead Time = 60` in the report still gets classified against a 150-day threshold for CRITICAL urgency. Tune via `SUPPLIER_LEAD_TIME_FLOOR` constant in `scripts/build_report.py` if shipping reality changes.

This is why some items with 80+ days of stock may still flag CRITICAL — they won't survive a fresh supplier PO cycle.

### Multi-channel (non-Amazon) fields

| Field | Source |
|---|---|
| Shopify on-hand | **ShipBob** On Hand Summary (overrides Valogix) |
| Walmart SS on-hand / forecast | Valogix |
| Walmart NFMD on-hand / forecast | Walmart Seller Center direct (NFMD is not in Valogix) |
| Floship on-hand / forecast | Valogix |
| 30-day actual sales velocity (non-Amazon) | Valogix monthly history (last fully closed month) |

### Cross-system fields

| Field | Source |
|---|---|
| ABC Classification | SAP Item Master (UPC match — never description) |
| Cost / Unit | Valogix `Inventory Cost` field (only place we get unit cost) |
| Product description (canonical) | SAP Item Master (overrides marketplace-specific titles) |
| In-Transit Log entries (water / truck / air) | Manual In-Transit Log file |

### Why this layout

**SoStocked is for forecasting and velocity, not stock truth.** Their column names have changed multiple times in 2026 (e.g., `FBA Stock / Market or Region` → `FBA Available`, `Total Warehouse Stock` → `3PL: Amazon AWD`). Each rename silently broke our stock numbers until we caught it. Sourcing stock directly from Seller Central means the answer to "what's at FBA right now?" matches what you see when you log into Seller Central — and is immune to SoStocked format changes.

**ShipBob is the operational truth for Shopify and emergency Amazon stock.** Shopify orders ship from ShipBob, so ShipBob On Hand Summary is the real number — Valogix's snapshot of ShipBob stock is a forecast-tool side-view that lags reality.

**Valogix stays in the pipeline** for what it's actually best at: 24 months of sales history per channel, 18 months of forward forecast, and unit cost (the only place we get cost data).

### What a reclassification looks like

After all stock fields are loaded, `build_report.py` runs a **full Amazon reclassification** that uses the Seller Central numbers to recompute DOS and tier (TRUE STOCKOUT / AMAZON STOCKOUT / CRITICAL / HIGH / WATCH / FBA REPLENISHMENT / HEALTHY / INACTIVE / LOW VEL STOCKOUT). This is what catches items that SoStocked might have shown as 0 stock when they actually have hundreds at FBA.

You'll see this line in the log on every run:
```
→ Seller Central stock override: NN FBA · NN AWD · NN DOS recomputed
→ Amazon items reclassified after Seller Central override: NN
    XX× CRITICAL → HEALTHY      ← items SoStocked thought were stocked out
    XX× HEALTHY → INACTIVE      ← velocity dropped
    ...
```

If you ever see a priority item flagged TRUE STOCKOUT but you can confirm in Seller Central that there's stock, **it's a data-pipeline bug, not a real stockout** — flag it and we'll fix the reader.

---

# 1️⃣ SoStocked — 9 files

## SoStocked brand IDs (these end the filename)

| Brand | ID |
|---|---|
| Michael Todd Beauty (MTB) | **5118** |
| NasalFresh MD (NFMD) | **5109** |
| Spa Sciences (SS) | **5119** |

## Per brand, pull all 3 reports

🔑 **No renaming.** The script auto-detects each report by its content (column structure + brand ID embedded in the original SoStocked filename). Keep the file exactly as SoStocked names it — just drop it in the right brand folder.

### Report A — Projected Forecast Model
- **Where:** Forecast section → "Projected Forecast Model" export
- **What SoStocked names it:** `projected-forecast-model-{uuid}-{brand_id}.xlsx` (or `MichaelToddBeautyprojected-forecast-model-...` for MTB — the script handles both)
- **What it gives us:** weekly sales forecasts × markets × ASIN

### Report B — Inventory (Breakdown by Warehouses)
- **Where:** Inventory page → cloud-download icon (top right) → **"Export Inventory with Breakdown by Warehouses"** → Download
- **What SoStocked names it:** `inventory-{uuid}-{brand_id}.csv`
- **What it gives us:** the comprehensive ~50-column export — FBA Available Stock, Adj. Velocity, AWD Available, warehouse-level stock, Inbound to FBA, Lead Time, UPC, Stock Out Days

⚠️ **Verify after download:** the CSV should have ~50 columns and include `Adj. Velocity` and `FBA Available Stock`. If it only has 12-15 columns, you picked the wrong export option ("Export Current View" instead of "Breakdown by Warehouses") — re-pull.

### Report C — Forecasted vs Actual (FvA)
- **Where:** Reports section → "Forecasted vs Actual" or "Forecast Accuracy"
- **What SoStocked names it:** `{uuid}-{brand_id}.xlsx` (no prefix, just UUID + brand ID)
- **Sheet inside:** "Forecasted vs Actual Monthly" — that's how the combiner identifies it
- **What it gives us:** forecast accuracy per ASIN per month (script flags items off by 30%+)

## Where to drop them — and what runs

Drop the 9 files (as-named) into the brand subfolders:

```
reports\sostocked\MTB\     reports\sostocked\NFMD\     reports\sostocked\SS\
```

(The combiner also reads from `Downloads\` as a fallback if you want to skip the brand-folder step — but brand folders keep things organized and visually confirm you got all 3 reports per brand.)

Then run:

```
python scripts\combine_forecast.py
```

The script:
1. Auto-detects all 9 files by filename pattern + brand ID
2. Renames internally and combines into one `reports\weekly\Weekly_Forecast_YYYY-MM-DD.xlsx` (8 sheets)
3. Auto-archives the 9 raw files to `reports\archive\sostocked\YYYY-MM-DD\`

---

# 2️⃣ Amazon Seller Central — 6 files (2 reports × 3 brands)

## The 2 reports — pulled separately for each brand login

### Report A — AWD Inventory Report
- **Path:** `Inventory → AWD → Replenishment / Auto-Replenishment Dashboard` → Download as CSV
- **Key columns we use:** `ASIN`, `Inbound to AWD (units)`, `Outbound to FBA (units)`
- **Why:** the only direct supplier-to-AWD in-transit signal we have at ASIN level. Feeds the DOS calculation.

### Report B — FBA Inventory Report (full, 97 columns)
- **Path:** `Reports → Fulfillment → FBA Inventory` → Request → Download as CSV
- **Key columns we use:** `afn-inbound-shipped-quantity`, `afn-inbound-receiving-quantity`, `afn-inbound-working-quantity`, plus aging buckets
- **Why:** comprehensive FBA picture — what's sellable, what's inbound, what's at the FC pending. Newer Amazon UIs use the `afn-` prefix; the loader handles both old and new column names.

⚠️ **Don't pull "Manage FBA Inventory" from the Inventory tab** — that's the abbreviated 30-column version. The Reports → Fulfillment → FBA Inventory path gives you the full 97-column file.

ℹ️ **Inbound Shipment Items** (per-shipment detail) is OPTIONAL. If you find the right path, drop CSVs as `fba-shipments-*.csv` into the brand folder and the Shipment Tracking report's FBA tab populates. Otherwise that tab is skipped.

## Where to drop them

```
reports\seller-central\MTB\     reports\seller-central\NFMD\     reports\seller-central\SS\
```

**No renaming.** The script in `build_report.py` auto-classifies each CSV by its column structure (AWD vs FBA vs Inbound Shipment Items).

📚 Detailed per-brand walkthrough: [[06 Processes & SOPs/(C) Amazon Seller Central — Reports Pull List]]

---

# 3️⃣ ShipBob — 4 files (1 report × 4 brand logins)

ShipBob requires a separate login per brand. There's no master account.

| Brand login | Maps to |
|---|---|
| **MTB** | Michael Todd Beauty — Shopify MTB (Valogix `SBGA-MT`) |
| **NFMD** | NasalFresh MD — DTC + part of Valogix `SBGA-SS-NFMD` |
| **SS** | Spa Sciences — DTC + part of Valogix `SBGA-SS` |
| **LUMOS** | Lumos product line — separate ShipBob account |

## How to pull (per login)

1. Sign into shipbob.com for the brand
2. Inventory → Export → **On Hand Summary**
3. ShipBob emails a download link — must be logged into the **correct brand** when clicking the link

## Where to drop them

```
reports\shipbob\MTB\     reports\shipbob\NFMD\     reports\shipbob\SS\     reports\shipbob\LUMOS\
```

**No renaming.** The original ShipBob filename is fine.

**Why we pull this:**
- Validates Valogix's ShipBob inventory data (independent source of truth)
- Drives Shopify fulfillment readiness checks (Shopify orders ship from ShipBob)
- Sanity-checks Amazon emergency send-in plans (what's actually pullable)

📚 Detailed per-brand walkthrough: [[06 Processes & SOPs/(C) ShipBob — Reports Pull List]]

---

# 4️⃣ Walmart Seller Center — 2 files (NFMD + SS)

Only NFMD and SS have Walmart presence. MTB does not.

## How to pull (per brand login)

1. Sign into Walmart Seller Center for the brand
2. Left menu → **WFS** → **Inventory**
3. Right side → **Download** → **All items** → **Download**
4. File downloads as `.xlsx` (Excel format — not CSV)

## Where to drop them

```
reports\walmart\NFMD\     reports\walmart\SS\
```

**No renaming.**

**Why we pull this:**
- Valogix only carries Walmart-SS data. **NFMD on Walmart is invisible to Valogix** — the direct WM-NFMD pull fills that gap as a separate marketplace ("Walmart NFMD") in the Multi-Channel dashboard.
- Validates Walmart-SS data against Valogix.

📚 Detailed walkthrough: [[06 Processes & SOPs/(C) Walmart Seller Center — Reports Pull List]]

---

# 5️⃣ Floship — 1 file

International fulfillment center for MTB only.

## How to pull

1. Sign into Floship
2. Inventory → Product Inventory → Export

## Where to drop it

```
reports\floship\
```

**No renaming.** Used to validate Valogix `FLO-MTB` location data.

---

# 6️⃣ Valogix — 1 file (the multi-channel backbone)

Valogix is the source of truth for **non-Amazon channels** — Shopify MTB, Spa Sciences DTC (SS + NFMD mixed), Walmart-SS, Floship Intl. Plus:
- **Cost per UPC** (the only place we get unit cost — drives PO $ values across all marketplaces)
- **24 months of sales history** (used for the 90-day velocity calc)
- **18 months of forward forecast** (drives the monthly forecast columns Apr-Dec)

## How to pull

1. Log into Valogix
2. Reports → **Item Location History Forecast** → all items, all locations
3. Export as CSV

## Where to drop it

```
reports\valogix\
```

**Don't rename** — keep `schain_itemLocationHistoryForecast_YYYY_MM_DD.csv`. The pipeline auto-archives older Valogix CSVs to `reports\archive\valogix\YYYY-MM-DD\`.

## Location codes the pipeline reads

| Valogix Location | Display name | Brand |
|---|---|---|
| `SBGA-MT` | Shopify MTB | MTB |
| `FLO-MTB` | Floship Intl | MTB |
| `SBGA-SS` | Spa Sciences DTC SS | SS |
| `SBGA-SS-NFMD` *(synthetic)* | Spa Sciences DTC NFMD | NFMD |
| `WM-SS` | Walmart SS | SS |
| `WM-NFMD` *(direct, not Valogix)* | Walmart NFMD | NFMD |

⚠️ **`SBGA-SS` is mixed.** Valogix lumps SS and NFMD products in this single location. The loader auto-detects NFMD products (description contains "NasalFresh" / "Nasal Rinse") and remaps them to a synthetic `SBGA-SS-NFMD` location so they show up as their own marketplace row.

⚠️ **`WM-NFMD` is not in Valogix.** Walmart NFMD comes from the direct Walmart Seller Center pull (Section 4) — not from Valogix.

---

# 7️⃣ Sellerboard — 3 files (1 report × 3 brand logins)

Sellerboard is the source for **Amazon sales actuals** with 28-month historical depth — the cleanest monthly history we have for the Amazon channel. Drives the 📊 Amazon Sales History tab and the Phase 3 Demand Volatility scoring.

## How to pull (per brand login)

1. Sign into [sellerboard.com](https://sellerboard.com) for the brand
2. Reports → **Sales by product/month**
3. Set the date range to the **maximum available** (28 months back → today)
4. Export as `.xlsx`

⚠️ **Make sure the date range goes back at least 24 months** — short ranges (1-3 months) will show up as "INSUFFICIENT" volatility on the report. If only 1 month exports, you picked the wrong date range — re-pull.

## Where to drop them

```
reports\sellerboard\MTB\     reports\sellerboard\NFMD\     reports\sellerboard\SS\
```

**No renaming.** The loader picks the file with the widest date range automatically.

## What the pipeline uses it for

- **📊 Amazon Sales History tab** — last 12 months of actuals + TTM Qty + YoY % per ASIN
- **📈 Forecast Pivot tab** — Amazon side of the actuals heatmap (last 12 closed months)
- **Demand Volatility scoring** — coefficient of variation over last 12 months → STABLE / MODERATE / VOLATILE bucket on every Amazon row

---

# 8️⃣ Valogix Exception Report — 1 file

Statistical-outlier flagger. Valogix detects months where actual sales fell outside expected statistical bounds (3-sigma) — useful for catching bad-data months automatically (the Soniclear White Marble Jul/Aug 2/0 pattern).

## How to pull

1. Log into Valogix
2. Reports → **History Exception Report**
3. Export as CSV

## Where to drop it

```
reports\valogix-exceptions\
```

**Don't rename.** Standard filename is `schain_itemLocationHistoryException_YYYY_MM_DD.csv`.

## What the pipeline uses it for

- **📊 Sales Anomalies tab** — 20-ish flagged items per week sorted by severity, with direction flags (🔻 UNDER / 🔺 OVER)
- Quick scan target: items here often need a manual override before they trigger wrong replenishment decisions

---

# 9️⃣ SAP Open Purchase Orders — 1 file

Live view of every open PO in SAP — drives the **PO ETA** column on every per-marketplace tab + the dedicated **📋 SAP Open POs** tab.

## How to pull

1. SAP → **Open Purchase Order Report** (full export, no filtering)
2. File downloads as `SAP_Openpurchaseorderreport.xlsx`

## Where to drop it

```
reports\sap-open-pos\
```

**No renaming.** The loader picks the most-recently-modified `.xlsx` in the folder.

## Filter rules applied by the pipeline

The report contains 5,000+ historical rows. The loader filters to active open POs using these rules:

1. **Document Status ≠ C** — closed POs excluded
2. **Posting Date ≥ 2026-01-01** — older POs excluded
3. **Item No. = 12-digit UPC** — blank or non-numeric item numbers excluded
4. **Remaining Open Quantity > 0** — fully-received POs excluded

After filters, ~150 active POs remain.

## Field mapping

- **PO ETA** = `Original Due Date`
- **Open Qty** = `Remaining Open Quantity`
- **Channel routing** by `Warehouse Code`:
  - `AMZN-MT`, `AMZN-SS` → Amazon US
  - `SBGA-MT`, `SBGA-SS` → Shopify
  - `FLO-MTB`, `AMZ-MT*`, `AMZ-NF*` → Floship Intl

## ⚠ Same-day flag

Any PO where `Original Due Date == Posting Date` is flagged with ⚠ on both the per-marketplace tabs (PO ETA cell highlighted amber) and the dedicated 📋 SAP Open POs tab ("⚠ FIX SAP" badge in the rightmost column). These are SAP data-quality issues — the due date wasn't filled in correctly and needs to be updated in SAP.

**Action:** review the flagged rows on the 📋 SAP Open POs tab each week and update the due dates in SAP so the PO ETA column shows real expected arrival dates.

---

# 🔟 In-Transit Log — 1 file (when updated)

Manually-maintained Excel tracking every container, truck, and air shipment in flight.

## How to pull

1. Get latest version from team (SharePoint or whoever owns it)
2. Rename to `IN_TRANSIT_LOG_YYYY-MM-DD.xlsx`
3. Drop into `reports\in-transit\`

If nobody updated it this week, you can skip — the Shipment Tracking script falls back to whichever file is newest.

## Three sheets the script reads

`WATER` (sea freight) · `TRUCK` · `AIR`

Per shipment: PO #, Vendor, Container/Tracking #, Forwarder, Date Sailed/Pickup, ETA, Receiving Warehouse, Quantity, Commercial Invoice $, items/UPCs.

---

# 1️⃣1️⃣ SAP Item Master — 1 file (**as needed**, not on a schedule)

Canonical source of truth for **ABC classifications**, **descriptions**, and brand assignments. **Match key is UPC** (Item No.) — never description, since multiple SKUs can share the same description across product variants.

## When to refresh

**Only when classifications actually change in SAP.** No fixed schedule. The current `item_master.xlsx` is the working truth source — leave it alone until SAP changes are made and need to flow through. Triggers for a refresh:

- Tommy or the team reclassifies a SKU in SAP (e.g., A → S, E → Z)
- A new SKU is added to SAP
- ABC codes get cleaned up in batch

When that happens, follow the steps below. Otherwise, the file is stable.

## How to pull

1. SAP admin runs the **ABC Classification** export (default name: `SAPABCCLASSIFICATION.xlsx`)
   - Required columns: `Item No.` · `Item Description` · `ItemBranch` · `ABC Classification`
   - All-items export (do NOT filter to active only — the pipeline needs Z/F/I codes too)
2. File downloads to `Downloads\`
3. Rename to `item_master.xlsx`
4. **Replace** the existing file at `reports\item-master\item_master.xlsx`
5. Old version auto-renamed to `item_master_old_YYYY-MM-DD.xlsx` (audit trail kept)

## How the pipeline uses it

- Match key: **UPC** (the `Item No.` column) — never description
- Loads ~1,384 ABC codes + ~1,386 descriptions on every run
- Overrides marketplace-specific listing titles with SAP descriptions (one canonical name per UPC across all reports)
- Routes items to tabs based on ABC code:
  - **A / B / C / D** — main views (Weekly Summary, Inventory Overview, Priority Actions)
  - **E** — main views, but eligible for Phase-Out Review tab if 0 stock + 0 velocity
  - **F / I / S / Z** — automatically routed to `📦 Sales BOMs & Other` tab, removed from main views

## Mid-cycle SAP changes

If a single UPC's classification changes between weekly exports and you can't re-export immediately, add to `ABC_OVERRIDE` dict in `scripts/build_report.py`:

```python
ABC_OVERRIDE = {
    "850012345678": "S Sales BOM",   # Custom override until next SAP export
}
```

Override format: `"<UPC>": "<full ABC string with description>"`. Wipe these out on the next full SAP re-export — SAP becomes the truth source again.

## ABC code reference

| Code | Meaning | Routing |
|---|---|---|
| **A** | High Vol | Main views |
| **B** | Med Vol | Main views |
| **C** | Low Vol | Main views |
| **D** | Phase-In | Main views |
| **E** | Phase-Out | Main views (Phase-Out Review eligible) |
| **F** | Other | Sales BOMs & Other tab |
| **I** | Ind. Comp. (Industrial Component) | Sales BOMs & Other tab |
| **S** | Sales BOM (combo packs, gift sets) | Sales BOMs & Other tab |
| **Z** | Obsolete | Sales BOMs & Other tab |

Full reference: [[06 Processes & SOPs/(C) ABC Classification Reference]]

---

# ⊕ SKU Review — carryover from prior week

After each weekly run, `outputs\YYYY-MM-DD\sku-review-YYYY-MM-DD.xlsx` is generated for the priority items. You fill in:

| Col | Field | Values |
|---|---|---|
| M | Active? | `Y` / `N` (N = drop from all reports) |
| N | Replenish From | `SB <item#>` / `Manufacturer` / `Phase Out` / free text |
| O | Notes | free text |

**Folding the decisions forward into the next week:**
1. Save the prior week's filled-out file as `sku-review-YYYY-MM-DD.xlsx` for the new week
2. Drop into `outputs\YYYY-MM-DD\` (the new week's folder)
3. `demand_planning.py` picks it up automatically — phased-out items disappear, replenish notes flow into the action plan

If today's `sku-review-*.xlsx` doesn't exist, `build_action_plan.py` falls back to the most recent one (carryover-friendly).

---

# 🗂 Final folder layout (after all inputs are dropped)

```
C:\Users\[YourName]\MTB-SupplyChain\
├── reports\
│   ├── sostocked\
│   │   ├── MTB\         ← (or land in Downloads\ — combine_forecast.py reads both)
│   │   ├── NFMD\
│   │   └── SS\
│   ├── seller-central\
│   │   ├── MTB\         ← awd-*.csv + fba inventory.csv (any names)
│   │   ├── NFMD\
│   │   └── SS\
│   ├── shipbob\
│   │   ├── MTB\         ← On Hand Summary (any name)
│   │   ├── NFMD\
│   │   ├── SS\
│   │   └── LUMOS\
│   ├── walmart\
│   │   ├── NFMD\        ← inventory.xlsx
│   │   └── SS\
│   ├── floship\         ← Product Inventory export
│   ├── valogix\         ← schain_itemLocationHistoryForecast_*.csv
│   ├── valogix-exceptions\ ← schain_itemLocationHistoryException_*.csv
│   ├── sellerboard\
│   │   ├── MTB\         ← Sales by product/month .xlsx (any name)
│   │   ├── NFMD\
│   │   └── SS\
│   ├── sap-open-pos\    ← SAP_Openpurchaseorderreport.xlsx
│   ├── in-transit\      ← IN_TRANSIT_LOG_YYYY-MM-DD.xlsx
│   ├── item-master\
│   │   └── item_master.xlsx
│   ├── weekly\          ← (auto-generated by combine_forecast.py)
│   └── archive\         ← (auto-archive of prior raw files)
│       ├── sostocked\YYYY-MM-DD\
│       ├── valogix\YYYY-MM-DD\
│       └── ...
└── outputs\
    └── YYYY-MM-DD\
        ├── sku-review-YYYY-MM-DD.xlsx     ← (carryover, filled in by you)
        ├── demand-plan-YYYY-MM-DD.{xlsx,json,md}
        ├── weekly-report-YYYY-MM-DD.xlsx
        ├── action-plan-YYYY-MM-DD.xlsx
        └── shipment-tracking-YYYY-MM-DD.xlsx
```

---

# ✅ Pre-run checklist (28 weekly inputs)

- [ ] **9 SoStocked files** (3 brands × 3 reports — Forecast + Inventory + FvA) — in `Downloads\` or `reports\sostocked\[BRAND]\`
- [ ] **6 Amazon Seller Central files** (3 brands × 2 reports — AWD + FBA Inventory) — in `reports\seller-central\[BRAND]\`
- [ ] **4 ShipBob files** (4 brand logins — On Hand Summary) — in `reports\shipbob\[BRAND]\`
- [ ] **2 Walmart files** (NFMD + SS — WFS Inventory .xlsx) — in `reports\walmart\[BRAND]\`
- [ ] **1 Floship file** (Product Inventory export) — in `reports\floship\`
- [ ] **1 Valogix file** (Item Location History Forecast) — in `reports\valogix\`
- [ ] **3 Sellerboard files** (3 brand logins — Sales by product/month, max date range) — in `reports\sellerboard\[BRAND]\`
- [ ] **1 Valogix Exception Report** (History Exception export) — in `reports\valogix-exceptions\`
- [ ] **1 SAP Open PO report** (full export, no filtering) — in `reports\sap-open-pos\`
- [ ] **1 In-Transit Log** (latest) — in `reports\in-transit\` *(skip if not updated)*
- [ ] **`item_master.xlsx`** present in `reports\item-master\` *(no weekly refresh — only re-pull `SAPABCCLASSIFICATION.xlsx` when SAP classifications change)*
- [ ] **Carryover sku-review** in this week's `outputs\YYYY-MM-DD\` folder *(if you have decisions to fold in)*

When all checked → follow [[06 Processes & SOPs/(C) Weekly Analysis SOP — Step by Step]].

---

# 🔗 Per-source detail docs

- [[06 Processes & SOPs/(C) Amazon Seller Central — Reports Pull List]]
- [[06 Processes & SOPs/(C) ShipBob — Reports Pull List]]
- [[06 Processes & SOPs/(C) Walmart Seller Center — Reports Pull List]]

# 🔗 Companion SOPs

- [[06 Processes & SOPs/(C) Weekly Analysis SOP — Step by Step]] — the operational run-the-scripts playbook
- [[06 Processes & SOPs/(C) Weekly Analysis Cheat Sheet — 1 Page]] — print-and-stick version
- [[06 Processes & SOPs/(C) ABC Classification Reference]] — the 6 ABC codes
- [[06 Processes & SOPs/(C) Daily Morning Routine — SCM]] — daily routine
- [[15 Meetings & Decisions/(C) Weekly Run Log — 2026-05-01]] — current week's live runbook

---

*Rewritten: May 4, 2026 · Updated: May 6, 2026 (added Sellerboard · Valogix Exceptions · SAP Open POs) · Owner: Supply Chain*
