import os
from pathlib import Path
import pandas as pd

company_tickers = ['AAPL', 'AXP', 'BA', 'CAT', 'CSCO', 'CVX', 'DOW', 'DIS', 'WBA', 'GS', 'HD', 'IBM', 'INTC', 'JNJ', 'JPM', 'KO', 'MCD', 'MMM', 'MRK', 'MSFT', 'NKE', 'HON', 'PG', 'TRV', 'UNH', 'AMZN', 'VZ', 'V', 'WMT', 'CRM']
print(len(company_tickers))
repo_root = Path(__file__).resolve().parents[1]
datasets_root = Path(os.getenv("FIN_DATASETS_DIR", repo_root / "datasets"))
file_name = datasets_root / "CRSP" / "DJI_company.csv"
company_names = []
data = pd.read_csv(file_name)
for ticker in company_tickers:
    
    company_name = data[data['TICKER'] == ticker]
    company_name = company_name.drop_duplicates(subset=['CUSIP']) 
    print("company ticker: {}".format(ticker))
    print("company IP: {}".format(company_name['CUSIP'].values))
    print("company name: {}".format(company_name['COMNAM'].values))
    # company_names.append(company_name['CUSIP'].iloc[0])
print(company_names)
print(len(company_names))
