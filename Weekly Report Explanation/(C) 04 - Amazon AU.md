# Tab 4 — Amazon AU

**Purpose:** International placeholder — surfaces SAP supplier POs routed to Australia warehouse (`AMZ-MT-AU` / `AMZ-SS-AU`). Same structure as Amazon UK ([[(C) 03 - Amazon UK]]).

---

## What's Populated

| Column | Source |
|---|---|
| **BRAND** | SAP routing (`AMZ-MT-AU` → MTB, `AMZ-SS-AU` → SS) |
| **PRODUCT** | SAP item description |
| **SAP UPC** | SAP item number |
| **OPEN PO (SUPPLIER)** | `reports/_data/sap-open-pos/*.xlsx` — sum of open units for this UPC × AU |
| **PO ARRIVES ON** | Earliest SAP PO due date |

Everything else blank — no AU velocity / FBA / forecast sources yet.

---

## When This Tab Will Get Real Data

Same path as UK — see [[(C) 03 - Amazon UK]] notes. Need SC AU exports + SoStocked AU marketplace + AU FBA/AWD loaders.
