"""Test the within_page_range function."""

from ..templatetags.within_page_range import within_filter


def test_in_range_above():
    """One page above current should be displayed."""
    test_page = 5
    current_page = 4

    result = within_filter(test_page, current_page)
    assert result


def test_in_range_below():
    """One page below current should be displayed."""
    test_page = 3
    current_page = 4

    result = within_filter(test_page, current_page)
    assert result


def test_out_of_range_above():
    """20 pages above current should not be displayed."""
    test_page = 74
    current_page = 54

    result = within_filter(test_page, current_page)
    assert not result


def test_out_of_range_below():
    """20 pages below current should not be displayed."""
    test_page = 34
    current_page = 54

    result = within_filter(test_page, current_page)
    assert not result
