========
Examples
========

For a more in-depth example, we'll create a wagtail page implementing a simple blog app. This example is a little
contrived, but it will demonstrate some of the more advanced functionality that can be implemented using app pages.

.. code-block:: python

    # file: blog/models.py
    from django.db import models
    from wagtail.core.models import Page
    from wagtail_app_pages.models import AppPageMixin


    class Article(models.Model):
        slug = models.SlugField()
        title = models.CharField(max_length=200)


    class BlogPage(AppPageMixin, Page):
        url_config = 'blog.urls'

To implement the blog functionality as an extension of the blog page, it references the following url config:

.. code-block:: python

    # file: blog/urls.py
    from django.urls import path

    from .views import ArticleCreate, ArticleDetail, ArticleList


    urlpatterns = [
        path('articles/', ArticleList.as_view(), name='article_list'),
        path('articles/<slug:slug>/', ArticleDetail.as_view(), name='article_detail'),
        path('article/new/', ArticleCreate.as_view(), name='article_create'),
    ]

This url config is used to add additional endpoints to the page routing. It essentially turns the blog page into a blog
*app*.

.. code-block:: python

    # file: blog/views.py
    from django.views.generic import CreateView, DetailView, ListView

    from .models import Article


    class ArticleDetail(DetailView):
        model = Article


    class ArticleList(ListView):
        model = Article


    class ArticleCreate(CreateView):
        model = Article

        def get_success_url(self):
            # on successful create, redirect to the article_list url *for the same parent page*
            # if we have more than one BlogPage, each will have its own ArticleCreate view,
            # and this redirect will always happen with respect to the parent BlogPage
            return self.parent_page.reverse('article_list')

These views mostly work the way they always do. The `ArticleCreate` view highlights one exception. Any class-based
view served through an app-page will have access to a `parent_page` attribute. This will be a reference to the app-page
that served it (the BlogPage, in this case).

The previous example also shows how to perform a reverse lookup within the scope of the page. App-pages will have a
`reverse` method that does just that.

Performing a reverse lookup from a template within the app is also easy; a template tag is provided for this. It will
find the parent page from the context, so there's no need to supply it. This means that if there's more than one
BlogPage within a project, these lookups will always return urls that stay within that app's url structure.

The following example shows how to perform these lookups from the template:

.. code-block:: htmldjango

    {% load app_pages_tags %}
    <ul>
        {% for article in article_list %}
        <li>
            <a href="{% app_page_url 'article_detail' slug=article.slug %}">{{ article }}</a>
        </li>
        {% endfor %}
    </ul>
