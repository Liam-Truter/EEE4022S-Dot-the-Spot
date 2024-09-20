from opentrons import robot, instruments, containers
from ursina import *
import asyncio

def update():
    head_pos = robot._driver.get_head_position()['current']
    head_x = head_pos.coordinates.x 
    head_y = head_pos.coordinates.y
    head_z = head_pos.coordinates.z
    robot_head.x = -head_x # Mirror x-axis wtf
    robot_head.y = head_y
    robot_head.z = head_z
    coordinates_text.text = head_pos

    step_size = 10
    xlim = [0, 375]
    ylim = [0, 250]
    zlim = [-100, 100]

    dx = held_keys['d']*step_size
    dx -= held_keys['a']*step_size
    dy = held_keys['w']*step_size
    dy -= held_keys['s']*step_size
    dz = held_keys['e']*step_size
    dz -= held_keys['q']*step_size

    target_x = max(xlim[0], min(xlim[1], head_x+dx))
    target_y = max(ylim[0], min(ylim[1], head_y+dy))
    target_z = max(zlim[0], min(zlim[1], head_z+dz))

    robot.move_head(x=target_x, y=target_y, z=target_z)

def on_close():
    # Disconnect the robot
    robot.disconnect()

    application.quit()  # Ensures that the app quits after running custom code

app = Ursina()

robot.connect(robot.get_serial_ports_list()[0])
robot.home()

# Camera's current position (z is the height axis)
camera_position = Vec3(-800, -800, 300)

# Target point (where you want the camera to look)
target = Vec3(-200, 200, -100)

# Set the camera position
camera.position = camera_position

# Make the camera look at the target point, with the up direction along the z-axis
camera.look_at(target, up=Vec3(0, 0, 1))  # Ensures camera is upright

robot_head = Entity(model="cube", color=color.red, texture="white_cube", scale=40)

#Entity(model='cube', color=color.red, scale=10, position=target)

coordinates_text = Text(origin=(-.5,.5))
coordinates_text.x=-.87
coordinates_text.y=.49

# Create the axes at the origin
axis_length = 50  # Length of each axis
axis_thickness=0.5

# X-axis (red)
x_axis = Entity(model='cube', color=color.red, scale=(axis_length, axis_thickness, axis_thickness), position=(axis_length/2, 0, 0))

# Y-axis (green)
y_axis = Entity(model='cube', color=color.green, scale=(axis_thickness, axis_length, axis_thickness), position=(0, axis_length/2, 0))

# Z-axis (blue)
z_axis = Entity(model='cube', color=color.blue, scale=(axis_thickness, axis_thickness, axis_length), position=(0, 0, axis_length/2))

# Origin sphere for visualizing the center
origin = Entity(model='sphere', color=color.white, scale=2*axis_thickness, position=(0, 0, 0))

window.exit_button.on_click = on_close

app.run()