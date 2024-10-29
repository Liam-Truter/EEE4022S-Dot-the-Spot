import matplotlib.pyplot as plt
import numpy as np

step_sizes = [100, 50, 10, 5, 1, 0.5, 0.1]
time_taken = np.array([
    [0.696, 0.876, 1.973, 2.865, 7.13, 10.858, 32.004],  # X-axis times
    [0.697, 0.875, 1.971, 2.866, 7.144, 10.885, 32.155],  # Y-axis times
    [2.118, 2.216, 2.99, 3.953, 9.519, 14.274, 39.655]   # Z-axis times
])

data = 100*60/time_taken
plt.figure(figsize=(8, 6))
axes = ["X", "Y", "Z"]
for i, axis in enumerate(axes):
    plt.plot(step_sizes, data[i], label=f'Axis {axis}')

# Add labels and title
plt.title('Line Plot of Measured Head Speed With Varying Step Sizes Over a Distance of 100 mm')
plt.xlabel('Step Size (mm)')
plt.ylabel('Measured Speed (mm/min)')
plt.legend()
plt.grid(True)
#plt.xscale('log')

# Show the plot
plt.tight_layout()
plt.show()