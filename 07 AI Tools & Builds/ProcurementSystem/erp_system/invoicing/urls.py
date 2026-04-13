from django.urls import path
from . import views

app_name = 'invoicing'

urlpatterns = [
    path('', views.APInvoiceListView.as_view(), name='invoice_list'),
    path('<int:pk>/', views.APInvoiceDetailView.as_view(), name='invoice_detail'),
    path('create/', views.APInvoiceCreateView.as_view(), name='invoice_create'),
    path('<int:pk>/edit/', views.APInvoiceUpdateView.as_view(), name='invoice_edit'),
]
