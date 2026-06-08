# Tab 2 — Amazon CA

**Purpose:** Every active Amazon Canada listing. Same structure as Amazon US ([[(C) 01 - Amazon US]]) but with CA-specific data and a few column differences.

---

## What's Different from Amazon US

### Columns HIDDEN on Amazon CA (but shown on US)

| Column | Why |
|---|---|
| **OPEN PO (SUPPLIER)** | CA has no direct Amazon supplier POs — supplier ships to staging (Alliance WH) first, then routed to Amazon CA |
| **PO ARRIVES ON** | Same reason — always blank for CA |
| **DAILY SALES (AMAZON US)** | Wrong marketplace |

### Columns VISIBLE on Amazon CA (hidden on US)

| Column | Source | Calculation |
|---|---|---|
| **ALLIANCE WH (CA INBOUND)** | `reports/_data/sap-inventory/SAPInventoryinwarehouse.xlsx` (sections ASG-MTB / ASG-NF / ASG-SS) | Sum of "In Stock" + "Ordered" units in Alliance warehouses per UPC. These units are staged for CA and transfer to Amazon CA in ~60 days. |
| **DAILY SALES (AMAZON CA)** | (relabeled `daily_vel`) — SoStocked CA Adj. Velocity | Per-marketplace velocity. **Does NOT use Sellerboard CA Dashboard** (over-stated CA velocity by ~50× in prior runs). |

### Column Renamed on Amazon CA

| Original | Renamed on CA tab |
|---|---|
| STOCKOUT DATE (W/ INCOMING PO) | **STOCKOUT DATE (W/ ALLIANCE)** — because incoming = Alliance WH not supplier PO |

---

## CA-Specific Stock + Velocity Sources

| Data | Source |
|---|---|
| FBA stock | `reports/_data/seller-central/CA/<brand>/*.csv` (CA FBA Health Report) |
| Reserved FC Transfer | Same file (mapped from "Reserved FC Transfer" column) |
| AWD | CA does NOT use Amazon AWD — column shows 0 or blank |
| AWD Inbound | Same — 0 for CA |
| FBA Pipeline (inbound to FBA) | CA FBA Health Report — same fields as US |
| Alliance WH staging | `reports/_data/sap-inventory/SAPInventoryinwarehouse.xlsx` — ASG-MTB / ASG-NF / ASG-SS warehouse sections |
| Adj. Velocity (CA) | SoStocked CA — per-marketplace |
| 9-month forecast | SoStocked PFM "Forecasted Sales Monthly" tab — lookup by `(ASIN, "CA")` |
| CA seasonality (fallback) | Sellerboard CA Dashboard Products (`reports/_data/sellerboard/<brand>/canada/*.csv`) — used only when SoStocked CA PFM is missing for an ASIN |

---

## CA Forecast Source Priority

When determining the 9-month forecast for a CA item, the pipeline tries these sources in order:

1. **SoStocked CA PFM** — authoritative if `(ASIN, "CA")` exists in the "Forecasted Sales Monthly" tab with non-zero values
2. **CA Dashboard Seasonality** — anchored to SoStocked CA Adj. Velocity, shape from CA Dashboard quarterly factors. Math: `(adj_vel / current_q_factor) × month_q_factor × days_in_month`
3. **Flat-rate fallback** — `adj_vel × days_in_month` (no CA Dashboard data, no SoStocked CA PFM)

---

## What's the SAME as Amazon US

All other columns work identically:
- Identity columns (Status, Brand, ABC, Product, SAP UPC, Amazon SKU, ASIN)
- Stockout dates (with stockout_date_with_po relabeled — see above)
- Stock layout (TOTAL AT AMZN = FBA + FC + AWD where AWD is usually 0)
- DOS columns (4 progressively wider views — physical at Amazon = FBA + FC + AWD)
- Demand Swing
- Rolling 9-month forecast (sourced from CA PFM, not US PFM)
- Lead Time (60d) + Supplier Lead Time (140d)
- Scratch pad (SB Transfer, Cover Through, etc.)
- Audit columns (PFM 9MO, ACTUALS 9MO, FORECAST DELTA %)

---

## Status Logic on CA

Same as Amazon US, except:
- CRITICAL / HIGH thresholds are computed against `net_pos` which on CA = FBA + FC + AWD inbound + FBA pipeline (no AWD since CA has none)
- **PO COVERED** demotion fires when Alliance WH staging or a CA-bound SAP PO closes the gap

---

## Common CA Pitfalls

1. **Sellerboard Monthly velocity inflated 50×** — DO NOT apply US+CA combined Sellerboard data to CA. Pipeline explicitly skips this. CA velocity = SoStocked Adj. Velocity per marketplace.
2. **CA FBA Health export only returns SKUs with current inventory** — items that just stocked out may disappear from the source file. Synthesizers cover by reading Sellerboard CA Dashboard + SoStocked CA.
3. **AWD column = 0 on most rows** — that's correct; CA doesn't use Amazon AWD.
4. **Forecast may show seasonally heavy month then drop** — CA Dashboard data may have stockout months that depress historical seasonality. Pipeline anchors to SoStocked CA Adj. Velocity to avoid double-counting.
