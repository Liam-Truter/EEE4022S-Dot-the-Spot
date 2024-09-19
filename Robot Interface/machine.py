from opentrons import robot

class Machine:
    def __init__(self,mode='simulate'):
        self.mode = mode
