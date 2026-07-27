---
title: Amazon CA Replenishment Planner — SOP
created: 2026-07-27
updated: 2026-07-27
tags: [sop, amazon, canada, replenishment, planner]
brands: [MTB, SS, NFMD]
---

# Amazon CA Replenishment Planner — SOP

Forward-looking demand & replenishment plan for **Amazon Canada**, on the shared
ShipBob-model layout (`replen_layout.py`). Same look as the Amazon US and ShipBob
planners: half-month coverage map + inventory projection + persistent actions log.
Every number is computed in Python and written as a value; only the coverage map +
projection are formulas (so the live "Report as-of" date re-forecasts). No raw-data
tabs, no cross-sheet formulas.

**Script:** `MTB-SupplyChain/scripts/build_amazon_ca_replen.py`
**Output:** `outputs/YYYY-MM-DD/amazon-ca-replen-YYYY-MM-DD.xlsx`
**Run:** `python scripts\build_amazon_ca_replen.py` (or `build_all.py` for the whole suite)

---

## The CA supply model

Amazon CA is **staging-fed** and replenished from **Alliance** (Alliance Storage Group =
`ASG-*` in SAP). (`UNCA-*` / "UNIS Canada" is a **US** warehouse despite the name — it is
NOT the Amazon-CA replenisher.)

```
Supplier (ocean ~140d) → Alliance CA (ASG-*) → (~60d transfer) → Amazon CA FBA
```

| Column | What it is | Source |
|---|---|---|
| ASIN / SKU / Desc | identity — short (item-master) description | FBA listing + item master + DESCRIPTION_OVERRIDE |
| Demand (D–K) | monthly = CA FBA `units-shipped-t90 ÷ 90` × days-in-month, shaped by the matching **US SoStocked seasonality** curve (flat where no US match) | CA FBA export |
| On Hand (✎) | CA FBA `available + inbound-working + Reserved Staging + Reserved FC Processing` (units physically at the CA FC; matches the US planner). Excludes pending-removal and `inbound-shipped`. | CA FBA export |
| Inbound → FBA (projection) | FBA `inbound-shipped` — units shipped to FBA, **in transit, not yet received**. Shown separately; NOT in On Hand, NOT credited to coverage (so a stuck/unreceived load stays visible). | CA FBA export |
| Incoming (PO → CA) | supplier Open POs to `ASG-*`, phased at staging-ETA **+60d** (sellable-on-CA) | SAP Open POs |
| Alliance CA (projection) | Alliance/Hereford **direct** on-hand — read via a style-safe reader; **Remaining Quantity is in CASES → × case-pack** (`CS-24` → ×24). The **send-in reservoir**. Falls back to SAP ASG-* In Stock−Committed if the direct export is absent. | Alliance "My Inventory on Hand" export |
| Send-in-to-cover thru {mo} | units to **transfer from Alliance → Amazon CA** to avoid stockout | computed |

**Key model choices** (match the US planner):
- Only **Active & class A–D** SKUs show on the brand tabs; the rest go to the **Excluded** tab with a reason.
- Alliance staging is a **send-in reservoir**, NOT auto-credited into the coverage balance (it needs the 60d transfer). Coverage = On Hand + incoming POs − demand. The Send-in number tells you how much to move in; compare it to the Alliance-CA reservoir column.

---

## How to read it

1. **Coverage map (green→red half-months)** — projected Amazon-CA inventory each half-month; red = runs short.
2. **PO → CA blocks (blue)** — the half-month a supplier PO becomes *sellable on Amazon CA* (staging arrival + 60d). Hover a stepped-up cell for the PO breakdown.
3. **Inventory Projection (bottom)** — running end-of-month balance, exact **Stockout Date**, **Send-in-to-cover** (≈+3mo / +6mo / end), the **Alliance CA** reservoir, and the two-part **Actions** log (dated done-history + editable New action).
4. **Report as-of cell (yellow)** — edit the date to re-prorate the current month.
5. **On Hand cell (cream ✎)** — override and downstream numbers cascade.

---

## Inputs (auto-filed by `sort_downloads.py`)
- CA FBA exports → `seller-central/CA/{MTB,NFMD,SS}/` (content-sniffed by `marketplace=CA`).
- SAP Inventory in Warehouse → `reports/_data/sap-inventory/` (ASG-* staging).
- SAP Open POs → `reports/_data/sap-open-pos/` (supplier POs to ASG-*).

## Constants
`STAGING_TO_CA_DAYS=60` · `TRANSIT_DAYS=45` · `READY_TO_LOAD_DAYS=10` · `RECEIVING_LAG_DAYS=14` · `N_MONTHS=8` · `CA_STAGING_WH = ASG-MTB/ASG-NF/ASG-SS`.

---

## Sibling planners (same shared layout)
- **Amazon US** — `build_amazon_us_replen.py`. Demand = SoStocked; On Hand = FBA+AWD (removal-qty dropped); reservoir = ShipBob FREE-to-Transfer + Unis; arrivals = POs to AMZN-*/UNSC-*/UNCA-* + container. Reconciles with the retired legacy `amazon-replen` (same demand/on-hand/rows).
- **ShipBob** — `build_shipbob_replen.py`. UPC-first; demand = Valogix; On Hand = ShipBob sellable.
- Layout lives once in `replen_layout.py` — change it there, all three update.

## Notes / gotchas
- **All 3 brands.** SS **is** live on amazon.ca (real velocity, e.g. SIMA ~3,496 u/mo); CA velocity comes from the CA FBA export, not Sellerboard CA.
- **No CA forward forecast** (SoStocked is US-only) → demand is trailing velocity shaped by the US seasonal curve. Watch for a ramp lagging.
- **Open in Excel to calculate** — formulas written without cached values. Validated static: 0 cross-sheet refs, standard functions only.
