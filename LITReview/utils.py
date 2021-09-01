"""
General functions that can be reused
"""


def add_url_name_to_context(request, context) -> str:
    context['url_name'] = request.resolver_match.url_name
    return context['url_name']
