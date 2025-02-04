from django.urls import path, include
from . import views

APP_NAME = 'home'

urlpatterns = [
    path('', views.viewHome, name="HomeView"),
]
