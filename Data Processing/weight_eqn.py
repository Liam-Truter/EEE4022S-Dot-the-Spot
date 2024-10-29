import numpy as np
import matplotlib.pyplot as plt

# Data
agar_weight = np.array([76.4, 21.1, 79.5, 94.5, 49.6, 39.8, 55.9, 81.9, 71.4, 71.3, 64.4, 64.2, 59.2, 42.0, 74.1, 0.0])
average_height = np.array([7.1, 3.6, 6.5, 8.2, 4.7, 4.5, 4.9, 8.0, 6.3, 7.3, 6.7, 6.7, 6.3, 5.3, 7.4, 0.0])

plt.figure(figsize=(8,6))

# Scatter plot
plt.scatter(agar_weight, average_height, color='blue', label='Data Points')

# Least squares regression (line through the origin)
X = agar_weight#.reshape(-1, 1)
Y = average_height

# Finding the line of best fit passing through the origin (slope only)
slope = np.sum(X* Y) / np.sum(X**2)
line_fit = slope * X


# Plotting the regression line
plt.plot(agar_weight, line_fit, color='red', label=f'Best Fit Line: {slope:.4f} mm/g')

# Plot settings
plt.xlabel('Agar Weight (g)')
plt.ylabel('Average Height (mm)')
plt.title('Average Height Compared to Weight')
#plt.legend()
plt.grid(True)
plt.tight_layout
plt.show()

# RMSE calculation
rmse = np.sqrt(np.sum(np.square(Y - line_fit))/len(Y))
slope_g_per_mm = 1 / slope

# Print the slope in mm/g and g/mm, and the RMSE
slope, slope_g_per_mm, rmse

print("mm/g\tg/mm\tRMSE")
print(f"{slope:.3f}\t{slope_g_per_mm:.2f}\t{rmse:.2f}")
