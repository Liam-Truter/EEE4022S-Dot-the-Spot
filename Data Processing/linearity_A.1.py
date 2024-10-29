import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression

# Data for kitchen scale and designed scale
kitchen_weights = np.array([0,23,45,64,67,74,80,96,101,103,106,119,133,200,266])
scale_weights = np.array([0,23.6,44.7,63.4,66.3,73.2,79.5,95.0,100.0,103.1,105.5,118.1,132.8,199.5,265.9])

# Data for bearings
bearings = [0,1,2,3,4]
bearing_weights_theroetical = np.array([0,66.5,133,199.5,266])
bearing_weights_measured = np.array([0,66.3,132.8,199.5,265.9])

# Calculate errors
scale_errors = scale_weights - kitchen_weights
bearing_errors = bearing_weights_measured - bearing_weights_theroetical

# RMSE for scale and bearing methods
scale_rmse = np.sqrt(mean_squared_error(kitchen_weights, scale_weights))
bearing_rmse = np.sqrt(mean_squared_error(bearing_weights_theroetical, bearing_weights_measured))

print(f"Scale RMSE: {scale_rmse:.4f} g")
print(f"Bearing RMSE: {bearing_rmse:.4f} g")

# Linear regression for scale accuracy
scale_model = LinearRegression(fit_intercept=False)
scale_model.fit(kitchen_weights.reshape(-1, 1), scale_weights)

# Predict using the model
predicted_scale_weights = scale_model.predict(kitchen_weights.reshape(-1, 1))

# Slope of the regression line (should ideally be close to 1 for accuracy)
scale_slope = scale_model.coef_[0]
print(f"Scale slope (g/g): {scale_slope:.4f}")

# Plot for scale
plt.figure(figsize=(8, 6))
plt.plot(kitchen_weights, scale_weights, 'b-o', label='Designed Scale')
plt.plot(kitchen_weights, kitchen_weights, 'r--', label='Kitchen Scale', linewidth=1)
plt.plot(kitchen_weights, predicted_scale_weights, 'g-', label=f'Linear Fit (slope={scale_slope:.4f} g/g)')

plt.title('Measured Weight of Designed Scale vs Kitchen Scale')
plt.xlabel('Kitchen Scale Weight (g)')
plt.ylabel('Designed Scale Weight (g)')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Linear regression for bearings
bearing_model = LinearRegression(fit_intercept=False)
bearing_model.fit(bearing_weights_theroetical.reshape(-1, 1), bearing_weights_measured)

# Predict using the model
predicted_bearing_weights = bearing_model.predict(bearing_weights_theroetical.reshape(-1, 1))

# Slope of the regression line for bearings
bearing_slope = bearing_model.coef_[0]
print(f"Bearing slope (g/g): {bearing_slope:.4f}")

# Plot for bearings
plt.figure(figsize=(8, 6))
plt.plot(bearings, bearing_weights_measured, 'b-o', label='Measured Weights')
plt.plot(bearings, bearing_weights_theroetical, 'r--', label='Theoretical Weights', linewidth=1)
plt.plot(bearings, [0, bearing_slope*66.5, bearing_slope*133, bearing_slope*199.5, bearing_slope*266], 'g-', 
         label=f'Linear Fit (slope={66.5 * bearing_slope:.2f} g/bearing)')

plt.title('Measured Weight vs Theoretical Weight (Bearings)')
plt.xlabel('Number of Bearings')
plt.xticks(bearings)
plt.ylabel('Weight (g)')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()
