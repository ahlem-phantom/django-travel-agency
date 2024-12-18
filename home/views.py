from django.http import HttpResponse
from django.shortcuts import render
from news.models import TravelNews
from packages.models import TravelPackage
from news.views import update_image_url

def index(request):
    """
    Renders the homepage with the latest travel news articles, available travel packages, and a star rating range.

    This view fetches the latest three articles from the `TravelNews` model, updates their image URLs with specified dimensions 
    and quality, and renders them on the homepage. Additionally, it retrieves all available travel packages and prepares a 
    rating range for displaying star ratings.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered homepage template (`index.html`) with context data.
    """
    page_obj = TravelNews.objects.all()[:3]
    for article in page_obj:
        article.image_url = update_image_url(article.image_url, {'w': 500, 'h':'400', 'fit': 'crop', 'q': 75})

    travel_packages =  TravelPackage.objects.all()
    ratings_range = range(1, 6)  # Range for star rating
    return render(request, 'index.html', {'page_obj': page_obj, 'packages': travel_packages, 'ratings_range': ratings_range})  # Path to your template


def not_found(request, exception=None):
    """
    Renders a 404 error page when a requested resource is not found.

    This view handles the case when a user tries to access a non-existent page and provides a custom 404 error page.

    Args:
        request (HttpRequest): The HTTP request object.
        exception (Exception, optional): The exception raised during the 404 error. Default is None.

    Returns:
        HttpResponse: The rendered 404 error page (`404.html`) with a status code of 404.
    """
    return render(request, '404.html', status=404)

