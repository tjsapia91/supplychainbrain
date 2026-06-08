# Tab 15 — 🗑 Phase-Out, Obsolete & BOMs

**Purpose:** Items that are no longer actively replenished — phase-out candidates (E), obsolete (Z), and sales BOMs (F/I/S/Z routed to a dedicated tab for visibility but no action).

These items are filtered OUT of the main brand / marketplace / Priority Actions views so the active SKU pipeline stays clean.

---

## Two Sections

### Section 1 — Phase-Out Review (E → Z)

Items where:
- `ABC Classification = E` (Phase-Out)
- AND on-hand = 0
- AND velocity = 0

These are candidates for SAP reclassification from `E` → `Z` (officially obsolete).

Section header includes a count + the suggested action: "Review with management; reclassify in SAP as Z when confirmed obsolete."

### Section 2 — Sales BOMs & Other (F / I / S / Z classifications)

Items where `ABC Classification ∈ (F, I, S, Z)`. These aren't "items" in the supply-chain sense:

| Code | Meaning |
|---|---|
| **F** | Forecast-only (no inventory tracked) |
| **I** | Internal use only |
| **S** | Sales BOM (combo / gift set / multi-unit pack — ships as the SUM of underlying SKUs) |
| **Z** | Obsolete |

Section title shows the breakdown count: e.g., `F=8 · I=16 · S=18 · Z=29`.

---

## Columns

Same `INV_COLS` structure as the brand tabs (see [[(C) 01 - Amazon US]] for similar column logic).

The key visible columns:
- BRAND, ABC, PRODUCT, SAP UPC, ASIN
- TOTAL AT AMZN (on-hand at Amazon if any)
- TOTAL INBOUND (any incoming POs — usually 0 for E/Z)
- DAILY SALES (typically 0)
- DOS
- WRITE-OFF EXPOSURE (calculated for Z items only)

---

## Write-Off Exposure (Z Items)

For Z-classified items, the section header shows total write-off exposure:

```
write_off_$ = on_hand × cost_unit
total = sum across all Z items
```

This is the financial exposure of obsolete inventory still on the books.

---

## Why These Get Their Own Tab

Three reasons:
1. **Visibility** — these items still exist in SAP but shouldn't drive POs. Hiding them entirely loses sight; segregating keeps them on the radar without the noise.
2. **Cleanup workflow** — Tommy can review the Phase-Out list weekly and bulk-reclassify E → Z when confirmed obsolete.
3. **Accounting** — Z-class write-off exposure is reported (in Section 2 header) so finance/ops has visibility.

---

## Source Files

Filtered from `data["all_items"]` using ABC classification logic. The pipeline reclassifies items with `ABC_OVERRIDE` manual overrides too (currently 9 manual overrides locked in for items where SAP is wrong mid-cycle).

---

## Common Operations

| Task | What to look at |
|---|---|
| "What's eligible for SAP cleanup?" | Section 1 — Phase-Out Review (E → Z) |
| "What's our obsolete inventory exposure?" | Section 2 — Z subgroup, write-off $ in header |
| "What about combo SKUs?" | Section 2 — S subgroup; manage the underlying components in main views |
