"""
Parsers for each external system's CSV/Excel exports.

Each parser normalizes the source's column names into a standard dict with these keys:
  - sku (required)
  - product_name
  - inventory_level
  - sales_velocity
  - demand_forecast_30d / 60d / 90d
  - reorder_quantity
  - reorder_point
  - days_of_stock
  - extra_data (dict of any additional fields)

Parsers are deliberately flexible — they try multiple common column name variations
so users don't have to perfectly match the expected format.
"""
import pandas as pd
import io
import logging

logger = logging.getLogger(__name__)


def _find_column(df, candidates, required=False):
    """Find the first matching column from a list of candidates (case-insensitive)."""
    df_cols_lower = {c.lower().strip(): c for c in df.columns}
    for candidate in candidates:
        if candidate.lower().strip() in df_cols_lower:
            return df_cols_lower[candidate.lower().strip()]
    if required:
        raise ValueError(f"Could not find required column. Tried: {candidates}. Available: {list(df.columns)}")
    return None


def _safe_decimal(val):
    """Convert a value to float, returning None if not possible."""
    if pd.isna(val) or val == '' or val is None:
        return None
    try:
        cleaned = str(val).replace(',', '').replace('$', '').strip()
        if cleaned == '' or cleaned == '-':
            return None
        return float(cleaned)
    except (ValueError, TypeError):
        return None


def read_file_to_dataframe(file_obj, filename):
    """Read a CSV or Excel file into a pandas DataFrame."""
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    if ext in ('xlsx', 'xls', 'xlsm'):
        return pd.read_excel(io.BytesIO(file_obj.read()), engine='openpyxl')
    elif ext == 'csv':
        content = file_obj.read()
        # Try UTF-8 first, fall back to latin-1
        try:
            return pd.read_csv(io.BytesIO(content), encoding='utf-8')
        except UnicodeDecodeError:
            return pd.read_csv(io.BytesIO(content), encoding='latin-1')
    elif ext == 'tsv':
        content = file_obj.read()
        return pd.read_csv(io.BytesIO(content), sep='\t')
    else:
        raise ValueError(f"Unsupported file type: .{ext}. Please upload .csv, .xlsx, or .tsv")


def parse_generic(df):
    """
    Generic parser — tries to auto-detect column names using common patterns.
    Works as a fallback for any system without a dedicated parser.
    """
    sku_col = _find_column(df, [
        'SKU', 'sku', 'Item No', 'Item Number', 'item_no', 'ASIN', 'asin',
        'Product ID', 'product_id', 'Barcode', 'UPC', 'MSKU', 'Merchant SKU',
        'Seller SKU', 'seller-sku', 'Item ID', 'item_id',
    ], required=True)

    name_col = _find_column(df, [
        'Product Name', 'product_name', 'Description', 'description', 'Title',
        'title', 'Product Title', 'Item Name', 'item_name', 'Product',
    ])

    inv_col = _find_column(df, [
        'Inventory', 'inventory', 'Stock', 'stock', 'Quantity', 'qty',
        'Available', 'available', 'On Hand', 'on_hand', 'In Stock',
        'afn-fulfillable-quantity', 'FBA Inventory', 'Stock Level',
        'Fulfillable Quantity', 'Total Inventory',
    ])

    vel_col = _find_column(df, [
        'Sales Velocity', 'sales_velocity', 'Velocity', 'Daily Sales',
        'Avg Daily Sales', 'Units/Day', 'units_per_day', 'Daily Avg',
        'Average Daily Sales', 'Avg Sales', 'Daily Units',
    ])

    forecast_30_col = _find_column(df, [
        '30 Day Forecast', '30d Forecast', 'Forecast 30', 'forecast_30d',
        '30 Day Demand', 'Demand 30', '30-day forecast', 'Next 30 Days',
    ])

    forecast_60_col = _find_column(df, [
        '60 Day Forecast', '60d Forecast', 'Forecast 60', 'forecast_60d',
        '60 Day Demand', 'Demand 60', '60-day forecast', 'Next 60 Days',
    ])

    forecast_90_col = _find_column(df, [
        '90 Day Forecast', '90d Forecast', 'Forecast 90', 'forecast_90d',
        '90 Day Demand', 'Demand 90', '90-day forecast', 'Next 90 Days',
    ])

    reorder_col = _find_column(df, [
        'Reorder Qty', 'reorder_qty', 'Reorder Quantity', 'Recommended Order',
        'Suggested Order', 'Order Qty', 'Replenishment Qty',
    ])

    reorder_pt_col = _find_column(df, [
        'Reorder Point', 'reorder_point', 'Min Stock', 'Safety Stock',
    ])

    dos_col = _find_column(df, [
        'Days of Stock', 'days_of_stock', 'DOS', 'Days Supply',
        'Days of Supply', 'Days Remaining', 'Stock Days',
        'Days of Inventory', 'DOI',
    ])

    # Standard field columns
    standard_cols = {c for c in [sku_col, name_col, inv_col, vel_col,
                                  forecast_30_col, forecast_60_col, forecast_90_col,
                                  reorder_col, reorder_pt_col, dos_col] if c}

    rows = []
    for _, row in df.iterrows():
        sku_val = str(row[sku_col]).strip() if pd.notna(row[sku_col]) else ''
        if not sku_val:
            continue

        # Collect extra data (non-standard columns)
        extra = {}
        for col in df.columns:
            if col not in standard_cols and pd.notna(row[col]):
                extra[col] = str(row[col])

        rows.append({
            'sku': sku_val,
            'product_name': str(row[name_col]).strip() if name_col and pd.notna(row[name_col]) else '',
            'inventory_level': _safe_decimal(row[inv_col]) if inv_col else None,
            'sales_velocity': _safe_decimal(row[vel_col]) if vel_col else None,
            'demand_forecast_30d': _safe_decimal(row[forecast_30_col]) if forecast_30_col else None,
            'demand_forecast_60d': _safe_decimal(row[forecast_60_col]) if forecast_60_col else None,
            'demand_forecast_90d': _safe_decimal(row[forecast_90_col]) if forecast_90_col else None,
            'reorder_quantity': _safe_decimal(row[reorder_col]) if reorder_col else None,
            'reorder_point': _safe_decimal(row[reorder_pt_col]) if reorder_pt_col else None,
            'days_of_stock': _safe_decimal(row[dos_col]) if dos_col else None,
            'extra_data': extra,
            'raw_row': {str(k): str(v) for k, v in row.to_dict().items() if pd.notna(v)},
        })

    return rows


# ──────────────────────────────────────────────────────────────────────
# System-specific parsers (override column names when formats are known)
# ──────────────────────────────────────────────────────────────────────

def parse_sostocked(df):
    """Parse SoStocked inventory/forecast export."""
    return parse_generic(df)


def parse_valogix(df):
    """Parse Valogix demand planning export."""
    return parse_generic(df)


def parse_amazon(df):
    """Parse Amazon Seller Central inventory report."""
    # Amazon uses ASIN or Seller SKU — rename to generic before passing
    renames = {}
    for col in df.columns:
        cl = col.lower().strip()
        if cl in ('asin', 'seller-sku', 'seller sku', 'msku'):
            renames[col] = 'SKU'
        elif cl in ('product-name', 'product name', 'item-name'):
            renames[col] = 'Product Name'
        elif cl in ('afn-fulfillable-quantity', 'available'):
            renames[col] = 'Inventory'
    if renames:
        df = df.rename(columns=renames)
    return parse_generic(df)


def parse_shopify(df):
    """Parse Shopify product/inventory export."""
    renames = {}
    for col in df.columns:
        cl = col.lower().strip()
        if cl in ('variant sku', 'variant barcode'):
            renames[col] = 'SKU'
        elif cl == 'title':
            renames[col] = 'Product Name'
        elif cl in ('available', 'inventory quantity', 'on hand'):
            renames[col] = 'Inventory'
    if renames:
        df = df.rename(columns=renames)
    return parse_generic(df)


def parse_tiktok(df):
    """Parse TikTok Shop product/performance export."""
    renames = {}
    for col in df.columns:
        cl = col.lower().strip()
        if cl in ('seller sku', 'product id', 'sku id'):
            renames[col] = 'SKU'
        elif cl in ('product name', 'product title'):
            renames[col] = 'Product Name'
        elif cl in ('available stock', 'warehouse stock', 'stock'):
            renames[col] = 'Inventory'
    if renames:
        df = df.rename(columns=renames)
    return parse_generic(df)


def parse_walmart(df):
    """Parse Walmart Marketplace item/inventory export."""
    renames = {}
    for col in df.columns:
        cl = col.lower().strip()
        if cl in ('sku', 'item id', 'partner id'):
            renames[col] = 'SKU'
        elif cl in ('product name', 'item name'):
            renames[col] = 'Product Name'
        elif cl in ('available quantity', 'available', 'quantity'):
            renames[col] = 'Inventory'
    if renames:
        df = df.rename(columns=renames)
    return parse_generic(df)


def parse_shipbob(df):
    """Parse ShipBob inventory export."""
    renames = {}
    for col in df.columns:
        cl = col.lower().strip()
        if cl in ('sku', 'reference id'):
            renames[col] = 'SKU'
        elif cl in ('name', 'product name'):
            renames[col] = 'Product Name'
        elif cl in ('fulfillable quantity', 'on hand', 'available'):
            renames[col] = 'Inventory'
    if renames:
        df = df.rename(columns=renames)
    return parse_generic(df)


# ──────────────────────────────────────────────────────────────────────
# Parser registry
# ──────────────────────────────────────────────────────────────────────

PARSERS = {
    'sostocked': parse_sostocked,
    'valogix': parse_valogix,
    'amazon': parse_amazon,
    'shopify': parse_shopify,
    'tiktok': parse_tiktok,
    'walmart': parse_walmart,
    'shipbob': parse_shipbob,
    'other': parse_generic,
}


def get_parser(system_type):
    """Return the parser function for the given system type."""
    return PARSERS.get(system_type, parse_generic)
