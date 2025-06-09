import pandas as pd

df = pd.read_csv('data.csv')
mileages = df['km'].tolist()
prices = df['price'].tolist()
print(mileages)

def estimate_price(mileage, theta0, theta1):
	return theta0 + theta1 * mileage

theta0 = 0
theta1 = 0

total_error = 0
m = len(mileages)

for i in range(m):
    prediction = estimate_price(mileages[i], theta0, theta1)
    error = prediction - prices[i]
    print(f"Predicted price for {mileages[i]} km: {prediction}, Actual price: {prices[i]}, Error: {error}")
    total_error += error ** 2

print("Total error:", total_error)
