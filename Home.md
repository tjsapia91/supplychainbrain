# Supply Chain Team Brain
**Michael Todd Beauty — MTB · SS · NFMD**
Last demand plan: **April 27, 2026** | Next run: **May 4, 2026**

---

## 🔴 Active Inventory Priorities

8 items need action as of April 27, 2026. Source: SoStocked + ShipBob/Floship via Valogix (April 27 export).

| Product | Brand | Market | Status | DOS | Vel/day | Lead Time |
|---------|-------|--------|--------|-----|---------|-----------|
| NERA Lavender | SS | US | 🚨 AMAZON STOCKOUT | 1430 | 1.29 | 60d |
| Sonicsmooth 1.0 White | MTB | CA | 🔴 TRUE STOCKOUT | 0 | 0.14 | 117d |
| Soniclear Body Brush Head | MTB | US | 🔴 TRUE STOCKOUT | 0 | 1.00 | 61d |
| NF Salt Packets (Spanish) | NFMD | US | 🔴 TRUE STOCKOUT | 0 | 1.62 | 117d |
| Sonicsmooth 2.0 Lavender | MTB | US | 🔴 CRITICAL | 2 | 1.00 | 117d |
| Sonicsmooth Pro+ Peach | MTB | US | 🔴 CRITICAL | 22 | 25.54 | 61d |
| Echo Pink | SS | US | 🔴 CRITICAL | 22 | 1.20 | 60d |
| Soniclear Face Brush Plum | MTB | US | 🔴 CRITICAL | 71 | 10.70 | 117d |

> Updated weekly after each Monday demand plan run. AMZ Stockouts first, then TRUE STOCKOUTs, then CRITICAL.

---

## This Week

| | |
|--|--|
| Last demand plan run | April 27, 2026 |
| Next run | May 4, 2026 |
| Data source | SoStocked (9 files — Forecast + Inventory + FvA per brand) |
| Script | `demand_planning.py` at `C:\Users\Tom Sapia\MTB-SupplyChain\` |
| Output | `outputs\demand-plan-2026-04-27.xlsx` |
| Summary | 8 priority · 5 high · 187 total · 85 forecast accuracy flags · 960K ShipBob units now counted |

---

## Active Projects

| Project | Owner | Status | Priority |
|---------|-------|--------|----------|
| [[Projects/Demand Planning Script/Overview\|Demand Planning Script]] | Tommy | In Progress | 🔴 High |
| [[Projects/HIGH Tier Fix/Overview\|HIGH Tier Fix — demand_planning.py]] | Tommy | Pending | 🔴 High |
| [[Projects/Inbound FBA Bug Fix/Overview\|Inbound FBA Bug Fix]] | Tommy | Pending | 🔴 High |
| [[Projects/Procurement ERP/Overview\|Procurement ERP]] | Tommy | In Progress | 🟡 Medium |
| [[Projects/SoStocked Groupings Cleanup/Overview\|SoStocked Groupings Cleanup]] | Tommy | In Progress | 🟡 Medium |
| [[Projects/Team Brain — SharePoint Migration/Overview\|Team Brain — SharePoint Migration]] | Tommy | Backlog | 🟡 Medium |

→ [[Projects/README|All Projects]]

---

## Quick Links

| | |
|--|--|
| [[01 Purchasing & Inventory/(C) PO Tracker\|PO Tracker]] | [[06 Processes & SOPs/(C) Demand Planning SOP\|Demand Planning SOP]] |
| [[06 Processes & SOPs/(C) PO Creation SOP\|PO Creation SOP]] | [[03 3PL & Fulfillment/(C) 3PL Reference\|3PL Reference]] |
| [[02 Vendors & Suppliers/(C) Vendor Profile Template\|Vendor Profile Template]] | [[CLAUDE.md\|CLAUDE.md — Session Memory]] |

---

## How This Brain Works

**For the team:**
- [[Projects/README|Projects folder]] — where active work lives. Each project has an Overview, per-person task files, and a decision Log.
- [[06 Processes & SOPs|Processes & SOPs]] — how we do things. Read before you do it a new way.
- [[02 Vendors & Suppliers|Vendors & Suppliers]] — vendor contacts, lead times, profiles.
- [[01 Purchasing & Inventory/(C) PO Tracker|PO Tracker]] — all open and closed POs.

**For Tommy (weekly demand plan):**
→ [[06 Processes & SOPs/(C) Monday Demand Plan Runcard|Monday Demand Plan Runcard]] — follow this every Monday morning

**For new team members:**
Start with [[06 Processes & SOPs/(C) Demand Planning SOP|Demand Planning SOP]] and [[06 Processes & SOPs/(C) PO Creation SOP|PO Creation SOP]]. Then open the project folder for whatever you're working on.
