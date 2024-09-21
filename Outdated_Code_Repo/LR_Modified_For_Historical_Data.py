import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import os
from sklearn.impute import SimpleImputer
from scipy import stats


# Load your financial dataset (replace 'your_data.csv' with your actual file path)
def load_and_combine_data(file_paths):
    combined_df = pd.DataFrame()
    
    for file_path in file_paths:
        df = pd.read_csv(file_path)
        
        # Ensure necessary columns are present
        required_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Dividends', 'Stock Splits']
        for col in required_columns:
            if col not in df.columns:
                raise KeyError(f"Column '{col}' not found in the DataFrame from file: {file_path}")

        # Add a column indicating the source of the data
        df['Source_File'] = os.path.basename(file_path)
        
        # Append the data to the combined DataFrame
        combined_df = pd.concat([combined_df, df], ignore_index=True)
    
    return combined_df

def perform_linear_regression_on_combined_data(df):
    # Prepare the data
    features = df[['Open', 'High', 'Low', 'Volume']]
    target = df['Close']
    
    # Impute missing values
    imputer = SimpleImputer(strategy='mean')
    features_imputed = imputer.fit_transform(features)
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features_imputed, target, test_size=0.3, random_state=42)

    # Create and train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error: {mse}")

    # Print model coefficients
    print("Model Coefficients:", model.coef_)
    print("Model Intercept:", model.intercept_)

    # Plotting predictions vs actual values
    Visualize.Plot_Line(y_test,y_pred)

class Visualize:
    def Plot_Line(y_test,y_pred):
        # Optional: Visualize the actual vs. predicted values
        plt.plot(y_test.values, label='Actual', color='blue')
        plt.plot(y_pred, label='Predicted', color='red')
        plt.title('Actual vs Predicted Closing Prices')
        plt.legend()
        plt.show()

    def Plot_Scatter(y_test,y_pred):
        plt.figure(figsize=(10, 6))
        plt.scatter(y_test, y_pred, color='blue', alpha=0.5, label='Predictions vs Actual')
        plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--', label='Perfect Fit')
        plt.xlabel('Actual Close Prices')
        plt.ylabel('Predicted Close Prices')
        plt.title('Linear Regression: Predictions vs Actual Values')
        plt.legend()
        plt.show()
    
    def Scatter_and_Line(y_test,y_pred):
        plt.figure(figsize=(10, 6))
        plt.plot(y_test.values, label='Actual', color='blue')
        plt.plot(y_pred, label='Predicted', color='red')
        plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--', label='Perfect Fit')
        plt.scatter(y_test, y_pred, color='blue', alpha=0.5, label='Predictions vs Actual')
        
        
        plt.xlabel('Actual Close Prices')
        plt.ylabel('Predicted Close Prices')
        
        plt.title('Linear Regression: Predictions vs Actual Values')
        plt.legend()
        plt.show()



DataSet_Location = '/Users/adam/Documents/GitHub/Linear_Regression/Data_Collection/Storage_Location/1y_at_1d/2024-08-18/GOOGL_Data_1y_at_1d.csv'

# List of CSV file paths
csv_files = [
    '/Users/adam/Documents/GitHub/Linear_Regression/Data_Collection/Storage_Location/1y_at_1d/2024-08-18/KO_Data_1y_at_1d.csv',
    '/Users/adam/Documents/GitHub/Linear_Regression/Data_Collection/Storage_Location/1y_at_1d/2024-08-18/GOOGL_Data_1y_at_1d.csv',
    '/Users/adam/Documents/GitHub/Linear_Regression/Data_Collection/Storage_Location/1y_at_1d/2024-08-18/MSFT_Data_1y_at_1d.csv',
    '/Users/adam/Documents/GitHub/Linear_Regression/Data_Collection/Storage_Location/1y_at_1d/2024-08-18/TSLA_Data_1y_at_1d.csv'
]

# Load and combine data
#combined_df = load_and_combine_data(csv_files)

# Example usage

df = pd.read_csv(csv_files[0])
#df = df.dropna()  # clean up the data
#df = df[(np.abs(stats.zscore(df['column_name'])) < 3)]

perform_linear_regression_on_combined_data(df)

# Perform linear regression on the combined data
#perform_linear_regression_on_combined_data(combined_df)
