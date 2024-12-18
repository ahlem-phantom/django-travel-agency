from django.urls import path
from . import views

urlpatterns = [
    # TravelPackage URLs
    path('travel-packages/', views.travel_package_list, name='package_list'),
    path('travel-package/create/', views.travel_package_create, name='travel_package_create'),
    path('travel-package/<int:pk>/update/', views.travel_package_update, name='travel_package_update'),
    path('travel-package/<int:pk>/delete/', views.travel_package_delete, name='travel_package_delete'),

    # Tag URLs
    path('tags/', views.tag_list, name='tag_list'),
    path('tag/create/', views.tag_create, name='tag_create'),
    path('tag/<int:pk>/update/', views.tag_update, name='tag_update'),
    path('tag/<int:pk>/delete/', views.tag_delete, name='tag_delete'),

    # TravelPackageTag URLs
    path('', views.travel_package_list, name='travel_packages_list'),
    path('book/<int:pk>', views.book_package, name='travel_package_booking'),

    path('book/<int:package_id>/', views.booking_handler_view, name='booking_handler_view'),
    path('success/', views.booking_success, name='booking_success'),
    path('fail/', views.booking_fail, name='booking_fail'),
    path('recommendations/', views.packages_recommendations, name='packages_recommendations'),

]
