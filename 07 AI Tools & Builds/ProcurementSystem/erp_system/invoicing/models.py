from django.db import models
from django.core.validators import MinValueValidator


class APInvoice(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('matched', 'Matched'),
        ('partially_matched', 'Partially Matched'),
        ('approved', 'Approved for Payment'),
        ('paid', 'Paid'),
        ('disputed', 'Disputed'),
    ]
    invoice_number = models.CharField(max_length=100, db_index=True)
    vendor = models.ForeignKey('vendors.Vendor', on_delete=models.CASCADE)
    ppo = models.ForeignKey('procurement.PlannedPurchaseOrder', on_delete=models.SET_NULL, null=True, blank=True)
    grpo = models.ForeignKey('receiving.GoodsReceiptPO', on_delete=models.SET_NULL, null=True, blank=True)
    invoice_date = models.DateField()
    due_date = models.DateField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
    file = models.FileField(upload_to='ap_invoices/', blank=True, null=True)
    three_way_match = models.BooleanField(default=False, help_text="PO vs GRPO vs Invoice matched")
    match_notes = models.TextField(blank=True)
    payment_date = models.DateField(null=True, blank=True)
    payment_reference = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "AP Invoice"
        ordering = ['-invoice_date']

    def __str__(self):
        return f"INV-{self.invoice_number}"

    def check_three_way_match(self):
        """Check if PO, GRPO, and Invoice all match"""
        if not self.ppo or not self.grpo:
            return False
        po_total = self.ppo.total
        grpo_ok = self.grpo.status == 'posted'
        inv_total = self.total_amount
        tolerance = float(po_total) * 0.01
        amounts_match = abs(float(po_total) - float(inv_total)) <= tolerance
        self.three_way_match = amounts_match and grpo_ok
        self.save()
        return self.three_way_match


class APInvoiceLine(models.Model):
    invoice = models.ForeignKey(APInvoice, on_delete=models.CASCADE, related_name='lines')
    item = models.ForeignKey('items.Item', on_delete=models.CASCADE)
    description = models.CharField(max_length=500, blank=True)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    line_total = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])

    def save(self, *args, **kwargs):
        self.line_total = self.quantity * self.unit_price
        super().save(*args, **kwargs)
