from calibrator import Calibrator
from weight_reader import Weight_reader
import os
import numpy as np

output_dir="output_contact"
file_a = os.path.join(output_dir, "Surface info - 0.1.npy")

file_b = os.path.join(output_dir, "Surface info - 1.npy")

file_c = os.path.join(output_dir, "Surface info - 1.1.npy")

a = np.load(file_a)
b = np.load(file_b)
b[2*12+5,:] = a[2*12+5,:]

np.save(file_c, b)