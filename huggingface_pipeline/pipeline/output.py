import pandas as pd
from pipecat.processors.frame_processor import FrameProcessor

class OutputWriter(FrameProcessor):
    def __init__(self, filename):
        super().__init__()  # Initialize the base FrameProcessor class
        self.filename = filename
        self.results = []

    def process(self, data):
        if data:
            self.results.append(data)
    
    def finalize(self):
        try:
            df = pd.DataFrame(self.results)
            df.to_csv(self.filename, index=False)
            print(f"Results saved to {self.filename}")
        except Exception as e:
            print(f"Error saving results: {str(e)}")
