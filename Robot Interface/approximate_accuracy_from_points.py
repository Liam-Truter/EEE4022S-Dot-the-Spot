import os
import numpy as np
import matplotlib.pyplot as plt

output_dir = 'output_contact'
file_a = 'Surface info - 4.npy'
file_a = os.path.join(output_dir, file_a)

file_b = 'Surface info - 4.1.npy'
file_b = os.path.join(output_dir, file_b)

points = np.load(file_a)
#points_b = np.copy(points)
centroid = np.zeros(3)
centroid[0] = np.sum(points[:,0])/96
centroid[1] = np.sum(points[:,1])/96

points -= centroid
points_b = np.copy(points)
points_b[:,0:2] = -points[:,0:2]
points_b += centroid
points += centroid

#inverted_zs = points[::-1,2]

#points_b[:,2] = inverted_zs

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.scatter(points[:,0],points[:,1],points[:,2], color='b')

ax.scatter(points_b[:,0],points_b[:,1],points_b[:,2], color='g')

plt.show()

np.save(file_b, points)
