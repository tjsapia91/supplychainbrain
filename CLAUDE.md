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
1. **Drop every export → `reports\_inbox\`** (sorter files them automatically)
2. **Run ONE command:**
   ```
   cd C:\Users\Tom Sapia\MTB-SupplyChain
   python scripts\build_report.py
   ```
   `build_report.py` now auto-runs `demand_planning.py` first (Tommy 2026-06-22), so the report always reads a fresh same-day JSON. If the input check flags stale/missing data it stops and writes a marker — just run the same command again to build on existing data (stamps the stale banner). Override `SKIP_DEMAND_PLAN=1` to rebuild off the existing JSON without re-pulling.
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
- **`build_inventory_reconciliation.py`** — SAP↔ShipBob recon (operator's `inventory-reconciliation.md` procedure). Per-warehouse blocks, SAP+ShipBob column groups, Difference/Total. Computes values directly (no #N/A cleanup). Negative-Committed validator. Standalone: `python scripts\build_inventory_reconciliation.py`

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
**Last updated:** June 16, 2026

**Recent work (Jun 24):**
- 🟡 **THIS WEEK feeder wiring — brain FBA-t90 demand (increment 1 of N, Jun 24)** — per `THIS-WEEK-FEEDER-WIRING-for-Claudian-2026-06-24.md`, "wire in the brain" path (Tommy's call over patching feeders in place). **Amazon demand-of-record is now FBA sell-through (units-shipped-t90 ÷ 90)** pulled from the unified brain's loaders (`build_action_plan_proto.load_fba/load_awd_inv`, canonical-UPC keyed via `sku_rules.resolve_upc`) — Valogix no longer drives Amazon demand. Injected onto 296 Amazon US/CA rows; overrides `amzn_us_vel` + `daily_vel` (prior stashed as `daily_vel_pre_brain`). **Fixes the White (811573031113) smoking gun:** legacy `811573030475-M` row was 0.73/day → stockout "Aug 03 2056" → false DEFER; now both rows read true 42.9/day → Jan 2027. 1410 reads 159/day. Step 6 also done: `850003115030` (ECHO) + `811573031427` (Peach Fuzz) added to PHASE_OUT_UPCS. **Validated:** White ≈43/d, 1410 ≈160/d, ZERO rows <1/day-while-actuals->50, no 20xx-beyond-decade dates, section counts sane. **REMAINING increments:** Step 1 row-FOLD (White still renders as multiple rows — dedup to one per canonical UPC); Step 3 position columns (brain FBA/AWD injected as fields, not yet driving the position cols); Step 7 routing (1410 should route to ShipBob transfer, not Amazon ORDER 10,337); Steps 4-5 (stockout cap, PO tranche matching). Stale inputs to refresh before a clean run: SKU map (13d), Sellerboard SS (14d).

**Recent work (Jun 22):**
- ✅ **Reconciliation ShipBob-join fix (Jun 22)** — per `RECONCILIATION-FIX-for-Claudian.md`. The old `load_shipbob_recon()` summed all 3 ShipBob brand files into ONE pool, so SBGA-MT and SBGA-SS both matched the same combined qty → double-count + phantom SAP=0 gaps. Fixes: (1) brand-partitioned loader returns per-brand dicts; `build()` merges only the brand account(s) feeding each SAP warehouse via `SHIPBOB_BRAND_SOURCES` (SBGA-MT=MTB; SBGA-SS=SS+NFMD); blank-FC rollup row skipped. (2) `sku_rules.resolve_upc` replaces local `_bare_upc` + SAP rows folded to canonical UPC per warehouse (kills in-warehouse double-count from duplicate item records). (3) components stay out (SAP-driven). **Result: TRUE DIFFERENCE −97,677u → −1,331u.** SBGA-MT −16,222 → −6,066 (remaining = real cycle-count candidates 811573031335/31410/31090/31342); SBGA-SS −81,455 → +4,735. Layout/negative-Committed flag/output path unchanged. (Reconciliation is operator-triggered only: `python scripts\build_inventory_reconciliation.py` — separate from the weekly pipeline.)
- 🟡 **Unified brain — Phase 1 of the weekly-report rewire (Jun 22, IN PROGRESS)** — per `CLAUDIAN-HANDOFF-weekly-report-rewire.md`. Goal: keep `build_report.py`'s LOOK, replace its DATA layer (demand/position/ABC/actions) with the new unified brain (actual sell-through, multi-echelon position, sku_rules remaps). Approach = phased, validate-then-retire; **Phase 1 only this session — build_report.py UNTOUCHED.**
  - **Phase 1 DONE:** re-pointed all 6 sandbox-bound brain scripts (`build_sales_index`, `build_sales_demand`, `build_action_plan_proto`, `cross_check`, `validate_unified`, `run_unified`) from `/sessions/.../mnt` + `/tmp` to local folders: `reports/_brain/` (intermediate JSON), `reports/_brain_inputs/` (non-pipeline drop folder for Sales file + AWD tortuga + TikTok Inv Health), `outputs/unified/` (deliverables). `sku_rules.py` was already portable. Walmart now reads classified `reports/_data/walmart/`. Fixed Windows `.md` utf-8 crash. `run_unified.py` core-5 chain runs **EXIT=0**.
  - **Validator PASS (4/4):** inputs present · Pink (859886007586) folded to Green (811573031106, FBA t90=2263) · phase-outs not ordered · SHORT items have no transfer stock. 74 PO recs await Tommy sign-off.
  - **Cross-check (new actual vs old Valogix):** 326 SKUs · 78 agree ±25% · 91 new-higher (Valogix under-counted, e.g. Pro+ Lavender 3.5→301/d, VIVA White 0.1→65/d) · 79 new-lower (Valogix over-forecast — the SVP concern, e.g. NasalFresh Shipper 431→148/d, Hair Spray 526→339/d, NasalFresh Premium 469→288/d).
  - Deliverables in `outputs/unified/`: `Action-Plan-PROTO.xlsx` (8 tabs) · `CROSS-CHECK-REPORT.md` · `VALIDATION-REPORT.md`.
  - **NEXT (Phase 2, awaiting Tommy):** review the cross-check + the 6 vetted SKUs (all resolved w/ demand: White 48/d, Hair Spray 339/d, MTBLavendar 120/d, Pink→Green 36/d, dead tails 0.27/1.43). Only after sign-off → Phase 3 (swap build_report.py data layer, keep rendering) → Phase 4 (retire Valogix path). MTB-SupplyChain repo: brain committed (branch `master`, local-only). Two optional extras (`build_demand_plan.py`, `generate_action_html.py`) still sandbox-pathed — non-fatal, out of Phase-1 scope.

- ✅ **Weekly pipeline trimmed to ONLY the weekly report (Jun 22)** — `build_report.py` no longer emits side files. `build_order_list()` still computes the ORDER rows for the THIS WEEK tab but is now called with `write_workbook=False` so the standalone `order-list-*.xlsx` isn't written. The Velocity Watch auto-chain was removed — it's a separate 2-day-cadence workflow (`python scripts\build_velocity_watch.py`). `build_deep_plan` still runs INLINE (no file) to feed SUPPLY RISK. Net: one command → one output (`weekly-report-*.xlsx`). The `forecast-snapshot-*.csv` stays (it's the forecast-accuracy Phase-1 tracker, not a report deliverable). Standalone CLIs for order-list + velocity-watch + deep-plan unaffected.
- ✅ **Inventory Reconciliation report shipped (Jun 22)** — new `build_inventory_reconciliation.py` implements the operator's `inventory-reconciliation.md` procedure (SAP ↔ ShipBob). Reproduces the manual `MTB-SB recon.xlsx` layout — per-warehouse blocks in the SAP "Inventory in Warehouse" structure, merged SAP group (In Stock/Committed/QC/Available) + ShipBob group (In Stock/Committed/Internal Transfer/Available) + Difference/Item Price/Total/Confirmed — but driven off the auto-filed pipeline exports. Formulas: SAP Available = In Stock − Committed; ShipBob Available = In Stock − Committed + Internal Transfer; Difference = SAP − ShipBob (positive = SAP has more). QC column pulled from SBGAMTQC/SBGASSQC blocks for the SBGA-MT/SS rows. ShipBob comparison columns only populate on ShipBob warehouses (SBGA-MT/SS/SS-NFMD); ASG/FLO/WM/TIKTOK render as SAP-side audit. **Two improvements over the manual file:** (1) computes values directly so there's no #N/A→0 cleanup step, (2) auto-flags negative-Committed SAP rows red + a note (procedure rule: must fix before trusting). First run: TRUE DIFFERENCE −97,677 units / −$234,260 (ShipBob has more than SAP) · 20 negative-Committed rows flagged (FLO-MTB + TIKTOKMT). Output: `outputs/YYYY-MM-DD/inventory-reconciliation-YYYY-MM-DD.xlsx`. **Note:** MTB-SupplyChain is now a local git repo (branch `master`, no remote) — script committed there.

**Recent work (Jun 17):**
- ✅ **Shopify reserve bumped 30 → 90 days (Jun 17)** — `SHOPIFY_PROTECTION_DAYS` in build_report.py main + `SHOPIFY_SAFETY_DAYS` in deep_plan workflow both now `90`. ShipBob backup (`shipbob_emergency` NET) subtracts `shopify_velocity × 90` from the raw ShipBob on-hand before claiming units for Amazon transfer. Tooltips on Amazon US + ShipBob tabs updated to reflect "90 days × Shopify daily velocity". Verified: *"ShipBob backup netted of Shopify 90-day reserve: 258 Amazon items adjusted"* in latest build.

**Recent work (Jun 16):**
- ✅ **Phase-out / kit exclusion extended to CA/UK/AU triage sections (Jun 16)** — operator caught that Pink (`859886007586`) was being flagged "needs Alliance replenishment" on the 🇨🇦 CANADA section even though it's a phase-out SKU (the ORDER section was already excluding it). Now the same `PHASE_OUT_UPCS` + combo-kit check applies in CA + UK + AU sections. Phase-out / kit rows render as `"DO NOT REPLENISH — phase-out"` or `"DO NOT REPLENISH — kit"`, muted styling, sorted to the bottom (mirrors ORDER's behavior). Remap flag (`⚠ SKU≠UPC`) also stamps when applicable. Verified Pink row in CA now reads: *"DO NOT REPLENISH — phase-out · Legacy/transition SKU — let it run down on Canada too; never auto-replenish."*

- ✅ **Dedicated drop folder + input check shipped (Jun 16)** — two briefs (`DROP-FOLDER-for-Claudian.md` + `INPUT-CHECK-for-Claudian.md`) implemented end-to-end. Weekly run is now ONE fast command again.
  - **`sort_downloads.py` scans only `reports/_inbox/`** — replaced the previous `DEFAULT_INBOX` (`~/Downloads`) + `SECONDARY_INBOXES` (OneDrive Documents + Desktop) that caused 20+ min hangs scanning the whole SupplyChain1 project. `INBOX = os.path.join(BASE, "reports", "_inbox")` with `os.makedirs(INBOX, exist_ok=True)`. `include_secondary` kwarg kept as a silently-ignored no-op for backward compat. Marker files (`.`-prefix) and readme (`_`-prefix) skipped.
  - **Pre-flight sort re-enabled unconditionally** in `build_report.py`. The `SORT_DOWNLOADS=1` env-var gate is gone; the inbox sort runs every build (try/except so a bad file never blocks). New message: *"Pre-flight: filing reports/_inbox → reports/_data…"*.
  - **`scripts/check_inputs.py` — new** — verifies every required export is present + current (`STALE_DAYS=7`) before the build loads data. Manifest covers Valogix forecast/exceptions, SAP Inventory + Open POs + Transfer Reqs, item master, SKU map, plus per-brand FBA/AWD/ShipBob/Sellerboard/SoStocked PFM/FvA, plus Walmart for NFMD+SS only (MTB excluded — doesn't sell on Walmart). Date extraction reads `YYYY-MM-DD`, `YYYY_MM_DD`, `MM_DD_YY` from filenames with mtime fallback. Returns `('PROCEED_CLEAN', [])` / `('PROCEED_STALE', flagged)` / `('STOP', flagged)`.
  - **Run-twice override** replaces the env-var override (no `FORCE_BUILD`-style flag). First run with flags writes `reports/_inbox/.input_check_pending` (JSON: today's date + sorted flagged set) and STOPS — preserves the prior good `weekly-report-*.xlsx`. Second run with same-or-subset flagged set → PROCEED_STALE, build runs on existing data, **"⚠ Building with existing/stale data for: <list>" stamps on THIS WEEK row 2**, marker auto-cleared. A *new* gap or a marker from a prior day → re-flag and stop (never silently build through a fresh gap).
  - **Wired into `build_report.py`** between the inbox sort and data load. Stale flagged set is stashed on `data` so `build_this_week_tab()` can render the banner. `sys.exit(2)` on STOP.
  - **Acceptance verified end-to-end:** standalone `python scripts\check_inputs.py` prints the same checklist + flagged set; first build run with file removed → halts with marker written; second run → builds + stamps banner; restore file → clean build, banner absent.

- ✅ **SKU↔UPC remap detection + Pink phase-out shipped (Jun 16)** — operator brief `SKU-UPC-remap-detection-for-Claudian.md` implemented. The Pink false-stockout was the root signal: Amazon listing `859886007586` (legacy Pink) maps to SAP UPC `811573031106` (Green refill, on order ShipBob POs 5,026+5,000u due Oct 3/Oct 11), but the report was reading stock under the wrong key.
  - **Fix 1 — SKU→UPC normalization before stock/position lookups.** `sku_model.py` now accepts `sku_to_upc` kwarg and resolves every SAP-inventory / open-PO / Valogix-demand row through the alias map before aggregation. `build_report.py` passes `AMAZON_SKU_ALIAS` in. Pink-type listings now read stock under their canonical UPC.
  - **Fix 2 — Auto-register ALL Amazon SKU↔SAP UPC pairs.** Previously the dict-keyed loop dropped any duplicate Amazon SKU mapping to the same SAP UPC (so 859886007586 → 811573031106 never registered alongside 811573031106 → 811573031106). New loop iterates `all_pairs` and registers everything; dropped the `.isdigit()` exclusion that masked numeric remaps. **20 base(SKU)≠base(UPC) remap candidates auto-aliased** this run (includes Pink, Sonicsmooth White, Lavender, BODYBRBLK, NOVA Serum Head, etc.). 44 SKU→UPC aliases now applied for remap-safe lookups.
  - **Fix 3 — `⚠ SKU≠UPC` flag in renderers.** New helpers `base_sku()` (strips `-M`/`-AMZ`/`-AMZLabel`/`-FBA`/`-FBA-M`/`AMZ-stickerless`/`-stickerless`) + `is_remap_candidate()`. ORDER, EXPEDITE, and kit/phase-out rows now prepend `"⚠ SKU≠UPC — verify stock read under UPC (possible remap/transition)."` when triggered. 4 rows flagged on this run (Pink + Sonicsmooth Lavender + Sonicsmooth White + NOVA Serum Head).
  - **Fix 4 — Pink marked phase-out + distinct label.** `859886007586` added to `PHASE_OUT_UPCS` (same bucket as MIO kit — never auto-order). Renderer now distinguishes kits ("DO NOT ORDER — kit") from phase-outs ("DO NOT ORDER — phase-out"). Pink correctly shows as phase-out with the remap flag in ORDER. Amazon-direct unit count dropped 9,526 → 2,546 (-6,980 = exactly Pink's quantity).
  - **Result:** the 9 known remaps from the brief now resolve to the canonical UPC. Any future remap announces itself via the data-driven flag — no manual succession map to maintain.


- ✅ **Model gate made authoritative — 2 remaining leaks closed (Jun 16)** — operator verified after the sku_model wiring that `811573031410` (Hair Identifier Spray, 189d HEALTHY) and `860021001185` (NOVA Green w/USB, 218d HEALTHY) were still leaking into ORDER with small quantities. Root cause: build_order_list's local gap math (volatility_mult × demand) pushed demand a few days above model_position, generating tiny phantom POs. Fix: added a short-circuit at the top of the per-UPC loop in `build_order_list.py` — when `slot['model_status'] in ('HEALTHY', 'OVERSTOCK')`, skip emission entirely (kits are exempt — they still need their visible "DO NOT ORDER" row). Both leaks dropped on the next run. ORDER section settled at **7 rows** — 6 genuine orders (11,526 units total) + 1 kit marker — matching operator's predicted target.

- ✅ **MASTER-BUG-REGISTER sync — landed bugs marked, suggested fix order rewritten** — register at `10 System/SupplyChainClaude/Supply Chain Planning/MASTER-BUG-REGISTER.md` updated. Status truth: bugs A, B, C, 0, 1, 2, 3, 4, 5 all ✅ landed; bug E investigated (no code change). Pending: Bug 7 (now shipped — see below), Bug 6 (deferred per brief recommendation), Bug 8 (parked by operator), Bug 9 (parked).
- ✅ **REFACTOR — `sku_model` wired into `build_report.py`** — operator brief `REFACTOR-sku-model-wiring-for-Claudian.md` implemented. `scripts/sku_model.py` (already built + validated) now drives ORDER + EXPEDITE + downstream tabs via injected `model_position`, `model_demand`, `model_days_cover`, `model_status`, `model_open_po`, `model_open_po_by_wh` fields. 680 per-SKU rows enriched per run. Catalog truth: **160 OVERSTOCK · 28 HEALTHY · 28 BELOW ROP · 20 TRUE STOCKOUT** of 236 SKUs. All 5 brief acceptance checks pass (811573031335 HOLD, 811573031342 HOLD, 850003115948 HOLD, MIO Combo Kit visible as DO NOT ORDER, SonicSmooth Pink in ORDER as true stockout). `_us_total_stock_available()` and `_compute_horizon_demand()` in `build_order_list.py` now prefer model values when injected, with legacy fallbacks intact. SB PO engine adds a third skip-guard: `model_status in (HEALTHY, OVERSTOCK)` → no fresh PO.
- ✅ **Bug 7 — UNROUTED CRITICAL safety-net section** — new section at the TOP of the ✅ THIS WEEK tab. Scans `data["all_items"]` for any status containing CRITICAL or STOCKOUT; any item NOT routed to ORDER/EXPEDITE/TRANSFER/SUPPLY RISK/WATCH renders here with action "REVIEW MANUALLY". Today's run surfaces 22 unrouted critical items (CA stockouts + a few US edge-case SKUs like `860021001147AMZ-stickerless`). Console prints each one for traceability so the keying-logic gaps can be hunted down separately.

**Recent work (Jun 15):**
- ✅ **THIS WEEK ORDER section — brief v2 corrections shipped (Jun 15)** — operator updated the fix brief with two BUILD CORRECTIONS. Both shipped:
  - **FIX 2 corrected**: MIO Combo Kit must stay VISIBLE in ORDER with "DO NOT ORDER — kit" label (not silently removed). Changed `continue`/skip to emit a `kit_no_order=True` marker row, sorted to bottom via `stockout_date=date.max`. Renderer branches on the flag → muted navy_mid styling + kitting-rule context. Applied in BOTH order engines.
  - **FIX 3 corrected**: Interim warning was over-applied (12 of 13 ORDER rows). Soften when same UPC has an inbound PO in EXPEDITE. Built `_inbound_upcs` set from `expedite_rows`; if UPC matches, prepend `↪ Inbound PO already being expedited` instead of red `⚠ Stocks out before any PO can land`. Only 3 of 13 rows now carry the strong alarm.
  - **Hidden bug found + fixed**: kit rows have `days_cov=None`, which crashed `build_order_list`'s Excel renderer at `if days_cov < 60:`. The except block silently swallowed it, dropping all 4 Amazon-direct rows (incl. SonicSmooth Pink stockout = today). Now guarded.
  - **Plus: WATCH section dedupe** — UPCs appearing in multiple channel rows (US + CA) used to produce duplicate WATCH entries, one empty. Now dedup by bare UPC preferring the row with a populated `po_eta`. 8 rows → 5.
- ✅ **THIS WEEK ORDER section — 6 fixes shipped + brief verification done (Jun 15)** — operator-supplied fix brief implemented end-to-end, all 3 acceptance checks satisfied. Touched `build_report.py`, `build_order_list.py`, `build_deep_plan.py`, `sort_downloads.py`. Verification: (1) clean Jun 15 extract passes the gate after calibrating `EXPECTED_MIN_ITEMS` from 150 → 100 (historical extracts dropped from ~190 to 109 items around May 27 — 100 threshold catches genuinely broken without false-flagging current normal); (2) degraded extracts properly blocked with `FORCE_BUILD=1` override; (3) ORDER qty diff vs Jun 10 baseline = 13 UPCs unchanged + MIO Combo Kit removed (FIX 2 working). Per-PO missing-cost warning prints always (not verbose-gated) so data-quality gaps surface to the operator.
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
- `10 System/(C) SupplyChainClaude — Index.md` — junction-mounted OneDrive workbench: operating principles, runbook, bug register, deep-dives, fix briefs
- `07 AI Tools & Builds/(C) Forecast Accuracy & Buffer Sizing — Build Plan.md`

---

## Trigger Phrases (resume parked work)
- *"Pick up the forecast accuracy build plan"* — 5-phase plan
- *"Pick up the AWD-to-FBA pipeline"* — shipment visibility build
- *"Wire up the Inbound Shipment Items report"* — companion to In-Transit Log
