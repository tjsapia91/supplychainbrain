# (C) ABC Classification Reference

> Official ABC classification codes used by Michael Todd Beauty across all 3 brands (MTB, NFMD, SS). Source of truth: **SAP item master, matched by UPC**.
>
> **Last updated:** May 5, 2026

---

## The 9-code taxonomy

| Code | Meaning | Description |
|---|---|---|
| **A** | High Vol | Top-selling SKUs — tight stock control, never run out |
| **B** | Med Vol | Steady sellers — standard reorder cadence |
| **C** | Low Vol | Slow sellers — minimal stock, longer reorder cycles |
| **D** | Phase In | New SKU — building velocity, watch closely as demand develops |
| **E** | Phase Out | Winding down — deplete remaining stock, no new POs |
| **F** | Other | Items that don't fit standard A-E classification |
| **I** | Ind. Comp. | Industrial Component — packaging, raw materials, components, not finished goods |
| **S** | Sales BOM | Combo packs, gift sets, sales BOMs — not single-SKU listings |
| **Z** | Obsolete | Discontinued — no longer sold, write off remaining stock |

---

## How items get classified

**Match key: UPC** (the SAP `Item No.` column). Never description — multiple SKUs can share the same description (e.g., "Sonicsmooth -White - New" exists as both `811573031113` and `811573031526`, with different ABC codes).

Lookup chain:
1. Read `reports\item-master\item_master.xlsx` (refreshed weekly from SAP `SAPABCCLASSIFICATION.xlsx` export)
2. Match item UPC to `Item No.` column
3. Pull `ABC Classification` field
4. Apply any mid-cycle override from `ABC_OVERRIDE` dict in `scripts/build_report.py` (rare — only when SAP changes between weekly exports)

---

## Where each code shows up in the report

| Code | Routing |
|---|---|
| A · B · C · D | **Main views** — Weekly Summary, Inventory Overview, Priority Actions, brand tabs |
| E | **Main views** + eligible for **🔚 Phase-Out Review (E→Z)** tab if 0 stock + 0 velocity |
| F · I · S · Z | **📦 Sales BOMs & Other tab only** — filtered out of all main views |

---

## Color palette in the report

Every ABC badge in the workbook uses these colors. The **ABC legend strip** at the top of every stock-data tab shows them in a single horizontal row.

| Badge color | Code |
|---|---|
| 🟦 Deep teal | A — High Vol |
| 🟪 Indigo | B — Med Vol |
| 🟫 Plum | C — Low Vol |
| 🟪 Lavender | D — Phase In |
| 🟧 Burnt sienna | E — Phase Out |
| ⬜ Slate | F — Other |
| 🟦 Steel blue | I — Ind. Comp. |
| 🟫 Khaki / sand | S — Sales BOM |
| ⬛ Charcoal | Z — Obsolete |

ABC badges use a teal/indigo/plum/slate family so they're visually distinct from the muted brick/amber/sage palette used for **status** (Stockout / Critical / Warning / Healthy / Inactive).

If a row shows `—` instead of a badge, it means the item's UPC isn't in the SAP item master.

---

## Decision rules tied to ABC

| When you see... | What to do |
|---|---|
| **A** item flagged as low DOS | URGENT — A's drive revenue, never stock out |
| **B** item flagged as low DOS | Reorder normally — keep standard buffer |
| **C** item flagged as low DOS | Stock out is ok — assess whether to keep replenishing |
| **D** item with rising velocity | Watch — reclassify to A/B/C as it stabilizes |
| **E** item with 0 on hand + 0 velocity | Candidate for **Z** reclassification → see Phase-Out Review tab |
| **F** item appearing on main view | Probably old data — re-pull SAP item master |
| **I** item appearing on main view | Should not happen — components shouldn't be in sales reports. Investigate why it's tagged as a salable SKU. |
| **S** (Sales BOM) shows in main report | Re-pull SAP item master — likely stale classification |
| **Z** item still in active listings | Remove from sales channels — clean up listings |

---

## SAP refresh cadence

**As needed only — not on a fixed schedule.** Refresh whenever SAP classifications actually change. Don't include in the weekly Monday flow — leave the existing `item_master.xlsx` alone unless SAP changes need to flow through.

Workflow when a refresh IS needed (per the [[06 Processes & SOPs/(C) Weekly Inputs Sourcing SOP]]):
1. SAP admin runs **ABC Classification** export → `SAPABCCLASSIFICATION.xlsx` lands in Downloads
2. Rename to `item_master.xlsx`
3. Replace `reports\item-master\item_master.xlsx`
4. Old version auto-archived as `item_master_old_YYYY-MM-DD.xlsx`

---

*Updated: May 5, 2026*
*Reference: SAP `SAPABCCLASSIFICATION.xlsx` export (Item No. · Item Description · ItemBranch · ABC Classification)*
