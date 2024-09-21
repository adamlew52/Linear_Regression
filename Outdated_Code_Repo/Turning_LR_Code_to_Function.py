import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Folder containing CSV files (replace 'your_folder_path' with the actual path)
folder_path = '/Users/adam/Documents/GitHub/Linear_Regression/Training_Data'

# Get a list of all CSV files in the folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Loop through each CSV file
for csv_file in csv_files:
    # Construct the full file path
    file_path = os.path.join(folder_path, csv_file)
    
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    
    # Convert the 'Datetime' column to datetime format if it exists
    if 'Datetime' in df.columns:
        df['Datetime'] = pd.to_datetime(df['Datetime'])
    
    
    # Feature Engineering: Extract useful datetime features (e.g., day of the week, month)
    if 'Datetime' in df.columns:
        df['Day_of_Week'] = df['Datetime'].dt.dayofweek
        df['Month'] = df['Datetime'].dt.month
        df['Year'] = df['Datetime'].dt.year
    
    # Feature Engineering: Calculate daily returns (optional)
    if 'Adj Close' in df.columns:
        df['Daily_Return'] = df['Adj Close'].pct_change()
    
    # Drop rows with missing values generated from pct_change() or other transformations
    df = df.dropna()
    
    # Features: Select relevant columns for prediction
    if set(['Open', 'High', 'Low', 'Close', 'Volume', 'Day_of_Week', 'Month', 'Year', 'Daily_Return']).issubset(df.columns):
        X = df[['Open', 'High', 'Low', 'Close', 'Volume', 'Day_of_Week', 'Month', 'Year', 'Daily_Return']]
    
        # Target: For instance, predicting 'Next Day Close' (shift the 'Close' column by -1)
        df['Next_Day_Close'] = df['Close'].shift(-1)
        y = df['Next_Day_Close'].dropna()
    
        # Align the features (X) with the target (y) by dropping the last row in X
        X = X.iloc[:-1]
    
        # Split the data into training and testing sets, ensuring chronological order
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    
        # Initialize the Linear Regression model
        model = LinearRegression()
    
        # Train the model on the training data
        model.fit(X_train, y_train)
    
        # Make predictions on the test data
        y_pred = model.predict(X_test)
    
        # Evaluate the model's performance
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
    
        # Print the results for the current CSV file
        print(f"Results for {csv_file}:")
        print("Mean Squared Error:", mse)
        print("R-squared:", r2)
        print("Slope (Coefficient):", model.coef_)
        print("Intercept:", model.intercept_)
        print("-" * 50)
    
        # Optional: Visualize the actual vs. predicted values
        plt.plot(y_test.values, label='Actual', color='blue')
        plt.plot(y_pred, label='Predicted', color='red')
        plt.title(f'Actual vs Predicted Closing Prices for {csv_file}')
        plt.legend()
        plt.show()
    else:
        print(f"Skipping {csv_file} due to missing required columns.")
