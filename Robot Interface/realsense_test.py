import pyrealsense2 as rs
import numpy as np
import cv2
import os
import time

# Create output directory
output_dir = "output(agar)"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Initialize Intel RealSense pipeline
pipeline = rs.pipeline()
config = rs.config()

# Initialize resolutions
col_width = 640
col_height = 480
dep_width = 640
dep_height = 480

# Configure the pipeline to stream color and depth
config.enable_stream(rs.stream.color, col_width, col_height, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, dep_width, dep_height, rs.format.z16, 30)

# Start streaming
cfg = pipeline.start(config)

# Get the depth scale from the depth sensor
depth_sensor = pipeline.get_active_profile().get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()

# Set the laser power to max for agar
depth_sensor.set_option(rs.option.laser_power, 360)
print(f"Depth scale is: {depth_scale} meters per unit")

def save_frames(color_image, depth_image):
    """
    Save the color image and depth map to disk.

    Parameters:
    - color_image: The color image as a NumPy array
    - depth_image: The depth data as a NumPy array
    """

    # Get the current time in milliseconds
    timestamp = int(time.time() * 1000)
    color_filename = os.path.join(output_dir, f"color_{timestamp}_{col_width}x{col_height}.png")
    depth_filename = os.path.join(output_dir, f"depth_{timestamp}_{dep_width}x{dep_height}.png")
    depth_npy_filename = os.path.join(output_dir, f"depth_{timestamp}_{dep_width}x{dep_height}.npy")

    # Save the color image as PNG
    cv2.imwrite(color_filename, color_image)
    
    # Save the depth image as 16-bit PNG
    cv2.imwrite(depth_filename, depth_image)
    
    # Optionally, save the depth data as a NumPy .npy file for more precise analysis
    np.save(depth_npy_filename, depth_image)

    print(f"Saved color image to {color_filename} and depth map to {depth_filename} and {depth_npy_filename}")


try:
    frame_id = 0
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        
        if not depth_frame or not color_frame:
            continue

        # Convert depth and color frames to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        profile = cfg.get_stream(rs.stream.depth)
        depth_intrinsics = profile.as_video_stream_profile().get_intrinsics()

        # Apply colormap to depth image for better visualization
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        # Display the images
        cv2.imshow('RealSense Color', color_image)
        cv2.imshow('RealSense Depth', depth_colormap)

        # Save frames on 's' key press
        key = cv2.waitKey(1)
        if key == ord('s'):
            save_frames(color_image, depth_image)

        # Exit on 'q' key press
        if key == ord('q'):
            break

finally:
    # Stop streaming
    pipeline.stop()
    cv2.destroyAllWindows()
