from django.urls import path
from . import views

app_name = 'receiving'

urlpatterns = [
    path('', views.GoodsReceiptPOListView.as_view(), name='grpo_list'),
    path('<int:pk>/', views.GoodsReceiptPODetailView.as_view(), name='grpo_detail'),
    path('create/', views.GoodsReceiptPOCreateView.as_view(), name='grpo_create'),
    path('<int:pk>/edit/', views.GoodsReceiptPOUpdateView.as_view(), name='grpo_edit'),

    # API
    path('api/ppo-lookup/', views.ppo_lookup_api, name='ppo_lookup_api'),
]
