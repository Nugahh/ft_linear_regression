import json

def estimate_price(mileage, theta0, theta1):
    return theta0 + theta1 * mileage

# Load trained model
with open('model.json', 'r') as f:
    model = json.load(f)
    theta0 = model['theta0']
    theta1 = model['theta1']
    max_prices = model['max_prices']
    
# Ask user for mileage input
try:
    mileage_input = float(input("Enter the mileage of the car: "))
    normalized = mileage_input / model['max_mileage']
    predicted_price = estimate_price(normalized, theta0, theta1)
    actual_price = predicted_price * max_prices
    print("max")
    print(f"Estimated price: {actual_price:.2f}")
except ValueError:
    print("Please enter a valid number.")

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data.csv')
plt.scatter(df['km'], df['price'])
plt.xlabel('km')
plt.ylabel('Price')
plt.title('Mileage vs. Price')
plt.show()

plt.scatter(mileages, prices, color='blue', label='Actual data')
plt.xlabel('Mileage (km)')
plt.ylabel('Price (€)')
plt.title('Mileage vs Price')
plt.legend()
plt.grid(True)
plt.show()