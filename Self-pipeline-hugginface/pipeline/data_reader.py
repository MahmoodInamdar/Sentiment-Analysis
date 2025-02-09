import pandas as pd
from .exceptions import DataReadError

def read_csv(file_path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(file_path)
        if 'text' not in df.columns:
            raise ValueError("CSV must contain 'text' column")
        return df
    except Exception as e:
        raise DataReadError(f"Error reading {file_path}: {str(e)}")