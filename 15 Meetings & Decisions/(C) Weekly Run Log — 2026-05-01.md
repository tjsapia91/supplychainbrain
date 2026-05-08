# (C) Weekly Run Log — 2026-05-01

> Live runbook for the May 1 weekly cycle. Check off each box as we go.
>
> **Run date:** 2026-05-01 (for Monday May 4 cycle)

---

## 📥 Reports to pull

### SoStocked (9 files = 3 reports × 3 brands) — go to: app.sostocked.com ✅ COMPLETE

**Report A — Projected Forecast Model** (Forecast section)
- [x] MTB → `projected-forecast-model-{uuid}-5118.xlsx`
- [x] NFMD → `projected-forecast-model-{uuid}-5109.xlsx`
- [x] SS → `projected-forecast-model-{uuid}-5119.xlsx`

**Report B — Inventory** (Inventory page → cloud-download icon → **"Export Inventory with Breakdown by Warehouses"** → Download)
- [x] MTB → `inventory-{uuid}-5118.csv` ⚠️ verify ~49 columns incl. Adj. Velocity + FBA Available Stock
- [x] NFMD → `inventory-{uuid}-5109.csv`
- [x] SS → `inventory-{uuid}-5119.csv`

⚠️ **Lesson learned May 4:** "Export Current View" gives only ~12 columns — INSUFFICIENT for the demand planning script. Always pick "Export Inventory with Breakdown by Warehouses" for the comprehensive 49-column export.

**Report C — Forecasted vs Actual** (Reports section → FvA / Forecast Accuracy)
- [x] MTB → `{uuid}-5118.xlsx`
- [x] NFMD → `{uuid}-5109.xlsx`
- [x] SS → `{uuid}-5119.xlsx`

→ All 9 files land in: `C:\Users\Tom Sapia\Downloads\`
→ Then `combine_forecast.py` auto-detects, renames, combines, and archives them.

---

### Amazon Seller Central (6 files — 2 reports × 3 brands) ✅ COMPLETE

Drop CSVs into brand subfolders. **No renaming required** — the script auto-detects by columns.

**MTB account → drop in `reports\seller-central\MTB\`:**
- [x] AWD Inventory Report
- [x] FBA Inventory Report (the FULL 97-column version)

**NFMD account → drop in `reports\seller-central\NFMD\`:**
- [x] AWD Inventory Report
- [x] FBA Inventory Report (the FULL 97-column version)

**SS account → drop in `reports\seller-central\SS\`:**
- [x] AWD Inventory Report
- [x] FBA Inventory Report (the FULL 97-column version)

⚠️ **The FBA Inventory Report has 97 columns** including `inbound-shipped`, `inbound-received`, AND aging buckets. Don't pull "Manage FBA Inventory" from the Inventory tab — that's redundant.

---

### ShipBob (4 files — On Hand Summary per brand login)

⚠️ Sign in to each brand separately. Click Inventory → Export → On Hand Summary. ShipBob emails a download link — must be logged in to the correct brand to download.

- [ ] MTB On Hand Summary → `reports\shipbob\MTB\`
- [ ] NFMD On Hand Summary → `reports\shipbob\NFMD\`
- [ ] SS On Hand Summary → `reports\shipbob\SS\`
- [ ] LUMOS On Hand Summary → `reports\shipbob\LUMOS\`

### Floship (1 file)
- [x] Product Inventory export → `reports\floship\`

### Walmart Seller Center (2 files — NFMD + SS)
- [ ] NFMD Item Report → `reports\walmart\NFMD\`
- [ ] SS Item Report → `reports\walmart\SS\`

### Valogix (1 file)
- [x] Item Location History Forecast export

→ Dropped into: `C:\Users\Tom Sapia\MTB-SupplyChain\reports\valogix\`

---

### In-Transit Log (1 file — if updated this week)
- [ ] Latest version: `IN_TRANSIT_LOG_2026-05-01.xlsx`

→ Dropped into: `C:\Users\Tom Sapia\MTB-SupplyChain\reports\in-transit\`

---

### SKU Review (carryover from prior week — if you have decisions to fold in)
- [ ] Updated `sku-review-2026-05-04.xlsx` with new decisions

→ Dropped into: `C:\Users\Tom Sapia\MTB-SupplyChain\outputs\2026-05-04\`

---

## ⚡ Run scripts (after all inputs are dropped)

```
cd C:\Users\Tom Sapia\MTB-SupplyChain
python scripts\combine_forecast.py
python scripts\demand_planning.py
python scripts\build_report.py
python scripts\build_action_plan.py
python scripts\build_shipment_tracking.py
```

- [ ] All scripts ran clean
- [ ] Reviewed: `outputs\2026-05-04\weekly-report-2026-05-04.xlsx`

---

## 📝 Notes / issues this run

- 

---

*Created: 2026-05-01*
