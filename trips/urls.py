from django.urls import path
from .views import RecommendationView

urlpatterns = [
    path('recommendations/', RecommendationView.as_view(), name='recommendations'),
]
