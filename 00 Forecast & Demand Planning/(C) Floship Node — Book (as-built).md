---
tags: [demand-planning, floship, international, node-spec, as-built]
node: Floship (International)
brands: [MTB]
status: as-built-v1
updated: 2026-07-17
author: Claudian (with Tommy)
---

# Floship Node — Book (as-built)

> **What this is.** The as-built spec for `build_floship_book.py` — it reproduces
> Tommy's hand-built `BookFloship.xlsx` **as-is** (same 3 sheets), auto-generated
> from the raw Floship exports. Values are **hardwired/precomputed** so the data
> shows immediately (no Excel recalc needed). Floship is MTB's **international** 3PL
> (CN/HK). MTB-only, single view — no brand split.

```
python scripts\build_floship_book.py
→ outputs/YYYY-MM-DD/floship-book-YYYY-MM-DD.xlsx
```

## Sheets

1. **`Floship Orders `** *(trailing space)* — raw Floship orders export, plus a
   computed **Month** (`YYYY-MM` from Original transaction date) that the pivot
   matches on.
2. **`Sales by Month`** — two live blocks:
   - **Units Sold per Month by Item** — pivot: each SKU × month =
     `SUMIFS(Orders Total quantity, Item sku, Month)`. One row per inventory SKU +
     an **"Other (not in inventory)"** roll-up + a grand **Total** row.
   - **Inventory vs. Average Monthly Sales** — On Hand / Reserved (from the
     inventory sheet, Shenzhen warehouse, `AVERAGEIFS` to de-dupe) · Available ·
     **Months of Coverage** · **Status** (Reorder now <2mo / Low <3 / OK / Overstock
     >12 / No recent sales / Inactive) · **Avg Monthly Sales** (trailing **12
     complete months**, last partial month excluded) · **Need for Coverage** =
     `ROUNDUP(avg×12/365 × target-days, 0)` · **Incoming (in transit)** *(manual,
     yellow)* · **Order Qty** = `MAX(0, Need − Available − Incoming)`.
   - **Target coverage = 90 days** (Tommy 2026-07-17; `H26`). `Need` is hardwired at
     90d; **Order Qty** is a live formula, so typing an in-transit qty into the
     yellow **Incoming** cell updates the suggested buy. Rerun to change the 90d
     target. Aligning to 90d fixed the old gap where "Low" items (2–3 mo coverage)
     suggested **0** because the buy target was only 60 days.
3. **`floship Inventory`** — raw Floship inventory export (CN-Shenzhen /
   HK-YuenLong / HK-KwaiChung on-hand, Reserved, quarantine, dims, etc.).

## Notes / decisions

- **Hardwired values** (computed in Python, written as static values) — the book
  shows data immediately. *(Switched from live formulas: openpyxl can't write cached
  results, so the 30k-row SUMIFS pivot displayed blank until a manual Excel recalc.
  Precomputing fixes that — Tommy 2026-07-17.)* Only **Order Qty** stays a (simple)
  live formula off the value cells + editable `Incoming` (displays on open). Target
  coverage (`H26`=90) is a value — rerun to change it.
- **On Hand = Shenzhen only** (`Floship(CN)-Shenzhen`) — matches BookFloship; the HK
  warehouses are near-empty. De-duped via `AVERAGEIFS` (inventory export has Base
  Item + Master carton rows per SKU).
- **Incoming (in transit)** is a manual yellow input — the generator defaults it to
  0; type the in-transit qty in Excel and Order Qty reflows. *(This is the only
  thing that differs from a hand-filled BookFloship — validated: with Incoming
  matched, Order Qty is identical.)*
- **Avg Monthly Sales window** = trailing 12 complete months (excludes the current
  partial month), computed dynamically from the months present in the orders.
- Validated against BookFloship: pivot matches all SKUs; analysis block 93/95 cells
  exact (the 2 = manual Incoming, formula identical).

## Inputs — drop into `reports/_inbox` (auto-routed by content)

| Export | Detected by | Filed to |
|---|---|---|
| Floship **Orders** | `Item sku` + `Total quantity` | `reports/_data/floship/orders/` |
| Floship **Inventory** | `Floship(CN)-Shenzhen` (or `SKU`+`Reserved`+`Item ID`) | `reports/_data/floship/inventory/` |

Filenames need not be labelled. The router replaces the prior export of each type.
