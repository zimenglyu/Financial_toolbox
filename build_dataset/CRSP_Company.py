import pandas as pd
import os
class CRSP_Company:
    def __init__(self, name, data):
        self.name = name
        self.data = data
        print("CRSP_Company object created for {}, and it contains {} rows.".format(name, len(data)))

    def add_volumn_change(self):
        # df['VOL_CHANGE'] = df['VOL'].diff()
        # return df
        self.data['VOL_CHANGE'] = self.data['VOL'].pct_change(fill_method=None)

    def add_BA_Spread(self):
        self.data['BA_SPREAD'] = (self.data['ASK'] - self.data['BID'])/self.data['PRC']

    def add_Illiquidity(self):
        self.data['ILLIQUIDITY'] = self.data['RET'] /(self.data['VOL'] * self.data['PRC'])

    def add_TurnOver(self):
        self.data['TURNOVER'] = self.data['VOL'] / self.data['SHROUT']

    def replace_char_with_zero(self, column_name):
        """
        Replaces 'c' with 0 in the specified column of the DataFrame.
        
        Parameters:
        - df: pandas DataFrame containing the target column.
        - column_name: string, the name of the column to process.
        
        Returns:
        - DataFrame with the 'c' character replaced with 0 in the specified column.
        """
        # Convert the column to string, replace 'c' with '0', and convert back to float
        self.data[column_name] = self.data[column_name].astype(str).str.replace('C', '0').astype(float)

    def join_by_date(self, new_data, column_name):
        self.data['date'] = pd.to_datetime(self.data['date'],format="mixed")
        self.data = pd.merge(self.data, new_data[['date',column_name]], how="inner",  on='date')
        print("company {}, after join DJI, lenth {}".format(self.name, len(self.data)))

    def split_train_validation_test(self, train_start, train_end, validation_start, validation_end, test_start, test_end):
        self.train = self.data[(self.data['date'] >= train_start) & (self.data['date'] <= train_end)]
        self.validation = self.data[(self.data['date'] >= validation_start) & (self.data['date'] <= validation_end)]
        self.test = self.data[(self.data['date'] >= test_start) & (self.data['date'] <= test_end)]
        print("company {}, train: {}, validation: {}, test: {}".format(self.name, len(self.train), len(self.validation), len(self.test)))
    
    def save_to_csv(self, root_path):
        self.train.to_csv(os.path.join(root_path, "train/{}.csv".format(self.name)), index=False)
        self.validation.to_csv(os.path.join(root_path, "validation/{}.csv".format(self.name)), index=False)
        self.test.to_csv(os.path.join(root_path, "test/{}.csv".format(self.name)), index=False)

    def select_columns(self, list_columns):
        self.data = self.data[list_columns]
    
    def remove_nan(self):
        self.data.dropna(inplace=True)

    def save_raw_data(self, root_path):
        self.data.to_csv(os.path.join(root_path, "raw_data/{}.csv".format(self.name)), index=False)