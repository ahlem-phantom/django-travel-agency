import logging
import requests
from bs4 import BeautifulSoup
from .models import TravelNews
from celery import shared_task
from urllib.parse import urljoin
from datetime import datetime

# Set up logging
logger = logging.getLogger(__name__)
BASE_URL = "https://www.lonelyplanet.com/news"
MAX_PAGES = 2
# Function to convert the date into the proper format (YYYY-MM-DD)
def convert_date(date_str):
    try:
        # Convert date from "Aug 9, 2024" to "2024-08-09"
        return datetime.strptime(date_str, "%b %d, %Y").date()
    except ValueError:
        return None

@shared_task
def scrape_travel_news():
    page_number = 1
    while page_number <= MAX_PAGES:
        url = f"{BASE_URL}?page={page_number}"
        response = requests.get(url)
        
        # If the page doesn't exist or no content is returned, break out of the loop
        if response.status_code != 200:
            print(f"Failed to retrieve page {page_number}, stopping.")
            break
        soup = BeautifulSoup(response.content, 'html.parser')

        articles = soup.find_all('article')
        
        travel_news = []

        for article in articles:
            title_tag = article.find('a', class_='card-link')
            title = title_tag.text.strip() if title_tag else None
            
            # Extract the publication date and read time from the paragraph
            date_tag = article.find('p', class_='text-sm')
            if date_tag:
                date_and_time = date_tag.text.strip().split('•')
                date_str = date_and_time[0].strip() if len(date_and_time) > 0 else None
                read_time = date_and_time[1].strip() if len(date_and_time) > 1 else None
                read_time = int(read_time.split()[0]) if read_time else None
            else:
                date_str = read_time = None

            # Convert the date to YYYY-MM-DD format
            date = convert_date(date_str) if date_str else None

            link = title_tag['href'] if title_tag else None
            content = article.find('p', class_='line-clamp-2').text.strip() if article.find('p', class_='line-clamp-2') else None
            category = article.find('div', class_='text-sm uppercase font-semibold tracking-wide relative z-10 mb-2 w-90 text-black-400 block').text.strip() if article.find('div', class_='text-sm uppercase font-semibold tracking-wide relative z-10 mb-2 w-90 text-black-400 block') else None
            image_tag = article.find('img')
            image_url = image_tag['src'] if image_tag else None

            # Append data as a dictionary
            travel_news.append({
                'title': title,
                'date': date,
                'link': link,
                'image_url': image_url
            })
            
            # Check if article already exists in the database
            if TravelNews.objects.filter(title=title, link=link).exists():
                continue
            else:
                # Save each article to the database
                TravelNews.objects.create(
                    title=title,
                    published_date=date,  
                    link=link,
                    image_url=image_url,
                    content=content,
                    category=category,
                    read_time=read_time,
                )
            
        # Move to the next page
        page_number += 1
        
    else:
        logger.error("Failed to retrieve the webpage.")
        return []
















'''
import logging
import requests
from bs4 import BeautifulSoup
from .models import TravelNews
from celery import shared_task
from urllib.parse import urljoin
from datetime import datetime

# Set up logging
logger = logging.getLogger(__name__)

# Function to convert the date into the proper format (YYYY-MM-DD)
def convert_date(date_str):
    try:
        # Convert date from "Aug 9, 2024" to "2024-08-09"
        return datetime.strptime(date_str, "%b %d, %Y").date()
    except ValueError:
        return None

BASE_URL = "https://www.lonelyplanet.com/news"
MAX_PAGES = 2

@shared_task
def scrape_travel_news():
    page_number = 1
    while page_number <= MAX_PAGES:
        url = f"{BASE_URL}?page={page_number}"
        response = requests.get(url)
        
        # If the page doesn't exist or no content is returned, break out of the loop
        if response.status_code != 200:
            print(f"Failed to retrieve page {page_number}, stopping.")
            break
        
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('article')  # Adjust based on how articles are marked in HTML
        
        # If there are no articles on this page, stop scraping
        if not articles:
            print(f"No more articles found on page {page_number}, stopping.")
            break
        
        for article in articles:
            title_tag = article.find('a', class_='card-link')
            title = title_tag.text.strip() if title_tag else None
            link = title_tag['href'] if title_tag else None
            content_tag = article.find('div', class_='card-description')  # Adjust if necessary
            content = content_tag.text.strip() if content_tag else ""
            
            # Extract the date and convert it
            date_tag = article.find('p', class_='text-sm')  # Adjust based on the site's structure
            if date_tag:
                date_str = date_tag.text.strip().split('•')[0].strip()  # Example: 'Mar 26, 2024'
                try:
                    published_date = datetime.strptime(date_str, "%b %d, %Y").date()
                except ValueError:
                    published_date = None
            else:
                published_date = None
            
            # Extract image URL and category
            image_tag = article.find('img')
            image_url = image_tag['src'] if image_tag else None
            category_tag = article.find('span', class_='category')  # Adjust as needed
            category = category_tag.text.strip() if category_tag else None
            
            # Extract read time (if available)
            read_time_tag = article.find('span', class_='read-time')
            read_time = int(read_time_tag.text.strip()) if read_time_tag else None
            
            # if article is already in the database, skip it
            if TravelNews.objects.filter(title=title, link=link).exists():
                continue

            # Save data to the database
            TravelNews.objects.create(
                title=title,
                link=link,
                content=content,
                published_date=published_date,
                image_url=image_url,
                category=category,
                read_time=read_time
            )
        
        # Move to the next page
        page_number += 1
   

        print(f"Scraped page {page_number - 1}")

'''