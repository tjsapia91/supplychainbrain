"""
Management command: backup_intransit_log

Exports the current in-transit container data as a CSV and uploads it
to OneDrive under Backups/InTransitLog/FY{year}/.

Fiscal year runs Jul 1 - Jun 30.
Usage:
    python manage.py backup_intransit_log          # auto-detect fiscal year
    python manage.py backup_intransit_log --fy 2026
"""
import csv
import io
from datetime import date

from django.core.management.base import BaseCommand

from containers.models import ContainerPlan


def get_fiscal_year(d=None):
    """Return fiscal year (Jul-Jun). e.g. Jul 2025 - Jun 2026 -> FY2026"""
    d = d or date.today()
    return d.year if d.month >= 7 else d.year


class Command(BaseCommand):
    help = 'Backup in-transit container log to OneDrive'

    def add_arguments(self, parser):
        parser.add_argument('--fy', type=int, help='Fiscal year override (default: auto)')

    def handle(self, *args, **options):
        from integrations.onedrive import sync_intransit_log_backup, is_connected

        if not is_connected():
            self.stderr.write(self.style.ERROR('OneDrive is not connected. Run /oauth/connect/ first.'))
            return

        fy = options.get('fy') or get_fiscal_year()
        today = date.today().strftime('%Y-%m-%d')

        # Gather in-transit containers (all non-completed, non-cancelled)
        containers = ContainerPlan.objects.exclude(
            status__in=['completed', 'cancelled']
        ).select_related().prefetch_related('items', 'items__item')

        if not containers.exists():
            self.stdout.write('No active containers to back up.')
            return

        # Build CSV in memory
        buf = io.StringIO()
        writer = csv.writer(buf)

        # Header row
        writer.writerow([
            'Plan #', 'Container #', 'Status', 'Container Type',
            'Forwarder', 'Booking Ref', 'Incoterms', 'Routing',
            'Port of Loading', 'Port of Discharge', 'Warehouse',
            'Target Load Date', 'Actual Load Date', 'Date Sailed',
            'ETA Port', 'Warehouse Delivery',
            'Total CBM', 'Max CBM', 'CBM %',
            'Total Weight', 'Total Cartons', 'Total Units', 'Total Value',
            'Line Items (SKU x Qty -> Dest)',
        ])

        for c in containers:
            items_summary = '; '.join(
                f'{i.item.item_no if i.item else "?"} x{i.quantity} -> {i.destination}'
                for i in c.items.all()
            )
            writer.writerow([
                c.plan_number, c.container_number, c.get_status_display(),
                c.get_container_type_display(),
                c.forwarder, c.booking_reference, c.incoterms, c.routing_notes,
                c.port_of_loading, c.port_of_discharge, c.receiving_warehouse,
                c.target_load_date, c.actual_load_date, c.date_sailed,
                c.eta_port, c.warehouse_delivery_date,
                c.total_cbm, c.max_cbm, f'{c.cbm_utilization}%',
                c.total_weight, c.total_cartons, c.total_units, c.total_value,
                items_summary,
            ])

        csv_content = buf.getvalue().encode('utf-8')
        filename = f'InTransitLog_{today}.csv'

        try:
            sync_intransit_log_backup(fy, filename, csv_content, 'text/csv')
            self.stdout.write(self.style.SUCCESS(
                f'Backed up {containers.count()} containers to '
                f'OneDrive: Backups/InTransitLog/FY{fy}/{filename}'
            ))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Backup failed: {e}'))
