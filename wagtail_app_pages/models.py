from django.urls.exceptions import Resolver404

from wagtail_app_pages.compatibility import get_resolver, RouteResult


class AppPageMixin:
    @property
    def url_config(self):
        raise NotImplementedError('url_config')

    @property
    def is_preview_instance(self):
        served_through_preview = getattr(self, '_served_through_preview', False)
        return served_through_preview

    @staticmethod
    def _get_url_components(url):
        url_parts = url.split('?', 1)
        if len(url_parts) == 1:
            return url, None
        return url_parts

    def reverse(self, name, *args, **kwargs):
        sub_url = self._apppage_url_resolver.reverse(name, *args, **kwargs)
        url = self.url + sub_url.lstrip('/')
        url, query_string = self._get_url_components(url)

        if self.is_preview_instance:
            if query_string:
                query_string += '&preview'
            else:
                query_string = 'preview'

        if query_string:
            return '?'.join([url, query_string])
        return url

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

        page_instance = self
        if request.GET.get('preview') is not None:
            page_instance = page_instance.get_latest_revision_as_page()

        request.parent_page = page_instance

        # if this is a class-based view, we'll make the parent page available as an attribute as well
        if getattr(view, 'view_class', None):
            view.view_class.parent_page = page_instance

        return view(request, *args, **kwargs)

    def serve_preview(self, request, mode_name):
        self._served_through_preview = True
        result = self.route(request, [])
        return self.serve(request, *result.args)
