from django.urls import path
from .views import admin_dashboard

app_name = 'dashboardApp'

urlpatterns = [
    path('detail/', admin_dashboard, name='admin_dashboard'),
]
