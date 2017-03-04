"""Update current query string.

Useful for pagination.  Eg:

<a href="?{% querystring request page=page_obj.next_page_number %}">Link</a>

If the query string is already "?search=something&page=2" then the next page
should be "?search=something&page=3" (including the search term).

"""

from django import template

register = template.Library()


@register.simple_tag(name='querystring')
def query_transform(request, **kwargs):
    """Alter parameters in a query string while keeping the rest."""
    updated = request.GET.copy()
    for field, value in kwargs.items():
        updated[field] = value

    return updated.urlencode()
