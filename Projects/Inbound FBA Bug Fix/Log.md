# Log — Inbound FBA Bug Fix

---

## 2026-04-20 — Bug identified

**Who:** Tommy
**What happened:** demand_planning.py showing PO qty = 0 for ~10 CRITICAL MTB items. Root cause: SoStocked shows 46,129 units as inbound to FBA across many products (likely aggregate bleed from SoStocked data, not a real shipment).
**Decision / outcome:** Cannot remove from formula until SAP is checked. If it's a real shipment, it must stay in the calculation.
**Next step:** Check SAP for large MTB inbound PO.

---
