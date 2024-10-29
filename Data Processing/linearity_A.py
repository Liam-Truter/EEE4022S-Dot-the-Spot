import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

kitchen_weights = np.array([0,23,45,64,67,74,80,96,101,103,106,119,133,200,266])
scale_weights = np.array([0,23.6,44.7,63.4,66.3,73.2,79.5,95.0,100.0,103.1,105.5,118.1,132.8,199.5,265.9])
bearings = [0,1,2,3,4]
bearing_weights_theroetical = np.array([0,66.5,133,199.5,266])
bearing_weights_measured = np.array([0,66.3,132.8,199.5,265.9])

scale_errors = scale_weights - kitchen_weights
bearing_errors = bearing_weights_measured - bearing_weights_theroetical

# Create the line plot
plt.figure(figsize=(8, 6))


# Plot each column as a line
plt.plot(kitchen_weights, scale_weights, 'b-o', label='Designed Scale')

# Plot the y=x dotted line
plt.plot(kitchen_weights, kitchen_weights, 'r--', label='Kitchen Scale', linewidth=1)

# Add labels and title
plt.title('Line Plot of Measured Weight of the Designed Scale Compared to the Kitchen Scale')
plt.xlabel('Kitchen Scale Weight (g)')
plt.ylabel('Designed Scale Weight (g)')
plt.legend()
plt.grid(True)
plt.tight_layout()


# Create the line plot
plt.figure(figsize=(8, 6))

# Plot each column as a line
plt.plot(bearings, bearing_weights_measured, 'b-o', label='Scale')

# Plot the y=x dotted line
plt.plot(bearings, bearing_weights_theroetical, 'r--', label='Theoretical Estimate', linewidth=1)

# Add labels and title
plt.title('Line Plot of Measured Weight of the Scale Compared to the Number of Bearings')
plt.xlabel('Number of Bearings')
plt.xticks(bearings)
plt.ylabel('Weight (g)')
plt.legend()
plt.grid(True)
plt.tight_layout()


# Create the boxplot
plt.figure(figsize=(8, 6))

# Plot the boxplot
sns.boxplot(data=[scale_errors, bearing_errors], palette="Set3")
plt.xticks([0, 1], ['Scale', 'Bearings'])

# Overlay a swarm plot on the boxplot
sns.swarmplot(data=[scale_errors, bearing_errors], color=".25", size=5)

# Add title and labels
plt.title('Box and Whisker Plot of Weight Errors')
plt.ylabel('Error (g)')
plt.xlabel('Method')
plt.tight_layout()

# Show the plot
plt.show()