from typing import List

from transformers import pipeline
from pipecat.frames.frames import Frame
from pipecat.pipeline.base_pipeline import BasePipeline
from pipecat.processors.frame_processor import FrameProcessor, FrameDirection


class SentimentAnalysisProcessor(FrameProcessor):
    def __init__(self):
        super().__init__()
        self.classifier = pipeline("sentiment-analysis")

    async def process_frame(self, frame: Frame, direction: FrameDirection):
        # Call super first, then perform your specific operations.
        await super().process_frame(frame, direction)

        if direction == FrameDirection.DOWNSTREAM:
            text = frame.metadata.get("text", "")
            result = self.classifier(text)[0]
            frame.metadata["sentiment"] = result["label"]
            frame.metadata["score"] = result["score"]
            
        # Push the processed frame downstream.
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



## Running the Analysis:

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
    ]
    
    for text in texts:
        frame = Frame()
        frame.metadata={"text": text}
        await pipeline.process_frame(frame, FrameDirection.DOWNSTREAM)
        print(f"Input: {text}\nSentiment: {frame.metadata['sentiment']}\nScore: {frame.metadata['score']}\n")

asyncio.run(run_sentiment_analysis())

