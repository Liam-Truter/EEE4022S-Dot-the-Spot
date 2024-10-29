from opentrons import robot
import numpy as np
import time

robot.connect(robot.get_serial_ports_list()[0])
robot.home()
#robot.move_head(x=50)
print("Head Speed\tTime")
for i in range(int((21000-5000)/500+1)):
    head_speed = 5000 + 500*i
    robot.head_speed(head_speed)
    start = time.time()
    robot.move_head(x=100)
    end=time.time()
    duration = end-start
    print(f"{duration}")
    robot.head_speed(5000)
    robot.move_head(x=0)