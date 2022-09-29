from django.shortcuts import get_object_or_404
from django.urls.exceptions import Resolver404

from wagtail_app_pages.compatibility import get_resolver, Revision, RouteResult
from wagtail_app_pages.utils import extract_params


class AppPageMixin:
    @property
    def url_config(self):
        raise NotImplementedError('url_config')

    @classmethod
    def from_json(cls, json_data):
        # legacy
        revision = Revision.objects.filter(content_json=json_data).first()
        obj = super().from_json(json_data)
        obj._loaded_from_revision = revision.pk
        return obj

    def with_content_json(self, content):
        # we're overriding this method to intercept the revision data
        revision = Revision.objects.filter(content=content).first()
        page = super().with_content_json(content)
        page._loaded_from_revision = revision.pk
        return page

    def reverse(self, name, *args, **kwargs):
        sub_url = self._apppage_url_resolver.reverse(name, *args, **kwargs)
        url = self.url + sub_url.lstrip('/')
        url, query_string = extract_params(url)

        revision_id = getattr(self, '_loaded_from_revision', None)
        if revision_id:
            revision_query = 'apppage_revision={}'.format(revision_id)

            if query_string:
                query_string += '&' + revision_query
            else:
                query_string = revision_query

        if query_string:
            return '?'.join([url, query_string])
        return url

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        url_parts = self.get_url_parts()
        if url_parts:
            _, _, relative_url = url_parts
        else:
            relative_url = self.url

        self._apppage_url_resolver = get_resolver(relative_url, self.url_config)

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
        revision_id = request.GET.get('apppage_revision')
        if revision_id is not None:
            revision = get_object_or_404(self.revisions, id=revision_id)
            page_instance = revision.as_page_object()
            self._loaded_from_revision = revision_id

        request.parent_page = page_instance

        # if this is a class-based view, we'll make the parent page available as an attribute as well
        if getattr(view, 'view_class', None):
            view.view_class.parent_page = page_instance

        return view(request, *args, **kwargs)

    def serve_preview(self, request, mode_name):
        result = self.route(request, [])
        return self.serve(request, *result.args)
