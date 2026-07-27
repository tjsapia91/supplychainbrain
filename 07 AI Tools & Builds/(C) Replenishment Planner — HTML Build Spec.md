# (C) Replenishment Planner — HTML Build & Handoff Spec

**Purpose:** everything a developer needs to rebuild the ShipBob / Amazon
Replenishment Planner as a styled HTML web app. It documents the **files to
upload**, the **calculations**, the **output layout**, and the **business
rules**. Source of truth for the logic is the Python builders
(`build_shipbob_replen.py`, `build_amazon_replen.py`) in `MTB-SupplyChain/scripts/`.

Generated 2026-07-24.

---

## 1. What the report is

A per-SKU replenishment plan for each fulfillment node, one tab per brand
(**MTB / SPA (Spa Sciences) / NFMD**). For every active, A–D-classified SKU it shows:

- 8 months of **demand** (forecast)
- current **sellable** on-hand
- **open POs** and their phased arrivals
- a **half-month projected-inventory map** (coverage, colored green/red)
- the **stockout date** and the **units to send in** to cover through key months
- a persistent **Actions taken** log

Two planners share the same shape:
- **ShipBob** — node = ShipBob 3PL; demand = Shopify + TikTok + Walmart (Valogix).
- **Amazon** — node = Amazon FBA; demand = SoStocked.

---

## 2. FILES TO UPLOAD (drop these into the web app)

### ShipBob planner
| # | File | What it is | How the app finds it |
|---|------|-----------|----------------------|
| 1 | **`OpenPOs-ContainerPlan.xlsx`** | ONE workbook, 3 sheets: **`Container Plan`**, **`Open POs`**, **`In Transit`** (SAP + logistics) | detect a workbook containing ≥2 of those sheet names → split each sheet out |
| 2 | **ShipBob inventory export — MTB** | ShipBob "Inventory Status", blob **385579** | filename contains `385579` |
| 3 | **ShipBob inventory export — SS** | blob **385953** | filename contains `385953` |
| 4 | **ShipBob inventory export — NFMD** | blob **385954** | filename contains `385954` |
| 5 | **Valogix Combined Forecast** | raw wide export (History + Forecast + metadata). CSV or XLSX | headers include `Current Rolling 12 (history)` and `Forecast Total (Next 12 Months)` |
| 6 | **`ABC Class.xlsx`** | SAP item master: `Item No.`, `Item Classification` (A/B/C/D/E/F/I/S/Z), `Active` (Y/N) | headers `Item Classification` + `Active` |

### Amazon planner (additional)
| # | File | What it is |
|---|------|-----------|
| 7 | SoStocked **Projected Forecast** (per brand ×3) | Amazon demand |
| 8 | Amazon **FBA** inventory (US ×3) + **AWD** (×3) | on-hand / inbound |
| — | reuses #1 (Open POs + Container Plan + In-Transit) and #6 (ABC) | |

**One-inbox rule:** the user drops everything in a single folder; the app
classifies each file by **content** (sheet names / column headers), not filename.

---

## 3. Reference data (semi-static, stored)

- **Item master / SKU→UPC map** — resolves merchant SKUs (e.g. `811573030475-M`)
  to a canonical 12-digit UPC. Needed to merge listing variants.
- **Brand of a UPC** — determined by which ShipBob **blob** physically holds the
  stock (SS account = SS, etc.); UPC prefix is only a fallback. This is why an SS
  device on an NFMD-range UPC (e.g. SMARTGUN `850038082628`) still lands on SPA.

---

## 4. Processing pipeline (order of operations)

1. **Split** the combined `OpenPOs-ContainerPlan.xlsx` into its 3 sheets.
2. **Convert Valogix** raw export → forecast rows (see §5.1).
3. **Classify / file** every upload by content.
4. Per brand, build the SKU **universe** (§5.5), compute demand / sellable /
   arrivals, render the tab, apply the **ABC + Active filter** (§5.6).
5. Everything not (Active AND A–D) → an **"Excluded"** tab with a reason.

---

## 5. Per-SKU calculations

### 5.1 Demand — Valogix "Combined Forecast" (ShipBob)
- The Valogix export has 3 sections per row: **History** → `Current Rolling 12`
  → **FORECAST months** (starting Excel col **AF**) → `Forecast Total` → metadata.
- **Read the FORECAST block only** (the columns between `Current Rolling 12` and
  `Forecast Total (Next 12 Months)` — i.e. AF onward). Do **not** read history.
- Label the forecast columns **by position** from the current month (`Jul-26,
  Aug-26, …`) — Valogix's date headers have a post-December year bug; position
  labeling dodges it.
- This "Combined Forecast" **already includes Walmart WFS demand** → do NOT add
  Walmart separately. TikTok is a separate Valogix location (`TIKTOKMT/SS`) and IS
  added. So **ShipBob demand = Valogix SBGA Combined + TikTok**.
- Amazon demand instead comes from **SoStocked** projected forecast.

### 5.2 On-hand = **Sellable** (ShipBob)
- From the ShipBob export, use **Sellable** (= On Hand − Committed), NOT gross On Hand.
- **Exclude** any SKU variant whose name/SKU contains **`AMZ`** — those units are
  Amazon-stickered and reserved for FBA, not sellable to Shopify/TikTok/Walmart.
- Sum across FCs/lots per canonical UPC.

### 5.3 Open POs & arrivals (ETA)
Merge three sources, keyed by canonical UPC, deduped by **PO#**:
1. **SAP Open POs** — warehouse `SBGA-*`, status `O`, `Remaining Open Quantity > 0`.
   Provides the **quantity** (net of receipts).
2. **Container plan** — rows with Destination = **SB** (ShipBob).
3. **PO PDFs** (optional) — POs parsed from SAP PDFs.

**ETA rule (important):**
- If a PO# appears in the **container plan**, its **ETA = Load Date + 45 days**
  (ocean transit). This wins on timing — SAP due dates are unreliable ("posting =
  due" placeholders).
- If the PO is only in SAP (not in the container plan), ETA = SAP Original Due Date.
- SAP always supplies the **quantity**; the container plan supplies the **timing**.

Constants: **ocean transit = 45 days** (Load → dock). **Receiving lag = 14 days**
(dock → sellable at ShipBob).

### 5.4 Half-month phased map + coverage
- Split the 8-month horizon into **16 half-month buckets** (1–15 / 16–end).
- Each PO's **available date = ETA + 14-day receiving lag**; bucket by that.
- A PO only helps a half-bucket if it's available **before** that half begins
  (so a 7/29 arrival + 14d = ~8/12 → first covers the **Aug 16–31** bucket).
- **Projected inventory** per bucket = `Sellable + arrivals available before the
  bucket − demand through the bucket`. **Green ≥ 0 (covered), red < 0 (short).**

### 5.5 Universe (which SKUs appear on a brand tab)
- UPCs with **real stock (>0) in that brand's ShipBob blob**, PLUS
- demand UPCs that **classify to that brand** (by blob, else prefix).
- Zero-stock rows for the *other* brand (shared catalog) are excluded — this
  prevents phantom 0-sellable rows on the wrong tab.

### 5.6 ABC + Active filter
- **Main tabs show only SKUs that are Active (Y) AND classified A, B, C, or D.**
- Everything else (inactive, class E/F/I/S/Z, unclassified, or no activity) →
  a single **"Excluded (inactive, non A-D)"** tab with a per-row reason.

### 5.7 Current-month proration ("Report as-of" date)
- The current month is only partly left. A live **"Report as-of" date cell**
  (editable, defaults to build date) drives the remaining forecast:
  `remaining = month forecast × (days_in_month − day(as-of)) ÷ days_in_month`.
- Edit the as-of date → the current month's remaining demand, the projection, and
  the send-in numbers all recompute. Future months stay full.

### 5.8 Send-in to cover
- For checkpoints (≈ Oct / Jan / Feb) show **units to send in** =
  `MAX(0, −MIN(projected balance from now through that month))` — i.e. the deepest
  the balance goes negative, which is how many units must arrive (before the
  stockout) to stay covered through that checkpoint. `0` = already covered.
- **Stockout Date** = interpolated date the running balance first crosses 0.

---

## 6. Output layout (per brand tab)

Columns, left → right:

| Group | Fields |
|-------|--------|
| ID | UPC · Description · Supplier |
| Demand | 8 monthly forecast columns (Jul-26 … Feb-27), color-coded by coverage |
| Position | Total Forecast · **Sellable (editable)** · Incoming (Open PO) · Run Out (phased) |
| PO detail | Next Arrival (hover comment lists each PO by date) · Next PO# · Last Arrival |
| **Block A — Projected inventory (½-mo)** | 16 half-month cols; green=covers / red=short; hover comment "▲ +N units now sellable — PO ####" where inventory steps up |
| **Block B — PO arriving (½-mo)** | 16 half-month cols; units becoming sellable each half |

Below the grid: a **"Report as-of" date** cell, then the **INVENTORY PROJECTION**
table (UPC · Description · monthly end-of-month balance · Stockout Date ·
**Send-in to cover thru Oct/Jan/Feb** · **Actions taken (persists)**).

Plus tabs: **Excluded (inactive, non A-D)**.

---

## 7. Business rules & constants (quick reference)

| Rule | Value |
|------|-------|
| Ocean transit (Load → dock) | **45 days** |
| Receiving lag (dock → sellable) | **14 days** |
| Horizon | 8 months, split into 16 half-months |
| ABC codes kept on main tabs | **A, B, C, D** (+ must be Active=Y) |
| ShipBob on-hand basis | **Sellable** (On Hand − Committed), exclude `AMZ` variants |
| ShipBob demand | Valogix Combined Forecast (incl. Walmart) + TikTok |
| Amazon demand | SoStocked projected forecast |
| PO timing | container Load+45 wins over SAP due date; SAP gives qty |
| Current month | prorated to days remaining via the as-of date |
| Send-in qty | MAX(0, −min running balance through the checkpoint month) |

---

## 8. Colors & formatting (for the HTML styling)

- **Coverage green** `#63BE7B` · light green `#C6EFCE` · **orange** `#ED7D31` ·
  **red** `#F8696B`.
- Header band navy `#2E4E7E`, white bold text.
- Editable inputs (Sellable, Report-as-of date) = pale yellow `#FFF2CC` / `#FFFF00`.
- Block A header green `#1F7A54`; Block B header blue `#2E6DA4`; arrivals highlight `#BDD7EE`.
- Projected-inventory cell: green if ≥ 0, red if < 0.
- Half-month header shows the split on top: `1–15` / `16-<last day of month>`
  (use the real last day — 28/29/30/31).

---

## 9. Persistence — Actions log

- The **"Actions taken"** column must **carry forward between report runs**.
- Store it keyed by **UPC** (ShipBob) / **ASIN** (Amazon) in a small side store
  (JSON). On each generate: read the prior report's Actions column → merge into
  the store → re-inject into the new report. Clearing a cell removes it.
- In the web app this is naturally a per-SKU notes field saved in the DB.

---

## 10. Suggested HTML / web-app UX

- One page per brand (tabs), a **sticky left column** (UPC + Description) and a
  horizontally scrollable month grid.
- Render Block A as a **heatmap row** (green→red) with the arrival amount + PO#
  on hover (replaces the Excel cell comments).
- Make **Sellable** and **Report-as-of date** editable inputs that recompute the
  projection client-side (all the math is simple arithmetic per §5).
- Surface the **Send-in to cover thru Jan** as the headline action number per row,
  with the **Stockout Date** and a per-SKU **Actions** notes box saved server-side.
- Keep the **Excluded** list one click away with the exclusion reason.

---

*Logic authored in `MTB-SupplyChain/scripts/build_shipbob_replen.py` and
`build_amazon_replen.py`; supporting: `split_combined.py`, `valogix_convert.py`,
`planner_actions.py`, `sort_downloads.py`, `build_amazon_planner.load_abc_class`.*

---

## Appendix A — EXACT column headers (parse by these names)

Match columns by **header name** (order can vary). Fields the app actually reads are **bold**.

### ShipBob inventory export (CSV, one per brand)
`SKU · Inventory ID · Inventory Name · Lot Number · Expiration Date · Incoming ·
On Hand · Committed · Fulfillable · **Sellable** · Exception · Backordered ·
Internal Transfer · Fulfillment Center`
→ read **SKU** (skip any containing `AMZ`) and **Sellable** (fallback Fulfillable), summed per UPC.

### Combined workbook — sheet **`Container Plan`**
`Old PPO · **PPO#** · **UPC** · Desc · **Destination** · HTS · **Units** · Cases ·
CBM · PO Date · Ready Date · **Load Date** · Inspection Date · NOTES · Notes Harry`
→ rows where **Destination = `SB`**; ETA = **Load Date + 45**. (⚠ UPC column can be
truncated — match POs to SAP by **PPO#**, not UPC.)

### Combined workbook — sheet **`Open POs`** (SAP)
`**Document Number** · Segment · **Document Status** · Canceled · Posting Date ·
**Original Due Date** · Ref · Vendor Code · Vendor Name · **Item No.** ·
Item/Service Description · Quantity · Ship By Date · **Remaining Open Quantity** ·
**Warehouse Code** · Unit Price`
→ keep **Warehouse Code** starting `SBGA` (Amazon = `AMZN-*`), **Status = `O`**,
**Remaining Open Quantity > 0**; qty = Remaining Open Quantity.

### Combined workbook — sheet **`In Transit`** (Amazon planner only)
Key columns: `PO # · UPC · ITEM · QTY Shipped · CONTAINER # · RECEIVING WAREHOUSE ·
QTY RECEIVED · ETA AT PORT · WHSE DELV. DATE` (plus a lot of manual tie-out columns —
ignore the rest). Active = `QTY RECEIVED < QTY Shipped`.

### `ABC Class.xlsx` — sheet `ITEM MASTER`
`Item Description · **Item No.** · **Item Classification** · **Active**`
→ Item No. = UPC; keep **Active = `Y`** AND **Classification ∈ {A,B,C,D}** on main tabs.

### Valogix Combined Forecast (raw wide CSV/XLSX)
Layout, left → right:
`Item Number · Description · **Location** · Supplier ·
[~25 HISTORY month columns] · **History Total** · **Current Rolling 12 (history)** ·
[FORECAST month columns] · **Forecast Total (Next 12 Months)** · [~35 metadata columns]`
→ **Forecast block = the columns BETWEEN `Current Rolling 12 (history)` and
`Forecast Total (Next 12 Months)`** (starts at Excel col AF). Label them by position
from the current month. Filter **Location** to `SBGA-MT/SS` (Shopify+Walmart) and
`TIKTOKMT/SS` (TikTok). Month headers are dates with a post-Dec year bug — never trust
the header year; use position.

*(Amazon-only inputs — SoStocked Projected Forecast, FBA, AWD — follow the same
"match by header name" rule; add their headers here when those uploads are wired.)*
