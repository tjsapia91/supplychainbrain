# PO Tracker
**Owner:** Tommy Sapia — Supply Chain Manager
**Last updated:** April 13, 2026

Track all open and closed purchase orders across MTB, SS, and NFMD.

---

## How to Use

- Add a row every time a PO is placed
- Update **Status** as the PO moves through the pipeline
- Update **Actual Delivery** when stock is received
- Claude can read this file and factor in-transit inventory into demand planning

---

## Status Definitions

| Status | Meaning |
|--------|---------|
| Draft | PO being prepared, not yet submitted |
| Submitted | Sent to vendor, awaiting confirmation |
| Confirmed | Vendor confirmed the order |
| In Transit | Stock shipped, on the way |
| Received | Stock received in full |
| Partial | Stock partially received, remainder pending |
| Cancelled | PO cancelled |

---

## Open POs

| PO # | Brand | Vendor | SKU | Item | Qty | Unit Cost | Total Cost | Currency | Date Ordered | Expected Delivery | Status | Notes |
|------|-------|--------|-----|------|-----|-----------|------------|----------|--------------|-------------------|--------|-------|
| — | — | — | — | — | — | — | — | — | — | — | — | No open POs yet |

---

## Closed POs

| PO # | Brand | Vendor | SKU | Item | Qty | Unit Cost | Total Cost | Currency | Date Ordered | Expected Delivery | Actual Delivery | Status | Notes |
|------|-------|--------|-----|------|-----|-----------|------------|----------|--------------|-------------------|-----------------|--------|-------|
| — | — | — | — | — | — | — | — | — | — | — | — | — | No closed POs yet |

---

## Notes
- Lead time is ~120 days — Expected Delivery = Date Ordered + 120 days
- When placing a PO triggered by demand planning, reference the weekly analysis file
- ShipBob may transition to AmzPrep — note which 3PL stock is routing to
