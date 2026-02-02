import os
from pathlib import Path
import pandas as pd

dataset = "DJI_company_2022"
repo_root = Path(__file__).resolve().parents[1]
datasets_root = Path(os.getenv("FIN_DATASETS_DIR", repo_root / "datasets"))
results_root = Path(os.getenv("FIN_RESULTS_DIR", repo_root / "results"))

test_path = datasets_root / "CRSP" / dataset / "test"
prediction_path = results_root / f"{dataset}_lr_prediction"

company_list = ['AAPL', 'AMZN', 'AXP', 'BA', 'CAT', 'CRM', 'CSCO', 'CVX', 'DIS', 'DOW', 'GS', 'HD', 'HON', 'IBM', 'INTC', 'JNJ', 'JPM', 'KO', 'MCD', 'MMM', 'MRK', 'MSFT', 'NKE', 'PG', 'TRV', 'UNH', 'V', 'VZ', 'WBA', 'WMT']

merged = pd.DataFrame()
for company in company_list:
    test = pd.read_csv(test_path / f"{company}.csv")
    prediction = pd.read_csv(prediction_path / f"{company}_predictions.csv")
    merged[f"{company}_predicted_RET"] = prediction["predicted_RET"]
    merged[f"{company}_expected_RET"] = prediction["expected_RET"]
    merged[f"{company}_price"] = test["PRC"]

merged.to_csv(results_root / f"{dataset}_stock_price_return.csv")
