import pandas as pd


ticker = 'T'
row_count = 250
# Step 1: Read the file
# df = pd.read_csv('/Users/zimenglyu/Documents/datasets/CRSP/Honeywell.csv', parse_dates=["date"],low_memory=False)
# # df = pd.read_csv('/Users/zimenglyu/Documents/datasets/CRSP/chevron_corporation_old.csv', parse_dates=["date"],low_memory=False)
# # df = pd.read_csv('/Users/zimenglyu/Documents/datasets/CRSP/PhilipMorris_old.csv', parse_dates=["date"],low_memory=False)
# # df = pd.read_csv('/Users/zimenglyu/Documents/datasets/CRSP/DWDP.csv', parse_dates=["date"],low_memory=False)
# df = pd.read_csv('/Users/zimenglyu/Documents/datasets/CRSP/EK+XON+Z_old.csv', parse_dates=["date"],low_memory=False)
# df = pd.read_csv('/Users/zimenglyu/Documents/datasets/CRSP/dji_2.csv', parse_dates=["date"],low_memory=False)
# df = pd.read_csv('/Users/zimenglyu/Documents/datasets/CRSP/HWP.csv', parse_dates=["date"],low_memory=False)
df = pd.read_csv('/Users/zimenglyu/Documents/datasets/CRSP/DJI_Company.csv', parse_dates=["date"],low_memory=False)
for ticker in ['AAPL', 'AXP', 'BA', 'CAT', 'CSCO', 'CVX', 'DOW', 'DIS', 'WBA', 'GS', 'HD', 'IBM', 'INTC', 'JNJ', 'JPM', 'KO', 'MCD', 'MMM', 'MRK', 'MSFT', 'NKE', 'HON', 'PG', 'TRV', 'UNH', 'AMGN', 'VZ', 'V', 'WMT', 'CRM']:
# for ticker in [ 'JNJ', 'WMT', 'HD', 'INTC', 'MSFT', 'AAPL', 'UNH', 'VZ','CVX', 'CSCO', 'TRV', 'GS','NKE', 'V', 'WBA','DOW','AMGN','CRM']:
# for ticker in ['XOM']:
# for ticker in ['HON']:
# for ticker in ['DWDP']:
    # Step 2: Find rows where "ticker" equals "T"
    df_filtered = df[df['TICKER'] == ticker]

    # Step 3: Select data within a date range
    # Ensure the 'date' column is in datetime format
    # df_filtered['date'] = pd.to_datetime(df_filtered['date'])
    start_date = '1990-01-01'  # Start of your date range
    end_date = '2023-12-30'    # End of your date range
    df_date_filtered = df_filtered[(df_filtered['date'] >= start_date) & (df_filtered['date'] < end_date)]
    len_rows = len(df_date_filtered)
    # print('file {} len of rows is {}'.format(ticker, len_rows))
    # if len_rows != row_count:
        # print('file {} len of rows is {} not equal to {}'.format(ticker, len_rows, row_count))
    print('file {} len of rows is {} '.format(ticker, len_rows))
        # if len_rows > row_count:
        #     # Finding duplicate rows based on column 'A'
        #     duplicates = df_date_filtered.duplicated(subset='date', keep=False)
        #     # Selecting the duplicate rows
        #     duplicate_rows = df_date_filtered[duplicates]
        #     print(duplicate_rows)
    # Step 4: Save to a new file
    df_date_filtered.to_csv('/Users/zimenglyu/Documents/datasets/CRSP/DJI_company/{}.csv'.format(ticker), index=False)
