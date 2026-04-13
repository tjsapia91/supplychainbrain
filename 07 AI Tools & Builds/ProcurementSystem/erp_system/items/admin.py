from django.contrib import admin
from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_no', 'description', 'in_stock', 'abc_classification', 'branch', 'inactive')
    list_filter = ('abc_classification', 'branch', 'inactive', 'created_at')
    search_fields = ('item_no', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('item_no', 'description', 'branch')
        }),
        ('Inventory', {
            'fields': ('in_stock', 'default_warehouse', 'last_purchase_date', 'qty_ordered_by_customers', 'qty_ordered_from_vendors')
        }),
        ('Classification', {
            'fields': ('abc_classification', 'property_1', 'property_2')
        }),
        ('Dimensions & Specifications', {
            'fields': ('height_uom', 'length_uom', 'width_uom', 'weight_uom')
        }),
        ('Carton Information', {
            'fields': ('upc_inner_carton_qty', 'upc_master_carton_qty', 'master_carton_volume', 'height_purchasing_unit')
        }),
        ('Pricing', {
            'fields': ('issue_price',)
        }),
        ('Other', {
            'fields': ('superseding_item', 'inactive')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
