from typing import Callable, Any

class Pipeline:
    def __init__(self):
        self.stages = []
        
    def add_stage(self, stage: Callable[[Any], Any]) -> None:
        self.stages.append(stage)
        
    def run(self, initial_input: Any) -> Any:
        data = initial_input
        for stage in self.stages:
            try:
                data = stage(data)
            except Exception as e:
                print(f"Pipeline Error: {str(e)}")
                return None
        return data
    