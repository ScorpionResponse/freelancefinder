"""Text processing utilities."""

from collections import Counter
import string

from nltk.corpus import stopwords
import nltk

try:
    nltk.word_tokenize('test phrase')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')


def generate_fingerprint(text):
    """Generate a fingerprint to be used for comparison to other texts."""
    text_tokens = tokenize(text)
    filtered_tokens = [word for word in text_tokens if word not in stopwords.words('english')]
    count_tokens = Counter(filtered_tokens)
    common_tokens = count_tokens.most_common(15)
    fingerprint = sorted([x for x, y in common_tokens])  # pylint: disable=unused-variable
    return '-'.join(fingerprint)[:255]


def tokenize(text):
    """Split text into words."""
    exclude = set(string.punctuation)
    no_punctuation = ''.join(char.lower() for char in text if char not in exclude)
    return nltk.word_tokenize(no_punctuation)
