# SoStocked Regional Groupings Cleanup
**Owner:** Tommy Sapia
**Status:** In Progress
**Started:** April 2026
**Target completion:** TBD
**Priority:** Medium

---

## What we're doing and why

SoStocked has 22 regional grouping issues — MX rows still present, NAm/US+MX inconsistent naming. These create noise in every demand planning run and can cause incorrect DOS/PO calculations for affected SKUs.

---

## Who owns what

| Person | Role / Responsibility |
|--------|----------------------|
| Tommy | Identify all 22 issues, fix in SoStocked settings |

---

## Definition of done

- [ ] All 22 flagged grouping issues resolved in SoStocked
- [ ] MX rows removed or properly tagged
- [ ] NAm → US and US+MX → US applied consistently
- [ ] demand_planning.py runs with zero grouping warnings

---

## Open questions / blockers

- Need SoStocked admin access to update grouping settings
- Some CA listings may be dead (CIRRA, NERA) — verify before cleaning

---

## Links

- [[06 Processes & SOPs/(C) Demand Planning SOP]]
- Script output flags groupings: `analyze_sostocked.py`
