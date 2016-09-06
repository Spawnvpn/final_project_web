import unittest
from django.urls import reverse
from django.test.client import RequestFactory, Client
import views


class IndexTestCase(unittest.TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()

    def test_get_index(self):
        url = reverse(views.index)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_process_view(self):
        url = reverse(views.process_view)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_search_view(self):
        url = reverse(views.search_view) + '?keywords=cat'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        url = reverse(views.search_view)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_image_list_view(self):
        url = reverse('image_list')
        response = self.client.get(url)

        self.assertEqual(str(response.context['images_list']), '<QuerySet []>')


if __name__ == '__main__':
    unittest.main()
