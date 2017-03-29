"""Text processing utilities."""

from collections import Counter
import string

from nltk.corpus import stopwords
import nltk


def generate_fingerprint(text):
    """Generate a fingerprint to be used for comparison to other texts."""
    text_tokens = tokenize(text)
    filtered_tokens = [word for word in text_tokens if word not in stopwords.words('english')]
    count_tokens = Counter(filtered_tokens)
    common_tokens = count_tokens.most_common(15)
    fingerprint = sorted([x for x, y in common_tokens])
    return '-'.join(fingerprint)[:255]


def tokenize(text):
    """Split text into words."""
    # translator = str.maketrans('', '', string.punctuation)
    # no_punctuation = text.lower().translate(None, string.punctuation)
    exclude = set(string.punctuation)
    no_punctuation = ''.join(char.lower() for char in text if char not in exclude)
    return nltk.word_tokenize(no_punctuation)
