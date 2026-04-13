from django.contrib import admin
from .models import CostComponent, LandedCostDocument, LandedCostLine, LandedCostItemAllocation


@admin.register(CostComponent)
class CostComponentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'default_allocation', 'include_for_customs', 'is_active', 'sort_order']
    list_editable = ['sort_order', 'is_active']


class LandedCostLineInline(admin.TabularInline):
    model = LandedCostLine
    extra = 0


class LandedCostItemInline(admin.TabularInline):
    model = LandedCostItemAllocation
    extra = 0
    readonly_fields = ['customs_value', 'total_allocated_costs', 'warehouse_price', 'total_line_cost']


@admin.register(LandedCostDocument)
class LandedCostDocumentAdmin(admin.ModelAdmin):
    list_display = ['lc_number', 'status', 'vendor', 'branch', 'ppo', 'document_date', 'total_costs']
    list_filter = ['status', 'branch']
    inlines = [LandedCostLineInline, LandedCostItemInline]
