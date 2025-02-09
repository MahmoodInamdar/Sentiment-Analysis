class PipelineError(Exception):
    """Base class for pipeline exceptions"""
    pass

class DataReadError(PipelineError):
    """Error reading input data"""
    pass

class PreprocessingError(PipelineError):
    """Error during text preprocessing"""
    pass

class AnalysisError(PipelineError):
    """Error during sentiment analysis"""
    pass