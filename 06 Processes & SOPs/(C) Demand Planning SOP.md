# Demand Planning SOP — DEPRECATED

> ⚠️ **This document is deprecated as of May 4, 2026.** The workflow it described (SoStocked "Multi-Dashboard Report" + single-source DOS formula) was replaced over April-May 2026 with a multi-source pipeline pulling from 8 systems.

---

## Use these instead

| What you need | Where to look |
|---|---|
| **Where every input file comes from** | [[06 Processes & SOPs/(C) Weekly Inputs Sourcing SOP]] |
| **How to run the weekly pipeline end-to-end** | [[06 Processes & SOPs/(C) Weekly Analysis SOP — Step by Step]] |
| **One-page Monday cheat sheet** | [[06 Processes & SOPs/(C) Weekly Analysis Cheat Sheet — 1 Page]] |
| **This week's live runbook** | [[15 Meetings & Decisions/(C) Weekly Run Log — 2026-05-01]] |
| **ABC classification rules** | [[06 Processes & SOPs/(C) ABC Classification Reference]] |

---

## What changed (so you know what was wrong here)

| Old (this doc) | New (current) |
|---|---|
| Pull SoStocked "Multi-Dashboard Report (All Accounts)" — 1 file | Pull 9 SoStocked files (3 reports × 3 brands: Forecast + Inventory + FvA) |
| `DOS = (FBA Stock + AWD Stock) ÷ Adj. Velocity` | `DOS = (FBA Stock + AWD Available + AWD Inbound) ÷ Adj. Velocity` |
| Amazon-only analysis | 8-system multi-marketplace: Amazon US/CA · Shopify MTB · Spa Sciences DTC SS · Spa Sciences DTC NFMD · Walmart SS · Walmart NFMD · Floship Intl |
| `python combine_forecast.py` | `python scripts\combine_forecast.py` (scripts moved into `scripts/` folder) |
| 1 output file | 4 output files: weekly-report · action-plan · shipment-tracking · demand-plan |

---

*Deprecated: May 4, 2026 — superseded by the docs linked above. Kept for history; do not follow.*
