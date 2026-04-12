from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.container_dashboard, name='container_dashboard'),

    # Container CRUD
    path('list/', views.container_list, name='container_list'),
    path('new/', views.container_create, name='container_create'),
    path('<int:pk>/', views.container_detail, name='container_detail'),
    path('<int:pk>/edit/', views.container_edit, name='container_edit'),
    path('<int:pk>/status/', views.container_update_status, name='container_update_status'),

    # Container items
    path('<int:pk>/add-item/', views.container_add_item, name='container_add_item'),
    path('<int:pk>/allocate/', views.container_allocate_ppo, name='container_allocate_ppo'),
    path('<int:pk>/remove-item/<int:item_pk>/', views.container_remove_item, name='container_remove_item'),
    path('<int:pk>/receive/', views.container_receive, name='container_receive'),
    path('<int:pk>/generate-grpos/', views.container_generate_grpos, name='container_generate_grpos'),
    path('<int:pk>/confirm-grpos/', views.container_confirm_grpos, name='container_confirm_grpos'),

    # Exports
    path('<int:pk>/export/', views.export_container_csv, name='export_container_csv'),
    path('export-transit/', views.export_transit_csv, name='export_transit_csv'),

    # In-transit tracking
    path('in-transit/', views.in_transit_list, name='in_transit_list'),

    # Demand forecasting
    path('forecast/', views.forecast_dashboard, name='forecast_dashboard'),
    path('forecast/new/', views.forecast_create, name='forecast_create'),
    path('forecast/upload/', views.forecast_bulk_upload, name='forecast_bulk_upload'),
    path('forecast/item/<str:item_no>/', views.forecast_item_detail, name='forecast_item_detail'),

    # Smart Document Upload
    path('upload-doc/', views.document_upload, name='document_upload'),
    path('upload-doc/review/', views.document_review, name='document_review'),
    path('upload-doc/confirm/', views.document_confirm, name='document_confirm'),

    # API
    path('api/ppo-lines/', views.api_ppo_lines, name='api_ppo_lines'),
    path('api/forecast/<str:item_no>/', views.api_item_forecast, name='api_item_forecast'),
    path('api/alerts/', views.dashboard_alerts_api, name='dashboard_alerts_api'),
]
