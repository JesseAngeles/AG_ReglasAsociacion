import json
import pandas as pd

df = pd.read_csv("./data/dataset.csv")
df_len = len(df)

with open("./data/memory.json", "r") as f:
    data = json.load(f)
memory = {
    frozenset(tuple(item) for item in json.loads(key)): value
    for key, value in data.items()
}
epsilon = 1e-10

def save_memory():
    serializable = {}

    for key, value in memory.items():
        # Convertir llave (frozenset) → lista → string
        key_str = json.dumps([list(t) for t in key])

        # Convertir valor numpy.int64 → int
        serializable[key_str] = int(value)

    with open("./data/memory.json", "w") as f:
        json.dump(serializable, f, indent=4)

def intersection_count(X):
    key = frozenset(tuple(item) for item in X)
    
    if key in memory:
        return memory[key]
    
    
    mask = pd.Series([True] * df_len)
    for col, val in X:
        mask &= (df[col] == val)
        
    count = mask.sum()
    memory[key] = count
    
    return count
