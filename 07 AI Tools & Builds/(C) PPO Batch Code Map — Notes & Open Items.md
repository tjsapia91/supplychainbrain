---
type: build-note
status: v1 shipped — parked for refinements
created: 2026-08-05
script: MTB-SupplyChain/scripts/build_batch_code_map.py
tags: [batch-codes, ppo, traceability, parked]
---

# (C) PPO Batch Code Map — Notes & Open Items

**Resume trigger:** *"pick up the PPO batch code map"*

## Status — v1 SHIPPED ✅
Parser + Excel map built and working. Committed to MTB-SupplyChain (`14892f6`), published
to the SUPPLY CHAIN ANALYSIS hub as **Batch Code Map**.

- **Script:** `MTB-SupplyChain/scripts/build_batch_code_map.py` — `py -3 scripts\build_batch_code_map.py`
- **Input:** PPO PDFs in `…\Documents\SupplyChain1\PPOS\Batch codes\` (drop new PPOs there, rerun — it re-parses all)
- **Parses with:** pdfplumber (the PPO line table carries UPC · Qty · BATCH CODE · Dest.)
- **Current run:** 100 batch rows from 11 PPOs, 0 undecoded.

## The map (one row per batch assignment)
`Batch Code · Prefix · Batch (MM/YY) · Date code (NFMD) · UPC · Description · Brand · PO # · Region · Dest. · Ship Date · Qty`
Plus a **Prefix Key** sheet (prefix → product). Filterable (autofilter). Trace a batch code →
product/PO/dest/date, or filter a UPC → all its batches.

## Batch-code conventions decoded (3)
| Convention | Example | Decode |
|---|---|---|
| **MTB** `<prod><MMYY>` | `SPL0426` | Pro+ Lavender · batch 04/26 |
| **NFMD compound** `<prod><MMYY>-NFMD<MMDDYYYY>` | `NFP0426-NFMD04152026` | NasalFresh Premium · batch 04/26 · date 04/15/2026 |
| **NFMD single** `<prod><MMDDYYYY>[X]` | `NFMD03152026X` | Xylitol · date 03/15/2026 |
(line-wrapped cells joined; split carton/remainder lines aggregated by PO+UPC+batch+dest)

## OPEN ITEMS — to decide when we revisit
1. **What is the NFMD "Date code" (e.g. 04/15/2026)** — expiration or manufacture? Rename the
   column once confirmed (currently generic "Date code (NFMD)").
2. **Extra columns?** Can pull from the PPOs if wanted: container/BL #, Port of Loading, MC Qty,
   CBM, Total Cartons.
3. **Turn it into a tracker?** Add a **Received (Y/N)** + date field so batches can be checked in
   as they land (map → live tracker). Also decide if it should tie to the existing
   `01 Purchasing & Inventory/(C) Batch Code Tracker.md` (the email-brief decision log).
4. **Where it lives:** currently Excel on the hub. Decide if a vault table is also wanted.
