---
tags: [demand-planning, amazon, node-spec]
node: Amazon US
brands: [MTB, SS, NFMD]
status: draft-v1
updated: 2026-07-13
author: Claudian (with Tommy)
---

# Amazon US Node — Demand Planning Structure

> The demand-planning spec for the **Amazon US** node, learned from Tommy
> (2026-07-13) and built to mirror his Book111 architecture. One of the node
> sections (ShipBob has its own spec). US only for now.

---

## 1. Scope
- **Amazon US only.** Per brand: **MTB · SS · NFMD** (separate Seller Central logins).
- Amazon is its **own node** — kept out of the ShipBob plan and vice-versa.

> **ARCHITECTURE RULE (Tommy 2026-07-13): every Amazon marketplace is its OWN
> node / planner. Never merge them** — each is supplied by different 3PLs, with
> different lead times and waterfalls:
> | Amazon node | Supplied by |
> |---|---|
> | **US** | AWD + UNIS + ShipBob (US) |
> | **CA** | Alliance (CA staging) |
> | **UK / AU / EU** | Floship / international 3PLs |
>
> Naming convention: `build_amazon_us_planner.py`, `build_amazon_ca_planner.py`, …
> (CA/UK/AU/EU deferred — no item-level velocity/stock wired yet.)

---

## 2. Demand — Seller Central sell-through (NOT Valogix, NOT Sellerboard)
The demand of record is Amazon's own **units-shipped** from the Seller Central
FBA report:
- **Base velocity (DAV) = `units-shipped-t90` ÷ 90** — smoothed. Chosen over T30
  because T30 falls into seasonal troughs and lies (w/Shipper read T30≈1 → "never
  order" in Book111, while true T90 velocity is ~119/day).
- **`units-shipped-t30` ÷ 30 = TREND flag** (accelerating >1.3× / slowing <0.7×).
- Analysis tab also shows T7/T60 per-day for the full velocity picture.

> **Limitation:** Seller Central gives trailing *windows* (t7/30/60/90), not
> monthly history — so there is **no seasonal curve** on the Amazon side (unlike
> NFMD on ShipBob). If Amazon seasonality is needed, pull historical monthly
> shipped units separately.

---

## 3. Position — where the inventory sits
| Node | Source | Role |
|---|---|---|
| **FBA** = available + **in-transit** | FBA report (avail) + **Outbound Shipment Data** report (in-transit = open shipments' Confirmed−Received) | the sell point |
| **AWD** = available + inbound | AWD inventory report | Amazon's reserve warehouse |
| **UNIS** = cases × units-per-carton | UNIS WMS export (Alessandro) | **primary refill provider** |
| **ShipBob** = on-hand − channel reserve | ShipBob export (per-brand blob) | transitional — **sunset 2027** |

- **Days Cover = (FBA + AWD) ÷ DAV** — the "at Amazon" runway. Target **120 days**.
- **UNIS is in CASES.** Multiply by units-per-carton (§6). This is why Hair Spray
  reads 43,680 units (910 cases × 48), not 910.
- **ShipBob is shown NET** of its own Shopify/TikTok/Walmart reserve (90 days), so
  pulling to Amazon doesn't strand those channels.

---

## 4. The replenishment waterfall (the plan)
Refill FBA to its target by pulling from what you already own, cheapest/closest
first, before cutting a PO:

```
FBA need = MAX(0, DAV × FBA_target − FBA position)
  → ① pull AWD        (Amazon's own warehouse)
  → ② pull UNIS       (PRIMARY external provider; can supply FBA directly or AWD)
  → ③ pull ShipBob    (net; SUNSET end-2026 — toggle off for 2027)
  → ④ supplier PO     (whatever is still short)
```

- **FBA target = 90 days** (editable in-sheet, cell B2).
- **UNIS can supply FBA directly** (not only via AWD) — it fills FBA need at step ②.
- **ShipBob→Amazon is being eliminated for 2027.** Cell **B4 = Include ShipBob?**
  (1 = 2026 / **0 = 2027**). Set B4=0 and the waterfall drops ShipBob → the
  "PO (short)" column reveals the true UNIS + supplier-PO burden once ShipBob is gone.

---

## 5. Output — the workbook
Standalone, operator-triggered. **THREE clean tabs per brand** (Tommy 2026-07-14,
"keep it simple"): the dense combined Planner/waterfall was retired.

| Tab | Purpose | Cadence |
|---|---|---|
| **{brand} Send** | DOS-driven: FBA DOS (60) + AWD DOS (120) → Send → AWD, Send → FBA per SKU | daily/weekly |
| **{brand} Analysis** | position — FBA & AWD each Available / In-Transit / Total, UNIS, ShipBob, Amazon Pos, Days Cover, Proj Stockout | daily/weekly |
| **{brand} Map** | coverage heatmap (matches the 07-09 AMZ-Demand file): Jul→Feb monthly colored 🟢🟠🟩🔴, Total, Inventory (FBA+AWD), UNIS, Open PO, exact **Run Out** date | seasonal / peak prep |

The Map is the **date-driven analysis** — it shows month-by-month whether you're
covered through the Prime/Black-Friday/holiday window. The Send tab gives the
quantities; the Map shows the timing/coverage.

*(Retired: the waterfall + explicit AWD/FBA deadline-wave send sections. Sizing
lives on the Send tab; coverage/timing on the Map. `build_planner()` remains in
the script marked RETIRED — safe to delete.)*

<details><summary>Retired Planner-tab detail (for reference)</summary>

- **Planner tabs** (interactive): demand (DAV + T30 trend) → position
  (FBA/AWD/UNIS/ShipBob-net) → Days Cover → Proj Stockout → **FBA need →
  ①AWD ②UNIS ③ShipBob ④PO** waterfall → Action. Editable cells: FBA target,
  total target, Include-ShipBob toggle.
- **Send tabs** (`{brand} Send` — its own clean tab, DOS-driven): two editable
  cells — **FBA DOS** (default 60) and **AWD DOS** (default 120). Per SKU, live
  formulas: `AWD target = DAV × AWD_DOS → Send → AWD = max(0, target − AWD now)`;
  same for FBA. DAV = SoStocked forward 90-day (T90 fallback). Hazmat: Send→AWD =
  "—" (ships UNIS/ShipBob → FBA direct). This is the "how many units to send into
  AWD, then into FBA, given the DOS I want to hold at each" answer.
- **Analysis tabs**: demand (T30/day, T90/day, trend) + **position broken out per
  node — FBA and AWD each as Available / In-Transit / Total** (grouped under FBA
  and AWD bands), UNIS, ShipBob net, Amazon Pos (= Total FBA + Total AWD), Days
  Cover, Proj Stockout. In-Transit = open shipments to that node.
- **Coverage Map** (under each Planner tab): month-by-month color-coded heatmap.
  - Monthly demand = **SoStocked "Forecasted Sales Monthly"** where it exists,
    **else T90 sell-through spread flat** (the `Demand src` column flags which).
    SoStocked is the seasonal forecast (carries the Q4 ramp). Coverage (full
    exports): MTB ~25 SKUs, NFMD ~15, SS ~61. Marketplace labels vary — MTB/NFMD
    use `US`, SS uses `NAm` / `US+MX` — so the loader accepts any label starting
    `US` (incl. `US+MX`) or `NAm`/`NA`, and keeps the **largest-total row per UPC**
    (a few UPCs appear on multiple region rows — dedupe avoids double-count).
    T90 fallback covers any SKU SoStocked misses, so **nothing shows falsely
    "Covered."**
  - Supply tiers: **Inventory (FBA+AWD) + UNIS + Open PO**.
  - Colors (live conditional formatting — Tommy's 4 rules, cumulative demand vs tiers):
    🟢 covered by Inv+UNIS · 🟠 stockout month (PO exists) · 🟩 covered by PO if it
    lands this period · 🔴 blown through everything, no PO left.
  - **Run Out (incl PO)** = the exact date stock crosses Inv+UNIS+PO, computed by
    walking the **SoStocked WEEKLY forecast** (55 weeks) and interpolating within
    the crossout week — so it pins the stockout to the week, seasonally. Falls back
    to T90-flat (`today + supply/DAV`) when no SoStocked weekly. "Covered" if it
    holds past the map horizon.
- **AWD Send Plan** (under each Planner tab): how much to send **ShipBob → AWD**,
  in two waves tied to Amazon's peak deadlines (Tommy 2026-07-13):
  - **Wave 1 — by Sep 2** (Prime Big Deal Days): cover Sep–Oct demand − AWD on hand.
  - **Wave 2 — by Oct 14** (holidays; Oct 14 = cutoff to have holiday product in
    AWD): cover **Nov–Jan** demand − AWD left after Wave 1. Covers through Jan 31.
  - Each wave is a small waterfall — **pull UNIS first, then ShipBob** (net);
    what's left = **Short (PO)** = genuine supplier gap. Current demand (now→Sep)
    depletes AWD first. Demand = SoStocked weekly (T90 fallback). Columns: AWD now ·
    UNIS avail · ShipBob avail · Demand Sep–Oct · Demand Nov–Jan · W1 ←UNIS · W1 ←SB
    · W2 ←UNIS · W2 ←SB · Short (PO).
  - **HAZMAT excluded** (`sku_rules.HAZMAT`, e.g. Hair Spray) — Amazon AWD does not
    store hazmat; those items ship **UNIS/ShipBob → FBA direct** (see FBA plan).
  - *Sep 2 / Oct 14 are AWD-arrival deadlines — ship from ShipBob earlier by the
    ShipBob→AWD transit time.*
- **FBA Send Plan** (under each Planner tab): the downstream leg — how much to
  stage **AWD → FBA**, on the FBA deadlines:
  - **Wave 1 — by Sep 16** (Prime), **Wave 2 — by Oct 28** (holidays → Jan).
    Optimized-split dates (most sellers); minimal-split is a week earlier
    (Sep 9 / Oct 21).
  - Source = **AWD** for normal items (FBA's bulk reserve); **HAZMAT sources
    UNIS→ShipBob direct** (bypasses AWD). `Source` column flags which. "Short (PO)" =
    the source can't cover → restock AWD via the AWD Send Plan / supplier PO. Columns:
    FBA now · AWD avail · UNIS avail · ShipBob avail · Demand Sep–Oct · Demand Nov–Jan
    · Send by Sep 16 · Send by Oct 28 · Short (PO) · Source.
  - **Pipeline chain:** UNIS/ShipBob → AWD (AWD Send Plan) → FBA (FBA Send Plan).
    FBA Short uses *current* AWD, so it overstates for SKUs the AWD plan will
    restock (e.g. Hair Spray) — read the two plans together.

</details>

```
python scripts\build_amazon_us_planner.py
→ outputs/YYYY-MM-DD/amazon-us-planner-YYYY-MM-DD.xlsx   (tabs: Send · Analysis · Map ×3 brands)
```

---

## 6. Case-packs — UNIS cases → units (Tommy 2026-07-13)
UNIS `Available` is in **cases** (`Units/pkg` in the export is a useless "1").
Units-per-carton map (in `build_amazon_planner.CASE_PACK` — **TODO: promote to
`sku_rules`**):

| UPC | Item | units/carton |
|---|---|--:|
| 850038082383 | NasalFresh w/ Shipper | 16 |
| 811573031335 | SonicSmooth Clear Kit | 150 |
| 811573031342 | Pro+ Lavender device | 45 |
| 811573031359 | Pro+ Pink device | 45 |
| 811573031366 | Pro+ White device | 45 |
| 850003115078 | SIMA Replacement Blades | 150 |
| 811573031410 | Hair Identifier Spray | 48 |
| 850038082352 | NasalFresh Premium Bundle | 12 |
| 850038082567 | Eucalyptus Oil | 48 |
| 850038082543 | SIMA Premium Bundle (White) | 84 |
| 850038082536 | SIMA Premium Bundle (Mint) | 84 |

New UNIS SKUs missing a pack are logged at build time (`⚠ UNIS case-pack MISSING`).

---

## 7. Validation (first build, 2026-07-13)
- **Hair Spray (811573031410):** DAV 159/day · UNIS 43,680u · FBA need 3,038 →
  pulled from UNIS → **PO short 0.** (Matches "fed by UNIS, no PO.")
- **w/ Shipper (850038082383):** T90 → DAV 119/day (vs Book111 T30-trap "879,780
  days cover") · need 4,034 → pulled from AWD → PO short 0.
- **Premium Bundle (850038082352):** FBA=0 (stocked out) · DAV 220/day → need
  19,800 → AWD 16,212 + UNIS 3,588 → PO short 0. Flags urgent transfer.
- SKU counts: MTB 32 · SS 72 · NFMD 17.

---

## 8. Inputs to drop (`reports/_data`)
| Input | Path | Feeds |
|---|---|---|
| Seller Central FBA report ×3 | `seller-central/US/{brand}/*.csv` | demand + FBA available |
| Outbound Shipment Data ×3 | `seller-central/US/{brand}/*.xlsx` (tab "Outbound Shipment Data") | FBA in-transit (open shipments); confirms AWD→FBA is Amazon-Auto |
| AWD inventory report ×3 | `seller-central/US/{brand}/AWD-inventory-report*.csv` | AWD position |
| UNIS WMS export | `unis/*.xlsx` (Alessandro; `Available` in CASES) | UNIS position |
| ShipBob export ×3 | `shipbob/**/*<blob>*.csv` | ShipBob net (via ShipBob node) |
| SoStocked projected-forecast ×3 | `sostocked/{brand}/projected-forecast-model-*.xlsx` | coverage-map monthly demand ("Forecasted Sales Monthly", US) |
| SAP Open POs | `sap-open-pos/*.xlsx` | coverage-map Open PO tier |

---

## 9. Open items
- [ ] **2027 transition:** ShipBob→Amazon eliminated; UNIS is primary. Toggle built (B4).
- [ ] Promote `CASE_PACK` to `sku_rules` (single source of truth).
- [ ] Amazon **seasonality** — needs historical monthly shipped units (not in the
      trailing-window report).
- [ ] Wire UNIS export into `sort_downloads.py` auto-classification.
- [ ] Later: link Amazon's ShipBob-pull back to the ShipBob node's own plan so the
      two nodes reconcile (don't double-commit ShipBob units).
