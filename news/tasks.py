import logging
import requests
from bs4 import BeautifulSoup
from .models import TravelNews
from celery import shared_task
from urllib.parse import urljoin
from datetime import datetime
from time import sleep

# Set up logging
logger = logging.getLogger(__name__)
BASE_URL = "https://www.lonelyplanet.com/news"
MAX_PAGES = 2


def convert_date(date_str):
    try:
        # Convert date from "Aug 9, 2024" to "2024-08-09"
        return datetime.strptime(date_str, "%b %d, %Y").date()
    except ValueError:
        return None

@shared_task
def scrape_travel_news():
    """
    Scrape travel news articles from the Lonely Planet website and save them to the database.

    This task retrieves articles from multiple pages, extracts relevant information 
    (title, date, link, image URL, content, category, and read time), and saves them 
    to the TravelNews model. Duplicate articles are skipped.

    Workflow:
        1. Fetch each page using HTTP GET requests.
        2. Parse the HTML content using BeautifulSoup.
        3. Extract relevant fields from each article.
        4. Check if the article already exists in the database.
        5. Save new articles to the database.

    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
        ValueError: If the date format cannot be parsed.

    Returns:
        list: A list of successfully saved articles (optional for debugging purposes).
    """
    page_number = 1
    travel_news = []

    while page_number <= MAX_PAGES:
        url = f"{BASE_URL}?page={page_number}"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to retrieve page {page_number}: {e}")
            break

        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('article')

        if not articles:
            logger.info(f"No more articles found on page {page_number}, stopping.")
            break

        for article in articles:
            title_tag = article.find('a', class_='card-link')
            title = title_tag.text.strip() if title_tag else "Unknown Title"
            link = title_tag['href'] if title_tag and 'href' in title_tag.attrs else None

            date_tag = article.find('p', class_='text-sm')
            if date_tag:
                date_and_time = date_tag.text.strip().split('•')
                date_str = date_and_time[0].strip() if len(date_and_time) > 0 else None
                read_time = int(date_and_time[1].split()[0]) if len(date_and_time) > 1 else None
            else:
                date_str = read_time = None

            try:
                date = convert_date(date_str) if date_str else None
            except ValueError as e:
                logger.error(f"Date conversion failed for {date_str}: {e}")
                date = None

            content = article.find('p', class_='line-clamp-2').text.strip() if article.find('p', class_='line-clamp-2') else None
            category = article.find('div', class_='text-sm uppercase font-semibold tracking-wide relative z-10 mb-2 w-90 text-black-400 block').text.strip() if article.find('div', class_='text-sm uppercase font-semibold tracking-wide relative z-10 mb-2 w-90 text-black-400 block') else None
            image_tag = article.find('img')
            image_url = image_tag['src'] if image_tag else None

            # Save or skip if article exists
            travel_news_item, created = TravelNews.objects.get_or_create(
                link=link,
                defaults={
                    'title': title,
                    'published_date': date,
                    'image_url': image_url,
                    'content': content,
                    'category': category,
                    'read_time': read_time,
                }
            )
            if created:
                logger.info(f"New article added: {title}")

        page_number += 1
        sleep(2) 