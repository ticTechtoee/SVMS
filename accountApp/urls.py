from django.urls import path
from . import views

app_name  = 'accountApp'


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create-employee/', views.create_employee_view, name='create_employee'),
]

