from django.contrib import admin
from .models import Warehouse, StockLevel, StockMovement


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('code', 'name')


@admin.register(StockLevel)
class StockLevelAdmin(admin.ModelAdmin):
    list_display = ('item', 'warehouse', 'quantity', 'reorder_point', 'last_updated')
    list_filter = ('warehouse', 'last_updated')
    search_fields = ('item__item_no', 'warehouse__code')
    readonly_fields = ('last_updated',)


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('item', 'warehouse', 'movement_type', 'quantity', 'created_at')
    list_filter = ('movement_type', 'warehouse', 'created_at')
    search_fields = ('item__item_no', 'reference_number')
    readonly_fields = ('created_at',)
