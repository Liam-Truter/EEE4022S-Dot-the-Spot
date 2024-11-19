from opentrons import robot, instruments, containers
from scale import Scale
from opentrons.util.vector import Vector

robot.connect(robot.get_serial_ports_list()[0])
robot.home()

p10_rack = containers.load('tiprack-10ul', 'A2')
p1000_rack = containers.load('tiprack-1000ul', 'D2')

p10 = instruments.Pipette(axis='b', max_volume=10,tip_racks=p10_rack)
p1000 = instruments.Pipette(axis='a', max_volume=1000,tip_racks=p1000_rack)

p10.pick_up_tip(p10_rack[0])


plate = containers.load('96-flat', 'B1')
tube_rack = containers.load('tube-rack-15_50ml', 'C2')

scalept = containers.load('point', 'C1')

scale = Scale()
scale.start()
corner_point = Vector(228.00, 0.00, -9.00)
scale.calibrate(corner_point)
scale.touch_corners()
scale.make_plane()
scale.save_coords()
p10.drop_tip(p10_rack[0])