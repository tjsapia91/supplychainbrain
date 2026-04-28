# Tommy — HIGH Tier Fix
**Last updated:** April 20, 2026

---

## My tasks

- [ ] Open demand_planning.py — review HIGH tier logic (DOS ≤ lead_time + 30)
- [ ] Pull the 13 missing items from the raw SoStocked export — do they have velocity data?
- [ ] Check if items are being filtered out before tier assignment (inactive threshold, region filter, etc.)
- [ ] Apply fix and re-run
- [ ] Confirm Blade Refills (236/day) and Hair Spray (143/day) appear in output

---

## In progress

Not yet started. Priority: fix before April 27 demand plan run.

---

## Completed

- ✅ Bug identified April 20

---

## Notes

**Urgency:** Blade Refills at 236 units/day and Hair Spray at 143 units/day are the two highest-velocity items affected. If they flip to CRITICAL and are still missing from output, we will miss the PO window entirely.
