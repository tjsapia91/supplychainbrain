from django.db import models
from django.conf import settings


class ReportSource(models.Model):
    """
    Represents an external system that provides data (SoStocked, Amazon, Shopify, etc.)
    """
    SYSTEM_TYPES = [
        ('sostocked', 'SoStocked'),
        ('valogix', 'Valogix'),
        ('amazon', 'Amazon Seller Central'),
        ('shopify', 'Shopify'),
        ('tiktok', 'TikTok Shop'),
        ('walmart', 'Walmart Marketplace'),
        ('shipbob', 'ShipBob'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, unique=True)
    system_type = models.CharField(max_length=20, choices=SYSTEM_TYPES, default='other')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    color_class = models.CharField(max_length=30, blank=True, help_text='CSS class for badge styling')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class UploadedReport(models.Model):
    """
    Tracks each file upload — provides audit trail and allows re-processing.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('success', 'Success'),
        ('partial', 'Partial (with warnings)'),
        ('failed', 'Failed'),
    ]

    report_source = models.ForeignKey(ReportSource, on_delete=models.CASCADE, related_name='uploads')
    file = models.FileField(upload_to='reports/%Y/%m/')
    original_filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=10)  # csv, xlsx
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processing_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True)
    rows_total = models.IntegerField(default=0)
    rows_imported = models.IntegerField(default=0)
    rows_skipped = models.IntegerField(default=0)
    rows_matched = models.IntegerField(default=0, help_text='Rows matched to existing ERP items')
    data_date = models.DateField(null=True, blank=True, help_text='Date the data was current (defaults to upload date)')
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.report_source.name} - {self.original_filename} ({self.uploaded_at.strftime('%Y-%m-%d')})"


class FulfillmentLocation(models.Model):
    """
    Physical locations where inventory is stored (ShipBob, AWD, FBA warehouses, own warehouse).
    """
    LOCATION_TYPES = [
        ('3pl', '3PL Fulfillment'),
        ('fba', 'Amazon FBA'),
        ('awd', 'Amazon AWD'),
        ('own', 'Own Warehouse'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, unique=True)
    location_type = models.CharField(max_length=10, choices=LOCATION_TYPES)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ReportData(models.Model):
    """
    Normalized data from all external sources. One row = one SKU from one source at one point in time.
    Links to ERP Item when possible (matched on item_no/SKU).
    """
    uploaded_report = models.ForeignKey(UploadedReport, on_delete=models.CASCADE, related_name='data_rows')
    report_source = models.ForeignKey(ReportSource, on_delete=models.CASCADE, related_name='data_rows')
    item = models.ForeignKey('items.Item', on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='report_data', help_text='Matched ERP item')
    sku = models.CharField(max_length=100, db_index=True, help_text='SKU as it appears in the source system')
    product_name = models.CharField(max_length=500, blank=True)
    data_date = models.DateField(db_index=True, help_text='When this data was current')

    # Core inventory & demand metrics (all optional — different sources provide different data)
    inventory_level = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    sales_velocity = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                         help_text='Units sold per day')
    demand_forecast_30d = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                              help_text='Projected demand next 30 days')
    demand_forecast_60d = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                              help_text='Projected demand next 60 days')
    demand_forecast_90d = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                              help_text='Projected demand next 90 days')
    reorder_quantity = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    reorder_point = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    days_of_stock = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)

    # Fulfillment location (if the source provides it, e.g. ShipBob inventory by warehouse)
    fulfillment_location = models.ForeignKey(FulfillmentLocation, on_delete=models.SET_NULL,
                                              null=True, blank=True, related_name='report_data')

    # Flexible storage for source-specific fields we haven't normalized
    extra_data = models.JSONField(default=dict, blank=True,
                                  help_text='Any additional source-specific fields')

    # The original row data as parsed from the file (for debugging/auditing)
    raw_row = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_date', 'sku']
        indexes = [
            models.Index(fields=['report_source', 'sku', '-data_date']),
            models.Index(fields=['item', '-data_date']),
            models.Index(fields=['sku']),
        ]

    def __str__(self):
        return f"{self.sku} - {self.report_source.name} ({self.data_date})"

    @property
    def status(self):
        """Stock status based on days of stock remaining."""
        if self.days_of_stock is None:
            return 'unknown'
        if self.days_of_stock <= 14:
            return 'critical'
        if self.days_of_stock <= 30:
            return 'low'
        return 'ok'
