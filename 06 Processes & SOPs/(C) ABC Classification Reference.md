# (C) ABC Classification Reference

> Official ABC classification codes used by Michael Todd Beauty across all 3 brands (MTB, NFMD, SS). Source of truth: SAP item master.

| Code | Meaning | Description |
|---|---|---|
| **A** | High Volume | Top-selling SKUs — flag for tight stock control, never run out |
| **B** | Medium Volume | Steady sellers — standard reorder cadence |
| **C** | Low Volume | Slow sellers — keep minimal stock, longer reorder cycles |
| **D** | Phase In | New SKU — building velocity, watch closely as demand develops |
| **E** | Phase Out | Winding down — deplete remaining stock, no new POs |
| **Z** | Obsolete | Discontinued — no longer sold, write off remaining stock |

---

## How it's used in the Weekly Report

Every active SKU should have one of these 6 codes assigned in SAP. The Weekly Report displays the ABC code as a colored badge on each row:

| Badge color | Code |
|---|---|
| 🟦 Deep teal | A — High Volume |
| 🟪 Indigo | B — Medium Volume |
| 🟫 Plum | C — Low Volume |
| 🟪 Lavender | D — Phase In |
| 🟧 Burnt sienna | E — Phase Out |
| ⬛ Charcoal | Z — Obsolete |

ABC badges use a teal/indigo/plum palette so they're visually distinct from the
muted brick/amber/sage/slate used for inventory **status** (Stockout / Critical / Warning / Healthy / Inactive).

If an item shows "—" instead of a badge, it means:
- The item's UPC isn't in the item master, OR
- The item master has a different/unrecognized code in the ABC field

---

## Decision rules tied to ABC

| When you see... | What to do |
|---|---|
| **A** item flagged as low DOS | URGENT — A's are top revenue, never let them stock out |
| **B** item flagged as low DOS | Reorder normally — keep standard buffer |
| **C** item flagged as low DOS | Stock out is ok — assess whether to keep replenishing |
| **D** item with rising velocity | Reclassify to A/B/C as it stabilizes |
| **E** item with **0 on hand + 0 velocity** | Candidate for **Z** reclassification — see Phase-Out Review tab |
| **Z** item still showing in reports | Should be removed from sales channels — clean up listings |

---

*Created: April 28, 2026*
*Reference: SAP item master `Item No. + ABC Classification` columns*
