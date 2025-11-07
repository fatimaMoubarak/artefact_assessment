import arabic_reshaper
from bidi.algorithm import get_display


def display_arabic(text):
    """Reshapes Arabic text so it renders correctly in Matplotlib."""
    if not isinstance(text, str):
        return text
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)
