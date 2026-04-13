from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.reports_hub, name='hub'),
    path('upload/', views.upload_report, name='upload'),
    path('upload/<int:upload_id>/status/', views.upload_status, name='upload_status'),
    path('data/', views.data_list, name='data_list'),
    path('compare/', views.sku_compare, name='compare'),
    path('alerts/', views.reorder_alerts, name='alerts'),
    path('sources/', views.manage_sources, name='sources'),
    path('api/chart-data/', views.chart_data_api, name='chart_data'),
]
