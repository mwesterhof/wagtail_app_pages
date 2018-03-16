import unittest

from django.test import Client
from wagtail.core.models import Page


class TestWagtail_app_pages(unittest.TestCase):
    """Tests for `wagtail_app_pages` package."""

    def setUp(self):
        self.client = Client()
        self.home = Page.objects.get(slug='home').specific

    def test_reverse(self):
        """test the reverse() method on the app page"""
        self.assertEqual(self.home.reverse('testview-a'), '/test-a/')
        self.assertEqual(self.home.reverse('testview-b'), '/test-b/')

    def test_serve(self):
        """test if views are served correctly"""
        url = self.home.reverse('testview-a')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['parent'], self.home)
