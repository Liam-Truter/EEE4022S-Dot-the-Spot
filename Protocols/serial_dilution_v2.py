from opentrons import robot, instruments, containers

robot.connect(robot.get_serial_ports_list()[0])

p10_rack = containers.load('tiprack-10ul', 'A2')
p1000_rack = containers.load('tiprack-1000ul', 'D2')

p10 = instruments.Pipette(axis='b', max_volume=10,tip_racks=p10_rack)
p1000 = instruments.Pipette(axis='a', max_volume=1000,tip_racks=p1000_rack)

plate = containers.load('96-flat', 'B1')
tube_rack_2 = containers.load('tube-rack-2ml', 'B2')
tube_rack = containers.load('tube-rack-15_50ml', 'C2')

def serial_dilution(media_well, microbe_well, rows, cols, factor_horizontal=0.1, factor_vertical=0.5):
    global p1000_tip_counter
    volume = 400
    target_wells = []
    for row in range(1,len(rows)):
        for col in range(len(cols)):
            target_wells.append(plate.wells(rows[row] + cols[col]).bottom())

    media_vol = (1-factor_vertical)*volume
    p1000.transfer(media_vol, media_well.bottom(), target_wells, new_tip='never', trash=False)

    target_wells = []
    for col in range(1,len(cols)):
        target_wells.append(plate.wells(rows[0] + cols[col]).bottom())
    
    media_vol = (1-factor_horizontal)*volume
    p1000.transfer(media_vol, media_well.bottom(), target_wells, new_tip='never', trash=False)

    #p1000.drop_tip(p1000_rack.wells(p1000_tip_counter))
    #p1000_tip_counter += 1
    #p1000.pick_up_tip(p1000_rack.wells(p1000_tip_counter))
    p1000.transfer(volume, microbe_well.bottom(), plate.wells(rows[0] + cols[0]).bottom(), new_tip='never', trash=False)
    #p1000.drop_tip(p1000_rack.wells(p1000_tip_counter))
    #p10.pick_up_tip(p10_rack.wells(p10_tip_counter))
    for i in range(len(cols)-1):
        p1000.transfer(factor_horizontal*volume,
                        plate.wells(rows[0] + cols[i]).bottom(),
                        plate.wells(rows[0] + cols[i+1]).bottom(),
                        mix_after=(3,volume),
                        new_tip='never',
                        trash=False)
    for i in range(len(cols)):
        for j in range(len(rows)-1):
            p1000.transfer(factor_vertical*volume,
                            plate.wells(rows[j] + cols[i]).bottom(),
                            plate.wells(rows[j+1] + cols[i]).bottom(),
                            mix_after=(3,volume),
                            new_tip='never',
                            trash=False)

rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
cols = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
p1000_tip_counter = 0
p10_tip_counter = 0

p1000.pick_up_tip(p1000_rack[0])
serial_dilution(tube_rack.wells('A4'), tube_rack_2.wells('A1'), rows, cols[0:4])

p1000.drop_tip(p1000_rack[0])
p1000.pick_up_tip(p1000_rack[1])

serial_dilution(tube_rack.wells('A4'), tube_rack_2.wells('B1'), rows, cols[4:8], 0.2, 0.5)

p1000.drop_tip(p1000_rack[1])
p1000.pick_up_tip(p1000_rack[2])

serial_dilution(tube_rack.wells('A4'), tube_rack_2.wells('C1'), rows, cols[8:12], 0.4, 0.5)

p1000.drop_tip(p1000_rack[2])

