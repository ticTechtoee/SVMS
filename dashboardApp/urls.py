from django.urls import path
from .views import admin_dashboard, vehicle_maintenance_detail, viewUserDetail, support_view, faq_view

app_name = 'dashboardApp'

urlpatterns = [
    path('', admin_dashboard, name='admin_dashboard'),
    path('users_detail', viewUserDetail, name="UserDetailView"),
    path('vehicle/<str:vehicle_id>/maintenance/', vehicle_maintenance_detail, name='vehicle_maintenance_detail'),
    path('faq/', faq_view, name='faq'),
    path('support/', support_view, name='support'),

]
