# Monday Demand Plan Runcard
**Cadence:** Every Monday morning — do this before anything else
**Time required:** ~45 minutes
**Last updated:** April 27, 2026

---

## Step 1 — Download SoStocked Files (10 min)

Run the browser automation agent OR download manually:

> Full automation doc: [[11 Skills/(C) SoStocked Full Automation Agent]]

Manual downloads (if automation fails):
1. Log into SoStocked
2. Go to **Settings → Bulk Export/Import**
3. Download **Multi-Dashboard Report (All Accounts)** → drop into `reports\weekly\`
4. Download **Inventory Export** → drop into `reports\inventory\`

**All 6 files should land in the right folders before running anything.**

---

## Step 2 — Run the Pipeline (5 min)

```powershell
cd C:\Users\Tom Sapia\MTB-SupplyChain
python combine_forecast.py
python demand_planning.py
```

Output file: `outputs\demand-plan-YYYY-MM-DD.xlsx`

If errors → check that files landed in the right folders. See [[06 Processes & SOPs/(C) Demand Planning SOP]] for troubleshooting.

---

## Step 3 — Review the Output (15 min)

Open the Excel file. Go through sheets in this order:

**Sheet 1 — Priority Actions**
- [ ] Any new TRUE STOCKOUTs since last week?
- [ ] Any items that were CRITICAL last week and are still CRITICAL? (chronic — escalate)
- [ ] Any surprises — items you didn't expect to see here?

**Sheet 2 — HIGH / Watch**
- [ ] Any HIGH items close to flipping CRITICAL?
- [ ] Any velocity spikes on previously HEALTHY items?

**Sheet 3 — Low Vel Stockouts**
- [ ] Skim — anything here that shouldn't be? (active listing stocked out)

**Sheets 4–5 — Healthy / Inactive**
- [ ] Spot check only — flag anything unusual

> ⚠️ Known bugs as of April 27: HIGH tier missing 13 items. Inbound FBA bleed causing 0 PO qty on ~10 CRITICAL items. Don't trust PO qty = 0 on CRITICAL MTB items until fixed. See [[Projects/HIGH Tier Fix/Overview]] and [[Projects/Inbound FBA Bug Fix/Overview]].

---

## Step 4 — Take Action (15 min)

Work through Priority Actions top to bottom:

| What you see | What you do |
|---|---|
| TRUE STOCKOUT | Place PO immediately → log in [[01 Purchasing & Inventory/(C) PO Tracker\|PO Tracker]] |
| AMAZON STOCKOUT | Create FBA send-in from AWD/warehouse |
| CRITICAL | Place PO this week → use Order Qty from output |
| HIGH | Place PO by Friday |
| Chronic CRITICAL (3+ weeks) | Flag to DOS |
| Velocity spike | Investigate before acting — promo? Listing change? |

For PO creation: [[06 Processes & SOPs/(C) PO Creation SOP]]

---

## Step 5 — Update the Vault (5 min)

- [ ] Replace priorities table in [[Home]] with new output
- [ ] Update "Last demand plan run" and "Next run" dates in [[Home]]
- [ ] Save weekly snapshot → `00 Forecast & Demand Planning/[BRAND]/weekly-YYYY-MM-DD.md`
- [ ] Update any project statuses that changed

---

## Step 6 — Flag Anything That Needs DOS/SVP

Before you close out, ask yourself:
- Is anything chronic (flagged 3+ weeks in a row)?
- Did anything spike unexpectedly?
- Is any PO value going to exceed budget threshold?

If yes → send a quick note to DOS before end of day.

---

## Done. Close the Excel, open your PO tracker, start placing orders.
