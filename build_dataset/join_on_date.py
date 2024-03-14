import numpy as np
import pandas as pd

def join_by_date(df1, df2):
    merged_data = pd.merge(df1, df2, how="inner",  on='DateTime')
    return merged_data

if __name__ == '__main__':


    file2 = ""
    file1 = ""
    save_name = ""

    df1 = pd.read_csv(file1, parse_dates=["Date"], index_col="Date")
    df2 = pd.read_csv(file2, parse_dates=["Date"], index_col="Date")

    df = join_by_date(df1, df2)
    df.to_csv(save_name)