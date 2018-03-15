=============
Configuration
=============


To use Wagtail App Pages in your project, simply add it to your INSTALLED_APPS:


.. code-block:: python

    INSTALLED_APPS = [
        ...
        'wagtail_app_pages',
        ...
    ]

 and use the provided mixin in your page model(s):
.. code-block:: python

    from wagtail.core.models import Page
    from wagtail_app_pages.models import AppPageMixin


    class BlogPage(AppPageMixin, Page):
        url_config = 'blog.urls'
