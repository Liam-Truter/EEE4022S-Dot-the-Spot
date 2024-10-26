import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

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

heights = np.array([
           [6.0, 7.4, 7.7, 7.2],
           [4.0, 3.8, 2.8, 2.2],
           [6.8, 7.5, 5.9, 6.0],
           [8.4, 7.6, 7.6, 9.5],
           [5.5, 4.9, 3.7, 4.7],
           [3.9, 5.5, 4.3, 4.2],
           [4.9, 3.1, 5.1, 6.6],
           [6.1, 5.3, 10.5, 10.2],
           [5.7, 7.7, 6.1, 5.6]])
surface_file_idxs = ['1.1', '2.1', '3', '4.1', '5', '6', '7', '8', '9']

calib_coord_file = os.path.join(output_dir, 'Corner info - 0.npy')

calibration_coords = np.load(calib_coord_file)
origin = np.zeros(3)
for i in range(3):
    origin[i] = np.sum(calibration_coords[:,i])/4
calibration_coords -= origin

errors = np.zeros((9,96))

height_offset = np.array([0,0,0.2])

for i in range(len(heights)):
    corner_heights = heights[i,:]
    corner_points = np.copy(calibration_coords)
    corner_points[:,2] += corner_heights

    surface_file_idx = surface_file_idxs[i]
    surface_file = os.path.join(output_dir, f"Surface info - {surface_file_idx}.npy")
    surface = np.load(surface_file) - origin + height_offset

    X_surface = surface[:,0]
    Y_surface = surface[:,1]
    Z_surface = surface[:,2]
    
    X_corners = corner_points[:,0]
    Y_corners = corner_points[:,1]
    Z_corners = corner_points[:,2]

    a,b,d = fit_plane(corner_points)

    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(projection='3d')

    # Scatter plots for surface and corners
    ax.scatter(X_surface,Y_surface,Z_surface, color='g', alpha=1, label="Surface Points")
    ax.scatter(X_corners,Y_corners,Z_corners, color='b', alpha=1, label="Corner Points")
    ax.set_zlim(0,12)

    # Create a mesh grid for the fitted plane
    x_range = np.linspace(-60, 60, 10)
    y_range = np.linspace(-60, 60, 10)
    X_grid, Y_grid = np.meshgrid(x_range, y_range)
    Z_grid = a * X_grid + b * Y_grid + d
    Z_plane = a * X_surface + b * Y_surface + d

    # Get true Z heights at points
    Z_plane_surface = a * X_surface + b * Y_surface + d
    Z_plane_corners = a * X_corners + b * Y_corners + d

    # Calculate errors
    error = Z_plane - Z_surface
    errors[i,:] = error

    # Gather stats
    mean_error = np.mean(error)
    max_error = np.max(error)
    min_error = np.min(error)
    rmse = np.sqrt(np.sum(np.square(error)) / 96)

    # Print stats
    print(f"Error Plate {i+1}:")
    print("Mean\tMax\tMin\tRMSE")
    print(f"{mean_error:.2f}\t{max_error:.2f}\t{min_error:.2f}\t{rmse:.2f}")

    # Colour
    #norm = plt.Normalize(vmin=min_error, vmax=max_error)
    #colors = cm.viridis(norm(error))

    for j in range(len(X_surface)):
        ax.plot([X_surface[j], X_surface[j]], 
                [Y_surface[j], Y_surface[j]], 
                [Z_surface[j], Z_plane_surface[j]], 
                color='black', linewidth=1, alpha=1)
    for j in range(len(X_corners)):
        ax.plot([X_corners[j], X_corners[j]], 
                [Y_corners[j], Y_corners[j]], 
                [Z_corners[j], Z_plane_corners[j]], 
                color='black', linewidth=1, alpha=1)

    # Plot fitted plane
    ax.plot_surface(X_grid, Y_grid, Z_grid, alpha=0.5, color='r', edgecolor='w', linewidth=0.2, label="Fitted Plane")

    ax.set_xlabel("X (mm)")
    ax.set_ylabel("Y (mm)")
    ax.set_zlabel("Z (mm)")
    plt.tight_layout()

print("Total Error:")
print("Mean\tMax\tMin\tRMSE")
mean_error = np.mean(errors)
max_error = np.max(errors)
min_error = np.min(errors)
rmse = np.sqrt(np.sum(np.square(errors)) / (96 * 9))
print(f"{mean_error:.2f}\t{max_error:.2f}\t{min_error:.2f}\t{rmse:.2f}")

plt.show()
