import pandas as pd
import json

df = pd.read_csv('data.csv')
mileages = df['km'].tolist()
prices = df['price'].tolist()
max_prices = max(prices)
prices = [p / max_prices for p in prices]
max_mileage = max(mileages)
mileages = [m / max_mileage for m in mileages]
print(mileages)

def estimate_price(mileage, theta0, theta1):
	return theta0 + theta1 * mileage

learning_rate = 0.01

theta0 = 0
theta1 = 0

for epoch in range(100000):  # run many steps
    sum_error0 = 0
    sum_error1 = 0

    for i in range(len(mileages)):
        prediction = estimate_price(mileages[i], theta0, theta1)
        error = prediction - prices[i]

        sum_error0 += error
        sum_error1 += error * mileages[i]

    tmp_theta0 = (learning_rate * sum_error0) / len(mileages)
    tmp_theta1 = (learning_rate * sum_error1) / len(mileages)

    theta0 -= tmp_theta0
    theta1 -= tmp_theta1
    if epoch == 0:
        print(f"sum_error0 = {sum_error0}")
        print(f"sum_error1 = {sum_error1}")
        print(f"tmp_theta0 = {tmp_theta0}")
        print(f"tmp_theta1 = {tmp_theta1}")
        print(f"theta0 = {theta0}")
        print(f"theta1 = {theta1}")
        
    if epoch % 1000 == 0:
        print(f"Epoch {epoch}: theta0 = {theta0}, theta1 = {theta1}")

with open('model.json', 'w') as f:
	json.dump({'theta0': theta0, 'theta1': theta1, 'max_mileage': max_mileage, 'max_prices': max_prices}, f)
      
print(f"Final model: theta0 = {theta0}, theta1 = {theta1}")