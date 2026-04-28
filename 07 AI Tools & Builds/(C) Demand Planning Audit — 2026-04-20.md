# Demand Planning Script Audit — April 20, 2026
**Audited by:** Claude (demand_planning.py v2 + supply-chain-pulse.html)
**Data used:** Agencyreport4_16_26.xlsx + inventory4_16_26 (combined, all 3 brands)
**Status:** Issues documented. None fixed yet — prioritized for next session.

---

## Summary

| # | Issue | Severity | Impact | Status |
|---|---|---|---|---|
| 1 | Inbound to FBA inflates available stock → PO qty = 0 | 🔴 BUG | ~10 CRITICAL items show 0 units to order | Not fixed |
| 2 | HIGH tier (13 items) missing from dashboard | 🟠 GAP | Fast movers like Blade Refills (236/day) invisible | Not fixed |
| 3 | Cost / Unit blank for all products | 🟡 GAP | PO dollar value can't be calculated | Not fixed |
| 4 | SS lead times default to 60d | 🟡 GAP | Low risk — SS lead times are actually ~60d | Not fixed |

---

## Issue 1: Inbound to FBA Bug — PO Qty = 0 for Critical Items

### What's happening
The `Inbound to FBA` column in the combined inventory CSV shows **46,129** on the US row for many MTB products. This is not a per-product inbound quantity — it appears to be a SoStocked aggregate/total that bleeds across product rows.

When the PO quantity formula runs:
```
PO qty = daily_vel × (lead_time + 60 buffer) − total_stock − inbound_fba
```
...subtracting 46,129 from everything makes the result 0 or negative for any product with reasonable stock levels.

### Affected products (PO qty falsely showing 0)
| Product | Daily Vel | DOS | Real PO Needed |
|---|---|---|---|
| Soniclear Elite — White Marble | 75.76/d | 70d | Yes — confirm in SAP |
| Sonicsmooth Pro+ White | 78.54/d | 103d | Yes — confirm in SAP |
| Sonicsmooth 2.0 White | 30.23/d | 101d | Yes — confirm in SAP |
| Soniclear Face Brush — Plum | 9.63/d | 82d | Yes |
| Soniclear Face Brush — Sensitive | 4.97/d | 184d | Borderline |
| Sonicsmooth Pro+ Lavender | 183.7/d | 131d | Yes — fast mover |
| Blade Refills | 236.28/d | 124d | Yes — very fast mover |
| Sonicblend Replacement Head | 0.87/d | 24d | Yes |

### Raw evidence
```
Soniclear Elite - White Marble | US:  Inbound to FBA = 46,129
Sonicsmooth Pro+ White        | US:  Inbound to FBA = 46,129
Sonicsmooth 2.0 White         | US:  Inbound to FBA = 46,129
(MX and CA rows for same products: Inbound to FBA = NaN)
```
46,129 shows up identically on 11 different products' US rows — clearly not per-product data.

### Fix (when ready)
Remove `inbound_fba` from the PO qty formula entirely:
```python
# Current (broken):
available = r['total_stock'] + r['inbound_fba']

# Fixed:
available = r['total_stock']
# OR — only include if value is < some sane threshold
available = r['total_stock'] + (r['inbound_fba'] if r['inbound_fba'] < 5000 else 0)
```
If there IS a real inbound shipment, it'll land as stock and the next weekly run will pick it up automatically.

Also worth investigating in SoStocked: what exactly does "Inbound to FBA = 46,129" represent? Could be a single large PO in transit — if so, Tommy should verify in SAP.

---

## Issue 2: HIGH Tier Items Missing from Dashboard

### What's happening
The `supply-chain-pulse.html` dashboard only shows TRUE STOCKOUT and CRITICAL items. The HIGH tier (DOS ≤ lead_time + 30 days) has 13 items that aren't displayed at all.

### HIGH items not shown
| Product | Brand | DOS | Lead | Vel/day | Notes |
|---|---|---|---|---|---|
| Nose Pillows smaller size | NFMD | 57d | 30d | 1.19/d | |
| Nova Pink | SS | 65d | 60d | 11.70/d | Near CRITICAL |
| ECHO Brush Replacement Head | SS | 71d | 60d | 1.87/d | |
| AIVA Replacement Heads | SS | 72d | 60d | 2.77/d | |
| LUMOS Laser IPL | MTB | 79d | 61d | 4.61/d | |
| Sonicsmooth Pro+ Pink | MTB | 119d | 117d | 56.66/d | Fast mover |
| NF Xylitol Rinse Packets | NFMD | 122d | 117d | 0.23/d | |
| Auto Clean | NFMD | 122d | 117d | 4.87/d | |
| **Hair Identifier Spray** | **MTB** | **123d** | **117d** | **143.28/d** | **⚠️ Very fast — 6d from CRITICAL** |
| **Blade Refills** | **MTB** | **124d** | **117d** | **236.28/d** | **⚠️ Fastest mover in catalog** |
| Microsmooth Clear Tips | MTB | 127d | 117d | 3.90/d | |
| Sonicsmooth Pro+ Lavender | MTB | 131d | 117d | 183.70/d | Fast mover |
| Soniclear Face Brush — White | MTB | 142d | 117d | 11.23/d | |

### Fix (when ready)
Add a "🟠 Order Soon" section to the dashboard HTML below the CRITICAL cards, using the same card format but orange color coding.

---

## Issue 3: Cost / Unit Blank — PO Value Can't Calculate

### What's happening
The `Cost / Unit`, `Est. Shipping Cost / Unit`, and `Total COGS / Unit w/ Shipping` columns in the SoStocked Multi-Dashboard export are all 0 / blank for every row (262 rows). The script shows `Est. PO Value = $0` everywhere.

### Available price columns (selling price, not cost)
- `Retail Price - Actual Currency` — 127 non-zero rows, mix of USD/CAD
- `Sale Price - Actual Currency` — 118 non-zero rows

These are Amazon selling prices, not COGS. Can't use them for PO value.

### Fix options
1. **SoStocked settings** — enter cost per unit in each product's SoStocked profile. SoStocked will then include it in the export. (Preferred long-term solution.)
2. **SAP cross-reference** — build a cost lookup table from SAP. Join on SKU or ASIN.
3. **Manual cost CSV** — maintain a `costs.csv` mapping ASIN → cost. Load it as a 4th input file to demand_planning.py.

### Impact on PO value totals
With 17 priority items needing orders, the total PO value is significant but currently uncalculable. Example: Sonicsmooth Pro+ Peach needs 2,028 units — if COGS is $15/unit, that's a $30k PO. Leadership will want these numbers.

---

## Issue 4: SS Lead Times Defaulting to 60 Days

### What's happening
The combined inventory file (all 3 brands) has `Default Lead Time = NaN` for all Spa Sciences products. They fall back to the script's 60-day default.

### Is this a problem?
Probably not severe — the SS-only inventory file confirmed SS lead times are 60-61 days, so the 60-day default is approximately correct. But it means we're not using SKU-level precision for SS.

### Fix (when ready)
Two options:
1. Export a separate SS inventory file from SoStocked (the SS-only file had correct lead times). Load it alongside the combined file.
2. Investigate why lead times are NaN in the combined export — may be a SoStocked export setting.

---

## Verified Working Correctly

- ✅ Velocity columns are daily rates (confirmed by back-calculating DOS against SoStocked's own values)
- ✅ Adj. Velocity used as primary, 30-day as fallback
- ✅ INACTIVE_THRESHOLD = 0.1/day correctly separates real stockouts from dead listings
- ✅ Region normalization: NAm+US+MX → US, CA → separate, MX → removed
- ✅ Brand names map correctly: Michael Todd → MTB, Spa Sciences → SS, Nasalfresh MD → NFMD
- ✅ TRUE STOCKOUT items join correctly (0 stock, active velocity — confirmed 3 items)
- ✅ Lead times for MTB products sourced correctly from inventory (117d, 61d)
- ✅ Progress bars and urgency logic on dashboard are mathematically correct
- ✅ All 17 priority items confirmed present in dashboard and Excel

---

## Next Session Priorities

1. Fix inbound_fba in PO formula (15 min, high impact)
2. Add HIGH tier section to dashboard (30 min)
3. Investigate source of inbound = 46,129 — is it a real PO in SAP?
4. Get cost data solution figured out (SoStocked settings or SAP export)
5. Test full script on Windows machine end-to-end with fresh report files
