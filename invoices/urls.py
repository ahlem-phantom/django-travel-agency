# invoices/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Add your URL patterns for the invoices app here
    path('', views.index, name='index'),  # Example view
]
