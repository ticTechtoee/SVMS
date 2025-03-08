from django.urls import path
from .views import create_company

app_name  = 'companyApp'

urlpatterns = [
    path('create/', create_company, name='create_company'),
]
