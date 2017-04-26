
from .text import generate_fingerprint, tokenize, remove_punctuation


def test_punctuation():
    assert 'abc' == remove_punctuation('a,b.c!')
