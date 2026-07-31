---
type: batch-code-tracker
system-of-record: Prizm ERP (Reports → Generated Reports → Batch Code Tracking → CSV)
data-in-vault: 01 Purchasing & Inventory/_batch-data/ (drop the Prizm CSV here)
lookup: /batch-lookup <code | item# | UPC | PPO#>  (in-brain — no external app)
source: Outlook batch-code threads (Harry / Augusto / Michael)
last_scanned: 2026-07-31
status: living
---

# 🏷️ Batch Code Tracker

Batch/expiration codes matter for **Amazon compliance** (and retail). **Everything lives in the brain** — no external web app to maintain:
- **Full lot dataset** → drop the Prizm export in `_batch-data/`; search with **`/batch-lookup <code | item# | UPC | PPO#>`** (or just ask "look up batch …").
- **Conventions + live decisions** → this note (below), kept current by `/email-brief`.

## Batch-code convention (locked w/ Harry, Augusto 2026-07-27)
- **Format:** `PREFIX + MMYY` — e.g. **`RGS0726`** = Regular Salt, July 2026.
- **Salt prefixes:** Regular Salt = **`RGS`** · Xylitol Salt = **`XYS`** (use on all future salt batches).
- **Legacy codes still in the wild — BOTH salts** stay on their OLD codes until a **new batch is produced** (then switch to the `RGS`/`XYS` format + 5-yr exp):
  - Xylitol salt legacy = `NFMD03152026X` (NasalFresh + date + `X`).
  - Regular salt legacy = *(fill in — same NFMD+date format, no `X` suffix; confirm exact code)*.
- Example codes seen in Prizm: `NAC0426`, etc. (item prefix + MMYY).

## Expiration policy
- **Salt shelf life bumped 4 yrs → 5 yrs** (Michael's request, 7/27). Harry: applies **after current stock is used up** ("then we will change to 5 years"). Michael: *"this will keep things better for us at Amazon."*

## Active batch-code items (from email)
| Date | Item / order | Batch code | Status / action |
|---|---|---|---|
| **7/31** | **PO 3154** (final PI) | **new batch code** | ✅ Harry updated all codes on the final PI to the new code; PI attached — verify & sign |
| **7/31** | **PO 3152** (MTB order) | still **`0426`** (old) | 🔴 **DECISION NEEDED** — Harry: *"still the old 0426, do you need change?"* (device stays 0426) |
| **7/31** | **Salt bag** | **`RGS0726`** | 🔴 **CONFIRM** — Harry ordered bags at `RGS0726` (Juan's file, Tom confirmed 3 days ago); someone floated **`0826`** — Harry pushing back. Keep RGS0726 unless intended change |
| **7/31** | **Device** | **`0426`** | Harry: keep device same as `0426`; only the salt uses the new code |
| 7/30 | **EU order** (all boxes = **new print**) | new codes needed | 🟠 Harry needs the batch codes **shared with Juan** for the new-print boxes |
| 7/30 | **Regular salt** (current stock) | legacy code *(confirm)* | Stays on legacy until the **next batch** → then `RGS` + MMYY + 5-yr exp |
| 7/30 | **Xylitol salt** (current stock) | `NFMD03152026X` (legacy) | Stays on legacy until the **next batch** → then `XYS` + MMYY + 5-yr exp |
| 7/27 | New salt batches (both) | `RGS` / `XYS` + MMYY | New prefixes in effect once produced |

---
*Full lot-level data = the Prizm export in `_batch-data/`, searched via `/batch-lookup` (in-brain, replaces the old web app). This note tracks conventions + live decisions; `/email-brief` surfaces batch-code threads (Harry/Juan) and logs decisions here. (Tom 2026-07-30.)*
