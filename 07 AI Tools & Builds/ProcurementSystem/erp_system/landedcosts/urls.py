from django.urls import path
from . import views

app_name = 'landedcosts'

urlpatterns = [
    path('', views.LandedCostListView.as_view(), name='lc_list'),
    path('<int:pk>/', views.LandedCostDetailView.as_view(), name='lc_detail'),
    path('create/', views.LandedCostCreateView.as_view(), name='lc_create'),
    path('<int:pk>/edit/', views.LandedCostUpdateView.as_view(), name='lc_edit'),
    path('<int:pk>/calculate/', views.calculate_allocations, name='lc_calculate'),
    path('<int:pk>/post/', views.post_document, name='lc_post'),

    # API
    path('api/ppo-lookup/', views.ppo_lookup_for_lc, name='ppo_lookup_api'),
]
