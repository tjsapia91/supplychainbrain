# SupplyChainBrain
This is Tommy's operational brain for his role as Supply Chain Manager at Michael Todd Beauty — an $80M beauty company managing 3 brands across multiple sales channels with international expansion on the horizon. This brain is built to organize chaos, track what matters, and make Claude an effective supply chain thinking partner.

GitHub (private): https://github.com/tjsapia91/supplychainbrain
Syncs between: Personal machine (Obsidian vault) ↔ Work machine (Claude Code)

## ⚠️ SESSION SYNC RULE
At the end of every session, update this file's Current Status section with what changed.

This brain is used from both personal and work machines. Neither Claude instance shares memory — this file IS the shared memory. Before ending any session:

- Update "Current Status" with what was done
- Push changes: `git add . && git commit -m "description" && git push origin main`
- On the other machine: `git pull` to get the updates

If you are Claude and the user is ending the session, remind them to let you update this file and push first.

---

## Claude's Role
Claude operates here as a supply chain operations partner — part analyst, part strategist, part automation builder. The job is to help Tommy manage complexity across 3 brands, multiple channels, multiple 3PLs, and a growing international footprint.

- **Demand planning partner** — help analyze forecasts, spot trends, flag risks across brands and channels
- **Process builder** — help document and improve SOPs as Tommy learns and optimizes the role
- **Tool builder** — help build and improve AI-powered tools (ERP, dashboards, automation) that reduce the number of screens Tommy needs to look at
- **Strategic thinker** — help think through vendor decisions, 3PL transitions, international expansion logistics
- **Dashboard consolidator** — Tommy is drowning in dashboards (SoStocked, Sellerboard, SAP, Valogix, TrueOps, Excel). Help centralize and simplify.
- **Knowledge capture** — as Tommy learns this role, help him document what he's learning so nothing gets lost

If a session is drifting without moving toward clearer operations, better systems, or concrete next actions — nudge me back: *"What's the one thing that moves the supply chain forward today?"*

---

## The Company
Michael Todd Beauty — $80M/year beauty company

**Three brands:**
- Michael Todd Beauty (MTB) — flagship brand
- NasalFresh MD (NFMD) — nasal/health brand
- Spa Sciences (SS) — spa/beauty brand

Each brand has its own Amazon login, products, and forecasts.

**Sales Channels:**
- Amazon (separate accounts per brand)
- Walmart Marketplace
- TikTok Shop
- Shopify
- Nordstrom
- And more

**3PLs (Fulfillment):**
- Floship
- ShipBob (possibly transitioning to AmzPrep — not final)

**Tools Currently in Use:**
- SoStocked — inventory/forecasting
- Sellerboard — Amazon analytics
- SAP — ERP
- Valogix — demand planning
- TrueOps — operations management
- Excel — everything else
- Claude — manual prompting for analysis and tool building
- Custom ERP (built by Tommy in week 1)
- Custom QuickBooks-like tool (built by Tommy for golf cart business)

---

## Supply Chain Team
- Tommy — Supply Chain Manager (#2 on the team, 4-person team)
- Direct boss — Director of Supply Chain (DOS)
- SVP of Operations — senior leadership, works closely with Tommy
- 1 other team member

---

## What I Manage
- Purchasing
- Inventory management
- Freight
- Forecast analysis & demand planning (across all 3 brands and channels)
- 3PL relationships
- Still learning — more responsibilities TBD

---

## Process
1. **Monitor** — Check forecasts, inventory levels, sales velocity across brands and channels
2. **Analyze** — Run demand planning, identify trends, flag stockout risks or overstock situations
3. **Purchase** — Create and manage POs based on forecast and lead times
4. **Coordinate** — Work with 3PLs, vendors, and internal team on fulfillment and freight
5. **Build** — Create AI tools and automations that make all of the above faster and easier
6. **Document** — Write SOPs for every process as it's figured out
7. **Report** — Track key metrics and surface insights to leadership

---

## Folder Structure
```
SupplyChainBrain/
├── CLAUDE.md                          ← You are here
├── COMMANDS.md                        ← Available skills and commands
├── 00 Forecast & Demand Planning/     ← Forecasts, demand analysis, planning
│   ├── MTB/                           ← Michael Todd Beauty forecasts
│   ├── NFMD/                          ← NasalFresh MD forecasts
│   └── SS/                            ← Spa Sciences forecasts
├── 01 Purchasing & Inventory/         ← POs, inventory tracking, reorder points
├── 02 Vendors & Suppliers/            ← Vendor profiles, lead times, contacts, performance
├── 03 3PL & Fulfillment/             ← Floship, ShipBob/AmzPrep, fulfillment ops
├── 04 Sales Channels/                 ← Amazon, Walmart, TikTok, Shopify, Nordstrom notes
├── 05 International Expansion/        ← Customs, compliance, freight, new markets
├── 06 Processes & SOPs/               ← Standard operating procedures as you build them
├── 07 AI Tools & Builds/              ← ERP, dashboards, automations — prompts and docs
├── 08 Key Metrics & Dashboards/       ← Numbers that matter, tracking, receipts
├── 09 People & Relationships/         ← Who's who, how to work with them
├── 10 System/                         ← Scripts, config, reusable processes
├── 11 Skills/                         ← Skill markdown files
├── 12 Attachments/                    ← Images, screenshots, PDFs
├── 13 Iteration Logs/                 ← What to improve, retrospectives
├── 14 Learning & Development/         ← What you're learning about supply chain, the company, the industry
└── 15 Meetings & Decisions/           ← Key meetings, decisions made, action items
```

---

## Rules & Conventions
- **(C) prefix** — Files created by Claude are prefixed with `(C)` so it's clear they're AI-generated.
- **Editing rule** — Before editing any file without the `(C)` prefix, ask for permission first.
- **Work in small steps.** Don't dump walls of information. Each thing needs to register.
- **Be blunt.** If a process is inefficient, say so. If I'm overcomplicating something, call it out.
- **Brand abbreviations** — Use MTB, NFMD, SS when referring to brands.
- **Skills** — All reusable scripts/automations are saved as markdown files in the Skills folder, NOT as Claude Code skills.

---

## Current Status
**Last updated:** April 27, 2026 (evening — wrapping up to resume tomorrow)
**Status:** Full pipeline rebuild PLUS multi-marketplace integration (Valogix). Weekly report now spans Amazon · Shopify · Walmart · Floship · Spa Sciences DTC. **573 total item × channel rows** (177 Amazon + 396 Valogix). Output: `outputs/2026-04-27/weekly-report-2026-04-27.xlsx` + `demand-plan-2026-04-27.xlsx` + `action-plan-2026-04-27.xlsx` + new `wm-marketplace-review-2026-04-27.xlsx`.

---

### 🛑 PICK UP HERE TOMORROW

**Last thing we were doing:** Fixing ABC classification gaps across the report.
- ✅ Expanded `ABC_STYLE` palette to cover all 9 codes (A/B/C/D/E/F/I/S/Z) — was only A/B/C
- ✅ Added `_normalize_sku_for_lookup()` to strip suffixes (`-M`, `AMZ-stickerless`, `MT-` prefix) so Amazon SKU variants match bare UPCs in item master
- ⏳ **Still TODO**: Some items have custom non-UPC SKU codes (e.g. `BODYBRBLK`) that need a manual alias map. Tommy to provide list of these custom codes → UPC mappings.
- ⏳ **Still TODO**: 28 Valogix UPCs aren't in the item master — either add to item master or accept the gap.

**Next session priorities:**
1. Manual alias map for custom Amazon SKU codes (BODYBRBLK → 859886007791, etc.)
2. Walmart Marketplace SKU review — Tommy fills out `wm-marketplace-review-2026-04-27.xlsx` (94 items, 14 auto-flagged as zombies). Decisions feed back into Multi-Channel dashboard to phase out items.
3. Once WM review done, do the same review pattern for Shopify (SBGA-MT 121 SKUs), Spa Sciences DTC (SBGA-SS 163 SKUs), Floship (FLO-MTB 18 SKUs)
4. Owner-meeting walkthrough of the Weekly Summary tab — rehearse the narrative

---

### 🔴 Priority Actions (Apr 27 — current week)
| Product | Brand | Market | Status | DOS | Stockout | Vel/day |
|---|---|---|---|---|---|---|
| Soniclear Replacement Body Brush Head | MTB | US | TRUE STOCKOUT | 0 | Apr 27 | 1.0 |
| Pulverizador de agua faci (SS Spanish) | SS | US | CRITICAL | 18 | May 15 | 0.17 |
| Sonicblend Replacement Head | MTB | US | CRITICAL | 40 | Jun 06 | 1.13 |
| Nova Pink | SS | US | CRITICAL | 40 | Jun 06 | 13.07 |
| NOVA Serum Infusion Head | SS | US | CRITICAL | 42 | Jun 08 | 0.33 |
| Sonicblend Display Cradle | MTB | US | CRITICAL | 52 | Jun 18 | 1.43 |
| Soniclear Replacement Face Brush (Plum) | MTB | US | CRITICAL | 71 | Jul 07 | 10.7 |
| Sonicsmooth Pro+ White | MTB | US | CRITICAL | 77 | Jul 13 | 91.33 |

---

### ✅ Completed April 27 (evening session — multi-marketplace)

**Valogix Integration (NEW):**
- ✅ **Valogix CSV moved to pipeline** — `reports/valogix/schain_itemLocationHistoryForecast_*.csv` is now a standard weekly input. 396 item × location rows across 4 channels: Floship, Shopify MTB, Spa Sciences DTC, Walmart Marketplace
- ✅ **`load_valogix()` function** in build_report.py — reads the CSV, computes DOS = on_hand / (12mo forecast ÷ 365), per-channel status (STOCKOUT / BELOW ROP / LOW / HEALTHY / NO DEMAND)
- ✅ **`build_cost_lookup()`** — builds UPC → unit cost map from Valogix Inventory Cost field. **244 UPCs now have real cost data** — fills the long-standing cost gap. PO $ values now populate correctly
- ✅ **`build_multichannel_dashboard()`** — new sheet 🌐 Multi-Channel with KPI tiles, channel snapshot matrix, and one flat filterable list of all 396 marketplace items (auto-filter on header)

**Weekly Summary upgraded to multi-marketplace:**
- ✅ **5 KPI tiles** now span all marketplaces: Active SKUs · Priority Actions · Warning/High · On-Hand Value · On Order
- ✅ **Marketplace Snapshot section** added — one row per marketplace (Amazon FBA+AWD / Shopify MTB / Floship / Spa Sciences DTC / Walmart) with SKUs · On Hand · On Hand $ · On Order · 12mo Forecast · Need Action · Healthy
- ✅ **Priority Actions + High Tier sections now span all marketplaces** — combined Amazon + Valogix items, sorted by status urgency then DOS
- ✅ **MARKETPLACE column added** — shows where each priority/high item lives (Amazon US, Shopify MTB, Walmart, etc.)
- ✅ **ASIN column added** to all Amazon detail tables

**Color palette switched to muted:**
- Brick (#B85042) instead of bright red, sage (#6B8E5A) instead of bright green, amber (#B5894A) instead of yellow, slate (#8B96A0) instead of gray
- Easier on the eyes for owner-facing weekly meeting

**ABC Classification fixes:**
- ✅ Expanded ABC_STYLE to cover all 9 codes (A/B/C/D/E/F/I/S/Z) instead of just A/B/C
- ✅ SKU normalization for lookup — strips `-M`, `AMZ-stickerless`, `MT-` prefix etc. so Amazon SKU variants match bare UPCs
- 81% of Amazon items now show a colored ABC badge (was ~17%)

**Walmart Marketplace SKU Review (NEW):**
- ✅ `outputs/2026-04-27/wm-marketplace-review-2026-04-27.xlsx` built — 94 WM SKUs, sorted alphabetically
- ✅ 14 zombie items auto-flagged (zero on hand + zero forecast + zero history) — yellow highlight, "AUTO?" in Phase Out column
- ✅ Reusable builder script: `scripts/build_wm_marketplace_review.py`
- Tommy to fill out Active Y/N, Phase Out, Notes columns

**Cross-channel inventory lookups (this session):**
- B0758J2X6J — Sonicsmooth White Bundle: 0 (likely discontinued)
- B0758JDTXK — Sonicsmooth Lavender 2021 USB: 8,359 (Shopify 8,183 + Floship 176)
- B08D6X47HS — MicroSmooth Tips Fine/Coarse: 0 (true stockout)
- B08WB2L1M1 — Soniclear Elite Pink Sakura: 519 (FBA 1 + AWD 200 + Shopify 318)
- B0GHSN7NFB — Sonicsmooth Pro+ Dermaplane: 382 (Amazon FBA only — ~4 days at velocity)

---

### ✅ Completed April 27 (morning session)

**Repo Restructure:**
- ✅ **Moved all scripts to `scripts/`** — demand_planning.py, build_report.py, build_action_plan.py, combine_forecast.py, run_weekly_supply_chain_analysis.py, generate_weekly_excel.py
- ✅ **Moved all docs to `docs/`** — WEEKLY_CHECKLIST.md, SoStocked_Full_Automation_Agent.md, and other reference files
- ✅ **Dated output subfolders** — all outputs now save to `outputs/YYYY-MM-DD/` (e.g. `outputs/2026-04-27/`)
- ✅ **Fixed BASE path** in all scripts: `BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))` — scripts work from any location after the move
- ✅ **UTF-8 fix** — added `sys.stdout.reconfigure(encoding="utf-8", errors="replace")` to prevent Windows cp1252 crashes on emoji output

**SKU Review Integration:**
- ✅ **`load_sku_review()` function** in demand_planning.py — reads `sku-review-YYYY-MM-DD.xlsx`, returns inactive_asins, phase_out_asins, replenish_notes (ASIN → col N text)
- ✅ **Inactive items fully excluded** from all report sheets (not shown anywhere)
- ✅ **Phase-out items fully excluded** from all report sheets (deplete and done, no PO recommended)
- ✅ **Replenish From column (col N)** injected as `replenish_source` field — flows through JSON into all Excel sheets
- ✅ **ABC classification** added to dashboard priority table

**DOS Formula Fix — AWD Inbound:**
- ✅ **`load_awd_inbound()` function** — reads `reports/seller-central/awd-*.csv` (skiprows=3), maps ASIN → "Inbound to AWD (units)"
- ✅ **DOS formula updated**: `total_stock = fba_market + wh_stock (AWD available) + awd_inbound (AWD in transit)`
- ✅ **Validated**: Soniclear Elite White Marble corrected from DOS 69 (CRITICAL, Jul 5) → DOS 131 (HIGH, Sep 5) after including 4,872 AWD inbound units. 0 formula errors across all 177 items.

**Report Design Improvements:**
- ✅ **FBA Pipeline column** — condensed 3 in-transit columns (Inbound Shipped, At FC Pending, AWD→FBA Outbound) into one "FBA PIPELINE" display column in all sheets. Underlying data still in JSON.
- ✅ **New 📊 Weekly Summary sheet** — first sheet in weekly-report Excel. Shows KPI tiles, brand breakdown (SS/MTB/NFMD), priority items section, high items section, FBA replen section. Single-page executive view.
- ✅ **`build_executive_summary()` function** added to build_report.py

**Action Plan Script:**
- ✅ **`build_action_plan.py` built** — reads filled sku-review + demand plan JSON, generates 3-tab action plan Excel:
  - 🚚 ShipBob Send-ins — FBA replenishment from ShipBob
  - 📦 Supplier POs — purchase orders to place with manufacturers
  - ⚫ Inactive & Phase Out — no action needed
- ✅ **Nova Pink special case** — 700 units from ShipBob first, balance (~137 units) on Supplier PO
- ✅ **Saved to**: `outputs/2026-04-27/action-plan-2026-04-27.xlsx`

**ShipBob Item Reference:**
- ✅ **BODYBRBLK recorded** — Soniclear Replacement Body Brush Head (ASIN B07D2HWLPM) = ShipBob item **859886007791**. Updated in sku-review-2026-04-27.xlsx col N and flows through to replenish_source in all reports.

---

### ⚠️ CRITICAL VELOCITY FIX (Apr 20 — still applies)
SoStocked velocity columns (Adj. Velocity, 30 Day Velocity) are already in **units/day** — NOT monthly totals. Do NOT divide by 30.

---

### ⚠️ AWD INBOUND NOW IN DOS FORMULA (Apr 27)
AWD inbound units (in transit from supplier → AWD) are now included in total_stock for DOS calculation. Source: `reports/seller-central/awd-*.csv`. This is an ASIN-level number — CA market rows share the same AWD inbound figure, which may slightly inflate CA DOS. Watch for this.

---

### What Still Needs to Be Done

**Agent / Automation:**
- [ ] **Schedule the agent** — set up Monday 8am recurring trigger via Windows Task Scheduler
- [ ] **Test full agent run on Windows machine end-to-end** — verify PowerShell paths, Python env, all 6 downloads

**ShipBob Item References — Resolved Apr 27:**
All SB item numbers confirmed = UPC barcode (same as SAP item no.). Source: `Downloads/Amazon SKU Numbers In SAP (1).xlsx` + sku-review col F.

| Product | ASIN | ShipBob Item No. (UPC) | Updated in sku-review |
|---|---|---|---|
| Soniclear Replacement Body Brush Head | B07D2HWLPM | 859886007791 | ✅ |
| Sonicblend Replacement Head | B07CRS2PDJ | 859886007739 | — |
| NOVA Serum Infusion Head | B01ND4R0NU | 859886007722 | — |
| Sonicblend Display Cradle | B07D2JYZ2V | 859886007043 | — |
| Soniclear Elite White Marble | B08WB2L1M1 | 811573030093 | — |
| LUMOS | B0DCQTWWHN | 811573031397 | — |
| Sonicsmooth Pro+ White | B0D1GLNW5C | 811573031366 | — |
| Pulverizador (NANO MISTER) | B09B16JH5G | 850026141306 | ✅ |
| Sonicsmooth Hair Identifier Spray | B0DSLQKVVL | 811573031410 | ✅ |

**Data Gaps:**
- [ ] **Cost / Unit blank** — PO $ value = $0 across all items. Enter costs in SoStocked OR build SAP cost lookup.
- [ ] **CA AWD inbound double-counting** — AWD inbound is ASIN-level, applied to both US and CA rows. May inflate CA DOS. Monitor.
- [ ] **Inbound to FBA (46,129 units)** — Verify in SAP whether this is a real MTB PO in transit. If not, this was SoStocked aggregate bleed (previously excluded from formula — now irrelevant since we use AWD inbound instead).
- [ ] Clean up SoStocked regional groupings (22 issues previously flagged)
- [ ] Get MTB and NFMD forecast files from SoStocked (for future PO qty refinement)

**Reporting:**
- [ ] Decide final design for Django Reports Hub (need DOS/SVP input)
- [ ] Add `--json` flag to analyze_sostocked.py for Django integration

---

### Scripts — What Each Does (Updated Apr 27 evening)

All scripts now live in `MTB-SupplyChain\scripts\`. Run from the repo root:
```
cd C:\Users\Tom Sapia\MTB-SupplyChain
python scripts\demand_planning.py
python scripts\build_report.py
python scripts\build_action_plan.py
python scripts\build_wm_marketplace_review.py   # WM Marketplace SKU review (new)
```

**`demand_planning.py`** ← PRIMARY SCRIPT (Amazon)
- Input: Weekly Forecast (`reports\weekly\Weekly_Forecast_*.xlsx`) + AWD inbound CSV (`reports\seller-central\awd-*.csv`) + filled SKU review (`outputs\YYYY-MM-DD\sku-review-YYYY-MM-DD.xlsx`)
- Output: `outputs\YYYY-MM-DD\demand-plan-YYYY-MM-DD.xlsx` + `.json` + `.md`
- Does: Amazon DOS calc (FBA + AWD available + AWD inbound), PO qty, urgency tiers, excludes inactive/phase-out

**`build_report.py`** ← MULTI-MARKETPLACE
- Input: `demand-plan-YYYY-MM-DD.json` + Valogix CSV (`reports\valogix\`) + FBA/AWD CSVs + item master
- Output: `outputs\YYYY-MM-DD\weekly-report-YYYY-MM-DD.xlsx` (7 sheets)
- Does: Formats Excel dashboard with multi-marketplace executive summary, priority actions, inventory overview, brand breakdowns
- **Tabs**: 📊 Weekly Summary · 🌐 Multi-Channel · 📊 Dashboard · 📋 Inventory Overview · 🚨 Priority Actions · ✅ Action Plan · MTB / SS / NFMD

**`build_action_plan.py`**
- Input: `sku-review-YYYY-MM-DD.xlsx` + `demand-plan-YYYY-MM-DD.json`
- Output: `outputs\YYYY-MM-DD\action-plan-YYYY-MM-DD.xlsx` (3 tabs)
- Does: Translates SKU review decisions into ShipBob send-ins, Supplier POs, Inactive/Phase-out list

**`build_wm_marketplace_review.py`** ← NEW
- Input: Valogix CSV
- Output: `outputs\YYYY-MM-DD\wm-marketplace-review-YYYY-MM-DD.xlsx`
- Does: Walmart Marketplace SKU review template — auto-flags zombie items (zero stock + zero forecast + zero history)

**`combine_forecast.py`**
- Input: 6 individual SoStocked CSV downloads in `reports\sostocked\`
- Output: Combined `Weekly_Forecast_*.xlsx` in `reports\weekly\`

---

### Required Input Files (Weekly)

| File | Source | Drop Into |
|---|---|---|
| Weekly Forecast (all 3 brands) | SoStocked → 6 brand/market exports → combine_forecast.py | `reports\weekly\` |
| AWD Inbound report | Amazon Seller Central → AWD → Inventory → Export | `reports\seller-central\` |
| FBA Inbound report (per brand) | Amazon Seller Central → FBA Inventory → Export | `reports\seller-central\` |
| Valogix Item-Location-Forecast | Valogix export — `schain_itemLocationHistoryForecast_*.csv` | `reports\valogix\` |
| SKU Review (filled in) | Tommy fills out sku-review sheet from prior run | `outputs\YYYY-MM-DD\` |

---

### Formula (Locked In — Updated Apr 27)
```
Days of Supply = (FBA Stock + AWD Available Stock + AWD Inbound) ÷ Adj. Velocity

Order Qty = daily_velocity × (lead_time_days + 60 buffer_days) − total_stock

NOTE: Adj. Velocity and 30 Day Velocity from SoStocked are already in units/day. Do NOT divide by 30.
Fallback: if Adj. Velocity = 0, use 30 Day Velocity.
AWD Inbound source: reports/seller-central/awd-*.csv, col "Inbound to AWD (units)", skiprows=3
```

**Urgency tiers:**
- 🚨 AMAZON STOCKOUT — FBA=0 but warehouse stock exists (replenish FBA)
- 🔴 TRUE STOCKOUT — no stock anywhere (new PO needed)
- 🔴 CRITICAL — DOS ≤ lead time (at reorder point)
- 🟠 HIGH — DOS ≤ lead time + 30 days
- 🟡 FBA REPLENISHMENT — FBA empty but ShipBob stock > 30 days (routine send-in)
- 🟢 HEALTHY — DOS > lead time + 30 days
- 🔵 LOW VEL STOCKOUT — stocked out but velocity < 0.1/day (tracked, not a PO emergency)

---

### Key Docs in Vault
- `07 AI Tools & Builds/(C) SoStocked Reporting Module — Planning.md` — script architecture, Django integration paths
- `07 AI Tools & Builds/(C) Demand Planning Report — Build Plan.md` — meticulous build plan, formulas, open questions
- `07 AI Tools & Builds/(C) SoStocked Pipeline Discovery — 2026-04-15.md` — April 15 session findings

### Key Files in MTB-SupplyChain
- `scripts/demand_planning.py` — primary demand planning script
- `scripts/build_report.py` — Excel dashboard builder
- `scripts/build_action_plan.py` — action plan generator (new Apr 27)
- `scripts/combine_forecast.py` — SoStocked CSV combiner
- `outputs/2026-04-27/weekly-report-2026-04-27.xlsx` ← current week
- `outputs/2026-04-27/action-plan-2026-04-27.xlsx` ← current action plan

---

### Architecture (Three Layers — Don't Rebuild These)
| Layer | Tool | Purpose |
|---|---|---|
| Knowledge | Obsidian vault (`C:\Users\Tom Sapia\supplychainbrain\`) | SOPs, planning docs, weekly snapshots |
| Execution | `C:\Users\Tom Sapia\MTB-SupplyChain\` | Scripts, raw data, output reports |
| Procurement | Django ERP (Mac dev → GitHub → PythonAnywhere) | POs, invoicing, Reports Hub (planned) |
