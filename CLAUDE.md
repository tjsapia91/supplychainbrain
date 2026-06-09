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
**Last updated:** June 8, 2026

**Recent work (Jun 5-8):**
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
| Amazon Seller Central FBA (US + CA) | 6 | Weekly |
| Amazon Seller Central AWD (US) | 3 | Weekly |
| ShipBob (Inventory Status export) | 4 (MTB/NFMD/SS/LUMOS) | Weekly |
| Walmart (Marketplace bulk + Inventory Health) | 4 | Weekly |
| Floship (Product Inventory export) | 1 | Weekly |
| Valogix (Forecast + Exceptions) | 2 | Weekly |
| SAP Open POs (full export) | 1 | Weekly |
| In-Transit Log (SharePoint) | 1 | Weekly |
| Sellerboard CA Dashboard Products | 3 | Weekly |
| Sellerboard Sales by Product/Month | 3 | **Monthly** |

**Total:** ~37 files/week.

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
