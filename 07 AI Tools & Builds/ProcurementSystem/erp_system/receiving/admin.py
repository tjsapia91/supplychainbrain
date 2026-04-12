from django.contrib import admin
from .models import GoodsReceiptPO, GRPOLineItem


class GRPOLineItemInline(admin.TabularInline):
    model = GRPOLineItem
    extra = 1


@admin.register(GoodsReceiptPO)
class GoodsReceiptPOAdmin(admin.ModelAdmin):
    list_display = ('grpo_number', 'ppo', 'vendor', 'receipt_date', 'status')
    list_filter = ('status', 'receipt_date', 'warehouse')
    search_fields = ('grpo_number', 'ppo__ppo_number', 'vendor__name')
    readonly_fields = ('grpo_number', 'total_cartons_received', 'total_cbm_received', 'created_at', 'updated_at')
    inlines = [GRPOLineItemInline]
