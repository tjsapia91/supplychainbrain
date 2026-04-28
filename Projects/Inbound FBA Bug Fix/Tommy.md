# Tommy — Inbound FBA Bug Fix
**Last updated:** April 20, 2026

---

## My tasks

- [ ] Open SAP — check open POs for MTB — look for any shipment ~46,129 units inbound
- [ ] If no real shipment found: remove inbound_fba from PO formula in demand_planning.py
- [ ] Re-run demand plan after fix
- [ ] Document outcome in Log.md

---

## In progress

Pending SAP check.

---

## Completed

- ✅ Bug identified April 20 — root cause: SoStocked aggregate bleed

---

## Notes

Affected items are CRITICAL — this is the highest-priority script fix. The ~10 items with 0 PO qty are likely real reorder needs being masked.
