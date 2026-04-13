# Demand Planning SOP
**Owner:** Tommy Sapia — Supply Chain Manager
**Cadence:** Weekly (Monday morning)
**Last updated:** April 13, 2026
**Status:** v1 — working draft, refine as you learn the business

---

## Purpose
Analyze inventory levels across all channels and 3PLs, calculate days of supply per SKU, and identify reorder triggers before stockouts occur.

With a **120-day lead time**, you need to be placing POs 4+ months before you run out. This process catches reorder triggers early.

---

## The Core Formula

```
ROP = (Avg Daily Sales × 120 days) + Safety Stock
Safety Stock = Avg Daily Sales × 30 days

Total trigger = Avg Daily Sales × 150 days

If stock on hand < 150 days of supply → reorder now
```

---

## Step 1 — Pull Reports

Export CSVs from each source and drop into the correct folder on this machine.

| Dashboard | What to export | Drop into |
|-----------|---------------|-----------|
| SoStocked | Inventory levels by SKU | `reports/sostocked/` |
| Seller Central | Sales by SKU (30/60/90 day) | `reports/seller-central/` |
| Sellerboard | Sales analytics export | `reports/seller-central/` |
| Walmart Marketplace | Sales + inventory report | `reports/walmart/` |
| TikTok Shop | Sales + inventory report | `reports/tiktok-shop/` |
| Floship | On-hand inventory by SKU | `reports/floship/` |
| ShipBob | On-hand inventory by SKU | `reports/shipbob/` |
| Valogix / SAP | Inventory snapshot | `reports/valogix/` |

> **Note:** Reports folder is at `C:\Users\Tom Sapia\MTB-SupplyChain\reports\`

---

## Step 2 — Run Claude Analysis

Open Claude Code and run:

```
Run the weekly demand planning analysis. Read all CSVs from the reports folders.
For each SKU:
- Calculate total inventory across all locations
- Calculate avg daily sales across all channels
- Calculate days of supply remaining
- Flag anything under 150 days as a reorder trigger
- Segment by brand (MTB, SS, NFMD)
- Lead with urgent issues: stockouts first, then reorder triggers
Save output to: C:\Users\Tom Sapia\MTB-SupplyChain\outputs\
```

---

## Step 3 — Review Output

Claude will produce a weekly summary report. Review in this order:

1. **Stockouts** — SKUs at 0 or near 0. Escalate immediately.
2. **Reorder triggers** — SKUs under 150 days of supply. Place POs.
3. **Approaching trigger** — SKUs between 150–180 days. Watch closely.
4. **Observations** — Velocity shifts, channel anomalies, notes.

---

## Step 4 — Take Action

| Finding | Action |
|---------|--------|
| Stockout | Escalate to DOS, check if any stock can be expedited |
| Reorder trigger | Create PO — log in `01 Purchasing & Inventory/` |
| Velocity spike | Investigate cause (promo? seasonality?) — adjust forecast |
| Overstock | Flag for rebalancing between 3PLs or pause reorder |

---

## Step 5 — Save Output to Brain

Save the weekly analysis to:
```
00 Forecast & Demand Planning/[BRAND]/weekly-[YYYY-MM-DD].md
```

---

## Known Gaps — Refine Over Time

These are simplifications in v1 that need to be improved:

- [ ] **Seasonality** — flat avg daily demand doesn't capture holiday/promo spikes. Add seasonal adjustment once you have 2-3 months of data.
- [ ] **In-transit inventory** — stock already on order should count toward supply. Add PO tracking to the analysis.
- [ ] **Demand variability** — some SKUs are erratic. Safety stock should reflect variability, not just flat 30 days.
- [ ] **MOQs** — minimum order quantities need to factor into reorder recommendations.
- [ ] **Budget constraints** — not all reorder triggers can be acted on at once. Add budget check step.
- [ ] **Channel-level demand** — break out demand by Amazon / Walmart / TikTok / DTC for more precise inventory routing.

---

## Notes
- ShipBob may transition to AmzPrep — update this SOP when that happens
- Each brand (MTB, SS, NFMD) has separate Amazon accounts — treat separately in analysis
- ABC classification: prioritize A items first in any reorder decisions
