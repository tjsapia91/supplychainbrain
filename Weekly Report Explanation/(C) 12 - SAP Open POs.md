# Tab 12 — 📋 SAP Open POs

**Purpose:** Every open SAP supplier PO with destination warehouse, ETA, and a same-day flag for POs landing soon.

Direct view of `reports/_data/sap-open-pos/SAP Open Purchase Order Report*.xlsx` with light enrichment.

---

## Columns

| Column | Source | Calculation |
|---|---|---|
| **PO #** | SAP Open POs | Direct |
| **VENDOR** | SAP Open POs | Supplier name |
| **DESTINATION WAREHOUSE** | SAP Open POs | SAP warehouse code (`AMZN-MT`, `AMZN-SS`, `ASG-MTB`, `SBGA-MT`, etc.) |
| **DESTINATION CHANNEL** | Computed | Mapped from warehouse code via `SAP_WH_TO_CHANNEL` dict (e.g. `AMZN-MT → Amazon US`, `ASG-MTB → Alliance WH (CA staging)`) |
| **SAP UPC** | SAP Open POs | Item code |
| **PRODUCT** | SAP Open POs / item_master | Item description |
| **BRAND** | item_master | Branch lookup |
| **QTY** | SAP Open POs | Open units (not yet received) |
| **PO ETA** | SAP Open POs | Due date |
| **DAYS UNTIL ETA** | Computed | `PO ETA − TODAY()` |
| **⚠️ SAME-DAY FLAG** | Computed | 🚨 if PO ETA is within ±7 days of today |

---

## SAP Warehouse → Channel Routing

The pipeline maps SAP warehouses to display channels via this dict (in `build_report.py`):

```python
SAP_WH_TO_CHANNEL = {
    "AMZN-MT":   "Amazon US",
    "AMZN-SS":   "Amazon US",
    "AMZ-MT-CA": "Amazon CA",
    "AMZ-SS-CA": "Amazon CA",
    "AMZ-MT-UK": "Amazon UK",
    "AMZ-SS-UK": "Amazon UK",
    "AMZ-MT-AU": "Amazon AU",
    "AMZ-SS-AU": "Amazon AU",
    "AMZ-MT-EU": "Amazon EU",
    "AMZ-SS-EU": "Amazon EU",
    "AMZ-MT-TT": "TikTok",
    "AMZ-SS-TT": "TikTok",
    "ASG-MTB":   "Alliance WH (CA staging)",
    "ASG-NF":    "Alliance WH (CA staging)",
    "ASG-SS":    "Alliance WH (CA staging)",
    "SBGA-MT":   "ShipBob",
    "SBGA-SS":   "ShipBob",
    "SBGA-SS-NFMD": "ShipBob (NFMD)",
    # ... plus international + DTC channels
}
```

Each PO is routed to ONE channel based on its destination warehouse. The pipeline also uses this mapping to inject OPEN PO + PO ETA values into the respective marketplace tabs.

---

## Same-Day Flag Logic

```
flag = "🚨 SAME-DAY" if abs((PO ETA - TODAY()).days) <= 7
     = ""           otherwise
```

This flags POs that should be landing this week — alerts you to confirm receipt and book inventory.

---

## Source File

`reports/_data/sap-open-pos/SAP Open Purchase Order Report*.xlsx`

This file is maintained by Tommy / supply chain team. The pipeline reads the latest by mtime.

---

## Common Operations

| Task | What to look at |
|---|---|
| "What's landing this week?" | Filter on **⚠️ SAME-DAY FLAG** = 🚨 |
| "How much supply is incoming to Amazon US?" | Filter **DESTINATION CHANNEL** = "Amazon US" — sum QTY |
| "Why isn't this PO showing on the Amazon US tab?" | Check **DESTINATION WAREHOUSE** — if it's not in `SAP_WH_TO_CHANNEL`, the routing doesn't fire |
| "What POs are at the supplier still?" | All rows on this tab — they're all open (haven't received) |
