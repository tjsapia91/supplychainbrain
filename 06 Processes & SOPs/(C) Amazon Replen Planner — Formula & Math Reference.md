---
title: Amazon Replen Planner — Formula & Math Reference
created: 2026-07-27
tags: [sop, reference, amazon, replenishment, planner, formulas]
brands: [MTB, SS, NFMD]
---

# Amazon Replen Planner — Formula & Math Reference

Plain-English explanation of every formula in the **legacy formula-driven** Amazon
planner (`build_amazon_replen.py`). Captured 2026-07-27 **before** rebuilding Amazon
US in the Python-computed (ShipBob-model) layout, so the math is preserved and
defensible if anyone asks how a number is derived.

> **Why we're moving off these formulas:** they depend on exact export **column
> letters** (FBA `BC/CN/CL`, AWD `M`, …). When Amazon shifts a column, the formula
> silently reads the wrong cell. The rebuild computes each term explicitly in Python
> and writes values, so nothing is hidden and nothing drifts. This doc is the record
> of what the old formulas meant.

---

## Brand-tab columns (MTB / SPA / NFMD)

### Col C — Description
```
=IFERROR(VLOOKUP($B2,BAse!$A:$B,2,0),
  IFERROR(VLOOKUP(--$B2,BAse!$A:$B,2,0),
  IFERROR(VLOOKUP(--LEFT($B2,12),BAse!$A:$B,2,0),"")))
```
**Math:** look up the SKU in the `BAse` item-master tab and return its description.
Tries three ways so it matches regardless of how the SKU is stored: (1) the SKU as
text, (2) the SKU forced to a number (`--`), (3) the first 12 chars forced to a number
(strips Amazon suffixes like `-FBA`). First hit wins; blank if none.

### Cols D:K — Monthly demand (8 months)
Written as **values** from SoStocked's "Forecasted Sales Monthly" (US marketplace),
per SKU per month. Not a formula. This is the demand of record for Amazon US.

### Col L — Total Forecast
```
=SUM(D2:K2)
```
**Math:** sum of the 8 monthly demand figures. The total units Amazon is forecast to
sell across the horizon.

### Col M — Total Inventory (the on-hand position) ✎ editable
```
=SUMIF(FBA!$D:$D,$A2,FBA!$BC:$BC)   ← inbound-working
+SUMIF(FBA!$D:$D,$A2,FBA!$G:$G)     ← available
+SUMIF(FBA!$D:$D,$A2,FBA!$H:$H)     ← pending-removal-quantity  ⚠
+SUMIF(FBA!$D:$D,$A2,FBA!$CN:$CN)   ← Reserved Staging
+SUMIF(FBA!$D:$D,$A2,FBA!$CL:$CL)   ← Reserved FC Processing
+SUMIF(AWD!$D:$D,$A2,AWD!$G:$G)     ← Available in AWD
+SUMIF(AWD!$D:$D,$A2,AWD!$M:$M)     ← Reserved in AWD
```
**Math:** for this row's ASIN (`$A2`), sum the matching rows in the `FBA` and `AWD`
data tabs across seven inventory buckets — everything Amazon physically holds or has
committed at its network:

| Term | Field | Meaning |
|---|---|---|
| available | sellable now at FBA | ready to ship to customers |
| inbound-working | units in an inbound plan, not yet shipped | pipeline into FBA |
| Reserved Staging | held for an FC transfer | Amazon moving it between FCs |
| Reserved FC Processing | being processed at an FC | check-in / restow |
| Available in AWD | Amazon Warehousing & Distribution on-hand | upstream Amazon storage |
| Reserved in AWD | committed in AWD | earmarked upstream |
| **pending-removal-quantity** ⚠ | units flagged for removal/disposal | **see flag below** |

> ⚠ **Flag (Tommy 2026-07-27):** term `H` is **pending-removal-quantity** — inventory
> Amazon is about to remove (return/dispose), which arguably should NOT count as
> on-hand. The old SOP mislabeled this term "fc-transfer." The Python rebuild will
> make this an explicit, named choice (include or drop). Decision pending.

Editable (cream fill): overwrite the cell to override the position and every
downstream number recalculates.

### Col N — Unis (US staging)
```
=SUMPRODUCT((TEXT(Unis!$B$2:$B$20,"0")=TEXT($B2,"0"))*Unis!$G$2:$G$20)
```
**Math:** sum the `Current Qty` (col G) of every `Unis` staging row whose Item ID
(col B) equals this row's SKU. `TEXT(...,"0")` on both sides forces a text-vs-text
match so a numeric UPC and a text SKU still line up. Unis = the US staging warehouse
(Alessandro) that feeds Amazon FBA via a ~60-day send-in.

### Col O — Run Out (phased)
```
=IFERROR(INDEX($D$1:$K$1,MATCH(1,$BX2:$CE2,0)),"Covered")
```
**Math:** scan the hidden monthly "uncovered flag" cells (`BX:CE`, one per month);
`MATCH(1,…,0)` finds the FIRST month flagged uncovered (=1); `INDEX($D$1:$K$1,…)`
returns that month's label. If none are uncovered → "Covered". I.e. the first month
the item runs short.

### Col P — Match UPC
Resolves the listing SKU to its canonical SAP UPC so the arrival/PO lookups join
correctly. Per brand:
- **MTB:** `=IFERROR(--$B2, INDEX('sku map'!$A$100:$A$166, MATCH($B2,'sku map'!$B$100:$B$166,0)))` — use the SKU as a number, else look it up in the sku-map reverse region.
- **NFMD:** `=IFERROR(--$B2, --LEFT($B2,12))` — SKU as number, else first 12 digits.
- **SPA/other:** VLOOKUP against the In-Transit UPC bridge (`AT:AU`), else the SKU/first-12.

### Col Q — Incoming (In Transit + Plan)
```
=IF($P2="","",SUMIFS('In Transit'!$Z$2:$Z$n,'In Transit'!$Y$2:$Y$n,$P2,'In Transit'!$AC$2:$AC$n,1))
```
**Math:** sum the Qty (col Z) of every row in the In-Transit **consolidated block**
whose UPC (col Y) matches this row's Match-UPC **and** whose Include flag (col AC) = 1.
The consolidated block merges the In-Transit Log (Amazon/UNIS-bound) with the
container-plan mirror, so this is total units on the way to Amazon.

### Col R — PO Remaining Open Qty
```
=IF($P2="","",SUMIFS('container plan'!$G,'container plan'!$C,$P2)
             -SUMIFS('container plan'!$G,'container plan'!$C,$P2,'container plan'!$L,">0"))
```
**Math:** container-plan units for this UPC, **minus** the units whose supersede flag
(col L) is >0 (already on the water / counted in In-Transit). Nets out double-counting
so you see only PO units not yet in transit.

### Cols S / U — Next Arrival / Last Arrival
```
S: =IF($P2="","",IF(MINIFS(...AA..., ...Y...=$P2, ...AC...=1, ...AA...>0)=0,"",MINIFS(...)))
U: =IF($P2="","",IF(MAXIFS(...AA..., ...Y...=$P2, ...AC...=1)=0,"",MAXIFS(...)))
```
**Math:** over the consolidated block, `MINIFS`/`MAXIFS` return the **earliest** and
**latest** arrival date (col AA) among rows matching this UPC with Include=1. Next
Arrival = when the next PO lands; Last Arrival = when the final open PO lands.

### Col T — Next PO#
Array formula: finds the PO# (col AB) of the row whose arrival date equals Next Arrival
(col S) for this UPC. I.e. "which PO is the next to land."

---

## The coverage engine (half-month blocks)

The horizon is split into **16 half-month buckets** (1st–15th, 16th–end of each of 8
months). Two hidden mechanics drive everything:

### Receiving lag (14 days)
A PO helps a half-month only if it lands **before that half begins, minus 14 days** of
dock-to-sellable putaway. So a PO arriving 7/29 (+14d = 8/12) first credits coverage
from the **Aug 16+** bucket, not Aug 1. This prevents crediting stock that hasn't been
checked in yet.

### Half-month cumulative arrivals (hidden helper, HCOL)
```
=SUMIFS('In Transit'!$Z, 'In Transit'!$Y,$P2, 'In Transit'!$AC,1, 'In Transit'!$AA,"<"&<bucket-start − 14d>)
```
**Math:** running total of all PO units that have become sellable before each bucket's
(start − 14-day lag). Both blocks below are built off this.

### Block A — Projected inventory (½-month)
```
=$M2 + $N2 + <half-cumulative arrivals so far> − <demand consumed so far>
```
**Math:** starting position (Total Inventory `M` + Unis staging `N`), **plus** the PO
units that have landed by this half, **minus** demand consumed to date. Demand is split
50/50 across each month's two halves; the **current** month is prorated to the days
left as of the "Report as-of" date (see below). If the result is **< 0**, that half runs
short (colored red).

### Block B — PO arriving (½-month)
```
= <half-cumulative at b+1> − <half-cumulative at b>
```
**Math:** the delta of the running cumulative between consecutive halves = the units
that become sellable **in** that specific half. Shows when each PO lands.

### Current-month proration (the live "Report as-of" date)
```
DIM  = DAY(EOMONTH(asof,0))                 ← days in the current month
H1   = MAX(0,15−DAY(asof)) / DIM            ← fraction of the 1st half still ahead
REM  = MAX(0, DIM−DAY(asof)) / DIM          ← fraction of the whole month still ahead
```
**Math:** only the **remaining** portion of the current month's demand is subtracted,
based on today's date. Edit the yellow "Report as-of" cell and the whole map
re-forecasts — e.g. on the 24th of a 31-day month, only 7/31 of the month's demand is
still ahead.

### Status codes + coverage colors (hidden helpers)
- **Uncovered flag** (per month): `=--(SUM(demand to date) > (M + N + arrivals to date))` → 1 if cumulative demand exceeds cumulative supply.
- **Status code** (per month): 1 = green (fully covered by on-hand), 2 = light-green (covered with arrivals), 3 = orange (first uncovered month), 4 = red (uncovered thereafter). Drives the D:K color band.

---

## Inventory Projection block (bottom of each tab)

### Stockout Date
```
{=IF(N=0,"Covered", <month start of first negative> + (fractional day within that month))}
```
**Math:** `N` = the first month index whose end-balance goes negative (array `MATCH` of
the first `<0`). The exact date is that month's start plus the fraction of the month
consumed before hitting zero: `(balance + demand)/demand × days-in-month`. "Covered" if
never negative.

### Send-in to cover thru {month}
```
=MAX(0, −MIN(running balance from now through the checkpoint month))
```
**Math:** the deepest the running balance goes **negative** through that checkpoint =
the units you must **send in** (transfer from staging) so it never drops below zero.
Three checkpoints (≈ +3 mo, +6 mo, end-of-horizon). Zero if already covered.

### Unis / ShipBob / Replen From
- **Unis** = `=N{row}` — the staging figure carried down.
- **ShipBob** = `=SUMIF(shipbob!$J, ASIN, shipbob!$I)` — ShipBob FREE-to-transfer units for this ASIN (US: primary send-in source; also the CA cross-border emergency backup).
- **Replen From** = `=IF(Unis>0,"UNIS",IF(ShipBob>0,"ShipBob","—"))` — where to pull the send-in from.

---

## Transit / timing constants
| Constant | Value | Meaning |
|---|---|---|
| Transit | 45 d | container Load Date → at warehouse |
| Ready→Load | 10 d | if no Load Date yet, assume it loads Ready + 10 |
| Receiving lag | 14 d | dock → sellable (putaway) |
| Staging→Amazon | 60 d | ShipBob (US) / Alliance (CA) transfer into FBA |
| Supplier lead | 140 d | new ocean PO door-to-door |

Container-plan ETA = `Load + 45`; if no Load Date, `Ready + 10 + 45`.

---

## Migration note
The Python rebuild (ShipBob model) reproduces each number above **as an explicit
Python calculation**, then writes the value — keeping only the coverage-map and
projection cells as formulas (so the as-of date still re-forecasts live). The
`pending-removal-quantity` term (⚠ above) becomes an explicit, documented include/drop
decision rather than a hidden column reference.
