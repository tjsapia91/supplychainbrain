from django.db import models
from django.conf import settings
from decimal import Decimal


class CostComponent(models.Model):
    """Master list of cost types (Freight, Tariffs, Drayage, etc.)"""
    ALLOCATION_CHOICES = [
        ('quantity', 'Quantity'),
        ('volume', 'Volume (CBM)'),
        ('cash_value', 'Cash Value Before Customs'),
    ]
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=30, unique=True)
    default_allocation = models.CharField(max_length=20, choices=ALLOCATION_CHOICES, default='quantity')
    include_for_customs = models.BooleanField(default=False, help_text="Include in customs value calculation by default")
    is_active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name


class LandedCostDocument(models.Model):
    """A landed cost document — tracks all shipping/import costs for a PO shipment."""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('calculated', 'Calculated'),
        ('posted', 'Posted'),
        ('cancelled', 'Cancelled'),
    ]
    lc_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    vendor = models.ForeignKey('vendors.Vendor', on_delete=models.CASCADE, related_name='landed_costs',
                               help_text="Shipping/logistics vendor")
    branch = models.ForeignKey('vendors.Branch', on_delete=models.SET_NULL, null=True, blank=True)
    ppo = models.ForeignKey('procurement.PlannedPurchaseOrder', on_delete=models.CASCADE,
                            related_name='landed_costs', help_text="Purchase Order these costs apply to")
    container = models.ForeignKey('containers.ContainerPlan', on_delete=models.SET_NULL,
                                  null=True, blank=True, related_name='landed_costs')
    grpo = models.ForeignKey('receiving.GoodsReceiptPO', on_delete=models.SET_NULL,
                             null=True, blank=True, related_name='landed_costs',
                             help_text="Set when GRPO confirms receipt")
    document_date = models.DateField()
    posting_date = models.DateField(null=True, blank=True)
    total_costs = models.DecimalField(max_digits=14, decimal_places=2, default=0,
                                      help_text="Sum of all cost lines")
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                   null=True, related_name='landed_costs_created')
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                  null=True, blank=True, related_name='landed_costs_posted')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Landed Cost Document"
        verbose_name_plural = "Landed Cost Documents"
        ordering = ['-document_date']

    def __str__(self):
        return f"LC-{self.lc_number}"

    @classmethod
    def get_next_lc_number(cls):
        last = cls.objects.order_by('-id').first()
        if last:
            try:
                num = int(last.lc_number) + 1
            except ValueError:
                num = 1001
        else:
            num = 1001
        return str(num)

    def calculate_allocations(self):
        """Run the allocation engine — distribute costs across items."""
        items = self.item_allocations.all()
        cost_lines = self.cost_lines.all()

        if not items.exists() or not cost_lines.exists():
            return

        # Calculate totals for each allocation basis
        total_qty = sum(i.quantity or 0 for i in items)
        total_volume = sum(float(i.volume_cbm or 0) for i in items)
        total_cash_value = sum(float(i.base_doc_value or 0) for i in items)

        # Reset all allocations
        for item in items:
            item.total_allocated_costs = Decimal('0')
            item.customs_value = Decimal('0')

        # Distribute each cost line
        for cl in cost_lines:
            amount = cl.amount or Decimal('0')
            if amount == 0:
                continue

            for item in items:
                if cl.allocation_by == 'quantity' and total_qty > 0:
                    share = Decimal(str(item.quantity or 0)) / Decimal(str(total_qty))
                elif cl.allocation_by == 'volume' and total_volume > 0:
                    share = Decimal(str(float(item.volume_cbm or 0))) / Decimal(str(total_volume))
                elif cl.allocation_by == 'cash_value' and total_cash_value > 0:
                    share = Decimal(str(float(item.base_doc_value or 0))) / Decimal(str(total_cash_value))
                else:
                    share = Decimal('0')

                allocated = (amount * share).quantize(Decimal('0.01'))
                item.total_allocated_costs += allocated

                # If this cost is included for customs, add to customs value
                if cl.include_for_customs:
                    item.customs_value += allocated

        # Calculate per-unit prices and save
        total_all_costs = Decimal('0')
        for item in items:
            item.customs_value += item.base_doc_value  # Customs value = FOB value + customs-included costs
            qty = item.quantity or 1
            item.warehouse_price = ((item.base_doc_value + item.total_allocated_costs) / qty).quantize(Decimal('0.000001'))
            item.total_line_cost = item.base_doc_value + item.total_allocated_costs
            total_all_costs += item.total_allocated_costs
            item.save()

        # Update document total
        self.total_costs = sum(cl.amount or 0 for cl in cost_lines)
        self.status = 'calculated'
        self.save()

    def populate_items_from_ppo(self):
        """Auto-populate item lines from the linked Purchase Order."""
        if not self.ppo:
            return
        existing_lines = set(self.item_allocations.values_list('ppo_line_id', flat=True))
        for line in self.ppo.lines.select_related('item').all():
            if line.pk not in existing_lines:
                LandedCostItemAllocation.objects.create(
                    document=self,
                    ppo_line=line,
                    item=line.item,
                    quantity=line.quantity or 0,
                    base_doc_price=line.unit_price or Decimal('0'),
                    base_doc_value=line.line_total or Decimal('0'),
                    volume_cbm=line.cbm or Decimal('0'),
                    warehouse=self.ppo.ship_to_3pl,
                )


class LandedCostLine(models.Model):
    """One row in the Costs tab — a cost component with its amount and allocation method."""
    ALLOCATION_CHOICES = [
        ('quantity', 'Quantity'),
        ('volume', 'Volume (CBM)'),
        ('cash_value', 'Cash Value Before Customs'),
    ]
    document = models.ForeignKey(LandedCostDocument, on_delete=models.CASCADE, related_name='cost_lines')
    cost_component = models.ForeignKey(CostComponent, on_delete=models.CASCADE)
    allocation_by = models.CharField(max_length=20, choices=ALLOCATION_CHOICES)
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    include_for_customs = models.BooleanField(default=False)

    class Meta:
        ordering = ['cost_component__sort_order']

    def __str__(self):
        return f"{self.cost_component.name}: ${self.amount}"

    def save(self, *args, **kwargs):
        # Default allocation from cost component if not set
        if not self.allocation_by and self.cost_component:
            self.allocation_by = self.cost_component.default_allocation
        if self.cost_component and not self.pk:
            self.include_for_customs = self.cost_component.include_for_customs
        super().save(*args, **kwargs)


class LandedCostItemAllocation(models.Model):
    """One row in the Items tab — shows how costs are allocated to each PO line item."""
    document = models.ForeignKey(LandedCostDocument, on_delete=models.CASCADE, related_name='item_allocations')
    ppo_line = models.ForeignKey('procurement.PPOLineItem', on_delete=models.CASCADE, related_name='landed_cost_allocations')
    item = models.ForeignKey('items.Item', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    volume_cbm = models.DecimalField(max_digits=12, decimal_places=6, default=0)
    base_doc_price = models.DecimalField(max_digits=12, decimal_places=3, default=0,
                                         help_text="FOB unit price from PO")
    base_doc_value = models.DecimalField(max_digits=14, decimal_places=2, default=0,
                                         help_text="qty x base price")
    customs_value = models.DecimalField(max_digits=14, decimal_places=3, default=0,
                                        help_text="Value for customs calculation")
    total_allocated_costs = models.DecimalField(max_digits=14, decimal_places=2, default=0,
                                                help_text="All costs allocated to this line")
    warehouse_price = models.DecimalField(max_digits=12, decimal_places=6, default=0,
                                          help_text="Per-unit cost including all allocated costs")
    total_line_cost = models.DecimalField(max_digits=14, decimal_places=2, default=0,
                                          help_text="Full cost for this line (FOB + allocated)")
    warehouse = models.ForeignKey('vendors.ThreePLProvider', on_delete=models.SET_NULL,
                                  null=True, blank=True)

    class Meta:
        ordering = ['ppo_line__line_number']

    def __str__(self):
        return f"{self.item.item_no}: {self.quantity} units @ ${self.warehouse_price}/unit"
