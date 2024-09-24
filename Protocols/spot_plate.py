# imports
from opentrons import robot, containers, instruments

robot.connect()

robot.comment(containers.list())

# containers
#plate = containers.load('96-flat', 'C1')
plate2 = containers.load('96-flat', 'C1')
rack = containers.load('tube-rack-15_50ml', 'C2')
tiprack = containers.load('tiprack-10ul', 'A2')

# pipettes
pipette = instruments.Pipette(axis='b',
                               max_volume=10,
                                 tip_racks=[tiprack],
                                 aspirate_speed=200,
                                 dispense_speed=200)

rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
cols = ['1', '2', '3', '4', '5', '6', '7', '8','9', '10','11','12']
wells = []
for row in rows:
    for col in cols:
        wells.append(row+col)

pipette.pick_up_tip()

#pipette.transfer(10, rack.wells('A4'), plate2.wells(*wells),blow_out=True)
for i in range(10):
    pipette.aspirate(10,rack.wells('A4'))
    for j in range(10):
        if 10*i + j > 95:
            break
        pipette.move_to(plate2.wells(wells[10*i+j]).bottom())
        pipette.dispense(1)