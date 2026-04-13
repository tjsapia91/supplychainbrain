from django.urls import path
from . import views

app_name = 'procurement'

urlpatterns = [
    # ============================================================================
    # Purchase Requisitions
    # ============================================================================
    path('requisitions/', views.PurchaseRequisitionListView.as_view(), name='pr_list'),
    path('requisitions/<int:pk>/', views.PurchaseRequisitionDetailView.as_view(), name='pr_detail'),
    path('requisitions/create/', views.PurchaseRequisitionCreateView.as_view(), name='pr_create'),
    path('requisitions/<int:pk>/approve/', views.approve_requisition, name='pr_approve'),

    # ============================================================================
    # Planned Purchase Orders
    # ============================================================================
    path('ppos/', views.PlannedPurchaseOrderListView.as_view(), name='ppo_list'),
    path('ppos/<int:pk>/', views.PlannedPurchaseOrderDetailView.as_view(), name='ppo_detail'),
    path('ppos/create/', views.PlannedPurchaseOrderCreateView.as_view(), name='ppo_create'),
    path('ppos/<int:pk>/edit/', views.PlannedPurchaseOrderUpdateView.as_view(), name='ppo_edit'),

    # PPO Batch Send
    path('ppos/batch-send/', views.ppo_batch_send, name='ppo_batch_send'),
    path('ppos/batch-send/confirm/', views.ppo_batch_send_confirm, name='ppo_batch_send_confirm'),

    # PPO Workflow Actions
    path('ppos/<int:pk>/send-to-vendor/', views.ppo_send_to_vendor, name='ppo_send_to_vendor'),
    path('ppos/<int:pk>/mark-pi-received/', views.ppo_mark_pi_received, name='ppo_mark_pi_received'),
    path('ppos/<int:pk>/request-ceo-approval/', views.ppo_request_ceo_approval, name='ppo_request_ceo_approval'),
    path('ppos/<int:pk>/ceo-approve/', views.ppo_ceo_approve, name='ppo_ceo_approve'),
    path('ppos/<int:pk>/ceo-reject/', views.ppo_ceo_reject, name='ppo_ceo_reject'),
    path('ppos/<int:pk>/cancel/', views.ppo_cancel, name='ppo_cancel'),
    path('ppos/<int:pk>/mark-in-transit/', views.ppo_mark_in_transit, name='ppo_mark_in_transit'),
    path('ppos/<int:pk>/close/', views.ppo_close, name='ppo_close'),
    path('ppos/<int:pk>/generate-pdf/', views.ppo_generate_pdf, name='ppo_generate_pdf'),
    path('ppos/<int:pk>/duplicate/', views.ppo_duplicate, name='ppo_duplicate'),

    # PPO Attachments
    path('ppos/<int:pk>/upload-attachment/', views.ppo_upload_attachment, name='ppo_upload_attachment'),

    # ============================================================================
    # Proforma Invoices
    # ============================================================================
    path('proforma-invoices/', views.ProformaInvoiceListView.as_view(), name='pi_list'),
    path('proforma-invoices/<int:pk>/', views.ProformaInvoiceDetailView.as_view(), name='pi_detail'),
    path('proforma-invoices/create/', views.ProformaInvoiceCreateView.as_view(), name='pi_create'),

    # ============================================================================
    # API/AJAX Endpoints
    # ============================================================================
    path('api/item-search/', views.item_search_api, name='item_search_api'),
    path('api/item-detail/<int:item_id>/', views.item_detail_api, name='item_detail_api'),
    path('api/vendor-defaults/<int:vendor_id>/', views.vendor_defaults_api, name='vendor_defaults_api'),
]
