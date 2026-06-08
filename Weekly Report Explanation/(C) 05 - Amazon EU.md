# Tab 5 — Amazon EU

**Purpose:** International placeholder — surfaces SAP supplier POs routed to EU warehouses (`AMZ-MT-EU` / `AMZ-SS-EU`). Same structure as Amazon UK ([[(C) 03 - Amazon UK]]).

---

## What's Populated

| Column | Source |
|---|---|
| **BRAND** | SAP routing |
| **PRODUCT** | SAP item description |
| **SAP UPC** | SAP item number |
| **OPEN PO (SUPPLIER)** | Open SAP PO units for this UPC × EU warehouses |
| **PO ARRIVES ON** | Earliest SAP PO due date |

Everything else blank.

---

## When This Tab Will Get Real Data

Same path as UK — see [[(C) 03 - Amazon UK]]. EU Amazon is more complex because it spans 5+ marketplaces (DE, FR, IT, ES, NL) — when activated, the routing logic in `SAP_WH_TO_CHANNEL` may need to split by country.
