import open3d as o3d
import numpy as np

# Load the point cloud
points = np.loadtxt('pointcloud-09.xyz')

x_values = points[:,0]
y_values = points[:,1]
z_values = points[:,2]

xmax = 0.15
xmin = -0.04
ymax = 0.05
ymin = -0.15

# Get points in approximate ROI
mask = (x_values<xmax) & (y_values<ymax) & (x_values>xmin) & (y_values>ymin)
points = points[mask]

# Create Open3D point cloud object
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points)

# Visualize the point cloud
o3d.visualization.draw_geometries([pcd], window_name="Point Cloud Viewer")