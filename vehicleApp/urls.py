from django.urls import path
from .views import create_vehicle

urlpatterns = [
    path('create/', create_vehicle, name='create_vehicle'),
]
