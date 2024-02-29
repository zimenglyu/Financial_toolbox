import pandas as pd
import os

# Specify the directory containing the CSV files
directory = '/Users/zimenglyu/Documents/datasets/CRSP/DJI_history_new/single_stocks/test'

# Iterate over all files in the directory
for filename in os.listdir(directory):
    # Check if the file is a CSV file
    if filename.endswith('.csv'):
        # Construct the full file path
        file_path = os.path.join(directory, filename)
        
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Remove rows that contain any NaN values
        df_cleaned = df.dropna()
        
        # Save the cleaned DataFrame back to CSV
        df_cleaned.to_csv(file_path, index=False)
        
        print(f'Cleaned {filename}')
