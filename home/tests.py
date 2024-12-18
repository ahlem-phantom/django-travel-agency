from django.test import TestCase


class ViewsTestCase(TestCase):

    def test_index_view(self):
        # Your test for the index view
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Additional assertions here

    def test_not_found(self):
        # Test if the image URLs are being updated correctly
        response = self.client.get('65656')
        # Check if the image URL update function is called or test it directly
        self.assertEqual(response.status_code, 404)