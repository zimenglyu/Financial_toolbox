import pandas as pd
from glob import glob

prediction_path = "/Users/zimenglyu/Documents/cluster_results/DJI_Company_2023_lr_prediction"

files = glob(prediction_path + "/*.csv")
total_correct = 0
total = 0
for file in files:
    expected = pd.read_csv(file, usecols=['expected_RET']).to_numpy().flatten()
    predicted = pd.read_csv(file, usecols=['predicted_RET']).to_numpy().flatten()
    num_correct = sum([1 for i in range(len(expected)) if expected[i] * predicted[i] > 0])
    acc = num_correct / len(expected)
    total_correct += num_correct
    total += len(expected)
    print(f"Accuracy for {file}: {acc}")
print(f"Total accuracy: {total_correct / total}")