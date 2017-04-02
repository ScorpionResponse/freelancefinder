"""Test the markdown filter."""

from ..templatetags.markdown_filter import markdown_filter


def test_markdown_rendered():
    """Test basic markdown is rendered."""
    source = '**bold**'
    expected = '<p><strong>bold</strong></p>'

    result = markdown_filter(source)
    assert result == expected


def test_html_passed_through():
    """Test basic html is rendered the same."""
    source = '<strong>bold</strong>'
    expected = '<p><strong>bold</strong></p>'

    result = markdown_filter(source)
    assert result == expected


def test_html_stripped():
    """Test certain html is stripped."""
    source = '<blink>not blinking</blink>'
    expected = '<p>not blinking</p>'

    result = markdown_filter(source)
    assert result == expected


def test_additional_html_passed_through():
    """Test additional html tags are rendered the same."""
    source = '<pre>bold</pre>'
    expected = '<pre>bold</pre>'

    result = markdown_filter(source)
    assert result == expected
