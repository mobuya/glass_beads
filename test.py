import numpy as np
from prediction import process_object_size
from datetime import datetime
from config_manager import config_context


path_rsz = 'size_test/ENZFSCH_333_011_A.png'

try:
    with config_context(path_rsz) as config:
        wA, wb = process_object_size([path_rsz], config)
        print(f"The resized pearl value for A is: {wA} and for B: {wb}")
except ValueError as e:
    print(e)

 