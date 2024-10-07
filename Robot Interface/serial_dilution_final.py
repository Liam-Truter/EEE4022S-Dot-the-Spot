from opentrons import robot, instruments, containers
from scale import Scale
from opentrons.util.vector import Vector

p10_rack = containers.load('tiprack-10ul', 'A2')
p1000_rack = containers.load('tiprack-1000ul', 'D2')

p10 = instruments.Pipette(axis='b', max_volume=10,tip_racks=p10_rack)
p1000 = instruments.Pipette(axis='a', max_volume=1000,tip_racks=p1000_rack)

p10.calibrate_position()

plate = containers.load('96-flat', 'B1')
tube_rack = containers.load('tube-rack-15_50ml', 'C2')

scale = Scale()
corner_point = Vector(233.00, 0.00, -5.00)
scale.calibrate(corner_point)