# (C) Amazon Seller Central — Reports Pull List

> The exact 2 reports we pull from Seller Central each week. **Repeat for all 3 brands** (MTB / NFMD / SS) → 6 files total.
>
> **Last updated:** May 4, 2026

---

## 📋 Summary — what you're pulling

| # | Report | Path in Seller Central | What it gives us |
|---|---|---|---|
| 1 | **AWD Inventory Report** | Inventory → AWD → Replenishment / Auto-Replenishment Dashboard | AWD inbound + outbound to FBA + auto-replenishment metrics |
| 2 | **FBA Inventory Report** (full, 97 columns) | Reports → Fulfillment → **FBA Inventory** | Aging buckets + inbound-shipped/received + days-of-supply — single comprehensive file |

**Per brand × 3 brands = 6 files total per week.**

⚠️ **Don't pull "Manage FBA Inventory" from the Inventory tab** — that's redundant. The FBA Inventory Report (Reports → Fulfillment → FBA Inventory) is the comprehensive version with all 97 columns.

ℹ️ **Inbound Shipment Items** report is OPTIONAL (it would populate the Shipment Tracking report's FBA tab with per-shipment detail). It's not in the standard weekly cycle yet — Tommy is still hunting for the right path in Seller Central.

**No renaming required.** Drop original Amazon CSVs into the right brand folder:
```
C:\Users\[YourName]\MTB-SupplyChain\reports\seller-central\MTB\    ← MTB downloads
C:\Users\[YourName]\MTB-SupplyChain\reports\seller-central\NFMD\   ← NFMD downloads
C:\Users\[YourName]\MTB-SupplyChain\reports\seller-central\SS\     ← SS downloads
```

The script auto-detects each report by its column headers — file names don't matter.

---

## 🔄 The routine — repeat 3 times (once per brand)

You'll log in to **MTB**, pull both reports, log out. Then **NFMD**, pull both, log out. Then **SS**, pull both, log out.

**Tip:** Open 3 Chrome incognito windows (one per brand) so you can have all 3 logged in at once.

Per login session, pull the 2 reports below. **All as CSV. No renaming required** — drop into the right brand subfolder and the script detects each by columns.

### ① AWD Inventory Report
1. Top nav → **Inventory** → **AWD** → **Replenishment** / **Auto-Replenishment Dashboard**
2. Top-right → **Download** → **CSV**
3. Drop file into `reports\seller-central\[BRAND]\`

Filename will look like: `AWD-inventory-report-MM_DD_YY-HH-MM-SS.csv`

### ② FBA Inventory Report (the comprehensive 97-column version)
1. Top nav → **Reports** → **Fulfillment** → **FBA Inventory**
2. ⚠️ Make sure you get the **full version** (97 columns including `inbound-shipped`, `inbound-received`, AND aging buckets). Don't pick the abbreviated version.
3. Click **Request Report** → wait ~1 min → **Download** → **CSV**
4. Drop file into `reports\seller-central\[BRAND]\`

Filename will look like: `[6-digit number]020577.csv` (e.g., `281078020577.csv`)

This single report covers everything we need from FBA — aging, inbound, days-of-supply, recommendations.

→ Sign out. Sign into the next brand. Repeat.

---

## 🔍 How to verify the FBA file is the right one

After download, open the CSV and check that it has:
- ✅ ~97 columns (not 30 or 22)
- ✅ Column named `inbound-shipped` (around column 56)
- ✅ Column named `inbound-received` (around column 57)
- ✅ Column named `inv-age-0-to-90-days` (around column 9)
- ✅ Column named `days-of-supply` (around column 39)

If yes → that's the right report. If only ~30 columns → look for an option to download the extended/full version.

---

## ✅ End-state — what `reports\seller-central\` should contain

After all 3 brand sessions you should have **6 files** (2 per brand) split across 3 brand subfolders:

```
reports\seller-central\
├── MTB\
│   ├── AWD-inventory-report-*.csv         ← AWD
│   └── XXXXXXXXX020577.csv                ← FBA Inventory (97 cols)
├── NFMD\
│   ├── AWD-inventory-report-*.csv
│   └── XXXXXXXXX020577.csv
└── SS\
    ├── AWD-inventory-report-*.csv
    └── XXXXXXXXX020577.csv
```

The script auto-classifies by column structure — file names don't matter as long as they contain the right data.

The script doesn't care what the files are named — it identifies each report by checking its columns.

---

## 🎯 Why each report matters

| Report | What it tells us | Used for |
|---|---|---|
| AWD Inventory Report | Units in transit supplier → AWD + AWD → FBA outbound + auto-replenishment metrics | DOS calculation, shipment tracking |
| FBA Inventory Report (full) | FBA stock + inbound-shipped/received/working + aging buckets + days-of-supply + recommendations | DOS calc, "is this really critical or is replenishment in flight?" check, future aging analysis |

---

## ⚠️ Common gotchas

| Issue | Fix |
|---|---|
| AWD ledger only shows last few days | Scroll to date filter, set last 7-14 days |
| FBA download stuck at "preparing" | Wait 1-2 min, refresh page, try again |
| Inbound Shipment Items not in nav | Use the legacy URL: `https://sellercentral.amazon.com/gp/ssof/reports/search.html` |
| File downloads with weird name | Just rename it after — doesn't matter what Amazon called it |
| Wrong brand's data | You forgot to switch Seller Central accounts. Sign out + sign back in. |

---

## Related docs

- [[06 Processes & SOPs/(C) Weekly Inputs Sourcing SOP]] — full sourcing reference (all data sources, not just Seller Central)
- [[06 Processes & SOPs/(C) Weekly Analysis SOP — Step by Step]] — running the scripts after you have inputs
- [[06 Processes & SOPs/(C) Weekly Analysis Cheat Sheet — 1 Page]] — the print-and-stick version

---

*Created: April 30, 2026*
*Owner: Supply Chain team*
