from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


class GoodsReceiptPO(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('cancelled', 'Cancelled'),
    ]
    grpo_number = models.CharField(max_length=20, unique=True)
    ppo = models.ForeignKey('procurement.PlannedPurchaseOrder', on_delete=models.CASCADE, related_name='goods_receipts')
    vendor = models.ForeignKey('vendors.Vendor', on_delete=models.CASCADE)
    receipt_date = models.DateField()
    posting_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', db_index=True)
    warehouse = models.ForeignKey('vendors.ThreePLProvider', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Receiving 3PL")
    reference = models.CharField(max_length=100, blank=True, help_text="AWB/BL or tracking reference")
    notes = models.TextField(blank=True)
    received_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    total_cartons_received = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    total_cbm_received = models.DecimalField(max_digits=12, decimal_places=6, default=0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Goods Receipt PO"
        verbose_name_plural = "Goods Receipt POs"
        ordering = ['-receipt_date']

    def __str__(self):
        return f"GRPO-{self.grpo_number}"

    @classmethod
    def get_next_grpo_number(cls):
        last = cls.objects.order_by('-id').first()
        if last:
            num = int(last.grpo_number) + 1
        else:
            num = 1001
        return str(num)


class GRPOLineItem(models.Model):
    grpo = models.ForeignKey(GoodsReceiptPO, on_delete=models.CASCADE, related_name='lines')
    ppo_line = models.ForeignKey('procurement.PPOLineItem', on_delete=models.CASCADE, related_name='grpo_lines')
    item = models.ForeignKey('items.Item', on_delete=models.CASCADE)
    description = models.CharField(max_length=500, blank=True)
    destination = models.CharField(max_length=200, blank=True)
    quantity_expected = models.IntegerField(validators=[MinValueValidator(0)])
    quantity_received = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    quantity_damaged = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    quantity_accepted = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    batch_number = models.CharField(max_length=100, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        self.quantity_accepted = self.quantity_received - self.quantity_damaged
        super().save(*args, **kwargs)

    @property
    def variance(self):
        return self.quantity_received - self.quantity_expected

    def __str__(self):
        return f"{self.item.item_no}: {self.quantity_received}/{self.quantity_expected}"
