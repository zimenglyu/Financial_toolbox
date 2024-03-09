
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
    folders =['91-97', '97-99', '99-04', '04-08', '08-08', '08-09', '09-12', '12-13', '13-15', '15-18', '18-19','19-20', '20-20', '20-22']
    columns = ["date","RET", "VOL_CHANGE", "BA_SPREAD", "ILLIQUIDITY"]
    repeat_columns = ["RET", "VOL_CHANGE", "BA_SPREAD", "ILLIQUIDITY"]
    stock_names = pd.read_csv(stock_name_path)
    DJI = pd.read_csv(DJI_path)
    DJI['date'] = pd.to_datetime(DJI['date'])
    for folder in folders:
        print("Processing folder: ", folder)
        combined_df = pd.DataFrame()
        file_count = 0
        names_over_period = stock_names[folder].values
        # print(names_over_period)
        sub_folder = os.path.join(root_folder, folder)
        for stock_name in names_over_period:
            filename = os.path.join(sub_folder, '{}_{}.csv'.format(stock_name, folder))
            df = pd.read_csv(filename)
            df_selected = df[columns].copy()
            df_selected = rename_columns(df_selected, repeat_columns, file_count)
            if file_count == 0:
                combined_df = df_selected
            else:
                combined_df['date'] = pd.to_datetime(combined_df['date'])
                df_selected['date'] = pd.to_datetime(df_selected['date'])
                combined_df = pd.merge(combined_df, df_selected, how="inner",  on='date')
                if(len(combined_df) != len(df_selected)):
                    print('file {} len of rows is {} not equal to {}'.format(stock_name, len(df_selected), len(combined_df)))
            file_count += 1
        df['date'] = pd.to_datetime(df['date'])
        combined_df = pd.merge(combined_df, df[['date','sprtrn']], how="inner",  on='date')
        combined_df = pd.merge(combined_df, DJI[['date','DJI_Return']], how="inner",  on='date')
        combined_df.to_csv(os.path.join(root_folder, folder + '.csv'), index=False)
