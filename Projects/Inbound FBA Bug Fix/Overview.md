# Inbound FBA Bug Fix
**Owner:** Tommy Sapia
**Status:** Pending — needs SAP verification first
**Started:** April 20, 2026
**Target completion:** ASAP — blocking ~10 CRITICAL items
**Priority:** High

---

## What we're doing and why

SoStocked is showing 46,129 units as inbound to FBA across many MTB products. This appears to be an aggregate data bleed, not real inventory. Because the script includes inbound_fba in the available stock calculation, PO quantity = 0 for ~10 CRITICAL items that actually need orders placed.

Before removing the inbound count from the formula, we need to verify in SAP whether there is a real large MTB shipment in transit.

---

## Who owns what

| Person | Role / Responsibility |
|--------|----------------------|
| Tommy | SAP verification, script fix |

---

## Definition of done

- [ ] SAP checked for large MTB inbound shipment (~46,129 units)
- [ ] Determination made: real shipment or data bleed
- [ ] If data bleed: inbound_fba removed from PO formula in demand_planning.py
- [ ] If real shipment: documented and factored into demand plan correctly
- [ ] Re-run demand plan to confirm correct PO quantities for affected CRITICAL items

---

## Open questions / blockers

- **Blocker:** Must verify in SAP before changing formula. Removing real inventory from the calculation would cause over-ordering.

---

## Links

- [[06 Processes & SOPs/(C) Demand Planning SOP]]
- Script: `C:\Users\Tom Sapia\MTB-SupplyChain\demand_planning.py`
