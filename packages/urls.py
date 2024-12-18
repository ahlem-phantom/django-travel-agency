from django.urls import path
from . import views

urlpatterns = [
    path('', views.travel_package_list, name='travel_packages_list'),
    path('book/<int:package_id>/', views.booking_handler_view, name='booking_handler_view'),
    path('success/', views.booking_success, name='booking_success'),
    path('fail/', views.booking_fail, name='booking_fail'),
    path('recommendations/', views.packages_recommendations, name='packages_recommendations')
]
