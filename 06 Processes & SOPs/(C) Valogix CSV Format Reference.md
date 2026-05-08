# (C) Valogix CSV Format Reference — `Item-Location-History-Forecast`

> Canonical column structure for the Valogix `schain_itemLocationHistoryForecast_*.csv` weekly export. Use this as the definitive reference whenever building scripts, parsers, or one-offs against this file. Updated and confirmed by Tommy: May 8, 2026.

---

## File pattern

`schain_itemLocationHistoryForecast_YYYY_MM_DD.csv`

Default location for weekly pipeline: `reports/valogix/`
One-off pulls land in `Downloads/`.

---

## Column layout (left → right, in CSV order)

| # | Block | Columns | Description |
|---|---|---|---|
| 1 | **Identity** | `Item Number` · `Description` · `Location` · `Supplier` | UPC, product name, warehouse code, supplier name |
| 2 | **History (24+ months actuals)** | `24-May` · `24-Jun` · `24-Jul` · ... · `26-Apr` · `26-May` | Each column = one month of historical actual sales/usage. Format: `YY-MMM` where YY is 2-digit year (e.g. `24` = 2024) and MMM is 3-letter month abbreviation. **The current calendar month appears here in partial form** (sales-to-date) and also again under Projected Forecast (with a `.1` suffix). |
| 3 | **History aggregates** | `History Total` · `Current Rolling 12 (history)` | Total of all historical months · trailing-12-months sum |
| 4 | **Projected Forecast (forward)** | `26-May.1` · `26-Jun` · `26-Jul` · ... · `27-Nov` | Each column = forward-looking projected forecast for that month. The `.N` suffix on the first column is pandas' auto-deduplication marker — Valogix repeats the current month's name (because it appears in both History as partial-month and Forecast as projection); pandas adds `.1` to the second occurrence. Subsequent forecast months don't collide with history names so they appear plain. |
| 5 | **Forecast aggregate** | `Forecast Total (Next 12 Months)` | Sum of the next 12 forward months |
| 6 | **Metadata / planning fields** | `Inventory Cost` · `Reorder Point` · `Lead Time` · `On Hand` · `Committed` · `On Order Total` · `Seasonal Metric` · `Planning Group` · `Item Class` · `Forecast Type` · `Forecast Flag` · `Service Level` · `BOM Parent` · `BOM Child` · `Phase In` · `Phase Out` · `Priority Code` · `Supersedes Item` · `Forecast PH` · `Local (Independent) Short/Long History Average` · `(Combined) Short/Long History Average` | Single-value scalar fields per item-location row. |

---

## Date parsing — handle both formats

Valogix has used two date-column formats over time:

- **Old (YY-MMM):** `26-Apr` → April 2026
- **New (MMM-YY):** `Apr-26` → April 2026 *(current as of May 2026)*

Parser must accept both. See `_col_date_key()` in `scripts/build_report.py` — already supports both forms.

---

## Distinguishing History vs Projected Forecast columns

A column is **Projected Forecast** if it has a `.N` pandas-dedup suffix (`26-May.1`) OR if its (year, month) is ≥ today's calendar month.

A column is **History** if it has no suffix AND its (year, month) is < today's calendar month.

The current month is special — it appears in BOTH blocks (partial actual on the left side, full projection on the right side).

```python
def is_history(col):  # plain MMM-YY or YY-MMM, no suffix
    return bool(re.match(r"^\d{2}-[A-Za-z]{3}$", col)
              or re.match(r"^[A-Za-z]{3}-\d{2}$", col))

def is_forecast(col):  # has .N suffix (current-month duplicate marker)
    return bool(re.match(r"^\d{2}-[A-Za-z]{3}\.\d+$", col)
              or re.match(r"^[A-Za-z]{3}-\d{2}\.\d+$", col))
```

To split the full timeline cleanly, find the index of the first `.N`-suffixed column. Everything before is History; everything from that index onward is Projected Forecast (including plain-named forward months that come after the duplicate-suffix anchor).

---

## Locations the pipeline cares about

Filter to these `Location` codes for the weekly report:

| Location | Display name | Channel |
|---|---|---|
| `SBGA-MT` | Shopify MTB | Shopify |
| `SBGA-SS` | Spa Sciences DTC SS | Shopify (split: NFMD products remap to `SBGA-SS-NFMD`) |
| `FLO-MTB` | Floship Intl | Floship Intl |
| `WM-SS` | Walmart SS | Walmart |
| `AMZN-MT`, `AMZN-SS` | Amazon supplier-on-order | Amazon US (used for the `ON ORDER (SUPPLIER)` column) |

Other locations (`AM - MTB`, `AM - SS`, `BERLINSS`, `OXYGENSS`, `CHRATLSS`, etc.) are legacy/unused and can be ignored.

---

## Common Valogix one-offs that read this file

- `scripts/build_report.py::load_valogix()` — main weekly loader
- `scripts/build_report.py::load_amazon_supplier_on_order()` — pulls AMZN-MT/SS open-PO totals
- `scripts/one_off_valogix_forecast_variance.py` — Forecast-vs-Historical variance analysis (Valogix-style stacked card per item)

---

## Authoritative answer to "where's the Projected Forecast?"

**The Projected Forecast IS the forward forecast columns** (right side of the CSV after the `.N`-suffixed marker). There is **no separate "Projected" data series** in this CSV — Valogix's UI may show multiple forecast types (Effective, Combined, Local, etc.) via dropdowns, but the CSV export contains only one set of monthly forecast values.

If a future workflow needs a different forecast type (e.g. "Local Independent Forecast"), it would need to be exported as a separate Valogix report and merged in by UPC + month.

---

*Created: May 8, 2026 · Updated as canonical reference per Tommy's instruction*
