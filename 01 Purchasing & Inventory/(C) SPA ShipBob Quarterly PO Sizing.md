---
type: po-sizing-plan
scope: Spa Sciences (SS) items on ShipBob
target: quarterly order-up-to (230 days = ~140d ocean lead + 90d / one-quarter buffer)
script: MTB-SupplyChain/scripts/size_spa_pos.py
last_run: 2026-07-31
status: living
---

# 🧮 SPA ShipBob — Quarterly PO Sizing

Sizes a suggested PO for every Spa Sciences item on ShipBob to a **quarterly order-up-to target**.
Re-runnable on fresh data: `py -3 scripts\size_spa_pos.py [--cover 230] [--all]`.

## 🔁 To revisit / re-run
Say **"Run the SPA ShipBob PO sizing"** (or *"size the SPA POs"*). That re-runs the script on the
latest ShipBob export and rebuilds this list. Change the target with `--cover N` (e.g. 200 tighter,
260 more cushion).

## The math (same for every item)
```
PO = max(0, Target − Position)

Position   = ShipBob on-hand + de-kit add-back + Incoming(in-transit + container-plan + open-PO)
Demand/day = (next 6 months of forecast, summed) ÷ 183
Target     = Demand/day × 230        # 230 = ~140-day ocean lead + 90-day (one quarter) buffer
```
- **Incoming already counts every open PO** (all three supply tiers), so the PO is the *true* gap.
- **Target = 230d** makes it a quarterly cadence: order enough that when the next container lands
  (~140d out) you still hold ~a full quarter of stock.
- **De-kit add-back** = manual, for units physically on-hand but tied up in a work order (see below).

## Current plan — run 2026-07-31 (order-up-to 230d)
| UPC | Item | On-hand | +De-kit | Incoming | Position | d/day | Target | **PO** |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 850003115139 | MIO Green w/USB | 1,626 | +1,167 | 1,415 | 4,208 | 32.6 | 7,508 | **3,300** |
| 860021001178 | NOVA Pink w/USB | 198 | — | 1,056 | 1,254 | 17.7 | 4,082 | **2,828** |
| 850003115634 | AIVA Black* | 5,756 | — | 4,224 | 9,980 | 50.3 | 11,558 | **1,578** |
| 860021001161 | MIO Pink w/USB | 2,734 | — | 3,024 | 5,758 | 27.7 | 6,361 | **603** |
| 860021001123 | SIMA Pink w/USB | 3,312 | — | 0 | 3,312 | 16.1 | 3,701 | **389** |
| 850026141382 | LORI LED Eye/Lip | 341 | — | 0 | 341 | 2.4 | 553 | **212** |
| 850026141184 | PRIMA Massager | 618 | — | 12 | 630 | 3.3 | 763 | **133** |

**Total ≈ 9,043 units across 7 POs.** (80 other SPA items already covered.)

## Manual adjustments in effect
- **MIO Green (850003115139) +1,167** — units physically on-hand but locked in **de-kitting WRO 388151795** (separating MIO Green from the white commingle). Coded in `size_spa_pos.py` → `DEKIT_ADDBACK`. **Remove once the WRO completes** and the next ShipBob export shows the higher on-hand on its own.

## Caveats to hand-fix before placing
- **\*AIVA Black (1,578) is understated.** Its d/day (50.3) carries the one-time **August CVS reset fill** but **not** the ongoing CVS replen at the restored **2,738 doors** (not forecast yet). Real PO ≈ **5,000–7,000**. Vendor = **Ningbo Dream Big (V2691)**, ~140d ocean. See [[01 Purchasing & Inventory/(C) PO Tracker — Harry (Ningbo Zeyu).md]] once placed.
- **MIO Green on-hand is the commingled read** — the de-kit fixes part of it; confirm the base is clean.

## Next steps (when ready)
1. Lock the target (230d default) + the AIVA CVS number.
2. Output the formal quarterly buy sheet (by vendor) → **SUPPLY CHAIN ANALYSIS** hub.
3. Load the 7 POs into the PO tracker by vendor.

---
*Method + script are the durable part; the table is a snapshot. Re-run to refresh. (Tom 2026-07-31.)*
