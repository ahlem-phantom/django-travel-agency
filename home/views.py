# home/views.py
from django.http import HttpResponse
from django.shortcuts import render
from news.models import TravelNews
from packages.models import TravelPackage
from news.views import update_image_url

def index(request):
    page_obj = TravelNews.objects.all()[:3]
    for article in page_obj:
        article.image_url = update_image_url(article.image_url, {'w': 500, 'h':'400', 'fit': 'crop', 'q': 75})

    travel_packages =  TravelPackage.objects.all()
    ratings_range = range(1, 6)  # Range for star rating
    return render(request, 'index.html', {'page_obj': page_obj, 'packages': travel_packages, 'ratings_range': ratings_range})  # Path to your template


def not_found(request, exception=None):
    return render(request, '404.html', status=404)

