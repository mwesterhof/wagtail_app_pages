========
Examples
========


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

.. code-block:: python

    # file: blog/urls.py
    from django.urls import path

    from .views import ArticleDetail, ArticleList


    urlpatterns = [
        path('articles/', ArticleList.as_view(), name='article_list'),
        path('articles/<slug:slug>/', ArticleDetail.as_view(), name='article_detail'),
        path('article/new/', ArticleCreate.as_view(), name='article_create'),
    ]

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



.. code-block:: htmldjango

    {% load app_pages_tags %}
    <ul>
        {% for article in article_list %}
        <li>
            <a href="{% page_url 'article_detail' slug=article.slug %}">{{ article }}</a>
        </li>
        {% endfor %}
    </ul>
