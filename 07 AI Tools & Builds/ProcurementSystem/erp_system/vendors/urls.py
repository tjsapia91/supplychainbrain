from django.urls import path
from . import views

app_name = 'vendors'

urlpatterns = [
    # Vendors
    path('', views.VendorListView.as_view(), name='vendor_list'),
    path('<int:pk>/', views.VendorDetailView.as_view(), name='vendor_detail'),
    path('create/', views.VendorCreateView.as_view(), name='vendor_create'),
    path('<int:pk>/edit/', views.VendorUpdateView.as_view(), name='vendor_edit'),
    path('<int:pk>/delete/', views.VendorDeleteView.as_view(), name='vendor_delete'),

    # Branches
    path('branches/', views.BranchListView.as_view(), name='branch_list'),
    path('branches/create/', views.BranchCreateView.as_view(), name='branch_create'),
    path('branches/<int:pk>/edit/', views.BranchUpdateView.as_view(), name='branch_edit'),

    # 3PL Providers
    path('3pl/', views.ThreePLListView.as_view(), name='threepl_list'),
    path('3pl/<int:pk>/', views.ThreePLDetailView.as_view(), name='threepl_detail'),
    path('3pl/create/', views.ThreePLCreateView.as_view(), name='threepl_create'),
    path('3pl/<int:pk>/edit/', views.ThreePLUpdateView.as_view(), name='threepl_edit'),

    # Bill-To Addresses
    path('billto/', views.BillToAddressListView.as_view(), name='billto_list'),
    path('billto/create/', views.BillToAddressCreateView.as_view(), name='billto_create'),
    path('billto/<int:pk>/edit/', views.BillToAddressUpdateView.as_view(), name='billto_edit'),

    # Ship-To Addresses (legacy)
    path('shipto/', views.ShipToAddressListView.as_view(), name='shipto_list'),
    path('shipto/create/', views.ShipToAddressCreateView.as_view(), name='shipto_create'),
    path('shipto/<int:pk>/edit/', views.ShipToAddressUpdateView.as_view(), name='shipto_edit'),
]
