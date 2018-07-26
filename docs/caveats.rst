Caveats
=======

There are things to be considered when using this library.

Root URL or page template?
--------------------------

A page that uses the AppPageMixin, can route to different views using a supplied url config. In the case of the root
URL of the page (in other words, the actual page url), 2 different scenarios are possible:

1) if there's a root URL in the pages' url config, it will be used as expected
2) if no root URL is specified for the page, it will be served as any other wagtail page

This means that it's up to the developer who uses this library to decide which is more appropriate for his case.

Lack of determinism
-------------------

When using the regular django MTV (Model, Template, View) architecture, the act of calling *reverse()* or using the *{%
url %}* template tag is relatively straight forward. We always target a view in a way that should yield (no more than)
one url. This will always work, no matter the context.

Since this library introduces a different way to integrate urls and views, it won't always be quite that simple.
Consider the following:

.. code-block:: python

    # file blog/models.py
    from django.db import models
    from wagtail.core.models import Page
    from wagtail_app_pages.models import AppPageMixin


    class Article(models.Model):
        slug = models.SlugField()
        title = models.CharField(max_length=200)


    class BlogPage(AppPageMixin, Page):
        url_config = 'blog.urls'


.. code-block:: python

    # file blog/urls.py
    from django.urls import path

    from blog.views import ArticleDetail, ArticleList


    urlpatterns = [
        path('articles/', ArticleList.as_view(), name='article_list'),
        path('articles/<slug:slug>/', ArticleDetail.as_view(), name='article_detail'),
    ]


.. code-block:: python

    # file blog/views.py
    from django.views.generic import DetailView, ListView

    from .models import Article


    class ArticleList(ListView):
        model = Article


    class ArticleDetail(DetailView):
        model = Article


.. code-block:: html

    <!-- file blog/article_list.html -->
    {% load app_page_tags %}
    <ul>
        {% for article in article_list %}
        <li>
            <a href="{% app_page_url "article_detail" slug=article.slug ">{{ article.title }}</a>
        </li>
        {% endfor %}
    </ul>


This example will attach 2 views to a page, an *article list view* and an *article detail view*. The list view will
render links to the detail view for the respective rendered article. The url lookup will happen within the same app
page, and will work as desired. Any view served through wagtail_app_pages will have access to the *parent_page* object,
available in the context.

If the view is served from outside of the app, the *{% app_page_url %}* won't be able to resolve the url lookup. This
is a direct consequence of extending pages with urls, although there are different ways to deal with it.


* *Can we assume that only one blogpage ever exists?* In that case, a very simple custom templatetag could resolve it:

.. code-block:: python

    # file templatetags/blog_tags.py
    @register.simple_tag
    def blog_page_url(name, *args, **kwargs):
        blog_page = BlogPage.objects.live().first()
        return blog_page.reverse(name, *args, **kwargs)

* *Multiple blogpages exist, but one per site* In this case, one could create a site setting to specify the main blog
  page for that site. Any code that has access to the request object, could use this to perform a
  *request.site.blog_page.reverse* Even if there are multiple versions of the blog page for the site, this could be
  used to find the "default one".
* *Multiple blogpages exist, and we want to use a specific one* If we want all url lookups from a certain page to
  always use a specific blogpage instance, we could simply link these together in the content. For instance, we could
  write a ProductsPage to serve all the views of a product catalogue. We could have 2 versions of this products page,
  one *main* one, that shows all the products, and is set to show up in the menu. Aside from this, we'd have a
  *promotion* version, configured to only show products with a promotional state. We'll want the main version to be
  used by default, and the promotional one when linking from the blogpage. This could simply be achieved by adding a
  parentalkey to the blogpage model, and explicitly linking the pages together.
