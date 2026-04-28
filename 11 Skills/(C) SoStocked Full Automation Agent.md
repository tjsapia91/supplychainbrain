---
name: sostocked-full-automation
description: >
  Full end-to-end SoStocked automation. Downloads all 9 required files
  (3 Projected Forecast Models + 3 Inventory Current Views + 3 Forecasted vs Actual)
  across all three brands (SS, MTB, NFMD), runs combine_forecast.py to build the
  Weekly_Forecast workbook, then runs demand_planning.py to produce the demand plan.
  Runs every Monday at 8:00 AM or on demand via the chat command
  "run the weekly supply chain report".
---

# SoStocked Full Automation Agent

## Purpose

Zero-manual-touch weekly supply chain pipeline across three SoStocked brands:

| Brand | Abbreviation | Brand ID |
|---|---|---|
| Spa Sciences | SS | 5119 |
| Nasalfresh MD | NFMD | 5109 |
| Michael Todd Beauty | MTB | 5118 |

### What it produces

1. **`Weekly_Forecast_YYYY-MM-DD.xlsx`** — combined forecast + inventory workbook  
   - Location: `~/Downloads/` AND `MTB-SupplyChain\reports\weekly\`  
   - Sheets: Forecast SS, Forecast MTB, Forecast NFMD, Red Flags, Inv. MTB, Inv. SS, Inv. NFMD, Forecast Accuracy

2. **`demand-plan-YYYY-MM-DD.xlsx`** — full demand plan with urgency tiers  
   - Location: `MTB-SupplyChain\outputs\`  
   - Sheets: Priority Actions, High Tier, Watch, Healthy, Low Vel Stockouts

3. **`demand-plan-YYYY-MM-DD.md`** — markdown version for Obsidian vault  
   - Auto-copied to: `supplychainbrain\00 Forecast & Demand Planning\`

4. **`demand-plan-YYYY-MM-DD.json`** — JSON for ERP Reports Hub ingestion

---

## Schedule

- **Recurring:** Every Monday at 8:00 AM local time (`cron: 0 8 * * 1`)
- **On-demand:** Chat command: `run the weekly supply chain report`
- **On failure:** Retry once after 60 seconds. If still failing, stop and notify Tommy with the specific error.

---

## Prerequisites

1. Chrome is open and signed into `https://app.sostocked.com` (session cookies persist between runs).
2. Access to `~/Downloads` folder (read + write + delete).
3. Python 3 with `openpyxl` and `pandas` installed.
4. Scripts present at `C:\Users\Tom Sapia\MTB-SupplyChain\`:
   - `combine_forecast.py`
   - `demand_planning.py`
5. Folder `C:\Users\Tom Sapia\MTB-SupplyChain\reports\weekly\` exists (create if not).

---

## Phase 1 — Download Projected Forecast Models (3 brands)

### 1.1 Navigate to Forecasts page

```
https://app.sostocked.com/me/product-calculations
```

If redirected to login → **stop and notify Tommy** that the SoStocked session has expired and he needs to log in manually.

### 1.2 Download forecast for each brand: SS → NFMD → MTB

For **each** brand, repeat these steps:

**a) Switch to the brand**

Click the **avatar button at the bottom-left of the sidebar** (shows the current brand initials: "SS", "NM", or "MT"). A "Switch Account" dropdown appears listing: Michael Todd, Nasalfresh MD, Spa Sciences. Click the desired brand name. Wait ~3 seconds for the Forecasts page to reload with that brand's data.

**b) Open the download dropdown**

Click the **cloud download icon** in the filter toolbar (right side, next to the search box). Tooltip: "Download Forecast Reports to Excel". A dropdown appears with three radio options.

**c) Select Projected Forecast Model via JavaScript**

⚠️ **CRITICAL:** Do NOT trust the default selection — the default is "Consolidated Forecast w/ Profits". Always explicitly click the Projected Forecast Model radio using this JavaScript:

```javascript
const radios = Array.from(document.querySelectorAll('input[type="radio"]'))
  .filter(r => r.offsetParent !== null);
const projRadio = radios.find(r =>
  (r.parentElement?.innerText || '').includes('Projected'));
if (projRadio) projRadio.click();
const dlBtn = Array.from(document.querySelectorAll('button'))
  .find(b => b.offsetParent !== null && b.textContent.trim() === 'Download');
if (dlBtn) dlBtn.click();
```

**d) Confirm download**

Wait up to 15 seconds for the file to appear in `~/Downloads`. Expected filename pattern:

```
projected-forecast-model-<uuid>-<brand_id>.xlsx
```

Brand IDs: 5119 = SS, 5109 = NFMD, 5118 = MTB.

If no file appears within 15 seconds → retry the download step once. If still nothing → notify Tommy and stop.

### Download order and expected files

| Brand | Brand ID | Expected file pattern |
|---|---|---|
| SS | 5119 | `projected-forecast-model-*-5119.xlsx` |
| NFMD | 5109 | `projected-forecast-model-*-5109.xlsx` |
| MTB | 5118 | `projected-forecast-model-*-5118.xlsx` |

---

## Phase 2 — Download Inventory Current View (3 brands)

### 2.1 Navigate to Inventory page

Click **Inventory** in the left sidebar, or navigate directly to:

```
https://app.sostocked.com/me/inventory
```

### 2.2 Download inventory for each brand: MTB → SS → NFMD

For **each** brand, repeat these steps:

**a) Switch to the brand** (same avatar button method as Phase 1)

**b) Wait ~2 seconds** for the inventory grid to load.

**c) Open the export dropdown**

Click the **cloud/export icon** in the filter toolbar (right side). Tooltip: "Export to Excel". A dropdown appears with radio options: "Export Current View" (default), "Inventory Snapshot", "Export Inventory with Breakdown by Warehouses".

**d) Select Export Current View via JavaScript**

```javascript
const radios = Array.from(document.querySelectorAll('input[type="radio"]'))
  .filter(r => r.offsetParent !== null);
const exportCurrent = radios.find(r =>
  (r.parentElement?.innerText || '').includes('Export Current View'));
if (exportCurrent) exportCurrent.click();
const dlBtn = Array.from(document.querySelectorAll('button'))
  .find(b => b.offsetParent !== null && b.textContent.trim() === 'Download');
if (dlBtn) dlBtn.click();
```

**e) Confirm download**

Wait up to 15 seconds. Expected filename pattern:

```
inventory-<uuid>-<brand_id>.csv
```

Note: inventory files are **.csv** (not .xlsx).

⚠️ **If the dropdown closes without a file downloading:** click the export icon a second time to reopen it, then run the JavaScript again.

### Download order and expected files

| Brand | Brand ID | Expected file pattern |
|---|---|---|
| MTB | 5118 | `inventory-*-5118.csv` |
| SS | 5119 | `inventory-*-5119.csv` |
| NFMD | 5109 | `inventory-*-5109.csv` |

---

## Phase 2b — Download Forecasted vs Actual (3 brands)

Stay on the **Forecasts page** (`/me/product-calculations`).

For **each** brand (SS → NFMD → MTB), repeat:

**a) Switch to the brand** (same avatar button method)

**b) Open the download dropdown** (same cloud download icon)

**c) Select Forecasted vs Actual via JavaScript**

```javascript
const radios = Array.from(document.querySelectorAll('input[type="radio"]'))
  .filter(r => r.offsetParent !== null);
const fvaRadio = radios.find(r =>
  (r.parentElement?.innerText || '').includes('Forecasted vs Actual'));
if (fvaRadio) fvaRadio.click();
const dlBtn = Array.from(document.querySelectorAll('button'))
  .find(b => b.offsetParent !== null && b.textContent.trim() === 'Download');
if (dlBtn) dlBtn.click();
```

**d) Confirm download** — wait up to 15 seconds. Expected filename pattern:

```
<uuid>-<brand_id>.xlsx
```

Note: NO prefix — just UUID + brand ID. Different from Projected Forecast Model files.

| Brand | Brand ID | Expected file pattern |
|---|---|---|
| SS | 5119 | `*-5119.xlsx` (no projected-forecast-model prefix) |
| NFMD | 5109 | `*-5109.xlsx` |
| MTB | 5118 | `*-5118.xlsx` |

---

After Phases 2 and 2b, `~/Downloads` should contain 9 new files:
- 3 × `projected-forecast-model-*-<id>.xlsx`
- 3 × `inventory-*-<id>.csv`
- 3 × `<uuid>-<id>.xlsx` (Forecasted vs Actual)

---

## Phase 3 — Run combine_forecast.py

Open **PowerShell** and run:

```powershell
cd "C:\Users\Tom Sapia\MTB-SupplyChain"
python combine_forecast.py
```

⚠️ Note the quotes around the path — required because of the space in `Tom Sapia`.

### What this does

- Auto-finds the 6 downloaded files by brand_id pattern in `~/Downloads`
- Renames them to `SS_Forecast_YYYY-MM-DD.xlsx`, `MTB_Forecast_YYYY-MM-DD.xlsx`, etc.
- Extracts the "Forecasted Sales" sheet from each forecast file
- Appends all 3 inventory CSVs as sheets
- Runs the Red Flags analysis (steady forecasts with 1–3 anomalous zero weeks)
- Saves `Weekly_Forecast_YYYY-MM-DD.xlsx` to `~/Downloads`
- Cleans up the 6 individual files

### Expected output

```
Saved ~/Downloads/Weekly_Forecast_YYYY-MM-DD.xlsx
  Sheets: ['Forecast SS', 'Forecast MTB', 'Forecast NFMD', 'Red Flags', 'Inv. MTB', 'Inv. SS', 'Inv. NFMD']
  SS: N rows | MTB: N rows | NFMD: N rows | N red flags
```

If any brand has 0 rows → check that the correct brand's forecast file was downloaded (brand_id must match).

---

## Phase 4 — Move workbook to reports\weekly\

```powershell
$today = Get-Date -Format "yyyy-MM-dd"
$src = "$env:USERPROFILE\Downloads\Weekly_Forecast_$today.xlsx"
$dst = "C:\Users\Tom Sapia\MTB-SupplyChain\reports\weekly\"
New-Item -ItemType Directory -Force -Path $dst | Out-Null
Copy-Item -Path $src -Destination $dst -Force
Write-Host "Copied Weekly_Forecast_$today.xlsx to reports\weekly\"
```

This makes the file available for `demand_planning.py` which auto-scans `reports\weekly\` for the most recent `Weekly_Forecast_*.xlsx`.

---

## Phase 5 — Run demand_planning.py

```powershell
cd "C:\Users\Tom Sapia\MTB-SupplyChain"
python demand_planning.py
```

### What this does

- Reads from `reports\weekly\Weekly_Forecast_YYYY-MM-DD.xlsx` (auto-finds latest)
- Applies region normalization: MX removed, NAm/US+MX → US, CA separate
- Calculates Days of Supply: `(FBA Stock + AWD Warehouse) ÷ Adj. Velocity`
- Applies urgency tiers: 🚨 AMAZON STOCKOUT → 🔴 TRUE STOCKOUT → 🔴 CRITICAL → 🟠 HIGH → 🟡 WATCH → 🟢 HEALTHY
- Calculates PO quantities for items at or past reorder point
- Outputs 3 files to `outputs\`

### Expected console output

```
✅ Loaded weekly workbook: Weekly_Forecast_YYYY-MM-DD.xlsx
   SS: N rows | MTB: N rows | NFMD: N rows
✅ Demand plan complete.
   Priority Actions (CRITICAL + TRUE STOCKOUT): N items
   HIGH tier: N items
   Output saved: outputs\demand-plan-YYYY-MM-DD.xlsx
   Vault copy: supplychainbrain\00 Forecast & Demand Planning\demand-plan-YYYY-MM-DD.md
```

---

## Phase 6 — Open outputs

After both scripts complete:

1. Open `MTB-SupplyChain\outputs\demand-plan-YYYY-MM-DD.xlsx` — the full demand plan for review and PO decisions.
2. Open `MTB-SupplyChain\reports\weekly\Weekly_Forecast_YYYY-MM-DD.xlsx` — the combined forecast workbook for visual review.

---

## Complete run summary (what the agent executes)

```
PHASE 1: FORECAST DOWNLOADS
  → Switch to SS → Click download → JS: select Projected → confirm file
  → Switch to NFMD → Click download → JS: select Projected → confirm file
  → Switch to MTB → Click download → JS: select Projected → confirm file

PHASE 2: INVENTORY DOWNLOADS
  → Go to Inventory
  → Switch to MTB → Click export → JS: select Export Current View → confirm file
  → Switch to SS → Click export → JS: select Export Current View → confirm file
  → Switch to NFMD → Click export → JS: select Export Current View → confirm file

PHASE 3: COMBINE
  → PowerShell: python combine_forecast.py
  → Verify: Weekly_Forecast_YYYY-MM-DD.xlsx exists with 7 sheets

PHASE 4: STAGE
  → PowerShell: copy Weekly_Forecast to reports\weekly\

PHASE 5: DEMAND PLAN
  → PowerShell: python demand_planning.py
  → Verify: demand-plan-YYYY-MM-DD.xlsx exists in outputs\

PHASE 6: OPEN OUTPUTS
  → Open demand plan in Excel
```

Total estimated runtime: **8–12 minutes** (mostly SoStocked download wait times).

---

## Failure handling

| Failure | Action |
|---|---|
| Redirected to SoStocked login | Stop. Notify Tommy: "SoStocked session expired — please log in at app.sostocked.com, then re-run." |
| Download not found within 15s | Retry the download step once. If still missing, notify and stop. |
| combine_forecast.py error: `Brand X has 0 rows` | One of the 6 files has the wrong brand_id in the filename. Check ~/Downloads for any leftover files from a previous run and delete them, then re-download that brand. |
| demand_planning.py: `No weekly workbook found` | The copy step (Phase 4) may have failed. Manually copy Weekly_Forecast file to `reports\weekly\`. |
| PowerShell: `PositionalParameterNotFound` | Path has a space — make sure `cd` path is in double quotes: `cd "C:\Users\Tom Sapia\MTB-SupplyChain"` |
| Any script exception | Retry the whole run once after 60 seconds. If still failing, notify with the full error traceback. |

---

## Known quirks (hard-learned)

1. **SoStocked download radio bug:** Setting `radio.checked = true` in JavaScript does NOT update Vue/React internal state. Always use `radio.click()` — this is the only method that actually changes the download type.

2. **Inventory dropdown may close on first click:** If the export dropdown opens and immediately closes, click the export icon a second time and run the JS again. This happens intermittently — the second click always works.

3. **Default forecast radio is NOT Projected Forecast Model:** The default is "Consolidated Forecast w/ Profits". Always run the JS selection before clicking Download, regardless of what looks selected visually.

4. **Inbound FBA excluded from PO formula:** SoStocked's combined export shows a consolidated 46,129-unit inbound figure on US rows (not per-product). demand_planning.py intentionally excludes inbound_fba from the PO quantity calculation until this is confirmed clean in SAP.

5. **Coordinate reference (for pixel-based click fallback):** Brand avatar button ≈ (55, 611). Forecast download icon ≈ (1016, 176) when warning banner is present, (1016, 116) without. Inventory export icon ≈ (1089, 162). Coordinates may shift slightly based on browser zoom level.

---

## File locations reference

| File | Location |
|---|---|
| combine_forecast.py | `C:\Users\Tom Sapia\MTB-SupplyChain\combine_forecast.py` |
| demand_planning.py | `C:\Users\Tom Sapia\MTB-SupplyChain\demand_planning.py` |
| Weekly workbook (Downloads) | `C:\Users\Tom Sapia\Downloads\Weekly_Forecast_YYYY-MM-DD.xlsx` |
| Weekly workbook (staged) | `C:\Users\Tom Sapia\MTB-SupplyChain\reports\weekly\Weekly_Forecast_YYYY-MM-DD.xlsx` |
| Demand plan Excel | `C:\Users\Tom Sapia\MTB-SupplyChain\outputs\demand-plan-YYYY-MM-DD.xlsx` |
| Demand plan markdown | `C:\Users\Tom Sapia\supplychainbrain\00 Forecast & Demand Planning\demand-plan-YYYY-MM-DD.md` |
| Demand plan JSON | `C:\Users\Tom Sapia\MTB-SupplyChain\outputs\demand-plan-YYYY-MM-DD.json` |

---

## Change log

- 2026-04-22 — Full unified agent created. Extends SoStocked_Weekly_Forecast_Agent to include demand_planning.py pipeline. Phase 3–5 added (combine → stage → demand plan). demand_planning.py confirmed to read from `reports\weekly\` as primary input (legacy agency/inventory folders are fallback only).
