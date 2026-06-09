# 🚀 Weekly Analysis — 1-Page Cheat Sheet

> Print this. Stick it next to your monitor. After 2-3 weeks you won't need the full SOP — just this.
>
> *Last updated: 2026-06-08 — reflects 5-section THIS WEEK tab, In Transit tab, PO Priority tab, days-first ranking, auto-classified Downloads workflow.*

---

## ✅ Download checklist (~37 weekly files)

**Drop everything into `C:\Users\Tom Sapia\Downloads\`. No folder navigation needed.**
`sort_downloads.py` (auto-runs first) classifies every recognized file and routes it to the right `reports/` subfolder.

| Source | Files | Cadence | Notes |
|---|---:|---|---|
| **SoStocked** (Forecast + Inventory + FvA × 3 brands) | 9 | Weekly | Inventory must be "Breakdown by Warehouses" (~50 cols) — not "Current View" |
| **Amazon Seller Central US** (FBA + AWD × 3 brands) | 6 | Weekly | FBA = full 97-col report from Reports → Fulfillment |
| **Amazon Seller Central CA** (FBA × 3 brands) | 3 | Weekly | CA has no AWD program for MTB; FBA only |
| **ShipBob** (Inventory Status → Export All Data) | 4 | Weekly | NEW format only — MTB, NFMD, SS, LUMOS |
| **Walmart** (Marketplace + Inventory Health × 2 brands) | 4 | Weekly | NFMD + SS only |
| **Floship** (Product Inventory export) | 1 | Weekly | |
| **Valogix** (Forecast + Exceptions) | 2 | Weekly | Item-Location-History-Forecast + History Exception Report |
| **SAP Open POs** (full export) | 1 | Weekly | |
| **Sellerboard CA Dashboard** (× 3 brands) | 3 | Weekly | Set marketplace filter = `amazon.ca` · last 90 days |
| **Sellerboard Sales by Product/Month** (× 3 brands) | 3 | **Monthly** | Max date range, marketplace ignored |
| **In-Transit Log** (`IN TRANSIT LOG*.xlsx`) | 1 | Weekly | From SharePoint — get latest before running |
| **Total weekly** | **~37** | | Plus 3 monthly Sellerboards |

**Optional / on-change-only:**
- SAP `SAPABCCLASSIFICATION.xlsx` → only when ABC codes change
- `amazon-sku-mapping.xlsx` → only when new Amazon SKUs launch

---

## ⚡ Run order — 2 commands

Open Command Prompt → `cd C:\Users\Tom Sapia\MTB-SupplyChain` → run:

```
python scripts\demand_planning.py
python scripts\build_report.py
```

`build_report.py` auto-chains the rest: `sort_downloads.py` (pre-flight) → demand-plan ingestion → 19-tab weekly report → velocity-watch → deep-plan workflow → order-list → in-transit + PO priority tabs.

**Run time:** 2-4 minutes total once Downloads is populated.

---

## 📂 What you should see in `outputs\YYYY-MM-DD\`

- ✅ `weekly-report-YYYY-MM-DD.xlsx` ⭐ **THE BIG ONE** (19 tabs)
- ✅ `demand-plan-YYYY-MM-DD.json` + `.md`
- ✅ `order-list-YYYY-MM-DD.xlsx`
- ✅ `velocity-watch-YYYY-MM-DD.xlsx`

All also copied to `outputs/latest/`.

---

## 🎯 The ONE tab to open: ✅ THIS WEEK

5 sections, top to bottom:

| Section | Action | When |
|---|---|---|
| 🛒 **ORDER** | Place a new supplier PO | This week |
| ⏱ **EXPEDITE** | Call supplier — PO is arriving AFTER our stockout | This week |
| 🚛 **TRANSFER** | File an SB→Amazon send-in | This week |
| ⚠ **SUPPLY RISK** | Confirm PO ETA — SAP same-day error means we don't know real date | This week |
| ⏳ **WATCH** | PO is in flight; verify next week | Next week |

---

## 🎯 Decision rules — days-first (June 5 update)

The PO Priority tab and SUPPLY RISK section both rank by **days to stockout**, not status string:

| Rank | Days to Stockout | What to do |
|---|---|---|
| 🔴 **OVERDUE** | < 0 | Already stocked out — manufacture immediately, evaluate air freight |
| 🔴 **CRITICAL** | ≤ 30 days | Place PO today/this week |
| 🟠 **HIGH** | 31-90 days | Place PO this week — fits in next supplier cycle |
| 🟡 **MEDIUM** | 91-180 days | Schedule for fall production |
| 🟢 **HEALTHY** | > 180 days | Monitor only |
| ⚪ **NO DATA** | (no calculable date) | Verify before ordering — data uncertainty |

---

## 🏭 PO Priority tab — what to send the supplier

After scanning ✅ THIS WEEK, open **🏭 PO Priority**. It's the vendor-by-vendor manufacturing priority list:
- Groups POs by vendor (Ningbo Dream Big · Ningbo Ocean · Ningbo Rivers · etc.)
- Each PO ranked by days-to-stockout for the item it covers
- "Still at supplier" qty = SAP open qty MINUS what's already in transit (per In-Transit Log)

Copy a vendor's section into an email → send to the supplier → "manufacture in this order."

---

## 📦 In Transit tab — POs already shipped

33 active line items typical: 21 Amazon-bound + 12 SB-bound. Shows real ETAs from the In-Transit Log (overrides SAP's same-day errors). Cross-reference here before assuming a PO is overdue.

---

## 🇨🇦 Amazon CA-specific notes

- Amazon CA has **FBA only** (no AWD program for MTB) — just 1 file per brand
- Sellerboard Monthly **combines US + CA** — DO NOT use for CA velocity
- Use Sellerboard **Dashboard Products** with `amazon.ca` filter for CA velocity
- SAP Open POs go to US Amazon ONLY → CA `PO ARRIVES ON` column shows `—`

---

## 🆘 Quick fixes

| Error | Fix |
|---|---|
| `PermissionError: weekly-report-*.xlsx` | Excel has the file open — close it |
| `❓ UNSORTED` in sort log | New file pattern — move manually OR add rule to `sort_downloads.py` |
| Numbers don't match Seller Central dashboard | CSV is cached — re-download FBA Inventory Report |
| `⚠️ Sellerboard Monthly is N days old` | Pull the 3 monthly Sellerboards (monthly cadence) |
| CA velocity inflated 30-50× | CA Dashboard pulled without `amazon.ca` filter |
| `→ ShipBob (LEGACY)` log line | Switch to `Inventory Status → Export All Data` (new format) |
| In-Transit Log shows stale dates | Get the latest from SharePoint and re-drop in Downloads |
| 🏭 PO Priority shows NO DATA on items in ORDER section | `supplier_rows` lookup gap — verify build_report ran clean to end |

---

## Master / detail docs

- Full step-by-step (this doc's expanded twin): [[06 Processes & SOPs/(C) Weekly Analysis SOP — Step by Step]]
- Where to source each file: [[06 Processes & SOPs/(C) Weekly Inputs Sourcing SOP]]
- Tab-by-tab reference (every column explained): `Weekly Report Explanation/` folder
- ShipBob channel reserve logic: [[06 Processes & SOPs/(C) ShipBob Inventory Protection — Channel Reserve Logic]]

---

*Updated: 2026-06-08 · 1-page reference · See Step-by-Step SOP for first-time walkthrough*
