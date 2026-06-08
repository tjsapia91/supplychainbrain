# (C) ShipBob — Reports Pull List

> The 3 ShipBob On-Hand Summary reports we pull weekly. Used to:
> 1. **Validate Valogix's ShipBob inventory data** (SBGA-MT, SBGA-SS locations) — independent source of truth
> 2. **Gauge Shopify fulfillment readiness** — Shopify orders ship from ShipBob, so ShipBob stock directly drives Shopify availability
> 3. **Sanity-check Amazon emergency send-in plans** — what's actually pullable from ShipBob to send to FBA
>
> **Last updated:** May 4, 2026

---

## 📋 Summary

**1 report × 4 brand logins = 4 files per week.**

| Report | Path in ShipBob | What it gives us |
|---|---|---|
| **On Hand Summary** | Inventory → Export → **On Hand Summary** | Current on-hand units per SKU at the ShipBob warehouse |

| ShipBob brand login | Maps to product line / Valogix location |
|---|---|
| **MTB** | Michael Todd Beauty — Shopify MTB (`SBGA-MT` in Valogix) |
| **NFMD** | NasalFresh MD — Shopify NFMD (part of `SBGA-SS` in Valogix) |
| **SS** | Spa Sciences — Shopify SS (part of `SBGA-SS` in Valogix) |
| **LUMOS** | Lumos product line — separate ShipBob account |

---

## 🔄 The routine — repeat 4 times (once per brand login)

### ⚠️ Important: ShipBob is brand-specific
- Each brand (MTB, NFMD, SS, LUMOS) has its own ShipBob login
- You must sign in to each brand separately
- The download link gets emailed — you can only download it while still logged in to the correct brand

### Per brand session:

1. **Log into ShipBob** at https://shipbob.com (use the brand-specific credentials)
2. Top nav → **Inventory**
3. Click → **Export** → **On Hand Summary**
4. ShipBob emails a download link to the email on file (usually within ~5 min)
5. Open the email **WHILE STILL LOGGED IN to that brand** — click the link → CSV downloads
6. Drop into the matching brand folder:

| Brand login | Folder |
|---|---|
| MTB | `reports\shipbob\MTB\` |
| NFMD | `reports\shipbob\NFMD\` |
| SS | `reports\shipbob\SS\` |
| LUMOS | `reports\shipbob\LUMOS\` |

7. Sign out → sign into next brand → repeat

### ⚠️ Don't skip the sign-in/sign-out
If you click the email link while logged into the wrong brand, ShipBob will give you the wrong brand's data. Check the brand name in the top-right of the ShipBob UI before downloading.

---

## 🎯 Why we pull this

ShipBob is the warehouse that fulfills:
- **Shopify orders** (MTB website, Spa Sciences website, NFMD website) — direct fulfillment
- **Amazon emergency send-ins** — when FBA stock runs low and we have stock at ShipBob, we ship it to FBA fast

So ShipBob inventory directly drives:
- ✅ Shopify availability per SKU
- ✅ Whether we can do emergency FBA send-ins
- ✅ Order fulfillment SLA on Shopify

---

## 🔍 Validation — comparing ShipBob direct vs. Valogix

Valogix CSV has ShipBob inventory at locations `SBGA-MT` (MTB Shopify warehouse) and `SBGA-SS` (Spa Sciences DTC warehouse + NFMD).

We compare:

| Valogix location | ShipBob brand login |
|---|---|
| `SBGA-MT` | MTB ShipBob account |
| `SBGA-SS` | SS / NFMD ShipBob account |

**Action when discrepancies appear:**
- Tolerance: discrepancy < 5% AND < 10 units → ignore (rounding / sync timing)
- Discrepancy ≥ 5% or ≥ 10 units → investigate (Valogix is stale, ShipBob counted wrong, etc.)

A validation script (`scripts/validate_shipbob_vs_valogix.py`) will run after both data sources are loaded and produce a side-by-side comparison Excel showing only SKUs where the two sources disagree by more than tolerance.

---

## ✅ End-state — what `reports\shipbob\` should contain

After all 4 brand logins:

```
reports\shipbob\
├── MTB\
│   └── (On Hand Summary CSV — any name from ShipBob)
├── NFMD\
│   └── (On Hand Summary CSV)
├── SS\
│   └── (On Hand Summary CSV)
└── LUMOS\
    └── (On Hand Summary CSV)
```

Just like Seller Central — file names from ShipBob don't matter. Brand is determined by the subfolder.

---

## Related docs

- [[06 Processes & SOPs/(C) Weekly Inputs Sourcing SOP]] — full sourcing reference
- [[06 Processes & SOPs/(C) Weekly Analysis SOP — Step by Step]] — running the scripts
- [[06 Processes & SOPs/(C) Amazon Seller Central — Reports Pull List]] — Amazon reports

---

*Created: May 4, 2026*
*Owner: Supply Chain team*
