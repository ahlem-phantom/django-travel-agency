# support/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Define URL patterns specific to the support app here
    path('', views.index, name='index'),  # Example view
]
