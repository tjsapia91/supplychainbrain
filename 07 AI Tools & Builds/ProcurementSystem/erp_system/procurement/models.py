from django.core.validators import MinValueValidator, FileExtensionValidator
from django.db import models, transaction
from django.conf import settings
from decimal import Decimal


class PurchaseRequisition(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('converted', 'Converted to PPO'),
        ('cancelled', 'Cancelled'),
    ]
    pr_number = models.CharField(max_length=20, unique=True)
    date = models.DateField(auto_now_add=True)
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='requisitions_created')
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='requisitions_approved')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    priority = models.CharField(max_length=10, choices=[('low','Low'),('medium','Medium'),('high','High'),('urgent','Urgent')], default='medium')
    notes = models.TextField(blank=True)
    approved_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"PR-{self.pr_number}"

    @classmethod
    def get_next_pr_number(cls):
        last = cls.objects.order_by('-pr_number').first()
        if last:
            try:
                num = int(last.pr_number) + 1
            except ValueError:
                num = 1001
        else:
            num = 1001
        return str(num)


class PurchaseRequisitionLine(models.Model):
    requisition = models.ForeignKey(PurchaseRequisition, on_delete=models.CASCADE, related_name='lines')
    item = models.ForeignKey('items.Item', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    notes = models.TextField(blank=True)
    suggested_vendor = models.ForeignKey('vendors.Vendor', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.requisition.pr_number} - {self.item.item_no}"


class PlannedPurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent_to_vendor', 'Sent to Vendor'),
        ('pi_received', 'PI Received'),
        ('pending_ceo_approval', 'Pending CEO Approval'),
        ('ceo_approved', 'CEO Approved'),
        ('ceo_rejected', 'CEO Rejected'),
        ('confirmed', 'Confirmed/Active'),
        ('in_transit', 'In Transit'),
        ('partially_received', 'Partially Received'),
        ('fully_received', 'Fully Received'),
        ('cancelled', 'Cancelled'),
        ('closed', 'Closed'),
    ]
    TRANSPORT_CHOICES = [
        ('container', 'Container'),
        ('air', 'Air Freight'),
        ('express', 'Express/Courier'),
        ('lcl', 'LCL (Less than Container)'),
        ('truck', 'Truck'),
    ]
    INCOTERM_CHOICES = [
        ('DDP', 'DDP - Delivered Duty Paid'),
        ('FOB', 'FOB - Free on Board'),
        ('CIF', 'CIF - Cost Insurance Freight'),
        ('EXW', 'EXW - Ex Works'),
        ('CFR', 'CFR - Cost and Freight'),
        ('DAP', 'DAP - Delivered at Place'),
    ]
    ppo_number = models.IntegerField(unique=True)
    date = models.DateField()
    branch = models.ForeignKey('vendors.Branch', on_delete=models.SET_NULL, null=True, blank=True, help_text="MTB, Spa Sciences, or NasalFresh MD")
    bill_to = models.ForeignKey('vendors.BillToAddress', on_delete=models.SET_NULL, null=True, blank=True)
    vendor = models.ForeignKey('vendors.Vendor', on_delete=models.CASCADE, related_name='purchase_orders')
    ship_to_3pl = models.ForeignKey('vendors.ThreePLProvider', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Ship To (3PL)")
    ship_to = models.ForeignKey('vendors.ShipToAddress', on_delete=models.SET_NULL, null=True, blank=True, help_text="Legacy - use 3PL instead")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', db_index=True)
    requested_ship_date = models.DateField(null=True, blank=True)
    estimated_ship_date = models.DateField(null=True, blank=True)
    actual_ship_date = models.DateField(null=True, blank=True)
    payment_terms = models.CharField(max_length=100, blank=True)
    mode_of_transport = models.CharField(max_length=20, choices=TRANSPORT_CHOICES, default='container')
    port_of_loading = models.CharField(max_length=200, blank=True)
    port_of_discharge = models.CharField(max_length=200, blank=True)
    country_of_origin = models.CharField(max_length=100, blank=True)
    incoterms = models.CharField(max_length=3, choices=INCOTERM_CHOICES, default='DDP')
    lead_time_days = models.IntegerField(null=True, blank=True)
    currency = models.CharField(max_length=3, default='USD')
    awb_bl_number = models.CharField(max_length=100, blank=True, verbose_name="AWB/BL #")
    special_notes = models.TextField(blank=True)
    wire_info = models.TextField(blank=True, help_text="Factory wire/bank information")
    total_cartons = models.IntegerField(default=0)
    total_cbm = models.DecimalField(max_digits=12, decimal_places=6, default=0)
    total_weight = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deposit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    balance_due = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    purchase_requisition = models.ForeignKey(PurchaseRequisition, null=True, blank=True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='ppos_created')
    pdf_file = models.FileField(upload_to='ppo_pdfs/', blank=True, null=True)
    vendor_email_sent_date = models.DateTimeField(null=True, blank=True)
    ceo_approval_requested_date = models.DateTimeField(null=True, blank=True)
    ceo_approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='ppos_approved')
    ceo_approval_date = models.DateTimeField(null=True, blank=True)
    ceo_rejection_reason = models.TextField(blank=True)
    ceo_signature_type = models.CharField(max_length=10, blank=True, choices=[('typed', 'Typed'), ('image', 'Uploaded Image')], help_text="How the CEO signed")
    ceo_signature_text = models.CharField(max_length=200, blank=True, help_text="Typed signature name")
    ceo_signature_image = models.ImageField(upload_to='signatures/', blank=True, null=True, help_text="Uploaded signature image")
    vendor_pi_number = models.CharField(max_length=100, blank=True, help_text="Vendor's PI reference number")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-ppo_number']

    def __str__(self):
        return f"{self.ppo_number}"

    # Standard container capacities in CBM
    CONTAINER_20FT_CBM = 28
    CONTAINER_40FT_CBM = 58
    CONTAINER_40HQ_CBM = 68

    def recalculate_totals(self):
        """Recalculate all totals from line items"""
        lines = self.lines.all()
        self.total_cartons = sum(l.cartons or 0 for l in lines)
        self.total_cbm = sum(l.cbm or 0 for l in lines)
        self.total_weight = sum(l.total_weight or 0 for l in lines)
        self.subtotal = sum(l.line_total or 0 for l in lines)
        self.balance_due = self.subtotal - self.deposit
        self.total = self.subtotal
        self.save()

    @property
    def estimated_containers_20ft(self):
        """Estimate number of 20ft containers needed based on total CBM"""
        import math
        if self.total_cbm and float(self.total_cbm) > 0:
            return math.ceil(float(self.total_cbm) / self.CONTAINER_20FT_CBM)
        return 0

    @property
    def estimated_containers_40ft(self):
        """Estimate number of 40ft containers needed based on total CBM"""
        import math
        if self.total_cbm and float(self.total_cbm) > 0:
            return math.ceil(float(self.total_cbm) / self.CONTAINER_40FT_CBM)
        return 0

    @property
    def estimated_containers_40hq(self):
        """Estimate number of 40ft HC containers needed based on total CBM"""
        import math
        if self.total_cbm and float(self.total_cbm) > 0:
            return math.ceil(float(self.total_cbm) / self.CONTAINER_40HQ_CBM)
        return 0

    @property
    def container_utilization_pct(self):
        """Container utilization as a percentage (based on 40ft container)"""
        if self.total_cbm and float(self.total_cbm) > 0:
            containers = self.estimated_containers_40ft
            capacity = containers * self.CONTAINER_40FT_CBM
            return round(float(self.total_cbm) / capacity * 100, 1)
        return 0

    @classmethod
    def get_next_ppo_number(cls):
        last = cls.objects.order_by('-ppo_number').first()
        return (last.ppo_number + 1) if last else 3149

    # Valid status transitions: from_status -> [allowed_to_statuses]
    VALID_TRANSITIONS = {
        'draft': ['sent_to_vendor', 'cancelled'],
        'sent_to_vendor': ['pi_received', 'cancelled'],
        'pi_received': ['pending_ceo_approval', 'cancelled'],
        'pending_ceo_approval': ['ceo_approved', 'ceo_rejected', 'cancelled'],
        'ceo_approved': ['confirmed', 'cancelled'],
        'ceo_rejected': ['draft', 'cancelled'],
        'confirmed': ['in_transit', 'partially_received', 'fully_received', 'cancelled'],
        'in_transit': ['partially_received', 'fully_received', 'cancelled'],
        'partially_received': ['partially_received', 'fully_received', 'cancelled'],
        'fully_received': ['closed', 'cancelled'],
        'cancelled': [],
        'closed': [],
    }

    def change_status(self, new_status, user, notes='', force=False):
        """Change PPO status and create an audit log entry.
        Validates the transition is allowed unless force=True.
        Uses atomic transaction to prevent partial updates.
        """
        with transaction.atomic():
            old_status = self.status
            if not force:
                allowed = self.VALID_TRANSITIONS.get(old_status, [])
                if new_status not in allowed:
                    raise ValueError(
                        f'Invalid status transition: {old_status} \u2192 {new_status}. '
                        f'Allowed transitions: {", ".join(allowed) or "none"}'
                    )
            self.status = new_status
            self.save(update_fields=['status', 'updated_at'])
            PPOStatusLog.objects.create(
                ppo=self,
                from_status=old_status,
                to_status=new_status,
                changed_by=user,
                notes=notes
            )


class PPOLineItem(models.Model):
    ppo = models.ForeignKey(PlannedPurchaseOrder, on_delete=models.CASCADE, related_name='lines')
    line_number = models.IntegerField()
    item = models.ForeignKey('items.Item', on_delete=models.CASCADE)
    description = models.CharField(max_length=500, blank=True)
    quantity = models.IntegerField(null=True, blank=True, default=0, validators=[MinValueValidator(0)])
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, default=0, validators=[MinValueValidator(Decimal('0'))])
    cartons = models.IntegerField(null=True, blank=True)
    cbm = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)
    total_weight = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    line_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    destination = models.CharField(max_length=200, blank=True, help_text="e.g., Shopify, Amazon, Walmart")
    batch_code = models.CharField(max_length=25, blank=True, help_text="Batch/lot code, up to 20 characters")
    qty_received = models.IntegerField(default=0)

    class Meta:
        ordering = ['line_number']

    def __str__(self):
        return f"Line {self.line_number}: {self.item.item_no}"

    def save(self, *args, **kwargs):
        if not self.description and self.item:
            self.description = self.item.description
        qty = self.quantity or 0
        price = self.unit_price or 0
        # Only auto-calculate cartons/cbm/weight if not already set (allows manual override)
        if self.item and qty:
            if not self.cartons:
                self.cartons = self.item.calculate_cartons(qty)
            if not self.cbm and self.cartons:
                self.cbm = self.item.calculate_cbm(self.cartons)
            if not self.total_weight and self.item.weight_uom:
                self.total_weight = round(qty * float(self.item.weight_uom), 2)
        self.line_total = qty * price
        super().save(*args, **kwargs)

    @property
    def is_fully_received(self):
        return self.qty_received >= self.quantity


class ProformaInvoice(models.Model):
    STATUS_CHOICES = [
        ('received', 'Received'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    SYNC_CHOICES = [
        ('not_synced', 'Not Synced'),
        ('synced', 'Synced'),
        ('failed', 'Failed'),
    ]
    ppo = models.ForeignKey(PlannedPurchaseOrder, on_delete=models.CASCADE, related_name='proforma_invoices')
    pi_number = models.CharField(max_length=100, help_text="Vendor's PI number (usually PO followed by number)")
    vendor = models.ForeignKey('vendors.Vendor', on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='received')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default='USD')
    file = models.FileField(upload_to='proforma_invoices/', help_text="Upload the PI document from vendor")
    notes = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    sync_status = models.CharField(max_length=15, choices=SYNC_CHOICES, default='not_synced')
    sync_error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"PI-{self.pi_number} (PPO-{self.ppo.ppo_number})"


class PPOStatusLog(models.Model):
    """Audit trail for all PPO status changes"""
    ppo = models.ForeignKey(PlannedPurchaseOrder, on_delete=models.CASCADE, related_name='status_logs')
    from_status = models.CharField(max_length=30)
    to_status = models.CharField(max_length=30)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"PPO-{self.ppo.ppo_number}: {self.from_status} → {self.to_status}"


class PPOAttachment(models.Model):
    """File attachments for PPO documents (PI, signed copies, shipping docs, etc.)"""
    TYPE_CHOICES = [
        ('pi_document', 'Proforma Invoice'),
        ('signed_ppo', 'Signed PPO'),
        ('ceo_approval', 'CEO Approval'),
        ('shipping_doc', 'Shipping Document'),
        ('other', 'Other'),
    ]
    SYNC_CHOICES = [
        ('not_synced', 'Not Synced'),
        ('synced', 'Synced'),
        ('failed', 'Failed'),
    ]
    ALLOWED_EXTENSIONS = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'csv', 'jpg', 'jpeg', 'png', 'gif', 'tiff']
    ppo = models.ForeignKey(PlannedPurchaseOrder, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(
        upload_to='ppo_attachments/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'xls', 'xlsx', 'csv', 'jpg', 'jpeg', 'png', 'gif', 'tiff'])],
        help_text='Allowed: PDF, Word, Excel, CSV, Images (max 25 MB)',
    )
    file_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='other')
    description = models.CharField(max_length=300, blank=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    sync_status = models.CharField(max_length=15, choices=SYNC_CHOICES, default='not_synced')
    sync_error = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_file_type_display()} - PPO-{self.ppo.ppo_number}"
