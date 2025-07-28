import json
import pandas as pd
import matplotlib.pyplot as plt

def estimate_price(mileage, theta0, theta1):
    return theta0 + theta1 * mileage

def r_squared(y_true, y_pred):
    """Calculate the precision of an algorithm"""
    # mean (average) value of all prices
    mean_y = sum(y_true) / len(y_true)
    # Total variance in the data.
    ss_total = sum((y - mean_y) ** 2 for y in y_true)
    # Measures how far your predictions are from the real values. (res for residuals)
    ss_res = sum((y_true[i] - y_pred[i]) ** 2 for i in range(len(y_true)))
    return 1 - (ss_res / ss_total)

def plot_regression(df, theta0, theta1, max_mileage, max_prices):
    """Plot the regression line and actual data points"""
    try:
        # Plotting the regression line
        x_vals = list(range(0, int(max_mileage) + 1, 1000))
        y_vals = [estimate_price(x / max_mileage, theta0, theta1) * max_prices for x in x_vals]
        
        # data points
        plt.scatter(df['km'], df['price'], color='blue', label='Actual data')
        # linear regression line
        plt.plot(x_vals, y_vals, color='red', label='Regression line')
        # add labels, title, legend and grid
        plt.xlabel('Mileage (km)')
        plt.ylabel('Price (€)')
        plt.title('Linear Regression Result')
        plt.legend()
        plt.grid(True)
        
        plt.savefig('regression_plot.png')
        plt.show()
        print("Plot saved as 'regression_plot.png' and displayed.")
    except Exception as e:
        print(f"Error while plotting: {e}")

def calculate_precision(df, theta0, theta1, max_mileage, max_prices):
    """Calculate and display the R² score and precision quality"""
    try:
        # Calculate R² score
        mileages_norm = [m / max_mileage for m in df['km'].tolist()]
        predictions = [(theta0 + theta1 * m) * max_prices for m in mileages_norm]
        score = r_squared(df['price'].tolist(), predictions)
        print(f"R² score: {score:.4f}")
        
        # Print quality scale
        if score >= 0.9:
            print("Precision: Excellent")
        elif score >= 0.8:
            print("Precision: Good")
        elif score >= 0.7:
            print("Precision: Fair")
        elif score >= 0.5:
            print("Precision: Poor")
        else:
            print("Precision: Very Poor")
        
        return score
    except Exception as e:
        print(f"Error calculating R² score: {e}")
        return None

def predict_price():
    """Main function to load model and data"""
    try:
        # Load model parameters
        with open('model.json', 'r') as f:
            model = json.load(f)
        theta0 = model['theta0']
        theta1 = model['theta1']
        max_mileage = model['max_mileage']
        max_prices = model['max_prices']
        print("Model loaded successfully.")
    except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
        print(f"Error loading model: {e}")
        return
    
    try:
        # Load dataset
        df = pd.read_csv('data.csv')
        if 'km' not in df.columns or 'price' not in df.columns:
            raise ValueError("CSV must contain 'km' and 'price' columns.")
        print("Dataset loaded successfully.")
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return
    
    # Core functionality: Get mileage input and predict price
    print("\n=== PRICE PREDICTION ===")
    while True:
        try:
            mileage_input = input("Enter the mileage (km) to estimate price: ").strip()
            mileage = float(mileage_input)
            if mileage < 0:
                print("Please enter a positive mileage value.")
                continue
            break
        except ValueError:
            print("Please enter a valid number for mileage.")
    
    # Normalize mileage and calculate prediction
    normalized_mileage = mileage / max_mileage
    predicted_price_normalized = estimate_price(normalized_mileage, theta0, theta1)
    predicted_price = predicted_price_normalized * max_prices
    
    print(f"\nEstimated price for {mileage:,.0f} km: {predicted_price:,.2f}€")
    
    # Ask user if they want to execute bonus parts
    print("\nBonus features available:")
    print("1. Plot regression graph")
    print("2. Calculate precision (R² score)")
    
    while True:
        choice = input("\nDo you want to execute bonus features? (y/n): ").lower().strip()
        if choice in ['y', 'yes']:
            execute_bonus = True
            break
        elif choice in ['n', 'no']:
            execute_bonus = False
            break
        else:
            print("Please enter 'y' for yes or 'n' for no.")
    
    if execute_bonus:
        print("\nExecuting bonus features...")
        
        # Ask which bonus features to execute
        while True:
            bonus_choice = input("Which bonus feature? (1: plot, 2: precision, 3: both): ").strip()
            if bonus_choice == '1':
                plot_regression(df, theta0, theta1, max_mileage, max_prices)
                break
            elif bonus_choice == '2':
                calculate_precision(df, theta0, theta1, max_mileage, max_prices)
                break
            elif bonus_choice == '3':
                plot_regression(df, theta0, theta1, max_mileage, max_prices)
                calculate_precision(df, theta0, theta1, max_mileage, max_prices)
                break
            else:
                print("Please enter 1, 2, or 3.")
    else:
        print("Skipping bonus features.")
    
    print("Program completed.")

if __name__ == "__main__":
    predict_price()