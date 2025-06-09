import json

def estimate_price(mileage, theta0, theta1):
    return theta0 + theta1 * mileage

# Load trained model
with open('model.json', 'r') as f:
    model = json.load(f)
    theta0 = model['theta0']
    theta1 = model['theta1']
    max_mileage = model['max_mileage']
# Ask user for mileage input
try:
    mileage_input = float(input("Enter the mileage of the car: "))
    normalized = mileage_input / max_mileage
    predicted_price = estimate_price(mileage_input, theta0, theta1)
    print(f"Estimated price: {predicted_price:.2f}")
except ValueError:
    print("Please enter a valid number.")

# import pandas as pd
# import matplotlib.pyplot as plt

# df = pd.read_csv('data.csv')
# plt.scatter(df['km'], df['price'])
# plt.xlabel('Mileage')
# plt.ylabel('Price')
# plt.title('Mileage vs. Price')
# plt.show()
