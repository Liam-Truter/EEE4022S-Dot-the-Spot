from calibrator import Calibrator
from weight_reader import Weight_reader
from opentrons import robot
from opentrons.util.vector import Vector
import os
import numpy as np

import time

def move_to(coordinate,corner=False):
    x_corn = corner_point['x']
    y_corn = corner_point['y']
    z_corn = corner_point['z'] + 5
    if corner:
        x_offset = 12
        y_offset = 12
        match coordinate:
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
    else:
        x_padding = (122-9*7)/2
        y_padding = (122-9*11)/2
        x_corn += x_padding + 9 * coordinate[0]
        y_corn += y_padding + 9 * coordinate[1]

    robot.move_head(x=x_corn,y=y_corn,z=z_corn)

def find_depth(coordinate, corner=False) -> Vector:
    z_corn = corner_point['z'] + 5

    move_to(coordinate, corner)

    while True:
        weight = weight_reader.get_weight()
        net_weight = weight-natural_weight
        #print(f"Natural Weight: {natural_weight} g \t Weight: {weight} g \t Applied Force: {net_weight} g")
        robot_pos = robot._driver.get_head_position()['current']
        robot_z = robot_pos['z']
        if net_weight > force_threshold:
            robot.move_head(z=z_corn)
            return robot_pos
        robot.move_head(z=robot_z-0.1)


if len(robot.get_serial_ports_list()) > 0:
    robot.connect(robot.get_serial_ports_list()[0])
else:
    robot.connect("Virtual Smoothie")

robot.home()

calib = Calibrator()

weight_reader = Weight_reader()
weight_reader.connect()

natural_weight = weight_reader.get_weight()
force_threshold = 0.5

baseline_depth = 0

corner_point = Vector(233.00, 0.00, -5.00)

output_dir = "output_contact"
calibrate = False
if calibrate:
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    baseline_depth = find_depth(4,True)

    calib_coords = np.zeros((5,3))
    calib_coords[0,:] = np.array(baseline_depth.to_tuple())

    for i in range(4):
        while weight_reader.get_weight() > natural_weight + force_threshold/5:
            pass
        coord = find_depth(i, True)
        calib_coords[i+1,:] = np.array(coord.to_tuple())

    filename = "Empty_plate_calib_v3.npy"
    filename = os.path.join(output_dir,filename)
    np.save(filename, calib_coords)

    while weight_reader.get_weight() > natural_weight + force_threshold/5:
        pass

while True:
    filename=input("Enter a name: ")
    filename = os.path.join(output_dir, f"Corner info - {filename}.npy")
    coords = np.zeros((4,3))
    natural_weight = weight_reader.get_weight()
    for i in range(4):
        coord = find_depth(i, True)
        coords[i,:] = np.array(coord.to_tuple())
        while weight_reader.get_weight() > natural_weight + force_threshold/5:
            pass
    robot.move_head(z=35)

    np.save(filename, coords)
