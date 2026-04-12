from django.contrib import admin
from .models import APInvoice, APInvoiceLine


class APInvoiceLineInline(admin.TabularInline):
    model = APInvoiceLine
    extra = 1


@admin.register(APInvoice)
class APInvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'vendor', 'invoice_date', 'total_amount', 'status', 'three_way_match')
    list_filter = ('status', 'invoice_date', 'vendor', 'three_way_match')
    search_fields = ('invoice_number', 'vendor__name', 'ppo__ppo_number')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [APInvoiceLineInline]
    fieldsets = (
        ('Invoice Information', {
            'fields': ('invoice_number', 'vendor', 'invoice_date', 'due_date')
        }),
        ('Amount & Currency', {
            'fields': ('total_amount', 'currency')
        }),
        ('Matching', {
            'fields': ('ppo', 'grpo', 'three_way_match', 'match_notes')
        }),
        ('Status', {
            'fields': ('status', 'file')
        }),
        ('Payment', {
            'fields': ('payment_date', 'payment_reference')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
