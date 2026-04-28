# Demand Planning Script (demand_planning.py)
**Owner:** Tommy Sapia
**Status:** In Progress
**Started:** April 16, 2026
**Target completion:** Ongoing — weekly tool
**Priority:** High

---

## What we're doing and why

Building and maintaining a Python script that automates weekly demand planning across all 3 brands. Replaces manual Excel analysis with a repeatable, scriptable process that outputs a priority action list every Monday.

---

## Who owns what

| Person | Role / Responsibility |
|--------|----------------------|
| Tommy | Script development, weekly execution, output review |

---

## Definition of done

- [ ] HIGH tier items appear correctly in output (currently 13 missing)
- [ ] Inbound FBA bug fixed (46,129 unit bleed removed from PO formula)
- [ ] Cost/unit populated in output (currently blank)
- [ ] SS lead times fix verified
- [ ] Script runs end-to-end on Windows machine without errors
- [ ] Weekly cadence established and documented in Demand Planning SOP

---

## Open questions / blockers

- Is the 46,129 inbound a real PO in SAP? Must verify before removing from formula.
- HIGH tier: why are 13 items not appearing? Bug in tier logic or data issue?

---

## Links

- [[06 Processes & SOPs/(C) Demand Planning SOP]]
- Script: `C:\Users\Tom Sapia\MTB-SupplyChain\demand_planning.py`
- Output: `C:\Users\Tom Sapia\MTB-SupplyChain\outputs\`
- [[07 AI Tools & Builds/(C) Demand Planning Report — Build Plan]]
