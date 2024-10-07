from weight_reader import Weight_reader
import numpy as np

weight_reader = Weight_reader()
weight_reader.connect()

samples = 1000

weights = np.zeros(samples)

for i in range(samples):
    weight = weight_reader.get_weight()
    weights[i] = weight
    print(weight)

mean = np.sum(weights)/samples
min_weight = np.min(weights)
max_weight = np.max(weights)
stddev = np.std(weights)
print(f"mean: {mean:.2f}\t min: {min_weight:.2f}\t max: {max_weight:.2f}\t stddev: {stddev:.2f}")