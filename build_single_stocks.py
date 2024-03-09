
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
def make_dir(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        print(f"Directory '{path}' already exists.")

def rename_columns(df, columns, file_count):
    for col in columns:
        df.rename(columns={col: col + '_' +str(file_count)}, inplace=True)
    return df


if __name__ == '__main__':
    root_folder = "/Users/zimenglyu/Documents/datasets/CRSP/DJI_history_train_vali_test"
    stock_name_path = "/Users/zimenglyu/Documents/datasets/CRSP/DJI_history_new/stock_name.csv"
    DJI_path = '/Users/zimenglyu/Documents/datasets/stock/DJI_stock_data.csv'
    # folders =['91-97', '97-99', '99-04', '04-08', '08-08', '08-09', '09-12', '12-13', '13-15', '15-18', '18-19','19-20', '20-20']
    folders = ['20-22']
    columns = ["date","TICKER","RET", "VOL_CHANGE", "BA_SPREAD", "ILLIQUIDITY", 'PRC','sprtrn']
    # repeat_columns = ["RET", "VOL_CHANGE", "BA_SPREAD", "ILLIQUIDITY"]
    stock_names = pd.read_csv(stock_name_path)
    DJI = pd.read_csv(DJI_path)
    DJI['date'] = pd.to_datetime(DJI['date'], format="mixed")
    
    for file_count in range(30):
        folder_count = 13
        # stock_data = pd.DataFrame()
        for folder in folders:
            sub_folder = os.path.join(root_folder, folder)
            stock_name = stock_names[folder].values[file_count]
            filename = os.path.join(sub_folder, '{}_{}.csv'.format(stock_name, folder))
            df = pd.read_csv(filename)
            df_selected = df[columns].copy()
            df_selected['date'] = pd.to_datetime(df_selected['date'],format="mixed")
            df_selected = df_selected.loc[df_selected['date'] >= '12/28/1992']
            file_name = stock_names['20-22'].values[file_count]
            combined_df = pd.merge(df_selected, DJI[['date','DJI_Return']], how="inner",  on='date')
            combined_df.to_csv(os.path.join(root_folder + "/single_stocks/temp", file_name + '_' + str(folder_count) + '.csv'), index=False)
            # combined_df.to_csv(os.path.join(root_folder + "/single_stocks", file_name + '.csv'), index=False)
            folder_count += 1
