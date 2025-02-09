import re
from pipecat.processors.frame_processor import FrameProcessor


class Preprocessor(FrameProcessor):
    def process(self, text):
        try:
            cleaned = re.sub(r'[^a-zA-Z0-9\s]', '', text)
            cleaned = cleaned.lower().strip()
            return cleaned
        except Exception as e:
            print(f"Error preprocessing text: {str(e)}")
            return None


# import re
# from pipecat.processors.frame_processor import FrameProcessor

# class Preprocessor(FrameProcessor):
#     def __init__(self):
#         super().__init__()  # Initialize the base FrameProcessor class

#     def process(self, text):
#         try:
#             cleaned = re.sub(r'[^a-zA-Z0-9\s]', '', text)
#             cleaned = cleaned.lower().strip()
#             return cleaned
#         except Exception as e:
#             print(f"Error preprocessing text: {str(e)}")
#             return None

