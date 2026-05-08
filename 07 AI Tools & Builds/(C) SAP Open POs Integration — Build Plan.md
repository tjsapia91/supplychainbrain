# (C) SAP Open POs Integration — Build Plan

> Parked idea — pull SAP open Purchase Orders into the weekly pipeline so we can answer "have I already committed to enough inventory to cover this CRITICAL item?"
>
> **Captured:** May 4, 2026
> **Status:** PARKED — to revisit when you're ready
> **Trigger phrase to revisit:** *"Let's pick up the SAP Open POs build plan"*

---

## The problem this solves

Currently when an item is flagged CRITICAL (DOS ≤ Lead Time), we know it needs a PO — but we don't see whether one's **already been placed in SAP**. The pipeline only sees:

- FBA Pipeline (Amazon-visible inbound)
- Inbound to AWD (Amazon-visible)
- In-Transit Log entries (after a shipment leaves the supplier)
- Valogix "On Order Total" (forecast-tool number, not SAP truth)

**Gap:** POs **placed in SAP but not yet shipped** are invisible. Could lead to redundant POs being placed.

---

## Recommended approach

### Source: **SAP** (not the In-Transit `NF Open POs` sheet)

| Factor | SAP | In-Transit Log sheet |
|---|---|---|
| Authoritative? | ✅ System of record | ❌ Manually maintained |
| Multi-brand coverage | ✅ MTB / SS / NFMD / LUMOS | ❌ NF-prefix suggests NFMD-only |
| Drift risk | Low | High |

### Surfacing: **New tab + summary column** (not a merge into ON ORDER)

Avoid the temptation to fold SAP qty into the existing `ON ORDER` column because:
- Would hide lifecycle (placed vs shipped vs received)
- High double-count risk (same PO shows in SAP + In-Transit + AWD inbound)
- We just fixed this category of bug for AWD/FBA — don't reintroduce

---

## Phase 1 — Foundation (the immediate win)

### What Tommy provides
1. SAP **Open Purchase Orders** export (one file, all brands)
2. File format (.xlsx / .csv / .txt?)
3. Column names SAP uses (don't guess — match exactly)
4. Drop into: `reports/sap-pos/`

### What Claude builds
1. **`load_sap_open_pos()`** reader function
2. **New tab `📋 Open POs`** on weekly report:
   - Grouped by vendor, sorted by expected delivery date
   - Columns: `PO#` · `Vendor` · `Brand` · `UPC` · `Product (SAP desc)` · `Qty Ordered` · `Qty Received` · `Qty Outstanding` · `Expected Date` · `Days Until` · `Linked Critical Item? (✓/✗)`
   - Auto-filter; color-coded by urgency (🔴 overdue · 🟠 next 30d · 🟢 60+d out)
3. **New column `OPEN PO QTY`** on Priority Actions tab — total outstanding SAP qty per UPC. Sits alongside ON ORDER (does NOT modify it).

---

## Phase 2 — Lifecycle reconciliation (next iteration)

After Phase 1 is in production:
- Auto-match SAP PO # → In-Transit Log PO # (so the same PO is visible across stages)
- New `STATUS` column: `PLACED` / `IN PRODUCTION` / `SHIPPED` / `AT AWD` / `RECEIVED`
- Flag POs that look **stuck**: placed >30d, no In-Transit entry yet → supplier follow-up trigger

---

## Phase 3 — Smart augmentation (down the road)

After 2-3 weeks running Phase 1+2, with confidence in PO matching:
- Fold SAP qty into a unified `TOTAL ON ORDER (all stages)` column on Priority Actions — only if double-count risk is fully understood
- Auto-downgrade CRITICAL items to WATCH if a confirmed open PO covers the gap before stockout

---

## What "done" looks like

A weekly run answers, for every CRITICAL item:
> "Yes you're at 84 DOS with 117-day lead time, but you've already placed PO 3140 in SAP for 5,000 units expected Aug 15 — that bridges the gap. No new PO needed."

---

## To revisit this build

Type any of:
- *"Let's pick up the SAP Open POs build plan"*
- *"Start Phase 1 of the SAP Open POs integration"*
- *"Open the parked SAP PO idea"*

Claude will read this doc and walk you through Phase 1 starting with the SAP export.

---

*Captured: May 4, 2026 · Owner: Tommy*
