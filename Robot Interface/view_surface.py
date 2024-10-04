from calibrator import Calibrator
from weight_reader import Weight_reader
from opentrons import robot
from opentrons.util.vector import Vector
import os
import numpy as np
import matplotlib.pyplot as plt

import time

output_dir = "output_contact"
filename = "Surface info - 1.1.npy"
filename = os.path.join(output_dir, filename)
points = np.load(filename)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.scatter(points[:,0],points[:,1],points[:,2])

plt.show()