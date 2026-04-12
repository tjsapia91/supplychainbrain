from django.urls import path
from integrations import views

urlpatterns = [
    path('callback/', views.oauth_callback, name='oauth_callback'),
    path('connect/', views.oauth_connect, name='oauth_connect'),
    path('status/', views.oauth_status, name='oauth_status'),
]
