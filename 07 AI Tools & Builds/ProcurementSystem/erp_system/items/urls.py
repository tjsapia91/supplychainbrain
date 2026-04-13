from django.urls import path
from . import views

app_name = 'items'

urlpatterns = [
    path('', views.ItemListView.as_view(), name='item_list'),
    path('<int:pk>/', views.ItemDetailView.as_view(), name='item_detail'),
    path('create/', views.ItemCreateView.as_view(), name='item_create'),
    path('<int:pk>/edit/', views.ItemUpdateView.as_view(), name='item_edit'),
    path('<int:pk>/delete/', views.ItemDeleteView.as_view(), name='item_delete'),
]
