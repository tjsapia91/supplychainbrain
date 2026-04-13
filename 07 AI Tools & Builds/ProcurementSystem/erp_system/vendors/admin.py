from django.contrib import admin
from .models import Vendor, BillToAddress, ShipToAddress, Branch, ThreePLProvider


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'city', 'country', 'is_active', 'rating')
    list_filter = ('is_active', 'country', 'created_at')
    search_fields = ('name', 'code', 'email', 'contact_name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'is_active')
        }),
        ('Contact Information', {
            'fields': ('address', 'city', 'state', 'country', 'postal_code', 'phone', 'email')
        }),
        ('Primary Contact', {
            'fields': ('contact_name', 'contact_email')
        }),
        ('Payment & Logistics', {
            'fields': ('payment_terms', 'lead_time_days', 'currency', 'wire_info')
        }),
        ('Performance', {
            'fields': ('rating', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'contact_email', 'is_active')
    search_fields = ('name',)


@admin.register(BillToAddress)
class BillToAddressAdmin(admin.ModelAdmin):
    list_display = ('branch', 'phone', 'is_default')
    list_filter = ('is_default',)
    search_fields = ('branch', 'address', 'contact')


@admin.register(ThreePLProvider)
class ThreePLProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'city', 'state', 'contact_name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code', 'contact_name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Provider Info', {
            'fields': ('name', 'code', 'account_number', 'is_active')
        }),
        ('Warehouse Address', {
            'fields': ('address', 'city', 'state', 'zip_code', 'country')
        }),
        ('Contact', {
            'fields': ('phone', 'contact_name', 'contact_email')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
    )


@admin.register(ShipToAddress)
class ShipToAddressAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'state', 'country', 'is_default')
    list_filter = ('country', 'is_default')
    search_fields = ('name', 'address', 'city')
