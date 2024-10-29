import matplotlib.pyplot as plt
import numpy as np

bearings = [0,1,2,3,4]
bearing_weights_theroetical = [0,66.5,133,199.5,266]
bearing_weights_measured = [0,66.3,132.8,199.5,265.9]

# Create the line plot
plt.figure(figsize=(8, 6))


# Plot each column as a line
plt.plot(bearings, bearing_weights_measured, label='Scale')

# Plot the y=x dotted line
plt.plot(bearings, bearing_weights_theroetical, 'r--', label='Theoretical Estimate', linewidth=1)

# Add labels and title
plt.title('Line Plot of Measured Weight of the Scale Compared to the Number of Bearings')
plt.xlabel('Number of Bearings')
plt.ylabel('Weight (g)')
plt.legend()
plt.grid(True)
#plt.xlim(5000, x_values[-1])
#plt.ylim(0,x_values[-1])
#plt.ylim(0, max(max(col) for col in columns) + 500)

# Show the plot
plt.tight_layout()
plt.show()