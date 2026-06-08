# Tab 13 — 📦 Replenishment Triggers

**Purpose:** Surfaces items where the reorder-point (ROP) trigger has fired — either a 2-tier supply chain alert (supplier → staging → Amazon) or a single-tier alert (Valogix channels).

This is a more *technical* view of "reorder needed" than the Priority Actions tab — Priority Actions uses DOS thresholds; this uses ROP-based triggers.

---

## The 2-Tier Replenishment Model (Tommy 2026-05-27)

For Amazon items:

```
Supplier (140d lead) → Staging (ShipBob US / Alliance CA) → Amazon (60d transfer)
```

Two trigger checks:
1. **Tier 1 (Supplier → Staging)**: Trigger a new supplier PO when staging falls below `daily_vel × 140` (the ocean lead time)
2. **Tier 2 (Staging → Amazon)**: Trigger an Amazon transfer when Amazon FBA falls below `daily_vel × 60` AND staging has units

For non-Amazon items (Shopify, Walmart, Floship), the trigger is Valogix's per-location ROP check.

---

## Columns

| Column | Source | Calculation |
|---|---|---|
| **TIER** | Computed | `🔴 EMERGENCY` (dos_with_po < 60d), `🟠 TIER-1 SUPPLIER`, `🟡 TIER-2 STAGING`, or `🟢 OK` |
| **BRAND** | item_master | |
| **PRODUCT** | item_master | |
| **SAP UPC** | item or SAP | |
| **DESTINATION** | Computed | "Amazon US" / "Amazon CA" / "Shopify MTB" / etc. |
| **CURRENT STOCK (at Amazon)** | Amazon FBA + FC + AWD | |
| **STAGING ON HAND** | ShipBob backup (US) or Alliance WH (CA) or N/A for Valogix items | |
| **PIPELINE TOTAL** | Computed | Current + Staging + AWD inbound + FBA pipeline + open SAP supplier PO |
| **DOS (W/ POs)** | Pipeline Total / daily_vel | Same as `dos_with_po` field |
| **MAX SB TRANSFER** | Computed | Min(staging on-hand, units needed to reach 90d Amazon coverage) — recommended transfer qty |
| **SHIPBOB** | ShipBob backup | Direct |
| **VELOCITY** | daily_vel | |
| **NOTES** | User input | |

---

## Tier Definitions

| Tier | Condition | What to do |
|---|---|---|
| 🔴 **EMERGENCY** | `dos_with_po < 60d` | Air freight / expedited transfer needed RIGHT NOW |
| 🟠 **TIER-1 SUPPLIER** | Total pipeline < 140-day demand AND no incoming PO covers gap | Place new supplier PO ASAP |
| 🟡 **TIER-2 STAGING** | Amazon FBA < 60-day demand AND staging has units | Trigger SB → FBA send-in (or Alliance → Amazon CA) |
| 🟢 **OK** | Above all thresholds | No action |

---

## Sorting

Rows sorted by:
1. Tier (Emergency first)
2. Within tier: dos_with_po ascending (most urgent first)

---

## Source Files

This tab is a *computed view* — no new file reads beyond what `build_report.py` already loaded for the Amazon and Valogix tabs.

---

## Common Operations

| Task | What to look at |
|---|---|
| "What's about to stock out even with all POs counted?" | Filter **TIER** = 🔴 EMERGENCY |
| "What needs a new supplier order?" | Filter **TIER** = 🟠 TIER-1 SUPPLIER |
| "What can I refill from ShipBob without ordering more?" | Filter **TIER** = 🟡 TIER-2 STAGING — look at MAX SB TRANSFER for suggested qty |
| "How much ShipBob do I have for emergency transfers?" | Sum **SHIPBOB** column |
