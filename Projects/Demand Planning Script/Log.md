# Log — Demand Planning Script

---

## 2026-04-20 — Critical velocity bug fixed

**Who:** Tommy
**What happened:** Discovered SoStocked exports velocity in units/day, not monthly totals. Script was dividing by 30, making every DOS calculation 30× too optimistic.
**Decision / outcome:** Removed ÷30. Added Adj. Velocity as primary (corrects for stockout suppression). Added 0.1/day inactive threshold.
**Next step:** Fix HIGH tier bug — 13 items missing from output.

---

## 2026-04-16 — Script built and first report generated

**Who:** Tommy
**What happened:** demand_planning.py built from scratch. Reads SoStocked Multi-Dashboard + Inventory Export. Outputs Excel with 5 sheets.
**Decision / outcome:** Script runs clean. First report: demand-plan-2026-04-16.xlsx.
**Next step:** Velocity bug fix (completed Apr 20).

---
