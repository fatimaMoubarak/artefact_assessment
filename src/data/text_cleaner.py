# text_cleaner.py
import re
import pandas as pd
from nltk.corpus import stopwords


class TextCleaner:
    def __init__(self):
        # Define stopwords for English and Arabic
        self.stop_words_eng = set(stopwords.words("english"))
        self.stop_words_ara = set(stopwords.words("arabic"))

    def normalize_arabic(self, text: str) -> str:
        """Normalize Arabic text to handle variations in certain characters."""
        text = re.sub(r"[إأٱآا]", "ا", text)  # Normalize Alif variants
        text = re.sub(r"[ؤء]", "ء", text)  # Normalize Hamza variants
        text = re.sub(
            r"[\u064B\u064C\u064D\u064E\u064F\u0650\u0651\u0652]", "", text
        )  # Remove diacritics
        return text

    def clean_text_english(self, text: str) -> str:
        """Clean and normalize English text."""
        if pd.isna(text) or text == "":
            return ""

        # Convert to lowercase and remove URLs
        text = str(text).lower()
        text = re.sub(r"http\S+|www\S+", "", text)

        # Remove special characters but keep spaces and clean extra whitespace
        text = re.sub(r"[^\w\s]", " ", text)
        text = " ".join(text.split())

        return text

    def clean_text_arabic(self, text: str) -> str:
        """Clean and normalize Arabic text."""
        if pd.isna(text) or text == "":
            return ""

        # Normalize Arabic text and remove URLs
        text = self.normalize_arabic(text)
        text = re.sub(r"http\S+|www\S+", "", text)

        # Remove Arabic punctuation and special characters
        text = re.sub(
            r"[^\w\s\u0600-\u06FF]", " ", text
        )  # Keep Arabic letters and spaces
        text = " ".join(text.split())

        return text

    def apply_cleaning(self, row: pd.Series) -> str:
        """Apply text cleaning based on the language."""
        if row["language"] == "ara":
            return self.clean_text_arabic(row["text_for_analysis"])
        else:
            return self.clean_text_english(row["text_for_analysis"])
