# (C) Forecast Accuracy & Buffer Sizing — Build Plan

> Comprehensive plan to add forecast vs actual analysis, per-SKU accuracy scoring, and accuracy-driven PO buffer sizing to the weekly pipeline. **Parked plan** — work through the open questions before executing.
>
> **Captured:** May 6, 2026
> **Status:** PARKED — awaiting decisions on open questions
> **Trigger phrase to revisit:** *"Let's pick up the forecast accuracy build plan"*

---

## Why this exists

We have rich forecast data (SoStocked weekly forecasts, Valogix 18-month forward forecasts, Walmart 3-window forecasts). What we DON'T have is a way to know:

1. **How accurate are our forecasts historically?** (Are we systematically over/under-forecasting?)
2. **Which SKUs have reliable forecasts and which don't?**
3. **How much PO buffer should each SKU carry given its forecast quality?**

Without this, every replenishment decision uses a flat 60-day buffer regardless of whether forecasts are 95% accurate or 50% accurate. That's leaving money on the table both ways — over-buying on accurate SKUs, under-buying on volatile ones.

---

## Data sources & their FvA capabilities

| Source | Has historical FvA? | Notes |
|---|---|---|
| **SoStocked FvA report** | ✅ YES — 12 months per ASIN | Already loaded into `Weekly_Forecast_*.xlsx` Forecast Accuracy sheet. Just need to surface it. |
| **Valogix `Item-Location-History-Forecast`** | ❌ Forecast overwritten by actual | Standard report we pull weekly — actuals + forward forecast only |
| **Valogix `History Exception Report`** | ⚠️ Partial — only outliers | Lists 20-ish items where actuals fell outside statistical bounds. Useful for bad-data flagging, not full FvA. |
| **Valogix `Forecast Override Report`** | ❌ Manual overrides only | Tracks where forecasts were hand-tuned, not auto vs actual |
| **Walmart Seller Center** | ❌ Forward only | 3 forecast windows + daily sales |
| **Snapshot tracker** (to build) | ✅ Will accumulate over 6-8 weeks | Save weekly Valogix forecast snapshots → compare to actual when month closes |

### Definitive answer on Valogix
After exhaustive search of Valogix's Analytics, Replenishment Planning, Inventory Data, and Settings sections — **Valogix does not provide a dedicated forecast accuracy report**. The closest thing (History Exception Report) catches anomalies but doesn't track every forecast vs every actual.

---

## Architecture — 5 phases

### Phase 1 — Snapshot infrastructure (must start IMMEDIATELY)
**Why first:** Every week we don't capture Valogix forecast snapshots is a week of FvA data we can never recover. Zero UI impact. ~10 lines of code.

**Build:**
- New folder: `reports/archive/valogix-forecasts/`
- Pre-archive hook in `build_report.py` (or separate script `archive_valogix_forecast.py`)
- Each weekly run: extract just the forecast columns (cols 31-50) + Item Number + Location + run-date, save as a flat `forecast-snapshot-YYYY-MM-DD.csv`
- After 6-8 weekly runs we have a meaningful sample for comparing prior forecasts to current actuals

**Deliverable:** weekly accumulating archive of forward forecasts. No new UI on the report yet.

---

### Phase 2 — Amazon FvA tab (ready to ship — uses existing SoStocked data)
**Why now:** SoStocked already publishes 12 months of Amazon FvA. We're loading it into `Weekly_Forecast_*.xlsx` but not surfacing it on the weekly report.

**Build:**
- New tab `📈 Amazon Forecast Accuracy` on `weekly-report.xlsx`
- Per ASIN row, columns:
  - `ASIN`, `Brand`, `Product`, `Status` (current)
  - For each of the last 6 months: `Forecast`, `Actual`, `Variance %`, `Variance units`
  - Trailing 6mo MAPE (Mean Absolute Percentage Error)
  - Color-coded variance: ≥±20% red, ±10-20% yellow, <±10% green
- Bottom: ABC + Status legend strips
- Tab color: deep teal (Amazon family)

**Deliverable:** dedicated Amazon FvA tab on weekly report with color-coded variance.

---

### Phase 3 — Per-SKU accuracy scoring
**Why:** Drives Phase 4 (buffer sizing). Need per-SKU accuracy to know which forecasts to trust.

**Build:**
- Compute trailing 6-month MAPE per ASIN (Amazon side, from Phase 2 data)
- Compute trailing 6-month MAPE per Item × Location (Valogix side, from Phase 1 archives — only available after 6 weeks)
- Add `FORECAST ACCURACY %` column to relevant tabs (Items Needing Action, Inventory Overview, Action Plan)
- Color-coded: ≥90% green, 70-90% yellow, <70% red
- Items with insufficient history show "—"

**Deliverable:** accuracy % visible on every priority/action item.

---

### Phase 4 — Accuracy-driven PO buffer sizing
**Why:** This is the operational payoff. PO recommendations auto-scale based on forecast quality.

**Build:**
- New formula in `demand_planning.py` PO sizing:
  ```
  effective_buffer_days = base_buffer_days × (2 - accuracy_score)
  
  where accuracy_score = MAPE_to_score (1.0 perfect → 0.5 terrible)
  ```
  Examples:
  - 95% accurate SKU: 60 × (2 - 0.95) = 63 day buffer
  - 70% accurate SKU: 60 × (2 - 0.70) = 78 day buffer
  - 50% accurate SKU: 60 × (2 - 0.50) = 90 day buffer
- New columns on Action Plan: `Standard Buffer`, `Accuracy-Adjusted Buffer`, `Δ Buffer Days`
- Hover comment explains the math
- Hard floor: 60 days (current minimum). Hard ceiling: 120 days (don't over-buy even if forecasts are bad).

**Deliverable:** dynamic PO sizing that reflects forecast confidence.

---

### Phase 5 — Sales Anomalies tab (independent, optional)
**Why:** Catches bad-data months automatically (the Soniclear White Marble Jul/Aug pattern).

**Build:**
- Add Valogix `History Exception Report` as a new weekly input (`reports/valogix-exceptions/`)
- New tab `📊 Sales Anomalies` on `weekly-report.xlsx`
- Columns: Item Number, Description, Location, Date, History Value, Expected Value (statistical), Variance, Severity
- Sorted by severity descending
- Useful for spotting bad SoStocked data before it triggers wrong replenishment decisions

**Deliverable:** weekly anomaly flagger. Can be built any time independently of Phases 1-4.

---

## Open questions to lock in before building

### Architectural
1. **Where do Valogix snapshots live?** Inside `reports/archive/valogix-forecasts/` (clean) or somewhere else?
2. **What gets archived — full Valogix file or just forecast columns?** Full file is safer (audit trail) but bigger.
3. **How does FvA interact with the SoStocked FvA we already load into Weekly_Forecast?** Use SoStocked's authoritative for Amazon, snapshot tracker for Valogix channels?

### Methodology
4. **Which accuracy metric — MAPE, weighted MAPE, or bias-adjusted?** MAPE is simplest; bias-adjusted catches systematic over/under-forecasting better.
5. **What lookback period — trailing 6 months or trailing 12?** Six is responsive; 12 is stable.
6. **Treat short-history SKUs differently?** New products have no track record. Show "—" or use category-level accuracy as fallback?
7. **How does manual override (like the CA 13% rule) factor in?** Items with manual overrides probably shouldn't ding "Valogix forecast accuracy" because we KNOW we're not using Valogix's forecast for those.

### Display
8. **Where does the accuracy column live?** Always-visible on Items Needing Action, or in the collapsible group?
9. **Color thresholds for accuracy?** ≥90/70/50 default, but might need tuning for low-volume SKUs.
10. **Show accuracy as % or as a score (0-1)?** % is more intuitive but takes more chars.

### Operational
11. **Will Augusto need to pull a new report each Monday?** History Exception Report yes (Phase 5). Snapshot tracker no (automatic).
12. **What if Valogix changes its file format again?** Snapshot tracker is column-name dependent — same risk as today.

---

## Recommended execution sequence

| Week | Action | Builds |
|---|---|---|
| **Week 0 (now)** | Phase 1 only — start the snapshot tracker. **No UI changes.** | Snapshot infrastructure |
| **Week 0** | Save THIS plan + answer open questions over the next few days | (planning) |
| **Week 1** | Phase 2 — Amazon FvA tab. Validate the SoStocked FvA data quality. | Amazon FvA visibility |
| **Week 2** | Phase 5 — Sales Anomalies tab (independent of Phase 3-4) | Bad-data flagging |
| **Weeks 2-7** | Snapshots accumulate. Watch the Amazon FvA tab — does it surface useful insights or is it noise? | (data accumulating) |
| **Week 8** | Phase 3 — Per-SKU accuracy scoring. By now we have ~8 weeks of Valogix snapshots. | Accuracy column |
| **Week 10** | Phase 4 — Accuracy-driven PO buffer sizing. Most operationally valuable, last to ship because it depends on validated accuracy data. | Smart PO buffer |

Total time: ~10 weeks calendar, ~2-3 weeks of actual build work spread across that window.

---

## Dependencies

```
Phase 1 (snapshots) ─────────────┐
                                  ↓
Phase 2 (Amazon FvA tab) ────→ Phase 3 (accuracy %) ────→ Phase 4 (buffer sizing)
                                  
Phase 5 (anomalies) — independent of all the above
```

---

## What this plan replaces

- The standalone "snapshot tracker" idea I floated earlier (now Phase 1)
- The "Layer 1 / 2 / 3" sketch from earlier conversation (now Phases 2 / 3 / 4)
- The "Sales Anomalies tab" idea (now Phase 5)

This is the consolidated, sequenced build plan.

---

## To revisit

Type:
- *"Let's pick up the forecast accuracy build plan"*
- *"Start Phase 1 of forecast accuracy"*
- *"Lock in the open questions on forecast accuracy"*

Claude will read this doc, ask which phase to start, and walk through the open questions as needed.

---

## Related docs

- [[06 Processes & SOPs/(C) Weekly Inputs Sourcing SOP]] — will need a new entry for History Exception Report (Phase 5)
- [[06 Processes & SOPs/(C) ABC Classification Reference]] — could mention accuracy interaction
- [[07 AI Tools & Builds/(C) SAP Open POs Integration — Build Plan]] — sibling parked plan
- [[07 AI Tools & Builds/(C) Inventory & Demand Planning Analysis Project — Parked]] — sibling parked plan

---

*Captured: May 6, 2026 · Owner: Tommy*
