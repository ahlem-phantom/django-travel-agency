# chat/urls.py
from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),
    path('handle_button_click/', views.handle_button_click, name='handle_button_click'),
]
