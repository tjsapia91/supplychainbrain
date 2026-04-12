import math
from datetime import datetime, timedelta


def calculate_cartons(upc_master_carton_qty, qty):
    """Calculate number of master cartons needed for given quantity"""
    if upc_master_carton_qty and upc_master_carton_qty > 0:
        return math.ceil(qty / upc_master_carton_qty)
    return None


def calculate_cbm(master_carton_volume, cartons):
    """Calculate CBM for given number of cartons"""
    if cartons and master_carton_volume and master_carton_volume > 0:
        return float(cartons) * float(master_carton_volume) * 0.0000163871
    return None


def format_date(date_obj):
    """Format date to string"""
    if date_obj:
        return date_obj.strftime('%Y-%m-%d')
    return ''


def get_business_day_offset(days=0):
    """Get date offset by business days"""
    current = datetime.now()
    for _ in range(abs(days)):
        if days > 0:
            current += timedelta(days=1)
            if current.weekday() >= 5:
                current += timedelta(days=2)
        else:
            current -= timedelta(days=1)
            if current.weekday() >= 5:
                current -= timedelta(days=2)
    return current.date()
