# flake8: noqa
try:
    from django.urls import URLResolver

except ImportError:
    from django.urls.resolvers import RegexURLResolver

    def get_resolver(url, url_config):
        return RegexURLResolver(r'^{}'.format(url), url_config)

else:
    from django.urls.resolvers import RegexPattern

    def get_resolver(url, url_config):
        return URLResolver(RegexPattern(r'^{}'.format(url)), url_config)

try:
    from wagtail.core.url_routing import RouteResult
except ImportError:
    from wagtail.url_routing import RouteResult

try:
    from wagtail.models import PageRevision
except ImportError:
    from wagtail.models import Revision

else:
    class Revision(PageRevision):
        class Meta:
            proxy = True
            app_label = 'wagtailcore'
