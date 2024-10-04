from calibrator import Calibrator
from weight_reader import Weight_reader
from opentrons import robot
import time

def find_depth():
    calib.start()
    natural_weight = weight_reader.get_weight()
    time.sleep(1)
    natural_weight = weight_reader.get_weight()
    print("Natural weight: ", natural_weight, "g")
    while True:
        weight = weight_reader.get_weight()
        net_weight = weight-natural_weight
        if net_weight > 0.5:
            print("Applied weight: ", net_weight, "g")
            print("Height: ", robot_z-baseline_depth)
            return robot_z
        robot_z = robot._driver.get_head_position()['current']['z']
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

baseline_depth = find_depth() + 0.15

while True:
    find_depth()
