=====
Usage
=====


To use Wagtail App Pages in your project, simply add it to your INSTALLED_APPS:


.. code-block:: python

    INSTALLED_APPS = [
        # ...
        'wagtail_app_pages',
        # ...
    ]

use the provided context processor:

.. code-block:: python

    TEMPLATES = [
        {
            # ...
            'OPTIONS': {
                'context_processors': [
                    # ...
                    'wagtail_app_pages.context_processors.parent_page',
                    # ...
                ],
            },
        },
    ]

and use the provided mixin in your page model(s):

.. code-block:: python

    # myapppage/models.py
    from wagtail.core.models import Page
    from wagtail_app_pages.models import AppPageMixin


    class MyAppPage(AppPageMixin, Page):
        url_config = 'myapppage.urls'

When using this mixin, the url_config attribute becomes a requirement. It should provide a dot-separated path to a
valid django url config module:

.. code-block:: python

    # myapppage/urls.py

    from django.urls import path

    from .views import ViewA, ViewB


    urlpatterns = [
        path('A/', ViewA.as_view(), name='view_a'),
        path('B/', ViewB.as_view(), name='view_b'),
    ]
