import os
import numpy as np
import matplotlib.pyplot as plt

def fit_plane(points: np.array) -> np.array:
    X = points[:,0]
    Y = points[:,1]
    Z = points[:,2]

    A = np.vstack([X,Y, np.ones(len(X))]).T
    B = Z

    coefficients, residuals, _, _ = np.linalg.lstsq(A,B,rcond=None)

    a, b, d = coefficients

    return a,b,d

output_dir="output_contact"

weights = [76.4, 21.1, 79.5, 94.5, 49.6, 39.8, 55.9, 81.9, 71.4]
mmpg = 0.09
surface_file_idxs = ['1.1', '2.1', '3', '4.1', '5', '6', '7', '8', '9']

calib_coord_file = os.path.join(output_dir, 'Corner info - 0.npy')


calibration_coords = np.load(calib_coord_file)
origin = np.zeros(3)
for i in range(3):
    origin[i] = np.sum(calibration_coords[:,i])/4
calibration_coords -= origin

errors = np.zeros((9,96))

for i in range(len(weights)):
    weight = weights[i]
    height_estimate = mmpg*weight

    surface_file_idx = surface_file_idxs[i]
    surface_file = os.path.join(output_dir, f"Surface info - {surface_file_idx}.npy")
    surface = np.load(surface_file) - origin

    X_surface = surface[:,0]
    Y_surface = surface[:,1]
    Z_surface = surface[:,2]

    heights = np.zeros(4)

    a,b,d = (0,0,height_estimate)

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    ax.scatter(X_surface,Y_surface,Z_surface, color='g')
    ax.set_zlim(0,12)

    x_range = np.linspace(-60, 60, 10)
    y_range = np.linspace(-60, 60, 10)
    X_grid, Y_grid = np.meshgrid(x_range, y_range)
    
    Z_grid = a * X_grid + b * Y_grid + d
    Z_plane = a*X_surface + b*Y_surface + d

    error = Z_plane - Z_surface

    print(f"Error Plate {i+1}:")
    print("Mean\tMax\tMin\tRMSE")

    mean_error = np.mean(error)
    max_error = np.max(error)
    min_error = np.min(error)
    rmse = np.sqrt(np.sum(np.square(error))/96)

    print(f"{mean_error:.2f}\t{max_error:.2f}\t{min_error:.2f}\t{rmse:.2f}")

    errors[i,:] = error

    ax.plot_surface(X_grid, Y_grid, Z_grid, alpha=0.5, color='r')

    #print(f"z = {a:.2f}x + {b:.2f}y + {d:.2f}")

print("Total Error:")
print("Mean\tMax\tMin\tRMSE")
mean_error = np.mean(errors)
max_error = np.max(errors)
min_error = np.min(errors)
rmse = np.sqrt(np.sum(np.square(errors))/(96*9))
print(f"{mean_error:.2f}\t{max_error:.2f}\t{min_error:.2f}\t{rmse:.2f}")
plt.show()