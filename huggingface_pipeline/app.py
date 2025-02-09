from pipecat.pipeline.pipeline import Pipeline
from pipeline.preprocessor import Preprocessor
from pipeline.sentiment_analyzer import SentimentAnalyzer
from pipeline.output import OutputWriter

def run_pipeline(user_input, output_file):
    # Initialize the pipeline with the processors
    pipeline = Pipeline([
        Preprocessor(),
        SentimentAnalyzer(),
        OutputWriter(output_file)
    ])
    # Process the user input
    pipeline.run(user_input)

if __name__ == "__main__":
    # Prompt the user for input
    user_input = input("Please enter the text for sentiment analysis: ")
    output_csv = "data/output_results.csv"
    run_pipeline(user_input, output_csv)
