import json
import logging
from datetime import date, timedelta
from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Max, Count, Avg, F
from django.http import JsonResponse
from django.utils import timezone
from django.core.paginator import Paginator

from items.models import Item
from .models import ReportSource, UploadedReport, ReportData, FulfillmentLocation
from .forms import ReportUploadForm
from .parsers import read_file_to_dataframe, get_parser

logger = logging.getLogger(__name__)


@login_required
def reports_hub(request):
    """Main Reports Hub dashboard — unified view of all external system data."""
    sources = ReportSource.objects.filter(is_active=True)
    recent_uploads = UploadedReport.objects.select_related('report_source', 'uploaded_by')[:10]

    # Get latest data per source
    source_stats = []
    for source in sources:
        latest = ReportData.objects.filter(report_source=source).order_by('-data_date').first()
        row_count = ReportData.objects.filter(report_source=source).count()
        last_upload = UploadedReport.objects.filter(
            report_source=source, processing_status='success'
        ).order_by('-uploaded_at').first()
        source_stats.append({
            'source': source,
            'latest_date': latest.data_date if latest else None,
            'row_count': row_count,
            'last_upload': last_upload,
        })

    # Summary stats
    total_skus = ReportData.objects.values('sku').distinct().count()
    matched_skus = ReportData.objects.filter(item__isnull=False).values('sku').distinct().count()

    # Alerts: items with low/critical stock
    critical_items = ReportData.objects.filter(
        days_of_stock__isnull=False,
        days_of_stock__lte=14,
    ).select_related('report_source', 'item').order_by('days_of_stock')[:10]

    low_items = ReportData.objects.filter(
        days_of_stock__isnull=False,
        days_of_stock__gt=14,
        days_of_stock__lte=30,
    ).select_related('report_source', 'item').order_by('days_of_stock')[:10]

    context = {
        'sources': sources,
        'source_stats': source_stats,
        'recent_uploads': recent_uploads,
        'total_skus': total_skus,
        'matched_skus': matched_skus,
        'critical_items': critical_items,
        'low_items': low_items,
        'upload_form': ReportUploadForm(),
    }
    return render(request, 'reports/hub.html', context)


@login_required
def upload_report(request):
    """Handle file upload and processing."""
    if request.method == 'POST':
        form = ReportUploadForm(request.POST, request.FILES)
        if form.is_valid():
            source = form.cleaned_data['report_source']
            uploaded_file = form.cleaned_data['file']
            data_date_val = form.cleaned_data.get('data_date') or date.today()

            # Create the UploadedReport record
            report = UploadedReport.objects.create(
                report_source=source,
                file=uploaded_file,
                original_filename=uploaded_file.name,
                file_type=uploaded_file.name.rsplit('.', 1)[-1].lower(),
                uploaded_by=request.user,
                processing_status='processing',
                data_date=data_date_val,
            )

            try:
                # Read and parse the file
                report.file.seek(0)
                df = read_file_to_dataframe(report.file, report.original_filename)
                parser = get_parser(source.system_type)
                parsed_rows = parser(df)

                report.rows_total = len(parsed_rows)

                # Build a lookup of existing items by item_no
                item_lookup = {}
                for item in Item.objects.filter(inactive=False):
                    item_lookup[item.item_no.strip().upper()] = item

                rows_imported = 0
                rows_skipped = 0
                rows_matched = 0

                for row_data in parsed_rows:
                    sku = row_data.get('sku', '').strip()
                    if not sku:
                        rows_skipped += 1
                        continue

                    # Try to match to an existing ERP item
                    matched_item = item_lookup.get(sku.upper())

                    rd = ReportData.objects.create(
                        uploaded_report=report,
                        report_source=source,
                        item=matched_item,
                        sku=sku,
                        product_name=row_data.get('product_name', ''),
                        data_date=data_date_val,
                        inventory_level=row_data.get('inventory_level'),
                        sales_velocity=row_data.get('sales_velocity'),
                        demand_forecast_30d=row_data.get('demand_forecast_30d'),
                        demand_forecast_60d=row_data.get('demand_forecast_60d'),
                        demand_forecast_90d=row_data.get('demand_forecast_90d'),
                        reorder_quantity=row_data.get('reorder_quantity'),
                        reorder_point=row_data.get('reorder_point'),
                        days_of_stock=row_data.get('days_of_stock'),
                        extra_data=row_data.get('extra_data', {}),
                        raw_row=row_data.get('raw_row', {}),
                    )
                    rows_imported += 1
                    if matched_item:
                        rows_matched += 1

                report.rows_imported = rows_imported
                report.rows_skipped = rows_skipped
                report.rows_matched = rows_matched
                report.processing_status = 'success'
                report.processed_at = timezone.now()
                report.save()

                messages.success(
                    request,
                    f'Successfully imported {rows_imported} rows from {report.original_filename}. '
                    f'{rows_matched} matched to ERP items, {rows_skipped} skipped.'
                )

            except Exception as e:
                logger.exception(f"Error processing upload {report.id}")
                report.processing_status = 'failed'
                report.error_message = str(e)
                report.processed_at = timezone.now()
                report.save()
                messages.error(request, f'Error processing file: {e}')

            return redirect('reports:hub')
    else:
        form = ReportUploadForm()

    context = {
        'form': form,
        'sources': ReportSource.objects.filter(is_active=True),
    }
    return render(request, 'reports/upload.html', context)


@login_required
def upload_status(request, upload_id):
    """JSON endpoint for checking upload processing status."""
    report = get_object_or_404(UploadedReport, id=upload_id)
    return JsonResponse({
        'status': report.processing_status,
        'rows_total': report.rows_total,
        'rows_imported': report.rows_imported,
        'rows_skipped': report.rows_skipped,
        'rows_matched': report.rows_matched,
        'error_message': report.error_message,
    })


@login_required
def data_list(request):
    """Unified data table — filterable by source, SKU, date range, stock status."""
    queryset = ReportData.objects.select_related('report_source', 'item', 'uploaded_report')

    # Filters
    source_filter = request.GET.get('source', '')
    sku_filter = request.GET.get('sku', '')
    status_filter = request.GET.get('status', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    matched_filter = request.GET.get('matched', '')

    if source_filter:
        queryset = queryset.filter(report_source__slug=source_filter)
    if sku_filter:
        queryset = queryset.filter(
            Q(sku__icontains=sku_filter) | Q(product_name__icontains=sku_filter)
        )
    if date_from:
        queryset = queryset.filter(data_date__gte=date_from)
    if date_to:
        queryset = queryset.filter(data_date__lte=date_to)
    if matched_filter == 'yes':
        queryset = queryset.filter(item__isnull=False)
    elif matched_filter == 'no':
        queryset = queryset.filter(item__isnull=True)
    if status_filter == 'critical':
        queryset = queryset.filter(days_of_stock__lte=14)
    elif status_filter == 'low':
        queryset = queryset.filter(days_of_stock__gt=14, days_of_stock__lte=30)
    elif status_filter == 'ok':
        queryset = queryset.filter(days_of_stock__gt=30)

    queryset = queryset.order_by('-data_date', 'sku')

    paginator = Paginator(queryset, 50)
    page = request.GET.get('page', 1)
    data_rows = paginator.get_page(page)

    sources = ReportSource.objects.filter(is_active=True)

    context = {
        'data_rows': data_rows,
        'sources': sources,
        'filters': {
            'source': source_filter,
            'sku': sku_filter,
            'status': status_filter,
            'date_from': date_from,
            'date_to': date_to,
            'matched': matched_filter,
        },
    }
    return render(request, 'reports/data_list.html', context)


@login_required
def sku_compare(request):
    """Compare a single SKU across all sources side-by-side."""
    sku_query = request.GET.get('sku', '').strip()
    comparison_data = []

    if sku_query:
        # Get the latest data for this SKU from each source
        sources = ReportSource.objects.filter(is_active=True)
        for source in sources:
            latest = ReportData.objects.filter(
                report_source=source,
                sku__iexact=sku_query,
            ).order_by('-data_date').first()
            if latest:
                comparison_data.append(latest)

    # Get list of all known SKUs for autocomplete
    all_skus = list(
        ReportData.objects.values_list('sku', flat=True)
        .distinct()
        .order_by('sku')[:500]
    )

    context = {
        'sku_query': sku_query,
        'comparison_data': comparison_data,
        'all_skus': json.dumps(all_skus),
    }
    return render(request, 'reports/compare.html', context)


@login_required
def reorder_alerts(request):
    """Show items that need reordering based on days of stock and reorder points."""
    # Get the most recent data per SKU per source
    critical = ReportData.objects.filter(
        days_of_stock__isnull=False,
        days_of_stock__lte=14,
    ).select_related('report_source', 'item').order_by('days_of_stock')

    low = ReportData.objects.filter(
        days_of_stock__isnull=False,
        days_of_stock__gt=14,
        days_of_stock__lte=30,
    ).select_related('report_source', 'item').order_by('days_of_stock')

    # Items with reorder recommendations
    reorder_recs = ReportData.objects.filter(
        reorder_quantity__isnull=False,
        reorder_quantity__gt=0,
    ).select_related('report_source', 'item').order_by('-reorder_quantity')[:50]

    context = {
        'critical': critical,
        'low': low,
        'reorder_recs': reorder_recs,
    }
    return render(request, 'reports/alerts.html', context)


@login_required
def manage_sources(request):
    """View and manage report sources."""
    sources = ReportSource.objects.all()
    context = {'sources': sources}
    return render(request, 'reports/sources.html', context)


@login_required
def chart_data_api(request):
    """API endpoint for chart data (inventory trends over time for a SKU)."""
    sku = request.GET.get('sku', '')
    source = request.GET.get('source', '')

    if not sku:
        return JsonResponse({'error': 'SKU required'}, status=400)

    queryset = ReportData.objects.filter(sku__iexact=sku)
    if source:
        queryset = queryset.filter(report_source__slug=source)

    queryset = queryset.order_by('data_date')

    data_points = []
    for rd in queryset:
        data_points.append({
            'date': rd.data_date.isoformat(),
            'inventory': float(rd.inventory_level) if rd.inventory_level else None,
            'velocity': float(rd.sales_velocity) if rd.sales_velocity else None,
            'days_of_stock': float(rd.days_of_stock) if rd.days_of_stock else None,
            'source': rd.report_source.name,
        })

    return JsonResponse({'sku': sku, 'data': data_points})
