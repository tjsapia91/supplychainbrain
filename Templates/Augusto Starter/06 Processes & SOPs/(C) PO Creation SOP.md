# PO Creation SOP
**Owner:** Tommy Sapia — Supply Chain Manager
**Last updated:** April 13, 2026
**Status:** v1 — refine as you learn vendor processes

---

## When to Create a PO

A PO should be created when:
- Demand planning analysis flags a reorder trigger (stock < 150 days of supply)
- A stockout is imminent and expedited order is needed
- Directed by DOS or SVP of Operations

---

## Step 1 — Confirm the Reorder Trigger

Before placing a PO, verify:
- [ ] Stock on hand (across all locations: FBA, Floship, ShipBob)
- [ ] Avg daily sales velocity
- [ ] Days of supply remaining
- [ ] Any stock already in transit (check PO Tracker for open POs)
- [ ] ABC classification — A items get priority

---

## Step 2 — Determine Order Quantity

```
Order Quantity = (Avg Daily Sales × 180 days) - Stock On Hand - In Transit Stock

Target: bring supply back up to 180 days (covers 120-day lead time + 60-day buffer)
```

> Adjust for MOQs (minimum order quantities) from the vendor.

---

## Step 3 — Create the PO in SAP

*(Add SAP-specific steps here once you learn the process)*

---

## Step 4 — Log in PO Tracker

Add a row to `01 Purchasing & Inventory/(C) PO Tracker.md`:

- Fill in all fields: PO #, Brand, Vendor, SKU, Qty, Cost, Date Ordered
- Set Expected Delivery = Date Ordered + 120 days
- Set Status = Submitted

---

## Step 5 — Confirm with Vendor

- Send PO to vendor
- Get written confirmation
- Update Status → Confirmed in PO Tracker

---

## Step 6 — Track to Receipt

- Update Status → In Transit when vendor ships
- Update Status → Received + fill in Actual Delivery when stock arrives
- Move row to Closed POs section in tracker

---

## Notes
- Always check open POs before placing a new one — avoid double ordering
- Factor in any upcoming promotions or seasonal spikes when setting order quantity
- Escalate to DOS if order exceeds budget threshold *(get threshold from DOS)*
