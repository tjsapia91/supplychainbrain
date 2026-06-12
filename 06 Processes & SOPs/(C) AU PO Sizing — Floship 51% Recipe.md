# (C) Australia PO Sizing — Floship 51% Recipe

> Use this when a supplier sends a draft PO for **Amazon AU** (`AMZ-MTAU` or `AMZ-NFAU`) and you need to confirm the qty before approving. Also useful for the quarterly AU-specific replenishment review.
>
> **Created:** 2026-06-11 · **Owner:** Tommy

---

## TL;DR — Just run the script

```
cd C:\Users\Tom Sapia\MTB-SupplyChain
python scripts\au_po_sizing.py
```

Output:
- Console table with all 17 FLOSHIP-planning-group SKUs + suggested 9-month PO size
- `outputs\YYYY-MM-DD\au-po-sizing-YYYY-MM-DD.xlsx` (formatted Excel)
- `outputs\latest\au-po-sizing-YYYY-MM-DD.xlsx` (mirror)

**Default parameters:** AU share 51% · Cover 9 months · Lead time 100 days · Planning group `FLOSHIP`

To override:
```
python scripts\au_po_sizing.py --cover 6 --au-share 0.55 --lead-days 120
```

---

## The recipe (5 steps + reorder trigger)

```
1. Filter Valogix → Planning Group = FLOSHIP
2. Sum last 12 closed months of Floship volume per SKU
3. ÷ 12                                   = monthly Floship avg
4. × 0.51 (AU share)                      = AU monthly demand
5. × 9 (cover months)                     = target PO size

Reorder trigger:
   AU monthly × (100 / 30.4) = AU monthly × 3.29
   → When Amazon AU on-hand drops to this level, place the NEXT PO
```

---

## Worked example — Sonicsmooth Pro+ Lavender

UPC `811573031342`, last 12 closed months at FLOSHIP planning group:

| Month | Units |
|---|---:|
| Jun-25 | 511 |
| Jul-25 | 266 |
| Aug-25 | 484 |
| Sep-25 | 411 |
| Oct-25 | 354 |
| Nov-25 | 1,115 |
| Dec-25 | 2,338 |
| Jan-26 | 1,401 |
| Feb-26 | 1,302 |
| Mar-26 | 2,133 |
| Apr-26 | 1,051 |
| May-26 | 1,293 |
| **Sum** | **12,659** |

```
Step 2: 12mo total       = 12,659
Step 3: monthly_avg      = 12,659 / 12         = 1,054.9
Step 4: au_monthly       = 1,054.9 × 0.51      = 538.0
Step 5: target_po (9mo)  = 538.0 × 9           = 4,842
        reorder_trigger  = 538.0 × 3.29        = 1,770
```

**Action:** Place 4,842 units. When AU on-hand drops to 1,770, place next PO (will arrive in 100 days, just as you run out).

---

## Why the parameters are what they are

### AU share = 51%
Of all Floship shipments (international Shopify), 51% land in Australia. Tommy's number, derived from historical destination breakdown. Re-validate annually or if you change Floship configuration.

### Lead time = 100 days
Supplier door-to-door for AMZ-MTAU. Ocean freight + customs + Amazon receiving. Confirmed Tommy 2026-06-11.

### Cover = 9 months
After PO arrives: covers 3.3 months until next PO triggers + 5.7 months safety. Doubles as the buffer for demand spikes.

### Planning Group filter = FLOSHIP
Excludes `No Replen` (phase-out / dead) and `Non Stock items` (limited-edition / hadn't launched). These have either no signal or aren't valid for replenishment planning.

---

## What this recipe does NOT cover

### 1. NFMD AU POs (warehouse `AMZ-NFAU`)
NFMD doesn't ship via Floship — no signal in this file. For NFMD AU sizing:
1. Log into Amazon Seller Central → switch marketplace to `amazon.com.au`
2. Reports → Business → **Detail Page Sales and Traffic by Child Item** (12-month range)
3. For each NFMD ASIN: sum "Units Ordered" ÷ 12 = AU monthly demand directly
4. × 9 = target PO (no 51% step — the data is already AU-only)

### 2. Volatility buffer for spiky SKUs
The recipe uses a flat 12-month average. For SKUs with high volatility (peak month / low month > 5×), add an extra 1-2 months of cover:
- Pro+ Lavender ranges 266 → 2,338 (8.8×) → consider 10-11 month cover
- Pro+ Pink ranges 0 → 251 (∞×) → consider 11-12 month cover

The script prints volatility % so spiky SKUs are visible.

### 3. Wholesale-order distortion
A single distributor refill can inflate a month by 2-5×. Spot-check the monthly history before sizing the top movers. If Dec-25 = 2,338 was actually one distributor order of 2,000 + organic 338, the underlying steady-state is much lower.

---

## When to re-run

| Trigger | Action |
|---|---|
| **Supplier sends new draft AU PO** | Run script, compare draft to suggested target |
| **Quarterly AU review** | Run script, document target vs actual deltas |
| **Floship volume shift** | Re-validate the 51% AU share; rerun |
| **New SKU launches in AU** | After 2-3 months of Floship history, run for sizing baseline |

---

## Last run results (2026-06-11)

12 SKUs from the AU draft POs — full table in `outputs\latest\au-po-sizing-2026-06-12.xlsx`.

| UPC | Product | 9mo target PO |
|---|---|---:|
| 811573031342 | Sonicsmooth Pro+ Lavender | **4,842** |
| 811573031335 | Sonicsmooth Clear Replacement Kit (8 Blades) | **2,511** |
| 811573031366 | Sonicsmooth Pro+ White | **963** |
| 811573031359 | Sonicsmooth Pro+ Pink | 315 |
| 811573031373 | MICROSMOOTH Clear Replacement Tips | 156 |
| 811573031090 | Sonicsmooth Lavender (New) | 145 |
| 811573031106 | Sonicsmooth Green (New) | 37 |
| 811573030468 | Soniclear White Marble | 35 |
| 811573031113 | Sonicsmooth White (New) | 29 |
| 859886007708 | Soniclear Brush Face — Sensitive | 5 |
| 859886007685 | Soniclear Brush Face — White | 0 (no Floship demand) |
| 859886007692 | Soniclear Brush Face — Plum | **no data** (not in FLOSHIP file) |

**Top 3 (Pro+ Lav · Replacement Kit · Pro+ White) = 91% of total AU PO volume.** Get those three right and you've handled AU.

---

## Future automation (deferred)

The current script is standalone. Could wire into the weekly pipeline so AU target column shows automatically on the Amazon AU tab — but only do that after using the standalone script for a few cycles to validate the recipe is stable.

Open follow-ups:
- [ ] Wire NFMD AU sales (from Amazon SC AU) into the pipeline so all 20 AU POs get auto-sized
- [ ] Add per-SKU `AU_SHARE_OVERRIDE` for SKUs that don't fit the 51% rule
- [ ] Volatility-adjusted cover (e.g. cover = 9 if CV<30, 11 if CV>30)

---

## Related docs

- [[06 Processes & SOPs/(C) Weekly Analysis SOP — Step by Step]]
- [[06 Processes & SOPs/(C) Weekly Inputs Sourcing SOP]]
- [[06 Processes & SOPs/(C) ABC Classification Reference]]

---

*Updated 2026-06-11 — created as standalone recipe + helper script*
