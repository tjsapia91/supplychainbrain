# Tab 14 — 🏷 Bundles & Custom SKUs

**Purpose:** Holds items with non-UPC SKUs (bundles, custom codes) + combo/special items (ABC=S) + special-account items (CVS NFMD UPC) — kept OUT of the main views to avoid cluttering brand / marketplace / inventory tabs.

---

## Three Sections

### Section 1 — Non-UPC SKUs

Items where the SKU is alphanumeric or has letters (not a clean 12-digit UPC). Examples:
- `BODYBRBLK` — Soniclear Replacement Body Brush Head
- `SSLB-PACK` — SS Lela & Blade bundle
- `DELSENBRSH` — Michael Todd Beauty bundle
- `MT-702877109441` — MTB-prefixed UPC (still mostly numeric but with prefix)

These flow through Amazon tabs normally, but the SKU column shows the raw code (not a UPC).

### Section 2 — Combos & Specials (ABC = S)

Items with `ABC Classification = S` in item_master — sales BOMs, gift sets, multi-unit packs that don't have their own per-SKU inventory but ship as the combination of underlying items.

Filter: `item_master["ABC Classification"] == "S"`.

### Section 3 — Special Account Items

Items routed to specific retail accounts (currently 2 items: CVS NFMD UPC 850038082314).

Filter: hard-coded `SPECIAL_ACCOUNT_UPCS` set in build_report.py.

---

## Columns

Same `INV_COLS` (Inventory Overview column set) as the brand tabs. Identity + stock + DOS + forecast. See [[(C) 01 - Amazon US]] for the most detailed column-by-column breakdown — the column set here is similar but tab uses INV_COLS instead of MP_COLS.

---

## Why Items Land Here Instead of Brand Tabs

By segregating these:
- Brand tabs (MTB / SS / NFMD) show CLEAN per-brand views without bundle noise
- Multi-Channel + Inventory Overview don't double-count units (the bundle ships as components, not as a separate SKU)
- Combo items don't trigger PO alerts (you'd reorder the COMPONENTS, not the bundle)

---

## Source Files

This tab is filtered FROM `data["all_items"]` using:

```python
is_non_upc_sku = lambda sku: not str(sku).split(".")[0].isdigit() or len(str(sku).split(".")[0]) < 11

# Section 1: non-UPC SKUs
non_upc_items = [i for i in all_items if is_non_upc_sku(i.get("sku", ""))]

# Section 2: S-class items
s_items = [i for i in all_items if (i.get("abc","") or "").strip().upper().startswith("S")]

# Section 3: Special accounts
SPECIAL_ACCOUNT_UPCS = {"850038082314", ...}
special_items = [i for i in all_items if str(i.get("sku","")).split(".")[0] in SPECIAL_ACCOUNT_UPCS]
```

These items are also REMOVED from main views so they only appear here.

---

## Common Operations

| Task | What to look at |
|---|---|
| "Where did my bundle SKU go?" | Section 1 — Non-UPC SKUs |
| "How do I treat sales BOMs?" | Section 2 — Combos & Specials; reorder the underlying components |
| "Where are the CVS items?" | Section 3 — Special Account Items |
