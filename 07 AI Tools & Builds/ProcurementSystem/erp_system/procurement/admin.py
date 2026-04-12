from django.contrib import admin
from .models import (
    PurchaseRequisition,
    PurchaseRequisitionLine,
    PlannedPurchaseOrder,
    PPOLineItem,
    ProformaInvoice,
    PPOAttachment,
    PPOStatusLog,
)


# ============================================================================
# PURCHASE REQUISITION ADMIN
# ============================================================================

class PurchaseRequisitionLineInline(admin.TabularInline):
    model = PurchaseRequisitionLine
    extra = 1
    fields = ('item', 'quantity', 'suggested_vendor', 'notes')


@admin.register(PurchaseRequisition)
class PurchaseRequisitionAdmin(admin.ModelAdmin):
    list_display = ('pr_number', 'date', 'requested_by', 'status', 'priority', 'created_at')
    list_filter = ('status', 'priority', 'date')
    search_fields = ('pr_number', 'requested_by__username', 'requested_by__first_name', 'requested_by__last_name')
    readonly_fields = ('pr_number', 'created_at', 'updated_at', 'approved_date')
    inlines = [PurchaseRequisitionLineInline]
    fieldsets = (
        ('Requisition Information', {
            'fields': ('pr_number', 'date', 'status', 'requested_by', 'approved_by', 'approved_date')
        }),
        ('Details', {
            'fields': ('priority', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PurchaseRequisitionLine)
class PurchaseRequisitionLineAdmin(admin.ModelAdmin):
    list_display = ('requisition', 'item', 'quantity', 'suggested_vendor')
    list_filter = ('requisition__status', 'suggested_vendor')
    search_fields = ('requisition__pr_number', 'item__item_no', 'item__description')
    fields = ('requisition', 'item', 'quantity', 'suggested_vendor', 'notes')


# ============================================================================
# PLANNED PURCHASE ORDER ADMIN
# ============================================================================

class PPOLineItemInline(admin.TabularInline):
    model = PPOLineItem
    extra = 1
    fields = ('line_number', 'item', 'quantity', 'unit_price', 'destination', 'notes')
    readonly_fields = ('line_number', 'cartons', 'cbm', 'total_weight', 'line_total')


class PPOAttachmentInline(admin.TabularInline):
    model = PPOAttachment
    extra = 1
    fields = ('file', 'file_type', 'description', 'uploaded_by', 'uploaded_at')
    readonly_fields = ('uploaded_by', 'uploaded_at')


class PPOStatusLogInline(admin.TabularInline):
    model = PPOStatusLog
    extra = 0
    fields = ('from_status', 'to_status', 'changed_by', 'timestamp', 'notes')
    readonly_fields = ('from_status', 'to_status', 'changed_by', 'timestamp', 'notes')
    can_delete = False


@admin.register(PlannedPurchaseOrder)
class PlannedPurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('ppo_number', 'vendor', 'date', 'status', 'total', 'currency', 'created_by')
    list_filter = ('status', 'vendor', 'date', 'mode_of_transport', 'incoterms')
    search_fields = ('ppo_number', 'vendor__name', 'created_by__username')
    readonly_fields = (
        'ppo_number', 'total_cartons', 'total_cbm', 'total_weight', 'subtotal',
        'balance_due', 'total', 'created_at', 'updated_at', 'vendor_email_sent_date',
        'ceo_approval_requested_date', 'ceo_approval_date'
    )
    inlines = [PPOLineItemInline, PPOAttachmentInline, PPOStatusLogInline]
    fieldsets = (
        ('Purchase Order Information', {
            'fields': ('ppo_number', 'date', 'status', 'vendor', 'created_by', 'purchase_requisition')
        }),
        ('Addresses', {
            'fields': ('bill_to', 'ship_to')
        }),
        ('Shipping Details', {
            'fields': (
                'requested_ship_date', 'estimated_ship_date', 'actual_ship_date',
                'mode_of_transport', 'port_of_loading', 'port_of_discharge',
                'country_of_origin', 'incoterms', 'awb_bl_number', 'lead_time_days'
            )
        }),
        ('Totals', {
            'fields': (
                'total_cartons', 'total_cbm', 'total_weight', 'subtotal',
                'deposit', 'balance_due', 'total'
            )
        }),
        ('Financial', {
            'fields': ('currency', 'payment_terms', 'wire_info', 'vendor_pi_number')
        }),
        ('Notes', {
            'fields': ('special_notes',)
        }),
        ('CEO Approval Workflow', {
            'fields': (
                'ceo_approval_requested_date', 'ceo_approved_by', 'ceo_approval_date',
                'ceo_rejection_reason'
            ),
            'classes': ('collapse',)
        }),
        ('Vendor Communication', {
            'fields': ('vendor_email_sent_date',),
            'classes': ('collapse',)
        }),
        ('Documents', {
            'fields': ('pdf_file',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PPOLineItem)
class PPOLineItemAdmin(admin.ModelAdmin):
    list_display = ('ppo', 'line_number', 'item', 'quantity', 'unit_price', 'line_total')
    list_filter = ('ppo__status', 'ppo__vendor', 'ppo__date')
    search_fields = ('ppo__ppo_number', 'item__item_no', 'item__description')
    readonly_fields = ('line_total', 'cartons', 'cbm', 'total_weight')
    fieldsets = (
        ('Line Item Details', {
            'fields': ('ppo', 'line_number', 'item', 'description', 'quantity', 'unit_price')
        }),
        ('Calculated Fields', {
            'fields': ('cartons', 'cbm', 'total_weight', 'line_total')
        }),
        ('Logistics', {
            'fields': ('destination', 'qty_received')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
    )


# ============================================================================
# PROFORMA INVOICE ADMIN
# ============================================================================

@admin.register(ProformaInvoice)
class ProformaInvoiceAdmin(admin.ModelAdmin):
    list_display = ('pi_number', 'ppo', 'vendor', 'date', 'status', 'total_amount', 'currency')
    list_filter = ('status', 'date', 'vendor', 'ppo__status')
    search_fields = ('pi_number', 'ppo__ppo_number', 'vendor__name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Proforma Invoice Details', {
            'fields': ('ppo', 'pi_number', 'vendor', 'date', 'status')
        }),
        ('Financial Information', {
            'fields': ('total_amount', 'currency')
        }),
        ('Documents', {
            'fields': ('file',)
        }),
        ('Review', {
            'fields': ('reviewed_by', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# ============================================================================
# PPO ATTACHMENT ADMIN
# ============================================================================

@admin.register(PPOAttachment)
class PPOAttachmentAdmin(admin.ModelAdmin):
    list_display = ('ppo', 'file_type', 'description', 'uploaded_by', 'uploaded_at')
    list_filter = ('file_type', 'uploaded_at', 'ppo__status')
    search_fields = ('ppo__ppo_number', 'description', 'uploaded_by__username')
    readonly_fields = ('uploaded_at',)
    fieldsets = (
        ('Attachment Details', {
            'fields': ('ppo', 'file', 'file_type', 'description')
        }),
        ('Upload Information', {
            'fields': ('uploaded_by', 'uploaded_at'),
            'classes': ('collapse',)
        }),
    )


# ============================================================================
# PPO STATUS LOG ADMIN (Read-only)
# ============================================================================

@admin.register(PPOStatusLog)
class PPOStatusLogAdmin(admin.ModelAdmin):
    list_display = ('ppo', 'from_status', 'to_status', 'changed_by', 'timestamp')
    list_filter = ('to_status', 'timestamp', 'ppo__vendor')
    search_fields = ('ppo__ppo_number', 'changed_by__username')
    readonly_fields = ('ppo', 'from_status', 'to_status', 'changed_by', 'timestamp', 'notes')
    fields = ('ppo', 'from_status', 'to_status', 'changed_by', 'timestamp', 'notes')
    can_delete = False

    def has_add_permission(self, request):
        return False
