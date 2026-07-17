---
tags: [demand-planning, amazon, node-spec, as-built]
node: Amazon US
brands: [MTB, SS, NFMD]
status: as-built-v1
updated: 2026-07-17
author: Claudian (with Tommy)
supersedes: "(C) Amazon US Node — Demand Planning Structure.md (3-tab Send/Analysis/Map)"
---

# Amazon US Node — Book1000 Planner (as-built)

> **What this is.** The as-built spec for `build_amazon_planner.py` — the "Book1000
> factory." It reproduces Tommy's hand-built `Book1000.xlsx` as an auto-generated
> **live-formula** workbook: one planning tab per brand (MTB / SPA / NFMD) driven by
> data tabs. This **replaces** the earlier 3-tab Send/Analysis/Map planner.

```
python scripts\build_amazon_planner.py
→ outputs/YYYY-MM-DD/amazon-planner-YYYY-MM-DD.xlsx
```

---

## 1. Design decisions (Tommy, Jul 2026)

- **Live Excel formulas** — you edit inventory / PO / forecast and everything
  re-flows. openpyxl writes formulas but does **not** calculate them, so the file
  looks blank until you open it in Excel (Excel recalcs on open). Expected.
- **Data tabs are BUILT, not pasted** — each column the brand-tab formulas need is
  placed at the exact Book1000 letter, pulled **by header name** from the raw
  exports. The raw FBA/AWD exports have drifted (`fc-transfer`, `Outbound to FBA`
  moved columns), so a raw paste would feed the formulas the wrong data.
- **Time-phased PO coverage** — a UNIS PO only counts as coverage in the month it
  actually lands (Load Date + **50d** transit vs each month's cutoff). Cols AF–AM.
- **Transit days** live in `$BH$1` (out of the data region) so the reference
  survives brands with many rows (SPA has 130+). Book1000 used `$E$28`; identical.
- **UPCs coerced to numbers** so numeric `SUMIF`/`SUMPRODUCT` matches work
  (Book1000 stores UPCs as numbers).

## 2. Stockout scope — TOTAL NETWORK (confirmed Tommy 2026-07-17)

`Total Inventory (M)` = `FBA available + FBA fc-transfer + Reserved FC Processing
+ AWD available + AWD outbound-to-FBA + UNIS units`. So the **stockout date counts
all inventory for the SKU, including AWD/UNIS in transit** — it reads *later* than
SoStocked (which counts FBA-sellable only). This is intended: it's the right basis
for PO timing because that upstream inventory really is inbound. (Example: SKU
`811573031397` — FBA 351 vs total 640; the extra 277 is an AWD shipment in transit
to FBA, so total-network stockout is ~Oct 19 vs SoStocked's FBA-only ~Sep 2.)

## 3. Brand tab layout (one row per canonical UPC)

**Main grid:**

| Col | Header | Logic |
|---|---|---|
| A · B · C | ASIN · SKU · Desc | Desc = VLOOKUP against `BAse` (SKU, then numeric, then LEFT-12) |
| D–K | 8 months (current → +7) | SoStocked "Forecasted Sales Monthly" (US) |
| L | Total Forecast | `SUM(D:K)` |
| M | **Total Inventory** | FBA(avail+fc-transfer+Reserved FC Processing) + AWD(avail+outbound) + N |
| N | Unis | `SUMPRODUCT` match of Unis Item ID vs SKU × Units |
| O | Open POs | `SUMIF` Open POs by ASIN (Amazon-US warehouses only) |
| P | Run Out (incl POs) | first month cumulative demand > M+O |
| Q | Match UPC | `--SKU`, else `sku map` reverse lookup |
| R–U | UNIS Incoming · Next Arrival · Next PO# · Last Arrival | `container plan`, Load Date **+50d** |
| V–AC | forecast mirror | the coverage color band |
| AF–AM | cumulative UNIS units arrived by each month | time-phased PO landing |
| AO–AV | status code 1/2/3/4 | drives coverage coloring |
| AX–BE | uncovered flag | demand > on-hand + arrived POs |

**Coverage colors** (CF on D:K and V:AC, driven by AO–AV): 🟢 covered by on-hand ·
🟩 covered by a PO that lands · 🟠 runs out this month · 🔴 no coverage left.

**Inventory Projection block** (below the grid):

| Col | Header | Logic |
|---|---|---|
| A–C | ASIN · SKU · Item | mirror of grid |
| D–K | running balance after each month | prev + PO arrivals − forecast; 🟢 ≥0 / 🔴 <0 |
| L | Stockout Date | interpolated day within the month it goes negative |
| M · O · P | **Cover thru [mo3] / [mo6] / [mo7]** | `MAX(0, −[that month's ending balance])` — shortfall covering demand **through the end of** that month (incl. its forecast). 🟠 when >0. *(Tommy 2026-07-17: "cover thru October = cover the month of October.")* |
| Q · R · S | Unis · ShipBob · **Replen From** | ShipBob = `SUMIF(shipbob, UPC, Fulfillable)`; Replen From = **UNIS first, then ShipBob**, else "—" |

## 4. Data tabs (built from raw exports)

| Tab | Source | Key columns |
|---|---|---|
| FBA | Seller Central FBA ×3 | D=asin, G=available, H=fc-transfer, CL=Reserved FC Processing |
| AWD | Seller Central AWD ×3 | D=ASIN, G=Available in AWD, Q=Outbound to FBA |
| Open POs | SAP Open POs (Amazon-US filter, ASIN-joined) | A=UPC, C=Remaining Qty, D=ASIN |
| Unis | UNIS WMS export (cases×CASE_PACK) | B=Item ID (UPC), H=Units |
| container plan | Container Plan ("US POs"-style sheet) | C=UPC, E=Destination, G=Units, L=Load Date, B=PPO# |
| sku map | amazon-sku-mapping.xlsx (reverse UPC↔merchant SKU) | A=UPC, B=Merchant SKU |
| BAse | **item_master.xlsx Sheet1 + sku-map merchant SKUs** (~1,430 rows) | A=Item No, B=Description |
| shipbob | ShipBob exports (MTB/SS/NFMD; LUMOS skipped) | A=UPC key, I=Fulfillable |

## 5. Row curation

Rows = FBA listings ∪ SoStocked-forecasted UPCs, **one per canonical UPC**
(representative ASIN/SKU per ASIN prefers a SKU that resolves to a description, then
max available). Amazon listing artifacts (`Uncommingled.*`, `*.missing*`, `MSKU.*`)
are filtered out. Zero-forecast FBA listings still appear (sorted to the bottom) so
carried inventory is visible.

## 6. Known characteristics / notes

- **Descriptions:** resolve for all but genuinely-new SKUs missing from the item
  master (e.g. `811573031502`). Add them to `item_master.xlsx` to fill.
- **Current-month demand** subtracts the *full* month's forecast from today's
  inventory (matches Book1000) — slightly conservative mid-month.
- **AF cutoff** counts a PO as "arrived by month M" only if it lands before the 1st
  of M (Load + 50d < M/1) — a mid-month arrival lands in the next month's bucket
  (Book1000 convention; conservative).
- **Manual M adders** (Book1000 had one-off `+1040` etc.) are omitted — M is pure
  formula; add adjustments by hand if needed.
- **Fixed ranges:** Unis `$2:$100` (fine, ~12 rows), MMULT `ROW($A$1:$A$8)` (8
  months). Both tied to current assumptions.
- **Verify in Excel:** openpyxl can't calculate, so always open the file once to
  confirm the recalc is clean.

## 7. Inputs (drop into `reports/_inbox`; auto-routed)

Seller Central FBA ×3 · AWD ×3 · SoStocked ×3 · Outbound Shipment Data ×3 ·
UNIS export · SAP Open POs · Container Plan · ShipBob ×3. (Item master +
amazon-sku-mapping live in `reports/item-master/`.)
