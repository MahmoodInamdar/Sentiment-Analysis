from typing import List
from transformers import pipeline
from pipecat.frames.frames import Frame
from pipecat.pipeline.base_pipeline import BasePipeline
from pipecat.processors.frame_processor import FrameProcessor, FrameDirection

class SentimentAnalysisProcessor(FrameProcessor):
    def __init__(self):
        super().__init__()
        # Use a model that classifies into positive, negative, and neutral
        self.classifier = pipeline(
            "sentiment-analysis", 
            model="cardiffnlp/twitter-roberta-base-sentiment", 
            tokenizer="cardiffnlp/twitter-roberta-base-sentiment"
        )

    async def process_frame(self, frame: Frame, direction: FrameDirection):
        await super().process_frame(frame, direction)

        if direction == FrameDirection.DOWNSTREAM:
            text = frame.metadata.get("text", "")
            result = self.classifier(text)[0]
            sentiment = result["label"]

            # Mapping label to human-readable sentiment
            if sentiment == "LABEL_0":
                sentiment = "negative"
            elif sentiment == "LABEL_1":
                sentiment = "neutral"
            else:
                sentiment = "positive"

            frame.metadata["sentiment"] = sentiment
            frame.metadata["score"] = result["score"]
            
        await self.push_frame(frame, direction)


class SentimentPipeline(BasePipeline):
    def __init__(self):
        super().__init__()
        self._processor = SentimentAnalysisProcessor()
        self._processors: List[FrameProcessor] = [self._processor]
        self._link_processors()

    async def process_frame(self, frame: Frame, direction: FrameDirection):
        await super().process_frame(frame, direction)
        await self._processor.process_frame(frame, direction)

    def _link_processors(self):
        prev = self._processors[0]
        prev.set_parent(self)


# Instructions for Running the Sentiment Analysis Pipeline
import asyncio
from pipecat.frames.frames import Frame
from pipecat.processors.frame_processor import FrameDirection

async def run_sentiment_analysis():
    pipeline = SentimentPipeline()
    texts = [
        "I love this product!",
        "This is the worst experience I've had.",
        "It's okay, nothing special.",
        "Absolutely fantastic service!",
        "I'm not sure how I feel about this."
        "It was okay, not bad not good."
    ]
    
    for text in texts:
        frame = Frame()
        frame.metadata = {"text": text}
        await pipeline.process_frame(frame, FrameDirection.DOWNSTREAM)
        print(f"Input: {text}\nSentiment: {frame.metadata['sentiment']}\nScore: {frame.metadata['score']}\n")

asyncio.run(run_sentiment_analysis())
