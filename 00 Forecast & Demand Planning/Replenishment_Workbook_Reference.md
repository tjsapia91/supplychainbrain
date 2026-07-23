# Amazon Demand & Replenishment Plan — Workbook Reference

_Documentation of structure, formulas, styling, and business logic._
_Source workbook: `Supply Chain - Documents/Demand Planning/Weekly Analysis/7-17-26-AMZ-Demand-ReplenPlan.xlsx` (Tommy's hand-built master)._

## 1. Purpose
Forecasts monthly demand vs. supply for Amazon FBA SKUs across three brand tabs (MTB, SPA, NFMD) and flags when each SKU will run out, factoring on-hand inventory, warehouse stock, and incoming POs (on the water + planned). Horizon: Jul 2026 – Feb 2027 (8 months, columns D–K).

## 2. Tabs
| Tab | Role |
|---|---|
| MTB / SPA / NFMD | Planning tabs (one row per SKU): demand, inventory, coverage map, run-out, projection. |
| FBA | Amazon FBA inventory report (by ASIN) — on-hand + inbound. |
| AWD | Amazon Warehousing & Distribution inventory (by ASIN). |
| container plan | Planned POs / containers (by UPC) with Load Dates. |
| In Transit | Containers on the water (by UPC), actual delivery dates. Hosts the consolidated calc block, tie-out, and UPC map. |
| Open POs | Open purchase orders (by PO# / Item No.) with remaining open qty. |
| Unis | Unis 3PL on-hand, by Item ID (UPC); column G = units. |
| shipbob | ShipBob 3PL; col I = "FREE to Transfer → Amazon", col J = Amazon ASIN. |
| sku map / BAse | Lookup helpers (SKU→UPC, SKU→description). |

## 3. Planning-tab columns (MTB / SPA / NFMD)
| Col | Header | Meaning |
|---|---|---|
| A | ASIN | Match key for FBA/AWD. |
| B | SKU | Seller SKU. |
| C | Desc | VLOOKUP from BAse. |
| D–K | Jul 2026 … Feb 2027 | Monthly demand forecast + the color coverage map. |
| L | Total Forecast | =SUM(D:K). |
| M | Total Inventory | FBA + AWD on-hand (excludes Unis). |
| N | Unis | Unis 3PL on-hand for this SKU. |
| O | Run Out (phased) | First uncovered month. |
| P | Match UPC | UPC used to match POs. |
| Q | Incoming (In Transit + Plan) | UNIS/AMZ-bound inbound units. |
| R | PO Remaining Open Qty | Container-plan units with no Load Date yet. |
| S | Next Arrival | Earliest scheduled arrival. |
| T | Next PO# | PO# of next arrival. |
| U | Last Arrival | Latest scheduled arrival. |

Helper columns: AF:AM cumulative arrivals by month; AO:AV status codes 1–4; AX:BE per-month uncovered flags.

## 4. Core formulas (row 2; fill down)

**Total Inventory — M**
```
=SUMIF(FBA!$D:$D,$A2,FBA!$BC:$BC)   'FBA Inbound
+SUMIF(FBA!$D:$D,$A2,FBA!$G:$G)     'FBA available
+SUMIF(FBA!$D:$D,$A2,FBA!$H:$H)     'FBA fc-transfer
+SUMIF(FBA!$D:$D,$A2,FBA!$CN:$CN)   'FBA Reserved Staging
+SUMIF(FBA!$D:$D,$A2,FBA!$CL:$CL)   'FBA Reserved FC Processing
+SUMIF(AWD!$D:$D,$A2,AWD!$G:$G)     'AWD available
+SUMIF(AWD!$D:$D,$A2,AWD!$M:$M)     'AWD reserved
```
Excludes: Unis (in N), FBA Customer-Order reserved, and AWD Outbound-to-FBA (already counted as FBA Inbound).

**Unis — N**
```
=SUMPRODUCT((TEXT(Unis!$B$2:$B$20,"0")=TEXT($B2,"0"))*Unis!$G$2:$G$20)
```

**Match UPC — P**
```
MTB:  =IFERROR(--$B2,IFERROR(INDEX('sku map'!$A$100:$A$166,MATCH($B2,'sku map'!$B$100:$B$166,0)),""))
NFMD: =IFERROR(--$B2,IFERROR(--LEFT($B2,12),""))
SPA:  =IFERROR(VLOOKUP(IFERROR(--$B2,IFERROR(--LEFT($B2,12),"")),'In Transit'!$AT:$AU,2,FALSE),IFERROR(--$B2,IFERROR(--LEFT($B2,12),"")))
```

**Incoming (In Transit + Plan) — Q**
```
=IF($P2="","",SUMIFS('In Transit'!$Z$2:$Z$175,'In Transit'!$Y$2:$Y$175,$P2,'In Transit'!$AC$2:$AC$175,1))
```

**PO Remaining Open Qty — R** (undated container-plan units)
```
=IF($P2="","",SUMIFS('container plan'!$G$2:$G$73,'container plan'!$C$2:$C$73,$P2)
             -SUMIFS('container plan'!$G$2:$G$73,'container plan'!$C$2:$C$73,$P2,'container plan'!$L$2:$L$73,">0"))
```

**Next / Last Arrival, Next PO# — S / U / T** — MINIFS / MAXIFS / INDEX-MATCH over In Transit consolidated Y/Z/AA/AB/AC ($2:$175).

**Cumulative arrivals by month — AF:AM** (ONE-MONTH LEAD)
```
=SUMIFS('In Transit'!$Z$2:$Z$175,'In Transit'!$Y$2:$Y$175,$P2,'In Transit'!$AC$2:$AC$175,1,'In Transit'!$AA$2:$AA$175,"<"&AF$1)
```
AF$1..AM$1 = first-of-month Jul…Feb. A PO counts toward a month only if it landed before that month begins (arrival in month X covers X+1).

**Uncovered flags — AX:BE** (credit Total Inventory + Unis)
```
=--(SUM($D2:<monthEnd>2) > ($M2+$N2) + <cumArrivalForMonth>)
```

**Status codes — AO:AV**
```
=IF(<flag>=0, IF(SUM($D2:<monthEnd>2)<=($M2+$N2),1,2), IF(SUM($AX2:<flag>)=1,3,4))
```
1 = covered by on-hand; 2 = covered with POs; 3 = first short month; 4 = short after.

**Run Out (phased) — O**
```
=IFERROR(INDEX($D$1:$K$1,MATCH(1,$AX2:$BE2,0)),"Covered")
```

**D–K color map (conditional formatting):** =AO2=1 → #63BE7B (dark green); =AO2=2 → #C6EFCE (light green); =AO2=3 → #ED7D31 (orange); =AO2=4 → #F8696B (red).

## 5. In Transit consolidated block (Y:AC)
- Rows 2–101 (In Transit mirror): Y=UPC(G), Z=qty(I), AA=delivery date(S), AB=PO#(B), AC=include(W).
- Rows 103–175 (container-plan mirror): Y=cp!C, Z=cp!G, AA=IF(cp!L="","",cp!L+TransitDays), AB=cp!B, AC=--((cp!E="UNIS")*(cp!Q=0)).
- In Transit col W (include): =IF(OR($U2="UNIS",$U2="AMZ"),1,0).
- container plan col Q (supersede): =--(COUNTIFS('In Transit'!$B:$B,$B2,'In Transit'!$G:$G,$C2)>0).
- TransitDays (defined name) = MTB!$E$22 = 45 days. Container-plan arrival = Load Date + 45; In Transit lines use actual delivery date (col S).

## 6. Inventory Projection (below each main table)
1:1 mirror of the main table. Ranges shift as SKUs change (approx. MTB 26–44, SPA 67–127, NFMD 22–37).
- Start balance: =M{x}+N{x}+AF{x}-D{x}  (Total Inventory + Unis + arrivals − demand).
- Running: prior + arrivals-this-month − demand.
- L Stockout Date; M/O/P "Cover thru Oct/Jan/Feb"; Q Unis; R ShipBob (=SUMIF(shipbob!$J:$J,$A{row},shipbob!$I:$I)); S Replen From (UNIS/ShipBob/—).
- Dynamic CF: positive → green, negative → red; cover cols → orange when > 0.

## 7. UPC-bridge map (In Transit AT:AV)
| Amazon UPC | PO UPC | Product |
|---|---|---|
| 850038082444 | 850003115634 | AIVA – Black |

SPA Match UPC consults this before its normal logic. Add a row to bridge a new mismatch.

## 8. Tie-out (In Transit AL:AR)
Per PO#: Open PO Rem. vs (In Transit + non-superseded Plan) → Diff → OK/CHECK. CHECK flags data mismatches to reconcile.

## 9. Business rules
1. Total Inventory excludes Unis; coverage map credits Total Inventory + Unis.
2. One-month receiving lead (PO must land before a month starts to help cover it).
3. AWD Outbound-to-FBA not added (already counted as FBA Inbound).
4. Transit = 45 days from container-plan Load Date.
5. Only UNIS/AMZ-bound incoming counts for Amazon coverage.
6. Supersede: a PO+UPC on the water suppresses its container-plan copy.
7. UPC mismatches bridged via the §7 map.
8. Next/Last Arrival comments are static snapshots; regenerate after data changes.

## 10. Maintenance
- Adding/removing SKU rows shifts the projection; keep it a 1:1 mirror.
- After updating source tabs, formulas recalc automatically; only arrival comments need regenerating.
- Watch the shipbob "FREE to Transfer" (col I): its Reserved (col H) has a circular reference (H → $H$3) that can zero the column.
- Save frequently.

## 11. Styling & Formatting

**Global**
- Font: Calibri, size 12, black (#000000) throughout.
- All three planning tabs (MTB / SPA / NFMD) share identical styling.
- No AutoFilter dropdowns on the planning tabs.

**Header row (row 1):** bold, center-aligned, size 12, no fill, row height ≈ 47 pt (headers wrap).

**Column widths:** row-label/summary columns wide — A (ASIN) ≈ 83, C (Desc) wide, M (Total Inventory) ≈ 130; month columns D–K narrow/uniform ≈ 49.

**Number formats**
- Total Forecast (L), Total Inventory (M), Unis (N), Incoming (Q), PO Remaining (R): `#,##0`.
- Dates — Next Arrival (S), Last Arrival (U), Stockout Date: `m/d/yyyy`.
- Demand months (D–K): `General`.
- Match UPC (P), Next PO# (T): integer `0`.

**Run Out column (O):** solid yellow fill `#FFFF00` on data cells.

**Coverage map — D–K conditional formatting** (from status codes AO:AV)
| Status | Meaning | Fill |
|---|---|---|
| 1 | covered by on-hand | dark green `#63BE7B` |
| 2 | covered with incoming POs | light green `#C6EFCE` |
| 3 | first short month | orange `#ED7D31` |
| 4 | short thereafter | red `#F8696B` |

**Projection map — D–K conditional formatting:** positive balance → green `#63BE7B`; negative → red `#F8696B`; cover columns (M/O/P) → orange `#ED7D31` when > 0.

**Tie-out Status (In Transit AR):** `CHECK` → light-red fill `#FFC7CE` + dark-red font `#9C0006`; `OK` → green font `#006100`.

**Helper columns (AF:AM, AO:AV, AX:BE):** plain/unstyled — calculation engine, not display.

**Comments / notes:** M1 documents the Total Inventory formula; the transit-days cell has a note on the 45-day assumption; Next/Last Arrival (S/U) cells carry per-SKU arrival comments (PO# + qty, static snapshots).
