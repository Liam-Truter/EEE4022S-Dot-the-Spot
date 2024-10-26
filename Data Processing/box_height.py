import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

d1 = np.load("box_height_640x480.npy")
d2 = np.load("box_height_640x360.npy")
d3 = np.load("box_height_480x270.npy")

distances = [d1, d2, d3]
# Plot using seaborn
plt.figure(figsize=(8, 6))
sns.boxplot(data=distances, palette="Set3")
plt.title("Measured Height of Box Surface")
plt.ylabel("Distance (mm)")
plt.xlabel("Resolution")
plt.xticks([0, 1, 2], ['640x480', '640x360', '480x270'])
plt.show()

print(len(d1))
print(len(d2))
print(len(d3))