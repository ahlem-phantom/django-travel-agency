from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import TravelPackage, Booking
from .tasks import send_confirmation_email, generate_pdf_invoice, package_recommendations
from .utils import validate_booking, calculate_total_price
from unittest.mock import patch
from datetime import datetime
from decimal import Decimal
import io

class TravelPackageTests(TestCase):
    
    def setUp(self):
        """
        Set up initial data for tests.
        """
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.package = TravelPackage.objects.create(
            name='Beach Holiday',
            description='A relaxing beach getaway.',
            price=500.00,
            rating=4.5,
            package_type='Beach',
            destination='Europe'
        )
        self.client.login(username='testuser', password='password')

    def test_travel_package_list_view(self):
        """
        Test that the travel packages list view works correctly.
        """
        response = self.client.get(reverse('travel_packages_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Beach Holiday')

    def test_booking_view(self):
        """
        Test that the booking view renders correctly.
        """
        response = self.client.get(reverse('booking_handler_view', args=[self.package.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Beach Holiday')

    def test_booking_handler_view_post(self):
        """
        Test booking creation via POST request.
        """
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'datetime': '2024-12-25',
            'SelectPerson': 2,
            'SelectKids': 1,
            'SelectGender': 'Male',
            'payment_method': 'Online',
            'consent': 'on'
        }
        response = self.client.post(reverse('booking_handler_view', args=[self.package.id]), data)
        self.assertRedirects(response, reverse('booking_success'))

    def test_booking_success_view(self):
        """
        Test booking success view.
        """
        response = self.client.get(reverse('booking_success'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Booking Successful')

    def test_booking_fail_view(self):
        """
        Test booking fail view.
        """
        response = self.client.get(reverse('booking_fail'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Booking Failed')

    def test_package_recommendations_view(self):
        """
        Test package recommendations view.
        """
        response = self.client.get(reverse('packages_recommendations'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Beach Holiday')





class UtilsTests(TestCase):

    def test_validate_booking(self):
        """
        Test booking form validation.
        """
        valid_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'booking_date': '2024-12-25',
            'num_adults': 2,
            'num_children': 1,
            'payment_method': 'Online',
            'consent': 'on'
        }
        errors = validate_booking(**valid_data)
        self.assertEqual(errors, {})

        invalid_data = valid_data.copy()
        invalid_data['name'] = 'J'  # Too short name
        errors = validate_booking(**invalid_data)
        self.assertEqual(errors['name'], 'Name must only contain letters and be at least 2 characters.')

    def test_calculate_total_price(self):
        """
        Test price calculation with discounts.
        """
        package = TravelPackage.objects.create(
            name='Beach Holiday',
            price=500.00,
            rating=4.5,
            package_type='Beach',
            destination='Europe'
        )
        total_price = calculate_total_price(package, 2, 1, Decimal('0.5'))
        self.assertEqual(total_price, Decimal('1500.00'))




class CeleryTaskTests(TestCase):

    @patch('django.core.mail.send_mail')
    def test_send_confirmation_email(self, mock_send_mail):
        """
        Test sending of confirmation email.
        """
        send_confirmation_email('John Doe', 'john@example.com', 'Beach Holiday', 500.00)
        self.assertTrue(mock_send_mail.called)
        self.assertEqual(mock_send_mail.call_count, 1)

    @patch('weasyprint.HTML.write_pdf')
    def test_generate_pdf_invoice(self, mock_write_pdf):
        """
        Test generating a PDF invoice.
        """
        booking = Booking.objects.create(
            package=self.package,
            name='John Doe',
            email='john@example.com',
            datetime=datetime(2024, 12, 25),
            num_adults=2,
            num_children=1,
            total_price=500.00,
            gender='Male',
            payment_status='Paid',
            payment_method='Online'
        )
        mock_write_pdf.return_value = b'%PDF-1.4'
        result = generate_pdf_invoice(booking.id)
        self.assertTrue(result.endswith('.pdf'))

    @patch('celery.result.AsyncResult.get')
    def test_package_recommendations_task(self, mock_get):
        """
        Test the package recommendations task.
        """
        mock_get.return_value = [self.package.id]
        recommended_package_ids = package_recommendations(self.user.id)
        self.assertEqual(recommended_package_ids, [self.package.id])