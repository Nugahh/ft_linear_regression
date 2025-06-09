import pandas as pd

df = pd.read_csv('data.csv')
mileages = df['km'].tolist()
prices = df['price'].tolist()
print(mileages)

def estimate_price(mileage, theta0, theta1):
	return theta0 + theta1 * mileage

theta = 0
theta1 = 0

total_error = 0