import pyrealsense2 as rs

# Initialize pipeline and configure it
pipeline = rs.pipeline()
config = rs.config()

# Enable the depth stream
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

# Start streaming
pipeline.start(config)

# Get the depth sensor (which controls the emitter/laser)
device = pipeline.get_active_profile().get_device()
depth_sensor = device.first_depth_sensor()

# Check if the sensor has an emitter option
if depth_sensor.supports(rs.option.emitter_enabled):
    print(f"Emitter Enabled: {depth_sensor.get_option(rs.option.emitter_enabled)}")
else:
    print("This device does not support emitter control.")

# Get the current emitter power (laser strength)
if depth_sensor.supports(rs.option.laser_power):
    current_laser_power = depth_sensor.get_option(rs.option.laser_power)
    print(f"Current Laser Power: {current_laser_power}")

    # Set a new laser power value (between the minimum and maximum allowed values)
    new_laser_power = 150  # Example value, adjust based on your needs
    min_laser_power = depth_sensor.get_option_range(rs.option.laser_power).min
    max_laser_power = depth_sensor.get_option_range(rs.option.laser_power).max
    print(f"Laser Power Range: {min_laser_power} - {max_laser_power}")
    
    if min_laser_power <= new_laser_power <= max_laser_power:
        depth_sensor.set_option(rs.option.laser_power, new_laser_power)
        print(f"Laser Power set to: {new_laser_power}")
    else:
        print(f"Laser power value {new_laser_power} is out of range.")

else:
    print("This device does not support laser power control.")

# Stop the pipeline
pipeline.stop()
