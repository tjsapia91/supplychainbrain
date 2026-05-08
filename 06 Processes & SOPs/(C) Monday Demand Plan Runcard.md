# Monday Demand Plan Runcard — DEPRECATED

> ⚠️ **This document is deprecated as of May 4, 2026.** The workflow it described (single SoStocked "Multi-Dashboard Report" + 2-script pipeline) was replaced with a 5-script multi-source pipeline pulling from 8 systems.

---

## Use these instead

| What you need | Where to look |
|---|---|
| **One-page Monday checklist** | [[06 Processes & SOPs/(C) Weekly Analysis Cheat Sheet — 1 Page]] |
| **Step-by-step Monday recipe** | [[06 Processes & SOPs/(C) Weekly Analysis SOP — Step by Step]] |
| **Where every input file comes from** | [[06 Processes & SOPs/(C) Weekly Inputs Sourcing SOP]] |
| **This week's live runbook with checkboxes** | [[15 Meetings & Decisions/(C) Weekly Run Log — 2026-05-01]] |

---

## TL;DR — the new Monday flow

1. Pull **24 input files** from 8 source systems (SoStocked, Amazon SC, ShipBob, Walmart, Floship, Valogix, In-Transit Log, item master) into brand subfolders. **No renaming.**
2. Run 5 scripts:
   ```
   cd C:\Users\Tom Sapia\MTB-SupplyChain
   python scripts\combine_forecast.py
   python scripts\demand_planning.py
   python scripts\build_report.py
   python scripts\build_action_plan.py
   python scripts\build_shipment_tracking.py
   ```
3. Open `outputs\YYYY-MM-DD\weekly-report-YYYY-MM-DD.xlsx` (12 tabs).

Full detail in the SOP linked above.

---

*Deprecated: May 4, 2026 — superseded. Kept for history; do not follow.*
