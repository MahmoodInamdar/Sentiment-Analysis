import asyncio # For handling asynchronous operations
import pandas as pd # For data manipulation
from pipecat.frames.frames import Frame # For creating and managing frames/Data Containers
from pipecat.pipeline.base_pipeline import BasePipeline # For creating a pipeline
from pipecat.processors.frame_processor import FrameProcessor, FrameDirection # For creating custom processors/ Procressing containers
from transformers import pipeline # For using the sentiment analysis model
import re # For regular expressions

"""
Every time the process_frame method is called:

It checks if data has to be loaded.
Selects one row from the dataframe.
It processes that row.
Updates the frame using the processed data.
Transfers the frame to the next processor.

The design allows for:

Memory-efficient processing (a row at a time)
Error resilience
Clean integration with other pipeline processors.
Asynchronous operation.
Simple data flow control
"""

# Step 1: Data Reading and Preprocessing
class DataReadingProcessor(FrameProcessor):
    def __init__(self, file_path):
        super().__init__() # Initialize the parent class
        self.file_path = file_path # Set the file path
    
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



"""

What this preprocessing accomplishes:

Removes punctuation marks (.,!,?, etc.).
Removes special characters like @, #, and $.
Removes emojis and other Unicode characters
transforms all text to lowercase.
Maintains a gap between words.
Keeps the numbers intact.

Be aware of these limitations:

Loss of potentially significant punctuation.
Deletes email addresses, URLs, and potentially useful symbols.
Capitalization information is lost.

"""


def preprocess_text(text):
    """
    Preprocesses the input text by removing special characters and converting to lowercase.
    """
    # Remove special characters (keeping only letters, digits, and spaces)
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    # Convert text to lowercase
    cleaned_text = cleaned_text.lower()
    return cleaned_text


"""

Key Features and Benefits:

Asynchronous processing uses async/await to efficiently handle multiple frames.
Custom Neutral Detection: Provides nuance to the basic positive/negative classification.
Score Preservation: Maintains the confidence score for potential future usage.
Human-Readable Labels: converts technical labels into simple terms.
Non-destructive: Adds to metadata without changing the original text.

"""


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
            if 0.40 <= score <= 0.60:
                sentiment = "neutral"
            
            # Map labels to human-readable form
            if sentiment == "LABEL_0":
                sentiment = "negative"
            elif sentiment == "LABEL_2":
                sentiment = "positive"

            frame.metadata["sentiment"] = sentiment
            frame.metadata["score"] = score
        
        await self.push_frame(frame, direction)

"""

Key Features and Benefits: Asynchronous Processing.

To efficiently handle many frames, use async/await.
Allows non-blocking processes, making it suitable for high-throughput systems.
Custom Neutral Detection
Introduces a criteria that classifies sentiment as neutral when the confidence score falls between 0.40 and 0.60.
Adds subtlety to the fundamental positive/negative categorization, increasing accuracy in ambiguous instances.
Score Preservation
The confidence score (score) is retained in the frame's metadata.
Allows for additional analysis or filtering based on the model's confidence in its predictions.
Human-readable labels
Converts technical labels (LABEL_0, LABEL_1, LABEL_2) to simple, understandable phrases.
Makes the output easier to understand and apply in subsequent applications.
Non-Destructive Processing.
Adds sentiment and a score to the frame's information without changing the original text.



"""

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

"""

Input and Output files:

Reads information from input_data.csv.
Saves the results to output_results.csv.
Pipeline Setup:
The input file is used to initialize a sentiment analysis pipeline.
Processing:
Each piece of text (frame) is evaluated to determine its sentiment and confidence level.
Stops when there is no more data to process.
Savings Results:
Saves the findings (text, sentiment, and score) to a CSV file.
If something goes wrong, it prints either a success message or an error.

"""

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
