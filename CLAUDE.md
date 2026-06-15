# SupplyChainBrain
Tommy's operational brain for Supply Chain Manager at Michael Todd Beauty — $80M beauty company, 3 brands, multi-channel. Built to organize chaos and make Claude an effective supply chain thinking partner.

GitHub (private): https://github.com/tjsapia91/supplychainbrain
Syncs between: Personal machine (Obsidian vault) ↔ Work machine (Claude Code)

## ⚠️ SESSION SYNC RULE
At the end of every session: update Current Status, commit, push. This file IS the shared memory between machines.
```
git add . && git commit -m "description" && git push origin main
```
On the other machine: `git pull` to receive updates.

---

## Claude's Role
Operations partner — analyst, strategist, tool builder.
- **Demand planning** — analyze forecasts, spot trends, flag risks across brands/channels
- **Process builder** — document and improve SOPs
- **Tool builder** — reduce screens Tommy needs to look at
- **Strategic thinker** — vendor decisions, 3PL transitions, international expansion
- **Knowledge capture** — document what's being learned

If a session drifts without moving toward clearer operations: *"What's the one thing that moves the supply chain forward today?"*

---

## The Company
**Michael Todd Beauty** — $80M/yr beauty. 3 brands:
- **MTB** (Michael Todd Beauty) — flagship
- **NFMD** (NasalFresh MD) — nasal/health
- **SS** (Spa Sciences) — spa/beauty

Each brand: separate Amazon login, products, forecasts.

**Channels:** Amazon (per-brand), Walmart Marketplace, TikTok Shop, Shopify, Nordstrom
**3PLs:** ShipBob (primary), Floship (international), Alliance (CA staging)
**Tools:** SAP (ERP), SoStocked, Sellerboard, Valogix, TrueOps, Excel, Claude

---

## Team
- **Tommy** — SCM (#2 on team)
- Director of Supply Chain (boss)
- SVP of Operations (senior leadership)

## What Tommy Manages
Purchasing · Inventory · Freight · Forecast/Demand Planning · 3PL Relationships

---

## Folder Structure
```
SupplyChainBrain/
├── 00 Forecast & Demand Planning/    (per brand: MTB/NFMD/SS)
├── 01 Purchasing & Inventory/        (POs, reorder points)
├── 02 Vendors & Suppliers/           (profiles, lead times)
├── 03 3PL & Fulfillment/             (ShipBob, Floship, etc.)
├── 04 Sales Channels/                (Amazon, Walmart, TikTok, Shopify)
├── 05 International Expansion/
├── 06 Processes & SOPs/              (the good stuff)
├── 07 AI Tools & Builds/             (build plans, parked projects)
├── 08 Key Metrics & Dashboards/
├── 09 People & Relationships/
├── 10 System/                        (architecture, sync)
├── 11 Skills/                        (reusable scripts as MD)
├── 12 Attachments/
├── 13 Iteration Logs/
├── 14 Learning & Development/
└── 15 Meetings & Decisions/          (incl. Daily Action Plans)
```

---

## Rules & Conventions
- **(C) prefix** — files created by Claude. Ask permission before editing non-(C) files.
- **Work in small steps.** No walls of information.
- **Be blunt.** Call out inefficient processes.
- **Brand abbreviations:** MTB, NFMD, SS
- **Skills** are markdown files in the Skills folder, NOT Claude Code skills.

### 🔁 Always-Update Rule (Tommy 2026-06-08)
**When a change ships AND is confirmed, immediately update the relevant docs in the same session — don't defer.** No more "we'll catch up later." Docs lag = audit pain.

When a code/process change is confirmed:
- New/changed tab in weekly report → update Weekly Analysis SOP + Cheat Sheet
- New ranking / decision logic → update ABC Classification Reference + Cheat Sheet decision rules
- New pipeline script or workflow change → update CLAUDE.md Current Status + relevant SOP
- New parked build plan → add to CLAUDE.md "Parked Build Plans" list
- Phase of a build plan ships → mark that phase ✅ SHIPPED in the build plan doc (don't leave "PARKED" on shipped work)
- New auto-classification rule in `sort_downloads.py` → update Weekly Inputs Sourcing SOP

This is operator discipline, not bureaucracy. If you don't update on the day, you'll spend 30+ minutes hunting stale references later.

---

## Architecture (Three Layers)
| Layer | Path | Purpose |
|---|---|---|
| Knowledge | `C:\Users\Tom Sapia\supplychainbrain\` (this vault) | SOPs, planning docs, weekly snapshots |
| Execution | `C:\Users\Tom Sapia\MTB-SupplyChain\` | Scripts, raw data, output reports |
| Procurement | Django ERP (planned) | POs, invoicing, Reports Hub |

---

## Weekly Workflow (Simplified)
Three steps:
1. **Download every report → `Downloads\`** (no manual sorting needed)
2. **Run the pipeline:**
   ```
   cd C:\Users\Tom Sapia\MTB-SupplyChain
   python scripts\demand_planning.py
   python scripts\build_report.py
   ```
3. **Open:** `outputs/latest/weekly-report-*.xlsx`

`build_report.py` auto-classifies Downloads via `sort_downloads.py`, then chains: demand plan → report → velocity watch → order list → deep plan.

---

## Key Scripts (`MTB-SupplyChain/scripts/`)
- **`demand_planning.py`** — SoStocked → demand-plan JSON (Amazon side)
- **`build_report.py`** — main pipeline + Excel dashboard (~19 tabs)
- **`build_deep_plan.py`** — 7-stage multi-echelon workflow library; standalone for Tier-3 deep dives
- **`build_order_list.py`** — "do I have 180d coverage?" supplier POs + staging transfers
- **`build_velocity_watch.py`** — Top-40 SKU velocity monitor (2-day cadence)
- **`sort_downloads.py`** — auto-classifier (pre-flight)
- **`build_shipment_tracking.py`** — shipment audit (containers/AWD/FBA)

---

## Weekly Report Tabs
1. **✅ THIS WEEK** — 5 action sections (ORDER · EXPEDITE · TRANSFER · SUPPLY RISK · WATCH)
2. **Amazon US/CA/UK/AU/EU** — per-marketplace flat list
3. **ShipBob / Walmart / TikTok / Floship Intl** — non-Amazon channels
4. **📋 SAP Open POs** — every open PO + same-day-error flag
5. **📦 In Transit** — active shipments from suppliers (WATER/AIR/TRUCK)
6. **🏭 PO Priority** — vendor-ranked manufacturing priority list
7. **🏷 Bundles & Custom SKUs** · **🗑 Phase-Out, Obsolete & BOMs**
8. **📈 Forecast Pivot** · **📊 Amazon Sales History** · **📈 Amazon FvA** · **📊 Sales Anomalies**

---

## Key Concepts
- **ABC Classification** (6 codes): A/B/C/D/E/Z. F/I/S are non-standard.
- **Urgency Tiers** (days-first ranking):
  - 🔴 OVERDUE (<0d) · 🔴 CRITICAL (≤30d) · 🟠 HIGH (≤90d) · 🟡 MEDIUM (≤180d) · 🟢 HEALTHY (>180d) · ⚪ NO DATA
- **Supplier Lead Time:** 140d door-to-door (production + ocean + customs + receiving). Floor in build_report.
- **Staging-to-Amazon LT:** 60d (SB→US + Alliance→CA).
- **Velocity sources:**
  - Amazon US: Sellerboard 90-day Monthly
  - Amazon CA: Sellerboard CA Dashboard (requires `amazon.ca` marketplace filter)
  - Shopify/Walmart-SS/Floship: Valogix last 90 days actual
  - Walmart NFMD: Walmart Seller Center daily units sold
  - TikTok: SAP wholesale receipts (Valogix significantly underestimates)

---

## Critical Gotchas (still apply)
- **SoStocked Adj. Velocity is in units/day.** Do NOT divide by 30.
- **CA AWD inbound is ASIN-level** — applied to both US and CA rows; may slightly inflate CA DOS.
- **TikTok forecast in Valogix undercounts by ~3-4×** vs actual TikTok Shop wholesale receipts.
- **SAP same-day PO errors** (posting = due date) are endemic. SUPPLY RISK section catches landings within 90d.
- **In-Transit Log is source of truth** for what's shipped vs SAP "open" — subtract before flagging supply risk.

---

## Current Status
**Last updated:** June 15, 2026

**Recent work (Jun 15):**
- ✅ **THIS WEEK ORDER section — 6 fixes shipped (Jun 15)** — operator-supplied fix brief implemented end-to-end. Touched `build_report.py`, `build_order_list.py`, `build_deep_plan.py`, `sort_downloads.py`.
  - **FIX 0 — Stale-extract gate.** `build_report.py main()` now aborts with a clear message when `all_items < 150` OR forecast-bearing items < 50%. Refuses to overwrite the last good `weekly-report-*.xlsx`. Operator override: `set FORCE_BUILD=1`. Caught Jun 15's degraded 109-item JSON.
  - **FIX 1 — Chronological sort.** ORDER rows now carry a real `stockout_date` (date object); both engine outputs (`build_order_list` Amazon-direct + SB PO Engine) are re-merged + re-sorted in `build_report` so the most urgent item appears at row 1. Previously sorted on the display string (`"Aug" < "Dec" < "Jul" < "Jun"`) — buried SonicSmooth Pink (stockout = today) at row 13.
  - **FIX 2 — Phase-out / combo-kit guard.** New `PHASE_OUT_UPCS = {"850003115139"}` in `build_order_list.py` + keyword catch (`"phase out"`, `"combo kit"`). Applied in BOTH order engines. MIO Green+White Combo Kit no longer auto-orders 10,000 units — kits get assembled against retailer orders only.
  - **FIX 3 — Interim warning.** New `SUPPLIER_LEAD_FLOOR = 140` constant. When current-pace stockout < lead time, ORDER row gets prepended: *"⚠ Stocks out before a new PO can land — expedite the open PO or transfer from ShipBob now."* Applied in both engines. Row still appears (next cycle still needs the PO) but timing problem is loud.
  - **FIX 4 — Real unit cost (replaces hardcoded $12).** New `load_cost_lookup()` in `build_deep_plan.py` reads SAP Inventory Items Cost Report (`reports/_data/cost/`). Threaded through `run_workflow_for_sku()` via new `cost_lookup` kwarg. 361 UPCs now load real costs. Example impact: 811573031335 PO value $370K (was $1.16M — 65% overstated). `DEFAULT_UNIT_COST = 0.0` documented fallback. New classifier rule in `sort_downloads.py`.
  - **FIX 5 — TikTok floor → named constant.** `TIKTOK_MONTHLY_FLOOR = 350` promoted from magic number in `compute_monthly_demand()` signature.
  - **Doc:** Operator brief lives at `(brief in OneDrive)` — implemented per its acceptance checks.

**Recent work (Jun 5-12):**
- ✅ **SharePoint sync trimmed to weekly report only (Jun 12)** — `outputs/latest/` is a Windows Junction → `michaeltoddbeauty.com\Supply Chain - Documents\ANALYSIS WEEKLY INVENTORY REPORT` (OneDrive synced). Every pipeline script used to mirror outputs there, so the team's SharePoint folder filled with velocity-watch / order-list / rebalance / deep-plan / etc. Now ONLY `weekly-report-*.xlsx` is published. 10 scripts edited: `build_order_list`, `build_velocity_watch`, `build_deep_plan`, `build_sap_rebalance`, `build_sap_sb_rebalance`, `build_sap_floship_rebalance`, `build_inventory_audit`, `build_po_lead_time_audit`, `build_container_loading_priority`, `au_po_sizing`, plus the order-list mirror inside `build_report.py`. Dated archive `outputs/YYYY-MM-DD/` still holds everything locally for operator reference.
- ✅ **AU PO Sizing recipe (Jun 11)** — standalone helper for sizing Amazon AU supplier POs based on Floship 12-month sales × 51% AU share rule. New script `scripts/au_po_sizing.py` + new SOP `06 Processes & SOPs/(C) AU PO Sizing — Floship 51% Recipe.md`. Default: 9-month cover, 100d lead time. CLI: `python scripts\au_po_sizing.py [--cover N --au-share 0.51 --lead-days 100]`. Covers MTB AU POs only — NFMD doesn't ship via Floship so it has no signal in this recipe (need Amazon SC AU FBA report for NFMD AU sizing).
- ✅ **ShipBob distinct-variant rendering (Jun 11)** — new `SHIPBOB_DISTINCT_VARIANT_SKUS` set in `build_report.py`. Lists ShipBob raw SKUs that share a UPC prefix but represent physically distinct products (e.g., `850003115139` = Mio Green w/USB kit vs `850003115139 - 1` = Mio Green Only device). These now render as SEPARATE rows on the ShipBob tab instead of being merged by `_bare_upc()`. Initial list: 4 entries (Mio Green, Nova Green, 2x NERA variants). AMZ-suffix variants stay merged (same physical product, Amazon-stickered).
- ✅ **SAP↔3PL rebalance tabs REMOVED from weekly report (Jun 11)** — 🔄 SAP↔SB, 🌏 SAP↔Floship, 🛒 SAP↔Walmart no longer build inside `weekly-report-*.xlsx`. Weekly report is now operational-planning only (19 tabs). Reconciliation lives ONLY in the standalone monthly file via `python scripts\build_sap_rebalance.py` → `outputs/YYYY-MM-DD/sap-rebalance-YYYY-MM-DD.xlsx` (11 tabs).
- ✅ **Rebalance simplified (Jun 11)** — dropped XFER OUT / XFER IN columns + the 🔁 SAP Transfer Requests tab. INTERNAL TRANSFER column (ShipBob FC-to-FC moves) moved into col 7 of ⚠ SB Variances. ShipBob total now = Σ(Fulfillable) + Σ(Internal Transfer). ShipBob "Incoming" column (supplier-inbound, not at SB yet) explicitly excluded.
- ✅ **SAP doc# fix (Jun 11)** — SAP Open POs export has two doc-number columns; the loader was reading the parent (#3118) instead of the line-level (#3206). Now uses `Document Number.1` (line-level) — affects every tab showing PO doc#s.
- ✅ **DESCRIPTION_OVERRIDE + AMAZON_SKU_ALIAS expanded (Jun 11)** — per-UPC clean descriptions that survive SAP item-master refreshes. Documented for DELSENBRSH / 859886007708 (Soniclear Sensitive Brush Head, ASIN B01IHAQZXA).
- ✅ **Weekly report UPC col now shows "UPC · ALIAS"** on THIS WEEK / PO Priority / In Transit — Ctrl+F finds items by either bare UPC or Amazon SKU.
- ✅ **THIS WEEK NOTES column (col H)** carries forward across rebuilds (already-existing mechanism extended to THIS WEEK).
- ✅ **WATCH_OVERRIDE_UPCS** — operator-managed list to route specific UPCs to WATCH instead of EXPEDITE on THIS WEEK (D-class phase-out items, etc.).
- ✅ **ASG-* warehouses route to Amazon CA channel** — supplier POs landing at Alliance staging now appear on the Amazon CA tab's PO ARRIVES ON column with `[ASG-MTB/NF/SS]` warehouse tags.
- ✅ **Walmart SB → WM TRANSFER column** (replaces PO ARRIVES ON on Walmart) — populated from SAP Inventory Transfer Requests filtered to `from=SBGA-*, to=WM-*`. STOCKOUT DATE / DAYS OF STOCK renamed to "WITH TRANSFER" + formula uses only the pending transfer qty (not full ShipBob NET pool).
- ✅ **Per-tab tooltip overrides** for ShipBob / Walmart / TikTok / Floship Intl — non-Amazon tabs no longer show Amazon-flavored hover text.
- ✅ **Hidden tabs:** Amazon AU + Amazon EU (right-click any tab to Unhide).
- ✅ **Walmart phantom-row cleanup** — drops Valogix WM-SS rows for UPCs in the WFS NFMD file (eliminates duplicate STOCKOUT rows for NFMD products).
- ✅ **Alliance CA Inventory on Hand (Hereford direct) wired in (Jun 10)** — new authoritative source for `alliance_wh_ca` column on the Amazon CA tab. Overrides SAP ASG-MTB / ASG-NF / ASG-SS (which lags until POs are formally received in SAP). Pattern matches ShipBob direct vs SAP SBGA. New loader `load_alliance_ca_onhand()` aggregates multi-lot rows; sort_downloads classifier rule `My Inventory on Hand*.xlsx` → `reports/_data/alliance-ca/`. First pull (2026-06-10): 21 UPCs / 12,152 units (MTB:9 · NFMD:7 · SS:5).
- ✅ **LUMOS dropped from ShipBob pull (Jun 10)** — LUMOS IPL was operationally consolidated into MTB at ShipBob (LUMOS account now all zeros). Removed from `sort_downloads.py` group-ID map, all ShipBob loaders (`build_report.py`, `build_sap_sb_rebalance.py`, `build_deep_plan.py`, `build_inventory_audit.py`), and SOPs. Weekly pull is now 3 ShipBob files. "LUMOS" keyword in brand-fallback retained — LUMOS-branded SKUs classify as MTB.
- ✅ **🏭 PO Priority tab** — vendor-ranked manufacturing list. Days-first ranking aligned with THIS WEEK ORDER section (Gap 1 + Gap 2 closed Jun 8).
- ✅ **📦 In Transit tab** — reads SharePoint In-Transit Log, filters to active (qty_received < qty_shipped), distinguishes AMZ-bound vs SB-bound.
- ✅ **⚠ SUPPLY RISK section** in THIS WEEK — subtracts in-transit qty so already-shipped POs don't false-alarm.
- ✅ **In-Transit Log loader** (`load_in_transit_log()` in build_report.py) — `IN TRANSIT LOG*.xlsx` auto-classifies to `reports/in-transit/`.
- ✅ **NFMD brand fallback** broadened — catches "NASAL RINSE", "SALT PACKET", "NOSE PILLOW", UPC prefix `850038082*`.
- ✅ **Stockout Date (WITH PO)** populates for HEALTHY items on ShipBob/Walmart/TikTok tabs (was suppressed, removed 999-day cap).
- ✅ **Amazon US tab** — added SHIPBOB TOTAL + SHOPIFY RESERVE columns for math transparency.

**Open follow-ups (deferred):**
1. **Forecast Accuracy & Buffer Sizing** — 5-phase plan, Phase 1 (Valogix forecast snapshots) running automatically. Open questions still need decisions.
2. **AWD-to-FBA Shipment Pipeline** — wire up AWD Outbound Shipment Data (per-SKU detail). Files in Downloads; not yet auto-classified.
3. **Manage FBA Shipments** companion data — need to pull Inbound Shipment Items report for per-SKU SB→FBA visibility.
4. **TrueOPS Shipment Module** — parked build (separate folder with system brief).
5. **SharePoint master brain migration** — two-brain model (personal local + SharePoint master) captured in architecture doc.

**Pilot SKU validated:** NFMD Premium Bundle (UPC 850038082352, ASIN B0DN6SJ8WB). PO 3204 = 9,492 units in transit, ~37,400 still at supplier. PO 3092 (4,320u) arrived May 13.

---

## Parked Build Plans (`07 AI Tools & Builds/`)
- Forecast Accuracy & Buffer Sizing — 5 phases
- AWD-to-FBA Shipment Pipeline
- SAP Open POs Integration
- Inventory Audit & Reconciliation
- ShipBob New Format Migration
- Master SupplyChainBrain — Architecture (SharePoint two-brain model)

---

## Pipeline Inputs (Weekly)
All drop into `Downloads\` — `sort_downloads.py` routes them:

| Source | Files | Cadence |
|---|---:|---|
| SoStocked (Projected Forecast + Inventory + FvA) | 9 (3/brand × 3) | Weekly |
| Amazon Seller Central FBA (US × 3 + CA × 2 — SS not on amazon.ca) | 5 | Weekly |
| Amazon Seller Central AWD (US) | 3 | Weekly |
| ShipBob (Inventory Status export) | 3 (MTB/NFMD/SS) — LUMOS dropped 2026-06-10 | Weekly |
| Walmart (Marketplace bulk + Inventory Health) | 4 | Weekly |
| Floship (Product Inventory export) | 1 | Weekly |
| Valogix (Forecast + Exceptions) | 2 | Weekly |
| SAP Open POs (full export) | 1 | Weekly |
| Alliance CA Inventory on Hand (Hereford direct) | 1 | Weekly |
| In-Transit Log (SharePoint) | 1 | Weekly |
| Sellerboard CA Dashboard Products | 3 | Weekly |
| Sellerboard Sales by Product/Month | 3 | **Monthly** |

**Total:** ~36 files/week (LUMOS ShipBob dropped 2026-06-10; Alliance CA Inventory on Hand added 2026-06-10; SS CA FBA confirmed not pulled — SS not launched on amazon.ca yet).

---

## Troubleshooting
| Symptom | Cause | Fix |
|---|---|---|
| `PermissionError: weekly-report-*.xlsx` | Excel has the file open | Close Excel, rerun |
| `❓ UNSORTED` in sort log | Classifier doesn't recognize pattern | Move manually OR add rule to `sort_downloads.py` |
| Numbers don't match Seller Central dashboard | CSV is older than dashboard (Amazon caches) | Re-download FBA Inventory Report |
| Velocity inflated 30-50× on CA items | CA Dashboard pulled without `amazon.ca` filter | Re-pull with marketplace filter set |
| `⚠️ Sellerboard Monthly is N days old` | Monthly cadence — pull the 3 Monthly reports | |

---

## Key Reference Docs
- `06 Processes & SOPs/(C) Weekly Analysis SOP — Step by Step.md`
- `06 Processes & SOPs/(C) Weekly Inputs Sourcing SOP.md`
- `06 Processes & SOPs/(C) Daily Morning Routine — SCM.md`
- `06 Processes & SOPs/(C) ABC Classification Reference.md`
- `10 System/(C) Master SupplyChainBrain — Architecture.md`
- `07 AI Tools & Builds/(C) Forecast Accuracy & Buffer Sizing — Build Plan.md`

---

## Trigger Phrases (resume parked work)
- *"Pick up the forecast accuracy build plan"* — 5-phase plan
- *"Pick up the AWD-to-FBA pipeline"* — shipment visibility build
- *"Wire up the Inbound Shipment Items report"* — companion to In-Transit Log
