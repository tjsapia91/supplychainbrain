# 🚀 Weekly Analysis — 1-Page Cheat Sheet

> Print this. Stick it next to your monitor. After 2-3 weeks you won't need the full SOP anymore — just this.

---

## ✅ Download checklist (24 files)

| # | Source | Report | Drop into | Rename to |
|---|---|---|---|---|
| 1 | SoStocked (MTB) | Projected Forecast Model | `Downloads\` | (auto — `*-5118.xlsx`) |
| 2 | SoStocked (NFMD) | Projected Forecast Model | `Downloads\` | (auto — `*-5109.xlsx`) |
| 3 | SoStocked (SS) | Projected Forecast Model | `Downloads\` | (auto — `*-5119.xlsx`) |
| 4 | SoStocked (MTB) | Inventory → **"Export Inventory with Breakdown by Warehouses"** | `Downloads\` | (auto — `inventory-*-5118.csv`) |
| 5 | SoStocked (NFMD) | Inventory → **"Export Inventory with Breakdown by Warehouses"** | `Downloads\` | (auto — `inventory-*-5109.csv`) |
| 6 | SoStocked (SS) | Inventory → **"Export Inventory with Breakdown by Warehouses"** | `Downloads\` | (auto — `inventory-*-5119.csv`) |
| 7 | SoStocked (MTB) | Forecasted vs Actual (FvA) | `Downloads\` | (auto — `*-5118.xlsx`) |
| 8 | SoStocked (NFMD) | Forecasted vs Actual (FvA) | `Downloads\` | (auto — `*-5109.xlsx`) |
| 9 | SoStocked (SS) | Forecasted vs Actual (FvA) | `Downloads\` | (auto — `*-5119.xlsx`) |
| 10 | Amazon SC (MTB) | AWD Inventory Report | `reports\seller-central\MTB\` | (no rename) |
| 11 | Amazon SC (MTB) | FBA Inventory Report (full — 97 cols) | `reports\seller-central\MTB\` | (no rename) |
| 12 | Amazon SC (NFMD) | AWD Inventory Report | `reports\seller-central\NFMD\` | (no rename) |
| 13 | Amazon SC (NFMD) | FBA Inventory Report (full — 97 cols) | `reports\seller-central\NFMD\` | (no rename) |
| 14 | Amazon SC (SS) | AWD Inventory Report | `reports\seller-central\SS\` | (no rename) |
| 15 | Amazon SC (SS) | FBA Inventory Report (full — 97 cols) | `reports\seller-central\SS\` | (no rename) |
| 16 | ShipBob (MTB) | On Hand Summary | `reports\shipbob\MTB\` | (no rename) |
| 17 | ShipBob (NFMD) | On Hand Summary | `reports\shipbob\NFMD\` | (no rename) |
| 18 | ShipBob (SS) | On Hand Summary | `reports\shipbob\SS\` | (no rename) |
| 19 | ShipBob (LUMOS) | On Hand Summary | `reports\shipbob\LUMOS\` | (no rename) |
| 20 | Floship | Product Inventory | `reports\floship\` | (no rename) |
| 21 | Walmart (NFMD) | WFS → Inventory → Download All Items (xlsx) | `reports\walmart\NFMD\` | (no rename) |
| 22 | Walmart (SS) | WFS → Inventory → Download All Items (xlsx) | `reports\walmart\SS\` | (no rename) |
| 23 | Valogix | Item-Location-History-Forecast | `reports\valogix\` | (keep original) |
| 24 | (manual) | In-Transit Log (if updated) | `reports\in-transit\` | `IN_TRANSIT_LOG_YYYY-MM-DD.xlsx` |
| ⊕ | SAP (as needed) | ABC Classification export → `SAPABCCLASSIFICATION.xlsx` | `reports\item-master\item_master.xlsx` | only refresh when SAP changes |

---

## ⚡ Run order — 5 commands

Open Command Prompt → `cd C:\Users\[YourName]\MTB-SupplyChain` → run these in order:

```
python scripts\combine_forecast.py
python scripts\demand_planning.py
python scripts\build_report.py
python scripts\build_action_plan.py
python scripts\build_shipment_tracking.py
```

---

## 📂 What you should see in `outputs\2026-MM-DD\`

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

## 🆘 Quick fixes

| Error | Fix |
|---|---|
| "No such file" | A file is missing from `reports\` — re-download |
| "Permission denied" | Excel has the file open — close it |
| "ModuleNotFoundError" | `pip install pandas openpyxl` |
| Numbers wrong | Check all 15 inputs are in the right folders, re-run from Script 1 |

---

*Updated: May 4, 2026 · Full SOPs:* [[06 Processes & SOPs/(C) Weekly Analysis SOP — Step by Step]] *(operational)* · [[06 Processes & SOPs/(C) Weekly Inputs Sourcing SOP]] *(where each file comes from)*
