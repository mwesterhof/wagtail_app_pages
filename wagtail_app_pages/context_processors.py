def parent_page(request):
    # ensure that the parent_page is always available in the context, if known
    # also make it available as 'self', so wagtail templates continue to
    # work as expected
    if hasattr(request, 'parent_page'):
        return {
            'parent_page': request.parent_page,
            'self': request.parent_page
        }

    return {}
