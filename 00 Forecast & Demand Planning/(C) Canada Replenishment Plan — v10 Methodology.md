# (C) Canada Replenishment Plan — v10 Methodology

> Reference doc capturing how the Canada FBA replenishment + supplier PO sizing was built. Use this to refresh the plan in future cycles or hand off to someone else.
>
> **Plan date:** May 1, 2026
> **Owner:** Tommy Sapia
> **Workbook:** `CA_Plan_v10.xlsx` (in SharePoint → Supply Chain → ANALYSIS WEEKLY INVENTORY REPORT)
> **Tabs:** `Replenishment Plan` (FBA shipment) · `Harry PO` (next supplier order)

---

## Project scope

Size the FBA Canada replenishment shipment plus the next supplier PO to Harry for **18 SKUs across three brands**:
- **MTB** — Sonicsmooth, Soniclear
- **NFMD** — NasalFresh family
- **SPA** — SIMA, Nova, Aiva

---

## Source files used to build v10

| File | Purpose |
|---|---|
| `Canada Shipment Plan (1).xlsx` | Original template — used for layout, formatting, formula structure |
| `MichaelToddBeautyprojected-forecast-model-...xlsx` | MTB SoStocked monthly forecast (May 2026 → Jan 2027) |
| `nasalfreshprojected-forecast-model-...xlsx` | NFMD SoStocked monthly forecast |
| `spascienceprojected-forecast-model-...xlsx` | SPA SoStocked monthly forecast |
| `inventory-export-blob_385579_*.csv` | ShipBob on-hand for MTB (143 SKUs) |
| `inventory-export-blob_385953_*.csv` | ShipBob on-hand for SPA (309 SKUs) |
| `inventory-export-blob_385954_*.csv` | ShipBob on-hand for NFMD (36 SKUs) |

---

## Demand methodology (locked in)

CA monthly demand is sourced per brand:

| Brand | CA demand source | Reasoning |
|---|---|---|
| MTB (existing 4 SKUs) | CA row from SoStocked file as-is | CA rows populated and reasonable |
| MTB Pro+ (Lavender, Pink) | **13% × US / US+MX / NAm fallback** | SoStocked CA rows = 0 for Pro+ variants |
| NFMD | CA row from SoStocked file as-is | CA rows populated |
| SPA (SIMA, Nova Green, Nova Pink) | **13% × US / US+MX / NAm fallback** | SPA CA rows mostly empty |
| SPA Aiva Black | Mirrored Aiva Deluxe pattern × 13% | Not in SoStocked file at all |

### The 13% rule
- Fallback order: **US row first**, then **US+MX** (combined), then **NAm** (US+MX+CA combined)
- Only one non-CA row exists per SKU in the SoStocked file — no double-counting risk

### Yellow-highlighted cells
Yellow demand cells in the workbook = estimates from the 13% rule. **Replace these when SoStocked publishes real CA forecasts.**

---

## Manual overrides

### Soniclear White Marble (B08HH883BK) — Jul/Aug demand smoothing

SoStocked file showed:

| Month | File value | Used | Why |
|---|---:|---:|---|
| May | 74 | 74 | trusted |
| Jun | 72 | 72 | trusted |
| **Jul** | **2** | **70** | obvious bad data — surrounding months ~70 |
| **Aug** | **0** | **70** | obvious bad data |
| Sep | 63 | 63 | trusted |

Replaced Jul/Aug with average of surrounding months. Without this fix, the model would have severely under-shipped this SKU.

### Inbound to FBA = 0 (all SKUs)

User confirmed nothing is currently in transit to Amazon CA. Original template had stale placeholder values (e.g., 1,500 inbound on NasalFresh MD w/Shipper). All inbound values forced to 0.

### SKUs explicitly excluded

| SKU | Reason |
|---|---|
| Sonicsmooth Pro+ Peach Fuzz | Phase-out item |
| Sonicsmooth Pro+ White | Removed per user request |
| Nova White | Removed per user request |

---

## Formula logic

### Replenishment Plan tab (FBA shipment) — cols T, U, V

```
T (Units to Send In)  = MAX(0, CEILING(R - (G + F), case_pack))
U (Case Count)         = T / VLOOKUP(SKU → Sheet4 master carton qty)
V (CBM)                = U × VLOOKUP(SKU → Sheet4 carton volume)

where:
  R = May→Sep demand = SUM(I:M)
  S = Oct→Jan demand = SUM(N:Q)
  F = Current FBA on-hand
  G = Inbound to FBA (= 0 currently)
```

### Harry PO tab (next supplier order) — cols W, X, Y

```
W (PO Units) = MAX(0, CEILING(IF('Replenishment Plan'!T = 0,
                              (R+S) - (F+G),    ← if no FBA shipment, PO covers full 9 months
                              S),                 ← if FBA shipment exists, PO covers only Oct→Jan
                              po_round))
X (Cases) = W / po_round
Y (CBM)   = X × VLOOKUP(SKU → Sheet4 carton volume)
```

The PO formula references the FBA tab's T column — change FBA shipment qty and the PO recalculates automatically.

### Pallet count & container utilization

```
Pallets = total CBM / 2.3            (assumes 2.3 m³ per pallet — international standard)
20' container utilization = total CBM / 28
```

---

## Final plan — FBA replenishment shipment

**Total: 13,376 units · 939 cases · 33.03 CBM · ~14.36 pallets**

| Brand | SKUs | Units | Pallets |
|---|---:|---:|---:|
| MTB | 6 | 7,680 | 5.95 |
| NFMD | 7 | 3,008 | 7.71 |
| SPA | 5 | 2,688 | 0.70 |

### Top 5 SKUs (drive 92% of shipment volume)

| Rank | SKU | Units | Pallets | % of total |
|---|---|---:|---:|---:|
| 1 | NasalFresh MD w/Shipper | 2,226 | 6.13 | 43% |
| 2 | Pro+ Lavender ⚠️ | 3,912 | 3.19 | 22% |
| 3 | Sonicsmooth Lavender | 2,136 | 1.43 | 10% |
| 4 | Premium Bundle | 318 | 1.40 | 10% |
| 5 | Pro+ Pink ⚠️ | 1,248 | 1.02 | 7% |

⚠️ = yellow-flagged in workbook (estimated demand using 13% rule)

---

## Final plan — Harry PO

**Total: 23,768 units · ~150% of a 20' container** (needs 40' or split shipment)

PO logic: covers full 9 months of demand minus current pipeline (FBA + ShipBob). When the FBA shipment runs from the Replenishment Plan tab, the PO automatically scales down to cover only the Oct→Jan window for those SKUs.

---

## ⚠️ Open items / things to watch

1. **Pro+ Lavender demand assumption** — 1,044 units/month CA estimate is based on 13% × US+MX. Sanity-check against actual recent CA sell-through. If actual is ~700/month, the FBA shipment is over-sized by ~1,200 units.

2. **Sheet4 column AC mislabeled** — "M/Carton Volume (Inches)" actually contains values in m³. Worth fixing the column header in your master item file to avoid confusion later.

3. **Pro+ PO case-pack rounding** — currently set to 24 (matches FBA case pack). Original Sonicsmooth Lavender uses 54 for PO rounding — likely Harry's pallet-tie or carton-of-cartons spec. Confirm with Harry what the right Pro+ PO round-up is.

4. **NasalFresh MD w/Shipper at 6 pallets in one shipment** — that's 5 months of cover for the highest-velocity SKU. Consider splitting into 2 shipments timed roughly 6 weeks apart to ease FBA storage limits and reduce stockout risk.

5. **Several small NFMD SKUs ship 100 units each** because of case-pack rounding (Auto Clean = 50/case, Replacement Pillows = 100/case). Those are 6+ months of cover for SKUs moving <1 unit/day. Consider FBM/MFN fulfillment from ShipBob instead of FBA for these slow movers.

6. **SIMA Replacement Blade Kit at 2,268 FBA units** — also on the 13% × US+MX assumption. Note in file says "sima- bump up to 1200" — need clarification on whether that's a separate manual override.

7. **SIMA Pink** has zero velocity and zero forecast. Note in file says "bump up to 1200" — currently shipping 0. Need direction on whether to add a manual override.

8. **Container utilization at 150% of a 20'** for the Harry PO — fits in one 40' or splits across two 20's. Either works depending on freight rates and timing.

---

## How to refresh this plan in future cycles

1. Drop new SoStocked forecast files into the uploads folder (one per brand)
2. Drop new ShipBob inventory CSVs (one per brand)
3. Drop the latest Amazon CA inventory export (when available — would replace the placeholder F/G/E values)
4. Re-run the build with the same SKU list, demand methodology, and overrides documented above

---

## File version history

| Version | Change |
|---|---|
| v1–v3 | Initial builds, formula validation, format match |
| v4 | Added Nova Green/Pink/White and Aiva Black, smoothed Soniclear White Marble |
| v5 | Added yellow highlights to estimated-demand cells |
| v6 | Added Pro+ Lavender, Pink, White (excluded Peach Fuzz) |
| v7 | Split PO into separate tab (custom layout — superseded) |
| v8 | Rebuilt Harry PO tab to mirror original Replenishment Plan format |
| v9 | Added pallet count to Harry PO tab; pre-calculated formula values |
| **v10** | **Final — removed Pro+ White and Nova White per user request** |

---

## Related

- Workbook: `CA_Plan_v10.xlsx` (SharePoint → Supply Chain → ANALYSIS WEEKLY INVENTORY REPORT)
- US weekly pipeline: [[06 Processes & SOPs/(C) Weekly Analysis SOP — Step by Step]]
- Sourcing: [[06 Processes & SOPs/(C) Weekly Inputs Sourcing SOP]]

---

*Created: May 5, 2026 — methodology captured from CA_Plan_Notes.md*
