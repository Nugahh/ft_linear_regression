import pandas as pd
import json

def load_and_normalize_data(csv_file):
    """Load data from CSV and normalize features"""
    try:
        df = pd.read_csv(csv_file)
        if 'km' not in df.columns or 'price' not in df.columns:
            raise ValueError("CSV must contain 'km' and 'price' columns.")
        
        mileages = df['km'].tolist()
        prices = df['price'].tolist()
        
        # Store original max values for denormalization
        max_mileage = max(mileages)
        max_prices = max(prices)
        
        # Normalize to [0, 1] range
        normalized_mileages = [m / max_mileage for m in mileages]
        normalized_prices = [p / max_prices for p in prices]
        
        print(f"Data loaded: {len(mileages)} samples")
        print(f"Mileage range: {min(mileages):,.0f} - {max(mileages):,.0f} km")
        print(f"Price range: €{min(prices):,.0f} - €{max(prices):,.0f}")
        
        return normalized_mileages, normalized_prices, max_mileage, max_prices
        
    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None, None, None

def estimate_price(mileage, theta0, theta1):
    """Linear regression prediction function"""
    return theta0 + theta1 * mileage

def train_model(mileages, prices, learning_rate=0.01, epochs=100000, verbose=True):
    """Train linear regression model using gradient descent"""
    theta0 = 0.0
    theta1 = 0.0
    n_samples = len(mileages)
    
    print(f"Starting training with {epochs} epochs, learning rate: {learning_rate}")
    
    for epoch in range(epochs):
        sum_error0 = 0
        sum_error1 = 0
        
        # Calculate gradients
        for i in range(n_samples):
            prediction = estimate_price(mileages[i], theta0, theta1)
            error = prediction - prices[i]
            sum_error0 += error
            sum_error1 += error * mileages[i]
        
        # Update parameters
        tmp_theta0 = (learning_rate * sum_error0) / n_samples
        tmp_theta1 = (learning_rate * sum_error1) / n_samples
        theta0 -= tmp_theta0
        theta1 -= tmp_theta1
        
        # Debug output for first epoch
        if epoch == 0 and verbose:
            print(f"\nFirst epoch details:")
            print(f"  sum_error0 = {sum_error0:.6f}")
            print(f"  sum_error1 = {sum_error1:.6f}")
            print(f"  tmp_theta0 = {tmp_theta0:.6f}")
            print(f"  tmp_theta1 = {tmp_theta1:.6f}")
            print(f"  theta0 = {theta0:.6f}")
            print(f"  theta1 = {theta1:.6f}")
        
        # Progress updates
        if verbose and epoch % 10 == 0:
            print(f"Epoch {epoch:6d}: theta0 = {theta0:.6f}, theta1 = {theta1:.6f}")
    
    print(f"\nTraining completed!")
    print(f"Final parameters: theta0 = {theta0:.6f}, theta1 = {theta1:.6f}")
    
    return theta0, theta1

def save_model(theta0, theta1, max_mileage, max_prices, filename='model.json'):
    """Save trained model parameters to JSON file"""
    model_data = {
        'theta0': theta0,
        'theta1': theta1,
        'max_mileage': max_mileage,
        'max_prices': max_prices
    }
    
    try:
        with open(filename, 'w') as f:
            json.dump(model_data, f, indent=2)
        print(f"Model saved to '{filename}'")
    except Exception as e:
        print(f"Error saving model: {e}")

def calculate_cost(mileages, prices, theta0, theta1):
    """Calculate mean squared error cost"""
    total_error = 0
    n_samples = len(mileages)
    
    for i in range(n_samples):
        prediction = estimate_price(mileages[i], theta0, theta1)
        error = prediction - prices[i]
        total_error += error ** 2
    
    return total_error / (2 * n_samples)

def main():
    """Main training function"""
    print("=== LINEAR REGRESSION TRAINING ===")
    
    # Load and normalize data
    mileages, prices, max_mileage, max_prices = load_and_normalize_data('data.csv')
    if mileages is None:
        return
    
    # Train the model
    theta0, theta1 = train_model(
        mileages, 
        prices, 
        learning_rate=1,
        epochs=1000, 
        verbose=True
    )
    
    # Calculate final cost
    final_cost = calculate_cost(mileages, prices, theta0, theta1)
    print(f"Final training cost: {final_cost:.6f}")
    
    # Save the model
    save_model(theta0, theta1, max_mileage, max_prices)
    
    print("\nTraining process completed successfully!")

if __name__ == "__main__":
    main()