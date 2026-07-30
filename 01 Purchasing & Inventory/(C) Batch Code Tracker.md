---
type: batch-code-tracker
system-of-record: Prizm ERP (Reports → Generated Reports → Batch Code Tracking → CSV)
lookup-tool: OneDrive\Desktop\Web Apps\Batch Code Lookup.html (search the full Prizm export)
source: Outlook batch-code threads (Harry / Augusto / Michael)
last_scanned: 2026-07-30
status: living
---

# 🏷️ Batch Code Tracker

Batch/expiration codes matter for **Amazon compliance** (and retail). Full per-lot dataset lives in **Prizm** — search it with the local **Batch Code Lookup** web app (drop the Prizm CSV; search by batch code / item # / PPO # / region). This note holds the **conventions** + the **active batch-code decisions** the routine pulls from email.

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
| 7/30 | **EU order** (all boxes = **new print**) | new codes needed | 🟠 Harry needs the batch codes **shared with Juan** for the new-print boxes |
| 7/30 | **Regular salt** (current stock) | legacy code *(confirm)* | Stays on legacy until the **next batch** → then `RGS` + MMYY + 5-yr exp |
| 7/30 | **Xylitol salt** (current stock) | `NFMD03152026X` (legacy) | Stays on legacy until the **next batch** → then `XYS` + MMYY + 5-yr exp |
| 7/27 | New salt batches (both) | `RGS` / `XYS` + MMYY | New prefixes in effect once produced |

---
*Full lot-level data = Prizm export via the Batch Code Lookup web app. This note tracks the conventions + live decisions; the /email-brief routine surfaces batch-code coordination threads (Harry/Juan) and logs decisions here. (Tom 2026-07-30.)*
