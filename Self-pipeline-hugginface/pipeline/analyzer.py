from transformers import pipeline
from .exceptions import AnalysisError

class SentimentAnalyzer:
    def __init__(self):
        try:
            self.classifier = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                return_all_scores=True
            )
        except Exception as e:
            raise AnalysisError(f"Model loading failed: {str(e)}")

    def analyze(self, text: str) -> str:
        try:
            result = self.classifier(text)
            # Extract the label with highest score
            return max(result[0], key=lambda x: x['score'])['label'].capitalize()
        except Exception as e:
            raise AnalysisError(f"Analysis failed: {str(e)}")

