# Demand Planning SOP
**Owner:** Tommy Sapia — Supply Chain Manager
**Cadence:** Weekly (Monday morning)
**Last updated:** April 20, 2026
**Status:** v2 — updated with SoStocked Multi-Dashboard workflow and velocity fix

> **Monday morning?** Use the runcard: [[06 Processes & SOPs/(C) Monday Demand Plan Runcard|Monday Demand Plan Runcard]] — checklist format, step by step.
> This SOP has the full detail and formulas behind it.

---

## Purpose
Analyze inventory levels across all channels, calculate days of supply per SKU, and identify reorder triggers before stockouts occur. With 60–117 day lead times, POs need to be placed well before stock runs out. This process catches reorder triggers early and surfaces the right SKUs to act on.

---

## Core Formulas (Locked In)

```
DOS = (FBA Stock + AWD Stock) ÷ Adj. Velocity

ROP = Adj. Velocity × (lead_time_days + 60 buffer)

Order Qty = Adj. Velocity × (lead_time_days + 60) − total_available_stock
```

**Velocity note:** SoStocked exports `Adj. Velocity` and `30 Day Velocity` in **units/day** already. Do NOT divide by 30. The old v1 formula was wrong.

**Fallback:** If `Adj. Velocity` = 0, use `30 Day Velocity`. Adj. Velocity is preferred because it corrects for stockout suppression — stocked-out products can't sell, so the 30-day figure is artificially low.

**Inactive threshold:** < 0.1 units/day → flagged as INACTIVE, not a PO emergency.

---

## Urgency Tiers

| Tier | Condition | Action |
|------|-----------|--------|
| TRUE STOCKOUT | No stock anywhere (FBA = 0, AWD = 0) | New PO immediately |
| AMAZON STOCKOUT | FBA = 0 but AWD/warehouse stock exists | Send-in to FBA |
| CRITICAL | DOS ≤ lead time | At reorder point — place PO now |
| HIGH | DOS ≤ lead time + 30 days | Place PO this week |
| WATCH | DOS ≤ 60 days | Monitor daily |
| HEALTHY | DOS > 60 days | No action needed |
| INACTIVE | < 0.1 units/day | Track separately — not a PO emergency |

---

## Step 1 — Download SoStocked Multi-Dashboard Report

This is the **one file** that replaces pulling 7 separate CSVs. It includes all 3 brands (MTB, SS, NFMD) in a single export.

**Where to get it:**
1. Log into SoStocked
2. Go to **Settings → Bulk Export/Import**
3. Click **"Multi-Dashboard Report (All Accounts)"**
4. Download the CSV (~262 rows, all 3 brands)

**Drop the file into:**
```
C:\Users\Tom Sapia\MTB-SupplyChain\reports\agency\
```

> You also need the **Inventory Export** (separate file) for FBA stock levels. Drop that into `reports\inventory\`.

---

## Step 2 — Run demand_planning.py

```bash
cd C:\Users\Tom Sapia\MTB-SupplyChain
python demand_planning.py
```

The script reads both source files, applies urgency tiers, calculates DOS and order quantities, and outputs:
- **Excel report** with 5 sheets → `outputs\demand-plan-YYYY-MM-DD.xlsx`
- Priority actions, broken out by tier and brand

**Script location:** `C:\Users\Tom Sapia\MTB-SupplyChain\demand_planning.py`

---

## Step 3 — Review Output Excel

Open the Excel file in `outputs\`. Review sheets in this order:

1. **Priority Actions** — TRUE STOCKOUTS and CRITICAL items. These need POs or FBA send-ins today.
2. **High / Watch** — Approaching reorder point. Place POs this week.
3. **Low Vel Stockouts** — Stocked out but < 0.1 units/day. Track but don't treat as emergencies.
4. **Healthy** — DOS > 60 days. No action needed.
5. **Inactive** — Zero velocity. Flag for SKU rationalization review.

Look for:
- Items that have been CRITICAL for multiple consecutive weeks → chronic issue, escalate
- Velocity spikes on HEALTHY items → may flip to WATCH/CRITICAL faster than expected
- Inbound FBA units showing large numbers → verify against SAP (known data quality issue as of Apr 20)

---

## Step 4 — Take Action

| Finding | Action |
|---------|--------|
| TRUE STOCKOUT | Place PO immediately — log in `01 Purchasing & Inventory/` |
| AMAZON STOCKOUT | Create FBA send-in shipment from AWD/warehouse |
| CRITICAL | Place PO this week — use Order Qty from output |
| HIGH | Place PO by end of week |
| Velocity spike | Investigate cause (promo? listing change?) — adjust forecast |
| Overstock | Flag for 3PL rebalancing or pause reorder |

When placing a PO, follow the PO Creation SOP: `06 Processes & SOPs/(C) PO Creation SOP.md`

---

## Step 5 — Save Weekly Snapshot to Brain

After reviewing the output, save a snapshot to the vault:

```
00 Forecast & Demand Planning/[BRAND]/weekly-[YYYY-MM-DD].md
```

Example: `00 Forecast & Demand Planning/MTB/weekly-2026-04-20.md`

The snapshot should include:
- Priority items table for that brand
- Recommended actions
- Low velocity stockouts
- Notes on any data quality issues or anomalies

Use `(C)` prefix if Claude generated it.

---

## Known Gaps — Still Open as of April 20, 2026

- [ ] **Inbound to FBA bug** — 46,129 units showing as inbound for many MTB products (SoStocked aggregate bleed). This causes PO qty = 0 for ~10 CRITICAL items. Fix: remove inbound_fba from PO formula. Do not trust inbound counts until fixed.
- [ ] **HIGH tier missing from dashboard** — 13 items not shown in output, including Blade Refills (236/day) and Hair Spray (143/day), both 6-7 days from flipping CRITICAL. Fix pending.
- [ ] **Investigate 46,129 inbound** — Is there a real large MTB shipment in transit in SAP? Check before dismissing.
- [ ] **Cost / Unit blank** — SoStocked export has no cost data. PO $ value = $0 in reports. Fix: enter costs in SoStocked product settings OR build SAP cost lookup.
- [ ] **SS lead times = NaN** — All SS defaults to 60 days in combined inventory file. Probably OK but worth fixing — try separate SS inventory export.
- [ ] **Seasonality** — Flat avg daily demand doesn't capture promo or holiday spikes. Revisit once 2-3 months of data is available.
- [ ] **MOQs** — Not yet factored into order quantity recommendations.
- [ ] **MTB and NFMD forecast files** — Not yet pulled from SoStocked. Will improve order qty accuracy.
- [ ] **SoStocked regional groupings** — 22 regional grouping issues flagged. MX rows still present, NAm/US+MX inconsistent. Clean up in SoStocked settings.

---

## Notes
- Each brand (MTB, SS, NFMD) has separate Amazon accounts — treated separately in script output
- ShipBob may transition to AmzPrep — update this SOP when confirmed
- ABC classification: prioritize A items first in any reorder decisions
- Lead times: MTB = 117 days, SS = 60 days, NFMD = 117 days (defaults — verify per vendor)
