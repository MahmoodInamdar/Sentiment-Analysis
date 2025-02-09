from pipecat.pipeline.pipeline import Pipeline
from pipeline.data_reader import DataReader
from pipeline.preprocessor import Preprocessor
from pipeline.sentiment_analyzer import SentimentAnalyzer
from pipeline.output import OutputWriter

def run_pipeline(input_file, output_file):
    components = [
        DataReader(input_file),
        Preprocessor(),
        SentimentAnalyzer(),
        OutputWriter(output_file)
    ]
    pipeline = Pipeline(components)
    #pipeline.run()

if __name__ == "__main__":
    input_csv = "data/sample_feedback.csv"
    output_csv = "data/output_results.csv"
    run_pipeline(input_csv, output_csv)



# from pipecat.pipeline.pipeline import Pipeline
# from pipecat.pipeline.runner import PipelineTask, PipelineRunner
# from pipeline.data_reader import DataReader
# from pipeline.preprocessor import Preprocessor
# from pipeline.sentiment_analyzer import SentimentAnalyzer
# from pipeline.output import OutputWriter

# def run_pipeline(input_file, output_file):
#     # Define the pipeline components
#     components = [
#         DataReader(input_file),
#         Preprocessor(),
#         SentimentAnalyzer(),
#         OutputWriter(output_file)
#     ]
    
#     # Create the pipeline
#     pipeline = Pipeline(components)
    
#     # Create a PipelineTask
#     task = PipelineTask(pipeline)
    
#     # Create a PipelineRunner
#     runner = PipelineRunner()
    
#     # Run the pipeline
#     runner.run(task)

# if __name__ == "__main__":
#     input_csv = "data/sample_feedback.csv"
#     output_csv = "data/output_results.csv"
#     run_pipeline(input_csv, output_csv)



# import asyncio
# from pipecat.pipeline.pipeline import Pipeline
# from pipecat.pipeline.runner import PipelineTask, PipelineRunner
# from pipeline.data_reader import DataReader
# from pipeline.preprocessor import Preprocessor
# from pipeline.sentiment_analyzer import SentimentAnalyzer
# from pipeline.output import OutputWriter

# async def run_pipeline(input_file, output_file):
#     # Define the pipeline components
#     components = [
#         DataReader(input_file),
#         Preprocessor(),
#         SentimentAnalyzer(),
#         OutputWriter(output_file)
#     ]
    
#     # Create the pipeline
#     pipeline = Pipeline(components)
    
#     # Create a PipelineTask
#     task = PipelineTask(pipeline)
    
#     # Create a PipelineRunner
#     runner = PipelineRunner()
    
#     # Run the pipeline
#     await runner.run(task)

# if __name__ == "__main__":
#     input_csv = "data/sample_feedback.csv"
#     output_csv = "data/output_results.csv"
#     asyncio.run(run_pipeline(input_csv, output_csv))
