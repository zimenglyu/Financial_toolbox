import os
from pathlib import Path
from glob import glob
import pandas as pd

repo_root = Path(__file__).resolve().parents[1]
datasets_root = Path(os.getenv("FIN_DATASETS_DIR", repo_root / "datasets"))
root_path = datasets_root / "CRSP" / "DJI_company"
file_names = glob(str(root_path / "complete_file" / "*.csv"))

for file in file_names:
    # Step 1: Read the CSV file
    df = pd.read_csv(file, parse_dates=['date'])
    file_name = Path(file).stem
    # Step 2: Define your datetime ranges for splitting
    train_start = pd.to_datetime('1/1/1990')
    train_end = pd.to_datetime('12/31/2021')
    validation_start = pd.to_datetime('1/1/2022')
    validation_end = pd.to_datetime('12/31/2022')
    test_start = pd.to_datetime('1/1/2023')
    test_end = pd.to_datetime('12/30/2023')

    # Step 3: Split the DataFrame into train, validation, and test datasets
    # Train dataset
    train_df = df[(df['date'] >= train_start) & (df['date'] <= train_end)]

    # Validation dataset
    validation_df = df[(df['date'] >= validation_start) & (df['date'] <= validation_end)]

    # Test dataset
    test_df = df[(df['date'] >= test_start) & (df['date'] <= test_end)]

    # Optional: Save these datasets to new CSV files if needed
    train_df.to_csv(root_path / "train" / f"{file_name}.csv", index=False)
    validation_df.to_csv(root_path / "validation" / f"{file_name}.csv", index=False)
    test_df.to_csv(root_path / "test" / f"{file_name}.csv", index=False)
