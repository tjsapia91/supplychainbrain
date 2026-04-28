# Demand Planning Report — Meticulous Build Plan
**Last updated:** April 16, 2026
**Status:** Planning phase — files analyzed, build ready to start
**Scope:** Spa Sciences (initial build) → expand to MTB + NFMD once confirmed

---

## The Three Source Files

### 1. Agency Report — `Agencyreport4_16_26.xlsx`
**What it is:** SoStocked Multi-Dashboard Report — ALL 3 brands in one file
**Sheet:** `Inventory - Full Report`
**Rows:** 262 | **Columns:** 27

| Brand | Row Count |
|---|---|
| Spa Sciences | 159 |
| Michael Todd | 70 |
| Nasalfresh MD | 33 |

**Marketplaces present:** US (83), CA (71), MX (62), NAm (27), US+MX (19)

**Key columns used:**
| Column | Purpose |
|---|---|
| Account Name | Brand identifier |
| Marketplace | Region (will be normalized) |
| Product Name | Display name |
| ASIN | Join key |
| SKU | Join key |
| 30 Day Velocity | Primary velocity for days-of-supply calc |
| Adj. Velocity | Secondary / cross-check |
| Total FBA Stock | FBA component of total stock |
| Total Warehouse Stock | All warehouses — NOT used directly (we use AWD from inventory file) |
| Next Stock Out Date | SoStocked estimate (we'll recalculate with our formula) |
| Days of Supply on AMZ | SoStocked estimate (we'll recalculate) |
| Cost / Unit | For PO cost estimates |
| Est. Shipping Cost / Unit | For landed cost |
| Total COGS / Unit w/ Shipping | Total landed cost per unit |
| AMZ Category | For grouping/filtering |

**⚠️ Highlighted columns — TO CONFIRM:** Tommy highlighted specific columns. Not visible programmatically — need confirmation.

---

### 2. Inventory Report — `inventory4_16_26.csv`
**What it is:** Per-warehouse inventory detail — **Spa Sciences ONLY** (76 ASINs)
**Rows:** 122 | **Columns:** 32

⚠️ **Important:** This file does NOT cover MTB or Nasalfresh MD. Separate exports needed for those brands.

**Warehouse breakdown:**
| Warehouse | Rows |
|---|---|
| Amazon AWD (only) | 77 |
| Amazon AWD + ShipBob GA | 24 |
| No warehouse listed | 21 |

**Rule applied:** Use AWD rows only. ShipBob rows are excluded per Tommy's instruction.

**Key columns used:**
| Column | Purpose |
|---|---|
| Marketplace | Region (will be normalized) |
| Product Name | Display |
| ASIN | Join key |
| SKU | Join key |
| Warehouse | Filter to "Amazon AWD" only |
| Warehouse Stock | AWD units — used in days-of-supply calc |
| FBA Available Stock | Cross-check against agency report |
| Total FBA Stock | Cross-check |
| Inbound to FBA | Units in transit to Amazon |
| Inbound to Warehouse | Units inbound to AWD |
| Default Lead Time | Days from order → arrival at warehouse |
| Default Product Lead Time | Days from order → FBA-ready |
| Supplier | Who to PO from |

**⚠️ Highlighted columns — TO CONFIRM:** Need confirmation from Tommy.

**Open question:** `Default Lead Time` vs `Default Product Lead Time` — which drives the reorder point?
- Default Lead Time values: 60, 61, 107 days
- Default Product Lead Time values: 60, 107, 172 days
- Recommendation: Use `Default Product Lead Time` — it's the full door-to-FBA timeline, which is what matters for not stocking out.

---

### 3. Projected Forecast — `projectedforecast4_16_26.xlsx`
**What it is:** SoStocked demand forecast — **Spa Sciences ONLY** (matches inventory file)
**Rows:** 120 per sheet | **Coverage:** 38 weeks (Apr 16 – Dec 31, 2026) + 9-month view

**Sheets and purpose:**
| Sheet | Use |
|---|---|
| Forecasted Sales | ✅ PRIMARY — weekly projected units sold |
| Forecasted Sales Monthly | Reference — monthly rollup |
| Forecasted Orders | ✅ SECONDARY — when SoStocked says to reorder |
| Forecasted Orders Monthly | Reference |
| Forecasted Transfers | ✅ SECONDARY — AWD→FBA transfer schedule |
| Forecasted Transfers Monthly | Reference |

**Key insight from Forecasted Orders:** SoStocked already calculates recommended PO dates and quantities. We can cross-reference our calculation against theirs as a sanity check.

**Key insight from Forecasted Transfers:** Shows when AWD stock should be pushed to FBA — this tells us when a product will naturally restock Amazon even without a new PO.

---

## Source Columns — Locked In ✅

### Agency Report (`Agencyreport4_16_26.xlsx`) — Confirmed Columns
| Excel Col | Index | Column Name | Use |
|---|---|---|---|
| L | 11 | Total FBA Stock | FBA component of stock |
| M | 12 | Total Warehouse Stock | AWD component of stock (AWD is what's connected in SoStocked) |
| T | 19 | 30 Day Velocity | Primary velocity for all calculations |

All other columns from agency report (ASIN, SKU, Account Name, Product Name, Marketplace, Cost/Unit, COGS) pulled as identifiers and reference data.

### Inventory File — Role
Used to extract AWD warehouse stock details, lead times, supplier, and inbound quantities. AWD stock in inventory cross-references column M in the agency report.

---

## Processing Rules (Locked In)

### Region / Marketplace Rules
| Raw Value | Rows | Action | Output |
|---|---|---|---|
| `US` | 83 | Keep | `US` |
| `NAm` | 27 | Rename to US | `US` |
| `US+MX` | 19 | ⚠️ **Pending confirmation** — all Spa Sciences | `US` or drop? |
| `CA` | 71 | Keep separate | `CA` |
| `MX` | 62 | **Remove entirely** | — |

**After cleanup (MX removed, NAm→US):** 110 US rows + 71 CA rows + 19 US+MX rows (pending)

**Combining NAm+US for same ASIN:**
Only 1 product has both rows: **Sonicsmooth 2.0 Lavender (MTB)**. All others map cleanly.
- FBA Stock → sum both rows
- Warehouse/AWD Stock → sum both rows
- 30-Day Velocity → sum both rows (combined US demand)

### Days of Supply Formula — Confirmed ✅
```
Days of Supply = (Col L + Col M) ÷ (Col T / 30)

Where:
  Col L = Total FBA Stock        (units at Amazon)
  Col M = Total Warehouse Stock  (AWD units in SoStocked)
  Col T = 30 Day Velocity        (total units sold in past 30 days)
  Col T / 30                     = daily velocity rate
```

**This replaces SoStocked's "Days of Supply on AMZ" which only uses FBA stock.**

### Two-Level Stockout Alert — Critical Design Decision
The formula can mask real emergencies. Example: AIVA Deluxe has FBA=0 but Warehouse=924 → DOS = 3,696 days. The math looks healthy but it's stocked out on Amazon **right now.**

Two separate flags are required:

| Flag | Condition | Meaning | Action |
|---|---|---|---|
| 🚨 AMAZON STOCKOUT | FBA = 0 AND velocity > 0 | Selling but nothing on Amazon | Send FBA replenishment from warehouse |
| 🔴 TRUE STOCKOUT | FBA + Warehouse = 0 AND velocity > 0 | No stock anywhere | Place new PO immediately |

These are different problems requiring different responses. A product can show 3,000 days of supply but still need an urgent FBA transfer.

### Full Urgency Tier System
| Tier | Label | Condition | Action |
|---|---|---|---|
| 🚨 | AMAZON STOCKOUT | FBA=0, velocity>0, WH>0 | Replenish FBA now |
| 🔴 | TRUE STOCKOUT | FBA+WH=0, velocity>0 | New PO immediately |
| 🔴 | CRITICAL | DOS ≤ Lead Time | At or past reorder point — order now |
| 🟠 | HIGH | DOS ≤ Lead Time + 30d | Order within the week |
| 🟡 | WATCH | DOS ≤ 60d | On radar |
| 🟢 | HEALTHY | DOS > 60d | No action needed |
| ⚫ | INACTIVE | Velocity = 0 | Dead/suppressed listing — separate review |

**Why lead time drives CRITICAL:** If DOS ≤ lead time, stock will run out before a new order arrives. That IS the reorder point mathematically.

---

## Data Join Logic

```
Agency Report (all 3 brands, all markets)
    ↓
    [1] Remove MX rows
    [2] Normalize marketplace (NAm+US → US, US+MX → US)
    [3] Aggregate duplicate rows: sum FBA stock + velocity
    ↓
LEFT JOIN Inventory CSV on [ASIN + normalized_market]
    ↓
    [4] Filter AWD only
    [5] Normalize marketplace
    [6] Aggregate AWD stock
    ↓
LEFT JOIN Forecast (Forecasted Sales) on [ASIN + normalized_market]
    ↓
    [7] Normalize marketplace
    [8] Aggregate weekly forecasted sales
    [9] Calculate: 4-week, 8-week, 13-week (90-day) totals
    ↓
CALCULATE all derived fields
    ↓
OUTPUT → sorted by urgency → Excel report + markdown
```

**Note:** LEFT JOIN means every product in the Agency Report gets a row even if it has no AWD stock or no forecast data.

---

## Output Fields (Per Row)

| Field | Source | Formula |
|---|---|---|
| Brand | Agency Report | Account Name |
| Product Name | Agency Report | Product Name |
| ASIN | Agency Report | ASIN |
| SKU | Agency Report | SKU (first if stacked) |
| Market | All files | Normalized (US / CA) |
| Supplier | Inventory | Supplier |
| Lead Time (days) | Inventory | Default Product Lead Time |
| 30-Day Velocity (units/day) | Agency Report | 30 Day Velocity ÷ 30 |
| FBA Stock | Agency Report | Total FBA Stock |
| AWD Stock | Inventory | Warehouse Stock (AWD only) |
| Inbound to FBA | Inventory | Inbound to FBA |
| Total Available | Calculated | FBA + AWD |
| **Days of Supply** | Calculated | (FBA + AWD) ÷ daily velocity |
| Projected Stockout Date | Calculated | Today + Days of Supply |
| Reorder Point Date | Calculated | Stockout Date − Lead Time |
| Urgency Tier | Calculated | See tier table above |
| Forecast 30d | Forecast | Sum weeks 1–4 |
| Forecast 60d | Forecast | Sum weeks 1–8 |
| Forecast 90d | Forecast | Sum weeks 1–13 |
| SoStocked Suggested Order | Forecast | Forecasted Orders Week 1 |
| Recommended PO Qty | Calculated | (see below) |
| Cost / Unit | Agency Report | Cost / Unit |
| Est. PO Value | Calculated | Recommended PO Qty × Cost / Unit |

### Recommended PO Quantity Formula
```
Coverage Target = Lead Time days + 60 days safety buffer  (confirm buffer)
Target Stock    = daily_velocity × coverage_target_days
Current Stock   = FBA + AWD + Inbound to FBA + Inbound to Warehouse
PO Qty          = max(0, Target Stock − Current Stock)
```
**Open question:** What's the target coverage buffer? (30 days? 60 days? Varies by product?)

---

## Report Output Format

### Summary Dashboard (top of report)
| Brand | 🔴 Stocked Out | 🔴 Critical (at ROP) | 🟠 High (≤ ROP+30d) | 🟡 Watch | 🟢 Healthy | ⚫ Inactive |
|---|---|---|---|---|---|---|
| Spa Sciences | | | | | | |
| Michael Todd | | | | | | |
| Nasalfresh MD | | | | | | |

### Priority Action Table (critical + stocked out items)
Sorted by urgency tier, then days of supply ascending. Columns: Brand, Product, Market, Days Supply, Stockout Date, Reorder By, PO Qty, Supplier, Lead Time, PO Value.

### Full Inventory Table (all active products)
All active products, all markets, all fields.

### Watch List (30–60 days)
Products approaching reorder point — no action yet but on radar.

### Inactive Listings
Products with zero velocity — for separate review (suppressed listings, dead SKUs).

### Regional Cleanup Flags
Products with conflicting or messy marketplace groupings.

---

## Open Questions — Must Confirm Before Build

- [ ] **Highlighted columns:** Which columns did Tommy highlight in the Agency Report and Inventory CSV?
- [ ] **US+MX handling:** Treat as US? (NAm=US confirmed, MX=remove confirmed, US+MX = ?)
- [ ] **MTB + NFMD inventory/forecast files:** Inventory CSV and forecast are SS-only. Do separate files exist for the other two brands?
- [ ] **Lead time column:** Use `Default Lead Time` or `Default Product Lead Time`?
- [ ] **PO coverage buffer:** How many days of safety stock beyond lead time? (30? 60? Per product?)
- [ ] **Inbound stock:** Should inbound to FBA and inbound to warehouse count toward total available stock in the days-of-supply calc?
- [ ] **Report format:** Excel output, markdown, or both? Does leadership need a PDF?
- [ ] **Brand scope for v1:** Build for SS only first, then add MTB + NFMD? Or wait until all 3 files are available?

---

## Build Sequence (once questions answered)

1. **Build data loader** — load all 3 files, apply region rules, filter AWD, drop MX
2. **Build joiner** — merge on ASIN + normalized market, handle missing matches
3. **Build calculator** — days of supply, stockout date, reorder point, PO qty
4. **Build urgency tagger** — apply tier logic based on lead time
5. **Build report generator** — priority table + full table + watch list + cleanup flags
6. **Test against real data** — verify numbers match manual calc for 3–5 spot-check products
7. **Save output** — Excel + markdown to MTB-SupplyChain/outputs/
8. **Add to Django Reports Hub** — once design is confirmed

---

## File Paths Reference

| File | Location |
|---|---|
| Agency Report | Upload → `MTB-SupplyChain/reports/agency/` |
| Inventory CSV | Upload → `MTB-SupplyChain/reports/inventory/` |
| Projected Forecast | Upload → `MTB-SupplyChain/reports/forecast/` |
| Build script | `MTB-SupplyChain/demand_planning.py` (to be created) |
| Output reports | `MTB-SupplyChain/outputs/demand-plan-YYYY-MM-DD.xlsx` |
| Vault snapshot | `supplychainbrain/00 Forecast & Demand Planning/SS|MTB|NF/` |
