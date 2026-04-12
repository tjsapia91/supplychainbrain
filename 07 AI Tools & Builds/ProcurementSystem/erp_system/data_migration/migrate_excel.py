"""
Data Migration Script for Michael Todd Beauty ERP System
Imports data from exported JSON files into Django models
"""

import os
import sys
import json
import django
from datetime import datetime
import math

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp.settings')
django.setup()

from items.models import Item
from vendors.models import Vendor, BillToAddress, ShipToAddress, Branch, ThreePLProvider
from inventory.models import Warehouse


def load_json_file(filepath):
    """Load JSON data from file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: File not found: {filepath}")
        return None
    except json.JSONDecodeError:
        print(f"ERROR: Invalid JSON in file: {filepath}")
        return None


def is_nan(value):
    """Check if a value is None, NaN, or NaT"""
    if value is None:
        return True
    if isinstance(value, str) and value.strip().lower() in ('', 'nan', 'nat', 'none'):
        return True
    if isinstance(value, float) and math.isnan(value):
        return True
    return False


def parse_date(date_value):
    """Parse date value, handle NaT and None"""
    if is_nan(date_value):
        return None
    if isinstance(date_value, str):
        try:
            # Handle datetime strings like "2025-01-15 00:00:00"
            return datetime.strptime(date_value.split(' ')[0], '%Y-%m-%d').date()
        except ValueError:
            return None
    return date_value


def map_abc_classification(value):
    """Map Excel ABC classification to model choices"""
    if not value or is_nan(value):
        return ''

    mapping = {
        'A High Vol': 'A',
        'C Low Vol': 'C',
        'D Phase-In': 'D',
        'E Phase-Out': 'E',
        'F Other': 'F',
        'I Ind. Comp.': 'I',
    }
    return mapping.get(str(value), '')


def to_bool(value):
    """Convert string to boolean"""
    if value is None or is_nan(value):
        return False
    if isinstance(value, bool):
        return value
    return str(value).lower() == 'yes'


def safe_int(value, default=0):
    """Safely convert to int"""
    if value is None or is_nan(value):
        return default
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return default


def safe_float(value, default=0.0):
    """Safely convert to float"""
    if value is None or is_nan(value):
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def safe_string(value, default=''):
    """Safely convert to string"""
    if value is None or is_nan(value):
        return default
    return str(value).strip()


def import_items(item_data_path, default_warehouse):
    """Import items from JSON"""
    print("Importing items...", end=' ', flush=True)

    data = load_json_file(item_data_path)
    if not data:
        print("FAILED")
        return 0

    created_count = 0
    updated_count = 0

    for item_dict in data:
        try:
            item_no = safe_string(item_dict.get('Item No.'))
            if not item_no:
                continue

            defaults = {
                'description': safe_string(item_dict.get('Item Description')),
                'in_stock': safe_float(item_dict.get('In Stock')),
                'default_warehouse': default_warehouse,
                'last_purchase_date': parse_date(item_dict.get('Last Purchase Date')),
                'qty_ordered_by_customers': safe_int(item_dict.get('Qty Ordered by Customers')),
                'abc_classification': map_abc_classification(item_dict.get('ABC Classification')),
                'qty_ordered_from_vendors': safe_int(item_dict.get('Qty Ordered from Vendors')),
                'property_1': safe_string(item_dict.get('Property 1'), 'No'),
                'property_2': safe_string(item_dict.get('Property 2'), 'No'),
                'height_uom': safe_float(item_dict.get('Height 1 - UoM for Purchasing')) or None,
                'length_uom': safe_float(item_dict.get('Length 1 - UoM for Purchasing')) or None,
                'width_uom': safe_float(item_dict.get('Width 1 - UoM for Purchasing')) or None,
                'weight_uom': safe_float(item_dict.get('Weight 1 - UoM for Purchasing')) or None,
                'superseding_item': safe_string(item_dict.get('Superseding Item')),
                'upc_inner_carton_qty': safe_int(item_dict.get('UPC Inner Carton Quantity')),
                'upc_master_carton_qty': safe_int(item_dict.get('UPC Master Carton Quantity')),
                'master_carton_volume': safe_float(item_dict.get('M/Carton Volume (Inches)')),
                'issue_price': safe_float(item_dict.get('Issue Price')),
                'height_purchasing_unit': safe_float(item_dict.get('Height 1 - Purchasing Unit')) or None,
                'inactive': to_bool(item_dict.get('Inactive')),
                'branch': safe_string(item_dict.get('Branch')),
            }

            item, created = Item.objects.update_or_create(
                item_no=item_no,
                defaults=defaults
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        except Exception as e:
            print(f"ERROR processing item {item_dict.get('Item No.')}: {str(e)}")
            continue

    total = created_count + updated_count
    print(f"{total} items imported ({created_count} new, {updated_count} updated).")
    return total


def import_vendors(vendor_data_path):
    """Import vendors from JSON"""
    print("Importing vendors...", end=' ', flush=True)

    data = load_json_file(vendor_data_path)
    if not data:
        print("FAILED")
        return 0

    created_count = 0

    for vendor_dict in data:
        try:
            name = safe_string(vendor_dict.get('Name'))
            if not name:
                continue

            # Parse contact field "Name - email@example.com"
            contact_name = ''
            contact_email = ''
            contact_field = safe_string(vendor_dict.get('Contact'))
            if contact_field and ' - ' in contact_field:
                parts = contact_field.split(' - ')
                contact_name = parts[0].strip()
                contact_email = parts[1].strip() if len(parts) > 1 else ''

            defaults = {
                'address': safe_string(vendor_dict.get('Address')),
                'city': safe_string(vendor_dict.get('City')),
                'phone': safe_string(vendor_dict.get('Phone')),
                'postal_code': safe_string(vendor_dict.get('Code')),
                'contact_name': contact_name,
                'contact_email': contact_email,
            }

            vendor, created = Vendor.objects.update_or_create(
                name=name,
                defaults=defaults
            )

            if created:
                created_count += 1

        except Exception as e:
            print(f"ERROR processing vendor {vendor_dict.get('Name')}: {str(e)}")
            continue

    print(f"{created_count} vendor imported.")
    return created_count


def import_bill_to_addresses(billto_data_path):
    """Import bill-to addresses from JSON"""
    print("Importing bill-to addresses...", end=' ', flush=True)

    data = load_json_file(billto_data_path)
    if not data:
        print("FAILED")
        return 0

    created_count = 0

    for billto_dict in data:
        try:
            branch = safe_string(billto_dict.get('Branch'))
            if not branch:
                continue

            defaults = {
                'address': safe_string(billto_dict.get('Address')),
                'phone': safe_string(billto_dict.get('Phone #')),
                'contact': safe_string(billto_dict.get('Contact')),
                'is_default': branch == 'Micahel Todd Beauty',  # Set first one as default (note typo in data)
            }

            billto, created = BillToAddress.objects.update_or_create(
                branch=branch,
                defaults=defaults
            )

            if created:
                created_count += 1

        except Exception as e:
            print(f"ERROR processing bill-to address {billto_dict.get('Branch')}: {str(e)}")
            continue

    print(f"{created_count} addresses imported.")
    return created_count


def create_default_warehouse():
    """Create default Michael Todd Beauty HQ warehouse"""
    print("Creating default warehouse...", end=' ', flush=True)

    try:
        warehouse, created = Warehouse.objects.get_or_create(
            code='MTB-HQ',
            defaults={
                'name': 'Michael Todd Beauty - HQ Warehouse',
                'address': '548 NW University Blvd., Suite 600, Port St. Lucie, FL 34986',
                'is_active': True,
            }
        )
        print("done.")
        return warehouse
    except Exception as e:
        print(f"FAILED: {str(e)}")
        return None


def create_default_ship_to():
    """Create default Michael Todd Beauty HQ ship-to address"""
    print("Creating default ship-to address...", end=' ', flush=True)

    try:
        ship_to, created = ShipToAddress.objects.get_or_create(
            name='Michael Todd Beauty - HQ',
            defaults={
                'address': '548 NW University Blvd., Suite 600',
                'city': 'Port St. Lucie',
                'state': 'FL',
                'zip_code': '34986',
                'country': 'USA',
                'is_default': True,
            }
        )
        print("done.")
        return ship_to
    except Exception as e:
        print(f"FAILED: {str(e)}")
        return None


def create_branches():
    """Create company branches: Michael Todd Beauty, Spa Sciences, NasalFresh MD"""
    print("Creating branches...", end=' ', flush=True)

    branches_data = [
        {
            'name': 'Michael Todd Beauty',
            'address': '548 NW University Blvd., Suite 600\nPort St. Lucie, FL 34986',
            'phone': '1-772-446-0149',
            'contact_email': 'supplychain@michaeltoddbeauty.com',
            'is_active': True,
        },
        {
            'name': 'Spa Sciences',
            'address': '548 NW University Blvd., Suite 600\nPort St. Lucie, FL 34986',
            'phone': '1-772-446-0149',
            'contact_email': 'supplychain@spasciences.com',
            'is_active': True,
        },
        {
            'name': 'NasalFresh MD',
            'address': '548 NW University Blvd., Suite 600\nPort St. Lucie, FL 34986',
            'phone': '1-772-446-0149',
            'contact_email': 'supplychain@nasalfreshmd.com',
            'is_active': True,
        },
    ]

    created_count = 0
    for branch_data in branches_data:
        try:
            name = branch_data.pop('name')
            branch, created = Branch.objects.get_or_create(
                name=name,
                defaults=branch_data
            )
            if created:
                created_count += 1
        except Exception as e:
            print(f"ERROR creating branch: {str(e)}")

    print(f"{created_count} branches created.")
    return created_count


def create_threepl_providers():
    """Create 3PL fulfillment providers: ShipBob, Floship, Amazon FBA"""
    print("Creating 3PL providers...", end=' ', flush=True)

    providers_data = [
        {
            'name': 'ShipBob',
            'code': 'SB',
            'address': 'TBD - Add ShipBob warehouse address',
            'city': '',
            'state': '',
            'zip_code': '',
            'country': 'USA',
            'phone': '',
            'contact_name': '',
            'contact_email': '',
            'account_number': '',
            'notes': 'Primary 3PL fulfillment partner. Update address after setup.',
            'is_active': True,
        },
        {
            'name': 'Floship',
            'code': 'FS',
            'address': 'TBD - Add Floship warehouse address',
            'city': '',
            'state': '',
            'zip_code': '',
            'country': '',
            'phone': '',
            'contact_name': '',
            'contact_email': '',
            'account_number': '',
            'notes': 'International 3PL fulfillment partner. Update address after setup.',
            'is_active': True,
        },
        {
            'name': 'Amazon FBA',
            'code': 'AMZ',
            'address': 'TBD - Add Amazon FBA warehouse address',
            'city': '',
            'state': '',
            'zip_code': '',
            'country': 'USA',
            'phone': '',
            'contact_name': '',
            'contact_email': '',
            'account_number': '',
            'notes': 'Amazon FBA fulfillment. Update address after setup.',
            'is_active': True,
        },
    ]

    created_count = 0
    for provider_data in providers_data:
        try:
            name = provider_data.pop('name')
            code = provider_data.pop('code')
            provider, created = ThreePLProvider.objects.get_or_create(
                name=name,
                code=code,
                defaults=provider_data
            )
            if created:
                created_count += 1
        except Exception as e:
            print(f"ERROR creating 3PL provider: {str(e)}")

    print(f"{created_count} 3PL providers created.")
    return created_count


def main():
    """Main migration function"""
    print("=" * 60)
    print("Michael Todd Beauty ERP - Data Migration")
    print("=" * 60)
    print()

    # Determine base path for data files (same directory as this script)
    base_path = os.path.dirname(os.path.abspath(__file__))

    item_data_path = os.path.join(base_path, 'item_data.json')
    seller_data_path = os.path.join(base_path, 'seller_data.json')
    billto_data_path = os.path.join(base_path, 'billto_data.json')

    # Create default structures first
    default_warehouse = create_default_warehouse()
    default_ship_to = create_default_ship_to()

    # Create branches and 3PL providers
    create_branches()
    create_threepl_providers()
    print()

    # Import main data
    import_vendors(seller_data_path)
    import_bill_to_addresses(billto_data_path)
    import_items(item_data_path, default_warehouse)

    print()
    print("=" * 60)
    print("Migration complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()
