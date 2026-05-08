# (C) Inventory & Demand Planning Analysis Project — Parked

> Larger project encompassing CA replenishment, demand methodology, and possible weekly-pipeline integration. **Parked** until we decide how (or whether) to fold it into the weekly cycle.
>
> **Captured:** May 5, 2026
> **Status:** PARKED — to revisit when ready
> **Trigger phrase to revisit:** *"Let's pick up the inventory & demand planning analysis project"*

---

## What this project covers

A standalone analysis effort to size:
1. **FBA Canada replenishment shipments** (units to send, cases, CBM, pallets)
2. **Supplier POs to Harry** (next manufacturing run sizing)

Currently lives outside the weekly US pipeline as a quarterly/ad-hoc workbook build. Question to answer later: should this be folded into the Monday weekly run, kept separate as a quarterly project, or rebuilt into something hybrid.

---

## Current assets

### Files
| Asset | Location |
|---|---|
| `CA_Plan_v10.xlsx` | SharePoint → Supply Chain → ANALYSIS WEEKLY INVENTORY REPORT |
| Methodology doc | [[00 Forecast & Demand Planning/(C) Canada Replenishment Plan — v10 Methodology]] |
| Working notes | (Claude session — local cache, may need re-import if revisited later) |

### What's in v10
- 18 SKUs across MTB / NFMD / SPA brands
- Replenishment Plan tab: 13,376 units · 14.4 pallets · ~33 CBM
- Harry PO tab: 23,768 units · ~150% of a 20' container

### Methodology highlights (full detail in linked doc)
- **13% × US fallback rule** for SKUs where SoStocked CA forecasts are empty
- Manual overrides (Soniclear White Marble Jul/Aug smoothed, 3 SKUs excluded)
- Yellow-flagged cells = estimated demand (replace when real CA forecasts publish)
- Formulas: `T = MAX(0, CEILING(R - (G+F), case_pack))` for FBA, PO auto-decrements based on FBA shipment

---

## Open questions to decide before revisiting

1. **Cadence** — weekly, monthly, quarterly, or ad-hoc when stockout risk surfaces?
2. **Integration** — separate workbook? Tab in `weekly-report.xlsx`? Standalone process?
3. **Demand source** — keep 13% rule, or pull real CA velocity from Amazon Seller Central CA reports once we standardize on those?
4. **Scope** — Canada only, or also international (Mexico, EU, etc.) under one roof?
5. **Output audience** — leadership, ops, supplier (Harry)? Different formats per audience?

---

## Possible directions (when we revisit)

### Direction A — Fold into the weekly pipeline
Add a `🍁 Canada Plan` tab to `weekly-report.xlsx` that:
- Pulls from the same SoStocked + ShipBob + Seller Central inputs we already use
- Auto-applies the 13% fallback rule
- Generates FBA shipment + Harry PO sizing each Monday

**Pros:** automated, always fresh, single source of truth
**Cons:** adds complexity to weekly run, CA data may not change weekly enough to justify

### Direction B — Keep as separate quarterly project
Leave `CA_Plan_vN.xlsx` as a standalone deliverable refreshed every 3 months when a new supplier PO is being scoped.

**Pros:** cleaner separation, doesn't bloat weekly cycle
**Cons:** manual refresh effort, methodology can drift between cycles

### Direction C — Hybrid
- Weekly pipeline tracks CA stockout risk only (DOS by SKU on the Amazon CA tab, currently missing)
- CA replenishment + Harry PO sizing stays standalone, triggered when one of the weekly DOS items hits CRITICAL on CA

### Direction D — Generalize to international
Build a multi-region module (CA / MX / EU / TikTok) with the same fallback logic, run on whatever cadence matches each region's data freshness.

---

## What's needed to revisit

When we pick this up:

1. **Read the methodology doc** to refresh on the 13% rule and override decisions
2. **Confirm SoStocked CA forecast freshness** — has any new data populated CA rows since May?
3. **Check if Amazon CA Seller Central data is now available** — would replace the 13% estimates
4. **Decide cadence + integration approach** (Directions A/B/C/D above)
5. **Pull latest source files** (SoStocked forecasts, ShipBob inventory, FBA CA inventory)

---

## To revisit

Type any of:
- *"Let's pick up the inventory & demand planning analysis project"*
- *"Open the parked CA replenishment project"*
- *"Revisit the Canada plan"*

Claude will read this doc + the methodology doc and pick up where we left off.

---

*Parked: May 5, 2026 — preserve until decision on integration is made*
