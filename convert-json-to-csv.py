import pandas as pd

df = pd.read_json(r'vn_12_12.json')
df.to_csv(r'vn_12_12.csv')
