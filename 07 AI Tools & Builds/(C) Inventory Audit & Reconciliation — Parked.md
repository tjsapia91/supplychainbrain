# (C) Inventory Audit & Reconciliation — Parked Build

> Cross-check what SAP says is in each warehouse against what the actual fulfillment centers (ShipBob, Floship, Amazon) report on hand. Surfaces data-integrity gaps and surfaces rebalancing opportunities — units sitting in the wrong warehouse for current demand.
>
> **Captured:** May 12, 2026
> **Status:** PARKED — input folder ready · awaiting SAP report sample + threshold rules
> **Trigger phrase to revisit:** *"Let's build the inventory audit report"*

---

## Why this exists

Today the weekly report shows inventory by channel using each channel's OWN source (Amazon Seller Central for FBA/AWD, ShipBob On Hand Summary for Shopify, etc.). But **SAP also tracks expected on-hand per warehouse** — and the two views often drift apart:

- Pick errors, lost shipments, mis-allocations
- ShipBob/Floship pick errors that haven't been reflected in SAP
- POs received in SAP but not yet physically counted at the 3PL
- Stock physically moved between FCs without SAP knowing

**The audit:** for each Item × Warehouse pair, compare SAP's expected qty vs the 3PL/Amazon's actual qty. Flag discrepancies. The output drives:

1. **Data corrections** — fix SAP entries to match physical reality
2. **3PL investigations** — when the actual count is far off SAP
3. **Rebalancing decisions** — when units are sitting in the "wrong" warehouse for current demand (e.g., 5,000 units at ShipBob-TX but velocity is all on the East Coast)

---

## Source: SAP "Inventory In Warehouse Report"

**Confirmed name (per Tommy, May 12 2026):** `Inventory In Warehouse Report`

**Pull steps** *(to be confirmed when first pulled)*:
1. SAP → Reports → Inventory → "Inventory In Warehouse Report"
2. Export full / all warehouses → `.xlsx`
3. Drop into `reports/sap-inventory/` (no renaming)

**Confirmed column structure** *(per Tommy screenshot, May 12 2026):*

| Column | Meaning |
|---|---|
| `Item No.` | UPC |
| `Item Description` | Product name |
| `Inventory` (e.g., "EA") | Unit type — each |
| `In Stock` | **Actual physical units at the warehouse** |
| `Committed` | Allocated to open orders, not yet shipped |
| `Ordered` | Open POs inbound to this warehouse |
| `Available` | `In Stock − Committed` (sellable / unallocated) |
| `Item Price` | Unit cost |
| `Total` | `In Stock × Item Price` (warehouse value) |
| `Confirmed` | Confirmation flag (TBD purpose) |

**Section-headed layout** — the report is NOT a flat table. Items are grouped by warehouse with header + subtotal rows interleaved:

```
Row 1:  [Item No., Item Description, Inventory, In Stock, Committed, ... (column headers)]
Row 2:  Whse: | AMZ-MTAU                                ← warehouse section header
Row 3:  [item row]
Row 4:  [item row]
...
Row N:  Total: AMZ-MTAU                                  ← subtotal row
Row N+1: Whse: | AMZ-MTEU                                ← next warehouse
Row N+2: [item rows for AMZ-MTEU]
...
```

**Parser logic:** scan row by row. When column A starts with "Whse:" → next column has warehouse code, save as current_wh. When column A starts with "Total:" → skip. Otherwise it's a data row — pair with current_wh.

**Warehouse codes seen (sample):**

| Code | Channel | Brand |
|---|---|---|
| `AMZ-MTAU` | Amazon Michael Todd | Australia |
| `AMZ-MTEU` | Amazon Michael Todd | Europe |
| `AMZ-MTUK` | Amazon Michael Todd | UK |
| `AMZ-NFAU` | Amazon NasalFresh MD | Australia |
| `AMZ-NFEU` | Amazon NasalFresh MD | Europe |
| `AMZ-NFUK` | Amazon NasalFresh MD | UK |
| `AMZN-MT` | Amazon US (supplier-side) | MTB |
| `AMZN-SS` | Amazon US (supplier-side) | SS/NFMD |
| `SBGA-MT` | Shopify MTB (ShipBob) | MTB |
| `SBGA-SS` | Shopify SS / NFMD (ShipBob) | SS/NFMD |
| `FLO-MTB` | Floship Intl | MTB |
| `WM-SS` | Walmart SS | SS |
| `OXYGENMT` / `OXYGENSS` | Oxygen Plant | MTB/SS |

---

## Cross-channel reconciliation map

| SAP Warehouse | Actual source (compare against) | Brand context |
|---|---|---|
| `SBGA-MT` | ShipBob MTB `On Hand Summary` | MTB |
| `SBGA-SS` | ShipBob SS + NFMD On Hand Summary (combined) | SS + NFMD |
| `FLO-MTB` | Floship Product Inventory export | MTB international |
| `AMZN-MT` | Amazon Seller Central FBA + AWD (MTB ASINs) | MTB Amazon |
| `AMZN-SS` | Amazon Seller Central FBA + AWD (SS + NFMD ASINs) | SS/NFMD Amazon |
| `WM-SS` | Walmart Seller Center WFS Inventory | SS Walmart |
| `WM-NFMD` | Walmart Seller Center WFS Inventory (direct pull) | NFMD Walmart |
| `OXYGENMT`, `OXYGENSS` | (no 3PL source today — SAP-only) | Oxygen Plant warehouses |

---

## Build plan (when ready)

### Phase 1 — Loader

`load_sap_inventory()` in a new script `scripts/build_inventory_audit.py`:
- Read newest `.xlsx` from `reports/sap-inventory/`
- Coerce types
- Build dict keyed by `(item_no, warehouse_code) → sap_qty`

### Phase 2 — Cross-reference

For each `(item_no, warehouse)` in SAP:
- Look up the matching 3PL/Amazon value per the map above
- Compute `gap = actual - sap` and `gap_pct = gap / sap × 100`

### Phase 3 — Flag rules

*(Pending Tommy's decision — see Open Questions below)*

Provisional defaults:
- **🔴 MATERIAL gap** — `|gap| ≥ 50 units` OR `|gap_pct| ≥ 10%` (whichever fires)
- **🟡 MINOR gap** — `|gap| ≥ 10 units` OR `|gap_pct| ≥ 5%`
- **🟢 MATCH** — within thresholds
- **⚪ SAP-only** — SAP has the item, no 3PL data
- **⚪ 3PL-only** — 3PL has the item, no SAP data

### Phase 4 — Output

*(Pending Tommy's decision — standalone Excel OR new tab on weekly-report.xlsx)*

If standalone (Option A):
- `outputs/<date>/inventory-audit-YYYY-MM-DD.xlsx`
- Tab 1: 📊 Reconciliation Summary (counts by gap tier, $ value at risk)
- Tab 2: 🔴 Material Discrepancies (sorted by absolute gap desc)
- Tab 3: 🟡 Minor Discrepancies
- Tab 4: ⚪ One-sided records (SAP-only or 3PL-only)
- Tab 5: 🟢 Matches (audit-trail completeness)

If embedded (Option B):
- New tab `📊 Inventory Audit` on the existing weekly-report.xlsx
- One sortable table with status badges per gap tier

### Phase 5 — Rebalancing intelligence (later)

Once audit is reliable, overlay velocity data:
- High-velocity SKUs sitting in low-throughput warehouses → flag for transfer
- Cost-of-misplaced inventory metric (units × cost_unit × days-stale)

---

## Locked-in scoping (per Tommy, May 12 2026)

- ✅ **Output format:** Standalone Excel — `outputs/<date>/inventory-audit-YYYY-MM-DD.xlsx`
- ✅ **Discrepancy threshold:** Flag ANY gap — no minimum threshold. Audit purpose is data integrity, not velocity-tiered urgency.
- ✅ **Scope:** Pure audit — SAP vs warehouse actuals. NOT tied to demand planning or velocity. This report's job is to ensure SAP and the physical warehouses match.
- ✅ **Purpose:** Driving (1) data corrections in SAP, (2) 3PL investigations on physical count mismatches, (3) future rebalancing decisions when reconciliation is reliable.

## Open questions still to lock

1. **Sample SAP export** — drop one in `reports/sap-inventory/` so the section-headed parser can be tested against real data.
2. **International Amazon warehouses** (AMZ-MTAU, AMZ-MTEU, AMZ-MTUK, AMZ-NFAU/EU/UK) — do we have an actual-source to compare against, or are these SAP-only (audit ends at the SAP value, no 3PL counter-check)?
3. **Cadence** — weekly alongside the regular pipeline, or ad-hoc when audit is needed?

---

## Input infrastructure (already set up)

```
reports/sap-inventory/    ← drop SAP "Inventory In Warehouse Report" .xlsx here
```

---

## Trigger phrases to revisit

- *"Let's build the inventory audit report"*
- *"Start the inventory reconciliation build"*
- *"Compare SAP warehouse to 3PL actuals"*

---

## Related docs

- [[06 Processes & SOPs/(C) Weekly Inputs Sourcing SOP]] — will need a new entry for SAP Inventory In Warehouse Report when this builds
- [[06 Processes & SOPs/(C) Weekly Analysis — System Map]] — will need to reference the new audit report
- [[07 AI Tools & Builds/(C) ShipBob New Format Migration — Parked]] — sibling parked build (the new ShipBob format gives MORE accurate actuals for this audit)

---

*Parked: May 12, 2026 — folder ready, plan documented, awaiting SAP report sample + scoping answers*
