import pandas as pd
import json

df = pd.read_csv("./data/diabetes_clean_dataset.csv")

mappings = {}

for column in df.columns:
    unique_vals = df[column].unique()
    mapping = {str(val): int(i) + 1 for i, val in enumerate(unique_vals)}
    
    mappings[column] = mapping
    df[column] = df[column].map(lambda x: mapping[str(x)])

df.to_csv("./data/dataset.csv", index=False)

with open("./data/dataset_mappings.json", "w") as f:
    json.dump(mappings, f, indent=4)