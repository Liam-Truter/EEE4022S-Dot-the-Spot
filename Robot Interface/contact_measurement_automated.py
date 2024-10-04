from calibrator import Calibrator
from weight_reader import Weight_reader
from opentrons import robot
from opentrons.util.vector import Vector

import time

def find_depth(corner):
    x_corn = corner_point['x']
    y_corn = corner_point['y']
    z_corn = corner_point['z'] + 15
    x_offset = 15
    y_offset = 15
    match corner:
        case 0:
            x_corn += x_offset
            y_corn += y_offset
        case 1:
            x_corn += 122-x_offset
            y_corn += y_offset
        case 2:
            x_corn += 122-x_offset
            y_corn += 122-y_offset
        case 3:
            x_corn += x_offset
            y_corn += 122-y_offset
        case 4:
            x_corn += 61
            y_corn += 61
    robot.move_head(x=x_corn,y=y_corn,z=z_corn)
    natural_weight = weight_reader.get_weight()
    time.sleep(1)
    natural_weight = weight_reader.get_weight()
    print("Natural weight: ", natural_weight, "g")
    while True:
        weight = weight_reader.get_weight()
        net_weight = weight-natural_weight
        robot_z = robot._driver.get_head_position()['current']['z']
        if net_weight > 0.1:
            print("Applied weight: ", net_weight, "g")
            print("Height: ", robot_z-baseline_depth)
            robot.move_head(z=z_corn)
            return robot_z
        robot.move_head(z=robot_z-0.1)


if len(robot.get_serial_ports_list()) > 0:
    robot.connect(robot.get_serial_ports_list()[0])
else:
    robot.connect("Virtual Smoothie")

robot.home()

calib = Calibrator()

weight_reader = Weight_reader()
weight_reader.connect()

baseline_depth = 0

corner_point = Vector(233.00, 0.00, -5.00)

baseline_depth = find_depth(4) + 0.15

while True:
    calib.start()
    for i in range(4):
        find_depth(i)
