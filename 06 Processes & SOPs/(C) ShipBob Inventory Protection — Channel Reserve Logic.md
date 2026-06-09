# (C) ShipBob Inventory Protection — Channel Reserve Logic

**Captured:** June 8, 2026
**Status:** Active reference + diagnostic checklist
**Why this exists:** When sizing SB→Amazon transfers, the system protects some inventory for non-Amazon channels. This doc explains how, what's missing, and how to validate the reserve is working.

---

## The problem in one sentence

ShipBob is the fulfillment center for **multiple channels** — not just Amazon. Pulling inventory out of SB to feed Amazon's FBA can starve Shopify, Walmart, TikTok, or retail orders that ship from the same SB warehouses.

---

## What SB actually serves

| Channel | Fulfillment path | Pulls from SB? |
|---|---|:---:|
| **Amazon FBA** (US) | SB → AWD → FBA (manual send-in or auto-replen) | ✅ Yes (indirect) |
| **Amazon FBA** (CA) | Alliance (CA staging) → Amazon CA | ❌ No (Alliance staging) |
| **Shopify (MTB + SS direct)** | SB → customer | ✅ Yes (direct) |
| **Walmart Marketplace (SS, NFMD)** | SB → customer (Walmart Direct Connect) | ✅ Yes (some SKUs) |
| **TikTok Shop** | SB → customer + wholesale receipts | ✅ Yes (some SKUs) |
| **Retail (Nordstrom, etc.)** | SB → retailer or direct ship | ✅ Yes (occasional) |

**Implication:** Every transfer out of SB to Amazon reduces capacity to fulfill the others.

---

## How the current logic works (June 2026)

### Code path
- File: `scripts/build_report.py`
- Function: After `apply_shipbob_overrides()`, around line ~12200
- Constants: `SHOPIFY_PROTECTION_DAYS = 30`

### The math (per UPC)

```
SHIPBOB TOTAL          = raw ShipBob fulfillable count (across all US FCs)
                         = sum of Fulfillable across Reno + Fairburn + Bethlehem +
                           Moreno Valley + Buford + Philadelphia + Grapevine +
                           Dayton + US CA West Hub + Ontario 6

SHOPIFY RESERVE        = (Shopify daily velocity) × 30 days

SHIPBOB NET (AMZ)      = SHIPBOB TOTAL − SHOPIFY RESERVE
                         (this is what's "available" for Amazon emergency transfers)
```

### Where you see it
- **Amazon US tab** → three columns: SHIPBOB TOTAL · SHOPIFY RESERVE · SHIPBOB NET (AMZ)
- **THIS WEEK tab → TRANSFER section** → context shows: `SB net: X u (Y raw − Z Shopify reserve)`

### Example (Sonicsmooth -White - New, 811573031113)

| Field | Value |
|---|---:|
| Raw SB inventory | 805 |
| Shopify daily velocity | ~8/day |
| Shopify reserve (30d × 8/day) | 240 |
| **Net available for Amazon transfer** | **565** |

If a transfer recommendation says "send 565 units to Amazon," SB still has 240 left for Shopify orders.

---

## ⚠ What's MISSING from the reserve

The current reserve protects **only Shopify**. It does **not** protect:

| Channel | Why it should also be reserved | Current state |
|---|---|---|
| **Walmart Marketplace** | Some SKUs ship from SB direct to Walmart customers (SS Marketplace path). Velocity tracked in Valogix `WM-SS` location. | ❌ Not reserved |
| **TikTok Shop** | Wholesale receipts + some direct fulfillment from SB. Velocity tracked in SAP `TIKTOKSS` location. | ❌ Not reserved |
| **Retail accounts** | Nordstrom, occasional direct-ship-from-SB orders. | ❌ Not reserved |

**Why this matters:** For a SKU sold heavily on Walmart + TikTok, the current reserve underestimates how much SB needs to keep on hand. A "safe" transfer recommendation can still starve those channels.

---

## 🔍 Diagnostic checklist — is the reserve working?

Run this audit monthly OR after any complaint of stockout on a non-Amazon channel.

### Step 1 — Find recent SB→AMZ transfers
- Open `outputs/latest/weekly-report-*.xlsx` → THIS WEEK tab → 🚛 TRANSFER section
- Also check 4 weekly reports back (prior runs) for items recently transferred
- Note the **SKUs** + **transfer quantities** + **dates**

### Step 2 — For each transferred SKU, check the other channels
For each SKU in step 1, check whether Shopify / Walmart / TikTok hit stockout within **14 days after** the transfer:

| Channel | Where to check |
|---|---|
| Shopify MTB | Shopify Admin → Inventory dashboard OR ShipBob outbound logs |
| Shopify SS (DTC) | Same |
| Walmart Seller Center (SS, NFMD) | Walmart Seller Center → Inventory → Out of Stock report |
| TikTok | TikTok Shop dashboard → orders ledger |
| Floship | Floship export → check On Hand on the WMS |

### Step 3 — Flag the failures
Any SKU where:
- A non-Amazon channel went to 0 within 14 days of an SB→AMZ transfer
- AND the SKU was NOT phasing out

→ **This is reserve failure.** Document the SKU, the channel that stocked out, the days between transfer and stockout, and the transfer qty.

### Step 4 — Compute the right reserve
For each failed SKU:
- Total non-Amazon daily velocity = Shopify + Walmart + TikTok + Retail (per-day rates from Valogix / Sellerboard / WM Seller Center)
- Required reserve = `total_non_amz_vel × RESERVE_DAYS` (suggest 30 days)
- Compare against current `SHOPIFY RESERVE` field on Amazon US tab
- The gap = inventory the system over-allocated to Amazon

---

## Proposed fix (if reserve is too narrow)

Two options — easier to harder:

### Option A — Multi-channel reserve (recommended)

Change the constant + the velocity source:
```python
NON_AMZ_PROTECTION_DAYS = 30
# Build reserve from all non-Amazon SB-served channels:
#   Shopify (SBGA-MT, SBGA-SS, SBGA-SS-NFMD)
#   Walmart (WM-SS, WM-NFMD — only if SKU ships from SB to WM)
#   TikTok (TIKTOKSS, TIKTOKMT — only if SKU ships from SB to TikTok)
#   Retail (manual flag — most SKUs are not retail-served)

non_amz_vel = (shopify_vel + walmart_sb_vel + tiktok_sb_vel + retail_vel)
reserve = non_amz_vel × NON_AMZ_PROTECTION_DAYS
```

**Effort:** ~30 minutes
**Output:** Renames "SHOPIFY RESERVE" column to "MULTI-CHANNEL RESERVE" with a tooltip showing the breakdown.

### Option B — Per-channel reserve (more accurate, harder)

Different days per channel based on each channel's velocity volatility:
- Shopify: 30 days (steady)
- Walmart: 21 days (faster reorder cycles)
- TikTok: 14 days (high volatility, frequent restocks)
- Retail: 30 days (slow movers)

**Effort:** ~2 hours (need to plumb per-channel velocity into the calc)
**Output:** Better precision but more knobs to tune.

---

## Operator instinct check

Even with code logic, the human should look at:

1. **"Does this transfer drain SB to less than 30 days of total non-Amazon demand?"**
   - If yes → push back on the transfer size, OR ship in waves
2. **"When was the last time SB ran below 30 days of non-Amazon coverage?"**
   - If "never" → reserve is probably fine
   - If "happens every 6-8 weeks" → reserve is too narrow
3. **"Are there SKUs where Shopify is the bigger channel?"**
   - If yes → Shopify reserve might need to be 45-60 days, not 30

---

## Related docs

- `(C) Weekly Analysis SOP — Step by Step.md` — Where the TRANSFER section comes from in the report
- `(C) ABC Classification Reference.md` — Item priority drives reserve sizing decisions
- `(C) Forecast Accuracy & Buffer Sizing — Build Plan.md` — Sister doc on volatility-driven safety stock
- `10 System/(C) Master SupplyChainBrain — Architecture.md` — Where the SB→Amazon pipeline fits in the overall system

---

## Trigger phrases to revisit this

- *"Audit the SB reserve logic"* — run the diagnostic checklist
- *"Expand the SB reserve to multi-channel"* — implement Option A
- *"Add per-channel reserve sizing"* — implement Option B
