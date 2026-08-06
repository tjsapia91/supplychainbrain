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
├── 06 Processes & SOPs/              (the good stuff)
├── 07 AI Tools & Builds/             (build plans, parked projects)
├── 10 System/                        (architecture, sync)
├── 11 Skills/                        (reusable scripts as MD)
├── 12 Attachments/
├── 13 Iteration Logs/
├── 14 Learning & Development/
├── 15 Meetings & Decisions/          (incl. Daily Action Plans)
├── Projects/                         (active build projects)
└── Weekly Report Explanation/        (per-tab documentation)
```
> Folder cleanup (Tommy 2026-06-29): removed 5 empty scaffolding folders that
> never got filled — `04 Sales Channels`, `05 International Expansion`,
> `08 Key Metrics & Dashboards`, `09 People & Relationships`, `Templates`.
> Recreate on demand if a real note needs one of those homes.

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
**Last updated:** August 6, 2026

**Recent work (Aug 6) — family grouping + Monthly-Flow what-if send-in input + EDI forecast report + email brief:**
- ✅ **Group "like items" on the flow + all 3 replen planners (MTB-SupplyChain).** New `sku_rules.product_family()` (single source of truth; whole-word match so "innovative" ≠ NOVA) clusters SonicSmooth / Soniclear / NOVA / AIVA / MIO / SIMA / NasalFresh etc. **Flow** groups families *within* each ABC section; **planners** group within each brand tab. Family ordered by total demand (biggest first), then demand desc, then UPC. SonicSmooth Pro+ + Hair Identifier Spray fold under SonicSmooth. Row reorder only — COM-verified 0 formula errors.
- ✅ **Monthly Flow (Amazon): editable "Your send-in (enter qty)" what-if input.** Blue cell under the "Suggest send-in (UNIS)" line — type a UNIS→FBA send-in qty → month-0 Ending picks it up → **Ending / Days of cover / Stockout date recalc live** ("how long are we good?"). Default 0 = baseline. COM-verified: +20k flips a SKU stockout Feb-6-2027 → covered-in-horizon; 0 errors. (POs on the Amazon report really land at UNIS → UNIS replenishes FBA, so this lets Tommy model the send-in.)
- ✅ **NEW EDI Forecast Report by retailer** (`01 Purchasing & Inventory/(C) EDI Forecast Report — by Retailer.md`). CVS 830 = the only true EDI forecast: **5,562u** horizon 8/23–10/24, 12 SKUs, full SKU×week matrix + week-over-week trend (5,430→5,196→5,562, +2.4% net). JCP = no EDI orders (POs by email; 32461438 rejected). Walmart EDI = admin/chargebacks only. Batch splits by **vendor account** (not DC).
- ✅ **Email brief + Action Triage 2026-08-06** (121 msgs). Blade fly-in elevated to #1 (Harry: 25,050 fly 8/15 + 25,050 fly 8/29; needs per-DC split + addresses; Donna split 50% Fairburn/27% PA/23% Reno; ShipBob = must inbound a hub then IPP to spokes). UNIS blade container ONEU6390520 (seal CNEB38651) + 3 cleanups. David/UNIS inventory call = calendar invite (tentative) today 2 PM ET.

**Recent work (Aug 4-5) — Monthly Inventory Flow report + container-plan/UNIS fixes + Batch Code Map + repo backup:**
- ✅ **"Incoming Transfer (SAP)" column wired into all 3 replen planners (US/CA/ShipBob) + the Monthly Flow (MTB-SupplyChain).** Reads `reports/_data/sap-transfer-requests/*.xlsx` (SAP Inventory Transfer Requests) via new `AP.load_transfer_reqs()` + `AP.transfer_in_by_upc(channel)`, and renders the incoming transfer qty as a column **at the receiving end** — US = AMZN/UNSC/UNCA · CA = ASG · ShipBob = SBGA. On the planners it's a **display-only** column (NOT fed into coverage tiers, so no double-count in the runway); on the flow it folds into the incoming box. `replen_layout` EXTRA now = inbound + transfer offsets so the coverage-map formulas shift safely — **COM-verified 0 formula errors on all 3**. Current pull: **ShipBob 274u · Amazon US 105,552u / 14 rows · Amazon CA 9,804u / 20 rows.** ⚠ The US total is large and Hair Spray (B0DSLQKVVL) = 43,680 exactly matches the UNIS reservoir figure → these requests are largely the paperwork moving units INTO UNIS; sanity-check they're still-open (not already received) before acting on the number.
- ✅ **NEW "Monthly Inventory Flow" report (`build_monthly_flow.py`) — the "Book3" view.** Per-channel workbooks (`amazon-us-inventory-flow-*.xlsx`, `shipbob-inventory-flow-*.xlsx`), a horizontal month-by-month waterfall per A–D SKU: **Forecast · Starting · PO (available) · Fly-in · Ending · Days of cover · Stockout date**. Published to the SUPPLY CHAIN ANALYSIS hub. Key rules (all in the vault SOP `06 Processes & SOPs/(C) Monthly Inventory Flow — Report Guide & Rules.md`):
  - **Editable (blue) cells:** Forecast, Starting, PO, Fly-in — all live formulas (Ending = Starting+PO+Fly-in−Forecast; Starting = prior Ending; live auto-calc). Fly-in blank by default (air = just-in-case).
  - **Only bankable supply counts:** In-Transit + Container-Plan. **Open POs shown in the incoming box "(not counted)"** + on the Watch List "to book onto a container."
  - **Timing:** PO lands (ETA) → **+2.5 weeks receiving** (`RECEIVING_DAYS=18`) → warehouse-available → **covers the month it becomes available**.
  - **UNIS is NOT counted as FBA stock** (Tommy): waterfall shows the true FBA/AWD position (negative Ending = how much to send in). UNIS shown in the box + a **"→ Suggest send-in (UNIS)"** line = MIN(UNIS avail, FBA shortfall), live.
  - **ABC grouping:** **CLASS A + D (phase-in)** together (D = phase-in, incorporated with A — new rule, also in ABC Classification Reference), then C, then Other. Ordered **within each section by descending total demand** to match the Amazon US replen.
  - **Incoming box** per SKU: PO/Source · Qty · **Load · ETA · Covers** · Type (colour-coded). Persisted per-UPC **Notes column (S)** — carried across rebuilds via `reports/_state/flow_notes_amazon-us.json`.
  - Exact **Stockout date** = live formula (first negative month + fractional day). Save-when-open fallback (timestamped copy if the file's open in Excel).
- ✅ **Container plan cols R/S/T (MTB-SupplyChain).** `load_container_plan` now: **units = Confirmed Qty Harry (col R) › G**; **load date = Confirmed LOAD Date Harry (col S) › plan Load (col M)** (fixed a bug that read col S as a ready date + didn't match the header). Also **cp_eta/cp_load keyed by (PO#, UPC)** in the US + ShipBob planners so one line's date no longer overwrites another's (PO 3221 blades: load 8/29→8/15, ETA 10/13→9/29). **Col T = "Confirmed Sail Date" added but NOT wired yet** — waiting on Tommy for the sail→sellable transit-days number, then it becomes the top ETA tier (sail › load › ready).
- ✅ **UNIS loader auto-computes eaches from the raw export.** Drop the raw UNIS `data` tab (one row per LP; QTY treated as CASES × item-master master-carton pack) → `load_us_reservoir` reproduces Tommy's hand-built "Item Summary" exactly (bundle 5,052 · Hair Spray 43,680, etc.). New format has `Item`/`QTY` cols (old loader looked for `UPC Code`/`On Hand` → read 0).
- ✅ **NEW Batch Code Map (`build_batch_code_map.py`).** Parses the PPO PDFs (pdfplumber) → filterable Excel: Batch Code · Prefix · Batch MM/YY · Date code (NFMD) · UPC · Desc · Brand · PO# · Region · Dest · Ship Date · Qty + Prefix Key. Decodes MTB `<prod><MMYY>`, NFMD compound `<prod><MMYY>-NFMD<MMDDYYYY>`, NFMD single `<prod><MMDDYYYY>[X]`. `PREFIX_OVERRIDE` for mis-stamps (SBB→SBD for 1632). 100 rows / 11 PPOs. **Parked for refinements** — see `07 AI Tools & Builds/(C) PPO Batch Code Map — Notes & Open Items.md` (trigger: *"pick up the PPO batch code map"*).
- ✅ **sku_rules:** MTBLavendar listing `B0CQKK2YCK` → UPC `811573031090` (Sonicsmooth Lavender, class A); `702877109441` (Plum brush) → PHASE_OUT (obsolete); SonicSmooth Pink `859886007586` split from Green `811573031106` (RESERVED, own line).
- ✅ **MTB-SupplyChain repo pushed to GitHub** (`github.com/tjsapia91/MTB-SupplyChain`, private) — was local-only, NOT backed up. `.gitignore` keeps data/outputs out; code only. Both repos now backed up.
- ✅ **CVS 830 parsed for AIVA (850003115634 / item 732452):** 8/2 planning schedule = **156u** across 3 DCs (N101 96 · L101 36 · F101 24) through late Oct — the ongoing trickle, **NOT** the September door-restore (logged in EDI tracker).
- 📋 **OPEN — AWD "Inbound to AWD" not tracked:** the AWD (tortuga) report has an `Inbound to AWD (units)` column (e.g. 811573031373 = 432u in transit ShipBob→AWD) that our loaders don't read — we only read `Available in AWD`. In-transit-to-AWD falls in a blind spot. Fix pending Tommy's call on how to treat it (count vs show).
- 🗣 **Preference (saved to memory):** do NOT use multiple-choice/predetermined-option questions — ask open-ended so Tommy can explain.

**Recent work (Aug 3):**
- ✅ **SoStocked RETIRED → Dave's "Amazon Forecast (Rolling 12 months)" is the new Amazon forecast (MTB-SupplyChain).** New `amazon_forecast.py` loader: `load(marketplace, key_by)` reads **STRICTLY one tab per marketplace — Amazon US = the USA tab ONLY** (never blends CA/UK/EU/AU; Tommy's explicit rule), keyed by canonical UPC or ASIN. Handles the 3-year stacked Jan-Dec header (year rolls on month-reset) + SPA's Aug start. Sorter routes `<BRAND> - Amazon Forecast*.xlsx` → `reports/_data/amazon-forecast/<brand>/`. `check_inputs` now requires **Amazon Forecast** (drops the 2 SoStocked entries). `build_report.load_amazon_forecast_pfm_lookup()` replaces `load_sostocked_pfm_lookup` as a drop-in (same `{(asin,market):{(y,m):qty}}` shape) — the forecast columns + Forecast Pivot + PO-quantity math now run on Dave's numbers. **Impact:** weekly ORDER shifted **7→6 POs / 30,519→35,801u (+5,282)** because Dave's Q4-ramp forecast runs hotter than SoStocked (e.g. AIVA US 671→1,511/mo vs ~460 t90). Files: MTB/NFMD/SPA all present. ⚠ Two dormant SoStocked readers remain (`build_amazon_us_planner.load_sostocked_monthly/weekly`, `combine_forecast.py`) — verify/retire if still on any live path. Non-fatal: build_report's subprocess reader-thread throws a cp1252 UnicodeDecodeError on demand_planning stdout (cosmetic, build completes).
- ✅ **Weekly report built on fresh 8/3 data** — 16-file drop sorted clean; FBA/AWD/ShipBob/Walmart/Valogix all 0-day. ORDER 6 POs/35,801u · 43 SAP same-day flags · 1 supply risk · 14 sales anomalies. Sellerboard (monthly) overdue ~7wk — CA velocity stale.
- ✅ **Email brief 8/3 + JCP order logged.** Harry: **boat delay — Saturday container → Tuesday-AM load** (blade ETAs shift ~3d; he'll update) + asked OK to ship partial. **CVS answered AIVA:** initial 4-WOS DC buildup bought, ongoing via the **830** (3 new 830s landed 8/2, horizon 10/25) — no big one-time fill owed. **JCP ordered 252× MIO Green (850003115139), deliver 8/10** — direct email (JCP orders are email, NOT EDI; only 812/820 come via EDI); must be TRUE green (de-kit WRO 388151795), tight ship-by ~8/6-7.

**Recent work (Jul 31):**
- ✅ **Container-plan date/qty hierarchy — Harry's confirmations firm up the plan, applied in the CENTRAL loader (MTB-SupplyChain).** `build_amazon_planner.load_container_plan` now resolves each PO's **effective ready date = Confirmed Date Harry (col S) › parsed Notes Harry (col Q) › plan Ready Date (col L)** and **effective units = Confirmed Qty Harry (col R) › Units (col G)**; Load Date (col M) passes through. Because every planner (US/CA/ShipBob) + the stockout reports + PO sizing + weekly report read this one loader, **all analysis uses the firmed-up dates at once** (Tommy: "this goes for all the analysis… Harry inputs his dates + confirmed qty and that firms up the container plan"). Container plan gained 2 cols: **R "Confirmed Qty Harry" · S "Confirmed Date Harry"** (empty until Harry fills them). Verified: 3244 now reads Harry's 9/12 (not plan 8/21) → lands ~11/20 across ledgers/calendars. New **Blade Arrival Map** report (`build_blade_arrival_map.py`, "build the blade arrival map") — chronological PO timeline (shipped/firm → loading → not-booked) with a ✈️ FLY BRIDGE box (suggested air qty + sellable-by date) + the R/S confirmed columns; ETAs now sourced from the pipeline so they match the ledgers.
- ✅ **Dedicated SharePoint ANALYSIS hub + overwrite-in-place discipline + combined stockout workbook (MTB-SupplyChain, Jul 31).** New `Supply Chain - Documents/SUPPLY CHAIN ANALYSIS/` folder (OneDrive-synced → SharePoint), junctioned to the repo at `outputs/analysis` (same pattern as `outputs/latest`). New shared helper **`analysis_publish.publish(src, fixed_name)`** copies any analysis there under ONE canonical filename — **replaces itself every run, so the team folder never clutters with dated copies** (dated history still kept in `outputs/<date>/`). Wired 3 analyses to publish: **Stockout Calendars & Ledgers.xlsx** · **Shopify Demand Analysis.xlsx** · **Inventory Reconciliation.xlsx**. Add a new analysis to the hub = one `publish(path, "Name.xlsx")` line.
  - **New `build_stockout_workbook.py`** — consolidates the many per-SKU calendar/ledger files into ONE workbook: a **Summary tab** (every SKU stocking out in a window, sorted by date, SB+US on-hand/stockout side-by-side, red-tinted ≤45d, "open →" hyperlink to each tab) + **one tab per product** (ShipBob ledger left / Amazon US ledger right, shared Date col, editable yellow start cell, red on stockout, in-transit=green "+recv" / container-plan+open-PO=amber "DUE, not counted"). Shipped-only floor. COM-verified 18 tabs / 0 formula errors, force-recalc on open. **Stopped generating the 17 standalone `inventory-calendar-*.xlsx`** (superseded; `build_inventory_calendar.py` stays for single-SKU deep dives).
  - **New `scan_stockouts.py`** — finds every A–D SKU whose shipped-only runway stocks out in a window on ShipBob and/or Amazon US (canonical-UPC keyed, recovers UPC from row when an ASIN doesn't map). `py -3 scripts\scan_stockouts.py [--start YYYY-MM-DD --end YYYY-MM-DD] [--gen]`. Current Aug–Oct set = **17 SKUs** (earliest: NOVA Pink 860021001178 SB 8/17; SonicSmooth White 811573031113 SB 8/31; blades 1335 SB 10/30). ⚠ AIVA (850003115634) US side rides ASIN `B0D7WJVVD4` whose row desc reads `850038082444` — a likely ASIN→UPC cross-wire; treat that US number as suspect.
- ✅ **Container Plan ALSO read LIVE from OneDrive-synced SharePoint (MTB-SupplyChain, Jul 31).** Tommy synced the separate **containerplan2** site → local `~/michaeltoddbeauty.com/Container Plan - Documents/Container Plan.xlsx`. `load_container_plan` now PREFERS it (`CONTAINER_PLAN_SYNCED`; override `CONTAINER_PLAN_SYNC_PATH` env), fallback reports/master → legacy. Reads US POs + International POs tabs; 150 rows verified. ⚠ **The live plan immediately surfaced that 3221/3244/3263/3276 have NO load date yet — only ready dates** (3221 ready **8/22–8/29**, 3244 8/21, 3263 9/6, 3276 9/13). The earlier "3221 loads 8/20 → land Oct 4" was from the stale manual copy; **none of these are booked to sail yet** — chase Harry/freight to book the loads (ETAs now compute off Ready+lead until a Load date lands).
- ✅ **In-Transit Log now read LIVE from OneDrive-synced SharePoint — no manual download (MTB-SupplyChain `7de476b`).** The In-Transit Log lives in the supplychain SharePoint library (`Shared Documents/In Transit/Container's/IN TRANSIT LOG.xlsx`), already synced to disk via OneDrive at `~/michaeltoddbeauty.com/Supply Chain - Documents/In Transit/Container's/IN TRANSIT LOG.xlsx` (updates a couple×/day). `build_amazon_planner.load_in_transit_eta` now PREFERS that live path (`IN_TRANSIT_SYNCED`; override `IN_TRANSIT_SYNC_PATH` env), falling back to `reports/master` then legacy `reports/in-transit`. mtime cache re-reads on each OneDrive update. Kills the manual download→rename→drop step; verified 100 in-transit ETAs load from the synced file. (SharePoint reachable live via the authorized M365 connector — search/read/upload.)
- ✅ **Email brief 7/31 + PO/EDI tracker refresh (vault `29fee6e`).** PO **3276 (30k SonicSmooth blades) SIGNED** by Michael 7/30 → covers ShipBob Dec; 3273 (Floship) shipping Sat→Mon; CA blades 1,500u booked ($7,935 DDU→Alliance); Oxygen Glow Facial Oil formula approved (pickup 8/7). Trackers updated (YAC 3236 / Oxygen / Emily-BMC sections added).

**Recent work (Jul 30) — Email/PO/EDI automation built on the Outlook (MS365) connector (vault-only; read-only):**
- ✅ **`/email-brief` command shipped** (`.claude/commands/email-brief.md`) — scans Outlook last-24h + vendor/EDI threads, filters robots, produces a prioritized brief + refreshes the PO tracker + EDI tracker, auto-commits. Ran live end-to-end (caught the blade blocker clearing + Donna's "Augusto-Review" meeting). Runs on-demand; Obsidian-open auto-trigger deferred (no clean hook — one-tap command is the path).
- ✅ **PO Approval Workflow SOP** (`06 Processes & SOPs`) — the real US 8-step process: SAP entry (delivery window = posting +40 prod +45 transit +40 receiving ≈125d, NO pricing/DDP) → PO→Harry → PI → adjust → **PPO Validator** (local web app) → Lilia(SVP)/Donna(Director)/SC → Michael(CEO) signs → signed copy→Harry = LIVE.
- ✅ **PO Tracker** (`01 Purchasing & Inventory`) — vendor POs placed at their workflow stage from email traffic + stuck flags. Current: PPO 3263/3264/3267 LIVE; **3276 SonicSmooth Blades at stage ⑥ (with approvers)** — reconcile vs SVP's 30k (Harry committed 8,250).
- ✅ **EDI Retail Orders Tracker** (`01 Purchasing & Inventory`) — parses `edisupport@ecom-specialist.com` 850/860 (CVS etc.) into the brain; cancellations float to the brief. (EDI = tracked, NOT filtered — it's how retail partners order.)
- ✅ **Build plan** (`07 AI Tools & Builds`) — full spec + locked params: scope=everything-24h, vendors=Harry/YAC/Oxygen/Emily, org map Michael(CEO)/Lilia(SVP)/Donna(Dir)/Leo(CMO), assoc Augusto/Elisa, ET timezone.
- 📋 **Email brief + SVP action list** live in `15 Meetings & Decisions`.

**Recent work (Jul 29) — master-files reorg + ShipBob/US planner refinements (MTB-SupplyChain commits `8552c4d`→`bbccfdc`):**
- ✅ **Master-files reorg started (Option B — separate master files).** New `reports/master/` folder = one authoritative, overwrite-on-update file each. Migrated:
  - **Container Plan → `reports/master/container-plan.xlsx`.** New `AP.load_container_plan()` reads **ONLY the `US POs` + `International POs` tabs** (all other tabs ignored). All 3 active readers (US/CA/ShipBob) rewired to it; reference tabs show the two tabs; sorter routes a dropped Container Plan → the master. Old `_data/container-plan/` pile deleted.
  - **In-Transit Log → `reports/master/in-transit-log.xlsx`** (~40MB). `load_in_transit_eta` rewritten: reads **all transport tabs** (WATER/INTL-WATER/TRUCK/AIR, not just the active sheet), **col V "QTY RECEIVED" EMPTY = still in transit** (Tommy's rule), disk-cached by mtime (80s→instant). In-Transit reference tab dropped (too big to embed). Old `reports/in-transit/` pile deleted.
  - **Open POs → `reports/master/open-pos.xlsx` (DONE Jul 30 — migration complete).** New `AP.open_pos_path()` resolver (master-wins, legacy `_data/sap-open-pos/` fallback) in `build_amazon_planner`. Repointed EVERY consumer: US/CA/ShipBob replen readers + reference tabs, `read_open_pos`, `build_deep_plan.load_open_pos`, `build_report.load_sap_open_pos` (weekly report) + its input-check manifest, `build_po_lead_time_audit` (via build_report). Sorter routes a dropped SAP Open POs export → `reports/master/open-pos.xlsx` (overwrite); `split_combined` no longer splits Open POs. All 3 planners + weekly loader verified green, PO counts unchanged (1335 = 149,700u / 13 lines). Combined `OpenPOs-ContainerPlan.xlsx` now retired for Open POs (still open in Excel — delete once next drop confirms). Note: `sku_model.build_sku_models` has a **pre-existing** `wb['Sheet1']` bug on the SAP *inventory* read (fails before it reaches open POs; caught by build_report try/except) — separate issue, untouched.
  - **Master reorg = COMPLETE.** Item Master + amazon-sku-mapping stay in `reports/item-master/`.
- ✅ **Three-tier incoming supply columns — "count only what's shipped" (Jul 30).** Replen planners (US/CA/ShipBob) now split incoming POs into 3 supply-confidence tiers instead of one blended "Incoming" number: **① In-Transit** (on the In-Transit Log — shipped) · **② Container Plan** (booked, NOT sailed — speculative) · **③ Open PO** (at supplier — least certain). **ONLY Tier ① feeds the coverage map / stockout runway**; ②/③ render as display-only upside columns (amber/gray) with hover comments. Container Plan comment carries the **load date + est. arrival** (e.g. `PO 3221 · load 8/20 · est arr 10/4 · 25,050`). Shared `replen_layout.split_incoming_tiers()` does the split + comments + IT-only `half_arr`/`af`; each planner tier-tags arrivals at the point the arrival-date hierarchy resolves (it_arr→IT, cp_eta→CP, else→PO) and carries the load date through. **This kills the phantom-gap bug** (the projection was booking unsailed containers ~1 month late → fake October holes → drove a bad 13,900-unit Unis→ShipBob transfer). Validated: 3 planners build green, **0 formula errors** (COM recalc) after the +2 column shift; SonicSmooth Clear (1335) ShipBob shows IT 28,650 / CP 50,100 / PO 30,000 with an honest late-Nov runway on shipped-only stock. MTB-SupplyChain: `replen_layout.py` + the 3 planners.
- ✅ **Coverage-map redesign — self-explanatory + 4-color (Jul 30).** Elapsed buckets now show current On Hand as a **gray starting anchor** (was a blank column the SVP read as missing data). Projection values stay **shipped-only** (honest floor); a hidden STAT band drives **4-color**: gray(elapsed) · green(covered on shipped) · **amber(covered ONLY if a not-yet-sailed container lands on time)** · red(uncovered even then). Visible legend + "on SHIPPED stock" label. `split_incoming_tiers` now also returns `half_arr_cp`. Committed `9307637`.
- ✅ **Day-by-day Inventory-Flow Calendar — NEW `build_inventory_calendar.py` (Jul 30).** Month-by-month calendar (weeks × days) per SKU; each day cell = projected on-hand (green/red), and the day a PO lands is marked with PO# + qty + confidence tier (✓ in-transit / ⚠ container-plan-not-sailed / ○ open-PO) + hover comment (received date). Covers **ShipBob + Amazon US + Amazon CA**. `py -3 scripts\build_inventory_calendar.py [UPC] [--channel shipbob|us|ca|all]`. First run: 1335 across all 3 channels.
- 📋 **OPEN — 1335 demand override:** rebuilds pull demand from Valogix (~15–17k/mo); Tommy's manual 24k Excel edit gets wiped on rebuild. Decide correct demand + add a persistent per-SKU `DEMAND_OVERRIDE` in `sku_rules` (like ABC_OVERRIDE) so it survives. At ~15–17k there is NO October gap (the crunch analysis assumed 24k).
- ✅ **ShipBob forecast — current-month actual override + rolling-forecast flag (SVP-driven, July blade spike).** Valogix col AC (current-month actual units sold, last history col) now preserved through `valogix_convert` as a `CurMonthActual` column. If this-month actuals > current-month forecast → actual takes over as that month's demand + **🚩 "check rolling forecast"** on the row. Skips phase-outs. **REQUIRES the full raw Valogix export (history+forecast).** 24 A-D items flagged (811573031335 SonicSmooth Clear: 23,855 actual vs low forecast).
- ✅ **ShipBob descriptions from item master / ShipBob's own Inventory Name, NOT amazon-sku-mapping** (fixed scrambled color labels — MIO Green was showing "Mint"). `build_desc_map` now sources SAP item-master `Item Description` first (UPC = truth). Supplier column removed. "Send-In Plan" tab → **"Vendor Order Plan"**.
- ✅ **Phase-out WITH stock now renders on the brand tab** ("sell through, DO NOT REPLENISH", demand zeroed) instead of hiding in Excluded; drops off at 0 stock. `E` class = phase-out. Removed 850003115139 (MIO Green, class A) + 850026141184 (PRIMA, class C) from PHASE_OUT; added `SHIPBOB_TRUE_SOURCE` (850003115139-1 = true green vs base = green/white mix, excluded from on-hand).
- ✅ **US planner: AWD Inventory Ledger ("tortuga") wired in** — `reports/_data/awd-ledger/` (per-brand). Ledger Ending Balance = authoritative AWD on-hand; AWD→FBA departures/day drives the FBA-thin flag (moving vs stalled). New **FBA-only DOS column** + "FBA thin but AWD full — watch AWD→FBA transfer" flag (`FBA_THIN_DAYS=30`). Send-in PO comments show destination (UNIS/Amazon) + exclude ShipBob-bound; fixed foreign (EU/AU/UK) POs leaking into US arrivals; added **"Runs out (no PO)" column**.
- ✅ **Coverage map: elapsed half-month buckets blanked** (projection starts at the run date, not a stale past bucket) + inventory-projection column gaps removed (Actions cols pack after the reservoir zone). ABC_OVERRIDE 850003115283 (SIMA Pink w/Bonus) E→A. `explain_sku.py` enriched.
- 📋 **SVP action items (2026-07-29)** captured at `[[15 Meetings & Decisions/(C) SVP Action Items — 2026-07-29.md]]` (blade shortage: Eunice→ShipBob transfer, 30k PO with Harry, pull Sept container to Aug, send SB position, weekly blade/Pro+/hair-spray forecast reviews).

**Recent work (Jul 27):**
- ✅ **Planner refinements — CA / Floship / inbound visibility (Jul 27, later)** —
  - **CA On Hand fix:** was counting FBA `available` only → badly undercounted (811573031335 showed 35 while 481 sat in Reserved FC Processing). CA On Hand now = `available + inbound-working + Reserved Staging + Reserved FC Processing` (matches US). 811573031335 → 516 (~127d, ties to Amazon's Total Days of Supply). US already had this.
  - **Inbound → FBA column (US + CA):** FBA `inbound-shipped` (units shipped to FBA, in transit) now shown as its own projection column — **NOT** in On Hand, **NOT** credited to coverage — so a shipped-but-unreceived load stays visible (catches stuck shipments). Aging/stuck flag still needs the *Manage FBA Inbound Shipments* report (per-shipment dates) — not yet wired.
  - **CA Alliance reservoir:** reads the Alliance/Hereford DIRECT "My Inventory on Hand" export via a style-safe zip/XML reader (openpyxl 3.14 crashes on it). **Remaining Quantity is in CASES** — multiply by the case-pack in the UoM code (`CS-24` → ×24). Total 9,894 u, cross-validates to SAP ASG exactly. `UNCA-*` is a **US** warehouse (added to US arrivals, excluded from CA); CA is Alliance `ASG-*` only.
  - **Floship:** matched BookFloship formatting (opaque `FF1F4E78` header, palette, title, target cell) + added a **Floship Plan** tab on the shared layout (coverage map + projection + send-in). Floship demand = trailing-12-mo avg monthly sales from order history (flat); On Hand = Shenzhen available (on-hand − reserved).
  - **sku_rules.DESCRIPTION_OVERRIDE** added (811573031410 → "Hair Identifier Spray"). Legacy `build_amazon_replen.py` archived; `build_all.py` runs the new US+CA planners.
- ✅ **Replenishment planner suite unified on a shared ShipBob-model layout (Jul 27)** — retired the formula-heavy legacy `build_amazon_replen.py` (archived to `MTB-SupplyChain/scripts/_archive/`) in favor of Python-computed planners that all render through ONE module `replen_layout.py` (single source of truth): `build_amazon_us_replen.py`, `build_amazon_ca_replen.py`, `build_shipbob_replen.py`. Every value computed in Python; only the coverage map + projection are formulas → **0 cross-sheet refs, standard functions only** (kills the column-letter `#REF`/`#NAME` fragility that broke the legacy).
  - **Layout:** Amazon = ASIN / SKU / short (item-master) Desc; ShipBob = UPC / Desc / Supplier. Half-month coverage map + inventory projection (Stockout Date, Send-in-to-cover) + two-part Actions log. All 3 filter to **Active & class A–D** (rest → Excluded).
  - **Amazon US** reconciles with the retired legacy: identical demand (51/51 UPCs, every month), on-hand effectively identical (dropping pending-removal-quantity per Tommy = −47u total), same 52 brand-tab rows (13/25/14) + 93 Excluded. Changes from legacy (both approved): drop pending-removal from on-hand; staging (ShipBob FREE-to-Transfer + Unis) is a send-in reservoir, NOT auto-credited into coverage.
  - **Amazon CA** is staging-fed from **Alliance (ASG-* only)** — `UNCA-*` is a US warehouse despite the name. Demand = CA FBA t90÷90 × US SoStocked seasonality shape; POs → CA phased at staging-ETA +60d; Alliance reservoir shown in the projection. 47 brand-tab rows (13/23/11).
  - **Warehouse routing:** US arrivals = AMZN-*/UNSC-*/UNCA-* + container; CA = ASG-* only. `build_all.py` now runs the US + CA planners (no more `amazon-replen-*.xlsx`).
  - **Also:** `sku_rules.DESCRIPTION_OVERRIDE` (short labels; first = 811573031410 → "Hair Identifier Spray"); deterministic row sort; ShipBob migration diff-validated 0 data diffs. Docs: `(C) Amazon Replen Planner — Formula & Math Reference.md` (legacy formula math preserved) + this CA SOP. MTB-SupplyChain commits `d669f76`→`e9b46a4`.
- ✅ **Task #7 singletons RESOLVED + SKU-map conflict guard shipped (Jul 27)** — both leftover FBA-position mismatches from the Jun 29 feeder work turned out to be the SAME root cause: a data-entry error in `amazon-sku-mapping.xlsx` where one product's Amazon Item No. was typed onto a *different* product's SAP row, so `sku_rules.resolve_upc` misrouted the wrong product's stock into the wrong UPC bucket.
  - **ECHO `860021001109`** (showed 4,703, should be 681): the SPA NFMD row had Soniclear Allure's Amazon # (`811573030468`) on ECHO's row → corrected the Amazon Item No. cell to `860021001109` (kept ECHO's ASIN B07MTMQ8XL). Soniclear now keeps its own 4,703; ECHO reads its true 681.
  - **NasalFresh base `850038082314`** (showed 6,707, should be ~6): the Dual-Powered bundle (`850038082383`, 6,700u — which has its OWN SAP UPC) was wrongly folded onto the base-kit UPC via two bad rows (`850038082383` + `850038082383-AMZ`). Removed both bad rows; Dual keeps UPC `850038082383`.
  - **Guardrail:** `sku_rules._load_map()` now records `MAP_CONFLICTS` when one Amazon SKU/FNSKU maps to >1 SAP UPC; new `warn_map_conflicts()` prints a build-time warning naming the SKU + conflicting UPCs + exact sheet/row. Wired into both replen planners' `build()` — an ECHO-type cross-wiring now announces itself instead of silently misrouting stock. (This guard is what surfaced the NasalFresh row conflict instantly.) Both planners rebuild green, zero conflicts. Mapping file backed up at `amazon-sku-mapping.BACKUP-2026-07-27.xlsx` (local, not versioned). MTB-SupplyChain repo commit `78186a2`.
- ✅ **Two-part persistent actions log in both replen planners (Jul 27)** — replaced the single editable "Actions taken" projection column with two: **✓ Actions — done (history)** (read-only, dated, compounds report-to-report) + **＋ New action (edit)** (editable). On rebuild, `planner_actions.harvest_and_promote()` reads the prior report's New-action column, stamps each entry with that report's as-of date, and moves it into the SKU's done-history (JSON store keyed by UPC/ASIN), then renders a fresh empty New-action field. ShipBob done=col R/new=col S; Amazon done=col T/new=col U. Round-trip verified. Repo commit `d669f76`.

**Recent work (Jun 29):**
- 🟡 **THIS WEEK feeder wiring — canonical row-fold (increment 2, Jun 29)** — Step 1 of the feeder brief. `build_report.main()` now folds duplicate Amazon US/CA rows that resolve to the same canonical SAP UPC into ONE row (right after the brain injection, before tabs build). Per-listing physical stock summed across ASINs; UPC-keyed fields kept from primary (no double-count); identical-SKU dupes collapse without summing. **White (811573031113) now renders ONCE** — daily 42.9, AWD inbound 4,188 (not doubled). 8 of 9 dup groups folded (Amazon US 139→135 rows, CA 77→73). One holdout left intentionally: `860021001109` (ECHO Black, Amazon SKU 811573030468) — its two rows carry different demand (72.66 vs 3.5/d) = distinct listings, not a pure dup. **Folded-row position is now set from the brain's canonical values (Step 3 for folded rows)** — initial summing version double-counted (Lavender 811573031090 → 9,966 vs true 4,972); switched to brain values, double-count-proof and verified (Lavender now 4,972; FBA-position 123/125 match brain). **Step 7 DONE (Jun 29):** 1410 (LEAD_TIME_OVERRIDE / ShipBob-replenished) was a phantom Amazon ORDER "Ship to AMZN-MT 16,895u" — now correctly routes to **TRANSFER 4,430u** (90-day cover). build_order_list flags `sb_replenished` slots + suppresses their Section-1 supplier PO (Section-2 transfer still runs); build_this_week_tab surfaces SB→AMZN suggestions in TRANSFER for items the 60-day staging trigger misses (on-hand credit from brain FBA+AWD position — item.on_hand read 0 and over-sized to 14,330; brain credit → correct 4,430). Acceptance #2 met. **REMAINING:** Step 3 *singletons* — ✅ RESOLVED Jul 27 (both `850038082314` and `860021001109` ECHO were mapping-file cross-wiring, not forensics — see Jul 27 entry above); Steps 4-5 (stockout cap, PO tranche matching) still open. Open design Q for Tommy: should SB→Amazon transfers target 90d cover (current) or match build_order_list's 60d trigger?
- ✅ **Cleanup Tier 1 + Tier 2 (Jun 29)** — **Tier 1:** deleted `build_report.BACKUP-2026-06-16.py` (untracked 15k-line dupe) + stale `__pycache__`; merged the duplicate vault folders `12_Attachments/` → `12 Attachments/` (git rename). **Tier 2 (single source of truth):** `build_order_list.PHASE_OUT_UPCS` was a hardcoded subset drifting from `sku_rules.PHASE_OUT` (we hit this adding the ECHO SKU). Now `build_order_list` re-exports `set(sku_rules.PHASE_OUT)` → canonical phase-out list lives ONLY in `sku_rules`; `build_report` (imports PHASE_OUT_UPCS from build_order_list) stays in sync automatically. Net: ORDER engine now also excludes 3 E-class phase-outs that were only in sku_rules (859886007043 / 850026141184 / 860021001154) — verified excluded, build clean. **Deliberately deferred** (Tier-3 / brain-rewire territory, too entangled to touch safely): the 4 `resolve_upc` copies + scattered lead/ROP/safety params.

**Recent work (Jun 24):**
- ✅ **Reconciliation Exposure column (Jun 24)** — renamed `Total` → **`Exposure ($)`** (units diff × unit cost, currency-formatted, sign-tinted) + added a plain-English **`What the exposure means`** column so the report reads on its own (e.g. "ShipBob holds 25 more units than SAP — $46 not yet in SAP (under-counted / found / pending receipt)"). `Difference` header clarified to "Difference (SAP − SB, units)". Subtotal/grand rows carry a net-direction note; negative-Committed warning moved into the meaning column; Confirmed shifted to col O. Verified clean on current data (TRUE DIFFERENCE −1,331u / −$62,179 net exposure). Inputs were stale (SAP 10d, ShipBob 14d) — refresh before acting on the dollar figures. **As-built spec now documented** at `10 System/SupplyChainClaude/Supply Chain Planning/inventory-reconciliation.md` (procedure + brand-partition join + computed-values/negative-Committed improvements + Exposure column). The operator procedure doc itself uses "exposure" for the difference-column dollar value, so the column is on-spec. (Spec lives in OneDrive-junction → versioned by OneDrive, not the vault repo.)
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
- **Email Brief & PO Tracker** — Outlook (MS365 connector, authorized) → daily prioritized brief + task list + self-updating PO tracker (stage machine off the 8-step PO workflow; stuck-PO flags). SPEC done 2026-07-30, Phases 1-2 POC'd; awaiting parameter sign-off (scope/cadence/vendors/escalation). ET timezone. Read-only.
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
| Amazon Seller Central FBA (US × 3 + CA × 3) | 6 | Weekly |
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

**Total:** ~36 files/week (LUMOS ShipBob dropped 2026-06-10; Alliance CA Inventory on Hand added 2026-06-10).
> **Correction (Tommy 2026-07-27):** SS **is** live on amazon.ca — the CA/SS FBA export has 74 active listings with real velocity (e.g. SIMA Dermaplaning ~3,496 u/mo). The prior "SS not on amazon.ca" note was stale. SS CA velocity comes from the CA FBA export (t90), not Sellerboard CA (SS still has no Sellerboard `canada/` folder). The Amazon CA planner covers all 3 brands.
> **Scope of the CA planner (Tommy 2026-07-28):** the CA FBA export is intentionally SHORT (only a handful of listings per brand) — those are the ONLY SKUs currently fulfilled from the Canada-dedicated warehouse (Alliance). Every other Amazon.ca listing is fulfilled from **US** inventory, so it lives in the US planner, NOT the CA/Alliance replen plan. A small CA row count is CORRECT, not a filtered/partial export — do NOT flag it. The list grows automatically as more SKUs move to Canada-only fulfillment (they appear in the CA FBA export → planner picks them up).

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
- *"Run the SPA ShipBob PO sizing"* — quarterly PO-sizing for all Spa items on ShipBob (`scripts/size_spa_pos.py`, 230d order-up-to). Plan/method: [[01 Purchasing & Inventory/(C) SPA ShipBob Quarterly PO Sizing.md]]
- *"Build the blade arrival map"* (or *"arrival map for <UPC>"*) — chronological arrival-timeline report for a SKU: in-transit (shipped) + container-plan POs with status + Harry's col-Q dates + running supply (`scripts/build_blade_arrival_map.py`; default 811573031335 SonicSmooth blades). Publishes to the SUPPLY CHAIN ANALYSIS hub. Reads Harry's hand-entered container-plan dates (col Q) — NOT just the plan's Ready column.
