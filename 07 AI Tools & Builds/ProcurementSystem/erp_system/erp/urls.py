from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import views as auth_views
from accounts.views import LoginView, LogoutView


@login_required
def dashboard(request):
    from procurement.models import PlannedPurchaseOrder, PurchaseRequisition, ProformaInvoice
    from receiving.models import GoodsReceiptPO
    from items.models import Item
    from vendors.models import Vendor
    from invoicing.models import APInvoice
    from containers.models import ContainerPlan

    context = {
        'total_items': Item.objects.count(),
        'active_items': Item.objects.filter(inactive=False).count(),
        'total_vendors': Vendor.objects.filter(is_active=True).count(),
        'total_ppos': PlannedPurchaseOrder.objects.count(),
        'draft_ppos': PlannedPurchaseOrder.objects.filter(status='draft').count(),
        'pending_ceo_ppos': PlannedPurchaseOrder.objects.filter(status='pending_ceo_approval').count(),
        'active_ppos': PlannedPurchaseOrder.objects.filter(status__in=['confirmed', 'in_transit', 'partially_received']).count(),
        'pending_prs': PurchaseRequisition.objects.filter(status__in=['draft', 'submitted']).count(),
        'total_grpos': GoodsReceiptPO.objects.count(),
        'pending_invoices': APInvoice.objects.filter(status='pending').count(),
        'recent_ppos': PlannedPurchaseOrder.objects.all()[:10],
        'recent_grpos': GoodsReceiptPO.objects.all()[:5],
        'containers_in_transit': ContainerPlan.objects.filter(status__in=['in_transit', 'at_port', 'customs']).count(),
        'containers_planning': ContainerPlan.objects.filter(status__in=['planning', 'packing']).count(),
    }
    return render(request, 'dashboard.html', context)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('items/', include('items.urls')),
    path('vendors/', include('vendors.urls')),
    path('procurement/', include('procurement.urls')),
    path('receiving/', include('receiving.urls')),
    path('inventory/', include('inventory.urls')),
    path('invoicing/', include('invoicing.urls')),
    path('reports/', include('reports.urls')),
    path('containers/', include('containers.urls')),
    path('landed-costs/', include('landedcosts.urls')),
    path('oauth/', include('integrations.urls')),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # Password reset flow
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset.html',
        email_template_name='registration/password_reset_email.txt',
        html_email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt',
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html',
    ), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
    ), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html',
    ), name='password_reset_complete'),
    path('', dashboard, name='dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
