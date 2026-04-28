# Demand Planning — Where I Left Off
**Last updated:** April 27, 2026

---

## Current Step

**Step 1: Pull 12 months of sales data for your top 10 SKUs by volume.**

Where to get it:
> Seller Central → Reports → Business Reports → Sales and Traffic by Child ASIN (Detail Page)
> - Set date range: last 12 months
> - Download the report
> - Put it in a spreadsheet — one row per product, one column per month
> - You want: units sold per ASIN per month

Once you have the data, answer these for each SKU:
- What's the average monthly sales?
- What's the highest month? Lowest month?
- Is there a trend — up, down, or flat?
- Any seasonality — spikes at certain times of year?
- Any anomalies — random huge month? Why? (Promotion? Viral? Restock after stockout?)

---

## My Job — What I Should Be Doing Daily

| Time | Task |
|------|------|
| Morning | Review inventory levels. What's low? Overstocked? Any stockouts imminent? |
| Mid-morning | Check open POs. What's arriving this week? Any delays from suppliers/freight? |
| Afternoon | Work on forecasts. Update projections. Place POs as needed. |
| End of day | Communicate with suppliers, freight forwarders, internal teams on issues. |
| ERP building | 30 min max per day or after hours. It's a tool, not the job. |

---

## Priority Stack (from job description)

1. **Forecasting & Demand Planning** — build forecasts for ALL SKUs
2. **Inventory Management** — replenishment, reorder points, prevent stockouts AND overstock
3. **Purchasing & PO Management** — POs, aligning orders with forecasts
4. **Import/Inbound Logistics** — freight forwarders, bills of lading, carrier bookings
5. **Analytics & Reporting** — data analysis, trends, the ERP fits here
6. **Supplier/Vendor Management** — communication, alignment on forecasts
7. **Process Improvement** — automation, streamlining (AFTER fundamentals are solid)

---

## The 5 Questions That ARE Demand Planning

Every day, for every product:

1. **How much will we sell?** (forecast)
2. **How much do we have?** (inventory)
3. **When do we need to reorder?** (reorder point)
4. **How much do we order?** (order quantity)
5. **What could go wrong?** (safety stock / risk)

---

## Key Formulas

| Formula | Calculation |
|---------|-------------|
| Daily Sales Rate | Monthly sales ÷ 30 |
| Reorder Point | (Daily sales × Lead time days) + Safety stock |
| Safety Stock (simple) | Daily sales × Buffer days |
| Days of Supply | Units on hand ÷ Daily sales rate |
| Forecast Accuracy | (1 - \|forecast - actual\| ÷ actual) × 100 |
| Inventory Turns | Annual COGS ÷ Average inventory value |
| Weeks of Supply | Units on hand ÷ Weekly sales rate |

---

## 90-Day Guide

Full guide is in the vault: `14 Learning & Development/(C) Demand Planning - 90 Day Guide.md`

**Phase 1 (Weeks 1–4): Learn the Machine**
- Pull sales data, map supply side, build first forecast BY HAND
- Compare your numbers to Valogix — learn the tool by checking its homework

**Phase 2 (Weeks 5–8): Expand and Refine**
- Own 5–10 products, track forecast accuracy, understand supplier reliability

**Phase 3 (Weeks 9–12): Own It and Optimize**
- Identify top 3 problems, build solutions, THEN automate the boring parts

> **Rule: Manual first, automate later. You can't automate what you don't understand.**

---

## Context

Tommy is ~5 weeks into this role with no prior supply chain experience. Built an ERP the SVP loves. Has been reminded not to lose sight of the core job — demand planning and inventory management.

**Learn by doing. One step at a time. Manual work before automation.**
