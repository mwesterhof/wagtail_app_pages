from wagtail.core.models import Page
from wagtail_app_pages.models import AppPageMixin


class HomePage(AppPageMixin, Page):
    url_config = 'home.urls'
