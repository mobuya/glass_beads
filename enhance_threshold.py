import cv2
import numpy as np


def enhance_and_threshold(image, configuration, dilated = False,  threshold_value = 223):
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

    if dilated:
        dilated = cv2.dilate(closing, DILATE_KERNEL_SIZE, iterations=DILATE_ITERATIONS)
        return dilated
    
    smooth_outline = cv2.dilate(closing, np.ones((3, 3), np.uint8), iterations = 1)
    return smooth_outline
