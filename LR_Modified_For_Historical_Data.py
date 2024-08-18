import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Load your financial dataset (replace 'your_data.csv' with your actual file path)
def Use_All_Data():
    

DataSet_Location = '/Users/adam/Documents/GitHub/Linear_Regression/Training_Data/GOOGL_Historical_Data.csv'
df = pd.read_csv(DataSet_Location)

# Convert the 'Datetime' column to datetime format
df['Datetime'] = pd.to_datetime(df['Datetime'])

# Feature Engineering: Extract useful datetime features (e.g., day of the week, month)
df['Day_of_Week'] = df['Datetime'].dt.dayofweek
df['Month'] = df['Datetime'].dt.month
df['Year'] = df['Datetime'].dt.year

# Feature Engineering: Calculate daily returns (optional)
df['Daily_Return'] = df['Adj Close'].pct_change()

# Drop rows with missing values generated from pct_change()
df = df.dropna()

# Features: Select relevant columns for prediction
# You can include 'Day_of_Week', 'Month', etc., along with price and volume data
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

print("Mean Squared Error:", mse)
print("R-squared:", r2)
print("Slope (Coefficient):", model.coef_)
print("Intercept:", model.intercept_)


class Visualize:
    def Plot():
        # Optional: Visualize the actual vs. predicted values
        plt.plot(y_test.values, label='Actual', color='blue')
        plt.plot(y_pred, label='Predicted', color='red')
        plt.title('Actual vs Predicted Closing Prices')
        plt.legend()
        plt.show()

Visualize.Plot()