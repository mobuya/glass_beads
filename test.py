import cv2
import numpy as np
import constants

from id_parser import parse_pearl_id_and_view
from prediction import process_object_size
from segmentation import process_images
from find_object import find_artifact_contour
from datetime import datetime
from pixel_per_metric import calculate_ppm
from enhance_threshold import enhance_and_threshold
from config_manager import config_context
import os
import csv



'''
config lives only now inside this scope, have to use it only there


maybde its best that for the config_ctx they just take the path, so that when im in porcess start while reading the separate paths i get the value like thaat without opening the file
'''

path_rsz = 'size_test/ENZFSCH_333_011_A.png'

try:
    with config_context(path_rsz) as config:
        wA, wb = process_object_size([path_rsz], config)
        print(f"The resized pearl value for A is: {wA} and for B: {wb}")
except ValueError as e:
    print(e)

 

'''original_img = cv2.imread(path_original)
resized_img = cv2.imread(path_resized)

print(f"Original pixel numer: {original_img.shape[0] * original_img.shape[1]}")
print(f"Resized pixel numer: {resized_img.shape[0] * resized_img.shape[1]}")

output_resized = process_images([path_resized])
output_original = process_images([path_original])

r_sizeA, _ = process_object_size([path_resized])
o_sizeA, _ = process_object_size([path_original])

print(f"Original pearl size: {o_sizeA}")
print(f"Found size after resizing is: {r_sizeA}")

for id, image in output_resized.items():
    cv2.imwrite('resized_output.png', image)

for id, image in output_original.items():
    cv2.imwrite('orginal_output.png', image)

'''
