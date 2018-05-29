from django.urls.exceptions import Resolver404

from wagtail_app_pages.compatibility import get_resolver, RouteResult


class AppPageMixin:
    @property
    def url_config(self):
        raise NotImplementedError('url_config')

    def reverse(self, name, *args, **kwargs):
        sub_url = self._apppage_url_resolver.reverse(name, *args, **kwargs)
        return self.url + sub_url.lstrip('/')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apppage_url_resolver = get_resolver(self.url, self.url_config)

    def route(self, request, path_components):
        # url config takes precedence over normal wagtail routing
        try:
            view, args, kwargs = self._apppage_url_resolver.resolve(request.path)
        except Resolver404:
            return super().route(request, path_components)
        else:
            return RouteResult(self, args=(view, args, kwargs))

    def serve(self, request, view=None, args=None, kwargs=None):
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        if view is None:
            return super().serve(request, *args, **kwargs)

        request.parent_page = self
        # if this is a class-based view, we'll make the parent page available as an attribute as well
        if getattr(view, 'view_class', None):
            view.view_class.parent_page = self

        return view(request, *args, **kwargs)
