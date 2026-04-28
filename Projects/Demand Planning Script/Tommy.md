# Tommy — Demand Planning Script
**Last updated:** April 20, 2026

---

## My tasks

- [ ] Fix HIGH tier bug — 13 items missing from output
- [ ] Fix inbound FBA bleed (remove inbound_fba from PO formula after SAP verification)
- [ ] Verify SAP for large MTB inbound shipment (~46,129 units)
- [ ] Fix SS lead times (NaN in combined inventory file)
- [ ] Add cost/unit lookup (SoStocked product settings or SAP)
- [ ] Clean up SoStocked regional groupings (22 issues)

---

## In progress

Investigating HIGH tier missing items — Blade Refills (236/day) and Hair Spray (143/day) are 6-7 days from flipping CRITICAL.

---

## Completed

- ✅ Built demand_planning.py (April 16)
- ✅ Fixed velocity bug — SoStocked exports units/day, was being divided by 30 (April 20)
- ✅ Added Adj. Velocity as primary with 30-day fallback (April 20)
- ✅ Added INACTIVE_THRESHOLD (0.1/day) — low vel stockouts tracked separately (April 20)
- ✅ Generated demand-plan-2026-04-20.xlsx — 17 priority items

---

## Notes

Weekly cadence: run every Monday morning. Drop SoStocked files → run script → review Excel → update Home.md priorities table.
