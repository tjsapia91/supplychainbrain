# SoStocked Pipeline Discovery
**Date:** April 15, 2026  
**Session:** Claude Cowork — Demand Planning & Inventory Analysis  
**Status:** 🔴 LIVE STOCKOUTS FOUND — ACTION REQUIRED

---

## 🔴 Critical Alerts — Stockouts as of April 15

| Product | Brand | Status | Action |
|---------|-------|--------|--------|
| AIVA Deluxe | SS | 🔴 STOCKOUT TODAY | Check inbounds immediately |
| Viva Foot Replacement Heads | SS | 🔴 STOCKOUT TODAY | Check inbounds immediately |
| Soniclear Replacement Body Brush Head | SS | 🔴 STOCKOUT TODAY | Check inbounds immediately |
| Sonicsmooth 2.0 Lavender (US) | MTB | 🔴 STOCKOUT TODAY | Check inbounds immediately |
| NERA Body Brush | SS | ⚠️ Apr 24 — 9 days | Confirm inbound or place PO |
| Sonicsmooth 1.0 White (CA) | MTB | ⚠️ May 4 | Queue FBA send-in from warehouse |
| Sonicsmooth Pro+ Peach (US) | MTB | ⚠️ May 6 — 21 days, no AWD backup | PO lead time = 61 days → ALREADY PAST ROP |
| Spanish Salt Packets (US) | NFMD | ⚠️ Apr 20 — 5 days | CRITICAL — no supplier listed in SoStocked |
| Premium Bundle (CA) | NFMD | ⚠️ Apr 20 — 5 days | AWD transfer required today |

---

## Key Discovery: Multi-Dashboard Report = Single Source of Truth

### What SoStocked's Multi-Dashboard Export Contains
- **Where:** SoStocked Settings → Bulk Export/Import → "Multi-Dashboard Report (All Accounts)"
- **Coverage:** All 3 brands in ONE file, one click
- **262 rows total:**
  - Spa Sciences: 159 rows
  - Michael Todd Beauty: 70 rows
  - NasalFresh MD: 33 rows

### 27 Columns Available
- Account Name, Marketplace, Product, ASIN, SKU
- **Days of Supply on AMZ** (pre-calculated)
- **Next Stock Out Date** (pre-calculated)
- FBA Stock, Warehouse Stock
- Velocity: 2/7/15/30/60/90/180-day windows
- Cost/Unit, Shipping Cost, COGS
- Adj. Velocity, Lost Sales, Overstock Fees
- Lead Time, Supplier, MOQ

### Why This Matters
SoStocked is **already doing the heavy lifting** — velocity, runway, stockout dates, reorder recommendations. The existing 7-folder agent system was going to re-derive what SoStocked already calculates.

This single export replaces the entire manual 7-folder CSV pipeline for Amazon inventory.

---

## SoStocked API Status

| Option | Available | Notes |
|--------|-----------|-------|
| Public REST API (pull data out) | ❌ NO | Their API is one-way — pulls from Amazon INTO SoStocked only |
| Bulk Export (manual, one click) | ✅ YES | Multi-Dashboard Report = all 3 brands, one file |
| Scheduled/automated export | ❌ Not native | Would need Chrome automation or third-party connector |
| Third-party connectors (APIx-Drive etc.) | ❓ Blocked by org network | Couldn't investigate fully |

---

## Data Quality Issues Found

### Regional Groupings (Root Cause of Most False Alerts)
The #1 data quality problem is inconsistent marketplace/region groupings across SKUs:

| Problem | Example | Impact |
|---------|---------|--------|
| US+MX grouped together | Sonicsmooth 2.0 Pink | MX velocity = 0.07/day creates fake 36,709-day runway |
| Some products NAm (all 3 together) | Sonicsmooth Pro+ Pink | Hides CA-specific issues |
| Dead MX listings still active | Spanish Salt Packets MX | 0 velocity inflating FBA pool math |
| "No Forecast" CA listings | Multiple SS SKUs | False positives/negatives in runway calc |
| No Supplier Listed | Multiple MTB + NFMD SKUs | Order recommendations missing |

### Cleanup Priority
1. **Decide standard grouping policy** — is MX grouped with US or tracked separately?
   - Recommendation: US+MX together where MX is active; disable MX where velocity = 0
2. Bulk update all products via Settings → Bulk Actions → Edit Regional Groupings
3. Assign suppliers to all SKUs missing them (especially NFMD)
4. Verify lead times (some 28-day vs 117-day inconsistencies on same brand)

---

## Architecture Insight: What You Actually Need

### Before (Over-Built)
```
7 CSV exports → 7 folders → preprocessing script → 3 analyst agents → 
planning lead → Excel generator → Monday output
Total: 7 CSVs manual + ~60 min Claude work
```

### After (Simplified)
```
1 Multi-Dashboard export → 1 analysis script → priority list
Total: 1 CSV manual → ~5 min automated output
```

### How Obsidian Fits
| Layer | Tool | What Lives There |
|-------|------|-----------------|
| Knowledge | Obsidian vault | SOPs, playbooks, decisions, vendor notes |
| Execution | MTB-SupplyChain scripts | Analysis scripts, weekly outputs |
| Procurement | Django ERP | PPOs, GRPOs, vendors, invoicing |

**These are already correctly separated.** Don't rebuild — extend.

---

## What the New Pipeline Should Look Like

### Input
- `SoStocked_MultiDashboard_YYYY-MM-DD.xlsx` (downloaded manually — one click)
- Eventually: automated via Chrome extension scheduled task

### Processing (Python script to build)
1. Load Multi-Dashboard export
2. Filter out zero-velocity MX rows (pending regional grouping cleanup)
3. Sort by Days of Supply ascending
4. Flag: STOCKOUT (0 days), CRITICAL (≤7 days), LOW (≤14 days), ROP TRIGGERED
5. Group by Brand

### Output
- `outputs/demand-analysis-YYYY-MM-DD.md` — Priority list by brand
- `outputs/YYYY-MM-DD_MTB_Weekly_WorkingFile.xlsx` — Excel for team
- Eventually: Django ERP demand planning records

---

## Warehouse Footprint (Full Picture)
Confirmed across all 3 brands:
- Amazon AWD
- ShipBob: NV (Sparks), PA (Philadelphia), CA (Moreno Valley/Ontario), GA (Buford/Fairburn), Bethlehem PA, TX
- Harry (3PL)
- MTB Port St Lucie (brand-owned)
- NasalFresh Port St Lucie (brand-owned)
- Bothwell Transport (Tolleson, AZ)
- Spa Sciences PA Transload (Kutztown, PA)

---

## MTB Brand — Key Findings

| Product | Market | Days Supply | Stockout Date | Alert |
|---------|--------|-------------|---------------|-------|
| Sonicsmooth Clear Blade Refills | US | 36 days | — | — |
| Sonicsmooth Pro+ White | US | 18 days | Jun 26 | ⚠️ Stockout Jun 26 |
| Soniclear Elite - White Marble | US | 41 days | Jun 24 | ⚠️ Stockout Jun 24 |
| Sonicsmooth 2.0 White | US+MX | 59 days | Jul 10 | ⚠️ Stockout Jul 10 |
| Sonicsmooth Pro+ Peach | US | 21 days | May 6 | 🔴 Lead time = 61d, ROP past |
| LUMOS Laser IP | US+MX | 77 days | Jul 1 | ⚠️ Stockout Jul 1 |
| Sonicsmooth 2.0 Lavender | US | 0 days | TODAY | 🔴 STOCKOUT |
| AIVA Deluxe | — | 0 days | TODAY | 🔴 STOCKOUT |

---

## NFMD Brand — Key Findings

| Product | Market | Days Supply | Stockout Date | Alert |
|---------|--------|-------------|---------------|-------|
| Spanish Salt Packets | US | 5 days | Apr 20 | 🔴 CRITICAL |
| Premium Bundle | CA | 5 days | Apr 20 | 🔴 CRITICAL |
| Night Time Blend Oil | US | 0 days | Apr 27 | 🔴 STOCKED OUT |
| Adjustable Nose Pillows | US/MX/CA | 0 days | — | 🔴 STOCKED OUT |
| Salt 90-Count | CA | 32 days | May 18 | ⚠️ Watch |

**Total lost sales (NFMD): $69,882**

---

## Next Steps

### This Week (URGENT)
- [ ] Verify inbound status for today's stockouts (AIVA Deluxe, Viva Heads, Soniclear Body, Sonic 2.0 Lav)
- [ ] Transfer AWD stock to CA FBA for NFMD Premium Bundle (5 days left)
- [ ] Resolve NFMD Spanish Salt Packets — supplier not listed, ROP triggered
- [ ] Check Sonicsmooth Pro+ Peach — 21 days left, 61-day lead time, already past ROP

### This Week (Build)
- [ ] Build simplified analysis script using Multi-Dashboard export
- [ ] Download a fresh Multi-Dashboard export and verify column structure
- [ ] Run the new script as a test before next Monday

### Near Term (Data Quality)
- [ ] Clean up SoStocked regional groupings (MX dead markets, CA no-forecast items)
- [ ] Assign suppliers to all SKUs missing them
- [ ] Verify lead times across all brands
- [ ] Decide MX policy: group with US or disable where velocity = 0?

### Future
- [ ] Build Chrome automation to schedule SoStocked export (no manual download)
- [ ] Add demand planning outputs to Django ERP Reports Hub

---

## Session Source
This discovery was made during a Claude Cowork desktop session on April 15, 2026.
Context captured to vault for continuity.
