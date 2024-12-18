from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from .models import TravelPackage, Booking
from unittest.mock import patch


class TravelPackageViewsTest(TestCase):

    def setUp(self):
        """
        Create test data for TravelPackage, User, and Booking.
        """
        self.package = TravelPackage.objects.create(
            name="Beach Holiday",
            destination="Maldives",
            package_type="Beach",
            price=Decimal('500.00'),
            duration="7 days",
            rating=4.5,
            description="A relaxing beach holiday.",
            available=True
        )

        self.user = User.objects.create_user(
            username='testuser', password='password123', email='testuser@example.com'
        )



   
