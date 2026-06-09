# (C) Forecast Accuracy & Buffer Sizing — Build Plan

> Comprehensive plan to add forecast vs actual analysis, per-SKU accuracy scoring, and accuracy-driven PO buffer sizing to the weekly pipeline.
>
> **Captured:** May 6, 2026 · **Last updated:** June 8, 2026
> **Status:** 🟡 **Phase 1 + 2 + 5 SHIPPED. Phase 3 awaiting data accumulation. Phase 4 still parked.**
> **Trigger phrase to revisit Phases 3+4:** *"Let's pick up Phase 3 of the forecast accuracy plan"*

---

## ✅ Shipped phases (as of June 8, 2026)

| Phase | Status | Where to see it |
|---|---|---|
| **Phase 1 — Snapshot infrastructure** | ✅ **SHIPPED** May 27, 2026 | `reports/archive/valogix-forecasts/forecast-snapshot-YYYY-MM-DD.csv` — 12+ snapshots accumulated, daily/weekly capture runs automatically as part of `build_report.py` |
| **Phase 2 — Amazon FvA tab** | ✅ **SHIPPED** | `📈 Amazon FvA` tab in `weekly-report.xlsx` — 105 ASINs × current month (May 2026 MTD as of last run). Sources from SoStocked Forecasted vs Actual reports. |
| **Phase 5 — Sales Anomalies tab** | ✅ **SHIPPED** | `📊 Sales Anomalies` tab in `weekly-report.xlsx` — uses Valogix `History Exception Report` (now a weekly input in `reports/_data/valogix-exceptions/`). 18 flagged anomalies last run. |

## 🟡 Still parked

| Phase | Status | Gating issue |
|---|---|---|
| **Phase 3 — Per-SKU accuracy scoring** | 🟡 **Data accumulating** | Need ~6-8 weeks of Phase 1 snapshots before MAPE computations are reliable. We have ~2 weeks so far. ETA: mid-July 2026. |
| **Phase 4 — Accuracy-driven PO buffer sizing** | ⏳ **PARKED** | Depends on Phase 3. Open questions (below) still need decisions. |

---

## Why this exists

We have rich forecast data (SoStocked weekly forecasts, Valogix 18-month forward forecasts, Walmart 3-window forecasts). What we DON'T have yet (Phase 3+4) is a way to know:

1. **How accurate are our forecasts historically?** (Are we systematically over/under-forecasting?)
2. **Which SKUs have reliable forecasts and which don't?**
3. **How much PO buffer should each SKU carry given its forecast quality?**

Without this, every replenishment decision uses a flat buffer regardless of whether forecasts are 95% accurate or 50% accurate. That's leaving money on the table both ways — over-buying on accurate SKUs, under-buying on volatile ones.

Phase 2 (Amazon FvA tab) gives visibility into Amazon-side accuracy. Phase 5 (Sales Anomalies) catches statistical outliers. The missing piece is **automatic accuracy scoring + PO buffer flex** (Phases 3+4).

---

## Data sources & their FvA capabilities

| Source | Has historical FvA? | Notes |
|---|---|---|
| **SoStocked FvA report** | ✅ YES — 12 months per ASIN | Loaded into `Weekly_Forecast_*.xlsx` → surfaced in `📈 Amazon FvA` tab (Phase 2 ✓) |
| **Valogix `Item-Location-History-Forecast`** | ❌ Forecast overwritten by actual | Standard weekly report — actuals + forward forecast only. Phase 1 snapshots solve this. |
| **Valogix `History Exception Report`** | ⚠️ Partial — only outliers | Lists 20-ish items where actuals fell outside statistical bounds. Drives `📊 Sales Anomalies` tab (Phase 5 ✓) |
| **Valogix `Forecast Override Report`** | ❌ Manual overrides only | Tracks where forecasts were hand-tuned, not auto vs actual |
| **Walmart Seller Center** | ❌ Forward only | 3 forecast windows + daily sales |
| **Phase 1 snapshot tracker** | ✅ Accumulating (Week ~2 of 8) | `reports/archive/valogix-forecasts/forecast-snapshot-*.csv` — compare prior weeks' forecasts to current actuals |

### Definitive answer on Valogix
After exhaustive search of Valogix's Analytics, Replenishment Planning, Inventory Data, and Settings sections — **Valogix does not provide a dedicated forecast accuracy report**. The closest thing (History Exception Report) catches anomalies but doesn't track every forecast vs every actual. This is why Phase 1 was critical to start early.

---

## Architecture — 5 phases

### Phase 1 — Snapshot infrastructure ✅ SHIPPED (May 27, 2026)

**Built:**
- Folder: `reports/archive/valogix-forecasts/`
- Pre-archive hook in `build_report.py` (`_snapshot_valogix_forecasts()` function at the end of `load_valogix()`)
- Each weekly run: extracts the forecast columns + Item Number + Location + run-date, saves as a flat `forecast-snapshot-YYYY-MM-DD.csv`
- Currently 12 snapshots stored (May 27 → Jun 8)

**Status:** Running automatically every pipeline run. By mid-July we'll have enough data for Phase 3.

---

### Phase 2 — Amazon FvA tab ✅ SHIPPED

**Built:** `📈 Amazon FvA` tab on `weekly-report.xlsx` with:
- Per ASIN row: ASIN · Brand · Product · Status · forecast/actual/variance for current period
- Color-coded variance (≥±20% red, ±10-20% yellow, <±10% green)
- Bottom: ABC + Status legend strips
- Tab color: deep teal (Amazon family)

**Function:** `load_amazon_fva()` + `build_amazon_fva_tab()` in `build_report.py`. Source: SoStocked Forecasted vs Actual files dropped into `reports/_data/sostocked/[BRAND]/fva-history/`.

**Last run:** 124 forecast records across 1 period (May 2026 MTD).

---

### Phase 3 — Per-SKU accuracy scoring 🟡 DATA ACCUMULATING

**Why:** Drives Phase 4 (buffer sizing). Need per-SKU accuracy to know which forecasts to trust.

**To build (when ~8 weeks of Phase 1 snapshots accumulated):**
- Compute trailing 6-month MAPE per ASIN (Amazon side — Phase 2 has this data already)
- Compute trailing 6-month MAPE per Item × Location (Valogix side — from Phase 1 archives)
- Add `FORECAST ACCURACY %` column to relevant tabs (THIS WEEK ORDER section, PO Priority, ShipBob, Walmart)
- Color-coded: ≥90% green, 70-90% yellow, <70% red
- Items with insufficient history show "—"

**ETA:** mid-July 2026 (8 weeks after Phase 1 started May 27).

---

### Phase 4 — Accuracy-driven PO buffer sizing ⏳ PARKED

**Why:** This is the operational payoff. PO recommendations auto-scale based on forecast quality.

**To build (after Phase 3 ships):**
- New formula in `demand_planning.py` PO sizing:
  ```
  effective_buffer_days = base_buffer_days × (2 - accuracy_score)

  where accuracy_score = MAPE_to_score (1.0 perfect → 0.5 terrible)
  ```
  Examples:
  - 95% accurate SKU: 60 × (2 - 0.95) = 63 day buffer
  - 70% accurate SKU: 60 × (2 - 0.70) = 78 day buffer
  - 50% accurate SKU: 60 × (2 - 0.50) = 90 day buffer
- New columns on the relevant action tabs: `Standard Buffer`, `Accuracy-Adjusted Buffer`, `Δ Buffer Days`
- Hover comment explains the math
- Hard floor: 60 days. Hard ceiling: 120 days.

**Deliverable:** dynamic PO sizing that reflects forecast confidence — replaces today's volatility-bucket buffer (STABLE 1.0× / MODERATE 1.1× / VOLATILE 1.25× in `build_order_list.py`).

---

### Phase 5 — Sales Anomalies tab ✅ SHIPPED

**Built:** `📊 Sales Anomalies` tab uses Valogix `History Exception Report` (`schain_itemLocationHistoryException_*.csv` in `reports/_data/valogix-exceptions/`).

**Columns shown:** Item Number · Description · Location · Date · History Value · Expected Value (statistical) · Variance · Severity. Sorted by severity descending.

**Function:** `load_valogix_exceptions()` + `build_sales_anomalies_tab()` in `build_report.py`. 18 anomalies flagged last run.

---

## Open questions to lock in before Phases 3 + 4

### Methodology
1. **Which accuracy metric — MAPE, weighted MAPE, or bias-adjusted?** MAPE is simplest; bias-adjusted catches systematic over/under-forecasting better.
2. **What lookback period — trailing 6 months or trailing 12?** Six is responsive; 12 is stable.
3. **Treat short-history SKUs differently?** New products have no track record. Show "—" or use category-level accuracy as fallback?
4. **How does manual override (like the CA 13% rule) factor in?** Items with manual overrides probably shouldn't ding "Valogix forecast accuracy" because we KNOW we're not using Valogix's forecast for those.

### Display
5. **Where does the accuracy column live?** Always-visible on THIS WEEK ORDER, or in a collapsible group?
6. **Color thresholds for accuracy?** ≥90/70/50 default, but might need tuning for low-volume SKUs.
7. **Show accuracy as % or as a score (0-1)?** % is more intuitive but takes more chars.

### Operational
8. **How does the accuracy buffer interact with the existing volatility buckets** (STABLE 1.0× / MODERATE 1.1× / VOLATILE 1.25× / INSUFFICIENT 1.3×) in `build_order_list.py`? Replace, multiply, or use whichever is more conservative?

---

## Revised execution sequence (June 8, 2026)

| Window | Action | Status |
|---|---|---|
| **May 27** | Phase 1 — snapshot tracker | ✅ Done |
| **~Early May** | Phase 2 — Amazon FvA tab | ✅ Done |
| **~Mid May** | Phase 5 — Sales Anomalies tab | ✅ Done |
| **Weeks 4-7** (current) | Snapshots accumulate. Audit `📈 Amazon FvA` quarterly — useful signal or noise? | 🟡 In progress |
| **Mid-July 2026** | Phase 3 — Per-SKU accuracy scoring. ~8 weeks of Valogix snapshots available. | ⏳ Pending |
| **Late-July / Aug 2026** | Phase 4 — Accuracy-driven PO buffer sizing. The operational payoff. | ⏳ Pending |

---

## Dependencies

```
Phase 1 (snapshots ✅) ──→ Phase 3 (accuracy %) ──→ Phase 4 (buffer sizing)
Phase 2 (Amazon FvA ✅) ──→ Phase 3 (Amazon-side data already there)
Phase 5 (anomalies ✅) — independent
```

---

## To revisit

Trigger phrases:
- *"Let's pick up Phase 3 of the forecast accuracy plan"* — once mid-July hits
- *"Lock in the open questions on forecast accuracy"* — answer the 8 methodology/display/ops questions before Phase 3 build
- *"Audit the Amazon FvA tab"* — quarterly review of whether Phase 2 is surfacing useful insights vs noise

---

## Related docs

- [[06 Processes & SOPs/(C) Weekly Inputs Sourcing SOP]] — History Exception Report + FvA pulls
- [[06 Processes & SOPs/(C) ABC Classification Reference]] — accuracy interacts with ABC routing
- [[06 Processes & SOPs/(C) ShipBob Inventory Protection — Channel Reserve Logic]] — buffer-sizing sibling concept (non-Amazon channels)
- [[07 AI Tools & Builds/(C) SAP Open POs Integration — Build Plan]] — sibling parked plan
- [[07 AI Tools & Builds/(C) Inventory & Demand Planning Analysis Project — Parked]] — sibling parked plan

---

*Captured: May 6, 2026 · Last updated: June 8, 2026 (marked Phases 1+2+5 as SHIPPED, refreshed timeline, set Phase 3 ETA to mid-July) · Owner: Tommy*
