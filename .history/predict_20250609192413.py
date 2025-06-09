import json
import pandas as pd
import matplotlib.pyplot as plt

def estimate_price(mileage, theta0, theta1):
    return theta0 + theta1 * mileage

# Load trained model
with open('model.json', 'r') as f:
    model = json.load(f)
    theta0 = model['theta0']
    theta1 = model['theta1']
    max_mileage = model['max_mileage']
    max_prices = model['max_prices']
    
# # Ask user for mileage input
# try:
#     mileage_input = float(input("Enter the mileage of the car: "))
#     normalized = mileage_input / model['max_mileage']
#     predicted_price = estimate_price(normalized, theta0, theta1)
#     actual_price = predicted_price * max_prices
#     print(f"Estimated price: {actual_price:.2f}")
# except ValueError:
#     print("Please enter a valid number.")

# # Plotting the data
df = pd.read_csv('data.csv')
# plt.scatter(df['km'], df['price'])
# plt.xlabel('km')
# plt.ylabel('price (€)')
# plt.title('Mileage vs. Price')
# plt.show()

# Plotting the regression line
# Predict prices for 0 → max mileage
x_vals = list(range(0, int(max_mileage) + 1, 1000))
print(f"x_vals: {x_vals}")
x_norm = [x / max_mileage for x in x_vals]
y_vals = [estimate_price(x / max_mileage, theta0, theta1) * max_prices for x in df['km'],]

# Plot
plt.scatter(df['km'], df['price'], color='blue', label='Actual data')
plt.plot(x_vals, y_vals, color='red', label='Regression line')
plt.xlabel('Mileage (km)')
plt.ylabel('Price (€)')
plt.title('Linear Regression Result')
plt.legend()
plt.grid(True)
plt.savefig('regression_plot.png')

def r_squared(y_true, y_pred):
    mean_y = sum(y_true) / len(y_true)
    ss_total = sum((y - mean_y) ** 2 for y in y_true)
    ss_res = sum((y_true[i] - y_pred[i]) ** 2 for i in range(len(y_true)))
    return 1 - (ss_res / ss_total)

# Recalculate predictions
mileages_norm = [m / max_mileage for m in x_vals]
predictions = [theta0 + theta1 * m for m in mileages_norm]

# Calculate R²
score = r_squared(y_vals, predictions)
print(f"R² score: {score:.4f}")
