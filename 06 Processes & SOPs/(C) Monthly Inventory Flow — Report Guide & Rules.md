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
grouped into **ABC sections**: **Class A + D (phase-in)** together first, then **C**, then
**Other/unclassified**. (Class D = phase-in SKUs, incorporated with A — Tommy 2026-08-05. D cards
keep their real "Class D" label so phase-ins stay identifiable inside the A section.)

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
4. **Amazon supply chain = demand → FBA ← AWD ← UNIS** (Tommy 2026-08-06 — full cascade modeled;
   ShipBob still has POs cover directly):
   - **The cascade:** demand hits FBA. **AWD auto-replenishes FBA FIRST** (`AWD → FBA` row =
     `MIN(AWD on-hand, FBA top-up need)`). **UNIS send-in covers only what AWD can't** (`UNIS → FBA` =
     `MAX(0, need − AWD→FBA)`, capped by UNIS on-hand). So FBA is fed AWD-first, UNIS-second, and stocks
     out only when FBA **and** AWD **and** UNIS are all dry. SKUs with no AWD just show AWD = 0 and go
     FBA ← UNIS.
   - **Rows:** Forecast · FBA start · AWD → FBA · UNIS → FBA (send-in) · Fly-in · **Ending (FBA)** ·
     **Days of cover** · AWD on-hand · UNIS on-hand · PO → UNIS (arriving) · Stockout date.
   - **FBA start = FBA only** (AWD is its own row now, not lumped in).
   - **Status tag per SKU** (on the title band, col 3) — at-a-glance triage from the TOTAL position
     (FBA + AWD + UNIS + landed POs) vs demand & lead time: **🟢 HEALTHY** (covered) · **🟡 SEND-IN
     NEEDED** (FBA+AWD alone run out, UNIS covers — you have a send-in to do) · **🟠 ORDER SOON** (total
     runs out in-horizon, beyond `LEAD_DAYS`=140 → place a supplier PO) · **🔴 CRITICAL** (total runs
     out *inside* lead time → expedite/fly, a normal PO can't land in time).
   - **🔒 SETTLED RULE — a PO becomes UNIS stock once it LANDS** (Tommy 2026-08-06, final call). Row
     **`PO → UNIS (arriving)`** (grey) shows POs arriving at UNIS. A PO is **informational while in
     transit** (it does NOT cover FBA early or go straight to FBA), but on its **arrival month it joins
     the UNIS on-hand pool** and the send-in can then draw on it. So `UNIS on-hand = prior on-hand +
     POs landed this month − send-in`. The stockout reflects real supply: FBA is covered as landed POs
     feed the send-in, and stocks out only when the UNIS pool (incl. landed POs) truly runs dry.
   - **`Send-in → FBA (auto)` is a min/max BATCH policy** (professional replenishment, Tommy 2026-08-06):
     send a batch **only when projected FBA drops below the reorder point**, then refill up to the
     order-up-to level. Draws **ONLY from physical UNIS on-hand** — so FBA stocks out when the physical
     UNIS pool (not future POs) can't cover it. Result = **lumpy** sends (months of 0), not a monthly
     top-up.
   - **Two editable knobs on each SKU's title band:**
     - **`Reorder ≤ (d)`** = reorder point in days (default **30**) — the trigger. Set it ≥ the send-in
       lead time (UNIS→FBA transfer + Amazon receiving ≈ 2–3 wks) + safety.
     - **`Up-to (d)`** = order-up-to days (default **90**) — the batch size. FBA peaks here right after a
       send; averages ~60d with a 30d reorder. **Frequency:** the wider the gap between up-to and
       reorder, the lumpier / less frequent the sends.
   - **`UNIS on-hand (covers)`** = prior on-hand **+ POs landed this month** − send-ins; starts at the
     on-hand shown on the band (`UNIS start <qty>`; eaches auto-computed from the raw export — see "UNIS
     inventory" below). This pool is what the send-in draws from.
   - **Ending (FBA) = Starting + Send-in + Fly-in − Forecast.**
   - **ShipBob → Amazon = pinch/as-needed only** — *never* auto-counted as Amazon supply.
   - **UNIS is also a transload point to ShipBob** — some UNIS-staged inventory is ShipBob-bound.
5. **Fly-in is the last resort.** Prefer expediting a PO through the pipeline so it lands in time;
   fly only to bridge a gap that can't be closed that way.

---

## Config knobs

| Want to change… | Where |
|---|---|
| Receiving lag (2.5 weeks) | `RECEIVING_DAYS` in `build_monthly_flow.py` |
| Default order-up-to days (90d) / reorder point (30d) | `DEFAULT_TARGET_DOC` / `DEFAULT_TRIGGER_DOC` in `build_monthly_flow.py` (or edit the per-SKU knobs on the band) |
| A SKU's UPC / listing mapping | `sku_rules.ALIAS` (e.g. `B0CQKK2YCK → 811573031090` = MTBLavendar) |
| Mark a SKU obsolete / phase-out | add its UPC to `sku_rules.PHASE_OUT` |
| ABC class override | `sku_rules` ABC override / item master |
| One-time PO reroute between channels | `build_amazon_planner.PO_REROUTE_TO_US` (auto-expiring) |

---

## UNIS inventory (auto-computed from the raw export)

The UNIS pool per SKU is computed automatically — **just drop the raw UNIS `data` export**
(the one-row-per-LP file) into `reports/_inbox/` and rebuild. The loader reproduces the
hand-built "Item Summary" method:

> **UNIS eaches = Σ QTY (col J, treated as CASES regardless of UOM) per Item × item-master
> master-carton pack (UPC Master Carton Quantity).**

No manual Units/Case entry. Verified to tie out to the Item Summary tab (e.g. bundle 850038082352
= 421 cases × 12 = 5,052; Hair Spray = 910 × 48 = 43,680). Code: `build_amazon_us_replen.load_us_reservoir`.

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
