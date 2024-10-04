import open3d as o3d
import numpy as np

# Load the point cloud
pointcloud = np.loadtxt('pointcloud-09.xyz')

# Create Open3D point cloud object
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(pointcloud)

# Visualize the point cloud
o3d.visualization.draw_geometries([pcd], window_name="Point Cloud Viewer")