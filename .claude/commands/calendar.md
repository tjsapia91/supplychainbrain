---
description: Generate the day-by-day Inventory-Flow Calendar for a SKU (ShipBob + Amazon US + CA) — projected on-hand each day with PO arrivals marked by confidence tier.
argument-hint: "<SKU/UPC>  e.g. 811573031335   [--channel shipbob|us|ca|all]"
---

# /calendar — day-by-day inventory-flow calendar for a SKU

Build the Inventory-Flow Calendar for `$ARGUMENTS` and report where it landed.

## Run it
From the MTB-SupplyChain repo, run:

```
cd C:\Users\Tom Sapia\MTB-SupplyChain
py -3 -W ignore scripts\build_inventory_calendar.py $ARGUMENTS
```

- First token in `$ARGUMENTS` = the SKU/UPC (defaults to `811573031335` if none given).
- Optional `--channel shipbob|us|ca|all` (default `all` → one tab per channel).
- Output: `outputs/<today>/inventory-calendar-<upc>-<today>.xlsx`.

**If a report is open in Excel** the underlying planners can't refresh — but the calendar
reads the last generated report, so it still builds. If demand looks stale, tell Tom to close
the report and re-run the weekly build first.

## What it shows (explain briefly when reporting back)
- One tab per channel; a real month-by-month calendar (weeks × days).
- Each day cell = **projected on-hand on SHIPPED stock** (GREEN in stock · RED stocked out · GRAY past), plus the day's movement:
  **▼ units sold** · **▲ in-transit PO received (adds)** · **⧗ container-plan⚠ / open○ PO due (PENDING — not counted in the floor).**
- Hover a marked day for the PO#, qty, received date, and tier.

## Report back
Print the output path, the channels built, on-hand today per channel, and the key PO-landing
dates (with tier). Flag any RED (shipped-only stockout) stretch and which PENDING container
would rescue it. Note if a SKU has a `DEMAND_OVERRIDE` in `sku_rules` (so the number is Tom's
corrected demand, not the raw forecast).
