# 🚀 Weekly Analysis — 1-Page Cheat Sheet

> Print this. Stick it next to your monitor. After 2-3 weeks you won't need the full SOP anymore — just this.
>
> *Last updated: 2026-05-21 — reflects Sellerboard CA Dashboard, Amazon CA FBA, NEW ShipBob format, US/CA seller-central split.*

---

## ✅ Download checklist (34 weekly files)

| # | Source | Report | Drop into | Rename to |
|---|---|---|---|---|
| **SoStocked — 9 files (Forecast + Inventory + FvA × 3 brands)** ||||
| 1-3 | SoStocked (MTB/NFMD/SS) | **Projected Forecast Model** | `Downloads\` | auto |
| 4-6 | SoStocked (MTB/NFMD/SS) | **Inventory → "Breakdown by Warehouses"** | `Downloads\` | auto |
| 7-9 | SoStocked (MTB/NFMD/SS) | **Forecasted vs Actual (FvA)** — current month | `reports\sostocked\[BRAND]\fva-history\` | `FvA_[BRAND]_YYYY-MM.xlsx` |
| **Amazon Seller Central — 9 files (US: 2 × 3 brands · CA: 1 × 3 brands)** ||||
| 10-12 | Amazon SC US (MTB/NFMD/SS) | **AWD Inventory Report** | `reports\seller-central\US\[BRAND]\` | (no rename) |
| 13-15 | Amazon SC US (MTB/NFMD/SS) | **FBA Inventory Report (97 cols)** | `reports\seller-central\US\[BRAND]\` | (no rename) |
| 16-18 | Amazon SC CA (MTB/NFMD/SS) | **FBA Inventory Report only — no AWD CA for MTB** | `reports\seller-central\CA\[BRAND]\` | (no rename) |
| **ShipBob — 4 files (NEW format)** ||||
| 19 | ShipBob (MTB) | `Inventory → Inventory Status → Export → Export All Data` | `reports\shipbob\MTB\` | (no rename) |
| 20 | ShipBob (NFMD) | same path | `reports\shipbob\NFMD\` | (no rename) |
| 21 | ShipBob (SS) | same path | `reports\shipbob\SS\` | (no rename) |
| 22 | ShipBob (LUMOS) | same path | `reports\shipbob\LUMOS\` | (no rename) |
| **Walmart — 2 files** ||||
| 23 | Walmart (NFMD) | WFS → Inventory → Download All Items (xlsx) | `reports\walmart\NFMD\` | (no rename) |
| 24 | Walmart (SS) | WFS → Inventory → Download All Items (xlsx) | `reports\walmart\SS\` | (no rename) |
| **Floship — 1 file** ||||
| 25 | Floship | Inventory → Product Inventory → Export | `reports\floship\` | (no rename) |
| **Valogix — 1 file** ||||
| 26 | Valogix | Item-Location-History-Forecast (CSV) | `reports\valogix\` | (keep original name) |
| **Sellerboard — 6 files (Monthly + CA Dashboard)** ||||
| 27 | Sellerboard (MTB) | **Sales by Product/Month** — max date range, marketplace ignored | `reports\sellerboard\MTB\` | (no rename) |
| 28 | Sellerboard (NFMD) | Sales by Product/Month | `reports\sellerboard\NFMD\` | (no rename) |
| 29 | Sellerboard (SS) | Sales by Product/Month | `reports\sellerboard\SS\` | (no rename) |
| 30 | Sellerboard (MTB) | 🇨🇦 **Dashboard Products** — set marketplace = `amazon.ca`, last 90 days | `reports\sellerboard\MTB\canada\` | (no rename) |
| 31 | Sellerboard (NFMD) | 🇨🇦 Dashboard Products (amazon.ca) | `reports\sellerboard\NFMD\canada\` | (no rename) |
| 32 | Sellerboard (SS) | 🇨🇦 Dashboard Products (amazon.ca) | `reports\sellerboard\SS\canada\` | (no rename) |
| **Valogix Exceptions — 1 file** ||||
| 33 | Valogix | History Exception Report (CSV) | `reports\valogix-exceptions\` | (no rename) |
| **SAP — 1 file** ||||
| 34 | SAP | Open Purchase Order Report (full export) | `reports\sap-open-pos\` | (no rename) |
| **Optional / when updated** |||||
| ⊕ | (manual) | In-Transit Log | `reports\in-transit\` | `IN_TRANSIT_LOG_YYYY-MM-DD.xlsx` |
| ⊕ | SAP (as needed) | ABC Classification → `SAPABCCLASSIFICATION.xlsx` | `reports\item-master\item_master.xlsx` | only when SAP classifications change |
| ⊕ | Amazon SKU Mapping | Internal MTB-maintained file | `reports\item-master\amazon-sku-mapping.xlsx` | only when new Amazon SKUs launch |

**One-time backfill: 15 FvA files** (5 months × 3 brands) → drop in `fva-history\` folders. Then just current month each week.

---

## ⚡ Run order — 5 commands

Open Command Prompt → `cd C:\Users\Tom Sapia\MTB-SupplyChain` → run these in order:

```
python scripts\combine_forecast.py
python scripts\demand_planning.py
python scripts\build_report.py
python scripts\build_action_plan.py
python scripts\build_shipment_tracking.py
```

---

## 📂 What you should see in `outputs\YYYY-MM-DD\`

- ✅ `demand-plan-YYYY-MM-DD.xlsx`
- ✅ `weekly-report-YYYY-MM-DD.xlsx` ⭐ THE BIG ONE
- ✅ `action-plan-YYYY-MM-DD.xlsx`
- ✅ `shipment-tracking-YYYY-MM-DD.xlsx`

---

## 🎯 Decision rules

| Status | What to do |
|---|---|
| 🔴 STOCKOUT / TRUE STOCKOUT | **Today.** ShipBob send-in if available, urgent PO if not. |
| 🔴 CRITICAL / BELOW ROP | **Today/tomorrow.** Place PO. |
| 🟠 HIGH / LOW | **This week.** Schedule the PO. |
| 🟡 FBA REPLENISHMENT | **This week.** Routine ShipBob → FBA send-in. |
| 🟢 HEALTHY | Skip. |
| ⚫ E or Z classification | **No new POs** — being phased out / obsolete. |

---

## 🇨🇦 Amazon CA-specific notes

- Amazon CA has **FBA only** (no AWD program for MTB) → just 1 file per brand from CA dashboard
- Sellerboard Monthly report **combines US + CA** — DON'T use for CA velocity
- Use Sellerboard **Dashboard Products** with `amazon.ca` marketplace filter for CA velocity + forecast
- SAP Open POs go to US Amazon ONLY → CA tab's PO ARRIVES ON column shows `—` until CA-specific PO source is added

---

## 🆘 Quick fixes

| Error | Fix |
|---|---|
| "No such file" | A file is missing from `reports\` — re-download |
| "Permission denied" | Excel has the file open — close it |
| "ModuleNotFoundError" | `pip install pandas openpyxl` |
| Numbers wrong | Check all 34 inputs are in the right folders, re-run from Script 1 |
| `→ ShipBob (LEGACY)` log line | Still pulling On Hand Summary — switch to `Inventory Status → Export All Data` |
| CA velocity inflated | Sellerboard Monthly applied to CA rows — verify pipeline F1 fix is active |

---

*Updated: 2026-05-21 · Full SOP:* [[06 Processes & SOPs/(C) Weekly Inputs Sourcing SOP]] *(master doc — inputs · architecture · steps)*
