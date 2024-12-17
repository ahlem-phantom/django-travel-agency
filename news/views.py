from django.http import HttpResponse
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import TravelNews
from .serializers import TravelNewsSerializer
from .scraper import scrape_travel_news  # Import your scraping function
from django.http import JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from urllib.parse import urlparse, urlunparse, urlencode

# Function-based view for the home/index route
def index(request):
    return HttpResponse("Welcome to the News app!")

# API View for listing TravelNews with filtering, searching, and ordering
class TravelNewsListView(ListAPIView):
    queryset = TravelNews.objects.all().order_by('-published_date')
    serializer_class = TravelNewsSerializer

    # Add filtering, searching, and ordering functionality
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['published_date']  # Filter by published_date
    search_fields = ['title', 'content']  # Search by title or content
    ordering_fields = ['published_date', 'title']  # Allow ordering by date or title

def trigger_scraping(request):
    # Trigger the scraping task to run asynchronously
    scrape_travel_news.apply_async()
    return JsonResponse({"status": "Scraping task has been triggered!"})


def update_image_url(url, new_params):
    parsed_url = urlparse(url)
    # Replace the query with the new parameters
    new_query = urlencode(new_params)
    updated_url = parsed_url._replace(query=new_query)
    return urlunparse(updated_url)

def display_travel_news(request):
    #scrape_travel_news()  # hereeee
     # Get all articles
    articles = TravelNews.objects.all().order_by('-published_date')
    for article in articles:
        article.image_url = update_image_url(article.image_url, {'w': 500, 'h':'400', 'fit': 'crop', 'q': 75})
    # Set up pagination
    paginator = Paginator(articles, 6)  # Show 5 articles per page
    page_number = request.GET.get('page')  # Get the page number from the URL
    page_obj = paginator.get_page(page_number)  # Get the correct page of articles

    # Render the page with articles
    return render(request, 'travel_news_list.html', {'page_obj': page_obj})
