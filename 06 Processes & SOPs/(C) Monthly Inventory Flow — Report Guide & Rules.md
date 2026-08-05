---
type: sop
created: 2026-08-05
owner: Tommy Sapia
tags: [sop, inventory, planning, amazon, shipbob, report]
script: MTB-SupplyChain/scripts/build_monthly_flow.py
---

# (C) Monthly Inventory Flow — Report Guide & Rules

The month-by-month supply/demand **waterfall** per SKU (the "Book3" view Tommy designed).
One editable workbook **per channel** that shows, for each SKU, whether it stays in stock
across the next 8 months and — if not — the exact day it runs out and what to do about it.

- **Code:** `MTB-SupplyChain/scripts/build_monthly_flow.py`
- **Run:** `cd C:\Users\Tom Sapia\MTB-SupplyChain` → `py -3 scripts\build_monthly_flow.py`
- **Outputs:** `outputs/<date>/amazon-us-inventory-flow-*.xlsx` and `…/shipbob-inventory-flow-*.xlsx`
- **Published to:** SUPPLY CHAIN ANALYSIS hub (OneDrive→SharePoint), a fresh dated copy each run.

---

## The card (one per SKU)

Each SKU is its own **banded block** (dark title band = UPC · Description · **Class** · Notes),
grouped into **ABC sections** (all **A** SKUs first, then **C**, **D**, then **Other/unclassified**).

| Row | Meaning |
|---|---|
| **Forecast** 🔵 | Monthly demand. *Editable.* |
| **Starting** 🔵 (month 1) | On-hand at the start. Month 1 is *editable* (override on-hand "just in case"); later months = the prior month's Ending (formula). |
| **PO (available)** 🔵 | Bankable supplier POs credited to the month they can cover. *Editable.* |
| **Fly-in (edit)** 🔵 | Air-freight — **blank by default** (just-in-case, never auto-suggested). *Editable.* |
| **Ending** | `= Starting + PO + Fly-in − Forecast`. Turns **light red** when negative. |
| **Days of cover** | `= Ending ÷ daily demand`. |
| **Stockout date** | Exact day inventory hits 0 (live formula). "covered in-horizon" if it never goes negative. |

**🔵 Blue cells are editable** — type into Forecast, Starting, PO, or Fly-in and the Ending,
Days-of-cover, Stockout date, and every later month **recalculate live**.

### Notes column (S)
Free-text per SKU, **persisted across rebuilds** (stored in `reports/_state/flow_notes_<channel>.json`,
keyed by UPC). Type a note in column **S**; the next run harvests it and re-renders it. An empty
cell never erases a saved note.

---

## The "Incoming POs & Transfers" box (right of each card)

`PO / Source · Qty · Load · ETA · Covers · Type`, colour-coded:

- 🟩 **In-Transit** — shipped, on the water/road (counts)
- 🟧 **Container Plan** — booked on a container, not yet sailed (counts)
- ⬜ **Open PO** — still at the supplier, *not booked on a container* → shown **"(not counted)"**
- 🟦 **Transfer** — UNIS staging / ShipBob-pinch availability (informational)

---

## The rules (why the numbers are what they are)

1. **Only bankable supply counts toward coverage** — In-Transit **+** Container-Plan only.
   **Open POs do NOT count** (their date is a soft SAP Ship-By + transit estimate). They appear in
   the box greyed and on the **Watch List** tab as "to book onto a container." *To make an open PO
   count, it has to move PO → supplier → container plan → in-transit.*
2. **Receiving lag = ~2.5 weeks** (`RECEIVING_DAYS = 18`). A PO becomes warehouse-available ~2.5
   weeks after it **lands (ETA)**.
3. **A PO covers the month it becomes available** (available part-way through a month still covers
   that month). End-of-month inventory is exact; an intra-month dip before a late-month availability
   isn't shown (standard monthly-sheet simplification).
4. **Network model** (Tommy 2026-08-04):
   - **UNIS → Amazon = a real, standing supply line** (e.g. Hair Spray). UNIS-warehouse POs count.
   - **ShipBob → Amazon = pinch/as-needed only** — *never* auto-counted as Amazon supply.
   - **UNIS is also a transload point to ShipBob** — some UNIS-staged inventory is ShipBob-bound.
5. **Fly-in is the last resort.** Prefer expediting a PO through the pipeline so it lands in time;
   fly only to bridge a gap that can't be closed that way.

---

## Config knobs

| Want to change… | Where |
|---|---|
| Receiving lag (2.5 weeks) | `RECEIVING_DAYS` in `build_monthly_flow.py` |
| A SKU's UPC / listing mapping | `sku_rules.ALIAS` (e.g. `B0CQKK2YCK → 811573031090` = MTBLavendar) |
| Mark a SKU obsolete / phase-out | add its UPC to `sku_rules.PHASE_OUT` |
| ABC class override | `sku_rules` ABC override / item master |
| One-time PO reroute between channels | `build_amazon_planner.PO_REROUTE_TO_US` (auto-expiring) |

---

## Data it reads (must be current)

Built from the replen-planner outputs (`amazon-us-replen-*.xlsx`, `shipbob-replen-*.xlsx`), so
**run the planners first** if the underlying data changed. Those in turn read: Dave's Amazon
Forecast (USA tab for US), SAP inventory + open POs, the live Container Plan + In-Transit Log
(OneDrive-synced), UNIS staging, and item-master ABC.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Edits don't recalculate | Workbook is set to auto-calc; if not, press **F9**. |
| "⚠ saved a fresh copy" in the run log | The dated file was open in Excel — it saved a timestamped copy instead of crashing. Close Excel and rerun for the clean canonical name. |
| A SKU shows in "Other (unclassified)" | It has no A–D class in the item master (or is keyed by ASIN with no UPC). Fix via `sku_rules` alias / ABC override. |
| Notes disappeared | They persist in `reports/_state/flow_notes_<channel>.json`; a note is only overwritten by a newer edit, never blanked. |

---

*Generated by Claudian 2026-08-05 · code lives in the MTB-SupplyChain repo (now on GitHub).*
