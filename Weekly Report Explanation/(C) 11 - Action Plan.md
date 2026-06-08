# Tab 11 — ✅ Action Plan

**Purpose:** Execution-ready view of what to DO this week. Splits actions by type:
1. **🚚 ShipBob Send-ins** — units to send from ShipBob → Amazon FBA
2. **📦 Supplier POs** — new orders to place with manufacturers
3. **⚫ Inactive & Phase-Out** — items to leave alone (no action)

Same idea as the `outputs/latest/order-list-*.xlsx` standalone file but built from the legacy SKU-review workflow.

---

## How Rows Are Routed

Each Amazon item is classified into one of three buckets based on:

| Bucket | Trigger |
|---|---|
| ShipBob Send-in | FBA + FC == 0 AND ShipBob backup > 0, OR FBA-only DOS < lead_time AND ShipBob has units |
| Supplier PO | Status = CRITICAL / HIGH / TRUE STOCKOUT AND no ShipBob coverage |
| Inactive / Phase-Out | abc ∈ (E, Z) OR status = INACTIVE / LOW VEL STOCKOUT |

For items that need BOTH (e.g. Nova Pink — partial from ShipBob, balance via supplier PO), the code splits the qty: first satisfy from ShipBob, balance via supplier.

---

## Columns

| Column | Purpose |
|---|---|
| **BRAND** | MTB / SS / NFMD |
| **PRODUCT** | Item description |
| **SAP UPC** | 12-digit code |
| **ASIN** | Amazon's product ID |
| **CURRENT FBA** | Sellable now |
| **ShipBob Stock** | Available for send-in (net of Shopify reserve) |
| **DAILY VEL** | SoStocked Adj. Velocity |
| **DOS** | (FBA + FC + AWD) / vel |
| **SEND QTY** | (ShipBob tab only) — units to ship to Amazon |
| **PO QTY** | (Supplier PO tab only) — units to order from supplier |
| **REPLENISH FROM** | (ShipBob tab) — ShipBob item number / source SKU |
| **NOTES** | User-fillable comments |

---

## Source Files

The Action Plan is built from `data["all_items"]` after all enrichment, then filtered + bucketed by `build_action_plan.py` logic embedded inside `build_report.py`.

Also reads:
- `outputs/<date>/sku-review-*.xlsx` (if present) — Tommy's SKU review decisions: "active Y/N", "replenish from", "phase out"

---

## Reading the Tab

Each section has a header row + count. The numbers add up to the total actionable Amazon items.

**ShipBob Send-in section**: scan SEND QTY column → that's your transfer list for the week
**Supplier PO section**: scan PO QTY column → that's the supplier order list

---

## Companion Files

- **🛒 ORDER NOW** (`outputs/latest/order-list-*.xlsx`) — newer standalone file; same idea but uses the 150-day coverage check and PFM-based sizing
- **[[(C) 10 - Priority Actions]]** — the unified by-marketplace view that feeds this tab
