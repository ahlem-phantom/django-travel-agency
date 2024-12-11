from celery import shared_task
import requests
from bs4 import BeautifulSoup
from .models import NewsArticle

@shared_task
def scrape_news():
    url = "https://example.com/news"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Assuming the news is in <article> tags
    articles = soup.find_all('article')

    for article in articles:
        title = article.find('h2').get_text()
        content = article.find('p').get_text()

        # Save the scraped news in the database
        NewsArticle.objects.create(title=title, content=content, published_on=timezone.now())
