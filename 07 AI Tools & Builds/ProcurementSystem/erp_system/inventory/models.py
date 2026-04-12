from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


class Warehouse(models.Model):
    code = models.CharField(max_length=20, unique=True, db_index=True)
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class StockLevel(models.Model):
    item = models.ForeignKey('items.Item', on_delete=models.CASCADE, related_name='stock_levels')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stock_levels')
    quantity = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    reorder_point = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    reorder_qty = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('item', 'warehouse')

    def __str__(self):
        return f"{self.item.item_no} @ {self.warehouse.code}: {self.quantity}"


class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('in', 'Stock In (GRPO)'),
        ('out', 'Stock Out'),
        ('adjustment', 'Adjustment'),
        ('transfer', 'Transfer'),
    ]
    item = models.ForeignKey('items.Item', on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES, db_index=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    reference_type = models.CharField(max_length=50, blank=True, help_text="GRPO, Adjustment, etc.")
    reference_number = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
