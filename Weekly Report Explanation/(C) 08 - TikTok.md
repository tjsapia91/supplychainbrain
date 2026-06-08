# Tab 8 — TikTok

**Purpose:** Single-channel inventory + replenishment view for TikTok Shop. Same UX as the ShipBob and Walmart tabs — what's at TikTok, what's coming, and how long it lasts at current velocity.

**Lead-time path:** Supplier (150d) → ShipBob → TikTok

Wired up 2026-06-03 (replaced the prior placeholder).

---

## Data Sources

| Field | Source | Where in the file |
|---|---|---|
| **AT TIKTOK** (on_hand) | SAP — *Inventory in Warehouse Report* | Warehouse sections `Whse: TIKTOKMT` (MTB items) and `Whse: TIKTOKSS` (SS + NFMD items, split by description). Uses the **In Stock** column. |
| **OPEN PO (SUPPLIER)** | SAP — *Open PO Report* | Open PO units where Warehouse Code = `TIKTOKMT` or `TIKTOKSS` (after the standard SAP filters — Doc Status ≠ C, Posting Date ≥ 2026-01-01, Item No. = 12-digit). |
| **PO ARRIVES ON** | SAP — *Open PO Report* | Earliest Original Due Date for the same warehouse rows. |
| **DAILY SALES (TIKTOK)** | *Wholesale - Monthly Sales* file → tab `Sales by Customer-Item-Detail` | Trailing 90 days of rows where **Customer/Vendor Name** ∈ {`TikTok-HL`, `TikTok-MTB`, `TikTok-SS`}, summed by **Item No.** ÷ 90. |
| **9-mo forecast (m1..m9)** | Valogix | Forward forecast columns for Location = `TIKTOKMT` / `TIKTOKSS` (already a Valogix planning group). |
| **BRAND** | Item Master | `TIKTOKMT` → MTB. `TIKTOKSS` mixes SS/NFMD — split by description (NFMD-detected items get tagged NFMD; everything else SS). |
| **COST/UNIT, ON HAND $** | Valogix | Inventory Cost × current on_hand. |

---

## Lead Time

Fixed at **150 days** for all TikTok items (matches ShipBob, since TikTok is staging-replenished via ShipBob — supplier ocean lead dominates the planning horizon).

The 30-day ShipBob → TikTok hop is noted in the title banner but doesn't drive PO sizing.

---

## How an Item Lands in Each Section

Same logic as ShipBob:

| Section | Trigger |
|---|---|
| 🔴 Action | Status ∈ STOCKOUT / BELOW ROP / LOW **and** no incoming PO covering the gap |
| ⏱ Watch (PO covered) | Status would be action, BUT an open SAP PO + current stock lifts DOS+PO ≥ 130 days |
| 🟢 Healthy | DOS ≥ lead-time threshold |
| ⚪ Inactive / 🔚 Phase-out | ABC = D/E/Z or no demand |

---

## FULL PIPELINE Math (TikTok)

```
DAYS OF STOCK (FULL PIPELINE) = (on_hand + on_order) ÷ daily_vel
```

Same as ShipBob — no extra staging math (TikTok IS the channel, not a staging point).

---

## Why Reading This Tab

- **Wholesale velocity, not platform velocity.** TikTok sales here are pulled from internal SAP wholesale invoicing (the orders we ship from `TIKTOKMT` / `TIKTOKSS` / `SBGA-*` to TikTok). This isn't necessarily what TikTok Shop's own analytics dashboard shows — it's what actually shipped from our warehouses.
- **Three customer codes** roll up into one channel:
  - `TikTok-MTB` — main MTB volume
  - `TikTok-HL` — Health Line (NFMD-bound items)
  - `TikTok-SS` — Spa Sciences (rare; <10 sales rows historically)
- **Most TikTok orders ship from SBGA-*** (ShipBob GA), not from the dedicated `TIKTOKMT` / `TIKTOKSS` warehouses. That's why the lead-time path runs through ShipBob.

---

## How to Refresh

1. Export the SAP **Inventory in Warehouse Report** → drop in Downloads. Auto-classifies to `reports/_data/sap-inventory/`.
2. Export the SAP **Open Purchase Order Report** → drop in Downloads.
3. Export the **Wholesale - Monthly Sales** file → drop in Downloads. Auto-classifies to `reports/_data/wholesale-sales/`.
4. Run `python scripts/build_report.py`.

The wholesale file is a single SAP-derived workbook (~90MB) with one tab per customer. We only read `Sales by Customer-Item-Detail` from it.

---

## Companion Docs

- [[(C) 00 - Data Source Map]] — exact column → source mapping
- [[(C) 06 - ShipBob]] — same UX pattern (single channel, SAP-sourced)
- [[(C) 07 - Walmart]] — also staging-replenished by ShipBob
