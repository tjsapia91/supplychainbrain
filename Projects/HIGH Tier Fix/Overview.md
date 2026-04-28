# HIGH Tier Fix — demand_planning.py
**Owner:** Tommy Sapia
**Status:** Pending
**Started:** April 20, 2026
**Target completion:** Before next demand plan run (April 27)
**Priority:** High

---

## What we're doing and why

13 items are not appearing in the demand planning output at all. Two of the missing items — Blade Refills (236 units/day) and Hair Spray (143 units/day) — are 6-7 days away from flipping to CRITICAL. If they don't appear in the output, no PO gets flagged and we miss the reorder window.

---

## Who owns what

| Person | Role / Responsibility |
|--------|----------------------|
| Tommy | Debug tier logic in script, identify and fix root cause |

---

## Definition of done

- [ ] Root cause of missing HIGH items identified (tier logic bug vs. data issue)
- [ ] Fix applied to demand_planning.py
- [ ] All 13 missing items appear in correct tier on next run
- [ ] Blade Refills and Hair Spray verified in output before April 27 run

---

## Open questions / blockers

- Is this a tier logic bug in the script, or are these items missing from the source data?
- Do these items have correct velocity data in SoStocked export?

---

## Links

- [[06 Processes & SOPs/(C) Demand Planning SOP]]
- Script: `C:\Users\Tom Sapia\MTB-SupplyChain\demand_planning.py`
- [[Projects/Demand Planning Script/Overview]]
