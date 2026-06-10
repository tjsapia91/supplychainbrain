# (C) Weekly Inputs Sourcing SOP — Where Every Report Comes From

> Canonical reference cataloging every input the weekly pipeline consumes. Tells you which dashboard, which menu, which export, where it lands, and how the script finds it.
>
> **Last updated:** May 21, 2026 (added Sellerboard CA Dashboard Products for per-marketplace CA velocity + forecast; documented US+CA Monthly combining caveat; CA Seller Central FBA file now extracts Reserved FC Transfer; PO data no longer attributed to CA market rows; lead time floor 120→145; Amazon SKU mapping file added; corrected Amazon Seller Central count to 9 files — CA has FBA only, no AWD)
> **This is the master Weekly Analysis SOP** — covers inputs, sourcing rules, system map, and run steps in one place.
> **Companion doc:** [[06 Processes & SOPs/(C) Weekly Analysis Cheat Sheet — 1 Page]] (print-and-stick quick reference)

---

## 📋 At a glance — 12 source systems, 34 weekly files (+2 occasional)

| # | Source | What | Files | Frequency | Drop into |
|---|---|---|---|---|---|
| 1 | **SoStocked** | 3 reports × 3 brands (Forecast + Inventory + FvA) | **9** | Weekly | `Downloads\` (auto-detected & moved) |
| 2 | **Amazon Seller Central** | US: AWD + FBA × 3 brands (6 files) · CA: FBA only × 3 brands (3 files — MTB doesn't have AWD CA) | **9** | Weekly | `reports\seller-central\[MARKET]\[BRAND]\` |
| 3 | **ShipBob** | On Hand Summary × 4 brand logins (MTB/NFMD/SS/LUMOS) | **4** | Weekly | `reports\shipbob\[BRAND]\` |
| 4 | **Walmart Seller Center** | WFS Inventory × 2 brands (NFMD + SS) | **2** | Weekly | `reports\walmart\[BRAND]\` |
| 5 | **Floship** | Product Inventory export | **1** | Weekly | `reports\floship\` |
| 6 | **Valogix** | Item Location History Forecast | **1** | Weekly | `reports\valogix\` |
| 7 | **Sellerboard — Sales by Product/Month** *(US+CA combined)* | × 3 brands (MTB/NFMD/SS) | **3** | Weekly | `reports\sellerboard\[BRAND]\` |
| 8 | **🆕 Sellerboard CA — Dashboard Products** *(CA-only, per-marketplace)* | × 3 brands (MTB/NFMD/SS) | **3** | Weekly *(or quarterly)* | `reports\sellerboard\[BRAND]\canada\` |
| 9 | **Valogix Exceptions** | History Exception Report (statistical outliers) | **1** | Weekly | `reports\valogix-exceptions\` |
| 10 | **SAP Open POs** | Open Purchase Order report (full export) | **1** | Weekly | `reports\sap-open-pos\` |
| 11 | **SAP Inventory in Warehouse** | Per-warehouse inventory snapshot — feeds 🔄 SAP↔SB Rebalance | **1** | Weekly | `reports\_data\sap-inventory\` |
| 12 | **SAP Inventory Transfer Requests** | Pending approved inter-warehouse moves | **1** | Weekly | `reports\_data\sap-transfer-requests\` |
| 13 | **In-Transit Log** | Master shipment tracker (manual) | **1** | When updated | `reports\in-transit\` |
| 14 | **SAP Item Master** | ABC Classification / Item Master export | **1** | **As needed** — only when SAP classifications change | `reports\item-master\` |
| ⊕ | **Amazon SKU Mapping** | Amazon listing SKU ↔ SAP UPC mapping | 1 | **As needed** — when new SKUs launch on Amazon | `reports\item-master\amazon-sku-mapping.xlsx` |
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
| **FBA Stock (US)** | **Amazon Seller Central US** | FBA Inventory Report + AWD Inventory Report | `available` (FBA) + `FC Transfer (units)` (AWD) — matches SC US "On-hand" panel |
| **FBA Stock (CA)** | **Amazon Seller Central CA** | FBA Inventory Report only | `available` (FBA) + `Reserved FC Transfer` (FBA, same file) — Amazon CA has no AWD |
| **AWD Stock (US only)** | **Amazon Seller Central US** | AWD Inventory Report | `Available in AWD (units)` (CA Amazon doesn't have AWD) |
| **Inbound to AWD** (supplier in transit) | **Amazon Seller Central US** | AWD Inventory Report | `Inbound to AWD (units)` |
| **Outbound to FBA** (AWD → FBA in transit) | **Amazon Seller Central US** | AWD Inventory Report | `Outbound to FBA (units)` |
| **FBA Inbound Pipeline** (working / shipped / received) | **Amazon Seller Central** | FBA Inventory Report (97-col) | `inbound-working` / `inbound-shipped` / `inbound-received` |
| **Velocity — US Amazon** | **Sellerboard Monthly** (90-day) | Sales by product/month (last 3 closed months) | `Quantity` summed ÷ days |
| **Velocity — CA Amazon** | **Sellerboard CA Dashboard** OR **SoStocked CA Adj. Vel** (fallback) | Dashboard Products (marketplace=amazon.ca) OR SoStocked Inventory | `Units` ÷ days_in_range |
| **Forecast — US Amazon** | SoStocked PFM + Sellerboard seasonality blend (by ABC class) | Projected Forecast Model + Sellerboard Monthly | per-month forecast |
| **Forecast — CA Amazon** | Sellerboard CA Dashboard quarterly seasonality | Dashboard Products (multiple quarterly files) | `CA_avg × Q_factor × days_in_month` |
| **Lead Time** | SoStocked | Inventory export | `Default Lead Time` (fallback 60d, floored at 145d for supplier ocean POs) |
| **ShipBob (Emergency)** | **ShipBob** | On Hand Summary export | `Total On Hand` |
| **SAP Open POs** | **SAP** | Open Purchase Order Report | applied ONLY to US Amazon rows — CA fulfillment doesn't share AMZN-MT/SS POs |

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

### Lead time floor: 145 days

The system applies a **145-day floor** to per-item lead times when classifying urgency. SoStocked's per-item `lead_time` is often understated (e.g., 60 days when reality is 150+). The 145-day floor reflects realistic supplier-to-receiving time:

- Production: 30-60 days
- Ocean freight: 30-45 days
- Customs + AWD/FBA receiving: 15-30 days
- **Total: ~145 days door-to-door** (often more with delays)

So an item showing `Lead Time = 60` in the report still gets classified against a 145-day threshold for CRITICAL urgency. Tune via `SUPPLIER_LEAD_TIME_FLOOR` constant in `scripts/build_report.py` if shipping reality changes.

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

### Report C — Forecasted vs Actual (FvA) — **monthly accumulation**
- **Where:** Reports section → "Forecasted vs Actual" or "Forecast Accuracy"
- **What SoStocked names it:** `{uuid}-{brand_id}.xlsx` (no prefix, just UUID + brand ID)
- **Sheet inside:** "Forecasted vs Actual Monthly" — that's how the combiner identifies it
- **What it gives us:** forecast accuracy per ASIN for the selected month (script flags items off by 30%+)

⚠ **Each FvA export covers ONE month at a time.** SoStocked doesn't give a multi-month aggregate via this report.

### How to build historical FvA — the accumulation workflow (per Tommy 2026-05-21)

To get a multi-month view of forecast accuracy (useful for trend analysis), you accumulate month-by-month exports:

**Step 1 — Initial backfill (one-time, ~30 minutes)**
- Per brand, export FvA for each closed month going back as far as you want:
  - Jan 2026
  - Feb 2026
  - Mar 2026
  - Apr 2026
  - May 2026 (MTD — partial, will be replaced)
- = **15 files total** (5 months × 3 brands)

**Step 2 — Weekly going forward**
- Pull only the **current month** FvA per brand (3 files weekly)
- As each month closes, that file becomes the final record for that month
- Next month, you pull the new current month — closed months stay untouched

**Step 3 — Where to drop them**
- All FvA files (backfill + weekly) go in: `reports\sostocked\[BRAND]\fva-history\`
- **One file per (brand × month)** — don't overwrite; let them accumulate
- Suggested filename convention (so months are visually distinguishable): rename to `FvA_[BRAND]_YYYY-MM.xlsx` after download (e.g., `FvA_MTB_2026-01.xlsx`)
- Pipeline picks up the most recent file per brand for the "Forecast Accuracy" sheet in the Weekly Forecast workbook

⚠ **Pipeline aggregation deferred (decision: 2026-05-21)**: `combine_forecast.py` reads ONE FvA file per brand at a time — the latest one. Multi-month aggregation across the `fva-history/` folder is **intentionally deferred** until we evaluate whether it actually drives a decision.

**Rationale**: per-month forecast accuracy could be a vanity metric — it doesn't directly change a PO call (the urgency tier already factors recent actuals). Better to accumulate the files for a few months, see if any pattern emerges that we'd actually act on, then build the aggregator if yes.

Until then, the backfill files give you a historical record on disk that you can analyze manually (open them in Excel, build a pivot). If a trend emerges you want to surface weekly, ping Claudian and we'll wire up the multi-month aggregation in ~30 min.

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

# 2️⃣ Amazon Seller Central — 9 files (US: 2 reports × 3 brands + CA: 1 report × 3 brands)

## The 2 reports

### Report A — AWD Inventory Report (US ONLY — Amazon CA does not offer AWD for MTB)
- **Path:** `Inventory → AWD → Replenishment / Auto-Replenishment Dashboard` → Download as CSV
- **Key columns we use:** `ASIN`, `Inbound to AWD (units)`, `Outbound to FBA (units)`, `Available in AWD (units)`, `FC Transfer (units)`
- **Why:** the only direct supplier-to-AWD in-transit signal we have at ASIN level. Feeds the DOS calculation.
- **Marketplace coverage:** US only. **Amazon CA has no AWD program** for MTB — skip this report on the Canadian dashboard. *(If/when CA AWD becomes available, drop the file in `reports\seller-central\CA\[BRAND]\` and the pipeline will auto-pick it up.)*

### Report B — FBA Inventory Report (full, 97 columns) — pull for **BOTH US and CA**
- **Path:** `Reports → Fulfillment → FBA Inventory` → Request → Download as CSV
- **Key columns we use:**
  - `afn-inbound-shipped-quantity`, `afn-inbound-receiving-quantity`, `afn-inbound-working-quantity` (or 97-col aliases)
  - `available` — sellable on FBA right now
  - **`Reserved FC Transfer`** — units moving between FBA FCs (Amazon CA's FC Transfer comes from THIS column, since CA has no AWD report)
  - Plus aging buckets, sales velocity figures
- **Why:** comprehensive FBA picture — what's sellable, what's inbound, what's at the FC pending. Newer Amazon UIs use the `afn-` prefix; the loader handles both old and new column names.

⚠️ **Don't pull "Manage FBA Inventory" from the Inventory tab** — that's the abbreviated 30-column version. The `Reports → Fulfillment → FBA Inventory` path gives you the full 97-column file.

ℹ️ **Inbound Shipment Items** (per-shipment detail) is OPTIONAL. If you find the right path, drop CSVs as `fba-shipments-*.csv` into the brand folder and the Shipment Tracking report's FBA tab populates. Otherwise that tab is skipped.

## What to pull per marketplace

| Marketplace | Login | Reports to pull | Files | Drop into |
|---|---|---|---|---|
| **US** (`sellercentral.amazon.com`) | US dashboard | AWD Inventory + FBA Inventory × 3 brands | **6** | `reports\seller-central\US\[BRAND]\` |
| **CA** (`sellercentral.amazon.ca`) | CA dashboard | **FBA Inventory ONLY** × 3 brands (no AWD CA for MTB) | **3** | `reports\seller-central\CA\[BRAND]\` |

**Total weekly: 9 Amazon Seller Central files** (was 12 before — the AWD CA pulls were assumed but MTB isn't enrolled in AWD CA).

```
reports\seller-central\
├── US\
│   ├── MTB\     ← 2 files: AWD Inv CSV + FBA Inv CSV
│   ├── NFMD\    ← 2 files
│   └── SS\      ← 2 files
└── CA\
    ├── MTB\     ← 1 file: FBA Inv CSV (no AWD CA)
    ├── NFMD\    ← 1 file
    └── SS\      ← 1 file
```

**No renaming.** The script in `build_report.py` auto-classifies each CSV by column structure (AWD vs FBA) and tags the data with the marketplace based on which folder it's in (US or CA). The loader keys ASIN data by `(ASIN, marketplace)` so US and CA stock for the same ASIN stay separate.

**For CA's FC Transfer**: since there's no CA AWD report, the pipeline reads `Reserved FC Transfer` from the CA FBA file instead. So CA TOTAL AT AMZN = `available + Reserved FC Transfer` (matches Seller Central CA's "On-hand" panel). *(This handling was added 2026-05-21 — verified with SKU 850038082383: 1,919 available + 135 FC Transfer = 2,054 total.)*


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

**Use the NEW format export only — don't pull On Hand Summary anymore.**

1. Sign into shipbob.com for the brand
2. `Inventory → Inventory Status → Export → Export All Data`
3. Filename ShipBob generates: `inventory-export-blob_{tenant}_{timestamp}.csv`
4. ShipBob emails a download link — must be logged into the **correct brand** when clicking the link

> ℹ️ The LEGACY `On Hand Summary` export still works as a fallback if ShipBob ever changes the path, but you don't need to pull it routinely. The NEW format is strictly more accurate (`Sellable` excludes Committed/Exception/Backordered; `Total On Hand` on the old report overstates).

## Two ShipBob export formats — pipeline auto-detects which one

### 🆕 NEW format — `inventory-export-blob_*.csv` (preferred)

Lot-level normalized export. **14 columns**, multiple rows per SKU (one per FC × lot):

| Column | What it shows |
|---|---|
| SKU | UPC / item number |
| Inventory ID | ShipBob internal ID |
| Inventory Name | Product name |
| Lot Number | Lot # (or `-` if no lots) |
| Expiration Date | Lot expiry (or `-`) |
| Incoming | Units in transit to ShipBob |
| On Hand | Total physical inventory at this FC × lot |
| Committed | Already allocated to open orders |
| Fulfillable | On Hand − Committed (ready to ship now) |
| Exception | Damaged / quarantined |
| **Sellable** ⭐ | **Free-to-ship — what the pipeline uses for `on_hand`** |
| Backordered | Customer orders waiting on stock |
| Internal Transfer | Moving between ShipBob FCs |
| Fulfillment Center | FC location (e.g., "Reno (NV)", "Buford (GA)") |

**Detection signature**: pipeline flags as NEW if BOTH `Sellable` AND `Fulfillment Center` columns are present.

### 🗄 LEGACY format — `On Hand Summary` (fallback)

Pivoted single-row-per-SKU view with `Total On Hand` column. Pipeline accepts it but uses Total On Hand directly (overstates true free-to-ship since it includes Committed/Exception units).

### Why NEW is better

| Aspect | LEGACY | NEW |
|---|---|---|
| Stock accuracy | `Total On Hand` includes Committed (overstates) | `Sellable` excludes Committed/Exception/Backordered |
| Lot visibility | None | Lot # + Expiration per FC |
| FC breakdown | Total only | Per-FC rows |
| FIFO planning ready | No | Yes (lot-level data preserved in the report) |

## Where to drop them

```
reports\shipbob\MTB\     reports\shipbob\NFMD\     reports\shipbob\SS\     reports\shipbob\LUMOS\
```

**No renaming.** The original ShipBob filename (e.g., `inventory-export-blob_385579_639150688574617481.csv`) is fine — pipeline reads by columns, not filename.

## Pipeline log to confirm NEW format

After running `build_report.py`, you'll see one of these per brand:
```
→ ShipBob MTB (NEW format): inventory-export-blob_385579_*.csv
→ ShipBob NFMD (NEW format): inventory-export-blob_385954_*.csv
→ ShipBob SS (NEW format): inventory-export-blob_385953_*.csv
→ ShipBob LUMOS (NEW format): inventory-export-blob_396348_*.csv
→ ShipBob: NN SKUs across 4 brand files (4 new-fmt) · XXX,XXX sellable units
```

If you see `(LEGACY)` instead of `(NEW format)`, you're still pulling the old export — switch to the new lot-level export path for better accuracy.

**Why we pull this:**
- Validates Valogix's ShipBob inventory data (independent source of truth)
- Drives Shopify fulfillment readiness checks (Shopify orders ship from ShipBob)
- Sanity-checks Amazon emergency send-in plans (what's actually pullable)
- Per-FC + per-lot detail enables future FIFO-aware allocation planning


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

# 7️⃣ Sellerboard — 6 files total: 3 Monthly (US+CA combined) + 3 CA Dashboard (per-marketplace)

Sellerboard is the source for **Amazon sales actuals** with 28-month historical depth — the cleanest monthly history we have for the Amazon channel. Drives the 📊 Amazon Sales History tab, the Phase 3 Demand Volatility scoring, and now the CA-specific velocity + forecast.

## ⚠ Critical caveat — Sellerboard report types behave differently

| Report type | Marketplace filter | Excludes any SKUs? | Used for |
|---|---|---|---|
| **Sales by Product/Month** | ❌ IGNORED — always shows US+CA combined | ✓ Includes all SKUs | US Amazon velocity + monthly history |
| **Dashboard Products** | ✓ RESPECTS marketplace filter | ⚠ Excludes ASINs with non-numeric SKUs (MTBLavendar, *-M, *-AMZ, *-FBA etc.) | CA-only velocity + CA quarterly seasonality |

This matters because:
- **Sales by Product/Month** is comprehensive (every SKU) but combines US+CA — so it slightly over-counts US (~2%, acceptable) and would dramatically over-count CA (~50×) if applied to CA rows. **Used for US Amazon ONLY.**
- **Dashboard Products** filters to true CA-only when marketplace = `amazon.ca` is selected. **Used for CA Amazon.**

The pipeline routes these correctly per the **F1 fix** (2026-05-21): Amazon US rows use Monthly (combined), Amazon CA rows use Dashboard (CA-only).

---

## Report A — Sales by Product/Month (Monthly history, 3 brands)

### How to pull (per brand login)

1. Sign into [sellerboard.com](https://sellerboard.com) for the brand
2. Reports → **Sales by product/month**
3. Set the date range to the **maximum available** (28 months back → today)
4. Export as `.xlsx`

⚠️ **Make sure the date range goes back at least 24 months** — short ranges (1-3 months) will show up as "INSUFFICIENT" volatility on the report. If only 1 month exports, you picked the wrong date range — re-pull.

### Where to drop them

```
reports\sellerboard\MTB\     reports\sellerboard\NFMD\     reports\sellerboard\SS\
```

**No renaming.** The loader picks the file with the widest date range automatically.

### What the pipeline uses it for

- **📊 Amazon Sales History tab** — last 12 months of actuals + TTM Qty + YoY % per ASIN
- **📈 Forecast Pivot tab** — Amazon side of the actuals heatmap (last 12 closed months)
- **Demand Volatility scoring** — coefficient of variation over last 12 months → STABLE / MODERATE / VOLATILE bucket on every Amazon row
- **Amazon US 90-day velocity** — derived from last 3 closed months, applied to `daily_vel` on US market rows (replaces SoStocked Adj. Velocity for the 118+ ASINs that match)

---

## 🆕 Report B — Dashboard Products, Amazon CA filtered (CA velocity + forecast)

Per-marketplace CA-only Sellerboard export. Drives accurate CA Amazon velocity (replacing the inflated US+CA combined number) AND the CA-specific monthly forecast on the Amazon CA tab.

### How to pull (per brand login)

1. Sign into [sellerboard.com](https://sellerboard.com) for the brand
2. ⚠ **Switch the marketplace selector** (top-right) to **`amazon.ca`** before exporting
3. Reports → **Dashboard Products** (NOT Sales by Product/Month — the format is different)
4. Set date range:
   - **Weekly workflow**: trailing 90 days (e.g., Feb 22 → May 21) — one file per brand per week
   - **OR quarterly snapshots**: pull one file per quarter (Q3 2025, Q4 2025, Q1 2026, etc.) — keeps a longer rolling window for seasonality
5. Export as `.xlsx`
6. Date range MUST be in filename: `..._DD_MM_YYYY-DD_MM_YYYY_*.xlsx` — pipeline parses it

### Where to drop them

```
reports\sellerboard\MTB\canada\     reports\sellerboard\NFMD\canada\     reports\sellerboard\SS\canada\
```

**No renaming.** The loader auto-detects every Dashboard Products file in the `canada/` subfolder and sums across non-overlapping date ranges.

### What the pipeline uses it for

- **Amazon CA velocity** — `avg = total_units ÷ total_days` per ASIN, replaces the previously-inflated US+CA combined number for CA market rows
- **Amazon CA quarterly seasonality** — derives Q1/Q2/Q3/Q4 factors per ASIN from the date-tagged files, applied to forward monthly forecasts (Apr-Dec)
- **CA forecast (9MO PLANNING column on Amazon CA tab)** — `monthly_forecast = CA_avg × Q_factor × days_in_month`

### Pipeline log to look for after running

```
→ Sellerboard CA velocity: NN ASINs across NN files (MTB: X units / X d × X f · NFMD: ... · SS: ...)
→ CA forecast: NN items use CA quarterly seasonality · NN use flat-rate (CA daily_vel × days)
```

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

# 9️⃣b SAP Inventory in Warehouse — 1 file (weekly)

Per-warehouse inventory snapshot from SAP. Feeds the **🔄 SAP↔SB Rebalance** tab in the weekly report + the standalone monthly reconciliation file.

## How to pull

1. SAP → **Inventory in Warehouse Report**
2. Run with **all warehouses** selected (don't filter — the parser splits by warehouse marker rows internally)
3. Export as Excel
4. Drop into `Downloads\` — auto-classifier handles the rest

**File-name variants the classifier recognizes** (any of these):
- `Inventory_in_warehouse*.xlsx`
- `SAP Inventory in Warehouse Report.xlsx`
- `Inventory In Warehouse Report.xlsx`
- `InventoryInWarehouse.xlsx`

**Auto-routed to:** `reports\_data\sap-inventory\`

## What the script reads

The file has a quirky format — warehouse codes appear as separator rows where `Item No. == "Whse:"`. The parser walks row-by-row tracking the current warehouse. Columns used:

- **Item No.** → 12-digit UPC
- **In Stock** → quantity at that warehouse
- **Item Price** → unit cost (used for $ at risk calc in the rebalance)

## ShipBob warehouse codes in SAP

The reconciliation aggregates across these warehouse codes (filters out everything else):

| SAP code | ShipBob FC | Brand split |
|---|---|---|
| `SBGA-MT` | Fairburn, GA | MTB |
| `SBGA-SS` | Fairburn, GA | SS + NFMD |
| `SBNV-MT` | Reno, NV | MTB |
| `SBNV-SS` | Reno, NV | SS + NFMD |
| `SBPA-MT` | Bethlehem, PA | MTB |
| `SBPA-SS` | Bethlehem, PA | SS + NFMD |
| `SBCA-MT` | Moreno Valley, CA | MTB only |
| `SBGAMTQC` | Fairburn QC hold | MTB |
| `SBGASSQC` | Fairburn QC hold | SS + NFMD |

NFMD inventory is tracked under the SS warehouse codes (NFMD shares the SS legal entity in SAP).

## Where the output shows up

- **🔄 SAP↔SB Rebalance** tab in weekly-report (auto, every Monday)
- **First Monday of month:** run `python scripts/build_sap_sb_rebalance.py` for the standalone 5-tab cleanup file

---

# 9️⃣c SAP Inventory Transfer Requests — 1 file (weekly)

Pending **approved-but-not-yet-shipped** inter-warehouse transfer requests from SAP. Adds critical context to the 🔄 SAP↔SB Rebalance by explaining variances that are "in flight between warehouses."

## How to pull

1. SAP → **Inventory Transfer Requests Report** (or similar — wherever pending SAP transfer requests live)
2. Filter to status = "Accept" (approved, awaiting shipment) if not already default
3. Export as Excel
4. Drop into `Downloads\` (or `OneDrive\Desktop\`, or any of the scanned inbox paths) — auto-classifier handles the rest

**File-name variants the classifier recognizes** (any of these):
- `SAPinventorytransferrequests.xlsx`
- `SAP Inventory Transfer Requests.xlsx`
- `Inventory Transfer Requests.xlsx`

**Auto-routed to:** `reports\_data\sap-transfer-requests\`

## What the script reads

Key columns:
- **Item No.** → 12-digit UPC
- **From Warehouse** / **To Warehouse** → e.g., `SBGA-SS → AMZN-SS`
- **Quantity** → units to transfer
- **EDI Line Status** → only `Accept` rows count (approved, waiting to ship)

The reconciliation script computes two per-UPC totals:
- **XFER OUT** = sum of `Quantity` where `From Warehouse` is a ShipBob warehouse (units about to leave SB)
- **XFER IN** = sum of `Quantity` where `To Warehouse` is a ShipBob warehouse (units about to arrive)

## Why this matters

When SAP says "SBGA-SS has 1,000 units of AIVA Black" but ShipBob shows fewer — and there's an approved transfer request for 1,308 units from SBGA-SS to AMZN-SS — the variance is **already explained**. Those units are pre-allocated to leave; ShipBob's view is more current than SAP's.

Without this data, the rebalance would flag the variance as "missing inventory." With it, the variance becomes "in flight" — no investigation needed.

## Where the output shows up

- **🔄 SAP↔SB Rebalance** tab — new columns **XFER OUT** (red) and **XFER IN** (green)
- **🔁 SAP Transfer Requests** tab in the standalone monthly file — full list of pending moves color-coded by direction (🔴 Leaving SB · 🟢 Arriving SB · 🟡 SB↔SB internal · ⚪ Non-SB)
- Summary tab KPI block: `SAP Transfer Requests (pending)`, `Units transferring OUT/IN of SB`

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
│   │   ├── MTB\         ← Forecast + Inventory exports (or land in Downloads\)
│   │   │   └── fva-history\  ← 🆕 month-by-month FvA accumulation (one file per closed month)
│   │   ├── NFMD\
│   │   │   └── fva-history\
│   │   └── SS\
│   │       └── fva-history\
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
│   │   ├── MTB\
│   │   │   ├── (Sales by product/month .xlsx — US+CA combined Monthly)
│   │   │   └── canada\  ← 🆕 (Dashboard Products .xlsx — marketplace=amazon.ca, CA-only)
│   │   ├── NFMD\
│   │   │   ├── (Sales by product/month .xlsx)
│   │   │   └── canada\
│   │   └── SS\
│   │       ├── (Sales by product/month .xlsx)
│   │       └── canada\
│   ├── sap-open-pos\    ← SAP_Openpurchaseorderreport.xlsx
│   ├── in-transit\      ← IN_TRANSIT_LOG_YYYY-MM-DD.xlsx
│   ├── item-master\
│   │   ├── item_master.xlsx
│   │   └── amazon-sku-mapping.xlsx  ← 🆕 (Amazon listing SKU ↔ SAP UPC mapping)
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

# ✅ Pre-run checklist (34 weekly inputs)

- [ ] **9 SoStocked files** (3 brands × 3 reports — Forecast + Inventory + FvA) — in `Downloads\` or `reports\sostocked\[BRAND]\`. FvA files go in `reports\sostocked\[BRAND]\fva-history\` to accumulate month-by-month (see Section 1 Report C). One-time backfill: 15 files (5 months × 3 brands) — then 3 current-month FvA files weekly.
- [ ] **9 Amazon Seller Central files** — US: AWD + FBA × 3 brands (6 files) in `reports\seller-central\US\[BRAND]\`. CA: FBA only × 3 brands (3 files — MTB doesn't have AWD CA) in `reports\seller-central\CA\[BRAND]\`. **Don't skip CA FBA pulls** — they drive CA stock + FC Transfer numbers on the Amazon CA tab.
- [ ] **4 ShipBob files** (4 brand logins — On Hand Summary) — in `reports\shipbob\[BRAND]\`
- [ ] **2 Walmart files** (NFMD + SS — WFS Inventory .xlsx) — in `reports\walmart\[BRAND]\`
- [ ] **1 Floship file** (Product Inventory export) — in `reports\floship\`
- [ ] **1 Valogix file** (Item Location History Forecast) — in `reports\valogix\`
- [ ] **3 Sellerboard Monthly files** (3 brand logins — Sales by product/month, max date range, marketplace ignored — US+CA combined) — in `reports\sellerboard\[BRAND]\`
- [ ] **🆕 3 Sellerboard CA Dashboard files** (3 brand logins — Dashboard Products, marketplace = amazon.ca, 90-day or quarterly range) — in `reports\sellerboard\[BRAND]\canada\`
- [ ] **1 Valogix Exception Report** (History Exception export) — in `reports\valogix-exceptions\`
- [ ] **1 SAP Open PO report** (full export, no filtering) — in `reports\sap-open-pos\`
- [ ] **1 In-Transit Log** (latest) — in `reports\in-transit\` *(skip if not updated)*
- [ ] **`item_master.xlsx`** present in `reports\item-master\` *(no weekly refresh — only re-pull `SAPABCCLASSIFICATION.xlsx` when SAP classifications change)*
- [ ] **`amazon-sku-mapping.xlsx`** present in `reports\item-master\` *(no weekly refresh — only update when new SKUs launch on Amazon. Maps Amazon listing SKU ↔ SAP UPC for the 30+ items where they differ — e.g., 859886007685-M → SAP 859886007685, BODYBRBLK → SAP 859886007791)*
- [ ] **Carryover sku-review** in this week's `outputs\YYYY-MM-DD\` folder *(if you have decisions to fold in)*

When all checked → run the 3 scripts (see "How to run" section above).

---

# 🔗 Companion SOPs

- [[06 Processes & SOPs/(C) Weekly Analysis Cheat Sheet — 1 Page]] — print-and-stick version
- [[06 Processes & SOPs/(C) ABC Classification Reference]] — the 6 ABC codes
- [[06 Processes & SOPs/(C) Daily Morning Routine — SCM]] — daily routine
- [[15 Meetings & Decisions/(C) Weekly Run Log — 2026-05-01]] — current week's live runbook

---

*Rewritten: May 4, 2026 · Consolidated: May 18, 2026 (absorbed Step-by-Step SOP + System Map + per-source pull lists) · Owner: Supply Chain*
