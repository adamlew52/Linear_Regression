# Import necessary libraries
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Example dataset (replace with your own data) 
# Creating a simple dataset with one feature and a target variable
data = { #dict
    'Feature': [1, 2, 3, 4, 5],
    'Target': [2, 4, 6, 8, 10],
    #'Date':,
    #'Open',
    #'High',
    #'Low',
    #'Close',
    #'Adj_Close',
    #'Volume'
}

#print(type(data))

# Convert the dictionary to a DataFrame
df = pd.DataFrame(data)

# Split the data into input features (X) and target variable (y)
X = df[['Feature']]  # Features should be in 2D (even if it's one feature)
y = df['Target']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Linear Regression model
model = LinearRegression()

# Train the model on the training data
model.fit(X_train, y_train)

# Make predictions on the test data
y_pred = model.predict(X_test)

# Evaluate the model's performance
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Output the results
print("Mean Squared Error:", mse)
print("R-squared:", r2)

# Get the coefficients (slope) and intercept (y-intercept) of the linear regression line
print("Slope (Coefficient):", model.coef_)
print("Intercept:", model.intercept_)

# Optional: Visualize the regression line (for 1D data)
#import matplotlib.pyplot as plt

def Visualization_of_Regression_Line():
    plt.scatter(X_test, y_test, color='blue', label='Actual')
    plt.plot(X_test, y_pred, color='red', label='Predicted')
    plt.xlabel('Feature')
    plt.ylabel('Target')
    plt.title('Linear Regression')
    plt.legend()
    plt.show()

#Visualization_of_Regression_Line()