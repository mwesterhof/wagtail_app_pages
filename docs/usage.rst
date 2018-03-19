=====
Usage
=====


To use Wagtail App Pages in your project, simply add it to your INSTALLED_APPS:


.. code-block:: python

    INSTALLED_APPS = [
        ...
        'wagtail_app_pages',
        ...
    ]

and use the provided mixin in your page model(s):

.. code-block:: python

    # file: blog/models.py
    from wagtail.core.models import Page
    from wagtail_app_pages.models import AppPageMixin


    class BlogPage(AppPageMixin, Page):
        url_config = 'blog.urls'

When using this mixin, the url_config attribute becomes a requirement. It should provide a dot-separated path to a
valid django url config module:

.. code-block:: python

    # file: blog/urls.py
    from django.urls import path

    from .views import A


    urlpatterns = [
        path('testview/', TestView.as_view(), name='testview')
    ]

.. code-block:: python

    # file: blog/views.py
    from django.views.generic import TemplateView


    class TestView(TemplateView):
        template_name = 'blog/test.html'
