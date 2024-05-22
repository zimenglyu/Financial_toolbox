import pandas as pd
from CRSP_Company import CRSP_Company
class CRSP_Dataset:
    def __init__(self, file_path, company_tickers):
        self.file_path = file_path
        self.company_tickers = company_tickers
        self.companies = []
    
    def get_CRSP_company(self):
        raw_data = pd.read_csv(self.file_path, parse_dates=["date"],low_memory=False)
        raw_data['CUSIP'] = raw_data['CUSIP'].astype(str)
        raw_data['TICKER'] = raw_data['TICKER'].astype(str)
        for ticker in  (self.company_tickers):
            # print("company name: {}, ticker: {}".format(name, ticker))
            df = raw_data[raw_data['TICKER'] == ticker]
            # df = raw_data[raw_data['COMNAM'] == name]
            df = df.drop_duplicates(subset='date') # remove duplicate rows, it is not common but happens
            # if (ticker == 'DOW'):
            #     df = df[df['CUSIP'] == '26054310']
            if(ticker == 'GS'):
                df = df[df['CUSIP'] == '38141G10']
            elif(ticker == 'HON'):
                df = df[df['CUSIP'] == '43851610']
            elif(ticker == 'JPM'):
                df = df[df['CUSIP'] == '46625H10']
            elif(ticker == 'TRV'):
                df = df[df['CUSIP'] == '89417E10']
            elif(ticker == 'V'):
                df = df[df['CUSIP'] == '92826C83']
            elif(ticker == 'CRM'):
                df = df[df['CUSIP'] == '79466L30']
            df = df.sort_values(by='date')
            company = CRSP_Company(ticker, df)
            self.companies.append(company)
    
    def add_predictors(self):
        for company in self.companies:
            company.replace_char_with_zero("RET")
            company.add_volumn_change()
            company.add_BA_Spread()
            company.add_Illiquidity()
            company.add_TurnOver()
            company.add_Transaction_Cost()
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