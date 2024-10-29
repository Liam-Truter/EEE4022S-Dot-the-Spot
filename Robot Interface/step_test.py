from opentrons import robot
import numpy as np
import time

robot.connect(robot.get_serial_ports_list()[0])
robot.home()

x=0
y=250
z=100

step_size = 0.1
target = 100 + step_size

X = np.arange(x,target, step_size)
Y = np.arange(y, y-target, -step_size)
Z = np.arange(z, z-target, -step_size)

start = time.time()

for xi in Z:
    robot.move_head(z=xi)

end = time.time()

duration = end-start
print("Target\tStep Size\tDuration")
print(f"{target-step_size}\t{step_size}\t{duration}")