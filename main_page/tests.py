from django.test import TestCase
from django.urls import reverse

# Create your tests here.

class MainPageTestCase(TestCase):

    def test_main_page_available(self):
        """Main page is available, code 200"""

        response = self.client.get(reverse('main_page:index_main'))
        self.assertEqual(response.status_code, 200)

    def test_about_available(self):
        """About page is available, code 200"""

        response = self.client.get(reverse('main_page:about'))
        self.assertEqual(response.status_code, 200)