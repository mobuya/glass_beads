import cv2
import numpy as np
import constants


# constants
 
'''
MORPH_KERNEL_SIZE = constants.CONFIGURATION["MORPH_KERNEL_SIZE"]   # used to be 5  5
MORPH_ITERATIONS = constants.CONFIGURATION["MORPH_ITERATIONS"] #  2 works very well with 9 9 
DILATE_KERNEL_SIZE = constants.CONFIGURATION["DILATE_KERNEL_SIZE"]   # used to be 5 , 5  i put 2 2 only for size predicstions
DILATE_ITERATIONS = constants.CONFIGURATION["DILATE_ITERATIONS"]
'''

def enhance_and_threshold(image, configuration, threshold_value = 223):
    # original ist 7952x5304
    MORPH_KERNEL_SIZE = configuration["MORPH_KERNEL_SIZE"]
    MORPH_ITERATIONS = configuration["MORPH_ITERATIONS"]
    DILATE_KERNEL_SIZE = configuration["DILATE_KERNEL_SIZE"]
    DILATE_ITERATIONS = configuration["DILATE_ITERATIONS"]
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  

    img = cv2.medianBlur(gray, 5)   

    _, th_test = cv2.threshold(img, threshold_value,255,cv2.THRESH_BINARY_INV)  

    img = cv2.medianBlur(th_test, 15)  

    closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, MORPH_KERNEL_SIZE, iterations=MORPH_ITERATIONS) 

    dilated = cv2.dilate(closing, DILATE_KERNEL_SIZE, iterations=DILATE_ITERATIONS)

    return dilated

