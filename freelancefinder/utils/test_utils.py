
from .text import generate_fingerprint, tokenize, remove_punctuation


def test_punctuation():
    assert 'a b c ' == remove_punctuation('a,b.c!')
