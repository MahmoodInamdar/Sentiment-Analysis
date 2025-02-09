import os
from pathlib import Path
from pipeline.data_reader import read_csv
from pipeline.preprocessor import clean_text
from pipeline.analyzer import SentimentAnalyzer
from pipeline.pipeline import Pipeline

def main():
    # Setup paths
    input_path = Path("data/input/sample_feedback.csv")
    output_dir = Path("data/output")
    output_dir.mkdir(exist_ok=True)
    
    # Initialize pipeline components
    analyzer = SentimentAnalyzer()
    
    # Build pipeline
    pipeline = Pipeline()
    pipeline.add_stage(lambda _: read_csv(input_path))
    pipeline.add_stage(lambda df: df['text'].apply(clean_text))
    pipeline.add_stage(lambda texts: [analyzer.analyze(text) for text in texts])
    
    # Execute pipeline
    results = pipeline.run(None)
    
    # Save and display results
    if results is not None:
        df = read_csv(input_path)
        df['sentiment'] = results
        output_path = output_dir / "results.csv"
        df.to_csv(output_path, index=False)
        print(f"\nResults saved to {output_path}")
        print("\nSample results:")
        print(df[['text', 'sentiment']].head().to_string(index=False))

if __name__ == "__main__":
    main()