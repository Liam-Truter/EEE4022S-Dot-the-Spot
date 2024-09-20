from opentrons import instruments, containers

p10_rack = containers.load('tiprack-10ul', 'A2')
p1000_rack = containers.load('tiprack-1000ul', 'D2')

p10 = instruments.Pipette(axis='b', max_volume=10,tip_racks=p10_rack)
p1000 = instruments.Pipette(axis='a', max_volume=1000,tip_racks=p1000_rack)

plate = containers.load('96-flat', 'B1')
spot = containers.load('96-flat', 'C1')
tube_rack = containers.load('tube-rack-15_50ml', 'C2')

def serial_dilution(water_well, media_well,rows, cols, factor_horizontal=0.1,factor_vertical=0.5):
    volumes = 10
    p10.pick_up_tip(p10_rack.wells('A1'))

    for i in range(3):
        p10.transfer(volumes*2*(1-(factor_horizontal**i)),
                      tube_rack.wells(water_well).bottom(),
                      plate.wells('A'+cols[i]).bottom(),
                      new_tip='never',
                      trash=False)
    for j in range(1,len(rows)):
        for i in range(3):
            p10.transfer(volumes*(1-factor_vertical)/factor_vertical,
                         tube_rack.wells(water_well).bottom(),
                         plate.wells(rows[j]+cols[i]).bottom(),
                         new_tip='never',
                         trash=False)
    for i in range(3):
        p10.transfer(volumes*2*(factor_horizontal**i),
                      tube_rack.wells(media_well).bottom(),
                      plate.wells('A'+cols[i]).bottom(),
                      mix_after=(3,10),
                      new_tip='never',
                      trash=False)
        for j in range(len(rows)-1):
            p10.transfer(volumes,
                         plate.wells(rows[j]+cols[i]).bottom(),
                         plate.wells(rows[j+1]+cols[i]).bottom(),
                         mix_after=(3,10),
                         new_tip='never',
                         trash=False)

def spot_plate(volumes, rows,cols):
    for i in range(len(rows)):
        for j in range(len(cols)):
            p10.transfer(volumes,
                         plate.wells(rows[i]+cols[j]).bottom(),
                         spot.wells(rows[i]+cols[j]).bottom(),
                         new_tip='never',
                         trash=False)

    
rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
cols = ['7', '8', '9']
serial_dilution('A4', 'B4', rows, cols,0.9,0.9)
spot_plate(2,rows,cols)
