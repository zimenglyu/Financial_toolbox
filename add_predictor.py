import pandas as pd
import numpy as np
import os
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


def add_volumn_change(df):
    df['VOL_CHANGE'] = df['VOL'].pct_change()
    return df

# def add_return(df):
#     df['Return'] = df['Adj Close'].pct_change()
#     return df
def add_BA_Spread(df):
    df['BA_SPREAD'] = (df['ASK'] - df['BID'])/df['PRC']
    return df

def add_Illiquidity(df):
    df['ILLIQUIDITY'] = df['RET'] /(df['VOL'] * df['PRC'])
    return df
# def add_TurnOver(df):
#     df['TURNOVER'] = df['VOL'] / df['SHROUT']
#     return df


def replace_char_with_zero(df, column_name):
    """
    Replaces 'c' with 0 in the specified column of the DataFrame.
    
    Parameters:
    - df: pandas DataFrame containing the target column.
    - column_name: string, the name of the column to process.
    
    Returns:
    - DataFrame with the 'c' character replaced with 0 in the specified column.
    """
    # Convert the column to string, replace 'c' with '0', and convert back to float
    df[column_name] = df[column_name].astype(str).str.replace('C', '0').astype(float)
    return df

if __name__ == '__main__':
    root_folder = "/Users/zimenglyu/Documents/datasets/CRSP/DJI_history"
    # file_path = "/Users/zimenglyu/Documents/datasets/CRSP/HWP.csv"
    # save_name = "/Users/zimenglyu/Documents/datasets/CRSP/HWP_new.csv"
    folders = get_folders_in_path(root_folder)
    for folder in folders:
        sub_folder = os.path.join(root_folder, folder)
        files = glob(os.path.join(sub_folder, "*.csv"))
        for file in files:
            file_name = file.split('/')[-1].split('.csv')[0]
            df = pd.read_csv(file)
            df = replace_char_with_zero(df, "RET")
            df = add_volumn_change(df)
            df = add_BA_Spread(df)
            df = add_Illiquidity(df)
            df.to_csv(os.path.join(sub_folder, file_name + "_new.csv"))
