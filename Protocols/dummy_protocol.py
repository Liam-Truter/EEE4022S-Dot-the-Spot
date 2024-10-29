from opentrons import instruments, containers

p10_rack = containers.load('tiprack-10ul', 'A2')
p1000_rack = containers.load('tiprack-1000ul', 'D2')

p10 = instruments.Pipette(axis='b', max_volume=10,tip_racks=p10_rack)
p1000 = instruments.Pipette(axis='a', max_volume=1000,tip_racks=p1000_rack)

plate = containers.load('96-flat', 'B1')
tube_rack_2 = containers.load('tube-rack-2ml', 'B2')
tube_rack = containers.load('tube-rack-15_50ml', 'C2')

scale = containers.load('point', 'C1')
scale_plate = containers.load('96-flat', 'D1')

p1000.pick_up_tip(p1000_rack.wells(0))
p1000.move_to(plate.wells(0))
p1000.move_to(tube_rack.wells(0))
p1000.move_to(tube_rack_2.wells(0))

p10.pick_up_tip(p10_rack.wells(0))
p10.move_to(plate.wells(0))
p10.move_to(scale)
p10.move_to(scale_plate.wells(0))