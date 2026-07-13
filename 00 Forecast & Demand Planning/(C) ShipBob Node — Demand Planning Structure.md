---
tags: [demand-planning, shipbob, node-spec]
node: ShipBob
brands: [MTB, SS, NFMD]
status: draft-v1
updated: 2026-07-01
author: Claudian (with Tommy)
---

# ShipBob Node — Demand Planning Structure

> **What this is.** The demand-planning spec for the **ShipBob** node, learned
> directly from Tommy (2026-07-01). ShipBob is one *section* of the overall
> demand plan — the others (Amazon, Alliance/CA, Floship/Intl) get their own
> specs. This is the living source of truth for how ShipBob demand is built.

---

## 1. What ShipBob is

ShipBob is the primary 3PL and **demand-aggregation node**. Two SAP warehouses:

| SAP warehouse | Brand(s) | ShipBob account (blob) |
|---|---|---|
| `SBGA-MT` | MTB | 385579 |
| `SBGA-SS` | SS + NFMD | 385953 (SS) + 385954 (NFMD) |

A supplier PO into ShipBob must cover **every channel ShipBob ships to** — that's
the whole point of planning at this node.

---

## 2. Scope — what's IN and OUT

**IN scope (channels ShipBob fulfills):**
- **Shopify** (DTC)
- **TikTok** (TikTok Shop)
- **Walmart** (SS + NFMD only — MTB does not sell on Walmart)

**OUT of scope:**
- **Amazon** — its own section, planned separately (supplier → AWD → FBA).
  Do **not** fold Amazon demand into the ShipBob plan. *(Tommy 2026-07-01.)*

> Book200's title "SBGA-MT (incl. TikTok)" reflected Tommy hand-adding TikTok
> onto the Shopify base. That aggregation is now automated (§3).

---

## 3. Demand model — channel × source

**ShipBob demand = Shopify + TikTok ( + Walmart for the SS warehouse ).**

| Channel | `SBGA-MT` (MTB) | `SBGA-SS` (SS + NFMD) | Source system |
|---|---|---|---|
| **Shopify** | Valogix `SBGA-MT` | Valogix `SBGA-SS` | Valogix history/forecast report (= sales) |
| **TikTok** | Valogix `TIKTOKMT` | Valogix `TIKTOKSS` | Valogix planning group *(confirmed)* |
| **Walmart** | — (not on Walmart) | Walmart Inventory Health (SS + NFMD) | Walmart Seller Center |

- **Shopify** = the Valogix `SBGA-*` location forecast. **CONFIRMED (Tommy
  2026-07-01): the Valogix historical forecast at the SBGA node IS the Shopify
  sales of record — authoritative. No separate Shopify sales file is needed.**
  (For MTB this is ~337,922 units Jul–Dec — validated as correct, not inflated.)
- **TikTok** = the Valogix `TIKTOKMT` / `TIKTOKSS` planning groups. Pulled from
  the *same* Valogix report, different Location rows — summed on top of Shopify.
- **Walmart** = the two Walmart **Inventory Health** exports (one per brand:
  NFMD + SS). Valogix `WM-SS` is **not** used (undercounts).

### Walmart demand field (PROPOSED — confirm)
Inventory Health gives two forward 28-day forecast buckets
(`Forecast <d1>` + `Forecast <d2>`). Use:

```
walmart_daily = (bucket1 + bucket2) / 56 days   →  extend flat across horizon
```

Filter to **Published + Active** rows only. Rejected alternatives: `Suggested
Units` (that's a reorder qty incl. Walmart safety stock, not demand);
`Sell-Through Rate` (needs conversion, messier).

> **Operator note:** Walmart is a *small* channel for SS/NFMD — a few units/day
> per SKU, mostly <0.5/d. Shopify + TikTok dominate. Don't over-engineer Walmart
> precision.

---

## 4. Inventory position (what's on hand at the node)

- **On hand** = ShipBob Inventory Status export, `On Hand` column, summed across
  all FCs, per canonical UPC (`sku_rules.resolve_upc`).
- **Open POs** = SAP open POs filtered to warehouse `SBGA-MT` / `SBGA-SS`
  (line-level doc number; exclude closed). Bucketed by ETA month for the
  inbound-by-month view.
- **Transloads / in-transit** not yet in SAP won't show until received — a known
  gap (e.g. the 54k Hair Spray transload; PO 3232). Overlay the In-Transit Log
  later if needed.

---

## 5. The order math — DAV × Coverage (interactive, per SKU)

Demand is expressed as **DAV** (Daily Average Velocity) = Shopify + TikTok
(+ Walmart) daily rate, forward-forecast basis, 60-day window (trailing shown as
a variance check). The report is **interactive** — Lead Time / Coverage / Safety
are editable cells and everything below recalculates via live Excel formulas.

```
Total DAV      = Shopify DAV + TikTok DAV + Walmart DAV
Target stock   = Total DAV × (Coverage + Safety)      # COVERAGE-ONLY (Tommy 2026-07-02)
New PO QTY     = MAX(0, Target − On Hand − Open PO)
To order       = CEILING(New PO, 500)
Days of Cover  = On Hand ÷ Total DAV
Stockout ETA   = TODAY() + (On Hand + Open PO) ÷ Total DAV
```

**Convention = Coverage-only (option B).** Lead Time is NOT in the PO quantity —
holding N days of stock is the target. Instead **Lead Time drives an EXPEDITE
flag**: when Days-Cover-w/PO < Lead Time, the item would run out before a new PO
can land → flagged. Defaults: **Lead 120d · Coverage 180d · Safety 0d** (all
editable in-sheet; set Coverage 90 for a 3-month plan).

**Gating (never auto-order):**
- Phase-out SKUs (`sku_rules.PHASE_OUT`) → "DO NOT order".

> **ShipBob is supplier-fed → every item here is PO-eligible.** The
> "ShipBob-replenished / transfer" tag (`sku_rules.LEAD_TIME_OVERRIDE`, e.g. Hair
> Spray `811573031410`) is an **Amazon-node** concept — it means *Amazon* is
> replenished by a transfer FROM ShipBob, not by a direct supplier PO. It does
> **NOT** gate the ShipBob planner (fixed 2026-07-02). The ShipBob→Amazon
> transfer lives in the Amazon section. `LEAD_TIME_OVERRIDE` still applies in
> `build_report`/`build_order_list` (the Amazon-side engines) — unchanged.

---

## 6. The "Adj" (adjustment) layer — RESOLVED (Tommy 2026-07-01)

**The adjustment is baked into Valogix.** Tommy adjusts the forecast *inside
Valogix*; the exported file already carries the adjusted numbers. There is no
separate manual "Adj" step to encode.

Proof: Book200's "Adj" Lavender device (`811573031342`) = 85,235. The current
Valogix `SBGA-MT` export (07-01) = **85,285** — identical (rounding). The earlier
"69,639" was simply the *stale* 06-15 export before Tommy's in-system update.

**Implication for the planner:** use the Valogix file **as-is**. It is the
adjusted forecast of record. No editable-column workaround, no encoded uplift
rule. The only discipline required: **always pull the current Valogix export**
so the latest in-system adjustments flow through.

---

## 7. Output — the "ShipBob PO Planner"

**ONE workbook, SIX tabs — a Planner tab AND an Analysis tab per brand**
(Tommy 2026-07-13): `MTB Planner · SS Planner · NFMD Planner · MTB Analysis ·
SS Analysis · NFMD Analysis`.

**Planner tabs** (interactive — the "what to order" view):
- **Editable inputs** (yellow): Lead Time · Coverage/DOS · Safety.
- Shopify/TikTok/Walmart DAV · Total DAV · Trail DAV · Trend · On Hand · Open PO's
  · Days Cover · Days Cover w/PO · Stockout ETA · Target Stock · New PO QTY ·
  To order · Note (EXPEDITE/gating) + **Open Purchase Orders** section.

**Analysis tabs** (the "what's demand doing" view):
- Shopify/TikTok/Walmart DAV · Total DAV · Trail DAV · Δ% · Trend · channel mix %
  · **quarterly demand blocks Q1–Q4 (this yr + next) + FY totals** (Valogix
  Shopify+TikTok units; Walmart stays in the DAV columns) · brand **TOTAL row**.

Brand split: MTB = ShipBob 385579 · Valogix SBGA-MT + TIKTOKMT ·
SS = 385953 · SBGA-SS + TIKTOKSS (SS items) + Walmart ·
NFMD = 385954 · SBGA-SS + TIKTOKSS (NFMD items) + Walmart.

**No Amazon** — excluded from this node entirely (its own section, Tommy 2026-07-01).

```
python scripts\build_shipbob_po_planner.py
→ outputs/YYYY-MM-DD/shipbob-po-planner-YYYY-MM-DD.xlsx   (tabs: MTB, SS, NFMD)
```

---

## 8. Inputs to drop weekly (`reports/_inbox\`)

| Input | File pattern | Feeds |
|---|---|---|
| Valogix history/forecast | `schain_itemLocationHistoryForecast_*.csv` | Shopify + TikTok demand |
| ShipBob Inventory Status ×2–3 | `inventory-export-blob_385579*` / `*385953*` / `*385954*` | On hand |
| SAP Open POs | `Open POs.xlsx` | Open PO's + ETAs |
| Walmart Inventory Health ×2 | `inventoryHealth*.csv` (NFMD + SS) | Walmart demand |

---

## 9. Open items
- [x] ~~Confirm Walmart demand field~~ — Forecast buckets extrapolated (§3). ✅
- [x] ~~Resolve the Adj layer~~ — baked into Valogix; use file as-is (§6). ✅
- [x] ~~Confirm Shopify source~~ — Valogix SBGA is the sales of record (§3). ✅
- [ ] Decide horizon: fixed Jul–Dec vs rolling 6 months.
- [ ] Later: overlay In-Transit Log for transload/PO visibility (§4).
- [ ] Later sections: **Amazon**, **Alliance/CA**, **Floship/Intl**.
