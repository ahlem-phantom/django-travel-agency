from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home-index'),  # Home page
    path('404/', views.not_found, name='404'),  # 404 page
]