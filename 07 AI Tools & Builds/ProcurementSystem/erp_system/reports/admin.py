from django.contrib import admin
from .models import ReportSource, UploadedReport, FulfillmentLocation, ReportData


@admin.register(ReportSource)
class ReportSourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'system_type', 'is_active', 'created_at']
    list_filter = ['system_type', 'is_active']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(UploadedReport)
class UploadedReportAdmin(admin.ModelAdmin):
    list_display = ['original_filename', 'report_source', 'processing_status',
                    'rows_total', 'rows_imported', 'rows_matched', 'uploaded_by', 'uploaded_at']
    list_filter = ['processing_status', 'report_source']
    readonly_fields = ['uploaded_at', 'processed_at']


@admin.register(FulfillmentLocation)
class FulfillmentLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'location_type', 'is_active']
    list_filter = ['location_type', 'is_active']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ReportData)
class ReportDataAdmin(admin.ModelAdmin):
    list_display = ['sku', 'product_name', 'report_source', 'data_date',
                    'inventory_level', 'sales_velocity', 'days_of_stock']
    list_filter = ['report_source', 'data_date']
    search_fields = ['sku', 'product_name']
    raw_id_fields = ['item', 'uploaded_report']
