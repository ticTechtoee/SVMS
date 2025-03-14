# Create urls.py
from django.urls import path
from .views import predict_view, train_model_view

urlpatterns = [
    path('train/', train_model_view, name='train_model'),
    path("predict/", predict_view, name="predict"),
]