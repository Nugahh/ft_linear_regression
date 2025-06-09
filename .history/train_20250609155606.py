import pandas as pd

df = pd.read_csv('data.csv')
mileages = df['mileage'].tolist()
prices = df['price'].tolist()
print(df)