def extract_params(url):
    url_parts = url.split('?', 1)
    if len(url_parts) == 1:
        return url, None
    return url_parts
