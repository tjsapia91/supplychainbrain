# Home
**Tommy's weekly starting point — updated after each demand plan run.**
Last demand plan: **April 20, 2026** | Next run: **April 27, 2026**

---

## Active Priorities

17 items need action as of April 20, 2026. Data source: SoStocked Multi-Dashboard (April 16 export).

| Product | Brand | Status | DOS | Vel/day | Lead Time |
|---------|-------|--------|-----|---------|-----------|
| Sonicsmooth 2.0 Lavender | MTB | TRUE STOCKOUT | 0 | 1.00 | 117d |
| Soniclear Body Brush Head | MTB | TRUE STOCKOUT | 0 | 1.07 | 117d |
| Viva Foot Replacement Heads | SS | TRUE STOCKOUT | 0 | 1.00 | 60d |
| NF Salt Packets (Spanish) | NFMD | CRITICAL | 3 | 2.17 | 117d |
| Sonicblend Replacement Head | MTB | CRITICAL | 24 | 0.87 | 117d |
| Sonicsmooth Pro+ Peach | MTB | CRITICAL | 34 | 23.42 | 61d |
| Echo Pink | SS | CRITICAL | 34 | 1.13 | 60d |
| MIO Diamond Tip Pink | SS | CRITICAL | 36 | 1.03 | 60d |
| Mattifying Potion | SS | CRITICAL | 42 | 4.10 | 60d |
| NOVA Serum Infusion Head | SS | CRITICAL | 57 | 0.30 | 60d |
| Sonicblend Display Cradle | MTB | CRITICAL | 70 | 1.23 | 117d |
| Soniclear Elite White Marble | MTB | CRITICAL | 70 | 75.76 | 117d |
| Soniclear Replacement Face Brush Plum | MTB | CRITICAL | 82 | 9.63 | 117d |
| Replacement Face Brush (Clarisonic compat) | MTB | CRITICAL | 96 | 0.50 | 117d |
| Sonicsmooth 2.0 White | MTB | CRITICAL | 101 | 30.23 | 117d |
| Sonicsmooth Pro+ White | MTB | CRITICAL | 103 | 78.54 | 117d |
| BioMist MD Steam Inhaler | NFMD | CRITICAL | 104 | 0.47 | 117d |

> Update this table after each weekly demand plan run.

---

## This Week

| | |
|--|--|
| Last demand plan run | April 20, 2026 |
| Next run | April 27, 2026 |
| Data source | SoStocked Multi-Dashboard |
| Script | `demand_planning.py` at `C:\Users\Tom Sapia\MTB-SupplyChain\` |
| Output | `outputs\demand-plan-2026-04-20.xlsx` |

---

## Active Projects

| Project | Status | Notes |
|---------|--------|-------|
| Demand Planning Script (demand_planning.py) | Running — v2 | Velocity fix applied Apr 20. HIGH tier bug still open. |
| SoStocked Regional Groupings Cleanup | In Progress | 22 grouping issues flagged |
| Inbound FBA Bug Fix | Pending | 46,129 units bleed causing 0 PO qty for ~10 CRITICAL items |
| Procurement ERP | Built, deployed | PythonAnywhere — POs, invoicing, Reports Hub planned |
| HIGH Tier Fix in demand_planning.py | Pending | 13 items missing from output |

---

## Quick Links

- [[01 Purchasing & Inventory/(C) PO Tracker|PO Tracker]]
- [[06 Processes & SOPs/(C) Demand Planning SOP|Demand Planning SOP]]
- [[06 Processes & SOPs/(C) PO Creation SOP|PO Creation SOP]]
- [[CLAUDE.md|CLAUDE.md — Session Memory]]
- [[03 3PL & Fulfillment/(C) 3PL Reference|3PL Reference]]
- [[02 Vendors & Suppliers/(C) Vendor Profile Template|Vendor Profile Template]]

---

## How to Use This Note

This is your snapshot, not a task manager. After each weekly demand plan run:

1. Replace the priorities table with the new output from `demand_planning.py`
2. Update "Last demand plan run" and "Next run" dates
3. Update Active Projects status if anything changed

The priorities table should reflect the current state of your 17 (or however many) flagged items — TRUE STOCKOUTs first, then CRITICAL, then HIGH. If an item gets resolved, remove it. If new items appear, add them.

If it's Monday morning and this table looks stale, run the demand plan before doing anything else.
