from opentrons import robot, instruments, containers
from ursina import *
import asyncio

def update():
    # Get current robot position
    head_pos = robot._driver.get_head_position()['current']

    # Decompose into xyz components
    head_x = head_pos.coordinates.x 
    head_y = head_pos.coordinates.y
    head_z = head_pos.coordinates.z

    # Move robot head entity to location
    robot_head.x = -head_x # Mirror x-axis: quirk of ursina engine
    robot_head.y = head_y
    robot_head.z = head_z

    # Update text to display coordinates
    coordinates_text.text = head_pos

    # Step size in mm
    step_size = 10

    # Calibrated max dimensions of the robot in mm (OT-One hood)
    xlim = [0, 375]
    ylim = [0, 250]
    zlim = [-100, 100]

    # Convert inputs into movements
    dx = held_keys['d']*step_size
    dx -= held_keys['a']*step_size
    dy = held_keys['w']*step_size
    dy -= held_keys['s']*step_size
    dz = held_keys['e']*step_size
    dz -= held_keys['q']*step_size

    # Make sure within max dimensions
    target_x = max(xlim[0], min(xlim[1], head_x+dx))
    target_y = max(ylim[0], min(ylim[1], head_y+dy))
    target_z = max(zlim[0], min(zlim[1], head_z+dz))

    # Move to target within max dimensions
    robot.move_head(x=target_x, y=target_y, z=target_z)

def on_close():
    # Disconnect the robot
    robot.disconnect()

    # Quit the application
    application.quit()

app = Ursina()

# Connect to robot and home
robot.connect(robot.get_serial_ports_list()[0])
robot.home()

# Camera position and target location
camera_position = Vec3(-800, -800, 300)
target = Vec3(-200, 200, -100)

# Set the camera position and orientation
camera.position = camera_position
camera.look_at(target, up=Vec3(0, 0, 1))  # Ensures camera is upright

# Robot head entity
robot_head = Entity(model="cube", color=color.red, texture="white_cube", scale=40)

# Coordinates text
coordinates_text = Text(origin=(-.5,.5)) # Align centered
# Top left corner
coordinates_text.x=-.87
coordinates_text.y=.49

# Create the axes at the origin
axis_length = 50  # Length of each axis
axis_thickness=0.5 # Thickness of each axis

# Axes:
# X: red
x_axis = Entity(model='cube', color=color.red, scale=(axis_length, axis_thickness, axis_thickness), position=(axis_length/2, 0, 0))
# Y: green
y_axis = Entity(model='cube', color=color.green, scale=(axis_thickness, axis_length, axis_thickness), position=(0, axis_length/2, 0))
# Z: blue
z_axis = Entity(model='cube', color=color.blue, scale=(axis_thickness, axis_thickness, axis_length), position=(0, 0, axis_length/2))
# Origin
origin = Entity(model='sphere', color=color.white, scale=2*axis_thickness, position=(0, 0, 0))

# Run closing protocol
window.exit_button.on_click = on_close

app.run()