# news/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Define URL patterns for the news app here
    path('', views.index, name='index'),  # Example view
]
