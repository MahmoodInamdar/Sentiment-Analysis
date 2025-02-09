from transformers import pipeline
from pipecat.processors.frame_processor import FrameProcessor

class SentimentAnalyzer(FrameProcessor):
    def __init__(self):
        super().__init__()  # Initialize the base FrameProcessor class
        self.model = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest"
        )

    async def process_frame(self, frame, direction):
        text = frame.get('text')
        if not text:
            return
        try:
            result = self.model(text)[0]
            sentiment_frame = {
                "text": text,
                "sentiment": result['label'],
                "confidence": result['score']
            }
            await self.push_frame(sentiment_frame, direction)
        except Exception as e:
            print(f"Error analyzing sentiment: {str(e)}")
