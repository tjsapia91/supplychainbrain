# Tab 10 — 🚨 Priority Actions

**Purpose:** Cross-marketplace consolidated view of items needing action this week. Pulls from every Amazon tab + Valogix-based tabs (Shopify, Walmart, Floship) and surfaces ONLY items requiring intervention.

This tab is what you scan first on Monday morning.

---

## What Lands Here

Items with status:
- 🚨 AMAZON STOCKOUT
- 🔴 TRUE STOCKOUT
- 🔴 CRITICAL
- 🟠 HIGH
- 🟡 FBA REPLENISHMENT
- 🔵 BELOW ROP / LOW (Valogix channels)

Items EXCLUDED:
- HEALTHY
- INACTIVE
- LOW VEL STOCKOUT
- PO COVERED (deferred to Watch sub-section)
- E / Z phase-out items

---

## Layout

Items grouped by marketplace section with section headers:
- Amazon US
- Amazon CA
- Shopify MTB
- Spa Sciences DTC
- Walmart NFMD
- Walmart SS
- Floship Intl

Within each section, items sorted by:
1. **Status sub-rank** — most urgent first (Stockout → Critical → High → FBA Replen → Below ROP → Low)
2. **ABC class** — A SKUs first, then B/C/D
3. **DOS ascending** — most urgent within each ABC cluster

A separate **Watch — PO Covered** sub-section lists items that would be CRITICAL but have a real SAP supplier PO landing in time.

---

## Columns

Same `WS_PRIORITY_COLS` structure as Amazon US tab. See [[(C) 01 - Amazon US]] for column-by-column details.

Key column on this tab: **MARKETPLACE** — shows where each row lives (Amazon US / CA / Shopify MTB / etc.).

---

## How It's Built

The unified list is constructed in `build_marketplace_tabs()` by:
1. Walking `data["priority_actions"]` + `data["high_tier"]` + `data["fba_replenishment"]` for Amazon items
2. Walking Valogix items filtered to action-tier statuses
3. Merging into one list with marketplace tag
4. Sorting by status × ABC × DOS

---

## Source Files

This tab is a *view* over data that's already in `data["all_items"]` (after all enrichment passes). No new file reads.

---

## Reading the Tab

Each marketplace block has its own header row plus column headers (so headers repeat as you scroll).

For each row:
- **DAYS OF STOCK LEFT** column tells you current Amazon-only runway
- **STOCKOUT DATE (AT CURRENT PACE)** tells you when it runs out
- **AMZ PO QTY (SUPPLIER)** suggests how much to order (legacy — prefer `🛒 ORDER NOW`)
- **SB→AMZN SUGGEST** suggests ShipBob transfer if item is SB-replenished

---

## Counts Banner

The title bar at the top counts items by status:
```
🚨 X Stockout · 🔴 X Critical · 🟠 X High · 🟡 X FBA Replen · ⏱ X Watch (PO covered)
```

---

## Companion Tabs

- **[[(C) 11 - Action Plan]]** — Same data sliced for execution (ShipBob send-ins vs Supplier POs)
- **`outputs/latest/order-list-*.xlsx`** (separate file) — newer, cleaner: "do I have 150 days of stock?"
