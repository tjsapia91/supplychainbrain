# (C) Walmart Seller Center — Reports Pull List

> The Walmart Item Report we pull weekly from Walmart Fulfillment Services (WFS). Used to:
> 1. **Validate Valogix's WM-SS data** (Spa Sciences Walmart inventory)
> 2. **NEW visibility for NasalFresh MD on Walmart** — not in Valogix today
>
> **Last updated:** May 4, 2026

---

## 📋 Summary

**1 report × 2 brand logins = 2 files per week.**

| Report | Path in Walmart Seller Center | Format | What it gives us |
|---|---|---|---|
| **WFS Inventory — All Items** | Left menu → **WFS** → **Inventory** → top-right **Download** → **All items** → **Download** | **.xlsx** (Excel) | Current WFS on-hand quantity per Walmart Item ID + GTIN |

| Walmart brand login | Folder | In Valogix? |
|---|---|---|
| **NFMD** | `reports\walmart\NFMD\` | ❌ NEW — not in Valogix today |
| **SS** | `reports\walmart\SS\` | ✅ Validates Valogix WM-SS |

---

## 🔄 The routine — repeat 2 times (once per brand login)

### ⚠️ Important: Walmart is brand-specific
- NFMD and SS each have their own Walmart Seller Center login
- You must sign in to each brand separately
- MTB does **not** sell on Walmart Marketplace

### Per brand session:

1. **Log into Walmart Seller Center** (use the brand-specific credentials)
2. Left menu → **WFS** (Walmart Fulfillment Services)
3. Click → **Inventory**
4. Right side → **Download** button
5. Choose: **All items**
6. Click **Download** — **.xlsx (Excel)** file downloads
7. Drop into the matching brand folder:

| Brand login | Folder |
|---|---|
| NFMD | `reports\walmart\NFMD\` |
| SS | `reports\walmart\SS\` |

8. Sign out → sign into next brand → repeat

No renaming required — the script auto-detects.

---

## 🎯 Why we pull this

WFS is Walmart's Fulfillment Services (their version of Amazon FBA). Items here are stored and shipped by Walmart for orders placed on Walmart Marketplace.

Direct WFS pull tells us:
- ✅ Real-time WFS stock per item
- ✅ NFMD's Walmart presence (currently invisible in our pipeline)
- ✅ Sanity-check against Valogix's WM-SS data (Spa Sciences)

---

## 🔍 Validation — comparing Walmart direct vs. Valogix

| Walmart brand | Valogix equivalent | Action |
|---|---|---|
| **SS** | `WM-SS` location in Valogix | Cross-check on-hand per SKU. If discrepancy > 5% AND > 10 units → flag |
| **NFMD** | _not in Valogix_ | Add as a new marketplace on the Multi-Channel dashboard |

A validation script will produce a side-by-side comparison Excel showing where the two sources disagree.

---

## ✅ End-state — what `reports\walmart\` should contain

After both brand sessions:

```
reports\walmart\
├── NFMD\
│   └── (WFS Inventory .xlsx — any name from Walmart)
└── SS\
    └── (WFS Inventory .xlsx)
```

File names from Walmart don't matter. Brand is determined by the subfolder. Files are **Excel (.xlsx)** not CSV.

---

## Related docs

- [[06 Processes & SOPs/(C) Weekly Inputs Sourcing SOP]] — full sourcing reference
- [[06 Processes & SOPs/(C) ShipBob — Reports Pull List]] — ShipBob pull pattern
- [[06 Processes & SOPs/(C) Amazon Seller Central — Reports Pull List]] — Amazon reports

---

*Created: May 4, 2026*
*Owner: Supply Chain team*
