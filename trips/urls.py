from django.urls import path
from .views import RecommendationView, package_list, package_detail, package_create, package_update, package_delete, rate_trip
from django.conf import settings
from django.conf.urls.static import static


app_name = 'trips' 

urlpatterns = [
    path('recommendations/', RecommendationView.as_view(), name='recommendations'),
    path('', package_list, name='package_list'),
    path('<int:pk>/', package_detail, name='package_detail'),
    path('create/', package_create, name='package_create'),
    path('<int:pk>/update/', package_update, name='package_update'),
    path('<int:pk>/delete/', package_delete, name='package_delete'),
    path('trip/rate/<int:trip_id>/', rate_trip, name='rate_trip'),  # Rate trip
]


# Add this for media file handling
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)