from django.http import HttpResponse
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import TravelNews
from .serializers import TravelNewsSerializer
from .scraper import scrape_travel_news  # Import your scraping function
from django.http import JsonResponse
from django.shortcuts import render
from .scraper import scrape_travel_news
from django.core.paginator import Paginator

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




def display_travel_news(request):
    scrape_travel_news()  # Scrape the news articles
     # Get all articles
    articles = TravelNews.objects.all().order_by('-published_date')

    # Set up pagination
    paginator = Paginator(articles, 5)  # Show 5 articles per page
    page_number = request.GET.get('page')  # Get the page number from the URL
    page_obj = paginator.get_page(page_number)  # Get the correct page of articles

    # Render the page with articles
    return render(request, 'travel_news_list.html', {'page_obj': page_obj})
