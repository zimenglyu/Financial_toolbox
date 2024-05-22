import pandas as pd

dataset = "DJI_company_2022"
test_path = f"/Users/zimenglyu/Documents/datasets/CRSP/{dataset}/test"
prediction_path = f"/Users/zimenglyu/Documents/cluster_results/{dataset}_lr_prediction"

company_list = ['AAPL', 'AMZN', 'AXP', 'BA', 'CAT', 'CRM', 'CSCO', 'CVX', 'DIS', 'DOW', 'GS', 'HD', 'HON', 'IBM', 'INTC', 'JNJ', 'JPM', 'KO', 'MCD', 'MMM', 'MRK', 'MSFT', 'NKE', 'PG', 'TRV', 'UNH', 'V', 'VZ', 'WBA', 'WMT']

merged = pd.DataFrame()
for company in company_list:
    test = pd.read_csv(f"{test_path}/{company}.csv")
    prediction = pd.read_csv(f"{prediction_path}/{company}_predictions.csv")
    merged[f"{company}_predicted_RET"] = prediction["predicted_RET"]
    merged[f"{company}_expected_RET"] = prediction["expected_RET"]
    merged[f"{company}_price"] = test["PRC"]

merged.to_csv(f"/Users/zimenglyu/Documents/cluster_results/{dataset}_stock_price_return.csv")
