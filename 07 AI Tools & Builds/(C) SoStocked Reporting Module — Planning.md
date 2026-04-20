# SoStocked Reporting Module — Planning Doc
**Last updated:** April 16, 2026
**Status:** In progress — script built, Django integration in design phase

---

## File Paths — Everything in One Place

### Scripts & Execution Layer
| File | Path |
|---|---|
| Main analysis script | `C:\Users\Tom Sapia\MTB-SupplyChain\analyze_sostocked.py` |
| SoStocked report drop folder | `C:\Users\Tom Sapia\MTB-SupplyChain\reports\sostocked\` |
| Script outputs (markdown reports) | `C:\Users\Tom Sapia\MTB-SupplyChain\outputs\` |
| Weekly output filename | `outputs\sostocked-analysis-YYYY-MM-DD.md` |

### Obsidian Vault (Knowledge Layer)
| Folder | Path |
|---|---|
| Vault root | `C:\Users\Tom Sapia\supplychainbrain\` |
| Demand planning root | `C:\Users\Tom Sapia\supplychainbrain\00 Forecast & Demand Planning\` |
| MTB brand snapshots | `C:\Users\Tom Sapia\supplychainbrain\00 Forecast & Demand Planning\MTB\` |
| SS brand snapshots | `C:\Users\Tom Sapia\supplychainbrain\00 Forecast & Demand Planning\SS\` |
| NF brand snapshots | `C:\Users\Tom Sapia\supplychainbrain\00 Forecast & Demand Planning\NF\` |
| AI Tools & Builds (this doc) | `C:\Users\Tom Sapia\supplychainbrain\07 AI Tools & Builds\` |
| Processes & SOPs | `C:\Users\Tom Sapia\supplychainbrain\06 Processes & SOPs\` |

### Django ERP (Procurement Layer)
| Resource | Path / URL |
|---|---|
| Local dev machine | Mac |
| Version control | GitHub (private) — https://github.com/tjsapia91 |
| Live app | PythonAnywhere (deployed) |
| Local project root | `~/` on Mac — confirm exact path |
| Reports Hub | Not yet built — planned addition |

### This Planning Doc
`C:\Users\Tom Sapia\supplychainbrain\07 AI Tools & Builds\(C) SoStocked Reporting Module — Planning.md`

---

## What We're Building

A demand planning reporting module that reads SoStocked inventory data and surfaces actionable weekly priorities across all 3 brands (MTB, SS, NFMD). Eventually lives inside the Django ERP as a Reports Hub. For now, runs as a standalone Python script.

---

## Current State — What's Built

### Script: `analyze_sostocked.py`
**Location:** `C:\Users\Tom Sapia\MTB-SupplyChain\analyze_sostocked.py`

**What it does:**
1. Finds the latest SoStocked Multi-Dashboard Report in `reports/sostocked/`
2. Loads all 262 rows across 3 brands (MTB, SS, NFMD)
3. Filters out noise (zero velocity + zero stock = dead/inactive listings)
4. Applies urgency tiers to every active row
5. Outputs a console summary + full markdown report
6. Saves per-brand snapshots to the Obsidian vault

**Weekly workflow (once script is integrated):**
1. Download SoStocked Multi-Dashboard Report (one click, all 3 brands)
2. Drop file into `MTB-SupplyChain/reports/sostocked/`
3. Run `python analyze_sostocked.py`
4. Review priority list — ~10 minutes total

---

## Data Structure

### Source File
- SoStocked Multi-Dashboard Report (All Accounts)
- Format: `.xlsx`, single sheet: `Inventory - Full Report`
- Coverage: 262 rows, 27 columns, all 3 brand accounts in one export

### Key Columns Used

| Script Name | SoStocked Column | Description |
|---|---|---|
| `brand` | Account Name | MTB / Spa Sciences / Nasalfresh MD |
| `market` | Marketplace | US, CA, MX, NAm, US+MX |
| `product` | Product Name | Full product name |
| `days_supply` | Days of Supply on AMZ | Pre-calculated by SoStocked |
| `stockout_date` | Next Stock Out Date | Projected stockout |
| `fba_stock` | Total FBA Stock | Units at Amazon |
| `wh_stock` | Total Warehouse Stock | Units at 3PL/warehouse |
| `velocity_adj` | Adj. Velocity | Adjusted daily sales velocity |
| `velocity_30` | 30 Day Velocity | 30-day rolling average |

### Urgency Tiers

| Tier | Label | Emoji | Condition |
|---|---|---|---|
| 0 | STOCKED OUT | 🔴 | FBA stock = 0 AND velocity > 0 (real demand, no inventory) |
| 1 | CRITICAL | 🔴 | ≤14 days supply with velocity |
| 2 | HIGH | 🟠 | ≤30 days supply |
| 3 | WATCH | 🟡 | ≤60 days supply |
| 4 | HEALTHY | 🟢 | >60 days supply |
| 5 | NO DATA | ⚪ | Days supply not available |
| 6 | INACTIVE | ⚫ | 0 velocity (suppressed/dead listing — not an inventory emergency) |

**Critical distinction fixed in v2:** SoStocked shows `0 days supply` when velocity = 0 (can't divide by zero). The old logic flagged these as STOCKED OUT. The new logic separates them as INACTIVE — 61 rows that looked like fires are actually dead/suppressed listings. Real action items went from 72 → 11.

### Noise Filtering Logic
Two types of rows are filtered out before analysis:
- **MX standalone + zero velocity** — regional grouping artifact, skews data
- **Zero velocity + zero FBA + zero WH stock** — completely inactive listing, nothing to act on

---

## Current Weekly Output (April 16 run against Apr 15 data)

### Summary Table

| Brand | 🔴 Stocked Out | 🔴 Critical (≤14d) | 🟠 High (≤30d) | 🟡 Watch (≤60d) | 🟢 Healthy | ⚫ Inactive |
|---|---|---|---|---|---|---|
| Spa Sciences | 3 | 1 | 0 | 13 | 54 | 35 |
| Michael Todd | 4 | 0 | 2 | 9 | 19 | 21 |
| Nasalfresh MD | 1 | 2 | 0 | 6 | 14 | 5 |

### True Stockouts (FBA=0, actively selling)

| Product | Brand | Velocity | WH Stock | Action |
|---|---|---|---|---|
| AIVA Deluxe | SS | 7.5/day 🔥 | 924 | Send FBA replenishment — stock exists |
| NERA Gray Shower Brush | SS | 1.5/day | 720 | Send FBA replenishment — stock exists |
| Viva Foot Replacement Heads | SS | 1.0/day | 0 | New PO needed |
| Sonicsmooth 2.0 Lavender | MTB | 1.0/day | 0 | New PO needed |
| Soniclear Body Brush Head | MTB | 1.07/day | 0 | New PO needed |
| NASALFRESH Hydrating Nose Oil | NFMD | 0.03/day | 0 | Low velocity — monitor |

### Critical (≤14 days supply)

| Product | Brand | Days Left | Out Date |
|---|---|---|---|
| NF Salt Packets (US) | NFMD | 5 days | Apr 20 |
| NF Premium Bundle (CA) | NFMD | 5 days | Apr 20 |
| ECHO Brush Replacement Head | SS | 12 days | ~Apr 28 |

### High (≤30 days supply)

| Product | Brand | Days | Velocity | Note |
|---|---|---|---|---|
| Sonicsmooth Pro+ White | MTB | 18d | 78.54/day | Moving fast — needs PO soon |
| Sonicsmooth Pro+ Peach | MTB | 21d | 23.42/day | Watch closely |

---

## Regional Grouping Issues (SoStocked Cleanup Needed)

22 issues flagged by the script. Key categories:

- **MX rows with velocity** — 2 MTB products tracked separately in MX with real sales (Sonicsmooth 2.0 Lavender, Sonicsmooth 2.0 Pink). Should be grouped with US.
- **Absurd days supply** — 20 SS rows with 500–16,994 days supply at <0.1 velocity/day. These are near-dead listings (SS skincare line, Spanish-language products). Consider hiding or disabling marketplace.
- **Duplicate US/US+MX grouping** — LUMOS Laser IPL Hair Removal has both US and US+MX groupings simultaneously — conflicting regions.

**Recommended cleanup order:**
1. Fix US/US+MX duplicate for LUMOS first (hardest conflict)
2. Group MTB MX listings with US (Sonicsmooth Pink/Lavender)
3. Review and disable the near-zero SS skincare listings if truly inactive

---

## Django Integration — Three Paths

### Option A — File-based bridge (quickest, build now)
Script writes JSON alongside the markdown. Django reads JSON and renders in a template.
- **Timeline:** ~half a day
- **Pro:** Works immediately, no model migrations
- **Con:** Data only as fresh as last script run
- **Best for:** Getting something visible in Django fast

### Option B — Django management command (right long-term architecture)
Script logic moves into `python manage.py analyze_sostocked`. Results saved to a `StockAlert` model. Reporting module queries model and renders natively. Can be triggered by a button in the UI or scheduled.
- **Timeline:** 1–2 days
- **Pro:** Proper architecture, data lives in the database, schedulable
- **Con:** Requires new model + migration
- **Best for:** Production use once design is finalized

### Option C — Upload → analyze → display (best UX eventually)
File upload view in Django. Drag SoStocked export into browser, analysis runs inline, results display immediately. No folders, no terminal.
- **Timeline:** Full feature, 2–3 days
- **Best for:** When the workflow is proven and you want to hand it off or share it

**Current recommendation:** Build Option A now, plan for Option B. The script's core logic is already clean functions — moving it into Django is mostly copy-paste, not a rewrite.

---

## Report Design — Open Questions

These need to be answered before building the Django UI:

- [ ] **Who is the audience?** Just Tommy (operational), or DOS/SVP too (leadership summary)? These are different reports with different detail levels.
- [ ] **What decisions does it drive?** Currently informational. Better version surfaces clear actions: "send FBA replenishment" vs "create PO" vs "no action."
- [ ] **One unified dashboard or per-brand tabs?** Script does brand-by-brand. Django could unify with filters.
- [ ] **Charts or tables?** Tables are faster to build. A bar chart of days-supply by brand may be more useful for leadership.
- [ ] **Snapshot vs. live feel?** Show "as of last export" with date stamp, or make it feel current?
- [ ] **What does DOS/SVP actually want to see weekly?** This drives the entire design.

---

## Architecture Reminder

Three separate layers — already correctly separated, nothing needs to be rebuilt:

| Layer | Tool | Purpose |
|---|---|---|
| Knowledge | Obsidian vault (`supplychainbrain/`) | SOPs, playbooks, weekly snapshots, planning docs |
| Execution | MTB-SupplyChain folder | Scripts, raw data, outputs |
| Procurement | Django ERP (PythonAnywhere) | POs, PPOs, GRPOs, invoicing, Reports Hub |

---

## Next Steps

- [ ] Add `--json` output flag to `analyze_sostocked.py` (20 min)
- [ ] Answer open design questions above (needs DOS/SVP input)
- [ ] Clean up SoStocked regional groupings (22 flagged issues)
- [ ] Build Django Reports Hub — start with Option A (file-based)
- [ ] Define what leadership-facing report looks like
- [ ] Automate SoStocked export with Claude in Chrome scheduled task (eventually)
