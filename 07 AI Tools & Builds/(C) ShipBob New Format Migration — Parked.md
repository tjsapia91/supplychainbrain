# (C) ShipBob New Format Migration — Parked Build

> Plan to migrate ShipBob ingestion from the legacy "On Hand Summary" pivoted export to the new normalized lot-level export. Strictly more data, more accurate availability, lot/expiration tracking. **Parked** — files can accumulate in a holding folder while we wait to build.
>
> **Captured:** May 11, 2026
> **Status:** PARKED — new-format files accumulating in holding folder, no pipeline integration yet
> **Trigger phrase to revisit:** *"Let's migrate ShipBob to the new format"*

---

## Why migrate

The new ShipBob export gives us **per-lot × per-FC detail with a full status breakdown**, replacing the legacy pivoted export's "Total On Hand by warehouse" view.

**Operational gaps the new format closes:**

| Field | Operational value | Existing format |
|---|---|---|
| **Sellable** | What's ACTUALLY pullable (excludes Committed, Exception, Backordered) | ❌ only `Total On Hand` (over-states availability) |
| **Committed** | Allocated to open orders — shouldn't count as free stock | ❌ |
| **Exception** | Damaged / quality-issue stock → write-off review | ❌ |
| **Backordered** | Orders waiting on stock → lost-sale signal | ❌ |
| **Incoming** | En-route to a specific FC | ❌ |
| **Lot Number + Expiration Date** | Shelf-life tracking (creams, oils, etc.) | ❌ |
| **Internal Transfer** | Inter-FC movement visibility | ❌ |

**The big payoff: Sellable vs Total On Hand**

Current pipeline uses `Total On Hand` for Shopify on-hand. If ShipBob has 1,000 units total but 300 are Committed/Exception/Backordered, the real number for stockout decisions is **700 Sellable**, not 1,000. Today's pipeline slightly over-states availability.

---

## Side-by-side reference

**Legacy export (currently in use):**
- 143 rows · 19 columns
- Pivot: SKU × warehouse — `Total On Hand` + 13 warehouse columns
- Sample columns: `SKU`, `Total On Hand`, `US (CA) West Hub 1`, `Bethlehem (PA)`, `Reno (NV)`, ...

**New export (target):**
- 604 rows · 14 columns
- Normalized: one row per (SKU × Lot × Fulfillment Center)
- Columns: `SKU`, `Inventory ID`, `Inventory Name`, `Lot Number`, `Expiration Date`, `Incoming`, `On Hand`, `Committed`, `Fulfillable`, `Exception`, `Sellable`, `Backordered`, `Internal Transfer`, `Fulfillment Center`

---

## Holding infrastructure (already set up)

```
reports/shipbob/_new-format/
├── MTB/         ← drop new-format MTB exports here
├── NFMD/
├── SS/
└── LUMOS/
```

**Why a holding folder:** the current `load_shipbob()` loader reads the `Total On Hand` column which doesn't exist in the new format. Putting new-format files in the regular `reports/shipbob/<BRAND>/` folder would cause the loader to fail or zero-out. The holding folder keeps them out of the active pipeline until we build the new loader.

**Until we migrate:** keep pulling BOTH the legacy "On Hand Summary" (into `reports/shipbob/<BRAND>/`) AND the new export (into `reports/shipbob/_new-format/<BRAND>/`). The pipeline keeps running on the legacy format; the new format accumulates ready for migration.

---

## Build plan (when ready)

### Phase 1 — Rewrite `load_shipbob()`

In `scripts/build_report.py`:
- Read newest file from `reports/shipbob/<BRAND>/` (or wherever we settle the file location post-migration)
- Detect format by columns:
  - If `Total On Hand` present → legacy format → fall back to existing parser
  - If `Sellable` present → new format → new parser
- For new format, aggregate by SKU:
  - `Sellable` (sum across FCs) → canonical on-hand number
  - `Committed`, `Exception`, `Backordered`, `Incoming`, `Internal Transfer` (sums) → stored as separate fields
  - Per-FC breakdown stashed in a side dict if a tab wants it
  - Lot-level expiration data stashed for the Expiration tab (Phase 3)
- Return dict shape compatible with current usage: `{upc: {"on_hand": <Sellable>, "brand": ..., "name": ...}}`
- Plus an extended dict for the new fields: `{upc: {"committed": N, "exception": N, "backordered": N, "incoming": N, "internal_transfer": N, "lots": [...]}}`

### Phase 2 — Update consumers

Files that consume `load_shipbob()` output today:
- `apply_shipbob_overrides()` — overrides Shopify on_hand + Amazon shipbob_emergency
- Switch from `on_hand` → `sellable` semantics
- Add new columns to per-marketplace tabs:
  - `BACKORDERED` (yellow if > 0)
  - `EXCEPTION` (amber/brick if > 0)
  - `COMMITTED` (informational)

### Phase 3 — NEW tab: 🟡 ShipBob Health Check

Surface the operational signals the new format unlocks:
- **Backorders** section: every SKU with `Backordered > 0` — sorted by qty desc — these are orders ShipBob has accepted but can't ship
- **Exceptions** section: every SKU with `Exception > 0` — damaged/quality-issue stock for write-off review
- **Lot Expiration** section: lots expiring within 90 days, sorted by expiration date asc — proactive recall/discount candidates
- **Internal Transfer** section: anything in motion between FCs — same-day visibility, helps avoid double-counting

### Phase 4 — Update related docs

- [[06 Processes & SOPs/(C) Weekly Inputs Sourcing SOP]] — note the export menu path change in ShipBob
- [[06 Processes & SOPs/(C) ShipBob — Reports Pull List]] — update pull instructions
- Brief on legacy-vs-new fields so Augusto knows which to pull

---

## Open questions to lock in before building

1. **Where in ShipBob's UI is the new export menu?** Confirm the path so the SOP can be updated. Same export option for all 4 brand logins?
2. **Is the legacy "On Hand Summary" still available** in the ShipBob UI? Should we phase it out entirely or keep as backup?
3. **`Sellable` vs `Fulfillable` vs `On Hand`** — what's the canonical "free to ship" number ShipBob recommends? Looks like `Sellable` is `Fulfillable - Backordered` but need to confirm with ShipBob docs.
4. **Lot expiration alert threshold** — 90 days, 60 days, 30 days? Beauty SKU shelf life varies (some products are stable for years, others 12-18 months).
5. **Exception handling** — should `Exception > 0` SKUs auto-deduct from the Sellable count in the pipeline? Or leave Sellable as-is and just surface the exception flag?
6. **Backordered SKUs on Amazon side** — if ShipBob has `Backordered > 0` for a UPC that's also active on Amazon, should we flag a potential emergency send-in?

---

## Trigger phrases to revisit

- *"Let's migrate ShipBob to the new format"*
- *"Start the ShipBob new format build"*
- *"Switch the pipeline to ShipBob's Sellable column"*

---

## Related docs

- [[06 Processes & SOPs/(C) Weekly Inputs Sourcing SOP]] — current ShipBob source-of-truth doc
- [[06 Processes & SOPs/(C) ShipBob — Reports Pull List]] — per-brand pull walkthrough
- [[07 AI Tools & Builds/(C) AWD-to-FBA Shipment Pipeline — Parked]] — sibling parked plan, same architecture

---

*Parked: May 11, 2026 — holding folder ready, files can accumulate while we wait to build*
