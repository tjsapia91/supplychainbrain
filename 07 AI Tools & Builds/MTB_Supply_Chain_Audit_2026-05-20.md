# MTB Supply Chain System — Audit

**Prepared by:** Senior Supply Chain audit, written 2026-05-20
**Scope:** Reliability, simplification opportunities, gaps, prioritized action list, and codebase cleanup plan
**Materials reviewed:** All 19 Python scripts (~18,500 lines), 7 vault SOPs, README, CLAUDE_BRIEFING.md, WEEKLY_ANALYSIS_SKILL.md, sample weekly-report-2026-05-19.xlsx output
**Verification status:** Source-grounded where noted; flagged as inference where I could not verify

**Revision history:**
- v1 (2026-05-20) — initial audit
- v2 (2026-05-20) — added Section 5B: Codebase Cleanup Plan; updated action list

---

## Executive summary

You have a working system that produces a sophisticated weekly output (15 tabs, 5 channels, 3 brands, 2 markets). The output is genuinely strong — better than what most $80M brands produce internally. **The system is reliable in its current form, but it has accumulated drift and duplication that will cause real failures in 6-12 months if not addressed.**

**The five things that matter most**, in priority order:

1. **You have a buffer-days mismatch that's silently sizing POs wrong.** `demand_planning.py` uses 60 days of buffer beyond lead time when calculating PO quantities. `build_report.py` uses 120 days for the Replenishment Triggers tab. Your CLAUDE_BRIEFING.md says 120 (4 months). This means the PO quantity number on the Action Plan and the recommended order quantity on Replenishment Triggers can disagree for the same SKU. **Severity: HIGH. Fix this first.**

2. **The "ShipBob gate" you said we needed to build... already exists.** It's implemented in two places in `build_report.py` (lines 7044 and 8088). The skill file documents it. The output workbook shows it as a column. You may not have realized this — which itself is the finding. If you don't know what's in your own system, you can't trust it. **Severity: HIGH for trust, MEDIUM for technical health.**

3. **Status classification logic lives in 5+ places with different rules.** I flagged this before; after re-reading the code I'm more concerned, not less. The Walmart NFMD block uses `<30 LOW`, Walmart SS uses `<60 LOW`, the Amazon recompute uses entirely different thresholds. **Severity: MEDIUM. Real consolidation work, real payoff.**

4. **Roughly 12 of 19 Python scripts are not called by the weekly skill.** Some are valid one-offs, some are obsolete predecessors, some are mystery files. Without a cleanup, every new planner who reads the codebase will waste time figuring out what's live. **Severity: LOW for current operation, HIGH for transferability.**

5. **You're collecting forecast-accuracy data and never feeding it back.** Your `📈 Amazon FvA` tab shows 282 SKUs with variance >30%. That signal sits in a tab and dies. The most valuable improvement to make this system smarter — not just bigger — is closing that loop. **Severity: LOW for current operation, GAME-CHANGING for system maturity.**

The rest of this document goes through each finding with reasoning, recommendations, and a prioritized action list at the end.

---

## Section 1 — Reliability findings

### R1. Buffer days mismatch — POs sized at 60 days, planning assumes 120 ⚠️ HIGH

**What I found.** Two different scripts use two different buffer constants for the same conceptual quantity.

```
demand_planning.py line 74:   BUFFER_DAYS = 60     # days of buffer beyond lead time
build_report.py line 7045:    COVERAGE_BUFFER_DAYS = 120  # 4 months minimum post-arrival
CLAUDE_BRIEFING.md says:      120 days (4 months) — locked-in business rule
```

**Why it matters.** The PO quantity formula in `demand_planning.py` is:
```
po_qty = po_velocity × (lead_time + BUFFER_DAYS) - available_stock
       = po_velocity × (120 + 60) - available     ← uses 180 days
```

The Replenishment Triggers logic in `build_report.py` is:
```
horizon = LEAD_120 + COVERAGE_BUFFER_DAYS  = 240 days
needed = velocity × 240 - pipeline
```

For a SKU selling 10 units/day, `demand_planning` will recommend a PO of `1800 - available`, while `build_report`'s Replenishment Triggers will recommend `2400 - pipeline`. **The two outputs in your own weekly workbook are giving different answers to the same question.**

**My recommendation.** Move `BUFFER_DAYS` to a single constant in a shared `config.py` module. Set it to 120 to match the briefing. Both scripts import from there. This is a 30-minute fix that prevents real money mistakes.

**Confidence:** High. I read the code; the values are what I report.

---

### R2. ShipBob gate is double-implemented ⚠️ MEDIUM

**What I found.** The Shopify-reserve-before-Amazon gate exists in **two places** in `build_report.py`:

- **Lines 7044-7095** (`SHOPIFY_SAFETY_DAYS = 30`) — used inside the Replenishment Triggers logic
- **Lines 8088-8120** (`SHOPIFY_PROTECTION_DAYS = 30`) — used to override the `shipbob_emergency` field on every Amazon item

Both apply the same 30-day rule. Both use Valogix SBGA-MT + SBGA-SS daily velocity. Both work today. But they're separate code paths with separate constant names, so a future change to one won't update the other.

**Why it matters.** This is the textbook "drift waiting to happen." If you decide next quarter to bump Shopify reserve to 45 days, you'll change one of them and forget the other. The system will silently produce inconsistent results between the Amazon tab's `SB AVAILABLE (NET)` column and the Replenishment Triggers tab.

**My recommendation.** Consolidate into a single function:
```python
def compute_shopify_reserve(upc, shopify_vel_by_upc, days=30):
    shop_vel = shopify_vel_by_upc.get(upc, 0)
    return round(shop_vel * days)
```
Call it from both locations. Single source of truth. Same fix pattern as R1.

**Confidence:** High. I read both blocks of code; they are functionally identical with cosmetic differences.

**Note to you:** This is also why I want you to read your own system regularly. The earlier-conversation request to "spec the ShipBob gate" was for something already built. Auditing periodically prevents that.

---

### R3. Status classification logic lives in five places ⚠️ MEDIUM

**What I found.** Confirmed by re-reading the code:

1. `demand_planning.py::urgency_tier()` — DOS-based with channel awareness
2. `build_report.py::recompute_amazon_status_with_inbound()` (line 1412) — the Seller Central reclassification
3. `build_report.py` Walmart NFMD block (~line 2535) — `<30 LOW`, `<60 LOW`, etc.
4. `build_report.py` Walmart SS block (~line 2696) — `<60 LOW`
5. `build_report.py` general non-Amazon block (~line 2798) — `<60 LOW`

The Walmart NFMD block uses two different thresholds in the same block: "< 30 → LOW" and "< 60 → LOW". That's not a typo — both map to the same label, which means the 30-day threshold does nothing. Either the original author meant to use "CRITICAL" for the first one, or one of them is dead code.

**Why it matters.** When a status looks wrong, you have 5 places to debug. Worse: when you want to change a rule (e.g., "let's call <14 days CRITICAL on Amazon"), you have to find all 5 places and edit each. Some will get missed. Bugs will appear weeks later.

**My recommendation.** Create `scripts/classify.py` with one function:
```python
def classify_status(channel, on_hand, in_pipeline, daily_vel, lead_time, has_open_po):
    """Single source of truth for status. Returns (status, tier, color)."""
    # All rules in one place
```

Replace the 5 inline implementations with calls to this function. Before deploying, run last week's data through both old and new code; confirm no item's status changes unexpectedly. Estimated effort: 1 day.

**Confidence:** High on the duplication. Medium on whether all 5 produce identical results today — they probably don't, but I haven't run side-by-side comparison.

---

### R4. SoStocked column-rename fragility is real and unaddressed ⚠️ MEDIUM

**What I found.** Your `demand_planning.py` line 236 has this comment:
```python
# SoStocked has used multiple naming conventions over time — accept any
# that match. NEW format ("FBA Available", "3PL: Amazon AWD") replaced
# OLD format ("FBA Stock / Market or Region", "Total Warehouse Stock")
# in early 2026.
num_col_aliases = {
    "fba_market":  ["FBA Available", "FBA Stock / Market or Region", "FBA Stock"],
    "wh_stock":    ["3PL: Amazon AWD", "Amazon AWD", ...],
    ...
}
```

You're already defending against this — that's good. **But the defense is incomplete.** If SoStocked renames `Adj. Velocity` to `Adjusted Velocity`, your script fills that column with 0 silently and produces wrong DOS calculations for every Amazon item. There's no validation, no error — just bad data.

**Why it matters.** SoStocked has renamed columns multiple times. Your code captured the renames after-the-fact. The next rename will happen during a busy week and you'll catch it three days later after a stockout.

**My recommendation.** Add column-validation guards at the top of every load function:
```python
REQUIRED_INV_COLS = {"Marketplace", "ASIN"}  # absolutely required
EXPECTED_NUMERIC_COLS = ["Adj. Velocity", "FBA Available", ...]
missing_required = REQUIRED_INV_COLS - set(df.columns)
if missing_required:
    raise SystemExit(f"❌ SoStocked Inv. {brand}: missing required columns {missing_required}")
missing_numeric = [c for c in EXPECTED_NUMERIC_COLS if c not in df.columns]
if missing_numeric:
    print(f"⚠️ SoStocked Inv. {brand}: missing numeric columns {missing_numeric} — filling 0")
```

The warning at least makes the silent failure loud. The error stops the run when something critical is gone. Effort: 2-3 hours across all loaders.

**Confidence:** High. The alias dict exists; the validation does not.

---

### R5. Two parallel pipelines, one is dead ⚠️ LOW (operational), HIGH (cleanliness)

**What I found.** Confirmed: the orchestrator `run_weekly_supply_chain_analysis.py` describes a 4-step workflow involving `preprocess_run.py` and manual Claude agents that **does not match what the skill executes.** Your actual Monday pipeline is the 3-script flow: `combine_forecast → demand_planning → build_report`.

**Dead/obsolete candidates** (the full cleanup plan is in **Section 5B**, below):
- `run_weekly_supply_chain_analysis.py` (222 lines) — orchestrates a workflow you don't use
- `preprocess_run.py` (561 lines) — feeds the dead orchestrator
- `analyze_sostocked.py` (426 lines) — predecessor of `combine_forecast.py`
- `generate_weekly_excel.py` (1,867 lines) — produces a *different* weekly file (`MTB_Weekly_WorkingFile.xlsx`) that I do not see in your outputs. May be dead.
- `build_marketplace_reviews.py` (254 lines) — single-file predecessor of the combined version
- `build_wm_marketplace_review.py` (232 lines) — Walmart-only subset of the combined script
- `one_off_check_walmart_exclusive_skus.py` (215 lines) — diagnostic, hardcoded UPC list
- `one_off_e_inventory_report.py` (221 lines) — one-shot E-class snapshot

**Why it matters.** New planners (human or AI) reading the codebase will assume these scripts matter. They'll waste hours trying to understand them, will hesitate to delete them ("what if it's important?"), and will design around them unnecessarily. Worse, an agent like Claudian may accidentally execute an obsolete script and produce confusing or stale output.

**My recommendation.** Archive to `scripts/_archive/` — don't delete. Cost of being wrong: zero (restore is a file move). Cost of leaving them: ongoing confusion. See **Section 5B** for the full step-by-step plan with safety net.

**Confidence:** High on six of eight candidates. Medium on `generate_weekly_excel.py` (verify first — see Section 5B's verification step). Medium on `build_marketplace_reviews.py` (very close to the combined version, but cosmetic differences exist).

---

### R6. Hardcoded personal paths in 8+ files

**What I found.** Searched all 19 scripts:
```
analyze_sostocked.py:    C:\Users\Tom Sapia\supplychainbrain\...
demand_planning.py:      C:\Users\Tom Sapia\supplychainbrain\...
generate_weekly_excel.py: C:\Users\Tom Sapia\OneDrive...
one_off_valogix_forecast_variance.py: C:\Users\Tom Sapia\Downloads\...
package_for_handoff.py:  C:\Users\Tom Sapia\...
CLAUDE_BRIEFING.md:      C:\Users\Tom Sapia\MTB-SupplyChain\
README.md:               cd C:\Users\Tom Sapia\MTB-SupplyChain
```

Plus the skill file references the path.

**Why it matters.** You said earlier in our conversation that you wanted this system transferable. With hardcoded usernames, it isn't. A new team member's machine will fail at multiple points until they grep-replace your name out of the codebase.

**My recommendation.** Create `scripts/config.py`:
```python
import os
BASE = os.environ.get("MTB_BASE",
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VAULT = os.environ.get("MTB_VAULT_PATH", "")  # blank = no vault publishing
SHAREPOINT = os.environ.get("MTB_SHAREPOINT_DIR", "")
```

Set env vars on your machine. Future planners set their own. Effort: 1 hour for the configuration, 30 minutes to grep-replace.

**Confidence:** High. Direct grep findings.

---

### R7. Documentation drift across four docs

**What I found.**

| Doc | Lead time floor | Lead time mentioned how |
|---|---|---|
| `CLAUDE_BRIEFING.md` | 120 days | "Supplier lead time floor 120 days" |
| `Weekly Inputs Sourcing SOP.md` | 150 days | "150-day door-to-door" |
| `build_report.py` line 41 | 120 days | `SUPPLIER_LEAD_TIME_FLOOR = 120` |
| `build_report.py` line 324 (comment) | 150 days | "Default supplier lead-time floor is 150 days" |

**Two of your docs say 150, two say 120, and one Python file contradicts itself in code and comment.** The code value (120) is what actually runs. Everything else is misleading.

**Why it matters.** When you onboard a new planner, they'll read the SOPs first. They'll learn the wrong number. They'll question recommendations the system makes because "shouldn't this be 150-day buffer?" Confusion compounds.

**My recommendation.** Pick a number. Update all four sources. Don't worry about the comments in code (just delete or fix them) but do worry about the SOPs that your team and AI references.

**Confidence:** High.

---

### R8. Override registries are healthy

**What I found.** Briefly worth noting what's *working*. Your override registries — `AMAZON_SKU_ALIAS`, `AWD_INELIGIBLE_ITEMS`, `LEAD_TIME_OVERRIDE`, `ABC_OVERRIDE`, `UPC_PARENT_FOR_METADATA` — are clean. Small. Commented. Documented in the briefing. This is the pattern your whole system should follow.

The fact that you can hot-fix a SKU misclassification by adding one line to `ABC_OVERRIDE` is *exactly* how internal tools should work. Keep this pattern. Apply it to the new `SHOPIFY_RESERVE_OVERRIDE` if you ever need per-SKU gate overrides.

**This is positive feedback. Save it.**

---

## Section 2 — Simplification opportunities

### S1. `build_report.py` is 8,554 lines — but don't refactor it

**What I found.** 145 functions in one file. Most of them are tied together by shared state and helper functions. The code works.

**My recommendation.** **Do not break this up.** Refactoring monoliths is high-risk, low-immediate-value work. Every refactor introduces bugs. Every bug in a weekly pipeline costs you a Monday. The only time to break up a monolith is when you can't *change* it anymore — and you can still change yours.

If you ever do refactor: extract loaders first (they're self-contained), then writers (also self-contained). Leave the enrichment chain alone — that's where coupling is highest.

**Confidence:** High. This is my professional recommendation from 40 years of watching teams refactor things that didn't need it.

---

### S2. The two marketplace review scripts are redundant

**What I found.**
- `build_marketplace_reviews.py` (254 lines) — outputs 4 separate Excel files, one per channel
- `build_marketplace_reviews_combined.py` (327 lines) — outputs one workbook with 4 tabs + a README

The combined one is strictly better: same data, easier to send around, has a README, includes channel summaries. The separate version is the predecessor.

**My recommendation.** Archive `build_marketplace_reviews.py`. Keep the combined one. If you don't already, link the combined output from your CLAUDE_BRIEFING.md as the "send to leadership monthly" deliverable. Also archive `build_wm_marketplace_review.py` — it's a Walmart-only subset of the combined output.

**Confidence:** High. Read both files; they're substantially the same.

---

### S3. The skill is in good shape — keep it close to as-is

**What I found.** The `WEEKLY_ANALYSIS_SKILL.md` you just shared is genuinely well-written. It has:
- A pre-flight check script with explicit pass/fail signals
- The exact run order (3 required, 4 optional)
- Expected console output for each step (so anomalies are visible)
- A clear "stop and ask Tommy" escalation list
- Common errors + fixes

This is *better* than 90% of what I see in internal tools. Don't tear it apart.

**Minor cleanups I'd recommend:**

1. The pre-flight check is correct but inline-Python in PowerShell is fragile. **Move it to `scripts/preflight_check.py`** and have the skill call `python scripts/preflight_check.py`. Same logic, easier to maintain, can be reused outside Claudian.
2. The "Locked-in constants" section in the skill should reference the briefing doc rather than duplicate values (which would drift). Say "see CLAUDE_BRIEFING.md → Critical business rules" rather than listing them again here. **This is the same drift problem as R7 — the skill itself can become a fifth source of truth that disagrees with the others.**
3. Add a section: "If output looks wrong, here are the 3 most likely causes." (Brand misroute / column rename / SAP item master stale.)

**Confidence:** High on the skill being good. The minor improvements are professional polish, not fixes.

---

### S4. Several one-off scripts that ran once

**What I found.**
- `one_off_check_walmart_exclusive_skus.py` — diagnostic script with a hardcoded list of 53 UPCs
- `one_off_e_inventory_report.py` — produces a one-shot E-class inventory snapshot
- `one_off_valogix_forecast_variance.py` — the heavy 1,176-line variance report (called by the skill, *not* a one-off despite the name)

**My recommendation.**
- The first two: move to `scripts/_archive/` unless you'll run them again
- The variance one: **rename** it to drop "one_off_" — it's a regular weekly script, the filename is lying. Maybe `build_valogix_variance.py`.

**Confidence:** Medium. The first two might still be referenced; verify before archiving. The rename of the variance one is unambiguous.

---

## Section 3 — Gap findings (things to add)

### G1. PO actual lead-time tracking — closes a critical loop ⭐ HIGH VALUE

**What I found.** You have `build_po_lead_time_audit.py` that compares posting date to expected due date for **open** POs. You don't track **actual** lead times once POs are received. So the 120-day floor stays a guess. Vendor scorecards stay subjective.

**Why this matters.** Vendor performance is the single most leveraged signal in your supply chain. A vendor consistently delivering at 145 days when they promised 120 should be penalized in the model — and you should know it before it surprises you next quarter. Right now you don't have the data.

**My recommendation (the spec).** Add a closing-PO log:
1. When a SAP PO transitions to closed status, log: `{po_no, vendor, upc, qty, posted_date, due_date, received_date, actual_lead_time_days}`
2. Build a `📊 Vendor Performance` tab in the weekly workbook:
   - Vendor × trailing-6mo average actual lead time
   - Vendor × on-time delivery % (within ±7 days of promise)
   - Vendor × forecast accuracy on their items
3. After 6 months of data, replace the global 120-day floor with **per-vendor actual lead times**. Bad vendors get longer buffers automatically.

**Effort:** 2 weeks for v1. **Impact:** the difference between a reporting tool and a learning system.

---

### G2. Forecast accuracy feedback loop ⭐ HIGH VALUE

**What I found.** Your `📈 Amazon FvA` tab shows 366 records, 282 flagged variance >30%. That data sits there. It does not feed back into:
- Next week's PO sizing (could add a "your forecast for this SKU has been off by 40% — consider buffer adjustment")
- Velocity calculations (could weight historical velocity higher for SKUs where the forecast is unreliable)
- Priority Actions (could flag "forecast risk" alongside "stockout risk")

**My recommendation.** Add a `📊 Forecast Risk` tab that:
1. For every SKU, computes 6-month rolling MAPE (mean absolute percentage error)
2. Buckets SKUs into FORECAST-TRUSTED / NEEDS-WATCH / UNRELIABLE
3. Annotates the existing Priority Actions tab with a "Forecast Trust" column

For unreliable SKUs, suggest a buffer bump (e.g., +20% PO quantity) or recommend manual review. This is *not* automatic — it's a signal. The planner still decides.

**Effort:** 1 week. **Impact:** Catches the 282 currently-unaddressed variance flags before they become stockouts or overstocks.

---

### G3. Container booking memory (or "in-flight reservations") ⭐ MEDIUM VALUE

**What I found.** Your container loading priority script tells the supplier what to manufacture first. But the system has no memory of *what's been booked into the next container*. If you tell the supplier to make 6,600 units of UPC X next week, your system doesn't know that — so next Monday it might recommend the same 6,600 units again.

**Why this matters.** Container planning happens between Mondays. The system snapshots state weekly but doesn't track decisions made between snapshots. Result: planners have to keep manual notes ("we already booked X").

**My recommendation.** Add a lightweight `pending_bookings.csv` file in the repo. After a container is booked, add rows: `{date, upc, qty, container_eta}`. The `build_container_loading_priority.py` script reads this file and excludes booked-qty from "what to manufacture next."

**Effort:** 1-2 days. **Impact:** Removes one entire class of "but didn't we already do this?" confusion.

---

### G4. Per-channel velocity decomposition

**What I found.** When you look at a SKU's "Adj. Velocity" today, it's a blended number across all marketplaces where it sells. The system computes per-channel velocity in some places but uses blended in others. This makes channel-specific decisions noisier than they need to be.

**My recommendation.** In the next iteration of the multi-channel tab, add columns: `Amzn US vel`, `Amzn CA vel`, `Shopify vel`, `Walmart vel`, `Floship vel`. Most are already computed internally — they're just not exposed.

**Effort:** 2-3 days. **Impact:** Better channel-specific decisions, especially for the "should we rebalance from Shopify to Amazon?" question.

---

### G5. Weekly run log — a Monday-after-Monday history

**What I found.** Today, the `outputs/YYYY-MM-DD/` folder stores each week's deliverables. There's no consolidated log that lets you compare "what did the system recommend last week vs this week."

**My recommendation.** Append one row per Monday run to `outputs/run_log.csv`:
```
{run_date, total_priority_items, emergency_count, order_now_count,
 total_po_value_recommended, total_units_recommended,
 tabs_with_errors, runtime_minutes}
```

Then a 1-page weekly trend chart shows: are priorities trending up? Are we ordering more or less? Did this Monday's run take 4× longer than usual (a sign of a data issue)?

**Effort:** Half a day. **Impact:** Trend awareness. Catches drift you'd otherwise miss.

---

## Section 4 — What I'd skip (and why)

These are things that might *seem* worth doing but I'd defer or skip entirely:

- **Don't refactor `build_report.py` into modules.** Already covered in S1. Too risky for the value.
- **Don't try to automate the manual file gathering.** Each source (SoStocked, Amazon, Walmart, ShipBob, Floship, Valogix) has its own auth, UI, and download flow. Five-minute manual download is the right tradeoff. Automating it costs weeks and breaks every time a vendor changes their UI.
- **Don't build a web UI on top of this.** Excel is the right delivery format for this audience. You don't have time to maintain a web app.
- **Don't try to integrate this directly with SAP.** SAP integrations are a multi-month project for one connection. Your file-based pipeline is dramatically faster to maintain.
- **Don't migrate to a "real" forecasting library** (Prophet, statsmodels, etc.) unless you have evidence the current forecasts are bad. They probably aren't great, but adding ML complexity without measuring current accuracy first is the classic mistake.

---

## Section 5 — The reliability summary

**Is the system reliable today?** Yes, for current usage. It produces correct outputs most Mondays. The reclassification logic is sound. The override registries are clean. The skill provides a stable execution path.

**Where will it break first?**
1. SoStocked column rename → silent bad data (R4)
2. Buffer-days mismatch → wrong PO quantities on the Action Plan (R1)
3. A documentation drift → a new planner makes a wrong decision based on the SOP (R7)

**What's the worst-case failure mode?** A SoStocked column gets renamed during a busy week. The script silently fills the column with zeros. DOS calculations come out wrong for half the catalog. The Action Plan recommends emergency send-ins for items that have plenty of stock. By Wednesday someone notices the numbers don't match Seller Central. You spend Thursday debugging.

**The fix that prevents that scenario specifically is R4** — column validation guards. That's why R4 ranks above its raw severity might suggest.

---

## Section 5B — Codebase cleanup plan (obsolete script archive)

This section operationalizes R5. It is a standalone work item — read it as instructions, not analysis.

### Why this matters in plain English

Every obsolete file in your codebase is a tax. Four reasons:

1. **Cognitive tax on you.** When you open `scripts/` next month and see 19 files, you have to remember which are live. Mental overhead every time.
2. **Confusion tax on Claudian.** When you ask Claudian to "fix X," it may modify a file that doesn't actually run. You won't see any effect on Monday's output and you'll waste hours debugging.
3. **Onboarding tax on the next planner.** A new team member reads obsolete files and assumes they matter. They design around them. They hesitate to delete because "what if it's important?" — and the system grows another generation of dead code.
4. **Real risk.** If you (or Claudian, or a future agent) accidentally run an obsolete script, it might overwrite a current output file with wrong data, read from a folder that was renamed, or write to a hardcoded path on a machine that doesn't have that user.

### Why this needs to be done carefully

The instinct is "delete it all, we can always restore from git." Two problems:

1. **Git history may not cover all of it.** I don't know whether this repo is in version control. If not, "restore later" doesn't work.
2. **Obsolete looks different from unused.** A script that looks dead might run quarterly, be called by another script you haven't traced, or be the backup if the live one breaks.

The plan below uses a 30-day safety net so nothing actually gets deleted until it has been proven dead.

### The three-step cleanup

**Step 1 — Archive, don't delete (Day 1, ~30 minutes)**

Create `scripts/_archive/` and move suspected-dead files there, one-line note per file. Nothing gets deleted. If something breaks, you just move the file back.

**The 8 archive candidates:**

| # | File | Reason | Risk if wrong |
|---|---|---|---|
| 1 | `run_weekly_supply_chain_analysis.py` | Describes a 4-step workflow the skill doesn't use | Low — skill doesn't call it |
| 2 | `preprocess_run.py` | Feeds the orchestrator above | Low — same chain |
| 3 | `analyze_sostocked.py` | Predecessor to `combine_forecast.py` | Low — confirmed superseded |
| 4 | `generate_weekly_excel.py` | Produces `MTB_Weekly_WorkingFile.xlsx`, not in your outputs | **Medium — verify first** |
| 5 | `build_marketplace_reviews.py` | Single-file version superseded by combined | Low |
| 6 | `build_wm_marketplace_review.py` | Walmart-only subset of combined script | Low |
| 7 | `one_off_check_walmart_exclusive_skus.py` | Diagnostic, hardcoded UPC list | Low — clearly named "one_off" |
| 8 | `one_off_e_inventory_report.py` | One-shot E-class snapshot | Low — clearly named "one_off" |

That's 8 of 19 files moved. Your `scripts/` directory drops to 11 active files — meaningfully cleaner.

**Pre-archive verification for `generate_weekly_excel.py`:**
Before archiving, search the vault and SOPs for the string "MTB_Weekly_WorkingFile" — if any doc references that filename, the script is still alive. If no doc references it, archive it.

```bash
# From the vault root:
grep -r "MTB_Weekly_WorkingFile" .
```

**Create the archive README:**
Inside `scripts/_archive/`, add a file `README.md` with one line per archived script. Format:

```
# Archived Scripts

Files here were moved out of active rotation on 2026-05-20 per the audit's
R5/Section 5B cleanup plan. Restore by moving back to scripts/ if needed.

- run_weekly_supply_chain_analysis.py — dead orchestrator (replaced by 3-script skill flow)
- preprocess_run.py — fed the dead orchestrator above
- analyze_sostocked.py — predecessor to combine_forecast.py
- generate_weekly_excel.py — produces MTB_Weekly_WorkingFile.xlsx (not in active outputs)
- build_marketplace_reviews.py — single-file predecessor, superseded by combined version
- build_wm_marketplace_review.py — Walmart-only subset of combined script
- one_off_check_walmart_exclusive_skus.py — one-shot diagnostic with hardcoded UPCs
- one_off_e_inventory_report.py — one-shot E-class inventory snapshot
```

**Step 2 — Watch for 30 days (passive)**

For the next 4 Mondays, run your normal pipeline. If nothing breaks and nothing feels missing, the archives were correctly archived.

What to watch for:
- Any script that fails because it can't import from an archived file → restore that file
- Any output file that's missing compared to last week → check if an archived script was generating it
- Any Claudian instruction that references one of the archived script names → either restore or update the instruction

**Step 3 — Delete or relocate after 30 days (Day 31, ~5 minutes)**

If 30 days pass with no issues:
- **Option A:** Delete `scripts/_archive/` entirely. Cleanest end state.
- **Option B:** Zip `scripts/_archive/` and move the zip outside the repo (e.g., to a "Reference / Legacy Code" folder in your vault). Same effect, keeps the artifact for nostalgia.

### How to hand this off to Claudian

A safe, scoped Claudian instruction:

```
Move these 8 files into scripts/_archive/, preserving them exactly:
  run_weekly_supply_chain_analysis.py
  preprocess_run.py
  analyze_sostocked.py
  generate_weekly_excel.py
  build_marketplace_reviews.py
  build_wm_marketplace_review.py
  one_off_check_walmart_exclusive_skus.py
  one_off_e_inventory_report.py

Then create scripts/_archive/README.md with the contents specified in the audit
Section 5B. Do not delete anything. Do not modify any other file. Do not modify
the active scripts in scripts/.

After completing the moves, run:
  python scripts/combine_forecast.py
  python scripts/demand_planning.py
  python scripts/build_report.py

If any of those fail with an ImportError or similar referencing an archived
file, immediately move that file back to scripts/ and report which one.
```

This instruction is scoped, reversible, and includes a built-in smoke test.

### What NOT to do

- **Don't have Claudian "find all dead code"** — it will over-archive. It can read code but not context.
- **Don't have Claudian delete files** in this task — moves only. Reversibility matters.
- **Don't have Claudian modify active scripts in the same session** — one change at a time. If you also want it to apply the buffer fix or lead time change, do those separately.
- **Don't skip the 30-day watch period.** Archiving without watching is just delayed deletion.

### What to track during the 30 days

Add a row to a running log each Monday:

| Week | Pipeline ran clean? | Anything missing in output? | Notes |
|---|---|---|---|
| 1 (5/26) | Y/N | Y/N | |
| 2 (6/2) | Y/N | Y/N | |
| 3 (6/9) | Y/N | Y/N | |
| 4 (6/16) | Y/N | Y/N | |

Four clean weeks → safe to delete the archive. Anything funky → investigate before deleting.

---

## Section 6 — Prioritized action list

Ranked by ratio of impact to effort. Each item is independently shippable.

| # | Item | Effort | Impact | Notes |
|---|---|---|---|---|
| 1 | **R7 — Reconcile lead-time floor to 120 in all 4 docs** | 30 min | High | Stops the "is it 120 or 150?" confusion forever |
| 2 | **R1 — Fix buffer-days mismatch (60 vs 120)** | 1 hour | High | Real PO sizing bug today |
| 3 | **R6 — Strip hardcoded paths, add `config.py`** | 1 hour | High | Makes system transferable |
| 4 | **R5 — Archive 8 dead scripts to `_archive/`** | 30 min + 30 day watch | High (clarity) | **Full plan in Section 5B.** Reversible. Stop confusing future readers. |
| 5 | **R4 — Column-validation guards on SoStocked loaders** | 3 hours | High | Prevents silent failures |
| 6 | **R2 — Consolidate ShipBob gate to single function** | 2 hours | Medium | Prevents future drift |
| 7 | **S3 — Move pre-flight script out of skill into `.py`** | 1 hour | Medium | Cleaner skill, reusable script |
| 8 | **R3 — Consolidate status classification to one module** | 1 day | Medium | Larger refactor; do this once everything above is done |
| 9 | **G2 — Forecast accuracy feedback loop** | 1 week | Game-changing | The biggest move — but do reliability first |
| 10 | **G1 — Per-vendor actual lead time tracking** | 2 weeks | Game-changing | Same priority as G2; pick one to do first |

**What I'd do this week:** items 1-5. That's 5-6 hours total. By Friday you'd have:
- One consistent lead-time floor across all 4 docs
- One consistent buffer across both scripts
- A system that runs on any machine without grep-replace
- A cleaner codebase with dead scripts archived
- Loud-failing column validation that catches the next SoStocked rename

**Then:** items 6-7 the following week (3 hours total).

**Then:** item 8 in week 3 (the bigger refactor).

**Then:** pick G1 or G2 as the strategic project for the next quarter.

---

## Section 7 — What I'm uncertain about

Honesty about limitations of this audit:

1. **I haven't run your code.** I read it carefully but I haven't executed a Monday run and watched the output. There could be runtime issues I missed.
2. **I don't know if `generate_weekly_excel.py` is alive or dead.** It produces a different output file (`MTB_Weekly_WorkingFile.xlsx`) that I don't see in your samples. Verify before archiving.
3. **The 5-place status classification finding** is correct on duplication, but I haven't proven they produce *different* outputs today. They might agree on every SKU by coincidence. Compare last week's outputs before refactoring.
4. **I'm guessing about your team size and cadence.** If you have a deputy planner running this when you're out, my "transferability" recommendations matter more. If you're a one-person show, they matter less.
5. **The G1 and G2 effort estimates are mine** based on what I see in your code. A real implementation could go 2× faster or slower depending on edge cases.

If any of these matter, push back and we'll get more specific.

---

*End of audit. Save this. Reference it weekly. Update it next quarter — systems drift, audits should refresh.*
