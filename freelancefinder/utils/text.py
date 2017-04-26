"""Text processing utilities."""

from collections import Counter
import operator
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
    common_tokens = sorted(count_tokens.most_common(), key=operator.itemgetter(1, 0), reverse=True)
    fingerprint = [x for x, y in common_tokens[:15]]  # pylint: disable=unused-variable
    return '-'.join(fingerprint)[:255]


def tokenize(text):
    """Split text into words."""
    return nltk.word_tokenize(remove_punctuation(text))


def remove_punctuation(text):
    """Remove all punctuation from a string."""
    exclude = set(string.punctuation)
    # return ''.join(char.lower() for char in text if char not in exclude)
    return ''.join(char.lower() if char not in exclude else ' ' for char in text)
