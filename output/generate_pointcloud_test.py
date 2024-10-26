import pyrealsense2 as rs
import numpy as np

def generate_pointcloud(depth_image, intrinsics, depth_scale):
    height, width = depth_image.shape
    pointcloud = []

    for y in range(height):
        for x in range(width):
            depth = depth_image[y, x] * depth_scale
            if depth == 0 or depth>0.45:
                continue
            point = rs.rs2_deproject_pixel_to_point(intrinsics, [x, y], depth)
            pointcloud.append(point)
    
    return np.array(pointcloud)

# Load depth data
depth_image = np.load('output\depth_1727338635804_480x270.npy')
print(np.min(depth_image[depth_image>0]))
# Approximate intrinsics for D455 at 640x480
intrinsics = rs.intrinsics()
intrinsics.width = 640
intrinsics.height = 480
intrinsics.fx = 387.0
intrinsics.fy = 387.0
intrinsics.ppx = 323.0
intrinsics.ppy = 237.7
intrinsics.model = rs.distortion.brown_conrady
intrinsics.coeffs = [0, 0, 0, 0, 0]

# Depth scale
depth_scale = 0.001  

# Generate point cloud
pointcloud = generate_pointcloud(depth_image, intrinsics, depth_scale)

# Save point cloud
np.savetxt("pointcloud_480x270.xyz", pointcloud)