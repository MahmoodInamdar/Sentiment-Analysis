# import pandas as pd

# def read_data(file_path):
#     try:
#         data = pd.read_csv(file_path)
#         return data
#     except Exception as e:
#         print(f"Error reading data: {e}")
#         return None


# import pandas as pd
# from pipecat.processors.frame_processor import FrameProcessor

# class DataReader(FrameProcessor):
#     def __init__(self, file_path):
#         super().__init__()
#         self.file_path = file_path

#     async def process_frame(self, frame, direction):
#         try:
#             data = pd.read_csv(self.file_path)
#             for _, row in data.iterrows():
#                 await self.push_frame(row.to_dict(), direction)
#         except Exception as e:
#             print(f"Error reading data: {e}")

# import pandas as pd
# from pipecat.processors.frame_processor import FrameProcessor

# class DataReader(FrameProcessor):
#     def __init__(self, file_path):
#         super().__init__()  # Initialize the base FrameProcessor class
#         self.file_path = file_path

#     async def process_frame(self, frame, direction):
#         # Call the superclass's process_frame method
#         await super().process_frame(frame, direction)
#         try:
#             data = pd.read_csv(self.file_path)
#             for _, row in data.iterrows():
#                 await self.push_frame(row.to_dict(), direction)
#         except Exception as e:
#             print(f"Error reading data: {e}")

import pandas as pd
from pipecat.processors.frame_processor import FrameProcessor

class DataReader(FrameProcessor):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    async def process_frame(self, frame, direction):
        try:
            data = pd.read_csv(self.file_path)
            for _, row in data.iterrows():
                await self.push_frame(row.to_dict(), direction)
        except Exception as e:
            print(f"Error reading data: {e}")
