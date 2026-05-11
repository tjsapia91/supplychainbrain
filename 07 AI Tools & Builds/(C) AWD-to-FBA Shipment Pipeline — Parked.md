# (C) AWD-to-FBA Shipment Pipeline — Parked Build

> Plan to incorporate Amazon Seller Central's "Download shipment details AWD to FBA" report into the weekly pipeline. **Parked** — folders are set up, files can accumulate, build work happens later.
>
> **Captured:** May 11, 2026
> **Status:** PARKED — input infrastructure ready, no code yet
> **Trigger phrase to revisit:** *"Let's build the AWD-to-FBA shipment pipeline"*

---

## What this report gives us

**Source:** Amazon Seller Central → AWD → "Download shipment details AWD to FBA"

**Granularity:** Per-shipment line items (NOT ASIN aggregates like the existing AWD Inventory Report).

**Columns:**
- `Merchant` · `Shipment ID` (FBA19...) · `Status` · `From` · `To` · `Created date`
- `FNSKU` · `MSKU` · `Confirmed quantity` · `Departed quantity` · `Received quantity` · `Replenishment mode`

**Statuses seen:** Receiving · Closed · In transit · Shipped · Checked in

**Sample volume (May 11, 2026 MTB pull):** 335 shipments · 117 active · ~5,024 units in motion

---

## Why we want it

Fills a gap between the two existing Seller Central reports:

| Report | What it answers |
|---|---|
| AWD Inventory Report (existing) | "How much AWD stock total?" — ASIN aggregate |
| FBA Inventory Report (existing) | "How much FBA stock + pipeline total?" — ASIN aggregate |
| **AWD-to-FBA shipment details (new)** | **"Which specific shipments are moving AWD→FBA right now, and at what stage?"** — per-shipment line items |

---

## Input infrastructure (already set up)

```
reports/awd-to-fba-shipments/
├── MTB/         ← drop MTB exports here
├── NFMD/        ← drop NFMD exports here
└── SS/          ← drop SS exports here
```

**No renaming.** Standard filename pattern from Seller Central is a timestamp like `2026-05-11T15_27_03.709Z.xlsx`. Loader will auto-pick the newest file per brand.

---

## Build plan (when ready)

### Phase 1 — Loader

`load_awd_to_fba_shipments()` in `scripts/build_report.py`:
- Read newest `.xlsx` from each brand folder (skiprows=1, since row 0 is descriptive text)
- Coerce types: `Created date` → datetime, qty cols → numeric
- Add computed `In Transit` column = `Confirmed - Received`
- Return list of shipments with brand tag

### Phase 2 — New tab `⏳ AWD→FBA Pipeline`

Layout:
- Title bar with totals (X shipments · Y units in motion · Z stuck >14d)
- Filterable table per brand
- Color-code by status (Receiving · In transit · Shipped · Checked in · Closed)
- Sort: oldest open shipments first (stuck-shipment surfacing)

Columns:
`STATUS · BRAND · SHIPMENT ID · FNSKU · MSKU · PRODUCT · CREATED · DAYS OPEN · CONFIRMED · DEPARTED · RECEIVED · IN TRANSIT · STUCK FLAG · MODE`

### Phase 3 — Stuck-shipment detector

- 🚨 STUCK if status in (Receiving, In transit, Shipped) AND `Created date` > 14 days ago
- 🟡 WATCH if 7-14 days
- Pull product description from SAP Item Master via UPC (MSKU)
- Pull ASIN from SoStocked lookup
- Surface stuck shipments at the top of the new tab

### Phase 4 — Reconciliation hook with TrueOPS Shipment Module

If `Departed quantity ≠ Received quantity` (and status = Closed) → potential lost-inbound case:
- Flag in this tab
- Cross-check against the TrueOPS Master_Shipment_Log to see if it's already being claimed
- If not, log to a "Potential New Claim" section for review

---

## Open questions to lock in before building

1. **Cadence** — pull weekly with the rest of the inputs, or daily during active stockout periods?
2. **Time horizon** — Amazon's report covers "open shipments + closed shipments from past month". Is 30-day lookback enough, or do we need to archive snapshots for longer-term audit?
3. **Stuck-shipment thresholds** — 14d for STUCK seems right for AWD→FBA leg (vs the 30d POD SLA on the lost-inbound claims side). Confirm before coding.
4. **TrueOPS integration** — should "Potential New Claim" findings auto-post to the TrueOPS Sync Log, or stay in the weekly report only?
5. **Per-shipment UI** — render as a flat filterable table only, or also group by AWD warehouse (From column)?

---

## Trigger phrases to revisit

- *"Let's build the AWD-to-FBA shipment pipeline"*
- *"Start Phase 1 of the AWD-to-FBA build"*
- *"Wire AWD-to-FBA shipments into the weekly report"*

---

## Related docs

- [[06 Processes & SOPs/(C) Weekly Inputs Sourcing SOP]] — will need a new entry for this report (Phase 1)
- [[06 Processes & SOPs/(C) Amazon Seller Central — Reports Pull List]] — will need the pull instructions
- [[07 AI Tools & Builds/TrueOPS Shipment Module/(C) TrueOPS Shipment Module — System Brief]] — sibling system, reconciliation hook in Phase 4

---

*Parked: May 11, 2026 — folders ready, files can accumulate while we wait to build*
