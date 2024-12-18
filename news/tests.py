from django.test import TestCase, Client
from django.urls import reverse
from django.utils.timezone import now
from .models import TravelNews
from .tasks import scrape_travel_news
from unittest.mock import patch, Mock 
from rest_framework.test import APIClient

class TravelNewsModelTests(TestCase):
    def setUp(self):
        # Create sample TravelNews objects for testing
        self.news1 = TravelNews.objects.create(
            title="Test News 1",
            link="https://example.com/news1",
            content="This is a test news article.",
            published_date=now().date(),
            image_url="https://example.com/image1.jpg",
            category="Travel",
            read_time=5,
        )
        self.news2 = TravelNews.objects.create(
            title="Test News 2",
            link="https://example.com/news2",
            content="Another test news article.",
            published_date=None,  
            image_url="https://example.com/image2.jpg",
            category="Business",
            read_time=3,
        )

    def test_travel_news_creation(self):
        self.assertEqual(TravelNews.objects.count(), 2)
        self.assertEqual(self.news1.title, "Test News 1")
        self.assertEqual(self.news2.category, "Business")

    def test_travel_news_str(self):
        self.assertEqual(str(self.news1), "Test News 1")

class TravelNewsViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.news1 = TravelNews.objects.create(
            title="Test News 1",
            link="https://example.com/news1",
            content="This is a test news article.",
            published_date=now().date(),
            image_url="https://example.com/image1.jpg",
            category="Travel",
            read_time=5,
        )

    def test_index_view(self):
        response = self.client.get(reverse('travel_news_list'))  
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test News 1")

    def test_travel_news_list_view(self):
        response = self.client.get(reverse('news-list')) 
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test News 1")

    def test_display_travel_news_view(self):
        response = self.client.get(reverse('travel_news_list'))  
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test News 1")  

class TravelNewsTaskTests(TestCase):
    @patch('news.tasks.scrape_travel_news.delay')
    def test_scrape_travel_news_task_called(self, mock_scrape_travel_news_delay):
        mock_task = Mock()
        mock_task.id = 1234  
        mock_scrape_travel_news_delay.return_value = mock_task  

        response = self.client.get(reverse('travel_news_list'))
        self.assertEqual(response.status_code, 200)
        mock_scrape_travel_news_delay.assert_called_once() 
