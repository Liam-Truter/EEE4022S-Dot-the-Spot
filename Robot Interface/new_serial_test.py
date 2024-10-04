from calibrator import Calibrator
from weight_reader import Weight_reader
from opentrons import robot
from opentrons.util.vector import Vector
import os
import numpy as np

import time

weight_reader = Weight_reader()
weight_reader.connect()

while True:
    weight = weight_reader.get_weight()
    print(f"Weight: {weight:.2f} g")