"""Test the query string templatetag."""

from ..templatetags.querystring import query_transform


def test_no_querystring(rf):
    """No querystring should return nothing."""
    request = rf.get('/')
    kwargs = {}

    result = query_transform(request, **kwargs)
    assert len(result) == 0


def test_one_argument_querystring(rf):
    """One argument querystring should return that."""
    request = rf.get('/')
    kwargs = {'steve': 'jobs'}

    result = query_transform(request, **kwargs)
    assert result == 'steve=jobs'


def test_multi_argument_querystring(rf):
    """Multi argument querystring should have & and =."""
    request = rf.get('/')
    kwargs = {'steve': 'jobs', 'bill': 'gates'}

    result = query_transform(request, **kwargs)
    assert result.count('?') == 0
    assert result.count('&') == 1
    assert result.count('=') == 2


def test_multi_argument_querystring_with_special_characters(rf):
    """Multi argument querystring should have the right numbers of & and =."""
    request = rf.get('/')
    kwargs = {'ste=ve': 'jo?bs', 'bi&ll': 'gat=es'}

    result = query_transform(request, **kwargs)
    assert result.count('?') == 0
    assert result.count('&') == 1
    assert result.count('=') == 2
