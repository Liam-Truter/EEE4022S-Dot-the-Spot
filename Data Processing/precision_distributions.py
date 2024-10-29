import matplotlib.pyplot as plt
import numpy as np

data = [
    [-0.3, 0, -0.1, 0.2, -0.3, -0.1, 0, 0.2, 0.1, 0.6, 0.1, 0.2, -0.3, -0.1, 0, -0.2, -0.1, -0.1, 0.5, 0.2, 0.2, -0.2, -0.1, -0.1],
    [-0.2, 0.3, -0.4, 0.3, -0.6, 0, -0.1, 0.4, 0.1, 0, -0.2, -0.2, 0.1, 0.3, 0.2, 0, -0.5, -0.2, 0.3, 0.4, 0.2, -0.9, 0.4, -0.2],
    [-0.3, -0.2, 0, 0, 0.2, -0.3, 0.3, -0.1, 0, -0.5, 0.5, 0.1, 0.1, -0.2, 0, 0.4, -0.3, -0.1, -0.3, 0.4, 0, 0.2, -0.1, 0],
    [0, -0.3, -0.1, 0, 0.1, -0.1, 0.1, -0.3, -0.1, -0.3, 0.1, -0.2, 0.1, -0.1, -0.1, 0.1, 0.2, 0, -0.1, 0.1, 0.1, -0.1, 0, -0.2],
    [-0.9, 0.2, 0, -0.5, -0.1, 0, 0.8, -0.5, -0.1, -0.1, -0.2, 0.4, -0.1, 0.1, -0.3, 0.1, -0.2, 0, -0.1, 0.4, -0.3, -0.3, -0.2, 0]
]

# Labels for the datasets
labels = ['X', 'Y', 'Z', 'A', 'B']

# Create the boxplot
plt.figure(figsize=(8, 6))
plt.boxplot(data, labels=labels)

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
