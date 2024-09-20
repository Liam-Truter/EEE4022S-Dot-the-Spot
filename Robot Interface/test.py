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
    print(head_pos)

    dx = 100 * time.dt

    # Move along the x-axis
    try:
        if held_keys['d'] and not held_keys['a'] and head_x+dx<=400:
            robot.move_head(x=head_x+dx)
        elif held_keys['a'] and not held_keys['d']:
            robot.move_head(x=head_x-dx)
    except:
        # Cancel movement if limit switch hit
        print("X Limit Switch Hit!")
        robot.move_head(x=head_x)

    # Move along the y-axis
    try:
        if held_keys['w'] and not held_keys['s']:
            robot.move_head(y=head_y+dx)
        elif held_keys['s'] and not held_keys['w'] and head_y-dx>=0:
            robot.move_head(y=head_y-dx)
    except:
        # Cancel movement if limit switch hit
        print("Y Limit Switch Hit!")
        robot.move_head(y=head_y)

app = Ursina()
robot.connect("Virtual Smoothie")
camera.position=(200,200,-1000)
robot_head = Entity(model="cube", color=color.red, texture="white_cube", scale=40)
app.run()