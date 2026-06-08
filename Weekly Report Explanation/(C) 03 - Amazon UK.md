# Tab 3 — Amazon UK

**Purpose:** International placeholder — surfaces SAP supplier POs routed to UK warehouse (`AMZ-MT-UK` / `AMZ-SS-UK`). No item-level stock or velocity data yet.

---

## Why This Tab Exists

The UK Amazon listings get supplier POs but don't yet have a feed for:
- FBA inventory (no SC UK exports configured)
- Velocity (no SoStocked UK marketplace)
- Sellerboard UK history

So the tab is built from one source only: **SAP Open POs routed to UK warehouses**. Each open PO gets one synthesized row so you can see what's coming.

---

## Columns

Same column structure as Amazon US ([[(C) 01 - Amazon US]]), but most fields are blank/zero:

### What's Populated

| Column | Source | Value |
|---|---|---|
| **BRAND** | SAP Open PO routing — `AMZ-MT-UK` → MTB, `AMZ-SS-UK` → SS | Direct |
| **PRODUCT** | Item description from SAP Open POs (falls back to item_master) | Direct |
| **SAP UPC** | SAP Open PO item number | 12-digit UPC |
| **OPEN PO (SUPPLIER)** | `reports/_data/sap-open-pos/*.xlsx` — open units for this item × UK warehouse | Sum |
| **PO ARRIVES ON** | Earliest open SAP PO due date | Date |

### What's Blank/Zero

- ASIN, AMAZON SKU — not mapped yet
- FBA, AWD, FC Transfer, all inbound stages — no UK SC feed
- DOS columns — can't compute without velocity
- Velocity — no UK marketplace velocity source
- 9-month forecast — no UK PFM

---

## Status

All rows show "PO ROUTED" or similar — they're informational only, not action items.

---

## Source File

- `reports/_data/sap-open-pos/SAP Open Purchase Order Report*.xlsx`

The SAP warehouse routing map:
```
SAP_WH_TO_CHANNEL = {
  "AMZ-MT-UK": "Amazon UK",
  "AMZ-SS-UK": "Amazon UK",
  ...
}
```

---

## When This Tab Will Get Real Data

When UK Amazon launches a real listing per brand, you'll need to:
1. Set up SC UK exports → drop into `reports/_data/seller-central/UK/<brand>/`
2. Configure SoStocked UK marketplace
3. Add UK FBA Inventory + AWD Inventory loaders to `build_report.py`

Until then, this tab is "what's on the water to the UK warehouse" only.
