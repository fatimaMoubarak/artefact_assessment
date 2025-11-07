from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


class TextTokenizer:
    def __init__(self):
        # Define stopwords for English and Arabic
        self.english_stopwords = set(stopwords.words("english"))
        self.arabic_stopwords = set(stopwords.words("arabic"))

    def remove_stopwords_and_tokenize(self, text, language_code: str) -> list:
        """Tokenize the text and remove stopwords based on the language."""

        if not text:
            return []

        # Tokenize the text
        tokens = word_tokenize(text)

        # Determine the stopwords set based on the language
        stop_words = self.get_stopwords(language_code)

        # Filter out stopwords and very short words (length > 2)
        filtered_tokens = [
            word for word in tokens if word.lower() not in stop_words and len(word) > 2
        ]
        return filtered_tokens

    def get_stopwords(self, language_code: str) -> set:
        """Get the stopwords set based on language code."""
        if language_code == "ara":
            return self.arabic_stopwords
        else:
            return self.english_stopwords
