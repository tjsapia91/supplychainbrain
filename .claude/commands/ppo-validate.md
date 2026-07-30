---
description: Validate a PO (PPO) against the vendor's PI — item #s, qtys, master-carton qty, order pairing, buyer/address. In-brain replacement for the PPO Validator web app's check step.
argument-hint: "<PO#>  e.g. 3276"
---

# /ppo-validate — check a PO against its PI (in the brain)

Validate PPO `$ARGUMENTS` against the vendor's Proforma Invoice. Read-only. Replicates the PPO/PI Validator web app's checks (it does NOT merge PDFs — that stays external if needed).

## Find the files
Look in `01 Purchasing & Inventory/_ppo-validate/` for a PO PDF and a PI PDF whose filename contains `$ARGUMENTS` (PO = file with "PPO"/"PO" in the name; PI = the other). If either is missing, say so and stop. (If Tom points at specific files or email attachments instead, use those.) Read both PDFs with the Read tool.

## Extract from each
- **PO (PPO):** PO#, buyer name + HQ address + ZIP (letterhead), vendor, incoterm, and per line: item # (UPC), qty, Master Carton qty. Remember our POs carry **NO pricing** (DDP with Harry) — do not flag missing/zero price.
- **PI:** PO# in header, seller/company name, buyer block (name/address/ZIP), incoterm, and per line: item #, qty, pcs/ctn (MC), batch code if present.

## Run the checks → label each ✅ ok / ⚠ review / ❌ error
**Header:**
1. **Order pairing** — PI header PO# == PPO# (digits only) → ok / ❌ ORDER MISMATCH.
2. **Buyer vs brand** — PI buyer matches the brand → ok / ⚠.
3. **Buyer ZIP** == PO letterhead ZIP → ok / ⚠ (vendor may be on an old template).
4. **Buyer address** consistent with PO letterhead (token overlap ≥ ~50%) → ok / ⚠.
5. **Incoterm** — note it (expect DDP).
6. **Vendor/seller** — PO vendor ~ PI seller → ok / ⚠.

**Per line item (match by item #/UPC):**
7. On PO but not PI, or on PI but not PO → ⚠.
8. **Qty match** — PO qty == PI qty → ok / ❌ QTY MISMATCH.
9. **MC qty match** — PO Master-Carton == PI pcs/ctn → ok / ❌ MC QTY MISMATCH (if PI omits MC, PO MC stands → ok).
10. **Full cartons** — PO qty is an exact multiple of MC → ok / ❌ not a full multiple.
11. **Batch code** — note it if the PI shows one (cross-ref [[01 Purchasing & Inventory/(C) Batch Code Tracker]] conventions).
12. **Master cross-check (optional):** if reachable, compare each item's MC to the SAP item master (`C:\Users\Tom Sapia\MTB-SupplyChain\reports\item-master\item_master.xlsx`, "UPC Master Carton Quantity") → flag mismatches / below MOQ.

## Verdict + report
- **FAIL** if any ❌ · **REVIEW** if any ⚠ (no ❌) · **PASS** if all ✅.
- Print the verdict at top, then the grouped check list (errors first). Lead with any qty/MC/pairing mismatch — those block sending to approvers.
