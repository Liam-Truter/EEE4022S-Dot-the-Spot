import numpy as np
import matplotlib.pyplot as plt


data = [
    [4643, 4647, 2850],
    [5027, 5035, 2850],
    [5452, 5453, 2850],
    [5801, 5809, 2850],
    [6153, 6152, 2852],
    [6516, 6520, 2851],
    [6827, 6834, 2851],
    [7114, 7116, 2850],
    [7426, 7423, 2851],
    [7695, 7697, 2851],
    [7942, 7934, 2850],
    [8191, 8182, 2851],
    [8384, 8388, 2851],
    [8582, 8594, 2851],
    [8780, 8789, 2851],
    [8970, 8958, 2850],
    [9109, 9123, 2850],
    [9259, 9264, 2850],
    [9423, 9414, 2851],
    [9516, 9524, 2849],
    [9616, 9611, 2850],
    [9710, 9717, 2851],
    [9795, 9812, 2850],
    [9886, 9892, 2850],
    [9956, 9944, 2851],
    [9988, 9994, 2852],
    [10033, 10034, 2850],
    [10097, 10079, 2850],
    [10094, 10093, 2849],
    [10105, 10117, 2852],
    [10117, 10132, 2851],
    [10137, 10122, 2849],
    [10141, 10124, 2851]
]

# Convert to an array of arrays (columns)
columns = [[row[i] for row in data] for i in range(len(data[0]))]

# X values starting from 5000, incremented in steps of 500
x_values = np.arange(5000, 5000 + 500 * len(columns[0]), 500)

# Create the line plot
plt.figure(figsize=(8, 6))


column_labels = ['X', 'Y', 'Z']
# Plot each column as a line
for i, column in enumerate(columns):
    plt.plot(x_values, column, label=f'Axis {column_labels[i]}')

# Plot the y=x dotted line
plt.plot(x_values, x_values, 'r--', label='Theoretical Speed', linewidth=1)

# Add labels and title
plt.title('Line Plot of Measured Head Speed Compared to Theoretical Head Speed Over a Distance of 100 mm')
plt.xlabel('Theoretical Speed (mm/min)')
plt.ylabel('Measured Speed (mm/min)')
plt.legend()
plt.grid(True)
plt.xlim(5000, x_values[-1])
plt.ylim(0,x_values[-1])
#plt.ylim(0, max(max(col) for col in columns) + 500)

# Show the plot
plt.tight_layout()
plt.show()