import os
from pathlib import Path
import pandas as pd

# Specify the directory containing the CSV files
repo_root = Path(__file__).resolve().parents[1]
datasets_root = Path(os.getenv("FIN_DATASETS_DIR", repo_root / "datasets"))
directory = datasets_root / "CRSP" / "DJI_company" / "complete_file"

# Iterate over all files in the directory
for filename in os.listdir(directory):
    # Check if the file is a CSV file
    if filename.endswith('.csv'):
        # Construct the full file path
        file_path = directory / filename
        
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Remove rows that contain any NaN values
        df_cleaned = df.dropna()
        
        # Save the cleaned DataFrame back to CSV
        df_cleaned.to_csv(file_path, index=False)
        
        print(f'Cleaned {filename}')
