from calibrator import Calibrator
from opentrons import robot, instruments, containers

if len(robot.get_serial_ports_list()) > 0:
    robot.connect(robot.get_serial_ports_list()[0])
else:
    robot.connect("Virtual Smoothie")
calib = Calibrator()
print("Calibrate Corner 1:")
calib.start()
corner1 = robot._driver.get_head_position()['current']
print("Calibrate Corner 2:")
calib.start()
corner2 = robot._driver.get_head_position()['current']
print("Calibrate Corner 3:")
calib.start()
corner3 = robot._driver.get_head_position()['current']

x_min = corner1['x']
x_max = max(corner2['x'], corner3['x'])
x_range = x_max-x_min
x_grids = x_range // 0.8
x_pad = (x_range % 0.8) / 2 + 0.4*(x_grids-8)

y_min = min(corner1['y'], corner2['y'])
y_max = corner3['y']
y_range = y_max-y_min
y_grids = y_range // 0.8
y_pad = (y_range % 0.8) / 2 + 0.4*(x_grids-8)

print()