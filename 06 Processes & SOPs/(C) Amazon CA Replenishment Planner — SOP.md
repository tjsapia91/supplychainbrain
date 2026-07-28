---
title: Amazon CA Replenishment Planner — SOP
created: 2026-07-27
updated: 2026-07-28
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
Supplier (ocean ~45d) → Alliance CA (ASG-*) → (~25d transfer) → Amazon CA FBA
```

> **Scope (Tommy 2026-07-28):** the CA planner covers ONLY the SKUs currently fulfilled
> from the Canada-dedicated warehouse (Alliance) — that's why the CA FBA export is short
> (a handful of listings per brand). Every other Amazon.ca listing is fulfilled from **US**
> inventory and is planned by the **US** planner, not here. A small row count is CORRECT,
> not a filtered export. The list grows automatically as more SKUs move to CA-only
> fulfillment (they show up in the CA FBA export).

| Column | What it is | Source |
|---|---|---|
| ASIN / SKU / Desc | identity — short (item-master) description | FBA listing + item master + DESCRIPTION_OVERRIDE |
| Demand (D–K) | **makeshift CA forecast** (BookFloship → `Canada Forecast` tab, per-SKU monthly units) where the SKU has one — stopgap until a solid CA forecast lands (Tommy 2026-07-28); **else** CA FBA `units-shipped-t90 ÷ 90` × days-in-month shaped by the matching **US SoStocked seasonality** curve | `reports/_data/ca-forecast/` (BookFloship) + CA FBA export |
| On Hand (✎) | CA FBA `available + inbound-working + Reserved Staging + Reserved FC Processing` (units physically at the CA FC; matches the US planner). Excludes pending-removal and `inbound-shipped`. | CA FBA export |
| Inbound → FBA (projection) | FBA `inbound-shipped` — units shipped to FBA, **in transit, not yet received**. Shown separately; NOT in On Hand, NOT credited to coverage (so a stuck/unreceived load stays visible). | CA FBA export |
| Incoming (PO → CA) | supplier Open POs to `ASG-*`. **Two dates:** arrival at Alliance = container-plan **Load + 45d** (concrete) if booked, else **Ship-By Date + 45d** (estimated), else Original Due Date; then **sellable on Amazon CA = Alliance arrival + 25d** transfer. Container plan overrides the open PO once a container books. | SAP Open POs + Container Plan |
| Alliance CA (projection) | Alliance/Hereford **direct** on-hand — read via a style-safe reader; **Remaining Quantity is in CASES → × case-pack** (`CS-24` → ×24). The **send-in reservoir**. Falls back to SAP ASG-* In Stock−Committed if the direct export is absent. | Alliance "My Inventory on Hand" export |
| Units needed (A / B) | **two editable coverage-target columns** — type a horizon in days (default 90 / 180); each shows the resolved future date + units to **transfer from Alliance → Amazon CA** to avoid stockout through that date | computed |

**Key model choices** (match the US planner):
- Only **Active & class A–E** SKUs show on the brand tabs; the rest go to the **Excluded** tab with a reason. **CA is one class wider than US/ShipBob** (which are A–D) — Canada's catalog is tiny, so every CA-fulfilled SKU incl. class E is worth eyes on (Tommy 2026-07-28; e.g. 850003115283 SIMA Pink Target, class E, 804u at Alliance). Controlled by `CA_ALLOWED_CLASSES` in `build_amazon_ca_replen.py`.
- Alliance staging is a **send-in reservoir**, NOT auto-credited into the coverage balance (it needs the 25d transfer). Coverage = On Hand + incoming POs − demand. The Units-needed number tells you how much to move in; compare it to the Alliance-CA reservoir column.
- **Next Arrival shows the Alliance landing date** (when product physically arrives); coverage/stockout math credits it 25 days later (sellable on Amazon CA). Hover the Next Arrival cell for both dates per PO.

---

## How to read it

1. **Coverage map (green→red half-months)** — projected Amazon-CA inventory each half-month; red = runs short.
2. **PO → CA blocks (blue)** — the half-month a supplier PO becomes *sellable on Amazon CA* (Alliance arrival + 25d). Hover a stepped-up cell for the PO breakdown.
3. **Inventory Projection (bottom)** — running end-of-month balance, exact **Stockout Date**, the two interactive **Units needed** columns, the **Alliance CA** reservoir, and the two-part **Actions** log (dated done-history + editable New action).
4. **Report as-of cell (yellow)** — edit the date to re-prorate the current month.
5. **Coverage Target A / B (cream ✎, below as-of)** — type any horizon in days (default 90 / 180); the target date and both Units-needed columns recalc live so you can compare two horizons.
6. **On Hand cell (cream ✎)** — override and downstream numbers cascade.

---

## Inputs (auto-filed by `sort_downloads.py`)
- CA FBA exports → `seller-central/CA/{MTB,NFMD,SS}/` (content-sniffed by `marketplace=CA`).
- SAP Inventory in Warehouse → `reports/_data/sap-inventory/` (ASG-* staging).
- SAP Open POs → `reports/_data/sap-open-pos/` (supplier POs to ASG-*).
- **CA forecast (BookFloship)** → `reports/_data/ca-forecast/` (filename `BookFloship*` **or** any workbook with a `Canada Forecast` tab; sorter routes it early, before the content sniffers). Drop the workbook in `_inbox` each week; the loader reads the newest and pulls the `YYYY-MM` columns for the planner horizon.

## Constants
`STAGING_TO_CA_DAYS=25` (Alliance→Amazon transfer, Tommy 2026-07-28; was 60) · `TRANSIT_DAYS=45` (ocean) · `READY_TO_LOAD_DAYS=10` · `RECEIVING_LAG_DAYS=14` · `N_MONTHS=8` · `CA_STAGING_WH = ASG-MTB/ASG-NF/ASG-SS`.

---

## Sibling planners (same shared layout)
- **Amazon US** — `build_amazon_us_replen.py`. Demand = SoStocked; On Hand = FBA+AWD (removal-qty dropped); reservoir = ShipBob FREE-to-Transfer + Unis; arrivals = POs to AMZN-*/UNSC-*/UNCA-* + container. Reconciles with the retired legacy `amazon-replen` (same demand/on-hand/rows).
- **ShipBob** — `build_shipbob_replen.py`. UPC-first; demand = Valogix; On Hand = ShipBob sellable.
- Layout lives once in `replen_layout.py` — change it there, all three update.

## Notes / gotchas
- **Makeshift forecast is SKU-scoped.** The BookFloship forecast lists MTB SonicSmooth/MicroSmooth/Soniclear SKUs; only the ~6 of them that are actually CA-fulfilled (in the CA FBA export) appear on the MTB tab with forecast demand. Forecast SKUs NOT in the CA FBA export are US-fulfilled → US planner, not here. Replace the workbook with a real forecast later and the loader picks it up automatically.
- **A UPC shows on a brand tab if ANY of: it's in that brand's CA FBA export, has an open PO to that brand's `ASG-*`, OR sits at Alliance for that brand.** The last one means **staging-only SKUs (at Alliance but not yet in the CA FBA export) now appear** so nothing sitting in Alliance is invisible (Tommy 2026-07-28) — they show with On Hand 0, the Alliance reservoir populated, and demand 0 (or forecast) until they land in FBA. Brand routing for staging reads the **Alliance export's Description column (col H)** and classifies by product-line keyword (SonicSmooth/Soniclear→MTB, SIMA/NOVA/AIVA→SS, NasalFresh/Sinus/Salt→NFMD) — self-contained in the Alliance file, no SAP dependency (Tommy 2026-07-28). SAP Inventory ASG-* warehouse code is a silent backup for anything the description doesn't classify. Validated: description brand matches SAP ASG on all 20 Alliance UPCs, 0 disagreements. This replaced the earlier bug where global staging put every staged UPC on all three tabs.
- **Short CA export is correct.** The CA FBA export lists only the SKUs currently fulfilled from Canada; the rest of Amazon.ca is fulfilled from US inventory and planned by the US planner. Don't treat a small FBA row count as a partial/filtered export (Tommy 2026-07-28). Note the brand tabs can still show *more* rows than the FBA export, because Alliance-staged SKUs (awaiting first send-in) are now included too.
- **All 3 brands.** SS **is** live on amazon.ca (real velocity, e.g. SIMA ~3,496 u/mo); CA velocity comes from the CA FBA export, not Sellerboard CA.
- **No CA forward forecast** (SoStocked is US-only) → demand is trailing velocity shaped by the US seasonal curve. Watch for a ramp lagging.
- **Open in Excel to calculate** — formulas written without cached values. Validated static: 0 cross-sheet refs, standard functions only.
