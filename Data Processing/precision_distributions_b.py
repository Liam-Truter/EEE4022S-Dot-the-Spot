import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

data = [
    [-0.13, -0.07, 0.10, 0.30, -0.13, -0.13, 0.30, -0.13],
    [-0.10, -0.10, 0.13, -0.13, 0.20, -0.23, 0.30, -0.23],
    [-0.17, -0.03, 0.07, 0.03, -0.03, 0.00, 0.03, 0.03],
    [-0.13, 0.00, -0.10, -0.13, -0.03, 0.10, 0.03, -0.10],
    [-0.23, -0.20, 0.07, 0.03, -0.10, -0.03, 0.00, -0.17]
    
    
]

# Labels for the datasets
labels = ['X', 'Y', 'Z', 'A', 'B']

# Create the boxplot
plt.figure(figsize=(8, 6))
# Plot the boxplot
sns.boxplot(data=data, palette="Set3")
plt.xticks([0, 1, 2, 3, 4], labels)

# Overlay a swarm plot on the boxplot
sns.swarmplot(data=data, color=".25", size=5)

# Add title and labels
plt.title('Box and Whisker Plot of Axis Errors')
plt.ylabel('Error (mm)')

print("Axis\tStd Dev\tRMSE")
for i, axis in enumerate(labels):
    dataset = data[i]
    rmse = np.sqrt(np.sum(np.square(dataset))/len(dataset))
    stddev = np.std(dataset)
    print(f"{axis}\t{stddev:.2f}\t{rmse:.2f}")

# Show the plot
plt.show()
