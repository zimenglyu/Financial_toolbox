import pandas as pd
from CRSP_Company import CRSP_Company
class CRSP_Dataset:
    def __init__(self, file_path, company_names):
        self.file_path = file_path
        self.company_names = company_names
        self.companies = []
    
    def get_CRSP_company(self):
        raw_data = pd.read_csv(self.file_path, parse_dates=["date"],low_memory=False)
        for company_name in self.company_names:
            df = raw_data[raw_data['TICKER'] == company_name]
            df = df.drop_duplicates(subset='date') # remove duplicate rows, it is not common but happens
            company = CRSP_Company(company_name, df)
            self.companies.append(company)
    
    def add_predictors(self):
        for company in self.companies:
            company.replace_char_with_zero("RET")
            company.add_volumn_change()
            company.add_BA_Spread()
            company.add_Illiquidity()
            company.add_TurnOver()
        print("finished adding predictors")
    
    def add_DJI_return(self, DJI_file_path):
        DJI = pd.read_csv(DJI_file_path)
        DJI['date'] = pd.to_datetime(DJI['date'], format="mixed")
        for company in self.companies:
            company.join_by_date(DJI, "DJI_Return")
    
    def select_columns(self, list_columns):
        for company in self.companies:
            company.select_columns(list_columns)
    
    def remove_nan(self):
        for company in self.companies:
            company.remove_nan()

    def save_raw_data(self, root_path):
        for company in self.companies:
            company.save_raw_data(root_path)

    def split_train_validation_test(self, train_start, train_end, validation_start, validation_end, test_start, test_end):
        for company in self.companies:
            company.split_train_validation_test(train_start, train_end, validation_start, validation_end, test_start, test_end)

    def save_to_csv(self, root_path):
        for company in self.companies:
            company.save_to_csv(root_path)