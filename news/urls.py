from django.urls import path
from .views import index, TravelNewsListView
from .views import trigger_scraping, display_travel_news

urlpatterns = [
    path('', display_travel_news, name='templates/travel_news_list'),
    path('api', TravelNewsListView.as_view(), name='news-list'),  # API for listing news
    #path('trigger-scraping/', trigger_scraping, name='trigger_scraping'),

]
