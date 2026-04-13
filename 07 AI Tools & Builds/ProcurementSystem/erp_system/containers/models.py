from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal
import math


class ContainerPlan(models.Model):
    """
    A container shipment plan - represents a physical container being packed and shipped.
    Maps to one row per container in the 'Container Plan Mar.xlsx' sheets like NYKU4749505, ONEU6377934, etc.
    """
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('packing', 'Packing / Allocating'),
        ('booked', 'Booked with Forwarder'),
        ('ready_to_load', 'Ready to Load'),
        ('loaded', 'Loaded'),
        ('in_transit', 'In Transit'),
        ('at_port', 'At Port'),
        ('customs', 'In Customs'),
        ('delivered', 'Delivered to Warehouse'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    CONTAINER_TYPE_CHOICES = [
        ('20ft', "20' Standard"),
        ('40ft', "40' Standard"),
        ('40hq', "40' High Cube"),
    ]
    TRANSPORT_MODE_CHOICES = [
        ('ocean', 'Ocean (FCL)'),
        ('ocean_lcl', 'Ocean (LCL)'),
        ('air', 'Air Freight'),
        ('truck', 'Truck'),
    ]

    # Identification
    plan_number = models.CharField(max_length=30, unique=True, help_text="Auto-generated plan reference")
    container_number = models.CharField(max_length=30, blank=True, help_text="Physical container # e.g. NYKU4749505")
    booking_reference = models.CharField(max_length=100, blank=True, help_text="Forwarder booking ref e.g. 2026Dream007")
    commercial_invoice = models.CharField(max_length=100, blank=True, help_text="Commercial invoice number")

    # Container specs
    container_type = models.CharField(max_length=10, choices=CONTAINER_TYPE_CHOICES, default='40hq')
    max_cbm = models.DecimalField(max_digits=8, decimal_places=2, default=67.5, validators=[MinValueValidator(0)], help_text="Max CBM capacity")
    max_weight_kg = models.DecimalField(max_digits=10, decimal_places=2, default=26000, validators=[MinValueValidator(0)], help_text="Max weight in kg")
    transport_mode = models.CharField(max_length=15, choices=TRANSPORT_MODE_CHOICES, default='ocean')

    # Shipping details
    forwarder = models.CharField(max_length=200, blank=True, help_text="Freight forwarder name")
    hbl_number = models.CharField(max_length=100, blank=True, verbose_name="House Bill of Lading")
    incoterms = models.CharField(max_length=10, blank=True, help_text="DDP, FOB, CIF, etc.")
    routing_notes = models.CharField(max_length=300, blank=True, help_text="e.g. DDP - Transload at LA, DDP - Harry")
    port_of_loading = models.CharField(max_length=200, blank=True)
    port_of_discharge = models.CharField(max_length=200, blank=True)
    receiving_warehouse = models.CharField(max_length=200, blank=True, help_text="e.g. CHR, Amware")

    # Status and dates
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning', db_index=True)
    target_load_date = models.DateField(null=True, blank=True, help_text="Target date to load container")
    actual_load_date = models.DateField(null=True, blank=True)
    date_sailed = models.DateField(null=True, blank=True)
    eta_port = models.DateField(null=True, blank=True)
    warehouse_delivery_date = models.DateField(null=True, blank=True)
    date_entry_summary_received = models.DateField(null=True, blank=True, help_text="Customs entry summary date")

    # Cross-dock tracking
    cross_dock_pickup_date = models.DateField(null=True, blank=True)
    cross_dock_delivery_date = models.DateField(null=True, blank=True)
    cross_dock_bol = models.CharField(max_length=100, blank=True, verbose_name="Cross-dock BOL #")

    # Totals (auto-calculated)
    total_cbm = models.DecimalField(max_digits=12, decimal_places=4, default=0, validators=[MinValueValidator(0)])
    total_weight = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    total_cartons = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    total_units = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    total_value = models.DecimalField(max_digits=14, decimal_places=2, default=0, validators=[MinValueValidator(0)])

    # Notes
    notes = models.TextField(blank=True)

    # Audit
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='container_plans_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        label = self.container_number or self.plan_number
        return f"{label} ({self.get_status_display()})"

    @classmethod
    def get_next_plan_number(cls):
        from datetime import date
        prefix = date.today().strftime('CP-%Y%m-')
        last = cls.objects.filter(plan_number__startswith=prefix).order_by('-plan_number').first()
        if last:
            try:
                seq = int(last.plan_number.split('-')[-1]) + 1
            except (ValueError, IndexError):
                seq = 1
        else:
            seq = 1
        return f"{prefix}{seq:03d}"

    @property
    def cbm_utilization(self):
        """CBM utilization as a percentage"""
        if self.max_cbm and self.max_cbm > 0:
            return round(float(self.total_cbm) / float(self.max_cbm) * 100, 1)
        return 0

    @property
    def weight_utilization(self):
        """Weight utilization as a percentage"""
        if self.max_weight_kg and self.max_weight_kg > 0:
            return round(float(self.total_weight) / float(self.max_weight_kg) * 100, 1)
        return 0

    @property
    def cbm_remaining(self):
        return float(self.max_cbm) - float(self.total_cbm)

    @property
    def days_in_transit(self):
        """Calculate days from sail to now or delivery"""
        if not self.date_sailed:
            return None
        end = self.warehouse_delivery_date or timezone.now().date()
        return (end - self.date_sailed).days

    @property
    def days_po_to_delivery(self):
        """Total days from earliest PO date to warehouse delivery"""
        if not self.warehouse_delivery_date:
            return None
        earliest_po = self.items.aggregate(models.Min('ppo_line__ppo__date'))['ppo_line__ppo__date__min']
        if earliest_po:
            return (self.warehouse_delivery_date - earliest_po).days
        return None

    def recalculate_totals(self):
        """Recalculate container totals from line items"""
        items = self.items.all()
        self.total_cbm = sum(i.cbm or 0 for i in items)
        self.total_weight = sum(i.total_weight or 0 for i in items)
        self.total_cartons = sum(i.cartons or 0 for i in items)
        self.total_units = sum(i.quantity or 0 for i in items)
        self.total_value = sum(i.line_value or 0 for i in items)
        self.save()


class ContainerItem(models.Model):
    """
    A line item within a container plan.
    Links a PPO line item to a specific container with quantity allocated.
    """
    container = models.ForeignKey(ContainerPlan, on_delete=models.CASCADE, related_name='items')
    ppo_line = models.ForeignKey('procurement.PPOLineItem', on_delete=models.CASCADE, related_name='container_allocations', null=True, blank=True)

    # If not linked to a PPO line, store item details directly
    item = models.ForeignKey('items.Item', on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=500, blank=True)
    destination = models.CharField(max_length=200, blank=True, help_text="AMZ, SB, AWD, 3PL, Walmart, Floship, etc.")
    hts_code = models.CharField(max_length=30, blank=True, verbose_name="HTS Code")

    # Quantities
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)], help_text="Units allocated to this container")
    cartons = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    cbm = models.DecimalField(max_digits=12, decimal_places=4, default=0, validators=[MinValueValidator(0)])
    total_weight = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    line_value = models.DecimalField(max_digits=14, decimal_places=2, default=0, validators=[MinValueValidator(0)], help_text="Commercial invoice value")

    # Receiving
    qty_received = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    receive_date = models.DateField(null=True, blank=True)
    variance = models.IntegerField(default=0, help_text="qty_received - quantity")
    vendor_invoice_no = models.CharField(max_length=100, blank=True)

    # Transfer tracking (post-warehouse)
    transfer_qty = models.IntegerField(default=0, help_text="Qty transferred (e.g. cross-dock)")
    transfer_date = models.DateField(null=True, blank=True)
    transfer_sap_doc = models.CharField(max_length=50, blank=True, help_text="SAP document # for transfer")
    transfer_bol = models.CharField(max_length=100, blank=True, help_text="BOL # for transfer")

    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['destination', 'item__item_no']

    def __str__(self):
        item_label = self.item.item_no if self.item else self.description[:30]
        return f"{item_label} x{self.quantity} -> {self.destination}"

    def save(self, *args, **kwargs):
        # Auto-populate from PPO line if linked
        if self.ppo_line and not self.item:
            self.item = self.ppo_line.item
        if self.ppo_line and not self.description:
            self.description = self.ppo_line.description
        if self.ppo_line and not self.destination:
            self.destination = self.ppo_line.destination

        # Auto-calculate cartons and CBM from item master data
        if self.item and self.quantity:
            if not self.cartons or self.cartons == 0:
                calc_cartons = self.item.calculate_cartons(self.quantity)
                if calc_cartons:
                    self.cartons = calc_cartons
            if (not self.cbm or self.cbm == 0) and self.cartons:
                calc_cbm = self.item.calculate_cbm(self.cartons)
                if calc_cbm:
                    self.cbm = Decimal(str(calc_cbm))

        # Calculate variance
        self.variance = self.qty_received - self.quantity

        super().save(*args, **kwargs)

    @property
    def is_fully_received(self):
        return self.qty_received >= self.quantity

    @property
    def ppo_number(self):
        if self.ppo_line:
            return self.ppo_line.ppo.ppo_number
        return None


class DemandForecast(models.Model):
    """
    Monthly demand forecast by SKU and channel.
    Maps to the NFMD sheet structure: month-by-month forecast with cumulative tracking.
    """
    CHANNEL_CHOICES = [
        ('amazon', 'Amazon'),
        ('shopify', 'Shopify'),
        ('walmart', 'Walmart'),
        ('amz_canada', 'AMZ Canada'),
        ('shipbob', 'ShipBob'),
        ('awd', 'AWD'),
        ('floship', 'Floship'),
        ('wholesale', 'Wholesale'),
        ('other', 'Other'),
    ]

    item = models.ForeignKey('items.Item', on_delete=models.CASCADE, related_name='demand_forecasts')
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES)
    month = models.DateField(help_text="First day of the forecast month")
    forecast_qty = models.IntegerField(default=0, validators=[MinValueValidator(0)], help_text="Forecasted demand for this month")
    actual_qty = models.IntegerField(default=0, validators=[MinValueValidator(0)], help_text="Actual sales (filled in after the month)")
    source = models.CharField(max_length=100, blank=True, help_text="SoStocked, Valogix, Manual, Historical")
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['item', 'channel', 'month']
        unique_together = ['item', 'channel', 'month']

    def __str__(self):
        return f"{self.item.item_no} - {self.get_channel_display()} - {self.month.strftime('%b %Y')}"

    @property
    def variance(self):
        """Forecast vs actual variance"""
        if self.actual_qty:
            return self.actual_qty - self.forecast_qty
        return None

    @property
    def accuracy_pct(self):
        """Forecast accuracy percentage"""
        if self.actual_qty and self.forecast_qty:
            return round((1 - abs(self.actual_qty - self.forecast_qty) / self.forecast_qty) * 100, 1)
        return None


class ContainerStatusLog(models.Model):
    """Audit trail for container status changes"""
    container = models.ForeignKey(ContainerPlan, on_delete=models.CASCADE, related_name='status_logs')
    from_status = models.CharField(max_length=30)
    to_status = models.CharField(max_length=30)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.container.plan_number}: {self.from_status} -> {self.to_status}"


class ShippingDocument(models.Model):
    """Uploaded shipping documents for containers (BOL, Signed BOL, Packing List, etc.)"""
    DOC_TYPE_CHOICES = [
        ('bol', 'Bill of Lading'),
        ('signed_bol', 'Signed Bill of Lading'),
        ('packing_list', 'Packing List'),
        ('commercial_invoice', 'Commercial Invoice'),
        ('customs_entry', 'Customs Entry'),
        ('other', 'Other'),
    ]
    SYNC_CHOICES = [
        ('not_synced', 'Not Synced'),
        ('synced', 'Synced'),
        ('failed', 'Failed'),
    ]
    container = models.ForeignKey(ContainerPlan, on_delete=models.CASCADE, related_name='shipping_documents')
    document_type = models.CharField(max_length=25, choices=DOC_TYPE_CHOICES)
    file = models.FileField(upload_to='shipping_documents/')
    description = models.CharField(max_length=300, blank=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    sync_status = models.CharField(max_length=15, choices=SYNC_CHOICES, default='not_synced')
    sync_error = models.TextField(blank=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.get_document_type_display()} - {self.container.plan_number}"
