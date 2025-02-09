import re
from .exceptions import PreprocessingError

def clean_text(text: str) -> str:
    try:
        # Remove special characters except apostrophes
        text = re.sub(r"[^a-zA-Z0-9'\s]", '', text)
        # Convert to lowercase
        text = text.lower().strip()
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        return text
    except Exception as e:
        raise PreprocessingError(f"Error cleaning text: {str(e)}")