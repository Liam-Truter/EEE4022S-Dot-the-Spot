from opentrons import robot, instruments, containers
from scale import Scale
from opentrons.util.vector import Vector
from pprint import pprint
import numpy as np

robot.connect(robot.get_serial_ports_list()[0])
robot.home()

p10_rack = containers.load('tiprack-10ul', 'A2')
p1000_rack = containers.load('tiprack-1000ul', 'D2')

p10 = instruments.Pipette(axis='b', max_volume=10,tip_racks=p10_rack)
p1000 = instruments.Pipette(axis='a', max_volume=1000,tip_racks=p1000_rack)

p10.pick_up_tip(p10_rack[1])


plate = containers.load('96-flat', 'B1')
tube_rack = containers.load('tube-rack-15_50ml', 'C2')

scalept = containers.load('point', 'C1')
scale_plate = containers.load('96-flat', 'D1')

scale = Scale()
coords = scale.load_coords()

#pprint(coords.tolist())
abs_pos = Vector(coords[0][0][0], coords[0][0][1], np.max(coords[:,:,2]))
rel_pos = scale_plate.wells(0).from_center(x=0, y=0, z=0, reference=scale_plate)

#p10.calibrate_position((scale_plate, rel_pos), abs_pos)
well_a1 = Vector(122.00, 10.00, -53.40)
for row in range(8):
    for col in range(4):
        p10.move_to(plate.wells(row + 8*col).bottom())
        p10.aspirate(10)
        p10.move_to(scale_plate.wells(row+8*col).bottom())
        p10.dispense(10)

p10.drop_tip(p10_rack[1])
p10.pick_up_tip(p10_rack[2])

for row in range(8):
    for col in range(4,8):
        p10.move_to(plate.wells(row + 8*col).bottom())
        p10.aspirate(10)
        p10.move_to(scale_plate.wells(row+8*col).bottom())
        p10.dispense(10)

p10.drop_tip(p10_rack[2])
p10.pick_up_tip(p10_rack[3])

for row in range(8):
    for col in range(8,12):
        p10.move_to(plate.wells(row + 8*col).bottom())
        p10.aspirate(10)
        p10.move_to(scale_plate.wells(row+8*col).bottom())
        p10.dispense(10)

p10.drop_tip(p10_rack[3])