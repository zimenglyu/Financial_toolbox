import pandas as pd
from glob import glob

file_path = '/Users/zimenglyu/Documents/datasets/CRSP/DJI_history_new/'
filenames = glob(file_path + '*.csv')
for file in filenames:
    df = pd.read_csv(file)
    df_cleaned = df.dropna()
    df_cleaned.to_csv(file)

# # names = df.columns.to_list()
# print(df.columns)
# with open('column_names.txt', 'w') as file:
#     for column in names:
#         file.write(column + '  ')