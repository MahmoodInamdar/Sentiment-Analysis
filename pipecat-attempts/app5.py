import asyncio
import pandas as pd
from pipecat.frames.frames import Frame
from pipecat.pipeline.base_pipeline import BasePipeline
from pipecat.processors.frame_processor import FrameProcessor, FrameDirection
from transformers import pipeline
import re

# Step 1: Data Reading and Preprocessing
class DataReadingProcessor(FrameProcessor):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
    
    async def process_frame(self, frame: Frame, direction: FrameDirection):
        await super().process_frame(frame, direction)
        
        if direction == FrameDirection.DOWNSTREAM:
            # Read data only once
            if not hasattr(self, 'df'):
                try:
                    self.df = pd.read_csv(self.file_path)
                    if 'text' not in self.df.columns:
                        raise ValueError("CSV file must contain a 'text' column.")
                    self.df['processed_text'] = self.df['text'].apply(lambda x: preprocess_text(x))
                except Exception as e:
                    print(f"Error reading CSV: {e}")
                    return
            
            # Push the rows one by one
            if len(self.df) > 0:
                row = self.df.iloc[0]  # Get the first row
                self.df = self.df.iloc[1:]  # Remove the first row from the DataFrame

                frame.metadata["text"] = row["text"]
                frame.metadata["processed_text"] = row["processed_text"]
                
            else:
                print("No more data to process.")
                
        await self.push_frame(frame, direction)


def preprocess_text(text):
    """
    Preprocesses the input text by removing special characters and converting to lowercase.
    """
    # Remove special characters (keeping only letters, digits, and spaces)
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    # Convert text to lowercase
    cleaned_text = cleaned_text.lower()
    return cleaned_text


# Step 2: Sentiment Analysis Processor with Custom Score Filter
class SentimentAnalysisProcessor(FrameProcessor):
    def __init__(self):
        super().__init__()
        self.classifier = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment",
            tokenizer="cardiffnlp/twitter-roberta-base-sentiment"
        )
    
    async def process_frame(self, frame: Frame, direction: FrameDirection):
        await super().process_frame(frame, direction)

        if direction == FrameDirection.DOWNSTREAM:
            text = frame.metadata.get("processed_text", "")
            result = self.classifier(text)[0]
            sentiment = result["label"]
            score = result["score"]

            # Implement custom filter for neutral based on score
            # if 0.40 <= score <= 0.60:
            #     sentiment = "neutral"
            
            # Map labels to human-readable form
            if sentiment == "LABEL_0":
                sentiment = "negative"
            elif sentiment == "LABEL_2":
                sentiment = "positive"
            elif sentiment == "LABEL_1":
                sentiment = "neutral"

            frame.metadata["sentiment"] = sentiment
            frame.metadata["score"] = score
        
        await self.push_frame(frame, direction)


# Step 3: Setting Up the Complete Pipeline
class SentimentPipeline(BasePipeline):
    def __init__(self, file_path):
        super().__init__()
        
        # Initialize processors
        self._data_reader = DataReadingProcessor(file_path)
        self._sentiment_processor = SentimentAnalysisProcessor()
        
        # Set processors
        self._processors = [self._data_reader, self._sentiment_processor]
        self._link_processors()

    async def process_frame(self, frame: Frame, direction: FrameDirection):
        await super().process_frame(frame, direction)
        for processor in self._processors:
            await processor.process_frame(frame, direction)

    def _link_processors(self):
        prev = self._processors[0]
        prev.set_parent(self)


# Step 4: Run the Pipeline and Output Results
async def run_sentiment_analysis():
    file_path = 'input_data.csv'  # Replace with the actual file path
    output_file_path = 'output_results.csv'
    
    # Initialize the pipeline with the file path
    pipeline = SentimentPipeline(file_path)
    
    # Process data using the pipeline
    results = []
    while True:
        frame = Frame()
        await pipeline.process_frame(frame, FrameDirection.DOWNSTREAM)
        
        # If the frame doesn't have any more data, break the loop
        if 'text' not in frame.metadata:
            break

        # Output results for each line
        sentiment = frame.metadata['sentiment']
        score = frame.metadata['score']
        text = frame.metadata['text']
        results.append({"text": text, "sentiment": sentiment, "score": score})

    # Saving results to CSV
    try:
        df = pd.DataFrame(results)
        df.to_csv(output_file_path, index=False)
        print(f"Sentiment analysis results saved to {output_file_path}")
    except Exception as e:
        print(f"Error saving results to CSV: {e}")

# Run the pipeline
asyncio.run(run_sentiment_analysis())