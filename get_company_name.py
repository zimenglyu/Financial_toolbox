import os
import pandas as pd
from glob import glob

def get_folders_in_path(path):
    """
    Returns a list of all folders/directories in the specified path.
    """
    # List all entries in the given path
    entries = os.listdir(path)
    
    # Filter entries to only include directories
    folders = [entry for entry in entries if os.path.isdir(os.path.join(path, entry))]
    
    return folders



if __name__ == '__main__':
    root_folder = "/Users/zimenglyu/Documents/datasets/CRSP/DJI_history_new"
    # folders = get_folders_in_path(root_folder)
    folders =['91-97', '97-99', '99-04', '04-08', '08-08', '08-09', '09-12', '12-13', '13-15', '15-18', '18-19','19-20', '20-20', '20-22']
    all_name = pd.DataFrame()
    for folder in folders:
        sub_folder = os.path.join(root_folder, folder)
        files = sorted(glob(os.path.join(sub_folder, "*.csv")))
        # print(files)
        names = []
        for file in files:
            file_name = file.split('/')[-1].split('.csv')[0].split('_')[0]
            names.append(file_name)
        all_name[folder] = names
    all_name.columns = all_name.columns.astype(str)
    all_name.to_csv('/Users/zimenglyu/Documents/datasets/CRSP/DJI_history_new/stock_name.csv', index=False)