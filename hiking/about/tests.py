from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_page_accessible_by_name_and_use_correct_templates(self):
        """
        URL called by url-name is available and uses correct template.
        """
        url_names_templates = {
            'about:author': 'about/author.html',
            'about:outfit': 'about/outfit.html',
            'about:navigation': 'about/navigation.html',
        }
        for url_name, template in url_names_templates.items():
            with self.subTest(url_name=url_name):
                response = self.guest_client.get(reverse(url_name))
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertTemplateUsed(response, template)
