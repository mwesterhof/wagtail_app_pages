from django.template import Library


register = Library()


@register.simple_tag(takes_context=True)
def app_page_url(context, name, *args, **kwargs):
    app_page = kwargs.pop('app_page', None)
    if not app_page:
        try:
            app_page = context['request'].parent_page
        except AttributeError:
            app_page = context['page']

    return app_page.reverse(name, *args, **kwargs)
