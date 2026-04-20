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
**Last updated:** April 20, 2026
**Status:** demand_planning.py updated with critical velocity fix. 17 items need action. Report generated.

---

### ⚠️ CRITICAL VELOCITY FIX (Apr 20)
SoStocked velocity columns (Adj. Velocity, 30 Day Velocity) are already in **units/day** — NOT monthly totals. The previous script was dividing by 30, making every DOS calculation 30× too optimistic. Fixed.

Two other improvements also applied:
- **Adj. Velocity as primary** (corrects for stockout suppression — stocked-out products can't sell, so 30-day is artificially low)
- **INACTIVE_THRESHOLD = 0.1 units/day** — below this, stocked-out items go to "Low Vel Stockout" tracker instead of Priority Actions

---

### 🔴 Priority Actions (as of Apr 20 — based on Apr 16 data)
| Product | Brand | Market | Status | DOS | Vel/day | Lead |
|---|---|---|---|---|---|---|
| Sonicsmooth 2.0 Lavender | MTB | US | TRUE STOCKOUT | 0 | 1.0 | 117d |
| Soniclear Body Brush Head | MTB | US | TRUE STOCKOUT | 0 | 1.07 | 117d |
| Viva Foot Replacement Heads | SS | US | TRUE STOCKOUT | 0 | 1.0 | 60d |
| NF Salt Packets (Spanish) | NFMD | US | CRITICAL | 3 | 2.17 | 117d |
| Sonicblend Replacement Head | MTB | US | CRITICAL | 24 | 0.87 | 117d |
| Sonicsmooth Pro+ Peach | MTB | US | CRITICAL | 34 | 23.42 | 61d |
| Echo Pink | SS | US | CRITICAL | 34 | 1.13 | 60d |
| MIO Diamond Tip Pink | SS | US | CRITICAL | 36 | 1.03 | 60d |
| Mattifying Potion | SS | US | CRITICAL | 42 | 4.1 | 60d |
| NOVA Serum Infusion Head | SS | US | CRITICAL | 57 | 0.3 | 60d |
| Sonicblend Display Cradle | MTB | US | CRITICAL | 70 | 1.23 | 117d |
| Soniclear Elite White Marble | MTB | US | CRITICAL | 70 | 75.76 | 117d |
| Soniclear Replacement Face Brush Plum | MTB | US | CRITICAL | 82 | 9.63 | 117d |
| Replacement Face Brush (Clarisonic compat) | MTB | US | CRITICAL | 96 | 0.5 | 117d |
| Sonicsmooth 2.0 White | MTB | US | CRITICAL | 101 | 30.23 | 117d |
| Sonicsmooth Pro+ White | MTB | US | CRITICAL | 103 | 78.54 | 117d |
| BioMist MD Steam Inhaler | NFMD | US | CRITICAL | 104 | 0.47 | 117d |

---

### 🔵 Low Velocity Stockouts (tracked, not PO emergencies — <0.1 units/day)
- MTB CA: Sonicsmooth 1.0 White, Sonicsmooth 2.0 Lavender CA, Hydrojet CA, Sonicblend Makeup Brush CA, Sonicsmooth Pro+ Blade Refills CA, Hydraskim Bundle CA, LUMOS CA
- MTB US: Sonicblend Makeup Brush, Sonicsmooth 1.0 White, Hydrojet
- NFMD US: Hydrating Nose Oil, AM/PM Oil Bundle, Night Time Blend, Adjustable Nose Pillows (US+CA)
- NFMD CA: BioMist MD CA, Adjustable Nose Pillows CA
- SS: Viva CA, MIO CA, Ziva Lady Shaver US+CA, Cabezal Afeitadora US+CA, Pulverizador CA, Hydrating Detox Mask CA, Sima Deluxe Pink US

---

### ✅ Completed April 16
- ✅ **`analyze_sostocked.py` built and tested** — reads SoStocked Multi-Dashboard, filters noise, applies urgency tiers, outputs markdown. Fixed key bug: 0-velocity = INACTIVE not STOCKED OUT.
- ✅ **`demand_planning.py` built and tested** — full demand planning script using 3-file system. Runs clean, outputs Excel + markdown.
- ✅ **Three planning docs created** in vault `07 AI Tools & Builds/`
- ✅ **First demand plan Excel generated** — `demand-plan-2026-04-16.xlsx`

### ✅ Completed April 20
- ✅ **Critical velocity bug fixed in `demand_planning.py`** — velocity was being divided by 30 (treating units/day as monthly totals). Confirmed SoStocked exports daily rates.
- ✅ **Adj. Velocity added as primary** with 30-day fallback
- ✅ **INACTIVE_THRESHOLD (0.1/day) implemented** — Low Vel Stockouts tracked separately
- ✅ **New demand plan generated** — `demand-plan-2026-04-20.xlsx` (17 priority items)

---

### Scripts — What Each Does

**Script 1: `analyze_sostocked.py`**
- Location: `C:\Users\Tom Sapia\MTB-SupplyChain\analyze_sostocked.py`
- Input: SoStocked Multi-Dashboard Report (1 file, all 3 brands)
- Drop file in: `MTB-SupplyChain\reports\sostocked\`
- Run: `python analyze_sostocked.py`
- Output: markdown priority list → `outputs\sostocked-analysis-YYYY-MM-DD.md`
- Purpose: Quick weekly scan — what's stocked out, what's critical, what needs attention

**Script 2: `demand_planning.py`** ← PRIMARY SCRIPT
- Location: `C:\Users\Tom Sapia\MTB-SupplyChain\demand_planning.py`
- Inputs: 2 files (see below)
- Drop files in: `reports\agency\` and `reports\inventory\`
- Run: `python demand_planning.py`
- Output: Excel with 5 sheets → `outputs\demand-plan-YYYY-MM-DD.xlsx`
- Purpose: Full demand planning — DOS, stockout dates, reorder points, PO quantities

---

### Source Files for demand_planning.py

| File | Where to get it | Drop into |
|---|---|---|
| Agency Report (all 3 brands) | SoStocked → Multi-Dashboard Export | `MTB-SupplyChain\reports\agency\` |
| Inventory Report (all 3 brands) | SoStocked → Inventory Export | `MTB-SupplyChain\reports\inventory\` |

**NOT needed yet:** Projected Forecast file (SS only — will add MTB/NFMD forecasts later)

---

### Formula (Locked In)
```
Days of Supply = (FBA Stock/Market [inventory file] + AWD Warehouse Stock [agency col M]) ÷ Adj. Velocity [agency col P]

Order Qty = daily_velocity × (lead_time_days + 60 buffer_days) − total_available_stock

NOTE: Adj. Velocity and 30 Day Velocity from SoStocked are already in units/day. Do NOT divide by 30.
Fallback: if Adj. Velocity = 0, use 30 Day Velocity (col T).
```

**Region rules (applied automatically every run):**
- NAm → US
- US+MX → US
- MX → removed
- CA → kept separate

**Urgency tiers:**
- 🚨 AMAZON STOCKOUT — FBA=0 but warehouse stock exists (replenish FBA)
- 🔴 TRUE STOCKOUT — no stock anywhere (new PO needed)
- 🔴 CRITICAL — DOS ≤ lead time (at reorder point)
- 🟠 HIGH — DOS ≤ lead time + 30 days
- 🟡 WATCH — DOS ≤ 60 days
- 🟢 HEALTHY — DOS > 60 days
- ⚫ INACTIVE — zero velocity (dead/suppressed listings)

---

### What Still Needs to Be Done

**Script / Data bugs (from Apr 20 audit — see `07 AI Tools & Builds/(C) Demand Planning Audit — 2026-04-20.md`):**
- [ ] **FIX: Inbound to FBA bug** — 46,129 units showing as inbound for many MTB products (SoStocked aggregate bleed). Causes PO qty = 0 for ~10 CRITICAL items. Fix: remove inbound_fba from PO formula.
- [ ] **FIX: Add HIGH tier to dashboard** — 13 items not shown, including Blade Refills (236/day) and Hair Spray (143/day), both 6-7 days from flipping to CRITICAL.
- [ ] **INVESTIGATE: Is inbound 46,129 a real PO in SAP?** — Check SAP for large MTB shipment in transit.
- [ ] **GAP: Cost / Unit blank in SoStocked export** — Enter costs in SoStocked product settings OR build SAP cost lookup. Currently PO $ value = $0.
- [ ] **GAP: SS lead times = NaN in combined inventory file** — All SS defaults to 60d (probably OK but worth fixing). Try separate SS inventory export.
- [ ] Verify SS Canada CIRRA and NERA stockout flags — are these active CA listings or dead?
- [ ] Clean up SoStocked regional groupings (22 issues flagged by analyze_sostocked.py)
- [ ] Get MTB and NFMD forecast files from SoStocked (for future PO qty refinement)
- [ ] Decide report design for Django Reports Hub (need DOS/SVP input)
- [ ] Add `--json` flag to analyze_sostocked.py for Django integration
- [ ] Test demand_planning.py on Tommy's Windows machine end-to-end

---

### Key Docs in Vault
- `07 AI Tools & Builds/(C) SoStocked Reporting Module — Planning.md` — script architecture, Django integration paths
- `07 AI Tools & Builds/(C) Demand Planning Report — Build Plan.md` — meticulous build plan, formulas, open questions
- `07 AI Tools & Builds/(C) SoStocked Pipeline Discovery — 2026-04-15.md` — April 15 session findings

### Key Files in MTB-SupplyChain
- `MTB-SupplyChain/analyze_sostocked.py`
- `MTB-SupplyChain/demand_planning.py`
- `MTB-SupplyChain/outputs/demand-plan-2026-04-16.xlsx` ← first real report

---

### Architecture (Three Layers — Don't Rebuild These)
| Layer | Tool | Purpose |
|---|---|---|
| Knowledge | Obsidian vault (`C:\Users\Tom Sapia\supplychainbrain\`) | SOPs, planning docs, weekly snapshots |
| Execution | `C:\Users\Tom Sapia\MTB-SupplyChain\` | Scripts, raw data, output reports |
| Procurement | Django ERP (Mac dev → GitHub → PythonAnywhere) | POs, invoicing, Reports Hub (planned) |
