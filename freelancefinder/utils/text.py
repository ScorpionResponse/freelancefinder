"""Text processing utilities."""

from collections import Counter
import string

from nltk.corpus import stopwords
import nltk

nltk.download('punkt')
nltk.download("stopwords")


def generate_fingerprint(text):
    """Generate a fingerprint to be used for comparison to other texts."""
    text_tokens = tokenize(text)
    filtered_tokens = [word for word in text_tokens if word not in stopwords.words('english')]
    count_tokens = Counter(filtered_tokens)
    common_tokens = count_tokens.most_common(15)
    fingerprint = sorted([x for x, y in common_tokens])
    return '-'.join(fingerprint)


def tokenize(text):
    """Split text into words."""
    translator = str.maketrans('', '', string.punctuation)
    no_punctuation = text.lower().translate(translator)
    return nltk.word_tokenize(no_punctuation)
