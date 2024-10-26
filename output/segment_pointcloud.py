import open3d as o3d
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load the point cloud (from .xyz, .ply, or other format)
pcd = o3d.io.read_point_cloud("pointcloud.xyz")

# Convert the point cloud to a NumPy array to manipulate
points = np.asarray(pcd.points)
x_values = points[:,0]
y_values = points[:,0]
z_values = points[:,2]

# Get the top surface depth
surface_depth = np.min(z_values[z_values>0])

# Get points in approximate ROI
mask = (x_values<0.150) & (y_values<0.150) & (x_values>-0.150) & (y_values>-0.150)
points = points[mask]

# Filter points closer to the camera
z_threshold = surface_depth + 0.03
filtered_points = points[points[:, 2] < z_threshold]

# Convert filtered points back into an Open3D PointCloud object
filtered_pcd = o3d.geometry.PointCloud()
filtered_pcd.points = o3d.utility.Vector3dVector(filtered_points)

# DBSCAN clustering
labels = np.array(filtered_pcd.cluster_dbscan(eps=0.02, min_points=10, print_progress=True))

# Find the largest cluster by 
max_label = labels.max()
cluster_sizes = np.bincount(labels[labels >= 0])
largest_cluster_idx = np.argmax(cluster_sizes)

largest_cluster_points = filtered_pcd.select_by_index(np.where(labels == largest_cluster_idx)[0])

# Segment the plane using RANSAC
plane_model, inliers = largest_cluster_points.segment_plane(distance_threshold=0.002,
                                                  ransac_n=3,
                                                  num_iterations=1000)

# Extract plane coefficients
[a, b, c, d] = plane_model
print(f"Plane equation: {a:.4f}x + {b:.4f}y + {c:.4f}z + {d:.4f} = 0")

# Extract inlier points
inlier_cloud = largest_cluster_points.select_by_index(inliers)

# Color the plane points for visualization
inlier_cloud.paint_uniform_color([1.0, 0, 0])  # Color the plane in red

# Extract the outlier points
outlier_cloud = largest_cluster_points.select_by_index(inliers, invert=True)

# Color the outlier points for visualization
outlier_cloud.paint_uniform_color([0, 0, 1])

inlier_points = np.asarray(inlier_cloud.points)

# Calculate the distance of each point from the plane
distances = np.abs(a * inlier_points[:, 0] + b * inlier_points[:, 1] + c * inlier_points[:, 2] + d) / np.sqrt(a**2 + b**2 + c**2)

# Compute RMSE
rmse = np.sqrt(np.mean(distances**2))
print(f"RMSE: {rmse:.4f} meters")

# Visualize the segmented plane and remaining points
#o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud], window_name="Plane Segmentation")

# Filter points further from the camera until a max value
z_threshold_min = z_threshold
z_threshold_max = 0.42
filtered_points_far = points[points[:,2] > z_threshold_min]
filtered_points_far = filtered_points_far[filtered_points_far[:,2] < z_threshold_max]

# Convert filtered points back into a pointcloud
filtered_far_pcd = o3d.geometry.PointCloud()
filtered_far_pcd.points = o3d.utility.Vector3dVector(filtered_points_far)
filtered_far_pcd.paint_uniform_color([0, 1.0, 0])

# Create a KDTree for fast nearest neighbor search on the inlier cloud
kdtree = o3d.geometry.KDTreeFlann(inlier_cloud)

# Define the distance threshold (in meters)
distance_threshold = 0.08  # Adjust this as needed

# Initialize a list to store the indices of points that are close to the inlier points
selected_far_indices = []

# For each point in filtered_far_pcd, find its nearest neighbor in inlier_cloud
for i, point in enumerate(filtered_far_pcd.points):
    [k, idx, dist] = kdtree.search_radius_vector_3d(point, distance_threshold)  # Search within the radius
    if k > 0:  # If at least one neighbor is found within the distance threshold
        selected_far_indices.append(i)
# Extract the selected points (those within the distance threshold)
selected_far_pcd = filtered_far_pcd.select_by_index(selected_far_indices)

# Visualize the selected points
#selected_far_pcd.paint_uniform_color([0, 1, 0])  # Color the selected points in green
#o3d.visualization.draw_geometries([inlier_cloud, selected_far_pcd], window_name="Selected Points Near Inlier Cloud")

# DBSCAN clustering using Open3D's cluster_dbscan method
labels_far = np.array(selected_far_pcd.cluster_dbscan(eps=0.02, min_points=10, print_progress=True))

# Find the largest cluster by counting the number of points in each cluster
max_label_far = labels_far.max()  # Find the highest label (i.e., largest cluster)
cluster_sizes_far = np.bincount(labels_far[labels_far >= 0])  # Count points per cluster (exclude noise)
largest_cluster_far_idx = np.argmax(cluster_sizes_far)  # Index of the largest cluster

largest_cluster_far_points = selected_far_pcd.select_by_index(np.where(labels_far == largest_cluster_far_idx)[0])

# Step 2: Segment the plane using RANSAC
# Use Open3D's built-in segment_plane function
plane_far_model, inliers_far = largest_cluster_far_points.segment_plane(distance_threshold=0.002,
                                                  ransac_n=3,
                                                  num_iterations=1000)

# Extract plane coefficients
[a_far, b_far, c_far, d_far] = plane_far_model
print(f"Far plane equation: {a_far:.4f}x + {b_far:.4f}y + {c_far:.4f}z + {d_far:.4f} = 0")

# Extract inlier points (points that lie on the plane)
inlier_far_cloud = largest_cluster_far_points.select_by_index(inliers_far)

# Color the plane points for visualization
inlier_far_cloud.paint_uniform_color([0, 1.0, 0])  # Color the plane in red

o3d.visualization.draw_geometries([inlier_cloud, inlier_far_cloud], window_name="Selected Points Near Inlier Cloud")
# Function to calculate perpendicular distances from a plane
def calculate_distances(points, plane_model):
    a, b, c, d = plane_model
    distances = np.abs(a * points[:, 0] + b * points[:, 1] + c * points[:, 2] + d) / np.sqrt(a**2 + b**2 + c**2)
    return distances * 1000

# Calculate distances for inlier_cloud
inlier_points = np.asarray(inlier_cloud.points)
distances_inlier = calculate_distances(inlier_points, plane_far_model)

# Compute statistics for inlier points
print("Inlier Plane Distance Statistics:")
print(f"Min: {np.min(distances_inlier):.2f}, Mean: {np.sum(distances_inlier)/len(distances_inlier):.2f} Max: {np.max(distances_inlier):.2f}, StdDev: {np.std(distances_inlier):.2f}")


# Plot using seaborn
plt.figure(figsize=(8, 6))
sns.boxplot(data=distances_inlier, palette="Set3")
plt.title("Measured Height of Box Surface")
plt.ylabel("Distance (mm)")
plt.show()
np.save("box_height_640x480.npy", distances_inlier)