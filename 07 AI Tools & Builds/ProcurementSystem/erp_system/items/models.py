from django.db import models
from django.core.validators import MinValueValidator
import math


class Item(models.Model):
    ABC_CHOICES = [
        ('A', 'A - High Volume'),
        ('C', 'C - Low Volume'),
        ('D', 'D - Phase-In'),
        ('E', 'E - Phase-Out'),
        ('F', 'F - Other'),
        ('I', 'I - Ind. Comp.'),
    ]
    item_no = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.CharField(max_length=500, blank=True)
    in_stock = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    default_warehouse = models.ForeignKey('inventory.Warehouse', null=True, blank=True, on_delete=models.SET_NULL)
    last_purchase_date = models.DateField(null=True, blank=True)
    qty_ordered_by_customers = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    abc_classification = models.CharField(max_length=2, choices=ABC_CHOICES, blank=True, db_index=True)
    qty_ordered_from_vendors = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    property_1 = models.CharField(max_length=100, blank=True, default='No')
    property_2 = models.CharField(max_length=100, blank=True, default='No')
    height_uom = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    length_uom = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    width_uom = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    weight_uom = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    superseding_item = models.CharField(max_length=50, blank=True)
    upc_inner_carton_qty = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    upc_master_carton_qty = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    master_carton_volume = models.DecimalField(max_digits=12, decimal_places=6, default=0, validators=[MinValueValidator(0)], help_text="Volume in cubic inches")
    issue_price = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    height_purchasing_unit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    inactive = models.BooleanField(default=False, db_index=True)
    branch = models.CharField(max_length=100, blank=True, db_index=True, help_text="Michael Todd Beauty, Spa Sciences, NasaFresh MD")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['item_no']

    def __str__(self):
        return f"{self.item_no} - {self.description}"

    def calculate_cartons(self, qty):
        """Calculate number of master cartons needed for given quantity"""
        if self.upc_master_carton_qty and self.upc_master_carton_qty > 0:
            return math.ceil(qty / self.upc_master_carton_qty)
        return None

    def calculate_cbm(self, cartons):
        """Calculate CBM for given number of cartons.
        master_carton_volume is already stored in CBM per carton.
        """
        if cartons and self.master_carton_volume and self.master_carton_volume > 0:
            return float(cartons) * float(self.master_carton_volume)
        return None
