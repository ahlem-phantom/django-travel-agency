from celery import shared_task
import requests
from bs4 import BeautifulSoup
from .models import NewsArticle
from .scraper import scrape_travel_news
from django.http import JsonResponse

@shared_task
def scrape_travel_news_task(request):
    scrape_travel_news().apply_async()
    return JsonResponse({"status": "Scraping task has been triggered!"})
