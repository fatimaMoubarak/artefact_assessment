import nltk
import re
import pandas as pd

# Download required NLTK data
try:
    nltk.data.find("tokenizers/punkt")
    nltk.data.find("corpora/stopwords")
except LookupError:
    print("Downloading NLTK data...")
    nltk.download("punkt", quiet=True)
    nltk.download("stopwords", quiet=True)
    nltk.download("punkt_tab", quiet=True)
    print("✓ NLTK data downloaded")

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

print("✓ NLP tools ready")

# Download necessary NLTK data
nltk.download("stopwords")
nltk.download("punkt")

# Define stopwords for Arabic and English
stop_words_eng = set(stopwords.words("english"))
stop_words_ara = set(stopwords.words("arabic"))


# Function to normalize Arabic text
def normalize_arabic(text):
    """Normalize Arabic text to handle variations in certain characters."""
    text = re.sub(r"[إأٱآا]", "ا", text)  # Normalize Alif variants
    text = re.sub(r"[ؤء]", "ء", text)  # Normalize Hamza variants
    text = re.sub(
        r"[\u064B\u064C\u064D\u064E\u064F\u0650\u0651\u0652]", "", text
    )  # Remove diacritics
    return text


# Clean English text function
def clean_text_english(text):
    """Clean and normalize English text."""
    if pd.isna(text) or text == "":
        return ""

    # Convert to lowercase
    text = str(text).lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # Remove special characters but keep spaces
    text = re.sub(r"[^\w\s]", " ", text)

    # Remove extra whitespace
    text = " ".join(text.split())

    return text


# Clean Arabic text function
def clean_text_arabic(text):
    """Clean and normalize Arabic text."""
    if pd.isna(text) or text == "":
        return ""

    # Normalize Arabic text (handle Alif, Yeh, Hamza variations)
    text = normalize_arabic(text)

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # Remove Arabic punctuation and special characters but keep spaces
    text = re.sub(
        r"[^\w\s\u0600-\u06FF]", " ", text
    )  # Keep Arabic letters, numbers, and spaces

    # Remove extra whitespace
    text = " ".join(text.split())

    return text


# Apply the respective cleaning function based on language
def apply_cleaning(row):
    """Apply text cleaning based on the language."""
    if row["language"] == "ara":
        return clean_text_arabic(row["text_for_analysis"])
    else:
        return clean_text_english(row["text_for_analysis"])


# Tokenization and stopword removal
def remove_stopwords(text, language):
    """Remove stopwords from text based on language."""
    if not text:
        return []
    tokens = word_tokenize(text)
    if language == "ara":
        # Remove Arabic stopwords
        stop_words = stop_words_ara
    else:
        # Remove English stopwords
        stop_words = stop_words_eng

    # Filter out stopwords and very short words (length > 2)
    filtered = [word for word in tokens if word not in stop_words and len(word) > 2]
    return filtered
